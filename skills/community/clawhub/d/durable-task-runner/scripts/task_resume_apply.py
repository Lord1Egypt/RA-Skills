#!/usr/bin/env python3
"""
Apply low-risk resume follow-through from task_resume_bootstrap plans.

Purpose:
- bridge bootstrap output into actual controller/state follow-through
- keep durable tasks moving after reporting their restart status
- stay intentionally narrow: only apply obvious, low-risk resume actions

Current scope:
- consumes the bootstrap helper JSON output (`--plan` recommended)
- updates task state/progress for resumable tasks
- records controller/resume events for low-risk follow-through
- does NOT try to execute arbitrary worker logic or invent new branching
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"


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


def pick_active_line(task: dict[str, Any]) -> str | None:
    for name, line in iter_lines(task):
        if line.get("status") == "assigned":
            return name
    return None


def pick_waiting_controller_line(task: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    for name, line in iter_lines(task):
        if line.get("status") in {"autopilot", "handoff"} and line.get("controller_decision", "pending") == "pending":
            return name, line
    return None


def apply_resume_flow(task: dict[str, Any], task_id: str, ts: str, action: str, applied: dict[str, Any]) -> dict[str, Any]:
    next_step = task.get("next_step", "")
    task["desired_state"] = "running"
    task["phase"] = task.get("phase", "resume-bootstrap")
    task["updated_at"] = ts
    active_line = pick_active_line(task)
    if action == "resume_active_line" and active_line:
        task["next_step"] = f"continue active line: {active_line}"
        applied["note"] = f"controller resumed active line {active_line}"
    else:
        task["next_step"] = next_step or "resume main execution"
        applied["note"] = "controller resumed main flow"
    save_task(task)
    append_event(task_id, {
        "ts": ts,
        "type": "resume_started",
        "task_id": task_id,
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {
            "action": action,
            "note": applied["note"],
        },
    })
    append_progress(task_id, f"resume apply: {applied['note']}")
    applied["applied"] = True
    return applied


def apply_controller_decision(task: dict[str, Any], task_id: str, ts: str, applied: dict[str, Any]) -> dict[str, Any]:
    picked = pick_waiting_controller_line(task)
    if not picked:
        applied["note"] = "no waiting controller line found"
        return applied
    name, line = picked
    next_role = line.get("next_role")
    if next_role in {None, "", "none", "main"}:
        applied["note"] = f"waiting line {name} is not low-risk auto-dispatchable"
        return applied

    line["controller_decision"] = "dispatch"
    line["controller_note"] = "auto-applied during resume bootstrap"
    line["status"] = "assigned"
    line["updated_at"] = ts
    task["desired_state"] = "running"
    task["updated_at"] = ts
    task["next_step"] = f"continue resumed line: {name}"
    save_task(task)
    append_event(task_id, {
        "ts": ts,
        "type": "controller_decision_recorded",
        "task_id": task_id,
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {
            "line": name,
            "decision": "dispatch",
            "note": "auto-applied during resume bootstrap",
            "next_role": line.get("next_role"),
            "status_value": line.get("status"),
        },
    })
    append_progress(task_id, f"resume apply: auto-dispatched resumed line {name}")
    applied["applied"] = True
    applied["note"] = f"auto-dispatched waiting line {name}"
    return applied


def apply_user_control(task: dict[str, Any], task_id: str, ts: str, applied: dict[str, Any]) -> dict[str, Any]:
    all_actions = list(task.get("pending_actions", []) or [])
    pending = [a for a in all_actions if isinstance(a, dict) and a.get("kind") == "user_control" and a.get("status") != "applied"]
    if not pending:
        applied["note"] = "no pending user control action found"
        return applied
    control = pending[-1]
    intent = control.get("intent")
    msg = control.get("message", "")
    if control.get("boundary") == "deferred":
        task["desired_state"] = "paused"
        task["operator_note"] = msg
        task["updated_at"] = ts
        control["status"] = "applied"
        control["applied_at"] = ts
        task["pending_actions"] = [a for a in all_actions if a is not control]
        task["reconcile"] = {"needed": False, "reason": "", "last_run_at": ts, "status": "clean"}
        save_task(task)
        append_event(task_id, {
            "ts": ts,
            "type": "pause_requested",
            "task_id": task_id,
            "phase": task.get("phase", ""),
            "status": "ok",
            "details": {"source": "pending_user_control", "intent": intent, "message": msg},
        })
        append_progress(task_id, f"resume apply: paused for pending user control ({intent})")
        applied["applied"] = True
        applied["note"] = f"paused for pending user control ({intent})"
        return applied
    if intent == "stop":
        task["desired_state"] = "stopped"
        task["operator_note"] = msg
    elif intent == "pause":
        task["desired_state"] = "paused"
        task["operator_note"] = msg
    elif intent == "resume":
        task["desired_state"] = "running"
        task["steering_note"] = msg
    else:
        task["steering_note"] = msg
    task["updated_at"] = ts
    control["status"] = "applied"
    control["applied_at"] = ts
    task["pending_actions"] = [a for a in all_actions if a is not control]
    remaining_pending = [a for a in task["pending_actions"] if isinstance(a, dict) and a.get("status") != "applied"]
    task["reconcile"] = {
        "needed": bool(remaining_pending),
        "reason": "pending_actions_remaining" if remaining_pending else "",
        "last_run_at": ts,
        "status": "pending" if remaining_pending else "clean",
    }
    save_task(task)
    append_event(task_id, {
        "ts": ts,
        "type": "user_control_applied",
        "task_id": task_id,
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {"intent": intent, "message": msg},
    })
    append_progress(task_id, f"resume apply: applied pending user control ({intent})")
    applied["applied"] = True
    applied["note"] = f"applied pending user control ({intent})"
    return applied


def apply_task(plan_item: dict[str, Any]) -> dict[str, Any]:
    task_id = plan_item["task_id"]
    task = load_task(task_id)
    ts = now_iso()
    action = plan_item.get("resume_plan", {}).get("action") or plan_item.get("recommendation", {}).get("action")
    applied = {
        "task_id": task_id,
        "action": action,
        "applied": False,
        "note": "",
    }

    if action == "ask_to_resume":
        applied["note"] = "resume requires explicit user confirmation"
        return applied

    if action in {"resume_active_line", "resume_main_flow"}:
        return apply_resume_flow(task, task_id, ts, action, applied)

    if action == "controller_decision_needed":
        return apply_controller_decision(task, task_id, ts, applied)

    if action == "user_control_pending":
        return apply_user_control(task, task_id, ts, applied)

    applied["note"] = "no low-risk auto-apply path for this action"
    return applied


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--file", help="bootstrap JSON file; defaults to stdin")
    args = p.parse_args()

    raw = Path(args.file).read_text() if args.file else __import__("sys").stdin.read()
    payload = json.loads(raw)
    tasks = payload.get("tasks", [])
    results = [apply_task(item) for item in tasks]
    print(json.dumps({"applied": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
