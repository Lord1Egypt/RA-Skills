#!/usr/bin/env python3
"""
gblog-bulk-post - Bulk publish TechRex blog posts to Blogger
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path

# Add gblog scripts to path
sys.path.insert(0, str(Path.home() / ".openclaw/workspace/skills/gblog/scripts"))
from gblog import api_request, print_success, print_error, print_info, Colors

BLOG_HTML_DIR = Path.home() / ".openclaw/workspace/techrex-website/content/blog/blogger-html"
POSTS_JSON = Path.home() / ".openclaw/workspace/techrex-website/content/blog/posts.json"

def load_posts_data():
    """Load posts metadata"""
    with open(POSTS_JSON) as f:
        return json.load(f)['blogPosts']

def publish_post(blog_id, post_data, html_content, draft=False):
    """Publish a single post"""
    post_body = {
        'kind': 'blogger#post',
        'title': post_data['title'],
        'content': html_content,
        'labels': post_data['tags']
    }
    
    try:
        endpoint = f"/blogs/{blog_id}/posts"
        if draft:
            endpoint += "?isDraft=true"
        
        result = api_request(endpoint, method='POST', data=post_body)
        return result
    except Exception as e:
        print_error(f"Failed to publish: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Bulk publish TechRex posts to Blogger')
    parser.add_argument('--blog-id', required=True, help='Blogger blog ID')
    parser.add_argument('--post-id', help='Publish specific post by ID (e.g., 01-llmfit-guide)')
    parser.add_argument('--draft', action='store_true', help='Publish as drafts')
    parser.add_argument('--start', type=int, default=1, help='Start from post number (1-19)')
    parser.add_argument('--end', type=int, default=19, help='End at post number (1-19)')
    parser.add_argument('--update-json', action='store_true', help='Update posts.json with published URLs')
    
    args = parser.parse_args()
    
    posts_data = load_posts_data()
    
    # Filter posts if specific ID provided
    if args.post_id:
        posts_to_publish = [p for p in posts_data if p['id'] == args.post_id]
        if not posts_to_publish:
            print_error(f"Post {args.post_id} not found")
            sys.exit(1)
    else:
        # Slice by start/end
        posts_to_publish = posts_data[args.start-1:args.end]
    
    print(f"🦖 TechRex Bulk Publisher")
    print(f"Blog ID: {args.blog_id}")
    print(f"Posts to publish: {len(posts_to_publish)}")
    print(f"Mode: {'DRAFT' if args.draft else 'PUBLISH'}\n")
    
    published_urls = {}
    
    for i, post in enumerate(posts_to_publish, 1):
        print(f"[{i}/{len(posts_to_publish)}] Publishing: {post['title']}")
        
        # Load HTML content
        html_file = BLOG_HTML_DIR / f"{post['id']}.html"
        if not html_file.exists():
            print_error(f"  HTML file not found: {html_file}")
            continue
        
        with open(html_file) as f:
            html_content = f.read()
        
        # Publish with retry on rate limit
        result = None
        for attempt in range(3):
            result = publish_post(args.blog_id, post, html_content, args.draft)
            if result:
                break
            if attempt < 2:
                wait = 30 * (attempt + 1)
                print_info(f"  Rate limited, retrying in {wait}s...")
                time.sleep(wait)
        
        if result:
            print_success(f"  Published: {result['url']}")
            published_urls[post['id']] = result['url']
        else:
            print_error(f"  Failed to publish (skipping)")
        
        # Delay between posts to avoid rate limiting
        if i < len(posts_to_publish):
            time.sleep(12)
        
        print()
    
    # Update posts.json if requested
    if args.update_json and published_urls:
        print_info("Updating posts.json with published URLs...")
        
        for post in posts_data:
            if post['id'] in published_urls:
                post['bloggerUrl'] = published_urls[post['id']]
        
        with open(POSTS_JSON, 'w') as f:
            json.dump({'blogPosts': posts_data}, f, indent=2)
        
        print_success("posts.json updated!")
    
    print(f"\n{Colors.GREEN}✓ Bulk publish complete!{Colors.END}")
    print(f"Published {len(published_urls)} posts")

if __name__ == '__main__':
    main()
