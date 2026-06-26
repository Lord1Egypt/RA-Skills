#!/usr/bin/env python3
"""
创建 Teambition 任务
用法: uv run scripts/create_task.py --title <标题> [选项]

时区说明: 日期参数请传入东八区时间，脚本自动转换为 UTC（减 8 小时）。
优先级: 0=紧急 1=高 2=中 3=低
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional

import call_api

CST = timezone(timedelta(hours=8))

def cst_to_utc(dt_str: str) -> str:
    """将东八区 ISO 字符串转换为 UTC ISO 字符串。若已含 Z/+00:00 则原样返回。"""
    if dt_str.endswith("Z") or "+00:00" in dt_str:
        return dt_str
    # 尝试解析为 naive datetime，视为 CST
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(dt_str, fmt)
            dt_cst = dt.replace(tzinfo=CST)
            dt_utc = dt_cst.astimezone(timezone.utc)
            return dt_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except ValueError:
            continue
    # 无法解析，原样返回
    return dt_str

def create_task(task_data: Dict[str, Any]) -> None:
    payload: Dict[str, Any] = {"content": task_data["content"]}

    optional = [
        "projectId", "executorId", "involveMembers", "taskflowstatusId",
        "startDate", "dueDate", "note", "priority", "parentTaskId",
        "progress", "visible", "storyPoint", "scenariofieldconfigId", "customfields",
    ]
    for field in optional:
        if field in task_data and task_data[field] is not None:
            payload[field] = task_data[field]

    data = call_api.post("v3/task/create", payload)
    task = data.get("result", data)
    print(json.dumps(task, ensure_ascii=False, indent=2))

def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/create_task.py --title <标题> [选项]

必需:
  --title <标题>                任务标题

可选:
  --project-id <ID>             项目 ID（先用 query_projects.py 按名称查询）
  --executor-id <ID>            执行人 ID（先用 query_members.py 按姓名查询）
  --involve-members <JSON>      参与者 ID 列表，JSON 数组
  --taskflowstatus-id <ID>      任务状态 ID（先用 get_taskflow_statuses.py 查询）
  --start-date <日期>           开始日期（东八区，自动转 UTC）
  --due-date <日期>             截止日期（东八区，自动转 UTC）
  --note <备注>                 任务备注
  --priority <0-3>              优先级（0=紧急 1=高 2=中 3=低）
  --parent-task-id <ID>         父任务 ID（创建子任务）
  --progress <0-100>            进度百分比
  --visible <类型>              可见性（involves=仅参与者 members=项目成员）
  --story-point <点数>          故事点
  --scenariofieldconfig-id <ID> 任务类型 ID
  --customfields <JSON>         自定义字段，JSON 数组
  --help                        显示帮助

示例:
  uv run scripts/create_task.py \\
    --project-id 'xxx' --title '完成需求文档'

  uv run scripts/create_task.py \\
    --project-id 'xxx' --title '实现登录模块' \\
    --executor-id 'uid' --due-date '2026-04-01' --priority 1""")
        sys.exit(0)

    task_data: Dict[str, Any] = {}
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--title" and i + 1 < len(sys.argv):
            task_data["content"] = sys.argv[i + 1]; i += 2
        elif arg == "--project-id" and i + 1 < len(sys.argv):
            task_data["projectId"] = sys.argv[i + 1]; i += 2
        elif arg == "--executor-id" and i + 1 < len(sys.argv):
            task_data["executorId"] = sys.argv[i + 1]; i += 2
        elif arg == "--involve-members" and i + 1 < len(sys.argv):
            task_data["involveMembers"] = json.loads(sys.argv[i + 1]); i += 2
        elif arg == "--taskflowstatus-id" and i + 1 < len(sys.argv):
            task_data["taskflowstatusId"] = sys.argv[i + 1]; i += 2
        elif arg == "--start-date" and i + 1 < len(sys.argv):
            task_data["startDate"] = cst_to_utc(sys.argv[i + 1]); i += 2
        elif arg == "--due-date" and i + 1 < len(sys.argv):
            task_data["dueDate"] = cst_to_utc(sys.argv[i + 1]); i += 2
        elif arg == "--note" and i + 1 < len(sys.argv):
            task_data["note"] = sys.argv[i + 1]; i += 2
        elif arg == "--priority" and i + 1 < len(sys.argv):
            task_data["priority"] = int(sys.argv[i + 1]); i += 2
        elif arg == "--parent-task-id" and i + 1 < len(sys.argv):
            task_data["parentTaskId"] = sys.argv[i + 1]; i += 2
        elif arg == "--progress" and i + 1 < len(sys.argv):
            task_data["progress"] = int(sys.argv[i + 1]); i += 2
        elif arg == "--visible" and i + 1 < len(sys.argv):
            task_data["visible"] = sys.argv[i + 1]; i += 2
        elif arg == "--story-point" and i + 1 < len(sys.argv):
            task_data["storyPoint"] = sys.argv[i + 1]; i += 2
        elif arg == "--scenariofieldconfig-id" and i + 1 < len(sys.argv):
            task_data["scenariofieldconfigId"] = sys.argv[i + 1]; i += 2
        elif arg == "--customfields" and i + 1 < len(sys.argv):
            task_data["customfields"] = json.loads(sys.argv[i + 1]); i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    if "content" not in task_data:
        print("❌ 缺少必需参数 --title", file=sys.stderr); sys.exit(1)

    create_task(task_data)

if __name__ == "__main__":
    main()