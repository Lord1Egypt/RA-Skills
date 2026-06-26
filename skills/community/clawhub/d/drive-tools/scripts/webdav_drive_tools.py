# -*- coding: utf-8 -*-
import time
import sys
import os
import json
import argparse
import io
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import urllib.parse
from typing import Optional, List, Dict, Any, Union, BinaryIO, Tuple

# Fix stdout encoding issues on some terminals (修复某些终端上的 stdout 编码问题)
if sys.stdout.encoding != 'UTF-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CONFIG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.json')

class ProgressMonitor:
    """
    Utility class for monitoring file transfer progress. Optimized: reduced refresh frequency to improve performance and provide a friendly progress bar output. (用于监控文件传输进度的工具类。已优化：降低刷新频率以提高性能，并提供友好的进度条输出。)
    """
    def __init__(self, filename: str, filesize: int):
        self.filename = filename
        self.filesize = filesize
        self.bytes_transferred = 0
        self.start_time = time.time()
        self.last_update_time = 0.0
        self.last_progress = -1.0

    def update(self, bytes_chunk_size: int) -> None:
        """
        Update transferred bytes and print progress in real-time. (更新已传输的字节数并实时打印进度。)
        
        :param bytes_chunk_size: Size of the current byte chunk (本次传输的字节块大小).
        """
        self.bytes_transferred += bytes_chunk_size
        current_time = time.time()
        
        # Calculate percentage progress (计算百分比进度)
        progress = (self.bytes_transferred / self.filesize) * 100 if self.filesize > 0 else 0
        
        # Optimization: Only refresh output when progress changes > 0.1% or interval > 0.1s to reduce console I/O loss (优化：仅在进度变化超过 0.1% 或间隔超过 0.1 秒时刷新输出，减少控制台 I/O 损耗)
        if (progress - self.last_progress >= 0.1) or (current_time - self.last_update_time >= 0.1) or (self.bytes_transferred == self.filesize):
            elapsed_time = current_time - self.start_time
            speed = self.bytes_transferred / elapsed_time if elapsed_time > 0 else 0
            
            # Format progress bar output (格式化输出进度条)
            # Use \r for single-line refresh and pad with spaces (使用 \r 实现单行刷新并用空格填充)
            disp_name = (self.filename[:20] + '..') if len(self.filename) > 22 else self.filename
            line = (
                f"\rTransfer (传输): {disp_name:<22} | "
                f"{progress:6.2f}% | "
                f"{self.bytes_transferred / 1024 / 1024:8.2f}/{self.filesize / 1024 / 1024:8.2f} MB | "
                f"{speed / 1024 / 1024:6.2f} MB/s"
            )
            sys.stdout.write(line.ljust(100))
            sys.stdout.flush()
            
            if self.bytes_transferred == self.filesize:
                sys.stdout.write('\n')
                sys.stdout.flush()

            self.last_update_time = current_time
            self.last_progress = progress

class WebDAVClient:
    """
    WebDAV client wrapper class, responsible for configuration loading, connection authentication, and common file/directory operations. 
    Directly implements WebDAV protocol using requests library (PROPFIND, PUT, GET, MKCOL, DELETE, MOVE). 
    (WebDAV 客户端封装类，负责管理配置加载、连接认证以及常用的文件/目录操作。使用 requests 库直接实现 WebDAV 协议。)
    """
    def __init__(self, config_name: Optional[str] = None):
        self.config: Dict[str, Any] = self._load_config(config_name)
        # Uniformly handle URL, ensuring no trailing slash (统一处理 URL，确保不带结尾斜杠)
        self.url: str = self.config.get('url', '').rstrip('/')
        self.auth = HTTPBasicAuth(self.config.get('user'), self.config.get('password'))
        self.base_path: str = self.config.get('path', '/').rstrip('/') or '/'
        
        # Parse URL for base and path components (解析 URL 以获取基础地址和路径组件)
        from urllib.parse import urlparse
        parsed = urlparse(self.url)
        self.base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.url_path = parsed.path.rstrip('/') # e.g. /dav

    def _load_config(self, name: Optional[str]) -> Dict[str, Any]:
        """
        Load specified WebDAV configuration from config.json. (从 config.json 文件中加载指定的 WebDAV 配置信息。)
        """
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
            webdav_configs = [cfg for cfg in data.get('webdav', []) if cfg]
            
            if not webdav_configs:
                print("Warning: No 'webdav' configuration found in config.json. Automatically adding template... (警告: config.json 中没有 'webdav' 配置。正在自动添加模板...)")
                self._create_template_config(existing_data=data)
                sys.exit(1)

            # [New] Duplicate name validation ([新增] 重名校验)
            names_seen = set()
            for cfg in webdav_configs:
                cfg_name = cfg.get('name')
                if cfg_name in names_seen:
                    print(f"Error: Duplicate name '{cfg_name}' found in WebDAV configs, please fix config.json (错误: 在 WebDAV 配置中发现重复的名称 '{cfg_name}'，请修正 config.json)。")
                    sys.exit(1)
                names_seen.add(cfg_name)
            
            if name:
                # Try to handle as a numeric index (尝试作为数字索引处理)
                if name.isdigit():
                    idx = int(name) - 1
                    if 0 <= idx < len(webdav_configs):
                        return webdav_configs[idx]
                
                # Try to handle as a configuration name (尝试作为名称处理)
                for cfg in webdav_configs:
                    if cfg.get('name') == name:
                        return cfg
                print(f"Error: Configuration '{name}' not found (错误: 未找到名为 '{name}' 的配置)。")
                sys.exit(1)
            
            # Default to loading the first configuration (默认加载第一个配置)
            return webdav_configs[0]

    def _create_template_config(self, existing_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Automatically create or supplement a template file. (当配置文件不存在或缺少配置项时，自动创建或补充模板文件。)
        """
        webdav_template = [
            {
                "name": "example",
                "user": "your_user",
                "password": "your_password",
                "url": "https://dav.jianguoyun.com/dav/",
                "path": "/"
            }
        ]
        
        if existing_data is not None:
            existing_data['webdav'] = webdav_template
            final_data = existing_data
            message = "WebDAV template has been added to the existing config.json. Please configure it and try again. (WebDAV 模板已添加到现有的 config.json 中，请配置后重试。)"
        else:
            final_data = {"webdav": webdav_template}
            message = "A template config.json has been generated in the current directory, please configure it and try again (已为您在当前目录下生成 config.json 模板，请配置后重试)。"

        print(message)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

    def _get_full_path(self, path: Union[str, os.PathLike]) -> str:
        """Merge requested path with configured base_path. (将请求路径与配置的 base_path 合并。)"""
        path = str(path).replace('\\', '/')
        clean_path = path.lstrip('/')
        full_path = f"{self.base_path}/{clean_path}".replace('//', '/')
        return full_path if full_path.startswith('/') else f"/{full_path}"

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """
        Internal generic HTTP request wrapper with basic authentication and path normalization. (内部通用的 HTTP 请求封装，包含基础认证与路径规范化。)
        """
        # Handle paths that already contain absolute URLs or are full server paths (处理已包含完整 URL 或服务器绝对路径的情况)
        if path.startswith('http'):
            url = path
        elif self.url_path and path.startswith(self.url_path):
            # If path already has the /dav prefix, join with base_url (基准地址)
            url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        else:
            # Standard relative path (标准相对路径)
            url = f"{self.url.rstrip('/')}/{path.lstrip('/')}"
            
        response = requests.request(method, url, auth=self.auth, **kwargs)
        if response.status_code == 401:
            print(f"\nAuth failed: Please check if the user {self.config.get('user')} credentials and drive configuration are correct (身份验证失败：请检查用户 {self.config.get('user')} 的凭据及云盘配置信息是否正确且有效)。")
            sys.exit(1)
        return response

    def connect(self) -> None:
        """
        Verify if the connection to the WebDAV server is active. (验证与 WebDAV 服务器的连接是否可用。)
        
        Example (CLI):
            python webdav_drive_tools.py --name "坚果云" ls /
        """
        resp = self._request('PROPFIND', self.base_path, headers={'Depth': '0'})
        if resp.status_code in [200, 207]:
            print(f"Connected to WebDAV server successfully (成功连接至 WebDAV 服务器) (Root/根路径: {self.base_path})。")
        else:
            print(f"Connection failed: Please check your drive configuration (连接失败：请检查云盘配置信息) {self.base_path} (HTTP {resp.status_code})")
            sys.exit(1)

    def list_dir(self, path: str = '/') -> None:
        """
        List files and directories in the remote path. (列出远程目录下的文件和文件夹。)
        
        :param path: Remote directory path (远程目录路径).
        
        Example (CLI):
            python webdav_drive_tools.py --name 1 ls /Photos
        """
        try:
            full_path = self._get_full_path(path)
            resp = self._request('PROPFIND', full_path, headers={'Depth': '1'})
            if resp.status_code != 207:
                print(f"List directory failed (列出目录失败): HTTP {resp.status_code}")
                return

            tree = ET.fromstring(resp.content)
            namespace = {'d': 'DAV:'}
            print(f"\nDirectory Listing (目录列表) [{full_path}]:")
            col_format = "{:<50} {:<20} {:<15}"
            print(col_format.format("Name (名称)", "Modify Date (修改日期)", "Size (大小)"))
            print("-" * 88)
            
            responses = tree.findall('d:response', namespace)
            for resp_node in responses:
                href = resp_node.find('d:href', namespace).text
                full_href_path = urllib.parse.unquote(href)
                
                # Exclude the directory itself (排除目录本身)
                rel_href = full_href_path.split('.com')[-1] if '.com' in full_href_path else full_href_path
                prefix = self.base_url.split('.com')[-1] if '.com' in self.base_url else ""
                clean_path = rel_href.replace(prefix, '', 1).rstrip('/')
                if clean_path == full_path.rstrip('/'):
                    continue

                name = os.path.basename(full_href_path.strip('/'))
                if not name: continue

                prop = resp_node.find('.//d:prop', namespace)
                resourcetype = prop.find('d:resourcetype', namespace)
                is_dir = resourcetype.find('d:collection', namespace) is not None
                
                size = 0
                size_node = prop.find('d:getcontentlength', namespace)
                if size_node is not None:
                    size = int(size_node.text)

                date_str = "N/A"
                date_node = prop.find('d:getlastmodified', namespace)
                if date_node is not None:
                    try:
                        import email.utils
                        dt = email.utils.parsedate_to_datetime(date_node.text)
                        date_str = dt.strftime("%Y-%m-%d %H:%M")
                    except:
                        date_str = date_node.text[:16]

                size_display = f"{size / 1024 / 1024:,.2f} MB" if not is_dir else "DIR (目录)"
                print(col_format.format(name, date_str, size_display))
        except Exception as e:
            print(f"Error parsing directory list (解析目录列表发生错误): {e}")

    def upload(self, local_path: str, remote_path: str) -> None:
        """
        Upload a local file to the WebDAV server with a progress bar. (上传本地文件到 WebDAV 服务器。支持进度条显示。)
        
        :param local_path: Source local file path (本地源文件路径).
        :param remote_path: Target remote path, including filename (目标远程路径，需包含文件名).
        
        Example (CLI):
            python webdav_drive_tools.py --name 坚果云 put ./notes.txt /Documents/notes.txt
        """
        try:
            full_remote_path = self._get_full_path(remote_path)
            if not os.path.exists(local_path):
                print(f"Error: Local file not found (错误: 本地文件不存在) {local_path}")
                return
                
            filesize = os.path.getsize(local_path)
            monitor = ProgressMonitor(os.path.basename(local_path), filesize)
            
            class CallbackReader:
                def __init__(self, file, callback):
                    self.file = file
                    self.callback = callback
                def read(self, size):
                    chunk = self.file.read(size)
                    if chunk: self.callback(len(chunk))
                    return chunk
                def __len__(self): return filesize
            
            with open(local_path, 'rb') as f:
                reader = CallbackReader(f, monitor.update)
                resp = self._request('PUT', full_remote_path, data=reader)
                if resp.status_code in [200, 201, 204]:
                    print(f"\nUpload success (上传成功): {local_path} -> {full_remote_path}")
                else:
                    print(f"\nUpload failed (上传失败): HTTP {resp.status_code}")
        except Exception as e:
            print(f"\nError occurred during upload (上传过程中发生错误): {e}")

    def download(self, remote_path: str, local_path: str) -> None:
        """
        Download a file from the WebDAV server to local path with a progress bar. (从 WebDAV 服务器下载文件到本地。支持进度条显示。)
        
        :param remote_path: Source remote file path (远程源文件路径).
        :param local_path: Target local file path (本地保存路径).
        
        Example (CLI):
            python webdav_drive_tools.py --name 1 get /Documents/report.pdf ./report.pdf
        """
        try:
            full_remote_path = self._get_full_path(remote_path)
            resp = self._request('GET', full_remote_path, stream=True)
            if resp.status_code != 200:
                print(f"Download failed (下载失败): HTTP {resp.status_code}")
                return
            
            total_size = int(resp.headers.get('content-length', 0))
            monitor = ProgressMonitor(os.path.basename(remote_path), total_size)
            
            local_dir = os.path.dirname(os.path.abspath(local_path))
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
                
            with open(local_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        monitor.update(len(chunk))
            print(f"\nDownload success (下载成功): {full_remote_path} -> {local_path}")
        except Exception as e:
            print(f"\nError occurred during download (下载过程中发生错误): {e}")

    def mkdir(self, path: str) -> None:
        """
        Create a new directory on the WebDAV server. (在服务器上创建目录。)
        
        :param path: Remote directory path to create (待创建的远程路径).
        """
        full_path = self._get_full_path(path)
        # Ensure trailing slash for directory creation to improve compatibility (确保末尾斜杠以提高目录创建的兼容性)
        if not full_path.endswith('/'):
            full_path += '/'
            
        resp = self._request('MKCOL', full_path)
        if resp.status_code in [201, 207]:
            print(f"Create directory success (创建目录成功): {full_path}")
        elif resp.status_code == 405:
            # Already exists (已存在)
            pass
        else:
            print(f"Create directory failed (创建目录失败): HTTP {resp.status_code}")

    def delete(self, path: str, is_dir: bool = False, recursive: bool = True) -> None:
        """
        Delete a file or directory on the WebDAV server. (删除服务器上的文件或目录。)
        
        :param path: Remote path to delete (远程路径).
        :param is_dir: Hint if path is a directory (提示是否为目录).
        :param recursive: If True, delete non-empty directory recursively by client-side traversal (如果是 True，则通过客户端侧遍历进行递归删除，以防服务端 403 限制).
        """
        full_path = self._get_full_path(path)
        
        if is_dir and recursive:
            # Client-side recursive delete to bypass server restrictions (客户端侧递归删除，以绕过服务器限制)
            self._delete_recursive(full_path)
        else:
            # Single item delete (单项删除)
            item_path = full_path + ('/' if is_dir and not full_path.endswith('/') else '')
            resp = self._request('DELETE', item_path)
            if resp.status_code in [200, 204]:
                print(f"Delete success (删除成功): {item_path}")
            else:
                print(f"Delete failed (删除失败): HTTP {resp.status_code} on {item_path}")

    def _delete_recursive(self, full_path: str) -> None:
        """Internal helper for client-side recursive deletion. (用于客户端侧递归删除的内部辅助项。)"""
        # Ensure trailing slash for listing (确保列出目录时带斜杠)
        list_path = full_path + ('/' if not full_path.endswith('/') else '')
        
        # 1. Get children using current listing logic (通过列表逻辑获取子项)
        # Note: We use PROPFIND via list_dir internally (我们内部使用 list_dir 调用的 PROPFIND)
        try:
            # We need raw items to know if they are dirs or files (我们需要原始项以确定是目录还是文件)
            # Reusing the parsing logic from list_dir would be best but let's do a quick focused PROPFIND
            headers = {'Depth': '1', 'Content-Type': 'application/xml; charset=utf-8'}
            resp = self._request('PROPFIND', list_path, headers=headers)
            if resp.status_code == 207:
                root = ET.fromstring(resp.content)
                namespace = {'d': 'DAV:'}
                
                # Iterate through responses (跳过第一个项，即父目录本身)
                entries = root.findall('.//d:response', namespace)
                for entry in entries:
                    href = entry.find('d:href', namespace).text
                    href = urllib.parse.unquote(href)
                    
                    # Normalize href for comparison (规范化用于比较的 href)
                    # Check if it's the directory itself (检查是否为目录本身)
                    if href.rstrip('/') == list_path.rstrip('/') or href.rstrip('/') == urllib.parse.quote(list_path.rstrip('/')):
                        continue
                    
                    # Determine type (判断类型)
                    resourcetype = entry.find('.//d:resourcetype', namespace)
                    is_coll = resourcetype is not None and resourcetype.find('d:collection', namespace) is not None
                    
                    # Get path relative to the remote root (获取相对于远程根目录的路径)
                    # href is usually absolute URL or absolute path on server. We need the segment after the DAV base.
                    # Simplified: if href starts with the base path, we can extract the tail.
                    # For jianguoyun, href might include /dav/ prefix.
                    # We can just use href directly for DELETE if it's a full URL or absolute path.
                    
                    # Recursive call for collections (若是集合则递归调用)
                    if is_coll:
                        self._delete_recursive(href)
                    else:
                        # Delete file (删除文件)
                        child_resp = self._request('DELETE', href)
                        if child_resp.status_code in [200, 204]:
                            print(f"Delete success (删除成功): {href}")
            
            # 2. Finally delete the now-empty parent directory (最后删除已清空的父目录)
            resp = self._request('DELETE', list_path)
            if resp.status_code in [200, 204]:
                 print(f"Delete success (删除成功): {list_path}")
            else:
                 print(f"Delete recursive failed at parent (递归删除父目录失败): HTTP {resp.status_code} on {list_path}")
                 
        except Exception as e:
            print(f"Recursive delete error (递归删除出错): {e}")

    def upload_dir(self, local_path: str, remote_path: str) -> None:
        """
        Recursively upload a local directory to the WebDAV server. (递归上传本地目录到 WebDAV 服务器。)
        
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
        Rename or move a file or directory on the WebDAV server. (重命名或移动服务器上的文件/目录。)
        
        :param old_path: Source remote path (原路径).
        :param new_path: Target remote path (新路径).
        
        Example (CLI):
            python webdav_drive_tools.py --name 1 mv /old_name.txt /new_name.txt
        """
        full_old = self._get_full_path(old_path)
        full_new = self._get_full_path(new_path)
        dest_url = f"{self.base_url}/{full_new.lstrip('/')}"
        resp = self._request('MOVE', full_old, headers={'Destination': dest_url})
        if resp.status_code in [201, 204]:
            print(f"Rename success (重命名成功): {full_old} -> {full_new}")
        else:
            print(f"Rename failed (重命名失败): HTTP {resp.status_code}")

    def search(self, path: str, keyword: str) -> None:
        """
        Recursively search for files or folders containing the keyword under path. (递归搜索指定目录下包含关键字的文件或文件夹。)
        
        :param path: Starting path for search (搜索起始路径).
        :param keyword: Keyword to search for (搜索关键字).
        
        Example (CLI):
            python webdav_drive_tools.py --name 1 find report --path /
        """
        try:
            full_path = self._get_full_path(path)
            self._search_recursive(full_path, keyword)
        except: pass

    def _search_recursive(self, full_path: str, keyword: str) -> None:
        """Recursive search helper method. (递归搜索辅助方法。)"""
        try:
            resp = self._request('PROPFIND', full_path, headers={'Depth': '1'})
            if resp.status_code != 207: return
            
            tree = ET.fromstring(resp.content)
            namespace = {'d': 'DAV:'}
            responses = tree.findall('d:response', namespace)
            
            for resp_node in responses:
                href = resp_node.find('d:href', namespace).text
                full_href_path = urllib.parse.unquote(href)
                
                rel_path = full_href_path.split('.com')[-1] if '.com' in full_href_path else full_href_path
                prefix = self.base_url.split('.com')[-1] if '.com' in self.base_url else ""
                clean_rel_path = rel_path.replace(prefix, '', 1)
                
                if clean_rel_path.rstrip('/') == full_path.rstrip('/'): continue
                
                name = os.path.basename(clean_rel_path.strip('/'))
                if keyword.lower() in name.lower():
                    print(f"[Match (匹配)] {clean_rel_path}")
                
                prop = resp_node.find('.//d:prop', namespace)
                resourcetype = prop.find('d:resourcetype', namespace)
                if resourcetype.find('d:collection', namespace) is not None:
                    self._search_recursive(clean_rel_path, keyword)
        except: pass

def main() -> None:
    """
    CLI entry function, responsible for parsing command line arguments and calling WebDAVClient methods. (CLI 入口函数，负责解析命令行参数并调用 WebDAVClient 对应方法。)
    """
    parser = argparse.ArgumentParser(description="WebDAV Drive Tools CLI (based on requests) (WebDAV 驱动工具命令行版)")
    parser.add_argument("--name", help="Connection name or 1-indexed index in config.json (配置文件中的连接名称或索引)", default=None)
    
    subparsers = parser.add_subparsers(dest="command", help="Subcommands (支持的子命令)")

    # test
    test_parser = subparsers.add_parser("test", help="Test connection (测试连接)")
    
    # ls
    ls_parser = subparsers.add_parser("ls", help="List directory content (列出目录内容)")
    ls_parser.add_argument("path", nargs="?", default="/", help="Remote path to query (要查询的远程路径)")
    
    # put
    put_parser = subparsers.add_parser("put", help="Upload local file (上传本地文件)")
    put_parser.add_argument("local", help="Local file path (本地文件路径)")
    put_parser.add_argument("remote", help="Target remote path, including filename (目标远程路径，含文件名)")
    
    # get
    get_parser = subparsers.add_parser("get", help="Download remote file (下载远程文件)")
    get_parser.add_argument("remote", help="Remote file path (远程文件路径)")
    get_parser.add_argument("local", help="Local save path (本地保存路径)")
    
    # mkdir
    mkdir_parser = subparsers.add_parser("mkdir", help="Create new directory (创建新目录)")
    mkdir_parser.add_argument("path", help="Remote directory path (远程目录路径)")
    
    # rm
    rm_parser = subparsers.add_parser("rm", help="Delete file/directory (删除文件或目录)")
    rm_parser.add_argument("path", help="Remote path to delete (要删除的远程路径)")
    
    # mv
    mv_parser = subparsers.add_parser("mv", help="Rename or move path (重命名或移动路径)")
    mv_parser.add_argument("old", help="Source path (源路径)")
    mv_parser.add_argument("new", help="Target path (新路径)")
    
    # find
    find_parser = subparsers.add_parser("find", help="Search recursively for keyword (递归搜索关键字)")
    find_parser.add_argument("keyword", help="Keyword to search (搜索关键字)")
    find_parser.add_argument("--path", default="/", help="Starting search path (起始搜索路径)")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    # Create client and establish connection (创建客户端并建立连接)
    client = WebDAVClient(args.name)
    client.connect()

    # Command dispatch logic (命令分发逻辑)
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
            client.delete(args.path)
        elif args.command == "mv":
            client.rename(args.old, args.new)
        elif args.command == "find":
            client.search(args.path, args.keyword)
        elif args.command == "test":
            # client.connect() is already called above, so if it reaches here, it's successful
            print(f"Connection test passed (连接测试通过) [{client.config.get('name', 'default')}]。")
    except KeyboardInterrupt:
        print("\nOperation cancelled (操作已取消)。")

if __name__ == "__main__":
    main()
