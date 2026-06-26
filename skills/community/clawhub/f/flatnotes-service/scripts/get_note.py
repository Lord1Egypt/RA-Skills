#!/usr/bin/env python3
"""
获取 Flatnotes 笔记内容
用法: python3 get_note.py "笔记标题" [--base-url URL]

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


def get_note(title: str, base_url: str = None):
    """获取笔记内容"""
    if base_url is None:
        base_url = get_base_url()
    
    token = get_token_from_credentials(base_url)
    
    url = f"{base_url}/api/notes/{quote(title)}"
    
    req = urllib.request.Request(url)
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            print(f"📄 {result['title']}\n")
            print(f"最后修改: {result['lastModified']}")
            print("-" * 40)
            print(result.get('content', '') or "(空内容)")
            return result
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ 笔记不存在: {title}")
        else:
            print(f"❌ 获取失败: {e.code} - {e.read().decode('utf-8')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="获取 Flatnotes 笔记")
    parser.add_argument("title", help="笔记标题")
    parser.add_argument("--base-url", help="服务地址（默认从 FLATNOTES_BASE_URL 读取）")
    
    args = parser.parse_args()
    get_note(args.title, args.base_url)
