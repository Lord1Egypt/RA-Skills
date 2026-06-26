#!/usr/bin/env python3
"""
aaPanel File Download Script

Features:
- Download files from URL to specified server directory
- Support waiting for download completion
- Display download progress

API Reference:
- /files?action=DownloadFile - Initiate download
- /task?action=get_task_lists - Query task progress
"""

import sys
import time
import json
import argparse
from pathlib import Path

# Add parent directory to sys.path to support importing bt_common
_script_dir = Path(__file__).parent
_skill_root = _script_dir.parent
if (_skill_root / "bt_common").exists():
    sys.path.insert(0, str(_skill_root))
else:
    sys.path.insert(0, str(_skill_root.parent))

from bt_common.bt_client import BtClient, BtClientManager
from bt_common.config import get_servers


def get_client(server_name: str = None) -> BtClient:
    """Get aaPanel client"""
    if server_name:
        servers = get_servers()
        for server in servers:
            name = server.name if hasattr(server, 'name') else server.get('name')
            if name == server_name:
                config = {
                    'name': server.name if hasattr(server, 'name') else server.get('name'),
                    'host': server.host if hasattr(server, 'host') else server.get('host'),
                    'token': server.token if hasattr(server, 'token') else server.get('token'),
                    'timeout': server.timeout if hasattr(server, 'timeout') else server.get('timeout', 10000),
                    'verify_ssl': server.verify_ssl if hasattr(server, 'verify_ssl') else server.get('verify_ssl', True)
                }
                return BtClient(
                    name=config['name'],
                    host=config['host'],
                    token=config['token'],
                    timeout=config['timeout'],
                    verify_ssl=config['verify_ssl']
                )
        raise ValueError(f"Server not found: {server_name}")
    else:
        manager = BtClientManager()
        return manager.get_client()


def format_size(size_bytes: int) -> str:
    """Format file size"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f}MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f}GB"


def format_time(seconds: int) -> str:
    """Format time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        return f"{seconds // 3600}h {(seconds % 3600) // 60}m"


def cmd_download(args):
    """Download file"""
    client = get_client(args.server)
    
    # Auto-extract file name (if not specified)
    filename = args.filename
    if not filename:
        # Use urllib to parse URL
        from urllib.parse import urlparse
        parsed = urlparse(args.url)
        # Extract file name from path
        path_parts = parsed.path.rstrip('/').split('/')
        filename = path_parts[-1] if path_parts and path_parts[-1] else 'downloaded_file'
    
    # 1. Initiate download request
    print(f"\n📥 Starting download...")
    print(f"   URL: {args.url}")
    print(f"   Target path: {args.path}")
    print(f"   File name: {filename}")
    print()
    
    endpoint = "/files?action=DownloadFile"
    # Note: filename is a required parameter, otherwise API returns 500
    params = {
        "url": args.url,
        "path": args.path,
        "filename": filename,  # Required!
    }
    
    try:
        result = client.request(endpoint, params)
        if result.get('status'):
            print(f"✅ Download task added to queue")
        else:
            print(f"❌ Failed to add download task: {result.get('msg', 'Unknown error')}")
            return 1
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return 1
    
    # 2. If no wait required, return directly
    if not args.wait:
        print("\n💡 Use --wait parameter to wait for download completion")
        return 0
    
    # 3. Wait for download to complete
    print("\n⏳ Waiting for download to complete...")
    print("-" * 60)
    
    task_id = None
    last_progress = -1
    start_time = time.time()
    timeout = args.timeout or 600  # default 10 minutes timeout
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            print(f"\n❌ Download timed out ({timeout}s)")
            return 1
        
        # Query task list
        try:
            task_result = client.request("/task?action=get_task_lists", {"status": "-3"})
            tasks = task_result if isinstance(task_result, list) else []
            
            # Find download task
            download_task = None
            for task in tasks:
                if task.get('type') == '1' and args.url in task.get('shell', ''):
                    download_task = task
                    task_id = task.get('id')
                    break
            
            if not download_task:
                # Task may have completed, check if file exists
                time.sleep(1)
                continue
            
            # Display progress
            log = download_task.get('log', {})
            if isinstance(log, str):
                try:
                    log = json.loads(log) if log else {}
                except:
                    log = {}
            
            # Safely get values, handle string types
            def safe_int(val, default=0):
                try:
                    return int(float(val)) if val else default
                except (ValueError, TypeError):
                    return default
            
            def safe_float(val, default=0.0):
                try:
                    return float(val) if val else default
                except (ValueError, TypeError):
                    return default
            
            progress = safe_float(log.get('pre', 0), 0)
            speed = safe_int(log.get('speed', 0), 0)
            used = safe_int(log.get('used', 0), 0)
            total = safe_int(log.get('total', 0), 0)
            remaining = safe_int(log.get('time', 0), 0)
            status = download_task.get('status')
            
            # Build progress bar
            bar_length = 40
            filled = int(bar_length * progress / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            # Only update display when progress changes
            if progress != last_progress:
                last_progress = progress
                print(f"\r   [{bar}] {progress:.1f}% | "
                      f"{format_size(used)}/{format_size(total) if total else '???'} | "
                      f"{format_size(speed)}/s | "
                      f"Remaining: {format_time(remaining)} | "
                      f"Status: {'Downloading' if status == -1 else 'Waiting' if status == 0 else 'Completed'}", 
                      end='', flush=True)
            
            # Check if completed
            if status == 1 or progress >= 100:
                print()  # Newline
                print("-" * 60)
                print(f"✅ Download completed!")
                print(f"   File: {args.path}/{filename}")
                print(f"   Size: {format_size(total) if total else 'Unknown'}")
                print(f"   Time: {format_time(int(elapsed))}")
                return 0
            
            # Check if failed
            if status == -2:
                print()  # Newline
                print("-" * 60)
                print(f"❌ Download failed")
                return 1
            
            time.sleep(1)  # Refresh every second
            
        except Exception as e:
            print(f"\n❌ Failed to query progress: {e}")
            time.sleep(2)


def cmd_tasks(args):
    """View task list"""
    client = get_client(args.server)
    
    endpoint = "/task?action=get_task_lists"
    params = {"status": args.status if hasattr(args, 'status') else "-3"}
    
    try:
        result = client.request(endpoint, params)
        tasks = result if isinstance(result, list) else []
        
        if not tasks:
            print("📭 No tasks")
            return 0
        
        print(f"\n📋 Task list ({len(tasks)} total)")
        print("-" * 80)
        print(f"{'ID':<6} {'Type':<10} {'Name':<20} {'Status':<10} {'Progress':<10}")
        print("-" * 80)
        
        status_map = {
            -2: "❌ Failed",
            -1: "⏳ Running",
            0: "⏸️ Waiting",
            1: "✅ Completed"
        }
        
        type_map = {
            "1": "Download",
            "2": "Extract",
            "3": "Compress"
        }
        
        for task in tasks:
            task_id = task.get('id', 'N/A')
            task_type = type_map.get(str(task.get('type', '')), 'Unknown')
            task_name = task.get('name', 'N/A')[:18]
            task_status = status_map.get(task.get('status'), 'Unknown')
            
            log = task.get('log', {})
            if isinstance(log, str):
                log = {}
            progress = f"{log.get('pre', 0):.1f}%" if log else 'N/A'
            
            print(f"{task_id:<6} {task_type:<10} {task_name:<20} {task_status:<10} {progress:<10}")
        
        print("-" * 80)
        return 0
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return 1


def cmd_cancel(args):
    """Cancel task"""
    client = get_client(args.server)
    
    endpoint = "/task?action=remove_task"
    params = {"id": args.task_id}
    
    try:
        result = client.request(endpoint, params)
        if result.get('status'):
            print(f"✅ Task {args.task_id} cancelled")
            return 0
        else:
            print(f"❌ Cancellation failed: {result.get('msg', 'Unknown error')}")
            return 1
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="aaPanel File Download Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download WordPress to specified directory (wait for completion)
  python3 download.py -s "Internal 172" download \\
      --url "https://cn.wordpress.org/latest-zh_CN.zip" \\
      --path "/www/test" \\
      --filename "wordpress.zip" \\
      --wait

  # View current task list
  python3 download.py -s "Internal 172" tasks

  # Cancel task
  python3 download.py -s "Internal 172" cancel --task-id 1
        """
    )
    
    # Global parameters
    parser.add_argument('-s', '--server', help='Server name')
    
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')
    
    # download command
    download_parser = subparsers.add_parser('download', help='Download file')
    download_parser.add_argument('--url', required=True, help='Download URL')
    download_parser.add_argument('--path', required=True, help='Target path')
    download_parser.add_argument('--filename', help='Save file name (optional, extracted from URL by default)')
    download_parser.add_argument('--wait', action='store_true', help='Wait for download completion')
    download_parser.add_argument('--timeout', type=int, default=600, help='Timeout (seconds, default 600)')
    download_parser.set_defaults(func=cmd_download)
    
    # tasks command
    tasks_parser = subparsers.add_parser('tasks', help='View task list')
    tasks_parser.add_argument('--status', default='-3', help='Task status (-3=all, -1=running, 0=waiting, 1=completed)')
    tasks_parser.set_defaults(func=cmd_tasks)
    
    # cancel command
    cancel_parser = subparsers.add_parser('cancel', help='Cancel task')
    cancel_parser.add_argument('--task-id', required=True, type=int, help='Task ID')
    cancel_parser.set_defaults(func=cmd_cancel)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
