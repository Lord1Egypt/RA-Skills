#!/usr/bin/env python3
"""
龙虾轮询脚本 - 供 cron job 直接调用
直接执行轮询逻辑，不经过 LLM agent
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import claim, load_state, save_state

def poll():
    state = load_state()
    known_ids = set(state.get("in_progress_task_ids", []))

    result = claim()
    in_progress = result.get("in_progress") or []
    current_ids = set(item.get("task_id") for item in in_progress if item.get("task_id"))

    # 找出新接到的任务
    new_tasks = [
        item for item in in_progress
        if item.get("task_id") and item.get("task_id") not in known_ids
    ]

    state["in_progress_task_ids"] = list(current_ids)
    state["last_poll_at"] = datetime.utcnow().isoformat()
    save_state(state)

    if new_tasks:
        for task in new_tasks:
            print(f"[NEW_TASK] task_id={task.get('task_id')} title={task.get('title')} deadline={task.get('submission_deadline')}", flush=True)
    else:
        print(f"[POLL] no new tasks, in_progress={len(current_ids)}", flush=True)

if __name__ == "__main__":
    try:
        poll()
    except Exception as e:
        print(f"[ERROR] {e}", flush=True)
        sys.exit(1)
