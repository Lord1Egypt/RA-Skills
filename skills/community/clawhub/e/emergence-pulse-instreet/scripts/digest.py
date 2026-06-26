#!/usr/bin/env python3
"""
InStreet Daily Pulse Generator
Generates a daily summary of trending posts from InStreet.

SECURITY MANIFEST:
  Environment variables accessed: none
  External endpoints called: https://instreet.coze.site/api/v1/ (Read-Only)
  Local files read: ~/.config/instreet/credentials.json (API Key)
  Local files written: none
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_BASE = "https://instreet.coze.site/api/v1"

def get_api_key():
    creds_file = os.path.expanduser("~/.config/instreet/credentials.json")
    if os.path.exists(creds_file):
        try:
            with open(creds_file) as f:
                data = json.load(f)
                return data.get("api_key")
        except:
            pass
    return None

def fetch_hot_posts(limit=10):
    api_key = get_api_key()
    if not api_key:
        raise ValueError("InStreet API Key not found in ~/.config/instreet/credentials.json")
    
    # Use /posts?sort=hot as per API reference
    url = f"{API_BASE}/posts?sort=hot&limit={limit}"
    req = Request(url)
    req.add_header("Authorization", f"Bearer {api_key}")
    try:
        with urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            # The InStreet API returns {"success": true, "data": {"data": [...], "total": ...}}
            data_wrapper = result.get("data", {})
            if isinstance(data_wrapper, list):
                return data_wrapper[:limit]
            return data_wrapper.get("data", [])[:limit]
    except (URLError, HTTPError) as e:
        print(f"Error fetching hot posts: {e}", file=sys.stderr)
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
            result = json.loads(response.read().decode())
            return result.get("data") or result.get("post") or result
    except (URLError, HTTPError) as e:
        print(f"Error fetching post {post_id}: {e}", file=sys.stderr)
        return None

def summarize_post(detail, title):
    """Generate Chinese summary from post detail."""
    if not detail:
        return f"关于「{title[:25]}...」的讨论"
    
    content = detail.get("content", "")
    if not content:
        return f"关于「{title[:25]}...」的讨论"
    
    # Clean content - remove markdown formatting
    clean = content.replace("**", "").replace("#", "").replace("`", "").replace("\n", " ")
    clean = " ".join(clean.split())
    
    # Simple Chinese sentence splitting
    import re
    sentences = re.split('[。！？]', clean)
    key_points = []
    for s in sentences[:8]:
        s = s.strip()
        if len(s) > 10:
            key_points.append(s)
        if len(key_points) >= 1:
            break
    
    if not key_points:
        return content[:100] + "..." if len(content) > 100 else content
    
    summary_text = key_points[0] + "。"
    return summary_text

def format_output(posts_with_details):
    if not posts_with_details:
        return "❌ 无法从 InStreet 获取热门动态"
    
    output = ["⚡ **InStreet 今日脉搏**", ""]
    
    for i, (post, detail) in enumerate(posts_with_details, 1):
        title = post.get("title", "无标题")[:50]
        author = post.get("agent", {}).get("username", "未知智能体")
        upvotes = post.get("upvotes", 0)
        comment_count = post.get("comment_count", 0)
        post_id = post.get("id", "")
        
        summary = summarize_post(detail, title)
        
        output.append(f"**{i}. {title}**")
        output.append(f"@{author}")
        output.append(f"{summary}")
        output.append(f"⬆️ {upvotes} | 💬 {comment_count}")
        output.append(f"https://instreet.coze.site/post/{post_id}")
        output.append("")
    
    output.append("技术支持: 涌现科学 https://emergence.science")
    return "\n".join(output)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="InStreet Pulse")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    
    try:
        posts = fetch_hot_posts(limit=args.limit)
        if not posts:
            print("未能获取到热门动态")
            return
        
        # Fetch details for top posts
        posts_with_details = []
        for post in posts:
            post_id = post.get("id")
            detail = fetch_post_detail(post_id)
            posts_with_details.append((post, detail))
        
        print(format_output(posts_with_details))
    except Exception as e:
        # print(f"Error: {e}", file=sys.stderr)
        # For agent execution, we might want to be more graceful
        print(f"未能生成 InStreet 脉搏摘要: {e}")

if __name__ == "__main__":
    main()
