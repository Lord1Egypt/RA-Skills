#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web Fetch Wrapper for Game News Crawler
使用 OpenClaw 的 web_fetch 工具抓取网页
"""

import sys
import json
import subprocess


def fetch_with_web_fetch(url: str) -> dict:
    """使用 OpenClaw 的 web_fetch 工具抓取网页"""
    try:
        # 调用 OpenClaw 的 web_fetch 工具
        result = subprocess.run(
            ['openclaw', 'web_fetch', url, '--extract-mode', 'markdown', '--max-chars', '5000'],
            capture_output=True, text=True, timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return {
                'success': True,
                'text': data.get('text', ''),
                'title': data.get('title', '')
            }
        else:
            return {
                'success': False,
                'error': result.stderr
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python web_fetch_wrapper.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = fetch_with_web_fetch(url)
    print(json.dumps(result, ensure_ascii=False))
