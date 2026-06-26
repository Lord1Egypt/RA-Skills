#!/usr/bin/env python3
"""
Repeatable smoke validation for durable-task-runner restart/apply flow.

Flow:
- create a throwaway non-bootstrap durable task
- seed a waiting controller line
- run resume bootstrap with plan output
- apply low-risk resume follow-through
- assert task state advanced as expected

This is intentionally narrow and local-only.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
SCRIPT_DIR = ROOT / "scripts"


def now_tag() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def run(*args: str, input_text: str | None = None) -> str:
    proc = subprocess.run(
        list(args),
        text=True,
        input=input_text,
        capture_output=True,
        check=True,
    )
    return proc.stdout


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def main() -> int:
    task_id = f"validation-smoke-{now_tag()}"
    milestones = json.dumps([
        {"id": "v1", "title": "Create validation task", "status": "done", "percent": 100},
        {"id": "v2", "title": "Exercise restart path", "status": "running", "percent": 50},
        {"id": "v3", "title": "Confirm state advanced", "status": "pending", "percent": 0},
    ])
    done_criteria = json.dumps([
        "bootstrap scan works",
        "resume apply works",
        "state advances after restart",
    ])
    constraints = json.dumps(["non-destructive", "local-only"])

    run(
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "create", task_id,
        "--title", "Validation smoke flow",
        "--goal", "Validate restart/apply flow on a throwaway non-bootstrap task",
        "--done-criteria", done_criteria,
        "--constraints", constraints,
        "--desired-state", "running",
        "--execution-priority", "tokens",
        "--phase", "validation",
        "--health", "healthy",
        "--next-step", "await controller resume decision",
        "--milestones", milestones,
    )

    run(
        "python3", str(SCRIPT_DIR / "task_subagent_ctl.py"), "assign", task_id,
        "validate-line",
        "Resume a waiting controller line on a non-bootstrap task",
        "--owner", "worker",
        "--node", "validation-node",
        "--summary", "Validation task waiting for a low-risk controller decision.",
    )

    worker_return = """tag: autopilot
task_id: {task_id}
line: validate-line
node: validation-node
goal_status: partial
next_role: worker

Goal
- Validate non-bootstrap resume/apply flow

Completed
- Reached waiting-controller state

Changed artifacts/files
- none

Current status
- waiting on controller decision

Next step
- controller dispatches line

Risk
- none
""".format(task_id=task_id)
    run(
        "python3", str(SCRIPT_DIR / "task_subagent_ctl.py"), "ingest", task_id,
        input_text=worker_return,
    )

    bootstrap_raw = run(
        "python3", str(SCRIPT_DIR / "task_resume_bootstrap.py"),
        "--task-id", task_id,
        "--plan",
    )
    bootstrap = json.loads(bootstrap_raw)
    task_summary = bootstrap["tasks"][0]
    recommendation = task_summary["recommendation"]["action"]
    if recommendation != "controller_decision_needed":
        raise SystemExit(f"unexpected recommendation: {recommendation}")

    apply_raw = run(
        "python3", str(SCRIPT_DIR / "task_resume_apply.py"),
        input_text=bootstrap_raw,
    )
    apply_payload = json.loads(apply_raw)
    apply_item = apply_payload["applied"][0]
    if not apply_item.get("applied"):
        raise SystemExit(f"resume apply did not apply: {apply_item}")

    task = load_task(task_id)
    line = None
    for item in task.get("artifacts", []):
        if isinstance(item, dict) and item.get("kind") == "subagent_lines":
            line = (item.get("lines", {}) or {}).get("validate-line")
            if line:
                break
    if not line:
        raise SystemExit("validate-line missing after apply")
    if task.get("desired_state") != "running":
        raise SystemExit(f"task not running after apply: {task.get('desired_state')}")
    if line.get("controller_decision") != "dispatch":
        raise SystemExit(f"unexpected controller_decision: {line.get('controller_decision')}")
    if line.get("status") != "assigned":
        raise SystemExit(f"unexpected line status: {line.get('status')}")
    if task.get("next_step") != "continue resumed line: validate-line":
        raise SystemExit(f"unexpected next_step: {task.get('next_step')}")

    print(json.dumps({
        "ok": True,
        "task_id": task_id,
        "bootstrap_action": recommendation,
        "apply": apply_item,
        "final": {
            "desired_state": task.get("desired_state"),
            "next_step": task.get("next_step"),
            "line_status": line.get("status"),
            "controller_decision": line.get("controller_decision"),
        },
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
