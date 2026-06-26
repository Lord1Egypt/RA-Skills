#!/usr/bin/env python3
"""
Resume / restart bootstrap helper for durable-task-runner.

Purpose:
- inspect durable tasks after reset/restart/startup
- classify which tasks are resumable, paused, stopped, completed, or need attention
- run reconcile checks when configured and useful
- emit a compact operator-facing summary with concrete resume recommendations
- optionally emit a controller-ready resume plan

Design bias:
- explicit, inspectable, low-magic
- prefer clear state classification over ambitious automation theater
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
CONFIG_PATH = ROOT / "config" / "defaults.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def load_defaults() -> dict[str, Any]:
    return load_json(CONFIG_PATH, {}) or {}


def iter_tasks() -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(STATE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue
        if isinstance(data, dict) and data.get("task_id"):
            rows.append((path, data))
    return rows


def append_event(task_id: str, payload: dict[str, Any]) -> None:
    path = STATE_DIR / f"{task_id}.events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def append_progress(task_id: str, line: str) -> None:
    path = STATE_DIR / f"{task_id}.progress.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")


def classify_task(task: dict[str, Any]) -> tuple[str, list[str], dict[str, int]]:
    reasons: list[str] = []
    desired_state = task.get("desired_state")
    reconcile = task.get("reconcile", {}) or {}
    artifacts = task.get("artifacts", []) or []

    counts = {
        "attention_lines": 0,
        "dropped_lines": 0,
        "resolved_lines": 0,
        "active_lines": 0,
    }
    for item in artifacts:
        if not isinstance(item, dict) or item.get("kind") != "subagent_lines":
            continue
        for _name, line in (item.get("lines", {}) or {}).items():
            status = line.get("status")
            next_role = line.get("next_role")
            controller_decision = line.get("controller_decision", "pending")
            if status in {"done", "idle", "blocked", "need_user"}:
                counts["resolved_lines"] += 1
            elif status == "assigned":
                counts["active_lines"] += 1
            if status in {"autopilot", "handoff"} and controller_decision == "pending":
                counts["attention_lines"] += 1
            if status in {"autopilot", "handoff"} and next_role in {None, "", "none"}:
                counts["dropped_lines"] += 1

    if desired_state == "paused":
        reasons.append("desired_state=paused")
        return "paused", reasons, counts
    if desired_state == "stopped":
        reasons.append("desired_state=stopped")
        return "stopped", reasons, counts
    if desired_state == "completed":
        reasons.append("desired_state=completed")
        return "completed", reasons, counts
    if desired_state == "failed":
        reasons.append("desired_state=failed")
        return "failed", reasons, counts
    if counts["dropped_lines"]:
        reasons.append(f"{counts['dropped_lines']} dropped orchestration line(s)")
        return "needs_attention", reasons, counts
    pending_user = [a for a in (task.get("pending_actions", []) or []) if isinstance(a, dict) and a.get("kind") == "user_control" and a.get("status") != "applied"]
    if pending_user:
        reasons.append(f"{len(pending_user)} pending user control action(s)")
        return "needs_attention", reasons, counts
    if reconcile.get("needed"):
        reasons.append("reconcile still needed")
        return "needs_attention", reasons, counts
    if counts["attention_lines"]:
        reasons.append(f"{counts['attention_lines']} orchestration line(s) awaiting controller action")
        return "needs_attention", reasons, counts
    if desired_state == "running":
        reasons.append("desired_state=running")
        return "resumable", reasons, counts
    reasons.append(f"unrecognized desired_state={desired_state}")
    return "needs_attention", reasons, counts


def recommend_action(task: dict[str, Any], classification: str, reasons: list[str], counts: dict[str, int]) -> dict[str, Any]:
    defaults = load_defaults()
    control_cfg = defaults.get("control", {}) or {}
    next_step = task.get("next_step", "") or "n/a"
    if classification == "resumable":
        if control_cfg.get("ask_before_resuming_after_reset", True):
            return {
                "action": "ask_to_resume",
                "summary": f"Ask whether to resume this task after reset/interruption; next step if resumed: {next_step}",
                "prompt": f"I found an interrupted durable task: {task.get('title', task.get('task_id'))}. Do you want me to continue it from the last safe step?",
            }
        if counts["active_lines"] > 0:
            return {
                "action": "resume_active_line",
                "summary": f"Resume the task and continue the active line(s); next step: {next_step}",
            }
        return {
            "action": "resume_main_flow",
            "summary": f"Resume the main task flow; next step: {next_step}",
        }
    if classification == "needs_attention":
        if counts["dropped_lines"] > 0:
            return {
                "action": "repair_orchestration_line",
                "summary": "Repair dropped orchestration line metadata before resuming execution.",
            }
        pending_user = [a for a in (task.get("pending_actions", []) or []) if isinstance(a, dict) and a.get("kind") == "user_control" and a.get("status") != "applied"]
        if pending_user:
            return {
                "action": "user_control_pending",
                "summary": "Apply or acknowledge the pending user control request before resuming execution.",
            }
        if counts["attention_lines"] > 0:
            return {
                "action": "controller_decision_needed",
                "summary": "Record an explicit controller decision for waiting autopilot/handoff line(s), then resume.",
            }
        return {
            "action": "reconcile_first",
            "summary": "Resolve reconcile/pending-action issues before resuming execution.",
        }
    if classification == "paused":
        return {
            "action": "stay_paused",
            "summary": "Task is intentionally paused; resume only if desired_state changes back to running.",
        }
    if classification == "stopped":
        return {
            "action": "stay_stopped",
            "summary": "Task is intentionally stopped; do not resume without an explicit new start decision.",
        }
    if classification == "completed":
        return {
            "action": "none",
            "summary": "Task is complete; no resume action needed.",
        }
    if classification == "failed":
        return {
            "action": "manual_recovery",
            "summary": "Task is failed; inspect failure details and create a recovery plan before resuming.",
        }
    return {
        "action": "manual_review",
        "summary": f"Manual review needed: {'; '.join(reasons) if reasons else 'unclear state'}",
    }


def build_resume_plan(task: dict[str, Any], classification: str, recommendation: dict[str, Any], counts: dict[str, int]) -> dict[str, Any]:
    next_step = task.get("next_step", "") or "n/a"
    plan = {
        "task_id": task["task_id"],
        "classification": classification,
        "action": recommendation["action"],
        "next_step": next_step,
        "steps": [],
    }
    if recommendation["action"] == "ask_to_resume":
        plan["steps"] = [
            "load_task_snapshot",
            "summarize_last_safe_step",
            "ask_user_whether_to_continue",
        ]
        plan["resume_prompt"] = recommendation.get("prompt", "Do you want me to continue this durable task?")
    elif recommendation["action"] == "resume_active_line":
        plan["steps"] = [
            "load_task_snapshot",
            "confirm_reconcile_clean",
            "select_active_line",
            "continue_controller_flow",
        ]
    elif recommendation["action"] == "resume_main_flow":
        plan["steps"] = [
            "load_task_snapshot",
            "confirm_reconcile_clean",
            "resume_main_execution",
        ]
    elif recommendation["action"] == "controller_decision_needed":
        plan["steps"] = [
            "load_task_snapshot",
            "inspect_waiting_lines",
            "record_controller_decision",
            "resume_controller_flow",
        ]
    elif recommendation["action"] == "user_control_pending":
        plan["steps"] = [
            "load_task_snapshot",
            "acknowledge_user_control",
            "apply_or_pause_for_user_control",
        ]
    elif recommendation["action"] == "repair_orchestration_line":
        plan["steps"] = [
            "load_task_snapshot",
            "repair_line_metadata",
            "re-run_bootstrap_scan",
        ]
    elif recommendation["action"] == "reconcile_first":
        plan["steps"] = [
            "load_task_snapshot",
            "resolve_pending_actions",
            "re-run_reconcile",
            "resume_if_clean",
        ]
    else:
        plan["steps"] = ["manual_review"]
    plan["line_counts"] = counts
    return plan


def run_reconcile(task_id: str, reason: str) -> dict[str, Any]:
    cmd = ["python3", str(SCRIPT_DIR / "task_reconcile.py"), task_id, "--reason", reason]
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def inspect_task(path: Path, task: dict[str, Any], run_reconcile_checks: bool, include_plan: bool) -> dict[str, Any]:
    ts = now_iso()
    task_id = task["task_id"]
    reconcile_result = None
    if run_reconcile_checks and task.get("desired_state") == "running":
        reconcile_result = run_reconcile(task_id, "resume_bootstrap_scan")
        task = load_json(path, task)

    classification, reasons, counts = classify_task(task)
    recommendation = recommend_action(task, classification, reasons, counts)
    summary = {
        "task_id": task_id,
        "title": task.get("title", task_id),
        "phase": task.get("phase", ""),
        "health": task.get("health", ""),
        "desired_state": task.get("desired_state"),
        "next_step": task.get("next_step", ""),
        "classification": classification,
        "reasons": reasons,
        "line_counts": counts,
        "recommendation": recommendation,
    }
    if include_plan:
        summary["resume_plan"] = build_resume_plan(task, classification, recommendation, counts)
    if reconcile_result is not None:
        summary["reconcile"] = reconcile_result.get("reconcile", reconcile_result)

    append_event(task_id, {
        "ts": ts,
        "type": "task_reset_detected",
        "task_id": task_id,
        "phase": task.get("phase", ""),
        "status": classification,
        "details": {
            "reasons": reasons,
            "next_step": task.get("next_step", ""),
            "recommendation": recommendation,
            "line_counts": counts,
        },
    })
    append_progress(task_id, f"resume bootstrap scan: {classification} — {recommendation['action']} — {'; '.join(reasons)}")
    return summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--task-id")
    p.add_argument("--no-reconcile", action="store_true")
    p.add_argument("--plan", action="store_true")
    args = p.parse_args()

    targets = iter_tasks()
    if args.task_id:
        targets = [(path, task) for path, task in targets if task.get("task_id") == args.task_id]
        if not targets:
            raise SystemExit(f"task not found: {args.task_id}")

    summaries = [inspect_task(path, task, run_reconcile_checks=not args.no_reconcile, include_plan=args.plan) for path, task in targets]
    buckets = {
        "resumable": [],
        "needs_attention": [],
        "paused": [],
        "stopped": [],
        "completed": [],
        "failed": [],
    }
    for item in summaries:
        buckets.setdefault(item["classification"], []).append(item)

    print(json.dumps({
        "scanned_at": now_iso(),
        "count": len(summaries),
        "summary": {k: len(v) for k, v in buckets.items()},
        "tasks": summaries,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
