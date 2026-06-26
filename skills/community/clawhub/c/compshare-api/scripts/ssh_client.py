#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CompShare SSH 客户端脚本

通过实例的 SshLoginCommand 和 Password 进行 SSH 连接，支持文件传输和远程操作

依赖: paramiko
"""

import os
import sys
import json
import re
import argparse
import stat
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

try:
    import paramiko
    from paramiko import SSHClient, SFTPClient, AutoAddPolicy
except ImportError:
    print("Error: paramiko is required. Install with: pip install paramiko")
    sys.exit(1)


def parse_ssh_login_command(ssh_command: str) -> Tuple[str, int, str]:
    """
    解析 SSH 登录命令，提取主机、端口和用户名
    
    Args:
        ssh_command: SSH 登录命令，如 "ssh -p 12345 root@192.168.1.1"
    
    Returns:
        (host, port, username)
    """
    # 默认值
    port = 22
    username = "root"
    
    # 解析端口: -p <port> 或 -p<port>
    port_match = re.search(r'-p\s*(\d+)', ssh_command)
    if port_match:
        port = int(port_match.group(1))
    
    # 解析用户名和主机: user@host
    user_host_match = re.search(r'(\w+)@([\w\.\-]+)', ssh_command)
    if user_host_match:
        username = user_host_match.group(1)
        host = user_host_match.group(2)
    else:
        # 尝试直接提取IP地址
        ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', ssh_command)
        if ip_match:
            host = ip_match.group(1)
        else:
            raise ValueError(f"无法从命令中解析主机地址: {ssh_command}")
    
    return host, port, username


class CompShareSSHClient:
    """CompShare SSH 客户端"""
    
    def __init__(self, ssh_command: str, password: str):
        """
        初始化 SSH 客户端
        
        Args:
            ssh_command: SSH 登录命令
            password: 登录密码
        """
        self.ssh_command = ssh_command
        self.password = password
        
        # 解析连接信息
        self.host, self.port, self.username = parse_ssh_login_command(ssh_command)
        
        # SSH 和 SFTP 客户端
        self.ssh_client: Optional[SSHClient] = None
        self.sftp_client: Optional[SFTPClient] = None
    
    def connect(self) -> Dict[str, Any]:
        """
        建立 SSH 连接
        
        Returns:
            连接结果
        """
        try:
            self.ssh_client = SSHClient()
            self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
            
            self.ssh_client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=30,
                allow_agent=False,
                look_for_keys=False
            )
            
            return {
                "success": True,
                "message": f"已连接到 {self.username}@{self.host}:{self.port}",
                "host": self.host,
                "port": self.port,
                "username": self.username
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def disconnect(self) -> Dict[str, Any]:
        """
        断开 SSH 连接
        """
        try:
            if self.sftp_client:
                self.sftp_client.close()
                self.sftp_client = None
            
            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None
            
            return {
                "success": True,
                "message": "已断开连接"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _ensure_sftp(self) -> SFTPClient:
        """确保 SFTP 连接已建立"""
        if not self.ssh_client:
            raise RuntimeError("SSH 连接未建立，请先调用 connect()")
        
        if not self.sftp_client:
            self.sftp_client = self.ssh_client.open_sftp()
        
        return self.sftp_client
    
    def execute(self, command: str, timeout: int = 60) -> Dict[str, Any]:
        """
        执行远程命令
        
        Args:
            command: 要执行的命令
            timeout: 超时时间（秒）
        
        Returns:
            执行结果
        """
        if not self.ssh_client:
            return {"success": False, "error": "SSH 连接未建立"}
        
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            
            exit_code = stdout.channel.recv_exit_status()
            stdout_text = stdout.read().decode('utf-8', errors='replace')
            stderr_text = stderr.read().decode('utf-8', errors='replace')
            
            return {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "command": command
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    def list_dir(self, remote_path: str = ".") -> Dict[str, Any]:
        """
        列出远程目录内容
        
        Args:
            remote_path: 远程目录路径
        
        Returns:
            目录内容列表
        """
        try:
            sftp = self._ensure_sftp()
            
            items = []
            for entry in sftp.listdir_attr(remote_path):
                item_type = "directory" if stat.S_ISDIR(entry.st_mode) else "file"
                items.append({
                    "name": entry.filename,
                    "type": item_type,
                    "size": entry.st_size,
                    "permissions": oct(entry.st_mode)[-3:],
                    "modified": entry.st_mtime
                })
            
            return {
                "success": True,
                "path": remote_path,
                "items": items
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": remote_path
            }
    
    def pwd(self) -> Dict[str, Any]:
        """
        获取当前工作目录
        
        Returns:
            当前目录路径
        """
        try:
            sftp = self._ensure_sftp()
            path = sftp.getcwd() or "."
            return {
                "success": True,
                "path": path
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def cd(self, remote_path: str) -> Dict[str, Any]:
        """
        切换远程目录
        
        Args:
            remote_path: 目标目录路径
        
        Returns:
            操作结果
        """
        try:
            sftp = self._ensure_sftp()
            sftp.chdir(remote_path)
            return {
                "success": True,
                "message": f"已切换到目录: {remote_path}",
                "path": sftp.getcwd()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": remote_path
            }
    
    def mkdir(self, remote_path: str) -> Dict[str, Any]:
        """
        创建远程目录
        
        Args:
            remote_path: 目录路径
        
        Returns:
            操作结果
        """
        try:
            sftp = self._ensure_sftp()
            sftp.mkdir(remote_path)
            return {
                "success": True,
                "message": f"已创建目录: {remote_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": remote_path
            }
    
    def rmdir(self, remote_path: str) -> Dict[str, Any]:
        """
        删除远程空目录
        
        Args:
            remote_path: 目录路径
        
        Returns:
            操作结果
        """
        try:
            sftp = self._ensure_sftp()
            sftp.rmdir(remote_path)
            return {
                "success": True,
                "message": f"已删除目录: {remote_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": remote_path
            }
    
    def rm(self, remote_path: str) -> Dict[str, Any]:
        """
        删除远程文件
        
        Args:
            remote_path: 文件路径
        
        Returns:
            操作结果
        """
        try:
            sftp = self._ensure_sftp()
            sftp.remove(remote_path)
            return {
                "success": True,
                "message": f"已删除文件: {remote_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": remote_path
            }
    
    def upload(self, local_path: str, remote_path: str, callback=None) -> Dict[str, Any]:
        """
        上传文件
        
        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径
            callback: 进度回调函数
        
        Returns:
            上传结果
        """
        try:
            sftp = self._ensure_sftp()
            
            local_file = Path(local_path)
            if not local_file.exists():
                return {
                    "success": False,
                    "error": f"本地文件不存在: {local_path}"
                }
            
            file_size = local_file.stat().st_size
            
            sftp.put(str(local_file), remote_path, callback=callback)
            
            return {
                "success": True,
                "message": f"已上传: {local_path} -> {remote_path}",
                "size": file_size
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "local_path": local_path,
                "remote_path": remote_path
            }
    
    def upload_dir(self, local_dir: str, remote_dir: str) -> Dict[str, Any]:
        """
        上传整个目录
        
        Args:
            local_dir: 本地目录路径
            remote_dir: 远程目录路径
        
        Returns:
            上传结果
        """
        try:
            sftp = self._ensure_sftp()
            
            local_path = Path(local_dir)
            if not local_path.exists():
                return {
                    "success": False,
                    "error": f"本地目录不存在: {local_dir}"
                }
            
            # 创建远程目录
            try:
                sftp.mkdir(remote_dir)
            except:
                pass  # 目录可能已存在
            
            uploaded_files = []
            
            for item in local_path.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(local_path)
                    remote_file_path = f"{remote_dir}/{relative_path}".replace("\\", "/")
                    
                    # 确保远程子目录存在
                    remote_subdir = str(Path(remote_file_path).parent).replace("\\", "/")
                    try:
                        self._mkdir_p(sftp, remote_subdir)
                    except:
                        pass
                    
                    sftp.put(str(item), remote_file_path)
                    uploaded_files.append({
                        "local": str(item),
                        "remote": remote_file_path,
                        "size": item.stat().st_size
                    })
            
            return {
                "success": True,
                "message": f"已上传目录: {local_dir} -> {remote_dir}",
                "files_count": len(uploaded_files),
                "files": uploaded_files
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _mkdir_p(self, sftp: SFTPClient, path: str):
        """递归创建目录"""
        dirs = path.split("/")
        current = ""
        for d in dirs:
            if d:
                current += "/" + d
                try:
                    sftp.stat(current)
                except:
                    try:
                        sftp.mkdir(current)
                    except:
                        pass
    
    def download(self, remote_path: str, local_path: str, callback=None) -> Dict[str, Any]:
        """
        下载文件
        
        Args:
            remote_path: 远程文件路径
            local_path: 本地文件路径
            callback: 进度回调函数
        
        Returns:
            下载结果
        """
        try:
            sftp = self._ensure_sftp()
            
            # 确保本地目录存在
            local_file = Path(local_path)
            local_file.parent.mkdir(parents=True, exist_ok=True)
            
            sftp.get(remote_path, str(local_file), callback=callback)
            
            file_size = local_file.stat().st_size
            
            return {
                "success": True,
                "message": f"已下载: {remote_path} -> {local_path}",
                "size": file_size
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "remote_path": remote_path,
                "local_path": local_path
            }
    
    def download_dir(self, remote_dir: str, local_dir: str) -> Dict[str, Any]:
        """
        下载整个目录
        
        Args:
            remote_dir: 远程目录路径
            local_dir: 本地目录路径
        
        Returns:
            下载结果
        """
        try:
            sftp = self._ensure_sftp()
            
            local_path = Path(local_dir)
            local_path.mkdir(parents=True, exist_ok=True)
            
            downloaded_files = []
            
            def download_recursive(rdir, ldir):
                for entry in sftp.listdir_attr(rdir):
                    rfile = f"{rdir}/{entry.filename}".replace("//", "/")
                    lfile = Path(ldir) / entry.filename
                    
                    if stat.S_ISDIR(entry.st_mode):
                        lfile.mkdir(exist_ok=True)
                        download_recursive(rfile, str(lfile))
                    else:
                        sftp.get(rfile, str(lfile))
                        downloaded_files.append({
                            "remote": rfile,
                            "local": str(lfile),
                            "size": entry.st_size
                        })
            
            download_recursive(remote_dir, local_dir)
            
            return {
                "success": True,
                "message": f"已下载目录: {remote_dir} -> {local_dir}",
                "files_count": len(downloaded_files),
                "files": downloaded_files
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def cat(self, remote_path: str) -> Dict[str, Any]:
        """
        查看远程文件内容
        
        Args:
            remote_path: 文件路径
        
        Returns:
            文件内容
        """
        try:
            sftp = self._ensure_sftp()
            
            with sftp.open(remote_path, 'r') as f:
                content = f.read().decode('utf-8', errors='replace')
            
            return {
                "success": True,
                "path": remote_path,
                "content": content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": remote_path
            }
    
    def stat(self, remote_path: str) -> Dict[str, Any]:
        """
        获取文件/目录信息
        
        Args:
            remote_path: 路径
        
        Returns:
            文件信息
        """
        try:
            sftp = self._ensure_sftp()
            
            attr = sftp.stat(remote_path)
            
            return {
                "success": True,
                "path": remote_path,
                "size": attr.st_size,
                "permissions": oct(attr.st_mode)[-3:],
                "modified": attr.st_mtime,
                "is_directory": stat.S_ISDIR(attr.st_mode),
                "is_file": stat.S_ISREG(attr.st_mode)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "path": remote_path
            }
    
    def rename(self, old_path: str, new_path: str) -> Dict[str, Any]:
        """
        重命名文件/目录
        
        Args:
            old_path: 原路径
            new_path: 新路径
        
        Returns:
            操作结果
        """
        try:
            sftp = self._ensure_sftp()
            sftp.rename(old_path, new_path)
            return {
                "success": True,
                "message": f"已重命名: {old_path} -> {new_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def chmod(self, remote_path: str, mode: int) -> Dict[str, Any]:
        """
        修改文件权限
        
        Args:
            remote_path: 文件路径
            mode: 权限模式（八进制，如 0o755）
        
        Returns:
            操作结果
        """
        try:
            sftp = self._ensure_sftp()
            sftp.chmod(remote_path, mode)
            return {
                "success": True,
                "message": f"已修改权限: {remote_path} -> {oct(mode)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def interactive_shell(self):
        """
        启动交互式 Shell
        """
        if not self.ssh_client:
            print("错误: SSH 连接未建立")
            return
        
        import select
        import termios
        import tty
        
        channel = self.ssh_client.invoke_shell()
        
        def posix_shell(chan):
            import sys
            
            # 保存原始终端设置
            oldtty = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                tty.setcbreak(sys.stdin.fileno())
                chan.settimeout(0.0)
                
                while True:
                    r, w, e = select.select([chan, sys.stdin], [], [])
                    if chan in r:
                        try:
                            x = chan.recv(1024)
                            if len(x) == 0:
                                print("\r\n*** 连接已关闭 ***\r\n")
                                break
                            sys.stdout.write(x.decode('utf-8', errors='replace'))
                            sys.stdout.flush()
                        except:
                            pass
                    if sys.stdin in r:
                        x = sys.stdin.read(1)
                        if len(x) == 0:
                            break
                        chan.send(x)
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        
        try:
            posix_shell(channel)
        except KeyboardInterrupt:
            print("\r\n*** 已退出交互式 Shell ***\r\n")


def main():
    parser = argparse.ArgumentParser(
        description="CompShare SSH 客户端 - 通过实例信息连接并管理远程服务器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  连接实例:
    python ssh_client.py connect --ssh-command "ssh -p 12345 root@192.168.1.1" --password "your-password"

  执行命令:
    python ssh_client.py exec --ssh-command "..." --password "..." --cmd "ls -la"

  列出目录:
    python ssh_client.py ls --ssh-command "..." --password "..." --path "/home"

  上传文件:
    python ssh_client.py upload --ssh-command "..." --password "..." --local ./file.txt --remote /home/file.txt

  下载文件:
    python ssh_client.py download --ssh-command "..." --password "..." --remote /home/file.txt --local ./file.txt

  交互式Shell:
    python ssh_client.py shell --ssh-command "..." --password "..."
        """
    )
    
    # 通用参数
    parser.add_argument("--ssh-command", required=True, help="SSH 登录命令，如 'ssh -p 12345 root@192.168.1.1'")
    parser.add_argument("--password", required=True, help="登录密码")
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # connect 命令
    connect_parser = subparsers.add_parser("connect", help="测试SSH连接")
    
    # exec 命令
    exec_parser = subparsers.add_parser("exec", help="执行远程命令")
    exec_parser.add_argument("--cmd", required=True, help="要执行的命令")
    exec_parser.add_argument("--timeout", type=int, default=60, help="超时时间（秒）")
    
    # ls 命令
    ls_parser = subparsers.add_parser("ls", help="列出目录内容")
    ls_parser.add_argument("--path", default=".", help="目录路径")
    
    # pwd 命令
    pwd_parser = subparsers.add_parser("pwd", help="显示当前目录")
    
    # cd 命令
    cd_parser = subparsers.add_parser("cd", help="切换目录")
    cd_parser.add_argument("--path", required=True, help="目标目录")
    
    # mkdir 命令
    mkdir_parser = subparsers.add_parser("mkdir", help="创建目录")
    mkdir_parser.add_argument("--path", required=True, help="目录路径")
    
    # rm 命令
    rm_parser = subparsers.add_parser("rm", help="删除文件")
    rm_parser.add_argument("--path", required=True, help="文件路径")
    
    # rmdir 命令
    rmdir_parser = subparsers.add_parser("rmdir", help="删除空目录")
    rmdir_parser.add_argument("--path", required=True, help="目录路径")
    
    # cat 命令
    cat_parser = subparsers.add_parser("cat", help="查看文件内容")
    cat_parser.add_argument("--path", required=True, help="文件路径")
    
    # stat 命令
    stat_parser = subparsers.add_parser("stat", help="获取文件信息")
    stat_parser.add_argument("--path", required=True, help="文件/目录路径")
    
    # rename 命令
    rename_parser = subparsers.add_parser("rename", help="重命名文件/目录")
    rename_parser.add_argument("--old", required=True, help="原路径")
    rename_parser.add_argument("--new", required=True, help="新路径")
    
    # chmod 命令
    chmod_parser = subparsers.add_parser("chmod", help="修改权限")
    chmod_parser.add_argument("--path", required=True, help="文件路径")
    chmod_parser.add_argument("--mode", required=True, help="权限模式，如 755")
    
    # upload 命令
    upload_parser = subparsers.add_parser("upload", help="上传文件")
    upload_parser.add_argument("--local", required=True, help="本地文件路径")
    upload_parser.add_argument("--remote", required=True, help="远程文件路径")
    
    # upload-dir 命令
    upload_dir_parser = subparsers.add_parser("upload-dir", help="上传目录")
    upload_dir_parser.add_argument("--local", required=True, help="本地目录路径")
    upload_dir_parser.add_argument("--remote", required=True, help="远程目录路径")
    
    # download 命令
    download_parser = subparsers.add_parser("download", help="下载文件")
    download_parser.add_argument("--remote", required=True, help="远程文件路径")
    download_parser.add_argument("--local", required=True, help="本地文件路径")
    
    # download-dir 命令
    download_dir_parser = subparsers.add_parser("download-dir", help="下载目录")
    download_dir_parser.add_argument("--remote", required=True, help="远程目录路径")
    download_dir_parser.add_argument("--local", required=True, help="本地目录路径")
    
    # shell 命令
    shell_parser = subparsers.add_parser("shell", help="启动交互式Shell")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 创建客户端
    client = CompShareSSHClient(args.ssh_command, args.password)
    
    # 连接
    if args.command != "shell":
        result = client.connect()
        if not result["success"]:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(1)
    
    # 执行命令
    result = None
    
    if args.command == "connect":
        result = client.connect()
        if result["success"]:
            client.disconnect()
    
    elif args.command == "exec":
        result = client.execute(args.cmd, args.timeout)
        client.disconnect()
    
    elif args.command == "ls":
        result = client.list_dir(args.path)
        client.disconnect()
    
    elif args.command == "pwd":
        result = client.pwd()
        client.disconnect()
    
    elif args.command == "cd":
        result = client.cd(args.path)
        client.disconnect()
    
    elif args.command == "mkdir":
        result = client.mkdir(args.path)
        client.disconnect()
    
    elif args.command == "rm":
        result = client.rm(args.path)
        client.disconnect()
    
    elif args.command == "rmdir":
        result = client.rmdir(args.path)
        client.disconnect()
    
    elif args.command == "cat":
        result = client.cat(args.path)
        client.disconnect()
    
    elif args.command == "stat":
        result = client.stat(args.path)
        client.disconnect()
    
    elif args.command == "rename":
        result = client.rename(args.old, args.new)
        client.disconnect()
    
    elif args.command == "chmod":
        mode = int(args.mode, 8)
        result = client.chmod(args.path, mode)
        client.disconnect()
    
    elif args.command == "upload":
        result = client.upload(args.local, args.remote)
        client.disconnect()
    
    elif args.command == "upload-dir":
        result = client.upload_dir(args.local, args.remote)
        client.disconnect()
    
    elif args.command == "download":
        result = client.download(args.remote, args.local)
        client.disconnect()
    
    elif args.command == "download-dir":
        result = client.download_dir(args.remote, args.local)
        client.disconnect()
    
    elif args.command == "shell":
        result = client.connect()
        if result["success"]:
            print(f"*** 已连接到 {result['host']}:{result['port']} ***")
            print("*** 按 Ctrl+C 退出交互式 Shell ***\n")
            try:
                client.interactive_shell()
            except KeyboardInterrupt:
                pass
            finally:
                client.disconnect()
    
    # 输出结果
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
