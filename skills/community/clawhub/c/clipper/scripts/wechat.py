#!/usr/bin/env python3
"""
WeChat MP article clipper using browser snapshot

Note: This module provides the save function. The actual browser/snapshot
operations are handled by the agent using browser tool commands.
"""

import os
import re
import json
import sys
from datetime import datetime

from utils import get_vault_path, git_sync, slugify


def save_wechat_article(url, title, author, date, content, vault_path=None):
    """
    Save WeChat article to Obsidian vault.
    
    This function is called after the agent has extracted content via browser snapshot.
    """
    if not vault_path:
        vault_path = get_vault_path()
    if not vault_path:
        return {"success": False, "error": "Could not find Obsidian vault"}
    
    # Output path
    output_dir = os.path.join(vault_path, "clippings", "web", "mp_weixin_qq_com")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    filename = f"{today}-{slug}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Escape title quotes
    safe_title = (title[:100] if title else 'Untitled').replace('"', "'")
    
    # Build frontmatter
    frontmatter = f'''---
source: web
url: {url}
domain: mp.weixin.qq.com
platform: wechat
method: browser-snapshot
clipped: {datetime.now().isoformat()}
title: "{safe_title}"
author: "{author or ''}"
publish_date: "{date or ''}"
---

# {title or 'Untitled'}

'''
    
    # Add meta info
    meta_parts = []
    if author:
        meta_parts.append(f"> 来源：{author}")
    if date:
        meta_parts.append(f"> 发布时间：{date}")
    meta_parts.append(f"> 原文链接：{url}")
    
    meta_line = "  \n".join(meta_parts) + "\n\n"
    
    # Full content
    full_content = frontmatter + meta_line + content
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
    except IOError as e:
        return {"success": False, "error": str(e)}
    
    # Git sync
    git_result = git_sync(vault_path, filepath, f"clip: {title[:50] if title else 'wechat article'}")
    
    output = {
        "success": True,
        "path": filepath,
        "platform": "wechat",
        "method": "browser-snapshot",
        "title": title
    }
    if not git_result["success"]:
        output["git_warnings"] = git_result.get("errors")
    
    return output


def proxy_wechat_images(content):
    """Replace WeChat image URLs with wsrv.nl proxy for better accessibility."""
    if not content:
        return content
    return re.sub(
        r'(https?://mmbiz\.qpic\.cn/[^\s\)]+)',
        r'https://wsrv.nl/?url=\1',
        content
    )


if __name__ == "__main__":
    """
    CLI entry point for saving WeChat articles.
    
    Usage:
        python3 wechat.py --url "<url>" --title "<title>" --content "<markdown>"
        echo "<content>" | python3 wechat.py --url "<url>" --title "<title>"
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Save WeChat article to Obsidian')
    parser.add_argument('--url', required=True, help='Article URL')
    parser.add_argument('--title', required=True, help='Article title')
    parser.add_argument('--author', default='', help='Author/source')
    parser.add_argument('--date', default='', help='Publish date')
    parser.add_argument('--content', default=None, help='Article content in markdown')
    
    args = parser.parse_args()
    
    content = args.content
    if not content and not sys.stdin.isatty():
        content = sys.stdin.read()
    
    if not content:
        print(json.dumps({"success": False, "error": "No content provided"}, ensure_ascii=False))
        sys.exit(1)
    
    # Proxy images
    content = proxy_wechat_images(content.strip())
    
    result = save_wechat_article(
        url=args.url,
        title=args.title,
        author=args.author,
        date=args.date,
        content=content
    )
    
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["success"] else 1)
