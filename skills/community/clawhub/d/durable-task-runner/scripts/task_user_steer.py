#!/usr/bin/env python3
"""
Record and classify fresh user control input for a running durable task.

Purpose:
- give the user an immediate control plane over background durable execution
- classify whether the request can be obeyed immediately or must wait for a safe boundary
- durably record the pending steer so the worker/controller path cannot ignore it
- keep token cost low by producing compact machine-friendly output
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"

INTENT_ALIASES = {
    "pause": "pause",
    "stop": "stop",
    "resume": "resume",
    "edit": "edit",
    "steer": "steer",
    "note": "note",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def save_task(task: dict[str, Any]) -> None:
    (STATE_DIR / f"{task['task_id']}.json").write_text(json.dumps(task, indent=2) + "\n")


def append_event(task_id: str, payload: dict[str, Any]) -> None:
    path = STATE_DIR / f"{task_id}.events.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def append_progress(task_id: str, line: str) -> None:
    path = STATE_DIR / f"{task_id}.progress.log"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")


def iter_lines(task: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for item in task.get("artifacts", []):
        if not isinstance(item, dict) or item.get("kind") != "subagent_lines":
            continue
        for name, line in (item.get("lines", {}) or {}).items():
            rows.append((name, line))
    return rows


def pending_control(task: dict[str, Any]) -> list[dict[str, Any]]:
    pending = task.setdefault("pending_actions", [])
    if not isinstance(pending, list):
        pending = []
        task["pending_actions"] = pending
    return pending


def current_activity(task: dict[str, Any]) -> str:
    active = []
    waiting = []
    for name, line in iter_lines(task):
        status = line.get("status")
        if status == "assigned":
            active.append(name)
        elif status in {"autopilot", "handoff"}:
            waiting.append(name)
    if active:
        return f"active line(s): {', '.join(active)}"
    if waiting:
        return f"waiting control line(s): {', '.join(waiting)}"
    return f"phase={task.get('phase', 'n/a')}"


def classify_boundary(args: argparse.Namespace, task: dict[str, Any]) -> tuple[str, str]:
    if args.unsafe_now:
        return "deferred", args.unsafe_reason or "unsafe_to_interrupt_immediately"
    if args.safe_boundary_only:
        return "deferred", "safe_boundary_requested"
    if args.intent in {"pause", "stop"}:
        return "immediate", "safe_control_request"
    if args.intent in {"resume", "edit", "steer", "note"}:
        return "immediate", "steer_update"
    return "immediate", "default_immediate"


def apply_immediate(task: dict[str, Any], args: argparse.Namespace, ts: str) -> dict[str, Any]:
    if args.intent == "pause":
        task["desired_state"] = "paused"
        task["operator_note"] = args.message
        task["updated_at"] = ts
        return {"applied": True, "desired_state": "paused", "next_step": task.get("next_step", "")}
    if args.intent == "stop":
        task["desired_state"] = "stopped"
        task["operator_note"] = args.message
        task["updated_at"] = ts
        return {"applied": True, "desired_state": "stopped", "next_step": task.get("next_step", "")}
    if args.intent == "resume":
        task["desired_state"] = "running"
        task["steering_note"] = args.message
        task["updated_at"] = ts
        return {"applied": True, "desired_state": "running", "next_step": task.get("next_step", "")}
    if args.intent in {"edit", "steer", "note"}:
        task["steering_note"] = args.message
        task["updated_at"] = ts
        return {"applied": True, "desired_state": task.get("desired_state", "running"), "next_step": task.get("next_step", "")}
    return {"applied": False, "desired_state": task.get("desired_state", "running"), "next_step": task.get("next_step", "")}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("intent", choices=sorted(INTENT_ALIASES))
    p.add_argument("message")
    p.add_argument("--unsafe-now", action="store_true")
    p.add_argument("--unsafe-reason", default="")
    p.add_argument("--safe-boundary-only", action="store_true")
    args = p.parse_args()

    task = load_task(args.task_id)
    ts = now_iso()
    boundary, reason = classify_boundary(args, task)

    action_id = f"user-{args.intent}-{ts}"
    pending_entry = {
        "id": action_id,
        "kind": "user_control",
        "created_at": ts,
        "status": "pending" if boundary == "deferred" else "applied",
        "intent": args.intent,
        "message": args.message,
        "safe_boundary_only": bool(args.safe_boundary_only or args.unsafe_now),
        "unsafe_reason": args.unsafe_reason or "",
        "boundary": boundary,
    }
    pending_control(task).append(pending_entry)

    immediate = {"applied": False, "desired_state": task.get("desired_state", "running"), "next_step": task.get("next_step", "")}
    if boundary == "immediate":
        immediate = apply_immediate(task, args, ts)
        pending_entry["status"] = "applied"
        pending_entry["applied_at"] = ts
    else:
        task["operator_note"] = args.message
        task["updated_at"] = ts

    task.setdefault("reconcile", {})
    task["reconcile"] = {
        "needed": boundary == "deferred" or bool(task.get("pending_actions")),
        "reason": "pending_user_control" if boundary == "deferred" else task.get("reconcile", {}).get("reason", ""),
        "last_run_at": task.get("reconcile", {}).get("last_run_at"),
        "status": "pending_user_control" if boundary == "deferred" else task.get("reconcile", {}).get("status", "idle"),
    }
    task["updated_at"] = ts
    save_task(task)

    event_type = "user_control_received" if boundary == "immediate" else "user_control_deferred"
    append_event(args.task_id, {
        "ts": ts,
        "type": event_type,
        "task_id": args.task_id,
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {
            "intent": args.intent,
            "message": args.message,
            "boundary": boundary,
            "reason": reason,
            "unsafe_reason": args.unsafe_reason or "",
        },
    })
    append_progress(args.task_id, f"user control {args.intent}: {boundary} — {args.message}")

    print(json.dumps({
        "task_id": args.task_id,
        "intent": args.intent,
        "boundary": boundary,
        "reason": reason,
        "current_activity": current_activity(task),
        "immediate": immediate,
        "pending_action_id": action_id,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
