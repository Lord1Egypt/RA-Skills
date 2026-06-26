#!/usr/bin/env python3
"""
Teambition 迭代管理（创建/开始/完成迭代）
用法: uv run scripts/manage_sprint.py --action <动作> [选项]

动作:
  create   创建迭代（需要 --project-id 和 --name）
  start    开始迭代（需要 --project-id 和 --sprint-id）
  complete 完成迭代（需要 --project-id 和 --sprint-id）
  list     查询项目迭代列表（需要 --project-id）
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from typing import Optional

import call_api

CST = timezone(timedelta(hours=8))

def cst_to_utc(dt_str: str) -> str:
    if dt_str.endswith("Z") or "+00:00" in dt_str:
        return dt_str
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(dt_str, fmt).replace(tzinfo=CST)
            return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except ValueError:
            continue
    return dt_str

def create_sprint(project_id: str, name: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> None:
    body: dict = {"name": name}
    if start_date:
        body["startDate"] = cst_to_utc(start_date)
    if end_date:
        body["endDate"] = cst_to_utc(end_date)
    data = call_api.post(f"v3/project/{project_id}/sprint/create", body)
    result = data.get("result", data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sprint_id = result.get("id", "?") if isinstance(result, dict) else "?"
    print(f"✅ 迭代已创建，ID: {sprint_id}", file=sys.stderr)

def start_sprint(project_id: str, sprint_id: str) -> None:
    data = call_api.put(f"v3/project/{project_id}/sprint/{sprint_id}/start", {})
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"✅ 迭代 {sprint_id} 已开始", file=sys.stderr)

def complete_sprint(project_id: str, sprint_id: str) -> None:
    data = call_api.put(f"v3/project/{project_id}/sprint/{sprint_id}/complete", {})
    print(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"✅ 迭代 {sprint_id} 已完成", file=sys.stderr)

def list_sprints(project_id: str) -> None:
    data = call_api.get(f"v3/project/{project_id}/sprints")
    result = data.get("result", data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    count = len(result) if isinstance(result, list) else "?"
    print(f"共找到 {count} 个迭代", file=sys.stderr)

def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/manage_sprint.py --action <动作> [选项]

动作:
  create    创建迭代
  start     开始迭代
  complete  完成迭代
  list      查询迭代列表

选项:
  --action <动作>         必需，见上方动作列表
  --project-id <ID>       项目 ID（create/list 时必需）
  --sprint-id <ID>        迭代 ID（start/complete 时必需）
  --name <名称>           迭代名称（create 时必需）
  --start-date <日期>     迭代开始日期（东八区，可选）
  --end-date <日期>       迭代结束日期（东八区，可选）
  --help                  显示帮助

示例:
  # 创建迭代
  uv run scripts/manage_sprint.py --action create --project-id 'xxx' --name 'Sprint 3'

  # 开始迭代
  uv run scripts/manage_sprint.py --action start --project-id 'xxx' --sprint-id 'yyy'

  # 完成迭代
  uv run scripts/manage_sprint.py --action complete --project-id 'xxx' --sprint-id 'yyy'

  # 查询迭代列表
  uv run scripts/manage_sprint.py --action list --project-id 'xxx'""")
        sys.exit(0)

    action: Optional[str] = None
    project_id: Optional[str] = None
    sprint_id: Optional[str] = None
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--action" and i + 1 < len(sys.argv):
            action = sys.argv[i + 1]; i += 2
        elif arg == "--project-id" and i + 1 < len(sys.argv):
            project_id = sys.argv[i + 1]; i += 2
        elif arg == "--sprint-id" and i + 1 < len(sys.argv):
            sprint_id = sys.argv[i + 1]; i += 2
        elif arg == "--name" and i + 1 < len(sys.argv):
            name = sys.argv[i + 1]; i += 2
        elif arg == "--start-date" and i + 1 < len(sys.argv):
            start_date = sys.argv[i + 1]; i += 2
        elif arg == "--end-date" and i + 1 < len(sys.argv):
            end_date = sys.argv[i + 1]; i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)

    if not action:
        print("❌ 缺少 --action（create/start/complete/list）", file=sys.stderr)
        sys.exit(1)

    if action == "create":
        if not project_id:
            print("❌ create 动作需要 --project-id", file=sys.stderr); sys.exit(1)
        if not name:
            print("❌ create 动作需要 --name", file=sys.stderr); sys.exit(1)
        create_sprint(project_id, name, start_date, end_date)
    elif action == "start":
        if not sprint_id:
            print("❌ start 动作需要 --sprint-id", file=sys.stderr); sys.exit(1)
        if not project_id:
            print("❌ start 动作需要 --project-id", file=sys.stderr); sys.exit(1)
        start_sprint(project_id, sprint_id)
    elif action == "complete":
        if not sprint_id:
            print("❌ complete 动作需要 --sprint-id", file=sys.stderr); sys.exit(1)
        if not project_id:
            print("❌ complete 动作需要 --project-id", file=sys.stderr); sys.exit(1)
        complete_sprint(project_id, sprint_id)
    elif action == "list":
        if not project_id:
            print("❌ list 动作需要 --project-id", file=sys.stderr); sys.exit(1)
        list_sprints(project_id)
    else:
        print(f"❌ 未知动作: {action}，支持 create/start/complete/list", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()