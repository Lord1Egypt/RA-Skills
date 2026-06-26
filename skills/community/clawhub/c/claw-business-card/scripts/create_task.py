#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
"""
create_task.py — 生成任务 JSON 文件
用法: python create_task.py --workspace <path> --title <title> --description <desc>
                            --budget <amount> [--deadline <ISO8601>]
                            --counterparty-id <agentId> --counterparty-name <name>
                            --role requester|provider
"""
import json
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path


def parse_args():
    args = {}
    i = 1
    while i < len(sys.argv):
        key = sys.argv[i].lstrip("-").replace("-", "_")
        if i + 1 < len(sys.argv) and not sys.argv[i + 1].startswith("--"):
            args[key] = sys.argv[i + 1]
            i += 2
        else:
            args[key] = True
            i += 1
    return args


def create_task(workspace: Path, args: dict):
    net_dir = workspace / "agent-network"
    tasks_dir = net_dir / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)

    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    # 默认截止时间：24小时后
    deadline = args.get("deadline") or (
        datetime.now(timezone.utc) + timedelta(hours=24)
    ).isoformat()

    task = {
        "taskId": task_id,
        "role": args.get("role", "requester"),
        "status": "pending",
        "title": args.get("title", "未命名任务"),
        "description": args.get("description", ""),
        "requirements": [],
        "budgetLimit": float(args.get("budget", 100.0)),
        "deadline": deadline,
        "counterpartyId": args.get("counterparty_id", ""),
        "counterpartyName": args.get("counterparty_name", ""),
        "createdAt": now,
        "updatedAt": now,
        "result": None,
        "bill": None,
        "timeline": [
            {
                "time": now,
                "event": "created",
                "note": "任务创建"
            }
        ]
    }

    task_path = tasks_dir / f"{task_id}.json"
    task_path.write_text(json.dumps(task, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] 任务已创建")
    print(f"   任务ID: {task_id}")
    print(f"   标题: {task['title']}")
    print(f"   预算上限: {task['budgetLimit']} AgentToken")
    print(f"   截止时间: {deadline}")
    print(f"   文件: {task_path}")
    print(f"\nTASK_ID={task_id}")  # 供调用方解析

    return task_id


if __name__ == "__main__":
    args = parse_args()
    workspace_str = args.get("workspace")
    workspace = Path(workspace_str) if workspace_str else Path(__file__).parent.parent.parent.parent
    create_task(workspace, args)
