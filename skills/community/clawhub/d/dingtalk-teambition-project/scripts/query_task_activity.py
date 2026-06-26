#!/usr/bin/env python3
"""
查询 Teambition 任务动态（操作历史）
用法: uv run scripts/query_task_activity.py --task-id <ID> [选项]

动态类型: comment=评论 status_change=状态变更 executor_change=执行人变更
         priority_change=优先级变更 due_date_change=截止时间变更
"""

import json
import sys
from typing import Optional

import call_api


def query_activity(
    task_id: str,
    actions: Optional[str] = None,
    exclude_actions: Optional[str] = None,
    language: str = "zh_CN",
    order_by: str = "created_desc",
    page_size: Optional[int] = None,
) -> None:
    params: dict = {"language": language, "orderBy": order_by}
    if actions:
        params["actions"] = actions
    if exclude_actions:
        params["excludeActions"] = exclude_actions
    if page_size:
        params["pageSize"] = page_size

    data = call_api.get(f"v3/task/{task_id}/activity/list", params=params)
    result = data.get("result", data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    count = len(result) if isinstance(result, list) else "?"
    print(f"共找到 {count} 条动态记录", file=sys.stderr)


def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/query_task_activity.py --task-id <ID> [选项]

必需:
  --task-id <ID>          任务 ID

可选:
  --actions <类型>        只查询指定类型（如 comment）
  --exclude-actions <类型> 排除指定类型
  --language <语言>       语言（默认 zh_CN）
  --order-by <排序>       排序方式（默认 created_desc）
  --page-size <数量>      每页数量
  --help                  显示帮助

示例:
  uv run scripts/query_task_activity.py --task-id '69b2ad9501c321cc9c927eaf'
  uv run scripts/query_task_activity.py --task-id '69b2ad9501c321cc9c927eaf' --actions comment
  uv run scripts/query_task_activity.py --task-id '69b2ad9501c321cc9c927eaf' --exclude-actions comment""")
        sys.exit(0)

    task_id: Optional[str] = None
    actions: Optional[str] = None
    exclude_actions: Optional[str] = None
    language = "zh_CN"
    order_by = "created_desc"
    page_size: Optional[int] = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--task-id" and i + 1 < len(sys.argv):
            task_id = sys.argv[i + 1]; i += 2
        elif arg == "--actions" and i + 1 < len(sys.argv):
            actions = sys.argv[i + 1]; i += 2
        elif arg == "--exclude-actions" and i + 1 < len(sys.argv):
            exclude_actions = sys.argv[i + 1]; i += 2
        elif arg == "--language" and i + 1 < len(sys.argv):
            language = sys.argv[i + 1]; i += 2
        elif arg == "--order-by" and i + 1 < len(sys.argv):
            order_by = sys.argv[i + 1]; i += 2
        elif arg == "--page-size" and i + 1 < len(sys.argv):
            page_size = int(sys.argv[i + 1]); i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)

    if not task_id:
        print("❌ 缺少 --task-id", file=sys.stderr)
        sys.exit(1)

    query_activity(task_id, actions, exclude_actions, language, order_by, page_size)


if __name__ == "__main__":
    main()
