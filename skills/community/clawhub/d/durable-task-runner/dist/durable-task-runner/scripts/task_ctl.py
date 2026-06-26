#!/usr/bin/env python3
"""
Durable task controller for OpenClaw.

Attribution note:
- This script is original to this repo.
- It was conceptually influenced by ClawHub `task-resume` (small helper-script approach
  for durable recovery state) and `restart-safe-workflow` (explicit task state / event
  discipline), but it does not directly embed large copied code blocks from those packages.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
CONFIG_PATH = ROOT / "config" / "defaults.json"
SCRIPT_DIR = ROOT / "scripts"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def task_paths(task_id: str) -> dict[str, Path]:
    return {
        "snapshot": STATE_DIR / f"{task_id}.json",
        "events": STATE_DIR / f"{task_id}.events.jsonl",
        "progress": STATE_DIR / f"{task_id}.progress.log",
    }


def load_snapshot(task_id: str) -> dict[str, Any]:
    path = task_paths(task_id)["snapshot"]
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def write_snapshot(data: dict[str, Any]) -> None:
    path = task_paths(data["task_id"])["snapshot"]
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n")


def append_event(task_id: str, event: dict[str, Any]) -> None:
    path = task_paths(task_id)["events"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=False) + "\n")


def append_progress(task_id: str, line: str) -> None:
    path = task_paths(task_id)["progress"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")


def parse_json_arg(raw: str | None, default: Any) -> Any:
    if raw is None:
        return default
    return json.loads(raw)


def has_delivery_binding(task: dict[str, Any]) -> bool:
    for item in task.get("artifacts", []):
        if isinstance(item, dict) and item.get("kind") == "delivery_binding":
            return True
    return False


def infer_delivery_binding() -> dict[str, Any] | None:
    channel = os.environ.get("OPENCLAW_CHANNEL") or os.environ.get("CHANNEL")
    account_id = os.environ.get("OPENCLAW_ACCOUNT_ID") or os.environ.get("ACCOUNT_ID") or "default"
    target = os.environ.get("OPENCLAW_CHAT_ID") or os.environ.get("CHAT_ID") or os.environ.get("OPENCLAW_TARGET")
    if not channel or not target:
        return None
    surface = os.environ.get("OPENCLAW_SURFACE") or "active-chat"
    return {
        "kind": "delivery_binding",
        "channel": channel,
        "account_id": account_id,
        "target": target,
        "surface": surface,
        "note": "auto-bound from active OpenClaw chat/session context",
    }


def maybe_add_delivery_binding(task: dict[str, Any]) -> bool:
    if has_delivery_binding(task):
        return False
    binding = infer_delivery_binding()
    if not binding:
        return False
    task.setdefault("artifacts", []).append(binding)
    return True


def maybe_send_now(task_id: str, event_type: str, force: bool = False) -> None:
    task = load_snapshot(task_id)
    if not has_delivery_binding(task):
        return
    cmd = ["python3", str(SCRIPT_DIR / "task_maybe_send_now.py"), task_id, event_type]
    if force:
        cmd.append("--force")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def milestone_changed(before: dict[str, Any], after: dict[str, Any]) -> bool:
    return json.dumps(before.get("milestones", []), sort_keys=True) != json.dumps(after.get("milestones", []), sort_keys=True)


def phase_changed(before: dict[str, Any], after: dict[str, Any]) -> bool:
    return before.get("phase") != after.get("phase")


def cmd_create(args: argparse.Namespace) -> int:
    ensure_dirs()
    paths = task_paths(args.task_id)
    if paths["snapshot"].exists() and not args.force:
        raise SystemExit(f"task already exists: {args.task_id} (use --force to overwrite)")

    ts = now_iso()
    data = {
        "task_id": args.task_id,
        "title": args.title,
        "goal": args.goal,
        "done_criteria": parse_json_arg(args.done_criteria, []),
        "constraints": parse_json_arg(args.constraints, []),
        "desired_state": args.desired_state,
        "execution_priority": args.execution_priority,
        "phase": args.phase,
        "health": args.health,
        "created_at": ts,
        "updated_at": ts,
        "status_update_interval_seconds": args.status_interval,
        "last_status_update_at": None,
        "last_verified_step": "",
        "next_step": args.next_step or "",
        "operator_note": "",
        "steering_note": "",
        "milestones": parse_json_arg(args.milestones, []),
        "subtasks": parse_json_arg(args.subtasks, []),
        "artifacts": parse_json_arg(args.artifacts, []),
        "risk_notes": parse_json_arg(args.risk_notes, []),
        "pending_actions": parse_json_arg(args.pending_actions, []),
        "action_states": parse_json_arg(args.action_states, {}),
        "idempotency_ledger": parse_json_arg(args.idempotency_ledger, {}),
        "reconcile": parse_json_arg(args.reconcile, {"needed": False, "reason": "", "last_run_at": None, "status": "idle"}),
    }
    auto_bound = maybe_add_delivery_binding(data)
    write_snapshot(data)
    append_event(args.task_id, {
        "ts": ts,
        "type": "task_created",
        "task_id": args.task_id,
        "phase": args.phase,
        "status": "ok",
        "details": {"title": args.title, "goal": args.goal, "auto_bound_delivery": auto_bound},
    })
    append_progress(args.task_id, f"task created: {args.title}")
    print(json.dumps(data, indent=2))
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    data = load_snapshot(args.task_id)
    print(json.dumps(data, indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    ensure_dirs()
    rows = []
    for path in sorted(STATE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        rows.append({
            "task_id": data.get("task_id"),
            "title": data.get("title"),
            "desired_state": data.get("desired_state"),
            "phase": data.get("phase"),
            "health": data.get("health"),
            "next_step": data.get("next_step"),
            "updated_at": data.get("updated_at"),
        })
    print(json.dumps(rows, indent=2))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    data = load_snapshot(args.task_id)
    before = deepcopy(data)
    for field in [
        "title", "goal", "desired_state", "execution_priority", "phase", "health",
        "next_step", "operator_note", "steering_note", "last_verified_step"
    ]:
        val = getattr(args, field)
        if val is not None:
            data[field] = val
    for field in ["done_criteria", "constraints", "milestones", "subtasks", "artifacts", "risk_notes", "pending_actions", "action_states", "idempotency_ledger", "reconcile"]:
        raw = getattr(args, field)
        if raw is not None:
            data[field] = json.loads(raw)
    if args.status_interval is not None:
        data["status_update_interval_seconds"] = args.status_interval
    data["updated_at"] = now_iso()
    write_snapshot(data)
    append_event(args.task_id, {
        "ts": data["updated_at"],
        "type": "task_updated",
        "task_id": args.task_id,
        "phase": data.get("phase", ""),
        "status": "ok",
        "details": {"before": before, "after": data},
    })
    if args.progress_note:
        append_progress(args.task_id, args.progress_note)

    if args.report_kind != "internal":
        if data.get("desired_state") == "completed":
            maybe_send_now(args.task_id, "completion")
        elif phase_changed(before, data):
            maybe_send_now(args.task_id, "phase")
        elif milestone_changed(before, data):
            maybe_send_now(args.task_id, "milestone")

    print(json.dumps(data, indent=2))
    return 0


def cmd_event(args: argparse.Namespace) -> int:
    snapshot = load_snapshot(args.task_id)
    phase = args.phase or snapshot.get("phase", "")
    event = {
        "ts": now_iso(),
        "type": args.type,
        "task_id": args.task_id,
        "phase": phase,
        "status": args.status,
        "details": parse_json_arg(args.details, {}),
    }
    append_event(args.task_id, event)
    if args.progress_note:
        append_progress(args.task_id, args.progress_note)

    if args.report_kind != "internal":
        kind_map = {
            "verification_passed": "milestone",
            "verification_failed": "blocker",
            "milestone_completed": "milestone",
            "pause_requested": "control",
            "resume_started": "resume",
            "stop_requested": "control",
            "task_completed": "completion",
            "task_failed": "blocker",
        }
        report_type = kind_map.get(args.type)
        if report_type:
            maybe_send_now(args.task_id, report_type)

    print(json.dumps(event, indent=2))
    return 0


def cmd_progress(args: argparse.Namespace) -> int:
    data = load_snapshot(args.task_id)
    ts = now_iso()
    data["last_status_update_at"] = ts
    data["updated_at"] = ts
    if args.phase:
        data["phase"] = args.phase
    if args.health:
        data["health"] = args.health
    if args.next_step:
        data["next_step"] = args.next_step
    write_snapshot(data)
    append_progress(args.task_id, args.message)
    append_event(args.task_id, {
        "ts": ts,
        "type": "status_reported",
        "task_id": args.task_id,
        "phase": data.get("phase", ""),
        "status": data.get("health", "healthy"),
        "details": {
            "message": args.message,
            "next_step": data.get("next_step", ""),
            "report_kind": args.report_kind,
        },
    })
    print(json.dumps({"task_id": args.task_id, "status": "ok", "message": args.message}, indent=2))
    return 0


def cmd_control(args: argparse.Namespace) -> int:
    data = load_snapshot(args.task_id)
    ts = now_iso()
    desired = args.desired_state
    data["desired_state"] = desired
    if args.note:
        if desired == "paused":
            data["operator_note"] = args.note
        else:
            data["steering_note"] = args.note
    data["updated_at"] = ts
    write_snapshot(data)
    event_type = {
        "paused": "pause_requested",
        "running": "resume_started",
        "stopped": "stop_requested",
    }.get(desired, "steer_received")
    append_event(args.task_id, {
        "ts": ts,
        "type": event_type,
        "task_id": args.task_id,
        "phase": data.get("phase", ""),
        "status": "ok",
        "details": {"desired_state": desired, "note": args.note or ""},
    })
    if args.note:
        append_progress(args.task_id, f"control update: {desired} — {args.note}")
    else:
        append_progress(args.task_id, f"control update: {desired}")
    if args.report_kind != "internal":
        maybe_send_now(args.task_id, "control")
    print(json.dumps(data, indent=2))
    return 0


def cmd_recent(args: argparse.Namespace) -> int:
    load_snapshot(args.task_id)
    path = task_paths(args.task_id)["events"]
    if not path.exists():
        print("[]")
        return 0
    lines = path.read_text().splitlines()
    selected = [json.loads(line) for line in lines[-args.limit:]]
    print(json.dumps(selected, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Durable task controller")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("create")
    c.add_argument("task_id")
    c.add_argument("--title", required=True)
    c.add_argument("--goal", required=True)
    c.add_argument("--done-criteria")
    c.add_argument("--constraints")
    c.add_argument("--desired-state", default="running")
    c.add_argument("--execution-priority", choices=["time", "tokens"], default="tokens")
    c.add_argument("--phase", default="planning")
    c.add_argument("--health", default="healthy")
    c.add_argument("--next-step")
    c.add_argument("--status-interval", type=int, default=300)
    c.add_argument("--milestones")
    c.add_argument("--subtasks")
    c.add_argument("--artifacts")
    c.add_argument("--risk-notes")
    c.add_argument("--pending-actions")
    c.add_argument("--action-states")
    c.add_argument("--idempotency-ledger")
    c.add_argument("--reconcile")
    c.add_argument("--force", action="store_true")
    c.set_defaults(func=cmd_create)

    s = sub.add_parser("show")
    s.add_argument("task_id")
    s.set_defaults(func=cmd_show)

    l = sub.add_parser("list")
    l.set_defaults(func=cmd_list)

    u = sub.add_parser("update")
    u.add_argument("task_id")
    for field in ["title", "goal", "desired_state", "execution_priority", "phase", "health",
                  "next_step", "operator_note", "steering_note", "last_verified_step",
                  "done_criteria", "constraints", "milestones", "subtasks", "artifacts", "risk_notes",
                  "pending_actions", "action_states", "idempotency_ledger", "reconcile"]:
        u.add_argument(f"--{field.replace('_','-')}")
    u.add_argument("--status-interval", type=int)
    u.add_argument("--progress-note")
    u.add_argument("--report-kind", choices=["normal", "internal"], default="normal")
    u.set_defaults(func=cmd_update)

    e = sub.add_parser("event")
    e.add_argument("task_id")
    e.add_argument("type")
    e.add_argument("--phase")
    e.add_argument("--status", default="ok")
    e.add_argument("--details")
    e.add_argument("--progress-note")
    e.add_argument("--report-kind", choices=["normal", "internal"], default="normal")
    e.set_defaults(func=cmd_event)

    pr = sub.add_parser("progress")
    pr.add_argument("task_id")
    pr.add_argument("message")
    pr.add_argument("--phase")
    pr.add_argument("--health")
    pr.add_argument("--next-step")
    pr.add_argument("--report-kind", choices=["normal", "internal"], default="normal")
    pr.set_defaults(func=cmd_progress)

    ctl = sub.add_parser("control")
    ctl.add_argument("task_id")
    ctl.add_argument("desired_state", choices=["running", "paused", "stopped"])
    ctl.add_argument("--note")
    ctl.add_argument("--report-kind", choices=["normal", "internal"], default="normal")
    ctl.set_defaults(func=cmd_control)

    r = sub.add_parser("recent")
    r.add_argument("task_id")
    r.add_argument("--limit", type=int, default=20)
    r.set_defaults(func=cmd_recent)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
