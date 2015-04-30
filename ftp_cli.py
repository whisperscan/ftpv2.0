#
#		writed by caramel 
#

import os
import sys
import getpass
import platform
from socket import *
import time

# A global varible for connecting server
sockfd = socket(AF_INET,SOCK_STREAM)
global_dir_name = 'FTP > '

#-- connect server --

def starting_server():
#{
	
	ADDR,PORT = 'localhost',50001
	
	
	try:
		sockfd.connect((ADDR,PORT))
		print 'Connected server'

	except Exception,e:
		print e
	
#}

#-- ending server --

def ending_server():
#{

	if(sockfd):
		sockfd.close()

#}


#-- send message --

def send_msg(msg):
#{
	
	if(sockfd):
		sockfd.sendall(msg)

#}

#-- receive message --

def rcv_msg():
#{

	if(sockfd):
	#{
		ret_msg = sockfd.recv(65535)
		if(ret_msg):
		#{
			return(ret_msg)
		#}
	#}
#}

#-- format message --

def fmt_msg(msg_string):
#{

	msg_dict = {}
	if(msg_string):
	#{
		for i in range(1,len(msg_string),2):
		#{
			msg_dict[msg_string[i]] = msg_string[i + 1]
		#}
	#}

	return(msg_dict)

#}



#-- input and format information --

def input_info_fmt(option):
#{

	username = raw_input(' username: ').strip()
	password = getpass.getpass(' password: ').strip()
	format_string = 'R,option,'+ option + ',username,' + username + ',password,' + password
	return(format_string)

#}

#-- show usage --

def show_usage():
#{
	i = os.system('clear')	
	
	print '''#-------------------------------------------------------------------------------------------
				<Welcome to Caramel's FTP>
<
	You use the two function about getfile and putfile, and it usage as following,
    and you can enter 'help' to show some help information or enter 'q/Q' to quit.
	
>
	
'''
#}

#-- help --

def help_func():
#{
	print '''getfile:
		getfile <filename>
		 
	putfile:
		putfile <filename>


	ls - list the server dictionary

	ll - list the local dictionary
	'''
#}


#-- logined process --

#-- get command --

def get_cmd():
#{
	while True:
	#{
		cmd_string = raw_input(global_dir_name)
		if(len(cmd_string) > 0):
		#{
			break
		#}
	#}

	return(cmd_string)
#}

#-- escape null--

def escape_null(cmd_string):
#{
	cmd_list = cmd_string.split(' ')

	while True:
	#{
		list_olen = len(cmd_list)
		try:
		#{
			cmd_list.remove('')
		#}
		except:
		#{
			pass
			break
		#}
		list_nlen = len(cmd_list)
		if(list_olen == list_nlen):
		#{
			break
		#}
	#}
	return(cmd_list)
#}


#-- list file on local --

def list_file_on_local():
#{
	sysInfo = platform.system()
	if((sysInfo == 'Linux') or (sysInfo == 'Darwin')):
	#{
		list_fd = os.popen('ls')
		list_result = list_fd.read()
		print list_result
	#}
	elif(sysInfo == 'Windows'):
	#{
		for each_file in os.listdir('d:\\download'):
		#{
			print each_file
		#}
	#}
#}


#-- seek file on local --

def seek_file_on_local(filename):
#{
	isExists = os.path.exists(filename)
	if(isExists):
	#{
		return(1)
	#}
	else:
	#{
		return(0)
	#}
#}


#-- get file from server --

def get_file(filename):
#{
	if(filename):
	#{
		send_string = 'R,option,S,filename,' + filename
		send_msg(send_string)

		rcv_string = rcv_msg().split(',')
		if((rcv_string[0] == 'A') and (rcv_string[4] == '1')):
		#{
			send_string = 'R,option,begin,filename,'+ filename
			send_msg(send_string)
			with open(filename,'wb') as dl_file_fd:
			#{
				while True:
				#{
					rcv_buff = rcv_msg()
					if((rcv_buff == 'null') or (rcv_buff == 'EOF')):
					#{
						break
					#}
					dl_file_fd.write(rcv_buff)
				#}
			#}

			if(rcv_buff == 'null'):
			#{
				os.remove(filename)
			#}	
		#}
		else:
		#{
			print ' Error: file not exists' 
		#}	
	#}
#}

#-- put file to server --

def put_file(filename):
#{
	if(seek_file_on_local(filename)):
	#{
		send_string = 'R,option,put,filename,' + filename
		send_msg(send_string)

		rcv_string = rcv_msg()
		if(rcv_string == 'begin'):
		#{
			with open(filename,'rb') as put_file_fd:
			#{
				read_buff = put_file_fd.read()
				send_msg(read_buff)
			#}
			time.sleep(1)
			send_msg('EOF')
		#}
	#}
	else:
	#{
		print ' Error: error file name'
	#}
#}

#-- show server list --

def show_file_list(cmd_string):
#{
	send_string = 'R,option,ls,cmd,'+ cmd_string
	send_msg(send_string)

	rcv_string = rcv_msg()

	print rcv_string
#}

#-- create a new dictionary

def mk_dir(dir_name):
#{
	if(dir_name):
	#{
		send_string = 'R,option,mkdir,dir_name,' + dir_name
		send_msg(send_string)

		result = rcv_msg().split(',')
		if((result[0] == 'A') and (result[4] == '1')):
		#{
			print ' create directory success'
		#}
		else:
		#{
			print ' directory is exists'
		#}
	#}
	else:
	#{
		print ' directory name is null'
	#}
#}

#-- enter a directory --

def cd_dir(dir_name):
#{
	if(dir_name):
	#{
		send_string = 'R,option,cd,dir_name,' + dir_name
		send_msg(send_string)

		result = rcv_msg().split(',')
		if((result[0] == 'A') and (result[4] == '1')):
		#{
			global global_dir_name 
			global_dir_name = dir_name + ' > '
		#}	
	#}
	else:
	#{
		print ' directory name is null'
	#}
#}


#-- process command --

def main_pro():
#{
	i = os.system('clear')
	
	#show welcome and help information
	show_usage()

	while True:
	#{
		#get operating
		cmd_string = get_cmd()
		#split the command and escape null string
		cmd_list = escape_null(cmd_string)
		
		if((cmd_list[0] == 'q') or (cmd_list[0] == 'Q')):
		#{
			sys.exit(0)
		#}
		elif(cmd_list[0] == 'help'):
		#{
			help_func()
		#}
		elif(cmd_list[0] == 'ls'):#list file on server directionary
		#{
			show_file_list(cmd_string)
		#}
		elif(cmd_list[0] == 'll'):#list file on local directionary
		#{
			list_file_on_local()
		#}
		elif(cmd_list[0] == 'getfile'):
		#{
			if(len(cmd_list) > 1):
			#{
				get_file(cmd_list[1])
			#}
			else:
			#{
				print ' Error: error command - usage: getfile <filename>'
			#}
		#}
		elif(cmd_list[0] == 'putfile'):
		#{
			if(len(cmd_list) > 1):
			#{
				put_file(cmd_list[1])
			#}
			else:
			#{
				print ' Error: error command - usage: putfile <filename>'
			#}
		#}
		elif(cmd_list[0] == 'mkdir'):
		#{
			if(len(cmd_list) > 1):
			#{
				mk_dir(cmd_list[1])
			#}
			else:
			#{
				print ' Error: error command - usage: mkdir <directory>'
			#}
		#}
		elif(cmd_list[0] == 'cd'):
		#{
			if(len(cmd_list) > 1):
			#{
				cd_dir(cmd_list[1])
			#}
			else:
			#{
				print ' Error: error command - usage: cd <directory>'
			#}
		#}
		else:
		#{
			print ' Error: error command'
		#}
	#}
#}

#-- main function --
# begin main()

if __name__ == '__main__':
#{
	starting_server()

	#judge operating system
	sysInfo = platform.system()
	#print sysInfo
	#time.sleep(3)
	if(sysInfo == 'Linux'):
	#{
		homeDir = os.environ['HOME']
		os.chdir(homeDir)
		isExists = os.path.exists('download')
		if(not isExists):
		#{
			os.mkdir('download')
		#}
		os.chdir('download')
	#}
	elif(sysInfo == 'Windows'):
	#{
		pathString = 'd:\\download'
		isExists = os.path.exists(pathString)
		if(not isExists):
		#{
			os.mkdir(pathString)
		#}
		os.chdir(pathString)
	#}
	elif(sysInfo == 'Darwin'):
	#{
		homeDir = os.environ['HOME']
		os.chdir(homeDir)
		os.mkdir('cd /Documents')
		isExists = os.path.exists('download')
		if(not isExists):
		#{
			os.mkdir('download')
		#}
		os.chdir('download')
	#}
	else:
	#{
		print 'system unknown'
		time.sleep(3)
		sys.exit(0)
	#}

	main_pro()

	ending_server()
#}
# end main()
