#!/usr/bin/env python3
"""
Automatic continuation helper for durable-task-runner.

Purpose:
- make desired_state=running mean active continuation, not just resumability
- keep logic narrow and inspectable: classify whether a task should keep running,
  pause for user control, or stop for real blockers/user-needed conditions
- emit compact JSON that higher-level runners can use without dragging tokens

Current scope:
- classify one task's continuation state
- apply low-risk next actions for pending user control via existing resume/apply plumbing
- pause tasks when real blocker / need_user conditions are present
- filter/repair stale ordinary running tasks that have no executable continuation hook
- leave worker-specific execution to later helpers instead of faking autonomy
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
STALE_IDLE_SECONDS = 300


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_ts(raw: str | None) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(raw.replace("Z", "+00:00"))


def age_seconds(raw: str | None) -> int | None:
    ts = parse_ts(raw)
    if ts is None:
        return None
    return max(0, round((datetime.now(timezone.utc) - ts).total_seconds()))


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


def has_subagent_lines(task: dict[str, Any]) -> bool:
    return any(isinstance(item, dict) and item.get("kind") == "subagent_lines" for item in task.get("artifacts", []))


def pending_user_controls(task: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        a for a in (task.get("pending_actions", []) or [])
        if isinstance(a, dict) and a.get("kind") == "user_control" and a.get("status") != "applied"
    ]


def blocker_lines(task: dict[str, Any]) -> list[str]:
    out = []
    for name, line in iter_lines(task):
        if line.get("status") in {"blocked", "need_user"}:
            out.append(name)
    return out


def active_lines(task: dict[str, Any]) -> list[str]:
    out = []
    for name, line in iter_lines(task):
        if line.get("status") == "assigned":
            out.append(name)
    return out


def attention_lines(task: dict[str, Any]) -> list[str]:
    out = []
    for name, line in iter_lines(task):
        if line.get("status") in {"autopilot", "handoff"} and line.get("controller_decision", "pending") == "pending":
            out.append(name)
    return out


def run_json(*args: str, input_text: str | None = None) -> dict[str, Any]:
    proc = subprocess.run(list(args), text=True, input=input_text, capture_output=True, check=True)
    raw = (proc.stdout or "").strip()
    if not raw:
        return {}
    return json.loads(raw)


def pause_task(task: dict[str, Any], reason: str, note: str) -> dict[str, Any]:
    ts = now_iso()
    task["desired_state"] = "paused"
    task["operator_note"] = note
    task["updated_at"] = ts
    save_task(task)
    append_event(task["task_id"], {
        "ts": ts,
        "type": "pause_requested",
        "task_id": task["task_id"],
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {"reason": reason, "note": note, "source": "task_auto_continue.py"},
    })
    append_progress(task["task_id"], f"auto-continue paused: {reason} — {note}")
    return {"status": "paused", "reason": reason, "note": note}


def mark_stale_idle(task: dict[str, Any]) -> dict[str, Any]:
    task_id = task["task_id"]
    idle_age = age_seconds(task.get("last_status_update_at"))
    note = (
        "ordinary running task has no subagent lines or executable continuation hook; "
        "marking as paused-stale so the scheduler stops pretending it is actively progressing"
    )
    if idle_age is not None:
        note += f" (last status {idle_age}s ago)"
    paused = pause_task(task, "stale_idle_running", note)
    append_event(task_id, {
        "ts": now_iso(),
        "type": "continuation_probe",
        "task_id": task_id,
        "phase": task.get("phase", ""),
        "status": "stale",
        "details": {
            "reason": "ordinary_running_task_without_hook",
            "idle_age_seconds": idle_age,
        },
    })
    return {"task_id": task_id, **paused, "idle_age_seconds": idle_age}


def continue_task(task_id: str) -> dict[str, Any]:
    task = load_task(task_id)
    if task.get("desired_state") != "running":
        return {"task_id": task_id, "status": "skipped", "reason": "not_running"}

    pending_user = pending_user_controls(task)
    if pending_user:
        bootstrap = run_json("python3", str(SCRIPT_DIR / "task_resume_bootstrap.py"), "--task-id", task_id, "--plan")
        apply = run_json("python3", str(SCRIPT_DIR / "task_resume_apply.py"), input_text=json.dumps(bootstrap))
        return {
            "task_id": task_id,
            "status": "applied_user_control",
            "reason": "pending_user_control",
            "apply": apply.get("applied", []),
        }

    if not has_subagent_lines(task):
        idle_age = age_seconds(task.get("updated_at")) or age_seconds(task.get("last_status_update_at")) or 0
        if idle_age >= STALE_IDLE_SECONDS:
            return mark_stale_idle(task)
        append_progress(task_id, f"auto-continue standby: ordinary running task without subagent lines ({idle_age}s since update); awaiting explicit continuation hook")
        append_event(task_id, {
            "ts": now_iso(),
            "type": "continuation_probe",
            "task_id": task_id,
            "phase": task.get("phase", ""),
            "status": "standby",
            "details": {"reason": "ordinary_running_task_without_hook", "idle_age_seconds": idle_age},
        })
        return {
            "task_id": task_id,
            "status": "standby",
            "reason": "ordinary_running_task_without_hook",
            "idle_age_seconds": idle_age,
        }

    blocked = blocker_lines(task)
    if blocked:
        note = f"blocked line(s): {', '.join(blocked)}"
        paused = pause_task(task, "blocked_or_need_user", note)
        return {"task_id": task_id, **paused}

    attention = attention_lines(task)
    if attention:
        bootstrap = run_json("python3", str(SCRIPT_DIR / "task_resume_bootstrap.py"), "--task-id", task_id, "--plan")
        apply = run_json("python3", str(SCRIPT_DIR / "task_resume_apply.py"), input_text=json.dumps(bootstrap))
        return {
            "task_id": task_id,
            "status": "controller_followthrough",
            "reason": "attention_lines",
            "lines": attention,
            "apply": apply.get("applied", []),
        }

    active = active_lines(task)
    if active:
        append_progress(task_id, f"auto-continue heartbeat: active line(s) still running ({', '.join(active)})")
        return {
            "task_id": task_id,
            "status": "running",
            "reason": "active_lines_present",
            "lines": active,
        }

    return mark_stale_idle(task)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    args = p.parse_args()
    print(json.dumps(continue_task(args.task_id), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
