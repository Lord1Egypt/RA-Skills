#!/usr/bin/env python3
"""
飞书待阅读任务自动创建脚本

用法：
    python create_reading_task.py --user-open-id <ou_xxx> --title <标题> --url <链接> --desc <描述>

或者通过环境变量传入：
    FEISHU_USER_OPEN_ID=ou_xxx python create_reading_task.py --title <标题> --url <链接>
"""

import argparse
import json
import sys
import os
from datetime import datetime

def create_reading_task(user_open_id: str, title: str, url: str = "", description: str = ""):
    """创建待阅读任务"""
    
    # 构建任务内容
    task_summary = f"待阅读：{title}"
    
    task_desc = []
    if url:
        task_desc.append(f"🔗 链接：{url}")
    if description:
        task_desc.append(f"\n📝 描述：{description}")
    
    task_desc.append(f"\n⏰ 添加时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    task_desc.append("\n---\n此任务由 feishu-reading-task 技能自动创建")
    
    full_description = "\n".join(task_desc)
    
    # 输出任务数据（供上层调用飞书 API）
    task_data = {
        "action": "create",
        "summary": task_summary,
        "description": full_description,
        "current_user_id": user_open_id,
        "members": [
            {"id": user_open_id, "role": "assignee"}
        ]
    }
    
    print(json.dumps(task_data, ensure_ascii=False, indent=2))
    return task_data


def main():
    parser = argparse.ArgumentParser(description="创建飞书待阅读任务")
    parser.add_argument("--user-open-id", required=True, help="用户 open_id (ou_xxx 格式)")
    parser.add_argument("--title", required=True, help="内容标题")
    parser.add_argument("--url", default="", help="链接 URL")
    parser.add_argument("--desc", default="", help="附加描述")
    
    args = parser.parse_args()
    
    create_reading_task(
        user_open_id=args.user_open_id,
        title=args.title,
        url=args.url,
        description=args.desc
    )


if __name__ == "__main__":
    main()
