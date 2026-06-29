from __future__ import annotations

import argparse
import json

from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action_value", required=True)
    args = parser.parse_args()

    value = args.action_value.strip()
    if value in {"target:personal", "target:team"}:
        out({
            "success": True,
            "action": "select_target",
            "target_scope": value.split(":", 1)[1],
            "next": "call_prepare_batch_again",
        })
        return

    if value.startswith("project:"):
        project_id = value.split(":", 1)[1]
        out({
            "success": True,
            "action": "select_project",
            "target_project_id": project_id,
            "needs_create_project": project_id == "create",
            "next": "call_prepare_batch_again" if project_id != "create" else "call_create_project",
        })
        return

    if value.startswith("start_batch:"):
        task_id = value.split(":", 1)[1]
        out({
            "success": True,
            "action": "start_batch",
            "command": "run_batch.py",
            "args": {"task_id": task_id},
            "sender_arg": "confirmed_by",
        })
        return

    if value.startswith("cancel_batch:"):
        task_id = value.split(":", 1)[1]
        out({
            "success": True,
            "action": "cancel_batch",
            "command": "cancel_task.py",
            "args": {"task_id": task_id},
        })
        return

    if value.startswith("job_status:"):
        job_id = value.split(":", 1)[1]
        out({"success": True, "action": "job_status", "job_id": job_id})
        return

    out(json_fail("unknown_card_action", "无法识别 batch_compile 卡片动作。"))


if __name__ == "__main__":
    main()
