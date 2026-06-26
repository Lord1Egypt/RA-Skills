#!/usr/bin/env python3
"""
搜索 Flatnotes 笔记
用法: python3 search_notes.py "搜索关键词" [--sort score|title|lastModified] [--order asc|desc] [--limit N]

环境变量:
  FLATNOTES_BASE_URL    - 服务地址
  FLATNOTES_USERNAME    - 用户名
  FLATNOTES_PASSWORD    - 密码
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from urllib.parse import quote


def get_base_url() -> str:
    base_url = os.getenv("FLATNOTES_BASE_URL")
    if not base_url:
        print("❌ 错误: FLATNOTES_BASE_URL 环境变量未设置")
        print()
        print("📌 请先配置以下环境变量：")
        print("   export FLATNOTES_BASE_URL=\"https://your-flatnotes-host\"")
        print("   export FLATNOTES_USERNAME=\"your-username\"")
        print("   export FLATNOTES_PASSWORD=\"your-password\"")
        print()
        print("   添加到 ~/.bashrc 后执行: source ~/.bashrc")
        sys.exit(1)
    return base_url


def get_token_from_credentials(base_url: str) -> str:
    """使用环境变量中的用户名密码获取令牌"""
    username = os.getenv("FLATNOTES_USERNAME")
    password = os.getenv("FLATNOTES_PASSWORD")
    
    if not username or not password:
        return None
    
    url = f"{base_url}/api/token"
    data = json.dumps({"username": username, "password": password}).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Content-Length": len(data)},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("access_token") or result.get("token")
    except Exception:
        return None


def search_notes(term: str, sort: str = "score", order: str = "desc", limit: int = None, base_url: str = None):
    """搜索笔记"""
    if base_url is None:
        base_url = get_base_url()
    
    token = get_token_from_credentials(base_url)
    
    params = [f"term={quote(term)}", f"sort={sort}", f"order={order}"]
    if limit:
        params.append(f"limit={limit}")
    
    url = f"{base_url}/api/search?{'&'.join(params)}"
    
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    
    try:
        with urllib.request.urlopen(req) as response:
            results = json.loads(response.read().decode("utf-8"))
            
            if not results:
                print("📭 未找到匹配笔记")
                return []
            
            print(f"🔍 找到 {len(results)} 条结果:\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['title']}")
                if r.get('contentHighlights'):
                    print(f"   摘要: {r['contentHighlights'][:100]}...")
                if r.get('tagMatches'):
                    print(f"   标签: {', '.join(r['tagMatches'])}")
                print(f"   修改时间: {r['lastModified']}")
                print()
            
            return results
    except urllib.error.HTTPError as e:
        print(f"❌ 搜索失败: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="搜索 Flatnotes 笔记")
    parser.add_argument("term", help="搜索关键词")
    parser.add_argument("--sort", choices=["score", "title", "lastModified"], default="score", help="排序方式")
    parser.add_argument("--order", choices=["asc", "desc"], default="desc", help="排序顺序")
    parser.add_argument("--limit", type=int, help="结果数量限制")
    parser.add_argument("--base-url", help="服务地址（默认从 FLATNOTES_BASE_URL 读取）")
    
    args = parser.parse_args()
    search_notes(args.term, args.sort, args.order, args.limit, args.base_url)
