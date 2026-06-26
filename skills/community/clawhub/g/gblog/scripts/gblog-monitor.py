#!/usr/bin/env python3
"""
gblog-monitor - Monitor Blogger blog for changes
Polls for new posts, updates, and comments
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from gblog import api_request, get_access_token, Colors, print_info, print_success, print_warning

CONFIG_DIR = Path.home() / ".config" / "gblog"
STATE_FILE = CONFIG_DIR / "monitor_state.json"

def load_state():
    """Load monitoring state"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {'known_posts': {}, 'last_check': None}

def save_state(state):
    """Save monitoring state"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def check_blog(blog_id, verbose=False):
    """Check blog for changes"""
    try:
        result = api_request(f"/blogs/{blog_id}/posts")
        posts = result.get('items', [])
        
        state = load_state()
        known_posts = state.get('known_posts', {})
        new_posts = []
        updated_posts = []
        
        for post in posts:
            post_id = post['id']
            post_info = {
                'id': post_id,
                'title': post['title'],
                'published': post['published'],
                'updated': post['updated'],
                'url': post['url'],
                'status': post.get('status', 'LIVE')
            }
            
            if post_id not in known_posts:
                new_posts.append(post_info)
            elif known_posts[post_id]['updated'] != post['updated']:
                updated_posts.append(post_info)
            
            known_posts[post_id] = post_info
        
        state['known_posts'] = known_posts
        state['last_check'] = datetime.now().isoformat()
        save_state(state)
        
        if new_posts:
            print(f"\n{Colors.GREEN}🆕 New Posts:{Colors.END}")
            for post in new_posts:
                print(f"   📄 {post['title']}")
                print(f"      URL: {post['url']}")
                print(f"      Status: {post['status']}")
        
        if updated_posts:
            print(f"\n{Colors.YELLOW}📝 Updated Posts:{Colors.END}")
            for post in updated_posts:
                print(f"   📄 {post['title']}")
                print(f"      Updated: {post['updated']}")
        
        if verbose and not new_posts and not updated_posts:
            print_info(f"No changes detected. {len(posts)} posts monitored.")
        
        return len(new_posts) + len(updated_posts)
        
    except Exception as e:
        print(f"{Colors.RED}✗ Error checking blog: {e}{Colors.END}")
        return 0

def main():
    parser = argparse.ArgumentParser(description='Monitor Blogger blog for changes')
    parser.add_argument('--blog-id', required=True, help='Blog ID to monitor')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds (default: 300)')
    parser.add_argument('--once', action='store_true', help='Check once and exit')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    print(f"🦖 gblog-monitor")
    print(f"Monitoring blog: {args.blog_id}")
    print(f"Interval: {args.interval} seconds")
    print(f"Press Ctrl+C to stop\n")
    
    if args.once:
        check_blog(args.blog_id, args.verbose)
    else:
        try:
            while True:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp}] Checking...", end=' ')
                changes = check_blog(args.blog_id, args.verbose)
                if changes == 0:
                    print("No changes")
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}⚠ Monitoring stopped{Colors.END}")

if __name__ == '__main__':
    main()
