#!/usr/bin/env python3
"""
123pan WebDAV Upload using rclone with progress tracking
Usage: python upload_rclone.py --file /path/to/file [--remote-path /folder]
"""

import os
import sys
import time
import subprocess
import argparse
import re
from pathlib import Path

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


def format_size(size_str: str) -> str:
    """Format size string."""
    return size_str.strip() if size_str else "Unknown"


def format_time(seconds: float) -> str:
    """Format seconds to human readable string."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds/60:.1f}m"
    else:
        return f"{seconds/3600:.1f}h"


def upload_with_progress(local_path: str, remote_path: str) -> bool:
    """Upload file with real-time progress using rclone."""
    local_path = Path(local_path)
    file_size = local_path.stat().st_size
    start_time = time.time()
    
    print(f"Uploading: {local_path.name}")
    print(f"Size: {file_size} bytes ({file_size / 1024 / 1024:.2f} MB)")
    print(f"Remote: {remote_path or 'root'}")
    print("-" * 60)
    
    # Build rclone command with progress
    cmd = [
        RCLONE_BIN,
        'copy',
        str(local_path),
        f'{REMOTE_NAME}:{remote_path}',
        '-P',  # Progress
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
        
        # Read and display output
        for line in process.stdout:
            line = line.strip()
            if line:
                # rclone progress format: *    long-file-name: 45% /1.234GBytes, 12.345 MBytes/s, 1m2s
                # Just print the line as-is since rclone handles the progress display
                if '%' in line or 'Bytes/s' in line:
                    print(f"\r{line[:80]}", end='', flush=True)
                elif 'Transferred' in line:
                    print(f"\n{line}")
                else:
                    print(line)
        
        process.wait()
        
        print()  # New line after progress
        
        if process.returncode == 0:
            elapsed = time.time() - start_time
            avg_speed = file_size / elapsed if elapsed > 0 else 0
            
            print("-" * 60)
            print(f"Upload complete!")
            print(f"Time: {format_time(elapsed)}")
            print(f"Average speed: {avg_speed / 1024 / 1024:.2f} MB/s")
            return True
        else:
            print(f"\nUpload failed with exit code: {process.returncode}")
            return False
            
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return False


def verify_upload(local_path: str, remote_path: str) -> bool:
    """Verify uploaded file size matches."""
    try:
        local_size = Path(local_path).stat().st_size
        remote_file = f'{REMOTE_NAME}:{remote_path}/{Path(local_path).name}' if remote_path else f'{REMOTE_NAME}:{Path(local_path).name}'
        
        # Get remote file info using rclone ls
        cmd = [RCLONE_BIN, 'lsjson', remote_file]
        result = subprocess.run(cmd, capture_output=True, text=True, env=get_rclone_env())
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            if data and len(data) > 0:
                remote_size = data[0].get('Size', 0)
                
                if remote_size == local_size:
                    print(f"Verification: OK ({local_size} bytes)")
                    return True
                else:
                    print(f"Verification FAILED: Expected {local_size}, got {remote_size}")
                    return False
        
        print("Verification: Could not verify (file may not exist)")
        return False
    except Exception as e:
        print(f"Verification error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload files to 123pan via WebDAV using rclone")
    parser.add_argument("--file", required=True, help="Path to file to upload")
    parser.add_argument("--remote-path", default="", help="Remote folder path (default: root)")
    parser.add_argument("--verify", action="store_true", help="Verify upload after completion")
    args = parser.parse_args()
    
    local_path = Path(args.file)
    if not local_path.exists():
        print(f"Error: File not found: {local_path}", file=sys.stderr)
        sys.exit(1)
    
    # Upload
    success = upload_with_progress(str(local_path), args.remote_path)
    
    if not success:
        sys.exit(1)
    
    # Verify if requested
    if args.verify:
        print("\nVerifying upload...")
        if not verify_upload(str(local_path), args.remote_path):
            sys.exit(1)
    
    remote_display = f"{args.remote_path}/{local_path.name}" if args.remote_path else local_path.name
    print(f"\nFile uploaded to: {remote_display}")
    print("Note: Use 123pan web interface to get share links for uploaded files.")


if __name__ == "__main__":
    main()
