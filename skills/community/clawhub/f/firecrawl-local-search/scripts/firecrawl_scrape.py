#!/usr/bin/env python3
"""Firecrawl 本地搜索 - 网页抓取脚本（不依赖 requests）"""
import sys, json, urllib.request, urllib.parse, urllib.error
from urllib.parse import urlparse

API_BASE_URL = "http://192.168.1.2:3002"

def scrape_url(url, formats=["markdown"]):
    """抓取网页内容"""
    try:
        data = json.dumps({"url": url, "formats": formats}).encode('utf-8')
        req = urllib.request.Request(
            f"{API_BASE_URL}/v1/scrape",
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.URLError as e:
        return {"error": f"连接失败: {e.reason}"}
    except Exception as e:
        return {"error": f"抓取失败: {str(e)}"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python3 firecrawl_scrape.py <URL>")
        print("示例：python3 firecrawl_scrape.py https://example.com")
        sys.exit(1)

    result = scrape_url(sys.argv[1])
    print(json.dumps(result, indent=2, ensure_ascii=False))
