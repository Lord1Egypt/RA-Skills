# -*- coding: utf-8 -*-
import io
import time
import sys
import os
import socket
import json
import argparse
import io
from typing import Optional, List, Dict, Any, Union, BinaryIO
from nmb.NetBIOS import NetBIOS
from smb.SMBConnection import SMBConnection

# Fix stdout encoding issues on some terminals (修复某些终端上的 stdout 编码问题)
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')

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

    def update(self, bytes_chunk: int) -> None:
        self.bytes_transferred += bytes_chunk
        current_time = time.time()
        
        # Calculate progress (计算进度)
        progress = (self.bytes_transferred / self.filesize) * 100 if self.filesize > 0 else 0
        
        # Optimization: Only refresh output when progress changes > 0.1% or interval > 0.1s to reduce I/O loss (优化：仅在进度变化超过 0.1% 或 间隔超过 0.1 秒时刷新输出，减少 I/O 损耗)
        if (progress - self.last_progress >= 0.1) or (current_time - self.last_update_time >= 0.1) or (self.bytes_transferred == self.filesize):
            elapsed_time = current_time - self.start_time
            speed = self.bytes_transferred / elapsed_time if elapsed_time > 0 else 0
            
            # Format progress bar output (格式化输出进度条)
            # Use \r and terminal clearing for single-line refresh (使用 \r 和终端清除实现单行刷新)
            # Limit filename display length to prevent physical line wrapping (限制文件名显示长度以防止物理换行)
            disp_name = (self.filename[:20] + '..') if len(self.filename) > 22 else self.filename
            line = (
                f"\rTransfer (传输): {disp_name:<22} | "
                f"{progress:6.2f}% | "
                f"{self.bytes_transferred / 1024 / 1024:8.2f}/{self.filesize / 1024 / 1024:8.2f} MB | "
                f"{speed / 1024 / 1024:6.2f} MB/s"
            )
            # Fill with spaces to clear potential trailing chars (用空格填充以清除旧行的残留字符)
            sys.stdout.write(line.ljust(100))
            sys.stdout.flush()
            
            # Print a newline when finished to ensure next message starts on a new line (完成后换行，确保后续消息在新行开始)
            if self.bytes_transferred == self.filesize:
                sys.stdout.write('\n')
                sys.stdout.flush()

            self.last_update_time = current_time
            self.last_progress = progress

class FileWrapper:
    """
    File wrapper to trigger progress updates during read/write. (文件包装器，用于在读取/写入时触发进度更新。)
    """
    def __init__(self, file_obj: BinaryIO, monitor: ProgressMonitor):
        self.file_obj = file_obj
        self.monitor = monitor

    def read(self, size: int = -1) -> bytes:
        chunk = self.file_obj.read(size)
        if chunk:
            self.monitor.update(len(chunk))
        return chunk
    
    def write(self, data: bytes) -> int:
        written = self.file_obj.write(data)
        self.monitor.update(len(data))
        return written
    
    def __getattr__(self, attr):
        return getattr(self.file_obj, attr)

class SMBClient:
    """
    SMB client wrapper class, responsible for configuration loading, connection lifecycle, and common file operations. (SMB 客户端包装类，负责管理配置加载、连接生命周期以及常用的文件操作。)
    """
    def __init__(self, config_name: Optional[str] = None):
        self.conn: Optional[SMBConnection] = None
        self.config: Dict[str, Any] = self._load_config(config_name)
        self.service_name: str = self.config.get('share')
        self.base_path: str = self.config.get('path', '/').rstrip('/') or '/'

    def _load_config(self, name: Optional[str]) -> Dict[str, Any]:
        if not os.path.exists(CONFIG_FILE):
            print(f"Error: Config file not found (错误: 找不到配置文件) {CONFIG_FILE}")
            self._create_template_config()
            sys.exit(1)

        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            # [New] Support for comments (// or /* */) while preserving URLs ([新增] 支持注释并保留 URL)
            import re
            pattern = r'("(?:\\.|[^"\\])*")|//[^\r\n]*|/\*.*?\*/'
            content = re.sub(pattern, lambda m: m.group(1) if m.group(1) else '', content, flags=re.DOTALL)
            data = json.loads(content)
            smb_configs = data.get('smb', [])
            
            if not smb_configs:
                print("Warning: No 'smb' configuration found in config.json. Automatically adding template... (警告: config.json 中没有 'smb' 配置。正在自动添加模板...)")
                self._create_template_config(existing_data=data)
                sys.exit(1)

            # [New] Duplicate name validation ([新增] 重名校验)
            names_seen = set()
            for cfg in smb_configs:
                cfg_name = cfg.get('name')
                if cfg_name in names_seen:
                    print(f"Error: Duplicate name '{cfg_name}' found in SMB configs, please fix config.json (错误: 在 SMB 配置中发现重复的名称 '{cfg_name}'，请修正 config.json)。")
                    sys.exit(1)
                names_seen.add(cfg_name)

            if name:
                for cfg in smb_configs:
                    if cfg.get('name') == name:
                        return cfg
                print(f"Error: Configuration '{name}' not found (错误: 未找到名为 '{name}' 的配置)。")
                sys.exit(1)
            else:
                # Default to returning the first one (默认返回第一个)
                return smb_configs[0]

    def _create_template_config(self, existing_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Automatically create or supplement a template file. (当配置文件不存在或缺少配置项时，自动创建或补充模板文件。)
        """
        smb_template = [
            {
                "name": "example",
                "user": "your_user",
                "password": "your_password",
                "ip": "192.168.1.100",
                "share": "shared_folder"
            }
        ]
        
        if existing_data is not None:
            # Supplement existing config (补充现有配置)
            existing_data['smb'] = smb_template
            final_data = existing_data
            message = "SMB template has been added to the existing config.json. Please configure it and try again. (SMB 模板已添加到现有的 config.json 中，请配置后重试。)"
        else:
            # Create new config (创建新配置)
            final_data = {"smb": smb_template}
            message = "A template config.json has been generated in the current directory, please configure it and try again (已为您在当前目录下生成 config.json 模板，请配置后重试)。"

        print(message)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

    def connect(self, timeout: int = 60) -> SMBConnection:
        """
        Establish connection to SMB server based on configuration. Supports NetBIOS name query and multi-port attempts. (根据配置建立与 SMB 服务器的连接。支持 NetBIOS 名称查询和多端口尝试。)
        
        :param timeout: Connection timeout in seconds (连接超时时间，秒).
        :return: Active SMBConnection object on success (成功建立连接的 SMBConnection 对象).
        
        Example (CLI):
            python smb_drive_tools.py --name test ls /
        """
        username = self.config.get('user')
        password = self.config.get('password')
        server_ip = self.config.get('ip')
        domain = self.config.get('domain', 'WORKGROUP')
        
        client_machine_name = socket.gethostname()
        
        # Try to get server name (尝试获取服务器名称)
        server_name = server_ip
        try:
            netbios = NetBIOS()
            server_names = netbios.queryIPForName(server_ip, timeout=timeout/4)
            if server_names:
                server_name = server_names[0]
            netbios.close()
        except:
            pass

        self.conn = SMBConnection(username, password, client_machine_name, server_name, domain=domain, use_ntlm_v2=True)
        print(f"Connecting (正在建立连接) [{self.config['name']}] -> {server_ip}...")
        
        try:
            if self.conn.connect(server_ip, 139, timeout=timeout) or self.conn.connect(server_ip, 445, timeout=timeout):
                print(f"Connected to SMB server successfully (成功连接至 SMB 服务器)。")
                return self.conn
            else:
                print("Connection failed: Auth failed, share inaccessible, or please check your drive configuration (连接失败：身份验证未通过、共享目录无法访问，或请检查云盘配置信息)。")
                sys.exit(1)
        except Exception as e:
            print(f"Connection failed: Please check your drive configuration (连接失败：请检查云盘配置信息) {server_ip} (Reason/原因: {e})")
            sys.exit(1)

    def close(self) -> None:
        """
        Close the current SMB connection. (关闭当前的 SMB 连接。)
        
        Example (CLI):
            python smb_drive_tools.py --name test ls /
        """
        if self.conn:
            self.conn.close()

    def _get_full_path(self, path: Union[str, os.PathLike]) -> str:
        """Merge requested path with configured base_path to implement scope limitation. (将请求路径与配置的 base_path 合并，实现范围限定。)"""
        # Ensure path is string and clean (确保路径为字符串并清理)
        path = str(path).replace('\\', '/')
        clean_path = path.lstrip('/')
        
        # Combine base_path and relative path (合并基础路径与相对路径)
        full_path = f"{self.base_path}/{clean_path}".replace('//', '/')
        return full_path if full_path.startswith('/') else f"/{full_path}"

    # Following are legacy functional methods (以下为封装的功能方法)

    def list_dir(self, path: str = '/') -> None:
        """
        List files and directories in the remote path and display them in a table format. (列出远程目录下的文件和文件夹，并以表格形式显示。)
        
        :param path: Remote directory path (远程目录路径).
        
        Example (CLI):
            python smb_drive_tools.py --name test ls /Documents
        """
        try:
            full_path = self._get_full_path(path)
            files = self.conn.listPath(self.service_name, full_path)
            print(f"\nDirectory Listing (目录列表) [{self.service_name}:{full_path}]:")
            col_format = "{:<50} {:<20} {:<15}"
            print(col_format.format("Name (名称)", "Modify Date (修改日期)", "Size (大小)"))
            print("-" * 88)
            for file in files:
                if file.filename not in ['.', '..']:
                    # Format date (格式化日期)
                    t = time.localtime(file.last_write_time)
                    date_str = time.strftime("%Y-%m-%d %H:%M", t)
                    
                    size_mb = f"{file.file_size / 1024 / 1024:,.2f} MB" if not file.isDirectory else "DIR (目录)"
                    print(col_format.format(file.filename, date_str, size_mb))
        except Exception as e:
            print(f"List directory failed (列出目录失败): {e}")

    def upload(self, local_path: str, remote_path: str) -> None:
        """
        Upload a local file to the SMB server with a progress bar. (上传本地文件到 SMB 服务器。支持显示进度条。)
        
        :param local_path: Local file source path (本地待上传路径).
        :param remote_path: Target remote path, including filename (目标远程路径，需包含文件名).
        
        Example (CLI):
            python smb_drive_tools.py --name test put ./data.zip /backups/data.zip
        """
        try:
            full_remote_path = self._get_full_path(remote_path)
            filesize = os.path.getsize(local_path)
            monitor = ProgressMonitor(os.path.basename(local_path), filesize)
            with open(local_path, 'rb') as file_obj:
                wrapped_file = FileWrapper(file_obj, monitor)
                self.conn.storeFile(self.service_name, full_remote_path, wrapped_file)
            print(f"\nUpload success (上传成功): {local_path} -> {full_remote_path}")
        except Exception as e:
            print(f"\nUpload failed (上传失败): {e}")

    def download(self, remote_path: str, local_path: str) -> None:
        """
        Download a file from the SMB server to local path with a progress bar. (从 SMB 服务器下载文件到本地。支持显示进度条。)
        
        :param remote_path: Source remote path (远程文件路径).
        :param local_path: Target local path, including filename (本地保存路径，需包含文件名).
        
        Example (CLI):
            python smb_drive_tools.py --name test get /movies/demo.mp4 ./demo.mp4
        """
        try:
            full_remote_path = self._get_full_path(remote_path)
            filesize = 0
            try:
                attr = self.conn.getAttributes(self.service_name, full_remote_path)
                filesize = attr.file_size
            except: pass
            monitor = ProgressMonitor(os.path.basename(remote_path), filesize)
            with open(local_path, 'wb') as file_obj:
                wrapped_file = FileWrapper(file_obj, monitor)
                self.conn.retrieveFile(self.service_name, full_remote_path, wrapped_file)
            print(f"\nDownload success (下载成功): {full_remote_path} -> {local_path}")
        except Exception as e:
            print(f"\nDownload failed (下载失败): {e}")

    def mkdir(self, path: str) -> None:
        """
        Create a new directory on the SMB server. (在服务器上创建新目录。)
        
        :param path: Remote directory path to create (待创建的远程路径).
        
        Example (CLI):
            python smb_drive_tools.py --name test mkdir /projects/new_folder
        """
        try:
            full_path = self._get_full_path(path)
            self.conn.createDirectory(self.service_name, full_path)
            print(f"Create directory success (创建目录成功): {full_path}")
        except Exception as e:
            print(f"Create directory failed (创建目录失败): {e}")

    def delete(self, path: str, is_dir: bool = False, recursive: bool = False) -> None:
        """
        Delete a file or directory on the SMB server. (删除服务器上的文件或目录。)
        
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
                    self.conn.deleteDirectory(self.service_name, full_path)
            else:
                self.conn.deleteFiles(self.service_name, full_path)
            print(f"Delete success (删除成功): {full_path}")
        except Exception as e:
            print(f"Delete failed (删除失败): {e}")

    def _delete_recursive(self, full_path: str) -> None:
        """Internal helper for recursive deletion. (递归删除的内部辅助方法。)"""
        files = self.conn.listPath(self.service_name, full_path)
        for f in files:
            if f.filename in ['.', '..']: continue
            item_path = f"{full_path}/{f.filename}".replace('//', '/')
            if f.isDirectory:
                self._delete_recursive(item_path)
            else:
                self.conn.deleteFiles(self.service_name, item_path)
        self.conn.deleteDirectory(self.service_name, full_path)

    def upload_dir(self, local_path: str, remote_path: str) -> None:
        """
        Recursively upload a local directory to the SMB server. (递归上传本地目录到 SMB 服务器。)
        
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
                # Calculate relative path (计算相对路径)
                rel_path = os.path.relpath(root, local_path)
                if rel_path == '.':
                    target_dir = remote_path
                else:
                    target_dir = f"{remote_path}/{rel_path}".replace('\\', '/').replace('//', '/')
                
                # Create subdirs (创建子目录)
                for d in dirs:
                    sub_dir = f"{target_dir}/{d}".replace('//', '/')
                    self.mkdir(sub_dir)
                
                # Upload files (上传文件)
                for f in files:
                    local_f = os.path.join(root, f)
                    remote_f = f"{target_dir}/{f}".replace('//', '/')
                    self.upload(local_f, remote_f)
            
            print(f"Directory upload completed (目录上传已完成): {local_path} -> {remote_path}")
        except Exception as e:
            print(f"Directory upload failed (目录上传失败): {e}")

    def rename(self, old_path, new_path):
        """
        Rename or move a file or directory on the SMB server. (重命名或移动服务器上的文件或目录。)
        
        :param old_path: Source remote path (原远程路径).
        :param new_path: Target remote path (新远程路径).
        
        Example (CLI):
            python smb_drive_tools.py --name test mv /old_name.txt /new_name.txt
        """
        try:
            full_old = self._get_full_path(old_path)
            full_new = self._get_full_path(new_path)
            self.conn.rename(self.service_name, full_old, full_new)
            print(f"Rename success (重命名成功): {full_old} -> {full_new}")
        except Exception as e:
            print(f"Rename failed (重命名失败): {e}")

    def search(self, path: str, keyword: str) -> None:
        """
        Recursively search for files containing the keyword under the specified path. (递归搜索指定目录下包含关键字的文件。)
        
        :param path: Starting path for search (搜索起始路径).
        :param keyword: Keyword to search for (搜索关键字).
        
        Example (CLI):
            python smb_drive_tools.py --name test find .mp4 --path /movies
        """
        try:
            full_path = self._get_full_path(path)
            self._search_recursive(full_path, keyword)
        except: pass

    def _search_recursive(self, full_path: str, keyword: str) -> None:
        """Recursive search helper using absolute path to avoid redundant base_path prepending (递归搜索辅助方法，使用绝对路径避免重复叠加 base_path)"""
        try:
            files = self.conn.listPath(self.service_name, full_path)
            for f in files:
                if f.filename in ['.', '..']: continue
                current_full_path = f"{full_path}/{f.filename}".replace('//', '/')
                if keyword.lower() in f.filename.lower():
                    print(f"[Match (匹配)] {current_full_path}")
                if f.isDirectory:
                    self._search_recursive(current_full_path, keyword)
        except: pass

def main() -> None:
    """
    CLI entry function, parses command line arguments and calls SMBClient methods. (CLI 入口函数，负责解析命令行参数并调用 SMBClient 对应方法。)
    """
    parser = argparse.ArgumentParser(description="SMB Drive Tools CLI (SMB 驱动工具命令行版)")
    parser.add_argument("--name", help="Connection name in config.json (配置文件中的连接名称)", default=None)
    
    subparsers = parser.add_subparsers(dest="command", help="Subcommands (子命令)")

    # test
    test_parser = subparsers.add_parser("test", help="Test connection (测试连接)")
 
    # ls
    ls_parser = subparsers.add_parser("ls", help="List directory (列出目录)")
    ls_parser.add_argument("path", nargs="?", default="/", help="Remote path (远程路径)")
 
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
    rm_parser.add_argument("path", help="Remote path (远程路径)")
    rm_parser.add_argument("-d", "--dir", action="store_true", help="Is directory (是否为目录)")
 
    # mv (rename)
    mv_parser = subparsers.add_parser("mv", help="Rename or move (重命名或移动)")
    mv_parser.add_argument("old", help="Old path (原路径)")
    mv_parser.add_argument("new", help="New path (新路径)")
 
    # find
    find_parser = subparsers.add_parser("find", help="Search files (搜索文件)")
    find_parser.add_argument("keyword", help="Keyword (关键字)")
    find_parser.add_argument("--path", default="/", help="Start path (起始路径)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    client = SMBClient(args.name)
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
