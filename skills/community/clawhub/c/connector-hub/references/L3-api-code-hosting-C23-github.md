# C23 - GitHub

## 基本信息

| 字段 | 值 |
|------|-----|
| ID | C23 |
| 连接器名 | github |
| 显示名 | GitHub |
| 层级 | L3 纯 API 查询型 |
| 可替代 | ✅ 完全可替代（Skill） |
| 分类 | 代码托管 |
| 替代难度 | 简单 |

## 连接器能力

| 能力 | 说明 |
|------|------|
| 仓库管理 | 创建/克隆/删除仓库 |
| PR 管理 | 创建/合并/审查 PR |
| Issue 管理 | 创建/关闭/标签管理 |
| CI/CD | GitHub Actions 状态 |
| Release | 发布管理 |

## Skill 替代方案

### 脚本位置

使用 connector-hub 技能中的脚本：

```
scripts/
├── L3-api-code-hosting-C23-github-create-pr.py      # 创建 Pull Request
└── L3-api-code-hosting-C23-github-manage-issues.py  # Issue 管理
```

### 鉴权方式

**方式一：gh CLI（推荐）**
```bash
gh auth login
```

**方式二：Personal Access Token**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

**方式三：GitHub App（企业）**
```bash
export GITHUB_APP_ID="your_app_id"
export GITHUB_APP_PRIVATE_KEY="path/to/private-key.pem"
```

### 核心脚本示例

**L3-api-code-hosting-C23-github-create-pr.py**：
```python
#!/usr/bin/env python3
"""创建 GitHub Pull Request"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

def run_gh(args: list) -> str:
    """运行 gh 命令"""
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"gh 命令失败：{result.stderr}")
    return result.stdout.strip()

def create_pull_request(title: str, body: str = "", base: str = "main", 
                       head: str = None, draft: bool = False) -> dict:
    """创建 PR"""
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

def format_output(data: dict) -> str:
    """格式化输出"""
    return f"""
PR 创建成功：

| 字段 | 值 |
|------|-----|
| 标题 | {data['title']} |
| 链接 | {data['url']} |
| 目标分支 | {data['base']} |
| 源分支 | {data['head']} |
"""

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
            print(format_output(data))
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**L3-api-code-hosting-C23-github-manage-issues.py**：
```python
#!/usr/bin/env python3
"""管理 GitHub Issues"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

def run_gh(args: list) -> str:
    """运行 gh 命令"""
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"gh 命令失败：{result.stderr}")
    return result.stdout.strip()

def create_issue(title: str, body: str = "", labels: list = None, 
                assignees: list = None) -> dict:
    """创建 Issue"""
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
    """列出 Issues"""
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

def format_issue_output(data: dict) -> str:
    """格式化 Issue 输出"""
    return f"""
Issue 创建成功：

| 字段 | 值 |
|------|-----|
| 标题 | {data['title']} |
| 链接 | {data['url']} |
| 标签 | {', '.join(data['labels']) if data['labels'] else '-'} |
| 指派人 | {', '.join(data['assignees']) if data['assignees'] else '-'} |
"""

def format_issues_list(issues: list) -> str:
    """格式化 Issues 列表"""
    if not issues:
        return "没有找到 Issues"
    
    output = f"## Issues 列表（{len(issues)} 个）\n\n"
    output += "| 编号 | 标题 | 状态 | 标签 |\n"
    output += "|------|------|------|------|\n"
    
    for issue in issues:
        output += f"| {issue['number']} | {issue['title']} | {issue['state']} | {issue['labels']} |\n"
    
    return output

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
            print(format_issue_output(data))
        elif args.command == "list":
            issues = list_issues(args.state, args.labels, args.limit)
            print(format_issues_list(issues))
        else:
            parser.print_help()
    except Exception as e:
        print(f"操作失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### 迁移成本

| 项目 | 说明 |
|------|------|
| CLI | gh CLI 已内置 |
| API | GitHub API 稳定 |
| 工作流 | 无需修改 |

### 对比

| 维度 | 连接器 | Skill |
|------|--------|-------|
| 鉴权 | 平台托管 | gh auth/Token |
| 功能 | 固定 | 可自定义 |
| 多平台 | 绑定 GitHub | 可对接 GitLab 等 |
| 输出格式 | 固定 | 模板化可定制 |
| 迁移 | 重配连接器 | 改 API 地址 |
