#!/usr/bin/env python3
"""
Repeatable smoke validation for user-control interruption semantics.

Flow:
- create a throwaway durable task
- record an immediate pause request and verify it applies now
- create another throwaway durable task with an active line
- record an unsafe-now stop request and verify it is acknowledged + deferred
- run bootstrap/apply and verify the deferred control pauses the task at the next safe boundary
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
SCRIPT_DIR = ROOT / "scripts"


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def run(*args: str, input_text: str | None = None) -> str:
    proc = subprocess.run(list(args), text=True, input=input_text, capture_output=True, check=True)
    return proc.stdout


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def create_task(task_id: str, next_step: str) -> None:
    milestones = json.dumps([
        {"id": "m1", "title": "create", "status": "done", "percent": 100},
        {"id": "m2", "title": "run", "status": "running", "percent": 50},
    ])
    run(
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "create", task_id,
        "--title", "Control smoke",
        "--goal", "Validate user control handling",
        "--desired-state", "running",
        "--phase", "control-smoke",
        "--health", "healthy",
        "--next-step", next_step,
        "--milestones", milestones,
    )


def main() -> int:
    immediate_id = f"control-smoke-immediate-{now_tag()}"
    create_task(immediate_id, "await immediate pause test")
    immediate_raw = run(
        "python3", str(SCRIPT_DIR / "task_user_steer.py"),
        immediate_id, "pause", "pause now for operator",
    )
    immediate = json.loads(immediate_raw)
    if immediate["boundary"] != "immediate":
        raise SystemExit(f"expected immediate boundary, got {immediate['boundary']}")
    task = load_task(immediate_id)
    if task.get("desired_state") != "paused":
        raise SystemExit(f"expected paused task, got {task.get('desired_state')}")

    deferred_id = f"control-smoke-deferred-{now_tag()}"
    create_task(deferred_id, "continue critical slice")
    run(
        "python3", str(SCRIPT_DIR / "task_subagent_ctl.py"), "assign", deferred_id,
        "critical-line",
        "Finish a critical bounded slice",
        "--owner", "worker",
        "--node", "critical-node",
        "--summary", "Simulate work that should pause only at the next safe boundary.",
    )
    deferred_raw = run(
        "python3", str(SCRIPT_DIR / "task_user_steer.py"),
        deferred_id, "stop", "stop after this bounded slice",
        "--unsafe-now",
        "--unsafe-reason", "mid-write critical section",
    )
    deferred = json.loads(deferred_raw)
    if deferred["boundary"] != "deferred":
        raise SystemExit(f"expected deferred boundary, got {deferred['boundary']}")
    reply = run("python3", str(SCRIPT_DIR / "task_control_reply.py"), deferred_id).strip()
    if "unsafe-now: mid-write critical section" not in reply:
        raise SystemExit(f"missing unsafe reason in reply: {reply}")

    bootstrap = json.loads(run("python3", str(SCRIPT_DIR / "task_resume_bootstrap.py"), "--task-id", deferred_id, "--plan"))
    action = bootstrap["tasks"][0]["recommendation"]["action"]
    if action != "user_control_pending":
        raise SystemExit(f"expected user_control_pending, got {action}")
    apply_payload = json.loads(run("python3", str(SCRIPT_DIR / "task_resume_apply.py"), input_text=json.dumps(bootstrap)))
    applied = apply_payload["applied"][0]
    if not applied.get("applied"):
        raise SystemExit(f"deferred user control was not applied: {applied}")
    task2 = load_task(deferred_id)
    if task2.get("desired_state") != "paused":
        raise SystemExit(f"expected paused deferred task, got {task2.get('desired_state')}")

    print(json.dumps({
        "ok": True,
        "immediate": {
            "task_id": immediate_id,
            "boundary": immediate["boundary"],
            "desired_state": task.get("desired_state"),
        },
        "deferred": {
            "task_id": deferred_id,
            "boundary": deferred["boundary"],
            "reply": reply,
            "bootstrap_action": action,
            "desired_state": task2.get("desired_state"),
        },
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
