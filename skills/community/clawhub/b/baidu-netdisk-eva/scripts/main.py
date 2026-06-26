#!/usr/bin/env python3
"""
百度网盘 Skill - 管理百度网盘文件
"""
import os
import sys
import json
import requests
import urllib.parse

# 凭证配置（从环境变量读取，不要硬编码！）
APP_ID = os.environ.get("BAIDU_APP_ID", "")
ACCESS_TOKEN = os.environ.get("BAIDU_NETDISK_TOKEN", "")

API_BASE = "https://pan.baidu.com/rest/2.0/xpan/file"

def api_call(method, params):
    """调用百度网盘API"""
    params["access_token"] = ACCESS_TOKEN
    params["app_id"] = APP_ID
    url = f"{API_BASE}?method={method}"
    resp = requests.post(url, data=params)
    return resp.json()

def list_files(path="/"):
    """列出文件"""
    result = api_call("list", {"dir": path})
    files = result.get("list", [])
    output = []
    for f in files:
        name = f.get("server_filename", "")
        isdir = f.get("isdir", 0)
        size = f.get("size", 0)
        if isdir:
            output.append(f"📁 {name}")
        else:
            size_mb = size / 1024 / 1024
            output.append(f"📄 {name} ({size_mb:.1f}MB)")
    return "\n".join(output) if output else "目录为空"

def search_files(keyword):
    """搜索文件"""
    result = api_call("search", {"key": keyword})
    files = result.get("list", [])
    output = []
    for f in files[:20]:
        name = f.get("server_filename", "")
        size = f.get("size", 0)
        size_mb = size / 1024 / 1024
        output.append(f"📄 {name} ({size_mb:.1f}MB)")
    return "\n".join(output) if output else "未找到文件"

def create_dir(path):
    """创建目录"""
    result = api_call("create", {"path": path, "isdir": 1, "rtype": 1})
    if result.get("errno") == 0:
        return f"✅ 目录创建成功: {path}"
    else:
        return f"❌ 创建失败: {result}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python baidu_netdisk.py <command> [args]")
        print("Commands:")
        print("  list [path]     - 列出文件")
        print("  search <keyword> - 搜索文件")
        print("  mkdir <path>    - 创建目录")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        path = sys.argv[2] if len(sys.argv) > 2 else "/"
        print(list_files(path))
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("请输入搜索关键词")
            sys.exit(1)
        print(search_files(sys.argv[2]))
    elif cmd == "mkdir":
        if len(sys.argv) < 3:
            print("请输入目录名")
            sys.exit(1)
        print(create_dir(sys.argv[2]))
    else:
        print(f"未知命令: {cmd}")

if __name__ == "__main__":
    main()
