#!/usr/bin/env python3
"""
General web clipper using x-reader

Supports: WeChat, XHS, Twitter, YouTube, Bilibili, RSS, and any web page
"""

import os
import re
import json
import subprocess
import hashlib
import sys
from datetime import datetime

from utils import get_vault_path, git_sync, slugify, detect_platform, get_domain


def proxy_images(content):
    """Proxy images for better accessibility."""
    if not content:
        return content
    # WeChat images
    content = re.sub(
        r'(https?://mmbiz\.qpic\.cn/[^\s\)]+)',
        r'https://wsrv.nl/?url=\1',
        content
    )
    return content


def fetch_with_x_reader(url):
    """Fetch content using x-reader CLI."""
    try:
        result = subprocess.run(
            ["x-reader", url],
            capture_output=True, text=True, timeout=60
        )
        
        if result.returncode != 0:
            return {"success": False, "error": f"x-reader failed: {result.stderr}"}
        
        output = result.stdout
        
        # Extract title
        title_match = re.search(r"Title: (.+)$", output, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else ""
        
        # Extract content
        content_match = re.search(r"Markdown Content:\n(.+)", output, re.DOTALL)
        content = content_match.group(1).strip() if content_match else output
        
        # Proxy images
        content = proxy_images(content)
        
        platform = detect_platform(url)
        
        return {
            "success": True,
            "title": title,
            "content": content,
            "platform": platform,
            "method": "x-reader"
        }
    
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout"}
    except FileNotFoundError:
        return {"success": False, "error": "x-reader not installed. Run: pipx install 'git+https://github.com/runesleo/x-reader.git'"}


def save_article(url, title, content, platform, method, vault_path=None):
    """Save article to Obsidian vault."""
    if not vault_path:
        vault_path = get_vault_path()
    if not vault_path:
        return {"success": False, "error": "Could not find Obsidian vault"}
    
    domain = get_domain(url)
    path_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    
    output_dir = os.path.join(vault_path, "clippings", "web", domain.replace('.', '_'))
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title) if title else path_hash
    filename = f"{today}-{slug}.md"
    filepath = os.path.join(output_dir, filename)
    
    safe_title = (title[:100] if title else 'Untitled').replace('"', "'")
    display_title = title if title else 'Untitled'
    
    frontmatter = f'''---
source: web
url: {url}
domain: {domain}
platform: {platform}
method: {method}
clipped: {datetime.now().isoformat()}
title: "{safe_title}"
---

# {display_title}

'''
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(frontmatter + content)
        return {"success": True, "path": filepath, "domain": domain}
    except IOError as e:
        return {"success": False, "error": str(e)}


def clip_web(url, vault_path=None):
    """Main entry point for web clipping."""
    fetch_result = fetch_with_x_reader(url)
    if not fetch_result["success"]:
        return fetch_result
    
    save_result = save_article(
        url,
        fetch_result["title"],
        fetch_result["content"],
        fetch_result["platform"],
        fetch_result["method"],
        vault_path
    )
    if not save_result["success"]:
        return save_result
    
    # Git sync
    git_result = git_sync(
        get_vault_path(vault_path),
        save_result["path"],
        f"clip: {fetch_result['title'][:50] if fetch_result['title'] else 'article'}"
    )
    
    output = {
        "success": True,
        "path": save_result["path"],
        "title": fetch_result["title"],
        "domain": save_result["domain"],
        "platform": fetch_result["platform"],
        "method": fetch_result["method"]
    }
    if not git_result["success"]:
        output["git_warnings"] = git_result.get("errors")
    
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: python3 web.py <url>"}, ensure_ascii=False))
        sys.exit(1)
    
    result = clip_web(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["success"] else 1)
