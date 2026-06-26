#!/usr/bin/env python3
# coding: utf-8
"""
aaPanel File Operations Client
Encapsulates aaPanel file management API interfaces
"""

import json
import urllib.parse
import warnings
from typing import Optional, Dict, Any, List

# Disable SSL warning
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

from .bt_client import BtClient, BtClientManager
from .config import get_servers, ServerConfig


def get_server_config(server_name: str = None) -> Optional[Dict]:
    """
    Get server configuration

    Args:
        server_name: Server name, returns first enabled server when None

    Returns:
        Server config dict or None
    """
    servers = get_servers()
    if not servers:
        return None

    if server_name:
        for server in servers:
            # Support both ServerConfig objects and dict formats
            name = server.name if hasattr(server, 'name') and hasattr(server, 'host') else server.get('name')
            if name == server_name:
                # Convert ServerConfig object to dict
                if hasattr(server, 'name') and hasattr(server, 'host'):
                    return {
                        'name': server.name,
                        'host': server.host,
                        'token': server.token,
                        'timeout': server.timeout,
                        'enabled': server.enabled,
                        'verify_ssl': server.verify_ssl if hasattr(server, 'verify_ssl') else True
                    }
                return server
        return None

    # Return first enabled server
    for server in servers:
        # Support both ServerConfig objects and dict formats
        enabled = server.enabled if hasattr(server, 'enabled') and hasattr(server, 'host') else server.get('enabled', True)
        if enabled:
            # Convert ServerConfig object to dict
            if hasattr(server, 'name') and hasattr(server, 'host'):
                return {
                    'name': server.name,
                    'host': server.host,
                    'token': server.token,
                    'timeout': server.timeout,
                    'enabled': server.enabled,
                    'verify_ssl': server.verify_ssl if hasattr(server, 'verify_ssl') else True
                }
            return server

    return None


class FilesClient:
    """aaPanel file operations client"""

    def __init__(self, server_name: str = None):
        """
        Initialize file client

        Args:
            server_name: Server name, uses default server when None
        """
        self.server_name = server_name
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize API client"""
        if self.server_name:
            config = get_server_config(self.server_name)
            if not config:
                raise ValueError(f"Server configuration not found: {self.server_name}")
            self.client = BtClient(
                name=config.get('name', self.server_name),
                host=config['host'],
                token=config['token'],
                timeout=config.get('timeout', 10000),
                verify_ssl=config.get('verify_ssl', True)
            )
        else:
            # Use default server
            manager = BtClientManager()
            self.client = manager.get_client()

    def _encode_path(self, path: str) -> str:
        """URL encode path"""
        return urllib.parse.quote(path, safe='')

    def get_dir(self, path: str = "/www", page: int = 1, show_row: int = 500) -> Dict[str, Any]:
        """
        Get directory info

        Args:
            path: Directory path
            page: Page number
            show_row: Items per page

        Returns:
            Directory info dict, containing dir (directory list) and files (file list)
        """
        encoded_path = self._encode_path(path)
        endpoint = f"/files?action=GetDirNew&path={encoded_path}&p={page}&showRow={show_row}"
        return self.client.request(endpoint)

    def get_file_body(self, path: str) -> Dict[str, Any]:
        """
        Read file content

        Args:
            path: File path

        Returns:
            File content dict, containing data, encoding, size, etc.
        """
        encoded_path = self._encode_path(path)
        endpoint = f"/files?action=GetFileBody&path={encoded_path}"
        return self.client.request(endpoint)

    def save_file_body(self, path: str, data: str, encoding: str = "utf-8",
                       st_mtime: str = None, force: bool = False) -> Dict[str, Any]:
        """
        Save file content

        Args:
            path: File path
            data: File content
            encoding: File encoding
            st_mtime: File modification timestamp (for concurrency detection)
            force: Whether to force save

        Returns:
            Save result dict
        """
        encoded_path = self._encode_path(path)

        # Use POST body to send data, avoid URL length issues
        params = {
            "path": path,
            "data": data,
            "encoding": encoding
        }
        if st_mtime:
            params["st_mtime"] = st_mtime
        if force:
            params["force"] = "1"

        endpoint = f"/files?action=SaveFileBody"
        return self.client.request(endpoint, params)

    def create_dir(self, path: str) -> Dict[str, Any]:
        """
        Create directory

        Args:
            path: Directory path

        Returns:
            Create result dict
        """
        encoded_path = self._encode_path(path)
        endpoint = f"/files?action=CreateDir&path={encoded_path}"
        return self.client.request(endpoint)

    def create_file(self, path: str) -> Dict[str, Any]:
        """
        Create file

        Args:
            path: File path

        Returns:
            Create result dict
        """
        encoded_path = self._encode_path(path)
        endpoint = f"/files?action=CreateFile&path={encoded_path}"
        return self.client.request(endpoint)

    def delete_dir(self, path: str) -> Dict[str, Any]:
        """
        Delete directory (move to recycle bin)

        Args:
            path: Directory path

        Returns:
            Delete result dict
        """
        encoded_path = self._encode_path(path)
        endpoint = f"/files?action=DeleteDir&path={encoded_path}"
        return self.client.request(endpoint)

    def delete_file(self, path: str) -> Dict[str, Any]:
        """
        Delete file (move to recycle bin)

        Args:
            path: File path

        Returns:
            Delete result dict
        """
        encoded_path = self._encode_path(path)
        endpoint = f"/files?action=DeleteFile&path={encoded_path}"
        return self.client.request(endpoint)

    def get_file_access(self, filename: str) -> Dict[str, Any]:
        """
        Get file permissions

        Args:
            filename: File path

        Returns:
            Permission info dict, containing chmod and chown
        """
        encoded_filename = self._encode_path(filename)
        endpoint = f"/files?action=GetFileAccess&filename={encoded_filename}"
        return self.client.request(endpoint)

    def set_file_access(self, filename: str, access: str, user: str = "www",
                        group: str = "www", all_files: bool = False) -> Dict[str, Any]:
        """
        Set file permissions

        Args:
            filename: File path
            access: Permission code (e.g. 755, 644)
            user: Owner username (default www)
            group: Group name (default www)
            all_files: Whether to recursively set subdirectories and files

        Returns:
            Set result dict
        """
        # aaPanel SetFileAccess API requires filename, access, user, group parameters
        # Note: user and group must be provided together, otherwise will fail
        params = {
            "filename": filename,
            "access": access,
            "user": user,
            "group": group
        }
        if all_files:
            params["all"] = "1"

        endpoint = f"/files?action=SetFileAccess"
        return self.client.request(endpoint, params)

    # ==================== Convenience Methods ====================

    def read_file(self, path: str) -> str:
        """
        Convenience method: Read file content directly as string

        Args:
            path: File path

        Returns:
            File content string
        """
        result = self.get_file_body(path)
        if result.get('status') or result.get('only_read') is False:
            return result.get('data', '')
        raise Exception(result.get('msg', 'Failed to read file'))

    def write_file(self, path: str, content: str, encoding: str = "utf-8") -> bool:
        """
        Convenience method: Write file content

        Args:
            path: File path
            content: File content
            encoding: File encoding

        Returns:
            Whether successful
        """
        # Get current file info to get st_mtime
        try:
            file_info = self.get_file_body(path)
            st_mtime = file_info.get('st_mtime')
        except:
            st_mtime = None

        result = self.save_file_body(path, content, encoding, st_mtime)
        return result.get('status', False)

    def list_dir(self, path: str = "/www") -> Dict[str, List]:
        """
        Convenience method: Get directory list

        Args:
            path: Directory path

        Returns:
            Dict containing directories and files
        """
        result = self.get_dir(path)
        return {
            'directories': result.get('dir', []),
            'files': result.get('files', []),
            'path': result.get('path', path)
        }


class FilesClientManager:
    """File client manager - multi-server support"""

    def __init__(self):
        self._clients: Dict[str, FilesClient] = {}

    def get_client(self, server_name: str = None) -> FilesClient:
        """
        Get file client

        Args:
            server_name: Server name

        Returns:
            FilesClient instance
        """
        if server_name is None:
            server_name = "_default"

        if server_name not in self._clients:
            self._clients[server_name] = FilesClient(server_name if server_name != "_default" else None)

        return self._clients[server_name]

    def list_servers(self) -> List[str]:
        """List all available servers"""
        config = get_servers()
        return [s.get('name') for s in config] if config else []
