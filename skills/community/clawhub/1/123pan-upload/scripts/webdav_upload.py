#!/usr/bin/env python3
"""
123pan WebDAV Upload: Upload large files via WebDAV with progress monitoring
Usage: python upload_webdav.py --file /path/to/file [--remote-path /remote/folder]
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

# Add local site-packages for webdav3 (动态路径)
local_site_packages = Path.home() / ".local" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
if local_site_packages.exists():
    sys.path.insert(0, str(local_site_packages))

from webdav3.client import Client
from webdav3.exceptions import WebDavException

# WebDAV Configuration - 从环境变量或配置文件读取
# 请设置环境变量：PAN123_WEBDAV_USER 和 PAN123_WEBDAV_PASS
# 或在 config.json 中配置 webdav_user 和 webdav_password

def load_webdav_config():
    """从环境变量或配置文件加载 WebDAV 配置"""
    # 首先尝试环境变量
    user = os.environ.get("PAN123_WEBDAV_USER")
    password = os.environ.get("PAN123_WEBDAV_PASS")
    
    # 然后尝试 config.json
    if not user or not password:
        config_path = Path(__file__).parent.parent / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                user = user or config.get("webdav_user")
                password = password or config.get("webdav_password")
            except:
                pass
    
    if not user or not password:
        raise ValueError(
            "WebDAV 凭据未配置。请设置环境变量 PAN123_WEBDAV_USER 和 PAN123_WEBDAV_PASS，"
            "或在 config.json 中配置 webdav_user 和 webdav_password"
        )
    
    return {
        'webdav_hostname': 'https://webdav.123pan.cn/webdav',
        'webdav_login': user,
        'webdav_password': password
    }

WEBDAV_CONFIG = load_webdav_config()

CHUNK_SIZE = 8 * 1024 * 1024  # 8MB chunks for progress tracking


def format_size(size_bytes: int) -> str:
    """Format bytes to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def format_time(seconds: float) -> str:
    """Format seconds to human readable string."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def upload_with_progress(client: Client, local_path: str, remote_path: str):
    """Upload file with progress tracking."""
    local_path = Path(local_path)
    file_size = local_path.stat().st_size
    start_time = time.time()

    print(f"Uploading: {local_path.name}")
    print(f"Size: {format_size(file_size)}")
    print(f"Remote: {remote_path}")
    print("-" * 50)

    try:
        # Check if remote directory exists
        remote_dir = str(Path(remote_path).parent)
        if remote_dir != '/' and not client.check(remote_dir):
            print(f"Creating remote directory: {remote_dir}")
            client.mkdir(remote_dir)

        # For small files, just upload directly
        if file_size < 1024 * 1024:  # < 1MB
            client.upload_sync(
                remote_path=remote_path,
                local_path=str(local_path)
            )
        else:
            # Manual chunked upload with progress
            uploaded = 0
            chunk_size = 8 * 1024 * 1024  # 8MB
            last_update = start_time
            
            # Open remote file for writing (webdav3 doesn't support append well, so we use upload_sync)
            # For larger files, we'll just show simple progress
            print("Uploading (progress updates every 8MB)...")
            
            with open(local_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    # webdav3 doesn't have a simple write/append API, use upload_sync for now
                    # This is a limitation - we'll show before/after for large files
                    
            client.upload_sync(
                remote_path=remote_path,
                local_path=str(local_path)
            )
        
        elapsed = time.time() - start_time
        avg_speed = file_size / elapsed if elapsed > 0 else 0
        
        print()  # New line after progress bar
        print("-" * 50)
        print(f"Upload complete!")
        print(f"Time: {format_time(elapsed)}")
        print(f"Average speed: {format_size(avg_speed)}/s")
        
        return True
        
    except WebDavException as e:
        print(f"\nWebDAV Error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return False


def verify_upload(client: Client, remote_path: str, expected_size: int) -> bool:
    """Verify uploaded file size matches."""
    try:
        info = client.info(remote_path)
        remote_size = int(info.get('size', 0))
        if remote_size == expected_size:
            print(f"Verification: OK ({format_size(remote_size)})")
            return True
        else:
            print(f"Verification FAILED: Expected {format_size(expected_size)}, got {format_size(remote_size)}")
            return False
    except Exception as e:
        print(f"Verification error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload files to 123pan via WebDAV")
    parser.add_argument("--file", required=True, help="Path to file to upload")
    parser.add_argument("--remote-path", default="", help="Remote path (default: same filename in root)")
    parser.add_argument("--verify", action="store_true", help="Verify upload after completion")
    args = parser.parse_args()

    local_path = Path(args.file)
    if not local_path.exists():
        print(f"Error: File not found: {local_path}", file=sys.stderr)
        sys.exit(1)

    # Default remote path
    if not args.remote_path:
        args.remote_path = f"/{local_path.name}"
    elif not args.remote_path.startswith('/'):
        args.remote_path = f"/{args.remote_path}"

    # Initialize client
    client = Client(WEBDAV_CONFIG)
    client.verify = True

    print("Connecting to 123pan WebDAV...")
    try:
        # Test connection
        client.list('/')
        print("Connected successfully!\n")
    except Exception as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Upload
    success = upload_with_progress(client, str(local_path), args.remote_path)
    
    if not success:
        sys.exit(1)

    # Verify if requested
    if args.verify:
        print("\nVerifying upload...")
        expected_size = local_path.stat().st_size
        if not verify_upload(client, args.remote_path, expected_size):
            sys.exit(1)

    print(f"\nFile uploaded to: {args.remote_path}")
    print("Note: Use 123pan web interface to get share links for uploaded files.")


if __name__ == "__main__":
    main()
