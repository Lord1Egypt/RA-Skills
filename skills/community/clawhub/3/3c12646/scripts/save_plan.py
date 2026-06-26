#!/usr/bin/env python3
"""
保存方案到任务目录
用法: python3 save_plan.py "任务ID" "内容类型" ["文件路径"]
内容类型: requirement | plan | log | report
"""
import os
import sys
from datetime import datetime

MISSION_CONTROL_DIR = "/home/huang/.hermes/mission_control"

def save_plan(task_id, content_type, content_or_path):
    today = datetime.now().strftime("%Y-%m-%d")
    today_folder = os.path.join(MISSION_CONTROL_DIR, today)
    task_folder = os.path.join(today_folder, task_id)

    # 确保任务目录存在
    os.makedirs(task_folder, exist_ok=True)

    # 映射内容类型到文件名
    filename_map = {
        "requirement": "t-requirement.md",
        "plan": "t-plan.md",
        "log": "t-log.md",
        "report": "t-report.md"
    }

    if content_type not in filename_map:
        print(f"错误: 未知内容类型 '{content_type}'")
        print(f"可用类型: {', '.join(filename_map.keys())}")
        return False

    filename = filename_map[content_type]
    filepath = os.path.join(task_folder, filename)

    # 如果内容是文件路径，读取文件内容
    content = content_or_path
    if os.path.isfile(content_or_path):
        with open(content_or_path, 'r', encoding='utf-8') as f:
            content = f.read()

    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"已保存: {filepath}")
    return filepath

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python3 save_plan.py <任务ID> <内容类型> <内容或文件路径>")
        print("内容类型: requirement | plan | log | report")
        sys.exit(1)

    task_id = sys.argv[1]
    content_type = sys.argv[2]
    content_or_path = sys.argv[3]

    save_plan(task_id, content_type, content_or_path)
