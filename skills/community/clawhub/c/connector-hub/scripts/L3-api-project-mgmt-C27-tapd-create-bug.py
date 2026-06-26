#!/usr/bin/env python3
"""创建 TAPD Bug"""

import os
import sys
import json
import argparse
import requests

API_BASE = "https://api.tapd.cn/bugs"

def create_bug(title: str, description: str = "", severity: str = "normal", 
               priority: str = "2", owner: str = "", module: str = "") -> dict:
    """创建 Bug
    
    Args:
        title: Bug 标题
        description: Bug 描述
        severity: 严重程度（fatal/serious/normal/slight）
        priority: 优先级（1-紧急 2-高 3-中 4-低）
        owner: 负责人
        module: 模块
    
    Returns:
        API 响应
    """
    workspace_id = os.environ.get("TAPD_WORKSPACE_ID")
    api_token = os.environ.get("TAPD_API_TOKEN")
    
    if not workspace_id or not api_token:
        raise ValueError("未设置 TAPD_WORKSPACE_ID 或 TAPD_API_TOKEN 环境变量")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "workspace_id": workspace_id,
        "title": title,
        "description": description or f"Bug：{title}",
        "severity": severity,  # fatal/serious/normal/slight
        "priority": priority,  # 1-紧急 2-高 3-中 4-低
        "owner": owner,
        "module": module,
        "status": "open"  # open/resolved/closed
    }
    
    resp = requests.post(
        API_BASE,
        headers=headers,
        json=payload,
        auth=(workspace_id, api_token)
    )
    resp.raise_for_status()
    
    return resp.json()

def format_output(data: dict) -> str:
    """格式化输出"""
    bug = data.get("Bug", {})
    return f"""
Bug 创建成功：

| 字段 | 值 |
|------|-----|
| ID | {bug.get('id', '-')} |
| 标题 | {bug.get('title', '-')} |
| 严重程度 | {bug.get('severity', '-')} |
| 优先级 | {bug.get('priority', '-')} |
| 状态 | {bug.get('status', '-')} |
| 负责人 | {bug.get('owner', '-')} |
| 创建时间 | {bug.get('created', '-')} |
| 链接 | https://www.tapd.cn/{bug.get('workspace_id')}/bugs/view/{bug.get('id')} |
"""

def main():
    parser = argparse.ArgumentParser(description="创建 TAPD Bug")
    parser.add_argument("title", help="Bug 标题")
    parser.add_argument("--desc", help="Bug 描述")
    parser.add_argument("--severity", choices=["fatal", "serious", "normal", "slight"], default="normal")
    parser.add_argument("--priority", choices=["1", "2", "3", "4"], default="2")
    parser.add_argument("--owner", help="负责人")
    parser.add_argument("--module", help="模块")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    
    args = parser.parse_args()
    
    try:
        data = create_bug(args.title, args.desc, args.severity, args.priority, args.owner, args.module)
        
        if args.json:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            print(format_output(data))
    except Exception as e:
        print(f"创建失败：{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
