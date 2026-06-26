#!/usr/bin/env python3
"""
123pan WebDAV Upload + Direct Link Generator
Upload via WebDAV, then use API to get file ID and generate direct link
Usage: python upload_webdav_link.py --file /path/to/file [--remote-folder folder_name]
"""

import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path

# Add skill path for imports (动态路径)
sys.path.insert(0, str(Path(__file__).parent))
import upload as pan123_api

# 检测 rclone 路径：环境变量 > 系统 PATH > 默认本地路径
RCLONE_BIN = os.environ.get("RCLONE_BIN") or subprocess.run(["which", "rclone"], capture_output=True, text=True).stdout.strip() or os.path.expanduser("~/.openclaw/rclone-v1.73.2-linux-amd64/rclone")

# 支持隔离的 rclone 配置（避免读取 ~/.config/rclone/rclone.conf）
RCLONE_CONFIG = os.environ.get("RCLONE_CONFIG")

REMOTE_NAME = "123pan-webdav"


def get_rclone_env():
    """获取 rclone 环境变量，支持配置隔离"""
    env = os.environ.copy()
    if RCLONE_CONFIG:
        env["RCLONE_CONFIG"] = RCLONE_CONFIG
        print(f"Using isolated rclone config: {RCLONE_CONFIG}")
    return env


def format_size(size_bytes: float) -> str:
    """Format bytes to human readable string."""
    if size_bytes < 0:
        return "Unknown"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
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


def upload_with_rclone(local_path: str, remote_path: str) -> bool:
    """Upload file with rclone."""
    local_path = Path(local_path)
    file_size = local_path.stat().st_size
    start_time = time.time()
    
    print(f"[WebDAV Upload] {local_path.name}")
    print(f"Size: {format_size(file_size)}")
    print(f"Remote folder: {remote_path or 'root'}")
    print("-" * 60)
    
    cmd = [
        RCLONE_BIN,
        'copy',
        str(local_path),
        f'{REMOTE_NAME}:{remote_path}',
        '-P',
        '--stats', '1s'
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=get_rclone_env()
        )
        
        for line in process.stdout:
            line = line.strip()
            if line and ('%' in line or 'Transferred' in line or 'Transferring' in line):
                print(f"\r{line[:80]}", end='', flush=True)
        
        process.wait()
        print()  # New line
        
        if process.returncode == 0:
            elapsed = time.time() - start_time
            avg_speed = file_size / elapsed if elapsed > 0 else 0
            print(f"Upload complete! Time: {format_time(elapsed)}, Speed: {format_size(avg_speed)}/s")
            return True
        else:
            print(f"Upload failed with exit code: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return False


def find_file_by_name(folder_id: int, filename: str, max_retries: int = 30) -> dict:
    """Find file in folder by name using API."""
    import requests
    
    for attempt in range(max_retries):
        try:
            resp = requests.get(
                f"{pan123_api.API_BASE}/api/v1/file/list",
                headers=pan123_api.get_headers(),
                params={
                    "parentFileId": folder_id,
                    "page": 0,
                    "limit": 100,
                    "orderBy": "file_id",
                    "orderDirection": "desc"
                },
                timeout=30
            )
            resp.raise_for_status()
            result = resp.json()
            
            if result.get("code") != 0:
                print(f"API Error: {result.get('message')}")
                return None
            
            # Search for file by name
            for file in result.get("data", {}).get("fileList", []):
                if file.get("filename") == filename:
                    return file
            
            # File not found, wait and retry (might be indexing)
            if attempt < max_retries - 1:
                if attempt % 5 == 0:
                    print(f"  File not found yet, waiting... (attempt {attempt + 1}/{max_retries})")
                time.sleep(3)
            
        except Exception as e:
            print(f"  Error finding file: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
    
    return None


def get_short_direct_link(file_id: int) -> str:
    """Generate short direct link using fileID."""
    user_id = pan123_api.get_user_id_from_token()
    if not user_id:
        # Try to get from API
        try:
            direct_link = pan123_api.get_direct_link(file_id)
            parts = direct_link.split(".")
            if parts:
                user_id = parts[0].split("//")[-1]
        except:
            pass
    return f"https://{user_id}.v.123pan.cn/{user_id}/{file_id}"


def resolve_folder_id(folder_name: str) -> tuple:
    """Resolve folder name to folder ID and search paths."""
    # Return list of folder IDs to search
    folder_ids = []
    
    # Always search root
    folder_ids.append(0)
    
    # Search configured folder
    config_folder = int(pan123_api.get_config("folder_id", "PAN123_DIRECT_FOLDER_ID", "0"))
    if config_folder != 0:
        folder_ids.append(config_folder)
    
    # Try to find folder by name using API
    import requests
    try:
        resp = requests.get(
            f"{pan123_api.API_BASE}/api/v1/file/list",
            headers=pan123_api.get_headers(),
            params={
                "parentFileId": 0,
                "page": 0,
                "limit": 100,
                "orderBy": "file_id",
                "orderDirection": "asc"
            },
            timeout=30
        )
        result = resp.json()
        
        if result.get("code") == 0:
            for file in result.get("data", {}).get("fileList", []):
                if file.get("type") == 1:  # folder
                    # If folder_name matches, use it
                    if folder_name and file.get("filename") == folder_name:
                        folder_ids.insert(0, file.get("fileID"))  # Prioritize exact match
                    # Also check if it's the openclaw folder
                    if "openclaw" in file.get("filename", "").lower():
                        folder_ids.append(file.get("fileID"))
    except Exception as e:
        print(f"Warning: Could not list folders: {e}")
    
    # Remove duplicates while preserving order
    seen = set()
    unique_ids = []
    for fid in folder_ids:
        if fid not in seen:
            seen.add(fid)
            unique_ids.append(fid)
    
    return unique_ids


def main():
    parser = argparse.ArgumentParser(
        description="Upload file via WebDAV and get direct link via API"
    )
    parser.add_argument("--file", required=True, help="Path to file to upload")
    parser.add_argument("--remote-folder", default="", 
                        help="Remote folder name (must exist in 123pan)")
    parser.add_argument("--link-type", choices=["short", "direct", "share"], default="short",
                        help="Type of link to generate (default: short)")
    args = parser.parse_args()
    
    local_path = Path(args.file)
    if not local_path.exists():
        print(f"Error: File not found: {local_path}", file=sys.stderr)
        sys.exit(1)
    
    # Step 1: Upload via WebDAV
    print("\n" + "=" * 60)
    print("STEP 1: Upload via WebDAV")
    print("=" * 60)
    
    if not upload_with_rclone(str(local_path), args.remote_folder):
        print("Upload failed!")
        sys.exit(1)
    
    # Step 2: Find file via API
    print("\n" + "=" * 60)
    print("STEP 2: Locate file via API")
    print("=" * 60)
    
    folder_ids = resolve_folder_id(args.remote_folder)
    print(f"Searching in folders: {folder_ids}")
    
    file_info = None
    for folder_id in folder_ids:
        print(f"  Searching in folder ID: {folder_id}...")
        file_info = find_file_by_name(folder_id, local_path.name)
        if file_info:
            print(f"  Found in folder {folder_id}!")
            break
    
    if not file_info:
        print(f"Error: Could not find uploaded file '{local_path.name}' via API")
        print("The file may have been uploaded but not yet indexed.")
        print("You can manually get the link from 123pan web interface.")
        sys.exit(1)
    
    file_id = file_info.get("fileID")
    file_size = file_info.get("size", 0)
    
    print(f"Found file: ID={file_id}, Size={format_size(file_size)}")
    
    # Step 3: Generate link
    print("\n" + "=" * 60)
    print("STEP 3: Generate Direct Link")
    print("=" * 60)
    
    try:
        if args.link_type == "short":
            link = get_short_direct_link(file_id)
            link_type_str = "short_direct_link"
        elif args.link_type == "direct":
            link = pan123_api.get_direct_link(file_id)
            link_type_str = "direct_link"
        else:  # share
            link = pan123_api.create_share_link(file_id, local_path.name)
            link_type_str = "share_link"
        
        result = {
            "success": True,
            "file_id": file_id,
            "filename": local_path.name,
            "size": file_size,
            "link": link,
            "link_type": link_type_str,
            "upload_method": "webdav",
            "remote_folder": args.remote_folder or "root"
        }
        
        print(f"\nLink generated successfully!")
        print("-" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error generating link: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
