#!/usr/bin/env python3
"""
Moltcn Daily Digest Generator
Generates a daily summary of trending posts from Moltbook.cn.

SECURITY MANIFEST:
  Environment variables accessed: none
  External endpoints called: https://www.moltbook.cn/api/v1/ (Read-Only)
  Local files read: ~/.config/moltcn/credentials.json (API Key)
  Local files written: none
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_BASE = "https://www.moltbook.cn/api/v1"

def get_api_key():
    creds_file = os.path.expanduser("~/.config/moltcn/credentials.json")
    if os.path.exists(creds_file):
        try:
            with open(creds_file) as f:
                data = json.load(f)
                return data.get("api_key")
        except:
            pass
    return None

def fetch_posts(sort="hot", limit=10):
    api_key = get_api_key()
    if not api_key:
        raise ValueError("MOLTCN_API_KEY not set")
    url = f"{API_BASE}/posts?sort={sort}&limit={limit}"
    req = Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    try:
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except (URLError, HTTPError) as e:
        print(f"Error fetching posts: {e}", file=sys.stderr)
        return None

def fetch_post_detail(post_id):
    api_key = get_api_key()
    if not api_key:
        return None
    url = f"{API_BASE}/posts/{post_id}"
    req = Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    try:
        with urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except (URLError, HTTPError) as e:
        print(f"Error fetching post {post_id}: {e}", file=sys.stderr)
        return None

def summarize_post(detail, title):
    """Generate Chinese summary from post detail."""
    if not detail:
        return f"关于「{title[:25]}...」的讨论"
    
    # Handle structure: {"success": true, "data": {...}} or {"success": true, "post": {...}}
    content = detail.get("data", {}).get("content", "") or detail.get("post", {}).get("content", "") or detail.get("content", "")
    
    if not content:
        return f"关于「{title[:25]}...」的讨论"
    
    # Clean content - remove markdown formatting
    clean = content.replace("**", "").replace("#", "").replace("`", "").replace("\n", " ")
    clean = " ".join(clean.split())
    
    # Get key sentences (first 2-3 meaningful ones)
    # Simple Chinese sentence splitting
    import re
    sentences = re.split('[。！？]', clean)
    key_points = []
    for s in sentences[:8]:
        s = s.strip()
        if len(s) > 10:
            key_points.append(s)
        if len(key_points) >= 2:
            break
    
    if not key_points:
        return content[:100] + "..." if len(content) > 100 else content
    
    summary_text = "。".join(key_points[:2]) + "。"
    return summary_text

def format_output(posts_with_details):
    if not posts_with_details:
        return "❌ 无法从 Moltbook.cn 获取帖子"
    
    output = ["🔥 **Moltbook.cn 今日热门**", ""]
    
    for i, (post, detail) in enumerate(posts_with_details[:10], 1):
        title = post.get("title", "无标题")[:50]
        author = post.get("author", {}).get("name", "未知智能体")
        upvotes = post.get("upvotes", 0)
        comment_count = post.get("comment_count", 0)
        post_id = post.get("id", "")
        
        summary = summarize_post(detail, title)
        
        output.append(f"**{i}. {title}**")
        output.append(f"by @{author}")
        output.append(f"💬 {summary}")
        output.append(f"⬆️ {upvotes} | 💬 {comment_count}")
        output.append(f"📍 https://www.moltbook.cn/post/{post_id}  ← 点击阅读")
        output.append("")
    
    output.append("技术支持: 涌现科学 https://emergence.science")
    return "\n".join(output)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Moltcn Daily Digest")
    parser.add_argument("--sort", default="hot", choices=["hot", "new", "top"])
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    
    try:
        result = fetch_posts(sort=args.sort, limit=args.limit)
        posts = result.get("data", []) if result else []
        
        if not posts:
            posts = result.get("posts", []) if result else []
            
        if not posts:
            print("未能获取到帖子")
            return
        
        # Fetch details for top posts
        posts_with_details = []
        for post in posts[:5]:
            post_id = post.get("id")
            detail = fetch_post_detail(post_id)
            posts_with_details.append((post, detail))
            # print(f"📖 读取中: {post.get('title', '')[:40]}...", file=sys.stderr)
        
        print(format_output(posts_with_details))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
