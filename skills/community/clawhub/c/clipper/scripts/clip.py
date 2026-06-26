#!/usr/bin/env python3
"""
Clipper - Universal web content clipper for Obsidian

Automatically routes to the best method based on URL:
- Twitter/X → Jina Reader (fast, reliable)
- WeChat MP → Browser snapshot (handles JS rendering)
- Other → x-reader (general purpose)

Usage:
    python3 clip.py <url>

Output:
    Saves to <vault>/clippings/<type>/<YYYY-MM-DD>-<slug>.md
"""

import sys
import json

from utils import detect_platform
import twitter
import wechat
import web


def clip(url, vault_path=None):
    """
    Clip any URL to Obsidian vault.
    
    Automatically detects platform and uses appropriate method.
    """
    platform = detect_platform(url)
    
    if platform == "twitter":
        return twitter.clip_twitter(url, vault_path)
    elif platform == "wechat":
        # WeChat needs browser - return instruction for agent
        return {
            "success": False,
            "needs_browser": True,
            "platform": "wechat",
            "url": url,
            "instruction": "Use browser tool to fetch content, then call wechat.save_wechat_article()"
        }
    else:
        return web.clip_web(url, vault_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "Usage: python3 clip.py <url>"
        }, ensure_ascii=False))
        sys.exit(1)
    
    url = sys.argv[1].strip()
    result = clip(url)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)
