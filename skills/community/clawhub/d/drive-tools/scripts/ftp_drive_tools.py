# -*- coding: utf-8 -*-
import time
import sys
import os
import json
import argparse
import ssl
import socket
import io
from ftplib import FTP, FTP_TLS, error_perm
from typing import Optional, List, Dict, Any, Tuple, Union, BinaryIO, Callable

# Fix stdout encoding issues on some terminals (修复某些终端上的 stdout 编码问题)
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')

class ReusableFTP_TLS(FTP_TLS):
    """FTP_TLS subclass optimized for Session Reuse. (针对 Session Reuse 优化的 FTP_TLS 子类。)"""
    def ntransfercmd(self, cmd: str, rest: Optional[int] = None) -> Tuple[socket.socket, Optional[int]]:
        try:
            self.sock.setblocking(False)
            try:
                # Type of self.sock depends on the state, but usually it's a socket or SSLSocket
                while self.sock.recv(1024): pass
            except: pass
        except: pass
        finally:
            self.sock.setblocking(True)

        conn, size = super().ntransfercmd(cmd, rest)
        if self._prot_p:
            session = getattr(self.sock, 'session', None)
            if session is None and hasattr(self.sock, '_sslobj'):
                session = getattr(self.sock._sslobj, 'session', None)
            conn = self.context.wrap_socket(
                conn, server_hostname=self.host, session=session, do_handshake_on_connect=True
            )
        return conn, size

class ProgressMonitor:
    """
    Utility class for monitoring file transfer progress. Optimized: reduced refresh frequency to improve performance. (用于监控文件传输进度的工具类。已优化：降低刷新频率以提高性能。)
    """
    def __init__(self, filename: str, filesize: int):
        self.filename = filename
        self.filesize = filesize
        self.bytes_transferred = 0
        self.start_time = time.time()
        self.last_update_time = 0.0
        self.last_progress = -1.0

    def update(self, bytes_chunk_size: int) -> None:
        self.bytes_transferred += bytes_chunk_size
        current_time = time.time()
        progress = (self.bytes_transferred / self.filesize) * 100 if self.filesize > 0 else 0
        if (progress - self.last_progress >= 0.1) or (current_time - self.last_update_time >= 0.1) or (self.bytes_transferred == self.filesize):
            elapsed_time = current_time - self.start_time
            speed = self.bytes_transferred / elapsed_time if elapsed_time > 0 else 0
            disp_name = (self.filename[:20] + '..') if len(self.filename) > 22 else self.filename
            line = (
                f"\rTransfer (传输): {disp_name:<22} | "
                f"{progress:6.2f}% | "
                f"{self.bytes_transferred / 1024 / 1024:8.2f}/{self.filesize / 1024 / 1024:8.2f} MB | "
                f"{speed / 1024 / 1024:6.2f} MB/s"
            )
            # Use \r and padding to ensure single line (使用 \r 和填充确保单行显示)
            sys.stdout.write(line.ljust(100))
            sys.stdout.flush()
            
            if self.bytes_transferred == self.filesize:
                sys.stdout.write('\n')
                sys.stdout.flush()

            self.last_update_time = current_time
            self.last_progress = progress

class FTPClient:
    """
    FTP client wrapper class, managing configuration and connection lifecycle. (FTP 客户端包装类，管理配置及连接生命周期。)
    """
    def __init__(self, config_name: Optional[str] = None):
        self.ftp: Optional[Union[FTP, ReusableFTP_TLS]] = None
        self.config: Dict[str, Any] = self._load_config(config_name)
        self.base_path: str = self.config.get('path', '/').rstrip('/') or '/'

    def _get_full_path(self, path: Union[str, os.PathLike]) -> str:
        """Merge requested path with configured base_path. (将请求路径与配置的 base_path 合并。)"""
        path = str(path).replace('\\', '/')
        clean_path = path.lstrip('/')
        full_path = f"{self.base_path}/{clean_path}".replace('//', '/')
        return full_path if full_path.startswith('/') else f"/{full_path}"

    def _load_config(self, name: Optional[str]) -> Dict[str, Any]:
        if not os.path.exists(CONFIG_FILE):
            print(f"Error: Config file not found (错误: 找不到配置文件) {CONFIG_FILE}")
            self._create_template_config()
            sys.exit(1)
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # [New] Support for comments (// or /* */) while preserving URLs ([新增] 支持注释)
            import re
            pattern = r'("(?:\\.|[^"\\])*")|//[^\r\n]*|/\*.*?\*/'
            content = re.sub(pattern, lambda m: m.group(1) if m.group(1) else '', content, flags=re.DOTALL)
            data = json.loads(content)
            ftp_configs: List[Dict[str, Any]] = data.get('ftp', [])
            if not ftp_configs:
                print("Warning: No 'ftp' configuration found in config.json. Automatically adding template... (警告: config.json 中没有 'ftp' 配置。正在自动添加模板...)")
                self._create_template_config(existing_data=data)
                sys.exit(1)

            # [New] Duplicate name validation ([新增] 重名校验)
            names_seen = set()
            for cfg in ftp_configs:
                cfg_name = cfg.get('name')
                if cfg_name in names_seen:
                    print(f"Error: Duplicate name '{cfg_name}' found in FTP configs, please fix config.json (错误: 在 FTP 配置中发现重复的名称 '{cfg_name}'，请修正 config.json)。")
                    sys.exit(1)
                names_seen.add(cfg_name)
            if name:
                for cfg in ftp_configs:
                    if cfg.get('name') == name: return cfg
                print(f"Error: Configuration '{name}' not found (错误: 未找到名为 '{name}' 的配置)。")
                sys.exit(1)
            return ftp_configs[0]

    def _create_template_config(self, existing_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Automatically create or supplement a template file. (当配置文件不存在或缺少配置项时，自动创建或补充模板文件。)
        """
        ftp_template = [
            {
                "name": "example",
                "user": "your_user",
                "password": "your_password",
                "ip": "192.168.1.100",
                "port": 21,
                "tls": True,
                "path": "/"
            }
        ]
        
        if existing_data is not None:
            existing_data['ftp'] = ftp_template
            final_data = existing_data
            message = "FTP template has been added to the existing config.json. Please configure it and try again. (FTP 模板已添加到现有的 config.json 中，请配置后重试。)"
        else:
            final_data = {"ftp": ftp_template}
            message = "A template config.json has been generated in the current directory, please configure it and try again (已为您在当前目录下生成 config.json 模板，请配置后重试)。"

        print(message)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

    def _create_context(self) -> ssl.SSLContext:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        if hasattr(ssl, 'TLSVersion'):
            context.minimum_version = ssl.TLSVersion.TLSv1_2
            context.maximum_version = ssl.TLSVersion.TLSv1_2
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context

    def connect(self, timeout: int = 60) -> Union[FTP, ReusableFTP_TLS]:
        """
        Establish FTP connection with support for various handshakes (TLS/ClearText) and auto-fallback. (建立 FTP 连接，支持多种握手顺序（TLS/明文）及自动回退逻辑。)
        
        :param timeout: Connection timeout in seconds (连接超时时间，秒).
        :return: Active FTP object on success (成功建立的 FTP 对象).
        
        Example (CLI):
            python ftp_drive_tools.py --name test ls /
        """
        host = self.config.get('host') or self.config.get('ip')
        port = self.config.get('port', 21)
        user = self.config.get('user', 'anonymous')
        password = self.config.get('password', '')
        use_tls = self.config.get('tls', True)
        
        print(f"Connecting (正在建立 FTP 连接) [{self.config.get('name', 'default')}] -> {host}:{port}...")
        
        if use_tls:
            try:
                self.ftp = ReusableFTP_TLS(context=self._create_context())
                self.ftp.encoding = 'utf-8'
                self.ftp.connect(host, port, timeout=timeout)
                try: self.ftp.auth()
                except: pass
                self.ftp.login(user, password)
                try:
                    self.ftp.prot_p()
                    time.sleep(0.3)
                except: pass
                self.ftp.set_pasv(True)
                # Change to the base path (切换到基础路径)
                try: self.ftp.cwd(self.base_path)
                except: pass
                print(f"Encrypted connection established successfully (成功建立加密连接) (Initial path/初始路径: {self.base_path})。")
                return self.ftp
            except Exception as e:
                # 530 error handling logic remains unchanged (530 错误处理逻辑保持不变)
                if "530" in str(e):
                    if self.ftp:
                        try: self.ftp.quit()
                        except: pass
                    time.sleep(0.5)
                else: print(f"Encrypted connection failed, please check your drive configuration (加密模式连接失败，请检查云盘配置信息) (Reason/原因: {e})")

        try:
            self.ftp = ReusableFTP_TLS(context=self._create_context()) if use_tls else FTP()
            self.ftp.encoding = 'utf-8'
            self.ftp.connect(host, port, timeout=timeout)
            self.ftp.login(user, password)
            if use_tls:
                try:
                    self.ftp.auth()
                    self.ftp.prot_p()
                except: pass
            self.ftp.set_pasv(True)
            try: self.ftp.cwd(self.base_path)
            except: pass
            print(f"Connection established successfully (成功建立连接) (Mode/模式: {'TLS' if use_tls else 'ClearText'}，Initial path/初始路径: {self.base_path})。")
            return self.ftp
        except Exception as e:
            print(f"Connection failed: Please check your drive configuration (连接失败：请检查云盘配置信息) {host} (Reason/原因: {e})")
            sys.exit(1)

    def close(self) -> None:
        """
        Close the current FTP connection. (关闭当前的 FTP 连接。)
        
        Example (CLI):
            python ftp_drive_tools.py --name test ls /
        """
        if self.ftp:
            try: self.ftp.quit()
            except: self.ftp.close()

    def list_dir(self, path: str = '/') -> None:
        """
        List files and directories in the remote path, preferring MLSD. (列出远程目录下的文件和文件夹，优先使用 MLSD。)
        
        :param path: Remote directory path (远程目录路径).
        
        Example (CLI):
            python ftp_drive_tools.py --name test ls /Movies
        """
        try:
            full_path = self._get_full_path(path)
            print(f"\nDirectory Listing (目录列表) [{full_path}]:")
            col_format = "{:<50} {:<20} {:<15}"
            print(col_format.format("Name (名称)", "Modify Date (修改日期)", "Size (大小)"))
            print("-" * 88)
            
            try:
                has_results = False
                for name, facts in self.ftp.mlsd(full_path):
                    if name in ['.', '..']: continue
                    has_results = True
                    raw_date = facts.get('modify', '')
                    if len(raw_date) >= 12:
                        date_str = f"{raw_date[0:4]}-{raw_date[4:6]}-{raw_date[6:8]} {raw_date[8:10]}:{raw_date[10:12]}"
                    else:
                        date_str = raw_date or "N/A"
                    
                    size_bytes = int(facts.get('size', 0))
                    size_str = f"{size_bytes / 1024 / 1024:,.2f} MB" if size_bytes > 0 else "DIR (目录)"
                    print(col_format.format(name, date_str, size_str))
                if not has_results: print("(Empty directory / 空目录)")
            except:
                lines = []
                self.ftp.retrlines(f'LIST {full_path}', lines.append)
                for line in lines:
                    parts = line.split(None, 8)
                    if len(parts) >= 9:
                        size_raw = parts[4]
                        date_str = f"{parts[5]} {parts[6]} {parts[7]}"
                        name = parts[8]
                        try:
                            s_val = int(size_raw)
                            size_display = f"{s_val / 1024 / 1024:,.2f} MB" if s_val > 0 else "0.00 MB"
                        except: size_display = size_raw
                        if line.startswith('d'): size_display = "DIR (目录)"
                        print(col_format.format(name, date_str, size_display))
        except Exception as e:
            print(f"List directory failed (列出目录失败): {e}")

    def upload(self, local_path: str, remote_path: str) -> None:
        """
        Upload a local file to the FTP server. (上传本地文件到 FTP 服务器。)
        
        :param local_path: Source local file path (本地文件路径).
        :param remote_path: Target remote path, including filename (目标远程路径，需包含文件名).
        
        Example (CLI):
            python ftp_drive_tools.py --name test put ./config.zip /backup/config.zip
        """
        try:
            full_remote_path = self._get_full_path(remote_path)
            filesize = os.path.getsize(local_path)
            monitor = ProgressMonitor(os.path.basename(local_path), filesize)
            with open(local_path, 'rb') as f:
                def callback(chunk): monitor.update(len(chunk))
                self.ftp.storbinary(f'STOR {full_remote_path}', f, callback=callback)
            print(f"\nUpload success (上传成功): {local_path} -> {full_remote_path}")
        except Exception as e:
            print(f"\nUpload failed (上传失败): {e}")

    def download(self, remote_path: str, local_path: str) -> None:
        """
        Download a file from the FTP server to the local path. (从 FTP 服务器下载文件到本地。)
        
        :param remote_path: Source remote file path (远程源文件路径).
        :param local_path: Target local file path (本地保存路径).
        
        Example (CLI):
            python ftp_drive_tools.py --name test get /data/logs.tar.gz ./logs.tar.gz
        """
        try:
            full_remote_path = self._get_full_path(remote_path)
            filesize = 0
            try: filesize = self.ftp.size(full_remote_path)
            except: pass
            monitor = ProgressMonitor(os.path.basename(remote_path), filesize or 1)
            with open(local_path, 'wb') as f:
                def callback(chunk):
                    f.write(chunk)
                    monitor.update(len(chunk))
                self.ftp.retrbinary(f"RETR {full_remote_path}", callback)
            print(f"\nDownload success (下载成功): {full_remote_path} -> {local_path}")
        except Exception as e:
            print(f"\nDownload failed (下载失败): {e}")

    def mkdir(self, path: str) -> None:
        """
        Create a new directory on the FTP server. (在服务器上创建目录。)
        
        :param path: Remote directory path to create (待创建的远程路径).
        """
        try:
            full_path = self._get_full_path(path)
            self.ftp.mkd(full_path)
            print(f"Create directory success (创建目录成功): {full_path}")
        except Exception as e:
            # If directory already exists, error 550 is common and can be ignored (如果目录已存在，550 错误通常是正常的，可以忽略)
            if "550" in str(e):
                pass
            else:
                print(f"Create directory failed (创建目录失败): {e}")

    def delete(self, path: str, is_dir: bool = False, recursive: bool = False) -> None:
        """
        Delete a file or directory on the FTP server. (删除服务器上的文件或目录。)
        
        :param path: Remote path to delete (远程路径).
        :param is_dir: True if target is a directory (是否为目录).
        :param recursive: If True, delete non-empty directory recursively (如果是 True，则递归删除非空目录).
        """
        try:
            full_path = self._get_full_path(path)
            if is_dir:
                if recursive:
                    self._delete_recursive(full_path)
                else:
                    self.ftp.rmd(full_path)
            else:
                self.ftp.delete(full_path)
            print(f"Delete success (删除成功): {full_path}")
        except Exception as e:
            print(f"Delete failed (删除失败): {e}")

    def _delete_recursive(self, full_path: str) -> None:
        """Internal helper for recursive deletion. (递归删除的内部辅助方法。)"""
        try:
            for name, facts in self.ftp.mlsd(full_path):
                if name in ['.', '..']: continue
                item_path = f"{full_path}/{name}".replace('//', '/')
                if facts.get('type') == 'dir':
                    self._delete_recursive(item_path)
                else:
                    self.ftp.delete(item_path)
        except:
            # Fallback for servers not supporting MLSD (为不支持 MLSD 的服务器提供回退)
            lines = []
            self.ftp.retrlines(f'LIST {full_path}', lines.append)
            for line in lines:
                parts = line.split(None, 8)
                if len(parts) >= 9:
                    name = parts[8]
                    if name in ['.', '..']: continue
                    item_path = f"{full_path}/{name}".replace('//', '/')
                    if line.startswith('d'):
                        self._delete_recursive(item_path)
                    else:
                        self.ftp.delete(item_path)
        self.ftp.rmd(full_path)

    def upload_dir(self, local_path: str, remote_path: str) -> None:
        """
        Recursively upload a local directory to the FTP server. (递归上传本地目录到 FTP 服务器。)
        
        :param local_path: Local directory path (本地目录路径).
        :param remote_path: Target remote directory path (目标远程目录路径).
        """
        try:
            if not os.path.isdir(local_path):
                print(f"Error: {local_path} is not a directory (错误: {local_path} 不是目录)。")
                return
            
            # Ensure target root dir exists (确保目标根目录存在)
            self.mkdir(remote_path)
            
            for root, dirs, files in os.walk(local_path):
                rel_path = os.path.relpath(root, local_path)
                if rel_path == '.':
                    target_dir = remote_path
                else:
                    target_dir = f"{remote_path}/{rel_path}".replace('\\', '/').replace('//', '/')
                
                for d in dirs:
                    sub_dir = f"{target_dir}/{d}".replace('//', '/')
                    self.mkdir(sub_dir)
                
                for f in files:
                    local_f = os.path.join(root, f)
                    remote_f = f"{target_dir}/{f}".replace('//', '/')
                    self.upload(local_f, remote_f)
            
            print(f"Directory upload completed (目录上传已完成): {local_path} -> {remote_path}")
        except Exception as e:
            print(f"Directory upload failed (目录上传失败): {e}")

    def rename(self, old_path: str, new_path: str) -> None:
        """
        Rename or move a file or directory on the FTP server. (重命名或移动服务器上的文件或目录。)
        
        :param old_path: Source remote path (原路径).
        :param new_path: Target remote path (新路径).
        
        Example (CLI):
            python ftp_drive_tools.py --name test mv /old_name.txt /new_name.txt
        """
        try:
            full_old = self._get_full_path(old_path)
            full_new = self._get_full_path(new_path)
            self.ftp.rename(full_old, full_new)
            print(f"Rename success (重命名成功): {full_old} -> {full_new}")
        except Exception as e:
            print(f"Rename failed (重命名失败): {e}")

    def search(self, path: str, keyword: str) -> None:
        """
        Recursively search for files or folders containing the keyword under path. (递归搜索指定目录下包含关键字的文件或文件夹。)
        
        :param path: Starting path for search (搜索起始路径).
        :param keyword: Keyword to search for (搜索关键字).
        
        Example (CLI):
            python ftp_drive_tools.py --name test find backup --path /
        """
        try:
            full_path = self._get_full_path(path)
            self._search_recursive(full_path, keyword)
        except: pass

    def _search_recursive(self, full_path: str, keyword: str) -> None:
        """Recursive search helper. (递归搜索辅助。)"""
        try:
            for name, facts in self.ftp.mlsd(full_path):
                if name in ['.', '..']: continue
                current_full_path = f"{full_path}/{name}".replace('//', '/')
                if keyword.lower() in name.lower():
                    print(f"[Match (匹配)] {current_full_path}")
                if facts.get('type') == 'dir':
                    self._search_recursive(current_full_path, keyword)
        except: pass

def main() -> None:
    """
    CLI entry function, parses command line arguments and calls FTPClient methods. (CLI 入口函数，负责解析命令行参数并调用 FTPClient 对应方法。)
    """
    parser = argparse.ArgumentParser(description="FTP Drive Tools CLI (FTP 驱动工具命令行版)")
    parser.add_argument("--name", help="Connection name in config.json (配置文件中的连接名称)", default=None)
    
    subparsers = parser.add_subparsers(dest="command", help="Subcommands (子命令)")

    # test
    test_parser = subparsers.add_parser("test", help="Test connection (测试连接)")
 
    # ls
    ls_parser = subparsers.add_parser("ls", help="List directory (列出目录)")
    ls_parser.add_argument("path", nargs="?", default="/", help="Remote path (路径)")
 
    # put
    put_parser = subparsers.add_parser("put", help="Upload file (上传文件)")
    put_parser.add_argument("local", help="Local path (本地路径)")
    put_parser.add_argument("remote", help="Remote path (远程路径)")
 
    # get
    get_parser = subparsers.add_parser("get", help="Download file (下载文件)")
    get_parser.add_argument("remote", help="Remote path (远程路径)")
    get_parser.add_argument("local", help="Local path (本地路径)")
 
    # mkdir
    mkdir_parser = subparsers.add_parser("mkdir", help="Create directory (创建目录)")
    mkdir_parser.add_argument("path", help="Directory path (目录路径)")
 
    # rm
    rm_parser = subparsers.add_parser("rm", help="Delete file/directory (删除文件或目录)")
    rm_parser.add_argument("path", help="Remote path (路径)")
    rm_parser.add_argument("-d", "--dir", action="store_true", help="Is directory (是否为目录)")
 
    # mv (rename)
    mv_parser = subparsers.add_parser("mv", help="Rename or move (重命名或移动)")
    mv_parser.add_argument("old", help="Source path (原路径)")
    mv_parser.add_argument("new", help="Target path (新路径)")
 
    # find
    find_parser = subparsers.add_parser("find", help="Search files (搜索文件)")
    find_parser.add_argument("keyword", help="Keyword to search (关键字)")
    find_parser.add_argument("--path", default="/", help="Start path (起始路径)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    client = FTPClient(args.name)
    client.connect()

    try:
        if args.command == "ls":
            client.list_dir(args.path)
        elif args.command == "put":
            client.upload(args.local, args.remote)
        elif args.command == "get":
            client.download(args.remote, args.local)
        elif args.command == "mkdir":
            client.mkdir(args.path)
        elif args.command == "rm":
            client.delete(args.path, args.dir)
        elif args.command == "mv":
            client.rename(args.old, args.new)
        elif args.command == "find":
            client.search(args.path, args.keyword)
        elif args.command == "test":
            # client.connect() is already called above, so if it reaches here, it's successful
            print(f"Connection test passed (连接测试通过) [{client.config.get('name', 'default')}]。")
    finally:
        client.close()

if __name__ == "__main__":
    main()
