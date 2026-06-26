#!/usr/bin/env python3
"""
Twitter/X clipper using Jina Reader
"""

import re
import json
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime

from utils import get_vault_path, git_sync

JINA_READER_URL = "https://r.jina.ai/"
TWITTER_PATTERNS = [
    r"https?://(?:www\.)?(?:twitter\.com|x\.com)/(\w+)/status(?:es)?/(\d+)",
]


def extract_tweet_info(url):
    """Extract handle and tweet ID from URL."""
    for pattern in TWITTER_PATTERNS:
        match = re.match(pattern, url)
        if match:
            return match.group(1), match.group(2)
    return None, None


def fetch_tweet(url):
    """Fetch tweet content using Jina Reader."""
    jina_url = f"{JINA_READER_URL}{url}"
    
    try:
        req = Request(jina_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=30) as response:
            content = response.read().decode("utf-8")
        
        # Extract title
        title_match = re.search(r"^Title: (.+)$", content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""
        
        # Remove metadata headers
        content = re.sub(r"^(Title|URL Source|Markdown Content): .+\n", "", content)
        content = re.sub(r"^---+\n", "", content, flags=re.MULTILINE)
        content = content.strip()
        
        return {"success": True, "title": title, "content": content}
    
    except HTTPError as e:
        return {"success": False, "error": f"HTTP error: {e.code}"}
    except URLError as e:
        return {"success": False, "error": f"Network error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def save_tweet(handle, tweet_id, title, content, vault_path):
    """Save tweet to Obsidian vault."""
    import os
    
    output_dir = os.path.join(vault_path, "clippings", "tweet")
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{handle}-{tweet_id}.md"
    filepath = os.path.join(output_dir, filename)
    
    frontmatter = f"""---
source: twitter
handle: @{handle}
tweet_id: "{tweet_id}"
url: https://x.com/{handle}/status/{tweet_id}
clipped: {datetime.now().isoformat()}
---

"""
    
    full_content = frontmatter + content
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
        return {"success": True, "path": filepath}
    except IOError as e:
        return {"success": False, "error": str(e)}


def clip_twitter(url, vault_path=None):
    """Main entry point for Twitter clipping."""
    handle, tweet_id = extract_tweet_info(url)
    if not handle or not tweet_id:
        return {"success": False, "error": "Invalid Twitter/X URL"}
    
    if not vault_path:
        vault_path = get_vault_path()
    if not vault_path:
        return {"success": False, "error": "Could not find Obsidian vault"}
    
    fetch_result = fetch_tweet(url)
    if not fetch_result["success"]:
        return fetch_result
    
    save_result = save_tweet(
        handle, tweet_id,
        fetch_result["title"], fetch_result["content"],
        vault_path
    )
    if not save_result["success"]:
        return save_result
    
    # Git sync
    git_result = git_sync(vault_path, save_result["path"], f"clip: @{handle} tweet")
    
    output = {
        "success": True,
        "path": save_result["path"],
        "handle": handle,
        "tweet_id": tweet_id,
        "platform": "twitter",
        "method": "jina-reader"
    }
    if not git_result["success"]:
        output["git_warnings"] = git_result.get("errors")
    
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "Usage: python3 twitter.py <url>"}, ensure_ascii=False))
        sys.exit(1)
    
    result = clip_twitter(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["success"] else 1)
