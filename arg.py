# importing the required modules
import os
import argparse
import psutil
import sys
import time
from time import strftime
from time import gmtime

def getAllTopProcess():
    '''
    Get list of running process sorted by Memory Usage
    '''
    process_list = []
    # Iterate over the list
    for process in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = process.as_dict(attrs=['pid', 'name', 'username'])
            pinfo['vms'] = process.memory_info().vms / (1024 * 1024)
            # Append dict to list
            process_list.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Sort list of dict by key vms i.e. memory usage
    process_list = sorted(process_list, key=lambda procObj: procObj['vms'], reverse=True)

    return process_list

def cpu_utilization():
    print('Cpu Utilization in %',psutil.cpu_percent())

def memory_utilization():
    print('memory % used:', psutil.virtual_memory()[2])

# def convert_to_gbit(value):
#     return value/1024./1024./1024.*8

def convert_to_gbit(bytes, to, bsize=1024):

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return(r)

def network_stats():
    upload = convert_to_gbit(psutil.net_io_counters().bytes_sent,'m')
    down=convert_to_gbit(psutil.net_io_counters().bytes_recv,'m')
    print("upload in mb: %0.3f Download stats in mb: %0.3f "%(upload,down))

def disk_utilization():
    disk_percent = psutil.disk_usage('/')[3]
    print("disk_percent is %s percent.  " % disk_percent)


def getProcessbylimit(limit=5):

    process = getAllTopProcess()[:limit]
    for proc in process:
        print(proc)

def getUpTime():
    print('System Uptime in Standard format',strftime("%H:%M:%S", gmtime(time.time() -psutil.boot_time())))

def followAction(arguments=None):
    refreshAction(arguments=arguments)


def refreshAction(arguments=None):
    count = 0
    sec = arguments.refresh[0] if arguments.refresh != None else 3
    while True:
        try:
            cpu_utilization()
            memory_utilization()
            network_stats()
            getUpTime()
            if arguments.limit:
                getProcessbylimit(limit=args.limit[0])
            else:
                getProcessbylimit()
            if not arguments.follow and count ==1:
                exit()
            else:
                time.sleep(sec)
            count +=1
        except KeyboardInterrupt:
            print('All done')
            exit()
            raise


def main():
    # create parser object
    parser = argparse.ArgumentParser(description="A System Administrator Program")

    # defining arguments for parser object
    parser.add_argument("-l", "--limit", type=int, nargs=1,
                        metavar="number", default=None,
                        help="Omit number of process")
    parser.add_argument("-f", "--follow", default=None,action="store_true",)
    parser.add_argument("-r", "--refresh", type=int, nargs=1,
                        metavar="number", default=None,
                        help="refresh the screen after given second and exit")



    if len(sys.argv) == 1:
        cpu_utilization()
        memory_utilization()
        network_stats()
        getUpTime()
        getProcessbylimit()
        exit()


    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.limit != None:
        cpu_utilization()
        memory_utilization()
        network_stats()
        getUpTime()
        getProcessbylimit(limit=args.limit[0])
    if args.follow != None:
        followAction(arguments=args)
    if args.refresh != None:
        refreshAction(arguments=args)


if __name__ == "__main__":
    # calling the main function
    main()