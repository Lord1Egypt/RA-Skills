#!/usr/bin/env python3
"""
Context-pressure guardrail helper for durable-task-runner.

Purpose:
- make the 45% prepare / 50% hard-stop rule explicit and scriptable
- checkpoint durable state before hot context becomes a cliff
- at hard stop: pause the durable task, queue immediate resume intent, and emit a
  compact machine-readable handoff payload for the next session

This helper intentionally does not perform the actual session reset itself.
It records the state needed so the surrounding runtime/controller can do that safely.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
SCRIPT_DIR = ROOT / "scripts"
QUEUE_PATH = STATE_DIR / "interrupt-queue.json"
PREPARE_THRESHOLD = 45
HARD_STOP_THRESHOLD = 50


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def load_queue() -> list[dict[str, Any]]:
    if not QUEUE_PATH.exists():
        return []
    try:
        data = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def current_context_bucket(percent: int) -> str:
    if percent >= HARD_STOP_THRESHOLD:
        return "hard_stop"
    if percent >= PREPARE_THRESHOLD:
        return "prepare"
    return "ok"


def recent_pending_resume(task_id: str) -> dict[str, Any] | None:
    for item in reversed(load_queue()):
        if item.get("task_id") != task_id:
            continue
        if item.get("source") != "context_guard_hard_stop":
            continue
        return item
    return None


def run_json(*args: str) -> dict[str, Any]:
    proc = subprocess.run(list(args), text=True, capture_output=True, check=True)
    raw = (proc.stdout or "").strip()
    if not raw:
        return {}
    return json.loads(raw)


def add_resume_queue(task: dict[str, Any], percent: int, session: str) -> dict[str, Any]:
    existing = recent_pending_resume(task["task_id"])
    if existing is not None:
        return existing
    title = f"Resume durable task after context reset: {task.get('title', task['task_id'])}"
    context = (
        f"Session context hit {percent}% hard stop. Resume durable task {task['task_id']} immediately after reset. "
        f"Phase={task.get('phase', 'n/a')}. Next step={task.get('next_step', 'n/a')}"
    )
    acceptance = "Task resumes from durable state in the new session without asking again."
    run_json(
        "python3", str(SCRIPT_DIR / "task_resume_queue.py"), "add",
        "--task-id", task["task_id"],
        "--title", title,
        "--context", context,
        "--acceptance", acceptance,
        "--source", "context_guard_hard_stop",
        "--session", session,
    )
    return recent_pending_resume(task["task_id"]) or {
        "task_id": task["task_id"],
        "title": title,
        "context": context,
        "acceptance": acceptance,
        "source": "context_guard_hard_stop",
        "session": session,
    }


def prepare(task: dict[str, Any], percent: int) -> dict[str, Any]:
    message = (
        f"Context reached {percent}%: prepare clean handoff now. "
        f"Checkpoint durable state and avoid expanding hot context further."
    )
    subprocess.run([
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "progress", task["task_id"], message,
        "--phase", task.get("phase", ""),
        "--health", task.get("health", "healthy"),
        "--next-step", task.get("next_step", ""),
        "--report-kind", "internal",
    ], check=True, stdout=subprocess.DEVNULL)
    return {
        "task_id": task["task_id"],
        "action": "prepare",
        "context_percent": percent,
        "message": message,
    }


def hard_stop(task: dict[str, Any], percent: int, session: str) -> dict[str, Any]:
    note = (
        f"Pause for hot-context reset: session crossed {percent}% context. Durable state is current. "
        f"After reset, resume immediately from task {task['task_id']} and continue: {task.get('next_step', 'n/a')}"
    )
    subprocess.run([
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "control", task["task_id"], "paused",
        "--note", note,
        "--report-kind", "internal",
    ], check=True, stdout=subprocess.DEVNULL)
    subprocess.run([
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "update", task["task_id"],
        "--phase", "pause",
        "--next-step", "After reset, resume immediately from durable state in the new session",
        "--report-kind", "internal",
    ], check=True, stdout=subprocess.DEVNULL)
    queued = add_resume_queue(task, percent, session)
    handoff = {
        "task_id": task["task_id"],
        "title": task.get("title", task["task_id"]),
        "context_percent": percent,
        "resume_queue": queued,
        "reset_requested": True,
        "resume_immediately": True,
        "next_step": task.get("next_step", ""),
        "note": note,
    }
    print(json.dumps(handoff, indent=2))
    return handoff


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("context_percent", type=int)
    p.add_argument("--session", default="current")
    args = p.parse_args()

    task = load_task(args.task_id)
    bucket = current_context_bucket(args.context_percent)
    if bucket == "ok":
        print(json.dumps({
            "task_id": args.task_id,
            "action": "none",
            "context_percent": args.context_percent,
            "thresholds": {"prepare": PREPARE_THRESHOLD, "hard_stop": HARD_STOP_THRESHOLD},
        }, indent=2))
        return 0
    if bucket == "prepare":
        print(json.dumps(prepare(task, args.context_percent), indent=2))
        return 0
    hard_stop(task, args.context_percent, args.session)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
