#!/usr/bin/env python3
"""检查点管理工具 - 创建、更新、读取任务检查点"""

import json
import os
import sys
from datetime import datetime, timezone

CHECKPOINT_DIR = os.path.expanduser("~/.openclaw/workspace/checkpoints")

def ensure_dir():
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

def create(task_id: str, description: str, total: int):
    """创建新检查点"""
    ensure_dir()
    cp = {
        "task_id": task_id,
        "description": description,
        "total": total,
        "completed": 0,
        "succeeded": 0,
        "failed": 0,
        "failed_items": [],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_checkpoint": datetime.now(timezone.utc).isoformat(),
        "output_file": None,
        "status": "running"
    }
    path = os.path.join(CHECKPOINT_DIR, f"{task_id}.json")
    with open(path, "w") as f:
        json.dump(cp, f, indent=2, ensure_ascii=False)
    print(f"✅ 检查点已创建: {path}")
    return cp

def update(task_id: str, succeeded: int = 0, failed: int = 0, failed_items: list = None, output_file: str = None):
    """更新检查点进度"""
    path = os.path.join(CHECKPOINT_DIR, f"{task_id}.json")
    with open(path) as f:
        cp = json.load(f)
    
    cp["succeeded"] += succeeded
    cp["failed"] += failed
    cp["completed"] = cp["succeeded"] + cp["failed"]
    if failed_items:
        cp["failed_items"].extend(failed_items)
    if output_file:
        cp["output_file"] = output_file
    cp["last_checkpoint"] = datetime.now(timezone.utc).isoformat()
    
    if cp["completed"] >= cp["total"]:
        cp["status"] = "done"
    
    with open(path, "w") as f:
        json.dump(cp, f, indent=2, ensure_ascii=False)
    
    pct = round(cp["completed"] / cp["total"] * 100) if cp["total"] > 0 else 0
    print(f"📊 进度: {cp['completed']}/{cp['total']} ({pct}%) | ✅{cp['succeeded']} ❌{cp['failed']}")
    return cp

def read(task_id: str):
    """读取检查点状态"""
    path = os.path.join(CHECKPOINT_DIR, f"{task_id}.json")
    if not os.path.exists(path):
        print(f"❌ 检查点不存在: {task_id}")
        return None
    with open(path) as f:
        cp = json.load(f)
    print(json.dumps(cp, indent=2, ensure_ascii=False))
    return cp

def list_all():
    """列出所有检查点"""
    ensure_dir()
    files = [f for f in os.listdir(CHECKPOINT_DIR) if f.endswith(".json")]
    if not files:
        print("没有检查点")
        return
    for f in sorted(files):
        with open(os.path.join(CHECKPOINT_DIR, f)) as fh:
            cp = json.load(fh)
        pct = round(cp["completed"] / cp["total"] * 100) if cp["total"] > 0 else 0
        status_icon = "✅" if cp["status"] == "done" else "🔄"
        print(f"{status_icon} {cp['task_id']}: {cp['description']} | {cp['completed']}/{cp['total']} ({pct}%)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: checkpoint.py <create|update|read|list> [参数]")
        print("  create <task_id> <description> <total>")
        print("  update <task_id> --succeeded N --failed N")
        print("  read <task_id>")
        print("  list")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "create" and len(sys.argv) >= 5:
        create(sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif cmd == "update" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        s, f = 0, 0
        for i, arg in enumerate(sys.argv[3:], 3):
            if arg == "--succeeded" and i + 1 < len(sys.argv):
                s = int(sys.argv[i + 1])
            elif arg == "--failed" and i + 1 < len(sys.argv):
                f = int(sys.argv[i + 1])
        update(task_id, succeeded=s, failed=f)
    elif cmd == "read" and len(sys.argv) >= 3:
        read(sys.argv[2])
    elif cmd == "list":
        list_all()
    else:
        print("参数错误，运行 checkpoint.py 查看用法")
