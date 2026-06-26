#!/usr/bin/env python3
"""
Background Download Skill - Main download logic
"""

import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime, timedelta, timezone

# Add ontology script path
ONTOLOGY_SCRIPT = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "skills", "ontology", "scripts", "ontology.py")
ONTOLGY_DIR = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace", "memory", "ontology")

def run_ontology_cmd(cmd):
    """Run ontology command and return parsed JSON"""
    full_cmd = f"python3 {ONTOLOGY_SCRIPT} {cmd}"
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Ontology command failed: {full_cmd}\n{result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Invalid JSON from ontology: {result.stdout}", file=sys.stderr)
        return None

def create_download_task(title, url, path, channel, max_retries=3):
    """Create a new DownloadTask entity in Ontology"""
    props = json.dumps({
        "title": title,
        "url": url,
        "path": path,
        "status": "pending",
        "retry_count": 0,
        "max_retries": max_retries,
        "created_by_channel": channel
    })
    cmd = f"create --type DownloadTask --props '{props}'"
    return run_ontology_cmd(cmd)

def update_task_status(task_id, status, retry_count=None):
    """Update task status in Ontology"""
    task = get_task(task_id)
    if not task:
        return None
    props = task['properties'].copy()
    props['status'] = status
    if retry_count is not None:
        props['retry_count'] = retry_count
    props_json = json.dumps(props)
    cmd = f"update --id {task_id} --props '{props_json}'"
    return run_ontology_cmd(cmd)

def get_task(task_id):
    """Get task by ID"""
    cmd = f"get --id {task_id}"
    return run_ontology_cmd(cmd)

def list_tasks(status_filter=None):
    """List all tasks, optionally filtered by status"""
    if status_filter:
        cmd = f"query --type DownloadTask --where '{{\"status\":\"{status_filter}\"}}'"
    else:
        cmd = f"list --type DownloadTask"
    result = run_ontology_cmd(cmd)
    return result if isinstance(result, list) else [result] if result else []

def send_notification(channel, message):
    """Send notification to original channel"""
    # Channel format: "type:target" e.g. "feishu:direct:ou_xxxxxxx"
    # or "feishu:chat:oc_xxxxxxx"
    parts = channel.split(":", 2)
    if len(parts) < 2:
        print(f"Invalid channel format: {channel}", file=sys.stderr)
        return False
    channel_type = parts[0]
    target = ":".join(parts[1:])
    cmd = f"openclaw message send --channel {channel_type} --target {target} --message '{message}'"
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def do_download(task):
    """Perform the actual download with resume"""
    url = task['properties']['url']
    path = task['properties']['path']
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    
    # Use curl with resume
    cmd = f"curl -C - -L -o '{path}' '{url}'"
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def background_download(task_id):
    """Background download process - runs detached"""
    task = get_task(task_id)
    if not task:
        print(f"Task {task_id} not found", file=sys.stderr)
        return
    
    max_retries = task['properties']['max_retries']
    retry_count = task['properties'].get('retry_count', 0)
    channel = task['properties']['created_by_channel']
    title = task['properties']['title']
    
    # Mark as downloading
    update_task_status(task_id, 'downloading', retry_count)
    
    while retry_count < max_retries:
        retry_count += 1
        print(f"Attempt {retry_count}/{max_retries} for {title}")
        
        if do_download(task):
            # Success
            update_task_status(task_id, 'completed', retry_count)
            message = f"✅ Background download completed: **{title}**\nPath: `{task['properties']['path']}`"
            send_notification(channel, message)
            print("Download completed successfully")
            return
        else:
            # Failed, retry after 30s
            update_task_status(task_id, 'downloading', retry_count)
            if retry_count < max_retries:
                print(f"Download failed, retrying in 30s... ({retry_count}/{max_retries})")
                time.sleep(30)
    
    # All retries failed
    update_task_status(task_id, 'failed', retry_count)
    message = f"❌ Background download failed after {max_retries} retries: **{title}**\nURL: {task['properties']['url']}"
    send_notification(channel, message)
    print(f"Download failed after {max_retries} retries")

def cleanup_zombies(max_hours=2):
    """Mark stale downloading tasks as failed"""
    downloading = list_tasks('downloading')
    cleaned = 0
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_hours)
    for task in downloading:
        created = datetime.fromisoformat(task['created'])
        if created < cutoff:
            update_task_status(task['id'], 'failed')
            channel = task['properties']['created_by_channel']
            message = f"⚠️ Background download timed out (> {max_hours}h): **{task['properties']['title']}**"
            send_notification(channel, message)
            cleaned += 1
    print(f"Cleaned up {cleaned} zombie tasks")
    return cleaned

def archive_old(days=7):
    """Archive completed tasks older than N days"""
    completed = list_tasks('completed')
    archived = 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    for task in completed:
        updated = datetime.fromisoformat(task['updated'])
        if updated < cutoff:
            update_task_status(task['id'], 'archived', None)
            archived += 1
    print(f"Archived {archived} old completed tasks")
    return archived

def main():
    parser = argparse.ArgumentParser(description='Background Download Manager')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start new background download')
    start_parser.add_argument('--title', required=True, help='Download title')
    start_parser.add_argument('--url', required=True, help='Download URL')
    start_parser.add_argument('--path', required=True, help='Save path')
    start_parser.add_argument('--channel', required=True, help='Notification channel (type:target)')
    start_parser.add_argument('--max-retries', type=int, default=3, help='Maximum retries')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Check task status')
    status_parser.add_argument('--id', required=True, help='Task ID')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List download tasks')
    list_parser.add_argument('--status', help='Filter by status')
    
    # Archive command
    archive_parser = subparsers.add_parser('archive', help='Archive old completed tasks')
    archive_parser.add_argument('--days', type=int, default=7, help='Archive completed older than N days')
    
    # Cleanup-zombies command
    cleanup_parser = subparsers.add_parser('cleanup-zombies', help='Clean up stale downloading tasks')
    cleanup_parser.add_argument('--hours', type=int, default=2, help='Max hours before considered stale')
    
    args = parser.parse_args()
    
    if args.command == 'start':
        # Create task
        result = create_download_task(args.title, args.url, args.path, args.channel, args.max_retries)
        if not result:
            print("Failed to create download task", file=sys.stderr)
            sys.exit(1)
        task_id = result['id']
        print(f"Created download task: {task_id}")
        print(f"Title: {args.title}")
        print(f"Status: pending -> starting background download")
        
        # Double-fork to background
        pid = os.fork()
        if pid > 0:
            # Parent exits immediately
            print(f"Download started in background, task ID: {task_id}")
            sys.exit(0)
        # First child continues
        os.setsid()
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        # Second child does the download
        background_download(task_id)
        sys.exit(0)
    
    elif args.command == 'status':
        task = get_task(args.id)
        if not task:
            print(f"Task {args.id} not found")
            sys.exit(1)
        print(json.dumps(task, indent=2, ensure_ascii=False))
    
    elif args.command == 'list':
        tasks = list_tasks(args.status)
        print(json.dumps(tasks, indent=2, ensure_ascii=False))
    
    elif args.command == 'archive':
        archive_old(args.days)
    
    elif args.command == 'cleanup-zombies':
        cleanup_zombies(args.hours)

if __name__ == '__main__':
    main()
