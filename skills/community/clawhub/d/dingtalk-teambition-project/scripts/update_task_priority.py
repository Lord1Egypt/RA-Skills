#!/usr/bin/env python3
"""
更新 Teambition 任务优先级
用法: uv run scripts/update_task_priority.py --task-id <ID> --priority <0-3>

⚠️  重要：企业通常会自定义优先级名称，调用本脚本前必须先确认企业优先级配置：
  1. uv run scripts/query_project_detail.py <projectId> --extra-fields organizationId
  2. uv run scripts/get_priority_list.py <organizationId>
  将用户描述的优先级名称与企业配置中的 name 字段匹配，再用对应的 priority 数值传入。

优先级数值含义（系统默认，企业可自定义）: 0=紧急 1=高 2=中 3=低
"""

import json
import sys
from typing import Optional

import call_api

# 系统默认优先级名称（兜底值）。
# 企业通常会自定义优先级名称，更新前应先调用 get_priority_list.py 获取企业真实配置，
# 将用户描述的优先级名称与企业配置匹配后，再用对应的 priority 数值调用更新接口。
DEFAULT_PRIORITY_LABEL = {0: "紧急", 1: "高", 2: "中", 3: "低"}

def update_task_priority(task_id: str, priority: int) -> None:
    data = call_api.put(f"v3/task/{task_id}/priority", {"priority": priority})
    label = DEFAULT_PRIORITY_LABEL.get(priority, str(priority))
    print(f"✅ 优先级已更新为 {priority}（{label}）", file=sys.stderr)
    print(json.dumps(data.get("result", data), ensure_ascii=False, indent=2))

def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/update_task_priority.py --task-id <ID> --priority <0-3>

必需:
  --task-id <ID>        任务 ID
  --priority <0-3>      优先级数值（系统默认：0=紧急 1=高 2=中 3=低）

⚠️  重要：企业通常会自定义优先级名称，更新前必须先确认企业真实配置：
  1. uv run scripts/query_project_detail.py <projectId> --extra-fields organizationId
  2. uv run scripts/get_priority_list.py <organizationId>
  将用户描述的优先级名称与企业配置中的 name 字段匹配，再用对应的 priority 数值传入。

示例:
  uv run scripts/update_task_priority.py --task-id '67ec9b8c3c6130ac88605c3e' --priority 0
  uv run scripts/update_task_priority.py --task-id '67ec9b8c3c6130ac88605c3e' --priority 1""")
        sys.exit(0)

    task_id: Optional[str] = None
    priority: Optional[int] = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--task-id" and i + 1 < len(sys.argv):
            task_id = sys.argv[i + 1]; i += 2
        elif arg == "--priority" and i + 1 < len(sys.argv):
            try:
                priority = int(sys.argv[i + 1])
            except ValueError:
                print("❌ priority 必须是整数", file=sys.stderr); sys.exit(1)
            i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    if not task_id:
        print("❌ 缺少 --task-id", file=sys.stderr); sys.exit(1)
    if priority is None:
        print("❌ 缺少 --priority", file=sys.stderr); sys.exit(1)

    update_task_priority(task_id, priority)

if __name__ == "__main__":
    main()