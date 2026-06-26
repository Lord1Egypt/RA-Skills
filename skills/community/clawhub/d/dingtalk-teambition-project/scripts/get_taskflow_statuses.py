#!/usr/bin/env python3
"""
获取 Teambition 项目工作流状态列表
用法: uv run scripts/get_taskflow_statuses.py <projectId> [--taskflow-id <ID>] [--q <关键词>] [--only-start]
"""

import json
import sys
from typing import Any, Dict, List, Optional

import call_api


def get_taskflow_statuses(
    project_id: str,
    taskflow_id: Optional[str] = None,
    q: Optional[str] = None,
    only_start: bool = False,
) -> None:
    params: Dict[str, Any] = {}
    if taskflow_id:
        params["tfIds"] = taskflow_id
    if q:
        params["q"] = q

    data = call_api.get(f"v3/project/{project_id}/taskflowstatus/search", params=params)
    statuses: List[Dict[str, Any]] = data.get("result", [])

    if only_start:
        statuses = [s for s in statuses if s.get("kind") == "start"]

    print(json.dumps(statuses, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("""用法: uv run scripts/get_taskflow_statuses.py <projectId> [选项]

参数:
  projectId              项目 ID（必需）

选项:
  --taskflow-id <ID>     指定工作流 ID
  --q <关键词>           按状态名称模糊搜索
  --only-start           只返回 kind=start 的状态（可用于创建任务的初始状态）
  --help                 显示帮助

示例:
  uv run scripts/get_taskflow_statuses.py 67ec9b8c3c6130ac88605c3e
  uv run scripts/get_taskflow_statuses.py 67ec9b8c3c6130ac88605c3e --only-start
  uv run scripts/get_taskflow_statuses.py 67ec9b8c3c6130ac88605c3e --q '进行中'""")
        sys.exit(0 if "--help" in sys.argv else 1)

    project_id = sys.argv[1]
    taskflow_id: Optional[str] = None
    q: Optional[str] = None
    only_start = False

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--taskflow-id" and i + 1 < len(sys.argv):
            taskflow_id = sys.argv[i + 1]; i += 2
        elif arg == "--q" and i + 1 < len(sys.argv):
            q = sys.argv[i + 1]; i += 2
        elif arg == "--only-start":
            only_start = True; i += 1
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    get_taskflow_statuses(project_id, taskflow_id, q, only_start)


if __name__ == "__main__":
    main()
