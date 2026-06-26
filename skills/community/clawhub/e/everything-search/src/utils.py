#!/usr/bin/env python3
"""
Utility functions for Everything Search.
"""

import urllib.parse
import socket
from typing import Optional


def format_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB", "256 KB")
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def encode_keyword(keyword: str) -> str:
    """
    URL-encode a search keyword (handles Chinese characters).
    
    Args:
        keyword: Search keyword (can contain Chinese)
        
    Returns:
        URL-encoded keyword
    """
    return urllib.parse.quote(keyword)


def check_connection(host: str = "127.0.0.1", port: int = 2853, timeout: int = 3) -> bool:
    """
    Check if Everything HTTP Server is accessible.
    
    Args:
        host: Server host
        port: Server port
        timeout: Connection timeout in seconds
        
    Returns:
        True if connection successful, False otherwise
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            # Try HTTP request
            import urllib.request
            req = urllib.request.Request(f"http://{host}:{port}/")
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.status == 200
        return False
        
    except Exception:
        return False


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension without dot (e.g., "jpg", "pdf")
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[-1].lower()
    return ""


def is_image_file(filename: str) -> bool:
    """Check if file is an image."""
    image_extensions = {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"}
    return get_file_extension(filename) in image_extensions


def is_document_file(filename: str) -> bool:
    """Check if file is a document."""
    doc_extensions = {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "md", "txt"}
    return get_file_extension(filename) in doc_extensions


def is_archive_file(filename: str) -> bool:
    """Check if file is an archive."""
    archive_extensions = {"zip", "rar", "7z", "tar", "gz", "bz2"}
    return get_file_extension(filename) in archive_extensions
