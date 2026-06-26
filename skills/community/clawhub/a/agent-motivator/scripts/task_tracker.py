#!/usr/bin/env python3
"""
任务进度追踪器 - 记录和管理任务进度

支持：
- 任务创建
- 进度更新
- 里程碑标记
- 完成统计
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATE_FILE = Path.home() / ".openclaw" / "agent-motivator" / "task_state.json"

def ensure_state_dir():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_state():
    if not STATE_FILE.exists():
        return {"tasks": [], "completed": 0, "total": 0}
    with open(STATE_FILE) as f:
        return json.load(f)

def save_state(state):
    ensure_state_dir()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def create_task(name, priority="normal"):
    state = load_state()
    task = {
        "id": len(state["tasks"]) + 1,
        "name": name,
        "priority": priority,
        "status": "pending",
        "progress": 0,
        "milestones": [],
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
    }
    state["tasks"].append(task)
    state["total"] += 1
    save_state(state)
    return task

def update_progress(task_id, progress):
    state = load_state()
    for task in state["tasks"]:
        if task["id"] == task_id and task["status"] != "completed":
            task["progress"] = min(100, max(0, progress))
            task["updated"] = datetime.now().isoformat()
            if progress >= 100:
                task["status"] = "completed"
                task["completed"] = datetime.now().isoformat()
                state["completed"] += 1
            save_state(state)
            return task
    return None

def add_milestone(task_id, milestone_name):
    state = load_state()
    for task in state["tasks"]:
        if task["id"] == task_id:
            milestone = {
                "name": milestone_name,
                "reached": datetime.now().isoformat(),
            }
            task["milestones"].append(milestone)
            task["updated"] = datetime.now().isoformat()
            save_state(state)
            return milestone
    return None

def list_tasks(show_completed=False):
    state = load_state()
    tasks = state["tasks"]
    if not show_completed:
        tasks = [t for t in tasks if t["status"] != "completed"]
    return tasks

def get_stats():
    state = load_state()
    pending = len([t for t in state["tasks"] if t["status"] == "pending"])
    in_progress = len([t for t in state["tasks"] if t["status"] == "in_progress"])
    completed = state["completed"]
    total = state["total"]
    return {
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
        "total": total,
        "completion_rate": f"{completed/total*100:.1f}%" if total > 0 else "0%",
    }

def main():
    if len(sys.argv) < 2:
        print("用法：task_tracker.py <command> [args]")
        print("命令：create, update, milestone, list, stats")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "create":
        name = sys.argv[2] if len(sys.argv) > 2 else "未命名任务"
        priority = sys.argv[3] if len(sys.argv) > 3 else "normal"
        task = create_task(name, priority)
        print(json.dumps(task, ensure_ascii=False, indent=2))
    
    elif cmd == "update":
        task_id = int(sys.argv[2])
        progress = int(sys.argv[3])
        task = update_progress(task_id, progress)
        if task:
            print(json.dumps(task, ensure_ascii=False, indent=2))
        else:
            print(f"任务 {task_id} 未找到或已完成")
    
    elif cmd == "milestone":
        task_id = int(sys.argv[2])
        name = sys.argv[3] if len(sys.argv) > 3 else "里程碑"
        milestone = add_milestone(task_id, name)
        if milestone:
            print(json.dumps(milestone, ensure_ascii=False, indent=2))
        else:
            print(f"任务 {task_id} 未找到")
    
    elif cmd == "list":
        show_completed = "--completed" in sys.argv
        tasks = list_tasks(show_completed)
        print(json.dumps(tasks, ensure_ascii=False, indent=2))
    
    elif cmd == "stats":
        stats = get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    
    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
