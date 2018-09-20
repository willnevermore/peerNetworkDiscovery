#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket, time
#import schedule
import threading

class NodeDiscover:
    def __init__(self,bradcast_port):
        self.bradcast_port = bradcast_port
        self.recv_port = bradcast_port
        self.send_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        self.dest = ('<broadcast>', self.bradcast_port)
        self.recv_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.recv_s.bind(('0.0.0.0',self.recv_port))
        self.liveCheckList = set()
        self.iplist = set()
        self.connectNum=0
        self.__online = False
        self.__getNodeFunc = None
        self.__lostNodeFunc = None
        return
    def startOnline(self):
        self.__online = True
        return
    def stopOnline(self):
        self.__online = False
        return
    def registGetNewNodeCallback(self,fun=None):
        self.__getNodeFunc = fun
        return
    def registLostNodeCallback(self,fun=None):
        self.__lostNodeFunc = fun
        return
    def run(self):
        self.startOnline()
        self.__sendBradcast("peer node add")
        #schedule.every(LiveInterval).seconds.do()
        threading.Thread(target=self.__do_handler).start()
        return
    def __liveTest(self):
        return
    def getNodeList(self):
        return self.iplist
    def getNodeListLen(self):
        return self.iplist.__len__()
    def delNode(self,addres):
        self.iplist.remove(addres)
    def delNodeBroadcast(self,address):
        self.iplist.remove(address)
        self.__sendBradcast("peer node remove")
    def __sendBradcast(self,cmdStr):
        self.send_s.sendto(cmdStr.encode('UTF-8'), self.dest)
        return
    def __do_handler(self):
        while(self.__online):
            data, address = self.recv_s.recvfrom(1024)
            if str(data).find("peer node add") != -1:
                if address[0] in self.iplist:
                    self.liveCheckList.add(address[0])
                else:
                    self.__sendBradcast("peer node add")
                    self.iplist.add(address[0])
                    if self.__getNodeFunc != None:
                        self.__getNodeFunc(address[0])
            if str(data).find("peer node remove") != -1:
                if address[0] in self.iplist:
                    self.iplist.remove(address[0])
                    if self.__lostNodeFunc != None:
                        self.__lostNodeFunc(address[0])
        return
    def __del__(self):
        return

#test unit
# def get_new_node(ip):
#     print("get new node {}".format(ip))
# ds = NodeDiscover(6464)
# ds.registGetNewNodeCallback(get_new_node)
# ds.run()



