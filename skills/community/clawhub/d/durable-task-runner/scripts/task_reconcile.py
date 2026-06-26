#!/usr/bin/env python3
"""
Task reconcile helper for durable-task-runner.

Attribution note:
- This script is original here, but it is conceptually influenced by ClawHub
  `restart-safe-workflow`, especially its explicit reconcile step, action-state tracking,
  and idempotency-ledger thinking.
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


def load_snapshot(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def save_snapshot(task_id: str, data: dict[str, Any]) -> None:
    path = STATE_DIR / f"{task_id}.json"
    path.write_text(json.dumps(data, indent=2) + "\n")


def append_event(task_id: str, payload: dict[str, Any]) -> None:
    path = STATE_DIR / f"{task_id}.events.jsonl"
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("task_id")
    p.add_argument("--reason", default="resume_consistency_check")
    args = p.parse_args()

    data = load_snapshot(args.task_id)
    ts = now_iso()
    pending = data.get("pending_actions", [])
    action_states = data.get("action_states", {})
    idempotency = data.get("idempotency_ledger", {})

    findings: list[dict[str, Any]] = []
    cleaned_pending: list[dict[str, Any]] = []

    for action in pending:
        action_id = action.get("id") or action.get("action_id") or "unknown"
        idem = action.get("idempotency_key") or action_id
        state = action_states.get(action_id, {})
        if action.get("kind") == "user_control":
            if action.get("status") == "applied":
                findings.append({"action_id": action_id, "result": "user_control_already_applied"})
                continue
            cleaned_pending.append(action)
            findings.append({"action_id": action_id, "result": "user_control_pending"})
            continue
        if idem in idempotency:
            findings.append({"action_id": action_id, "result": "already_applied_via_idempotency_ledger"})
            if state:
                state["status"] = "success"
                state["reconciled_at"] = ts
                action_states[action_id] = state
            continue
        if state.get("status") == "success":
            findings.append({"action_id": action_id, "result": "already_marked_success"})
            continue
        cleaned_pending.append(action)
        findings.append({"action_id": action_id, "result": "still_pending"})

    data["pending_actions"] = cleaned_pending
    data["action_states"] = action_states
    data["reconcile"] = {
        "needed": len(cleaned_pending) > 0,
        "reason": args.reason,
        "last_run_at": ts,
        "status": "pending_actions_remain" if cleaned_pending else "clean",
    }
    data["updated_at"] = ts
    save_snapshot(args.task_id, data)
    append_event(args.task_id, {
        "ts": ts,
        "type": "resume_consistency_check_passed" if not cleaned_pending else "resume_consistency_check_failed",
        "task_id": args.task_id,
        "phase": data.get("phase", ""),
        "status": data["reconcile"]["status"],
        "details": {"reason": args.reason, "findings": findings},
    })
    print(json.dumps({
        "task_id": args.task_id,
        "pending_actions_remaining": len(cleaned_pending),
        "reconcile": data["reconcile"],
        "findings": findings,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
