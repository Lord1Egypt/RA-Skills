#!/usr/bin/env python3
"""Gongfeng 仓库操作"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://gongfeng.woa.com/api/v1"

def list_repos() -> dict:
    """列出仓库"""
    token = os.environ.get("GONGFENG_TOKEN")
    if not token:
        raise ValueError("未设置 GONGFENG_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    resp = requests.get(f"{API_BASE}/repos", headers=headers)
    resp.raise_for_status()
    
    return resp.json()

def create_repo(name: str, description: str = "", private: bool = False) -> dict:
    """创建仓库"""
    token = os.environ.get("GONGFENG_TOKEN")
    if not token:
        raise ValueError("未设置 GONGFENG_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": name,
        "description": description,
        "private": private
    }
    
    resp = requests.post(f"{API_BASE}/repos", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="Gongfeng 仓库操作")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    subparsers.add_parser("list", help="列出仓库")
    
    create_parser = subparsers.add_parser("create", help="创建仓库")
    create_parser.add_argument("name", help="仓库名称")
    create_parser.add_argument("--desc", help="仓库描述")
    create_parser.add_argument("--private", action="store_true", help="是否私有")
    
    args = parser.parse_args()
    
    try:
        if args.command == "list":
            data = list_repos()
            repos = data.get("repos", [])
            if not repos:
                print("没有仓库")
            else:
                print(f"仓库列表（{len(repos)} 个）：")
                for repo in repos:
                    print(f"  - {repo.get('full_name', '-')} ({'私有' if repo.get('private') else '公开'})")
        elif args.command == "create":
            data = create_repo(args.name, args.desc, args.private)
            print(f"仓库创建成功：")
            print(f"  名称：{data.get('name')}")
            print(f"  链接：{data.get('html_url')}")
        else:
            parser.print_help()
    except Exception as e:
        print(f"操作失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
