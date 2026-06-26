#!/usr/bin/env python3
"""
更新 Teambition 任务（多字段并行更新）
用法: uv run scripts/update_task.py --task-id <ID> [字段选项...]

优先级: 0=紧急 1=高 2=中 3=低
日期: 传入东八区时间，脚本自动转换为 UTC
"""

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Tuple

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


def _do_update(label: str, method: str, path: str, body: Dict[str, Any]) -> Tuple[str, bool]:
    try:
        if method == "PUT":
            call_api.put(path, body)
        else:
            call_api.post(path, body)
        return label, True
    except SystemExit:
        return label, False


def update_task(task_id: str, updates: Dict[str, Any]) -> bool:
    """并行执行所有字段更新，返回是否全部成功。"""
    jobs: List[Tuple[str, str, str, Dict[str, Any]]] = []

    if "content" in updates:
        jobs.append(("标题", "PUT", f"v3/task/{task_id}/content", {"content": updates["content"]}))
    if "executorId" in updates:
        jobs.append(("执行人", "PUT", f"v3/task/{task_id}/executor", {"executorId": updates["executorId"]}))
    if "dueDate" in updates:
        jobs.append(("截止日期", "PUT", f"v3/task/{task_id}/dueDate", {"dueDate": updates["dueDate"]}))
    if "startDate" in updates:
        jobs.append(("开始日期", "PUT", f"v3/task/{task_id}/startDate", {"startDate": updates["startDate"]}))
    if "note" in updates:
        jobs.append(("备注", "PUT", f"v3/task/{task_id}/note", {"note": updates["note"]}))
    if "priority" in updates:
        jobs.append(("优先级", "PUT", f"v3/task/{task_id}/priority", {"priority": updates["priority"]}))
    if "storyPoint" in updates:
        jobs.append(("故事点", "PUT", f"v3/task/{task_id}/storyPoint", {"storyPoint": updates["storyPoint"]}))
    if "taskflowstatusId" in updates:
        jobs.append(("任务状态", "PUT", f"v3/task/{task_id}/taskflowstatus", {"taskflowstatusId": updates["taskflowstatusId"]}))

    # 参与者（involveMembers / addInvolvers / delInvolvers）
    involver_payload: Dict[str, Any] = {}
    if "involveMembers" in updates:
        involver_payload["involveMembers"] = updates["involveMembers"]
    if "addInvolvers" in updates:
        involver_payload["addInvolvers"] = updates["addInvolvers"]
    if "delInvolvers" in updates:
        involver_payload["delInvolvers"] = updates["delInvolvers"]
    if involver_payload:
        jobs.append(("参与者", "PUT", f"v3/task/{task_id}/involveMembers", involver_payload))

    # 自定义字段（每个字段单独调用 POST）
    for idx, cf in enumerate(updates.get("customfields", [])):
        jobs.append((f"自定义字段#{idx+1}", "POST", f"v3/task/{task_id}/customfield/update", cf))

    if not jobs:
        print("❌ 未指定任何要更新的字段", file=sys.stderr)
        return False

    print(f"并行更新 {len(jobs)} 个字段...", file=sys.stderr)
    results: List[Tuple[str, bool]] = []

    with ThreadPoolExecutor(max_workers=min(len(jobs), 10)) as executor:
        futures = {executor.submit(_do_update, label, method, path, body): label
                   for label, method, path, body in jobs}
        for future in as_completed(futures):
            label, ok = future.result()
            results.append((label, ok))
            status = "✅" if ok else "❌"
            print(f"  {status} {label}", file=sys.stderr)

    success_count = sum(1 for _, ok in results if ok)
    print(f"完成: {success_count}/{len(jobs)} 成功", file=sys.stderr)
    return success_count == len(jobs)


def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/update_task.py --task-id <ID> [字段选项...]

必需:
  --task-id <ID>                任务 ID

可更新字段:
  --title <标题>                任务标题
  --executor-id <ID>            执行人 ID
  --due-date <日期>             截止日期（东八区，自动转 UTC）
  --start-date <日期>           开始日期（东八区，自动转 UTC）
  --note <备注>                 任务备注
  --priority <0-3>              优先级（0=紧急 1=高 2=中 3=低）
  --story-point <点数>          故事点
  --taskflowstatus-id <ID>      任务状态 ID
  --involve-members <JSON>      参与者列表（完全替换）
  --add-involvers <JSON>        新增参与者
  --del-involvers <JSON>        移除参与者
  --customfields <JSON>         自定义字段数组（使用 customfieldId 而非 cfId）
  --help                        显示帮助

示例:
  uv run scripts/update_task.py --task-id 'xxx' --content '新标题' --priority 0
  uv run scripts/update_task.py --task-id 'xxx' --due-date '2026-04-01' --executor-id 'uid'""")
        sys.exit(0)

    task_id: Optional[str] = None
    updates: Dict[str, Any] = {}

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--task-id" and i + 1 < len(sys.argv):
            task_id = sys.argv[i + 1]; i += 2
        elif arg == "--title" and i + 1 < len(sys.argv):
            updates["content"] = sys.argv[i + 1]; i += 2
        elif arg == "--executor-id" and i + 1 < len(sys.argv):
            updates["executorId"] = sys.argv[i + 1]; i += 2
        elif arg == "--due-date" and i + 1 < len(sys.argv):
            updates["dueDate"] = cst_to_utc(sys.argv[i + 1]); i += 2
        elif arg == "--start-date" and i + 1 < len(sys.argv):
            updates["startDate"] = cst_to_utc(sys.argv[i + 1]); i += 2
        elif arg == "--note" and i + 1 < len(sys.argv):
            updates["note"] = sys.argv[i + 1]; i += 2
        elif arg == "--priority" and i + 1 < len(sys.argv):
            updates["priority"] = int(sys.argv[i + 1]); i += 2
        elif arg == "--story-point" and i + 1 < len(sys.argv):
            updates["storyPoint"] = sys.argv[i + 1]; i += 2
        elif arg == "--taskflowstatus-id" and i + 1 < len(sys.argv):
            updates["taskflowstatusId"] = sys.argv[i + 1]; i += 2
        elif arg == "--involve-members" and i + 1 < len(sys.argv):
            updates["involveMembers"] = json.loads(sys.argv[i + 1]); i += 2
        elif arg == "--add-involvers" and i + 1 < len(sys.argv):
            updates["addInvolvers"] = json.loads(sys.argv[i + 1]); i += 2
        elif arg == "--del-involvers" and i + 1 < len(sys.argv):
            updates["delInvolvers"] = json.loads(sys.argv[i + 1]); i += 2
        elif arg == "--customfields" and i + 1 < len(sys.argv):
            updates["customfields"] = json.loads(sys.argv[i + 1]); i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    if not task_id:
        print("❌ 缺少 --task-id", file=sys.stderr); sys.exit(1)

    ok = update_task(task_id, updates)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
