#!/usr/bin/env python3
"""创建 GitHub Pull Request"""

import os
import sys
import json
import argparse
import subprocess

def run_gh(args: list) -> str:
    """运行 gh 命令
    
    Args:
        args: gh 命令参数
    
    Returns:
        命令输出
    """
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"gh 命令失败：{result.stderr}")
    return result.stdout.strip()

def create_pull_request(title: str, body: str = "", base: str = "main", 
                       head: str = None, draft: bool = False) -> dict:
    """创建 PR
    
    Args:
        title: PR 标题
        body: PR 描述
        base: 目标分支
        head: 源分支
        draft: 是否为草稿
    
    Returns:
        PR 信息
    """
    args = ["pr", "create", "--title", title]
    
    if body:
        args.extend(["--body", body])
    
    if base:
        args.extend(["--base", base])
    
    if head:
        args.extend(["--head", head])
    
    if draft:
        args.append("--draft")
    
    output = run_gh(args)
    
    # 解析输出获取 PR URL
    pr_url = output.strip()
    
    return {
        "url": pr_url,
        "title": title,
        "base": base,
        "head": head or "current branch"
    }

def main():
    parser = argparse.ArgumentParser(description="创建 GitHub PR")
    parser.add_argument("title", help="PR 标题")
    parser.add_argument("--body", help="PR 描述")
    parser.add_argument("--base", default="main", help="目标分支")
    parser.add_argument("--head", help="源分支")
    parser.add_argument("--draft", action="store_true", help="创建草稿 PR")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_pull_request(args.title, args.body, args.base, args.head, args.draft)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(f"PR 创建成功：")
            print(f"  标题：{data['title']}")
            print(f"  链接：{data['url']}")
            print(f"  目标分支：{data['base']}")
            print(f"  源分支：{data['head']}")
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
