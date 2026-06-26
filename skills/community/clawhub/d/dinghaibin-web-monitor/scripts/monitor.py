#!/usr/bin/env python3
"""
Web Monitor - Track web pages for changes
Uses only standard library - no external dependencies required
"""

import argparse
import hashlib
import json
import os
import sys
import time
import re
from pathlib import Path
from datetime import datetime
import ssl
from urllib.request import urlopen, Request
from urllib.error import URLError


def fetch_page(url, selector=None):
    """Fetch page content, optionally extracting specific element."""
    try:
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        # Create SSL context that doesn't verify certificates
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urlopen(req, timeout=30, context=ctx) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            
            if selector:
                # Simple regex-based selector (class or id)
                # This is a basic implementation - for production use beautifulsoup
                if selector.startswith('.'):
                    class_name = selector[1:]
                    match = re.search(rf'<[^>]+class="[^"]*\b{class_name}\b[^"]*"[^>]*>(.*?)</[^>]+>', content, re.DOTALL)
                    if match:
                        # Strip HTML tags from matched content
                        text = re.sub(r'<[^>]+>', '', match.group(1))
                        return text.strip()
                elif selector.startswith('#'):
                    id_name = selector[1:]
                    match = re.search(rf'<[^>]+id="{id_name}"[^>]*>(.*?)</[^>]+>', content, re.DOTALL)
                    if match:
                        text = re.sub(r'<[^>]+>', '', match.group(1))
                        return text.strip()
                print(f"Warning: Simple selector '{selector}' not found, using full content")
            return content
    except URLError as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def compute_hash(content):
    """Compute SHA256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def save_content(path, data):
    """Save content metadata to file."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def load_content(path):
    """Load previous content metadata."""
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None


def monitor(args):
    """Main monitoring logic."""
    # Initial fetch
    content = fetch_page(args.url, args.selector)
    if not content:
        return 1
    
    current_hash = compute_hash(content)
    data = {
        'url': args.url,
        'selector': args.selector,
        'hash': current_hash,
        'content': content if not args.hash_only else None,
        'last_check': datetime.now().isoformat()
    }
    
    # Save current state
    if args.output:
        save_content(args.output, data)
        print(f"Content saved to {args.output}")
        print(f"Hash: {current_hash[:16]}...")
    
    # Compare with previous
    if args.compare:
        prev = load_content(args.compare)
        if prev:
            if prev['hash'] == current_hash:
                print("No changes detected")
                return 0
            else:
                print("CHANGE DETECTED!")
                print(f"Previous: {prev['hash'][:16]}...")
                print(f"Current:  {current_hash[:16]}...")
                if args.notify:
                    os.system(args.notify)
                return 2
        else:
            print(f"No previous data to compare (file: {args.compare})")
    
    # Watch mode
    if args.watch:
        interval = args.interval
        print(f"Watching {args.url} every {interval}s. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(interval)
                new_content = fetch_page(args.url, args.selector)
                if new_content:
                    new_hash = compute_hash(new_content)
                    if new_hash != current_hash:
                        print(f"\n[{datetime.now().isoformat()}] CHANGE DETECTED!")
                        if args.notify:
                            os.system(args.notify)
                        current_hash = new_hash
                        data['hash'] = new_hash
                        data['content'] = new_content if not args.hash_only else None
                        data['last_check'] = datetime.now().isoformat()
                        if args.output:
                            save_content(args.output, data)
        except KeyboardInterrupt:
            print("\nStopped")
    
    return 0


def main():
    parser = argparse.ArgumentParser(description='Monitor web pages for changes')
    parser.add_argument('--url', required=True, help='URL to monitor')
    parser.add_argument('--selector', help='CSS selector to monitor (optional)')
    parser.add_argument('--output', help='Save content to file')
    parser.add_argument('--compare', help='Compare against previous content file')
    parser.add_argument('--watch', action='store_true', help='Continuous monitoring mode')
    parser.add_argument('--interval', type=int, default=3600, help='Check interval in seconds')
    parser.add_argument('--notify', help='Command to run on change')
    parser.add_argument('--hash-only', action='store_true', help='Only store hash, not full content')
    
    args = parser.parse_args()
    return monitor(args)


if __name__ == '__main__':
    sys.exit(main())
