#!/usr/bin/env python3
"""
update-blogger-full.py - Update all Blogger posts with full content
"""

import json
import time
from pathlib import Path
import sys

sys.path.insert(0, str(Path.home() / ".openclaw/workspace/skills/gblog/scripts"))
from gblog import api_request, print_success, print_error, print_info

BLOG_ID = "857323745498581946"
POSTS_JSON = Path.home() / ".openclaw/workspace/techrex-website/content/blog/posts.json"
FULL_DIR = Path.home() / ".openclaw/workspace/techrex-website/content/blog/blogger-html-full"

def get_blogger_post_mapping():
    """Get mapping of post titles to Blogger IDs"""
    result = api_request(f'/blogs/{BLOG_ID}/posts?maxResults=50')
    posts = result.get('items', [])
    
    mapping = {}
    for p in posts:
        # Use first 50 chars of title as key
        key = p['title'][:50]
        mapping[key] = p['id']
    return mapping

def find_blogger_id(post_title, mapping):
    """Find Blogger post ID by matching title"""
    post_key = post_title[:50]
    
    for key, post_id in mapping.items():
        # Check if titles match (accounting for truncation)
        if post_key in key or key in post_title:
            return post_id
    return None

def update_post(blog_id, post_id, html_content):
    """Update a blog post"""
    try:
        data = {'content': html_content}
        result = api_request(f'/blogs/{blog_id}/posts/{post_id}', method='PATCH', data=data)
        return result
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg:
            return "RATE_LIMITED"
        raise

def main():
    # Load posts data
    with open(POSTS_JSON) as f:
        posts = json.load(f)['blogPosts']
    
    # Get Blogger post IDs
    print("Fetching Blogger post mapping...")
    mapping = get_blogger_post_mapping()
    print(f"Found {len(mapping)} posts on Blogger\n")
    
    # Find and update each post
    updated = 0
    failed = 0
    
    for i, post in enumerate(posts, 1):
        print(f"[{i}/19] Processing: {post['title'][:60]}...")
        
        # Find Blogger ID
        blogger_id = find_blogger_id(post['title'], mapping)
        if not blogger_id:
            print_error(f"  Could not find Blogger post ID")
            failed += 1
            continue
        
        # Load full HTML content
        html_file = FULL_DIR / f"{post['id']}.html"
        if not html_file.exists():
            print_error(f"  Full HTML not found: {html_file}")
            failed += 1
            continue
        
        with open(html_file) as f:
            html_content = f.read()
        
        # Update with retries
        for attempt in range(3):
            result = update_post(BLOG_ID, blogger_id, html_content)
            
            if result == "RATE_LIMITED":
                wait = 60 * (attempt + 1)
                print_info(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            
            if result:
                print_success(f"  Updated: {result['url']}")
                updated += 1
                break
            else:
                print_error(f"  Failed to update")
                if attempt == 2:
                    failed += 1
        
        # Delay between updates
        if i < len(posts):
            time.sleep(15)
        
        print()
    
    print(f"\n{'='*60}")
    print(f"Updated: {updated} posts")
    print(f"Failed: {failed} posts")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
