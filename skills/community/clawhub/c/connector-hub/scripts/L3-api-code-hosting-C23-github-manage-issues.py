#!/usr/bin/env python3
"""管理 GitHub Issues"""

import os
import sys
import json
import argparse
import subprocess

def run_gh(args: list) -> str:
    """运行 gh 命令"""
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"gh 命令失败：{result.stderr}")
    return result.stdout.strip()

def create_issue(title: str, body: str = "", labels: list = None, 
                assignees: list = None) -> dict:
    """创建 Issue
    
    Args:
        title: Issue 标题
        body: Issue 描述
        labels: 标签列表
        assignees: 指派人列表
    
    Returns:
        Issue 信息
    """
    args = ["issue", "create", "--title", title]
    
    if body:
        args.extend(["--body", body])
    
    if labels:
        args.extend(["--label", ",".join(labels)])
    
    if assignees:
        args.extend(["--assignee", ",".join(assignees)])
    
    output = run_gh(args)
    
    # 解析输出获取 Issue URL
    issue_url = output.strip()
    
    return {
        "url": issue_url,
        "title": title,
        "labels": labels or [],
        "assignees": assignees or []
    }

def list_issues(state: str = "open", labels: list = None, limit: int = 10) -> list:
    """列出 Issues
    
    Args:
        state: Issue 状态（open, closed, all）
        labels: 标签过滤
        limit: 数量限制
    
    Returns:
        Issue 列表
    """
    args = ["issue", "list", "--state", state, "--limit", str(limit)]
    
    if labels:
        args.extend(["--label", ",".join(labels)])
    
    output = run_gh(args)
    
    issues = []
    for line in output.split("\n")[2:]:  # 跳过表头
        if line.strip():
            parts = line.split("\t")
            if len(parts) >= 4:
                issues.append({
                    "number": parts[0].strip(),
                    "title": parts[1].strip(),
                    "state": parts[2].strip(),
                    "labels": parts[3].strip() if len(parts) > 3 else ""
                })
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="管理 GitHub Issues")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 创建 Issue
    create_parser = subparsers.add_parser("create", help="创建 Issue")
    create_parser.add_argument("title", help="Issue 标题")
    create_parser.add_argument("--body", help="Issue 描述")
    create_parser.add_argument("--labels", nargs="+", help="标签")
    create_parser.add_argument("--assignees", nargs="+", help="指派人")
    
    # 列出 Issues
    list_parser = subparsers.add_parser("list", help="列出 Issues")
    list_parser.add_argument("--state", choices=["open", "closed", "all"], default="open")
    list_parser.add_argument("--labels", nargs="+", help="标签过滤")
    list_parser.add_argument("--limit", type=int, default=10, help="数量限制")
    
    args = parser.parse_args()
    
    try:
        if args.command == "create":
            data = create_issue(args.title, args.body, args.labels, args.assignees)
            print(f"Issue 创建成功：")
            print(f"  标题：{data['title']}")
            print(f"  链接：{data['url']}")
            print(f"  标签：{', '.join(data['labels']) if data['labels'] else '-'}")
            print(f"  指派人：{', '.join(data['assignees']) if data['assignees'] else '-'}")
        elif args.command == "list":
            issues = list_issues(args.state, args.labels, args.limit)
            if not issues:
                print("没有找到 Issues")
            else:
                print(f"Issues 列表（{len(issues)} 个）：")
                for issue in issues:
                    print(f"  #{issue['number']} {issue['title']} [{issue['state']}] {issue['labels']}")
        else:
            parser.print_help()
    except Exception as e:
        print(f"操作失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
