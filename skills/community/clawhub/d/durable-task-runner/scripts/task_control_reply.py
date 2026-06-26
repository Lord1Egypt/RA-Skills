#!/usr/bin/env python3
"""
Render a compact user-facing control reply for a recorded steer/interruption.

Purpose:
- keep user control visible without large conversational overhead
- explain unsafe-to-interrupt conditions when needed
- tell the user what happens next in a compact deterministic format
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def latest_user_control(task: dict[str, Any]) -> dict[str, Any]:
    pending = task.get("pending_actions", []) or []
    controls = [p for p in pending if isinstance(p, dict) and p.get("kind") == "user_control"]
    if not controls:
        raise SystemExit("no user_control pending action found")
    return controls[-1]


def current_activity(task: dict[str, Any]) -> str:
    for item in task.get("artifacts", []):
        if not isinstance(item, dict) or item.get("kind") != "subagent_lines":
            continue
        lines = item.get("lines", {}) or {}
        active = [name for name, line in lines.items() if line.get("status") == "assigned"]
        if active:
            return f"active line(s): {', '.join(active)}"
    phase = task.get("phase", "n/a")
    next_step = task.get("next_step", "n/a")
    return f"{phase}; next: {next_step}"


def render(task: dict[str, Any], control: dict[str, Any]) -> str:
    boundary = control.get("boundary", "immediate")
    intent = control.get("intent", "steer")
    message = control.get("message", "")
    activity = current_activity(task)
    if boundary == "immediate":
        return f"ack: {intent} applied | {activity}"
    reason = control.get("unsafe_reason") or control.get("reason") or "unsafe right now"
    return f"ack: {intent} queued | doing: {activity} | unsafe-now: {reason} | will pause at next safe boundary"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    args = p.parse_args()
    task = load_task(args.task_id)
    control = latest_user_control(task)
    print(render(task, control))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
