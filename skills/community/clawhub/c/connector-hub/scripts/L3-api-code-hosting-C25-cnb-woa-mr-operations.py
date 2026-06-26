#!/usr/bin/env python3
"""CNB 司内版 MR 操作"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://cnb.woa.com/api/v1"

def list_mrs(repo: str) -> dict:
    """列出 MR"""
    token = os.environ.get("CNB_WOA_TOKEN")
    if not token:
        raise ValueError("未设置 CNB_WOA_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    resp = requests.get(f"{API_BASE}/repos/{repo}/pulls", headers=headers)
    resp.raise_for_status()
    
    return resp.json()

def create_mr(repo: str, title: str, source: str, target: str = "main", body: str = "") -> dict:
    """创建 MR"""
    token = os.environ.get("CNB_WOA_TOKEN")
    if not token:
        raise ValueError("未设置 CNB_WOA_TOKEN 环境变量")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "title": title,
        "head": source,
        "base": target,
        "body": body
    }
    
    resp = requests.post(f"{API_BASE}/repos/{repo}/pulls", headers=headers, json=payload)
    resp.raise_for_status()
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="CNB 司内版 MR 操作")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    list_parser = subparsers.add_parser("list", help="列出 MR")
    list_parser.add_argument("repo", help="仓库（owner/repo）")
    
    create_parser = subparsers.add_parser("create", help="创建 MR")
    create_parser.add_argument("repo", help="仓库（owner/repo）")
    create_parser.add_argument("title", help="MR 标题")
    create_parser.add_argument("--source", required=True, help="源分支")
    create_parser.add_argument("--target", default="main", help="目标分支")
    create_parser.add_argument("--body", help="MR 描述")
    
    args = parser.parse_args()
    
    try:
        if args.command == "list":
            data = list_mrs(args.repo)
            mrs = data.get("pulls", [])
            if not mrs:
                print("没有 MR")
            else:
                print(f"MR 列表（{len(mrs)} 个）：")
                for mr in mrs:
                    print(f"  #{mr.get('number', '-')} {mr.get('title', '-')} [{mr.get('state', '-')}]")
        elif args.command == "create":
            data = create_mr(args.repo, args.title, args.source, args.target, args.body)
            print(f"MR 创建成功：")
            print(f"  标题：{data.get('title')}")
            print(f"  链接：{data.get('html_url')}")
            print(f"  编号：#{data.get('number')}")
        else:
            parser.print_help()
    except Exception as e:
        print(f"操作失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
