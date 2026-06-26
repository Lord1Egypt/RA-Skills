#!/usr/bin/env python3
"""
为 Teambition 任务添加进展
用法: uv run scripts/create_trace.py --task-id <ID> --title <标题> [--status <状态>]

状态: 1=正常 2=风险 3=逾期
"""

import json
import sys
from typing import Optional

import call_api

STATUS_LABEL = {1: "正常", 2: "风险", 3: "逾期"}

def create_trace(
    task_id: str,
    title: str,
    status: int = 1,
) -> None:
    body = {
        "title": title,
        "content": title,
        "status": status,
    }
    data = call_api.post(f"v3/task/{task_id}/trace/create", body)
    print(json.dumps(data.get("result", data), ensure_ascii=False, indent=2))

def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/create_trace.py --task-id <ID> --title <标题> [选项]

必需:
  --task-id <ID>          任务 ID
  --title <标题>          进展标题

可选:
  --status <状态>         进展状态：1=正常（默认）2=风险 3=逾期
  --help                  显示帮助

示例:
  uv run scripts/create_trace.py --task-id 'xxx' --title '已完成需求评审'
  uv run scripts/create_trace.py --task-id 'xxx' --title '进度延迟，有风险' --status 2""")
        sys.exit(0)

    task_id: Optional[str] = None
    title: Optional[str] = None
    status = 1

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--task-id" and i + 1 < len(sys.argv):
            task_id = sys.argv[i + 1]; i += 2
        elif arg == "--title" and i + 1 < len(sys.argv):
            title = sys.argv[i + 1]; i += 2
        elif arg == "--status" and i + 1 < len(sys.argv):
            try:
                status = int(sys.argv[i + 1])
            except ValueError:
                print("❌ status 必须是整数", file=sys.stderr); sys.exit(1)
            i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    if not task_id:
        print("❌ 缺少 --task-id", file=sys.stderr); sys.exit(1)
    if not title:
        print("❌ 缺少 --title", file=sys.stderr); sys.exit(1)

    create_trace(task_id, title, status)

if __name__ == "__main__":
    main()
