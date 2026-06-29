from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def restore_or_remove_source(task: dict) -> str:
    source_id = task.get("source_id", "")
    if not source_id:
        return "no_source"
    if task.get("source_was_existing") and task.get("previous_source_record"):
        previous = task["previous_source_record"]

        def restore(current: dict) -> dict:
            current[source_id] = previous
            return current

        sc.update_json("sources.json", restore, default={})
        return "restored_previous_source"

    def remove(current: dict) -> dict:
        current.pop(source_id, None)
        return current

    sc.update_json("sources.json", remove, default={})
    return "removed_pending_source"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", required=True)
    parser.add_argument("--sender_id", required=True)
    args = parser.parse_args()

    tasks = sc.active_tasks()
    task = tasks.get(args.task_id)
    if not task:
        out(json_fail("task_not_found", "找不到待取消的批量编译确认任务。"))
        return
    if task.get("type") != "batch_compile_confirm":
        out(json_fail("bad_task_type", "该任务不是批量编译确认任务。"))
        return
    if task.get("created_by") != args.sender_id:
        out(json_fail("permission_denied", "只有发起该批量编译的人可以取消。"))
        return

    def mutate(current: dict) -> dict:
        current.pop(args.task_id, None)
        return current

    source_cleanup = restore_or_remove_source(task)
    sc.update_json("active_tasks.json", mutate, default={})
    out({
        "success": True,
        "cancelled": True,
        "task_id": args.task_id,
        "source_cleanup": source_cleanup,
        "cancelled_at": now_str(),
    })


if __name__ == "__main__":
    main()
