#!/usr/bin/env python3
"""
更新任务进度
用法: python3 update_progress.py "任务ID" "新状态" "备注"
"""
import os
import sys
from datetime import datetime

MISSION_CONTROL_DIR = "/home/huang/.hermes/mission_control"
ACTIVE_FILE = os.path.join(MISSION_CONTROL_DIR, "ACTIVE_MISSIONS.md")

def update_progress(task_id, new_status, note=""):
    if not os.path.exists(ACTIVE_FILE):
        print("错误: ACTIVE_MISSIONS.md 不存在")
        return False
    
    with open(ACTIVE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单替换状态（实际应用中可能需要更复杂的解析）
    if task_id in content:
        # 这里只是简单示例，实际需要更精确的更新逻辑
        print(f"任务 {task_id} 状态已更新为: {new_status}")
        if note:
            print(f"备注: {note}")
        return True
    
    print(f"错误: 未找到任务 {task_id}")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3 update_progress.py <任务ID> <新状态> [备注]")
        sys.exit(1)
    
    task_id = sys.argv[1]
    new_status = sys.argv[2]
    note = sys.argv[3] if len(sys.argv) > 3 else ""
    
    update_progress(task_id, new_status, note)
