#!/usr/bin/env python3
"""
查询任务所在工作流的任务状态列表
用法: uv run scripts/get_task_statuses.py <taskId> [--q <关键词>]

优势：只需 taskId 即可查询，无需先获取 projectId
API: GET /v3/task/{taskId}/tfs
"""

import json
import sys
from typing import Any, Dict, List, Optional

import call_api

def get_task_statuses(task_id: str, q: Optional[str] = None) -> None:
    """查询任务所在工作流的所有状态列表"""
    data = call_api.get(f"v3/task/{task_id}/tfs")
    statuses: List[Dict[str, Any]] = data.get("result", [])

    if q:
        # 按状态名称模糊过滤
        q_lower = q.lower()
        statuses = [s for s in statuses if q_lower in s.get("name", "").lower()]

    # 输出简化版状态列表
    for s in statuses:
        print(f"  {s.get('name', '?')} (id: {s.get('id', '?')}, kind: {s.get('kind', '?')})")

    # 也输出完整 JSON
    print("\n完整数据：")
    print(json.dumps(statuses, ensure_ascii=False, indent=2))

def main() -> None:
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("""用法: uv run scripts/get_task_statuses.py <taskId> [--q <关键词>]

参数:
  taskId          任务 ID（必需）

选项:
  --q <关键词>    按状态名称模糊搜索
  --help          显示帮助

示例:
  uv run scripts/get_task_statuses.py 69b2ad9501c321cc9c927eaf
  uv run scripts/get_task_statuses.py 69b2ad9501c321cc9c927eaf --q '进行中'

说明:
  直接通过任务 ID 查询该任务所在工作流的所有状态列表。
  相比 get_taskflow_statuses.py（需要 projectId），此脚本更简洁。
""")
        sys.exit(0 if "--help" in sys.argv else 1)

    task_id = sys.argv[1]
    q: Optional[str] = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--q" and i + 1 < len(sys.argv):
            q = sys.argv[i + 1]
            i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)

    get_task_statuses(task_id, q)

if __name__ == "__main__":
    main()
