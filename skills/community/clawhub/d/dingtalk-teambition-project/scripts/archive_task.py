#!/usr/bin/env python3
"""
归档或恢复 Teambition 任务
用法: uv run scripts/archive_task.py --task-id <ID> [--restore]
"""

import json
import sys
from typing import Optional

import call_api


def archive_task(task_id: str) -> None:
    data = call_api.put(f"v3/task/{task_id}/archive")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"✅ 任务 {task_id} 已归档", file=sys.stderr)


def restore_task(task_id: str) -> None:
    data = call_api.post(f"v3/task/{task_id}/restore", {})
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"✅ 任务 {task_id} 已恢复", file=sys.stderr)


def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/archive_task.py --task-id <ID> [选项]

必需:
  --task-id <ID>    任务 ID

可选:
  --restore         恢复已归档的任务（默认为归档）
  --help            显示帮助

示例:
  uv run scripts/archive_task.py --task-id '69b2ad9501c321cc9c927eaf'
  uv run scripts/archive_task.py --task-id '69b2ad9501c321cc9c927eaf' --restore""")
        sys.exit(0)

    task_id: Optional[str] = None
    restore = False

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--task-id" and i + 1 < len(sys.argv):
            task_id = sys.argv[i + 1]
            i += 2
        elif arg == "--restore":
            restore = True
            i += 1
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)

    if not task_id:
        print("❌ 缺少 --task-id", file=sys.stderr)
        sys.exit(1)

    if restore:
        restore_task(task_id)
    else:
        archive_task(task_id)


if __name__ == "__main__":
    main()
