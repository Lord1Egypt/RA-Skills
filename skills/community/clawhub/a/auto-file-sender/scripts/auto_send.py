#!/usr/bin/env python3
"""
Auto File Sender - Watch workspace and automatically send files to Feishu

Usage:
    python3 auto_send.py [options]

Options:
    --watch PATH       Directory to watch (default: /root/.openclaw/workspace)
    --recipient ID     Target recipient open_id
    --pattern PATTERN  File pattern to match (default: *)
    --once             Send existing files and exit (don't watch)
    --delay SECONDS    Delay between sends (default: 1)

Examples:
    # Watch and auto-send all new PDFs
    python3 auto_send.py --pattern "*.pdf" --recipient USER_ID

    # One-time send of all docx files
    python3 auto_send.py --pattern "*.docx" --once

    # Watch for any file changes
    python3 auto_send.py --watch /path/to/dir --recipient USER_ID
"""

import os
import sys
import time
import argparse
import json
from pathlib import Path
from datetime import datetime

# Default configuration
DEFAULT_WORKSPACE = "/root/.openclaw/workspace"
DEFAULT_DELAY = 1  # seconds between sends
SUPPORTED_EXTENSIONS = {
    '.docx', '.doc', '.pdf', '.txt', '.md',
    '.jpg', '.jpeg', '.png', '.gif', '.webp',
    '.xlsx', '.xls', '.csv',
    '.zip', '.tar', '.gz',
    '.mp3', '.mp4', '.wav',
    '.json', '.xml', '.yaml', '.yml'
}

MAX_FILE_SIZE_MB = 30


def log(message):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def get_file_size_mb(filepath):
    """Get file size in megabytes"""
    return os.path.getsize(filepath) / (1024 * 1024)


def is_supported_file(filepath):
    """Check if file type is supported for sending"""
    ext = Path(filepath).suffix.lower()
    return ext in SUPPORTED_EXTENSIONS


def should_send_file(filepath, min_age_seconds=5):
    """
    Check if file should be sent:
    - File must exist
    - File size must be under limit
    - File type must be supported
    - File must be stable (not being written)
    """
    if not os.path.exists(filepath):
        return False, "File does not exist"
    
    if not os.path.isfile(filepath):
        return False, "Not a file"
    
    # Check size
    size_mb = get_file_size_mb(filepath)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large ({size_mb:.1f}MB > {MAX_FILE_SIZE_MB}MB)"
    
    # Check extension
    if not is_supported_file(filepath):
        return False, "Unsupported file type"
    
    # Check if file is stable (not being written)
    try:
        initial_size = os.path.getsize(filepath)
        initial_mtime = os.path.getmtime(filepath)
        time.sleep(0.5)
        
        if os.path.getsize(filepath) != initial_size:
            return False, "File is still being written"
        
        # Check minimum age
        age_seconds = time.time() - initial_mtime
        if age_seconds < min_age_seconds:
            return False, f"File too new ({age_seconds:.1f}s < {min_age_seconds}s)"
            
    except OSError:
        return False, "Cannot access file"
    
    return True, "OK"


def scan_directory(directory, pattern="*"):
    """Scan directory for matching files"""
    files = []
    try:
        for item in Path(directory).glob(pattern):
            if item.is_file():
                files.append(str(item.absolute()))
    except Exception as e:
        log(f"Error scanning directory: {e}")
    
    return sorted(files)


def generate_send_command(filepath, recipient=None, message=None):
    """Generate the message.send tool call"""
    filename = os.path.basename(filepath)
    
    cmd = {
        "action": "send",
        "filePath": filepath,
        "filename": filename
    }
    
    if recipient:
        cmd["target"] = recipient
    
    if message:
        cmd["message"] = message
    
    return cmd


def print_send_instructions(files, recipient=None):
    """Print instructions for sending files"""
    print("\n" + "="*60)
    print("AUTO FILE SENDER - Send Instructions")
    print("="*60 + "\n")
    
    print(f"Found {len(files)} file(s) to send:\n")
    
    for i, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)
        size_mb = get_file_size_mb(filepath)
        print(f"  {i}. {filename} ({size_mb:.1f}MB)")
    
    print("\n" + "-"*60)
    print("Use the following tool calls to send files:")
    print("-"*60 + "\n")
    
    for filepath in files:
        cmd = generate_send_command(filepath, recipient)
        print(json.dumps(cmd, indent=2, ensure_ascii=False))
        print()
    
    print("="*60)


def watch_directory(directory, recipient, pattern, delay=1):
    """Watch directory for new files and print send commands"""
    log(f"Starting watch mode on: {directory}")
    log(f"Pattern: {pattern}")
    log(f"Recipient: {recipient or 'current user'}")
    log("Press Ctrl+C to stop\n")
    
    # Track sent files to avoid duplicates
    sent_files = set()
    
    try:
        while True:
            files = scan_directory(directory, pattern)
            
            for filepath in files:
                if filepath in sent_files:
                    continue
                
                should_send, reason = should_send_file(filepath)
                
                if should_send:
                    filename = os.path.basename(filepath)
                    size_mb = get_file_size_mb(filepath)
                    
                    log(f"New file detected: {filename} ({size_mb:.1f}MB)")
                    
                    # Print the send command
                    cmd = generate_send_command(filepath, recipient)
                    print("\n" + "-"*40)
                    print("SEND COMMAND:")
                    print("-"*40)
                    print(json.dumps(cmd, indent=2, ensure_ascii=False))
                    print("-"*40 + "\n")
                    
                    sent_files.add(filepath)
                    time.sleep(delay)
                
            time.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        log("\nWatch mode stopped")
        log(f"Total files detected: {len(sent_files)}")


def send_once(directory, recipient, pattern):
    """Send all matching files once and exit"""
    log(f"Scanning directory: {directory}")
    log(f"Pattern: {pattern}\n")
    
    files = scan_directory(directory, pattern)
    
    if not files:
        log("No matching files found")
        return
    
    # Filter files that can be sent
    valid_files = []
    for filepath in files:
        should_send, reason = should_send_file(filepath)
        if should_send:
            valid_files.append(filepath)
        else:
            filename = os.path.basename(filepath)
            log(f"Skipping {filename}: {reason}")
    
    if not valid_files:
        log("No valid files to send")
        return
    
    print_send_instructions(valid_files, recipient)


def main():
    parser = argparse.ArgumentParser(
        description="Auto File Sender - Watch and send files to Feishu"
    )
    parser.add_argument(
        "--watch",
        default=DEFAULT_WORKSPACE,
        help=f"Directory to watch (default: {DEFAULT_WORKSPACE})"
    )
    parser.add_argument(
        "--recipient",
        help="Target recipient open_id"
    )
    parser.add_argument(
        "--pattern",
        default="*",
        help="File pattern to match (default: *)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Send existing files and exit (don't watch)"
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=DEFAULT_DELAY,
        help=f"Delay between sends in seconds (default: {DEFAULT_DELAY})"
    )
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.watch):
        log(f"Error: Directory not found: {args.watch}")
        sys.exit(1)
    
    if args.once:
        send_once(args.watch, args.recipient, args.pattern)
    else:
        watch_directory(args.watch, args.recipient, args.pattern, args.delay)


if __name__ == "__main__":
    main()
