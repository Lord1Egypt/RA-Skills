#!/usr/bin/env python3
"""
Broader repeatable smoke coverage for durable-task-runner core helpers.

Scope:
- task create/update/progress/report/ticker
- subagent line assign/ingest/check
- resume bootstrap/apply path via the existing validation smoke helper

This stays local-only and favors practical regression coverage over a giant test rig.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
STATE_DIR = ROOT / "state" / "tasks"


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


def assert_contains(haystack: str, needle: str, label: str) -> None:
    if needle not in haystack:
        raise SystemExit(f"{label}: expected to find {needle!r} in output: {haystack}")


def main() -> int:
    task_id = f"core-smoke-{now_tag()}"
    milestones = json.dumps([
        {"id": "s1", "title": "Create smoke task", "status": "done", "percent": 100},
        {"id": "s2", "title": "Exercise core helpers", "status": "running", "percent": 70},
        {"id": "s3", "title": "Verify outputs", "status": "pending", "percent": 0},
    ])
    done_criteria = json.dumps([
        "reporting renders",
        "subagent line flow renders",
        "resume smoke passes",
    ])
    constraints = json.dumps(["non-destructive", "local-only"])

    run(
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "create", task_id,
        "--title", "Core smoke task",
        "--goal", "Exercise core durable-task-runner helpers",
        "--done-criteria", done_criteria,
        "--constraints", constraints,
        "--desired-state", "running",
        "--execution-priority", "tokens",
        "--phase", "smoke",
        "--health", "healthy",
        "--next-step", "exercise reporter and subagent helpers",
        "--milestones", milestones,
    )

    run(
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "progress", task_id,
        "smoke baseline recorded",
        "--phase", "smoke",
        "--health", "healthy",
        "--next-step", "exercise reporter and subagent helpers",
    )

    ticker = run("python3", str(SCRIPT_DIR / "task_ticker.py"), task_id)
    assert_contains(ticker, "task [", "ticker")
    assert_contains(ticker, "proj [", "ticker")

    report = run("python3", str(SCRIPT_DIR / "task_report.py"), task_id, "--level", "3")
    assert_contains(report, "current [", "report")
    assert_contains(report, "project [", "report")

    run(
        "python3", str(SCRIPT_DIR / "task_subagent_ctl.py"), "assign", task_id,
        "smoke-line",
        "Exercise worker return ingestion",
        "--owner", "worker",
        "--node", "smoke-node",
        "--summary", "Core smoke line for subagent helper coverage.",
    )
    worker_return = f"""tag: autopilot\ntask_id: {task_id}\nline: smoke-line\nnode: smoke-node\ngoal_status: partial\nnext_role: worker\n\nGoal\n- Exercise worker return ingestion\n\nCompleted\n- Produced a structured worker return\n\nChanged artifacts/files\n- none\n\nCurrent status\n- waiting on controller decision\n\nNext step\n- controller dispatches next node\n\nRisk\n- none\n"""
    run(
        "python3", str(SCRIPT_DIR / "task_subagent_ctl.py"), "ingest", task_id,
        input_text=worker_return,
    )
    line_check = json.loads(run("python3", str(SCRIPT_DIR / "task_subagent_ctl.py"), "check", task_id))
    if not line_check.get("attention"):
        raise SystemExit(f"expected attention line after autopilot return: {line_check}")

    validation = json.loads(run("python3", str(SCRIPT_DIR / "task_validation_smoke.py")))
    if not validation.get("ok"):
        raise SystemExit(f"validation smoke did not pass: {validation}")

    print(json.dumps({
        "ok": True,
        "task_id": task_id,
        "ticker": ticker.strip(),
        "report": report.strip(),
        "line_check": {
            "attention": len(line_check.get("attention", [])),
            "active": len(line_check.get("active", [])),
            "resolved": len(line_check.get("resolved", [])),
        },
        "resume_validation_task": validation.get("task_id"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
