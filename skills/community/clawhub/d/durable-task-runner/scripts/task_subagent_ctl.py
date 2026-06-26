#!/usr/bin/env python3
"""
Subagent/controller helper for durable-task-runner.

Attribution note:
- Original to this repo, but influenced by ClawHub `subagent-orchestrator`
  for controller/worker separation, structured return headers, and anti-drop checks.
- This implementation intentionally keeps the first cut narrow: assign lines,
  generate worker briefs, ingest worker returns, detect dropped lines, and let
  the controller explicitly resolve the next state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
ALLOWED_TAGS = {"autopilot", "done", "idle", "blocked", "handoff", "need_user"}
ALLOWED_GOAL_STATUS = {"partial", "complete", "waiting", "blocked"}
ALLOWED_NEXT_ROLES = {"main", "verify", "research", "worker", "user", "none"}
RESOLVED_STATUSES = {"done", "idle", "blocked", "need_user"}
REQUIRED_HEADERS = ["tag", "task_id", "line", "node", "goal_status", "next_role"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def task_path(task_id: str) -> Path:
    return STATE_DIR / f"{task_id}.json"


def events_path(task_id: str) -> Path:
    return STATE_DIR / f"{task_id}.events.jsonl"


def progress_path(task_id: str) -> Path:
    return STATE_DIR / f"{task_id}.progress.log"


def load_task(task_id: str) -> dict[str, Any]:
    path = task_path(task_id)
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def write_task(task: dict[str, Any]) -> None:
    task_path(task["task_id"]).write_text(json.dumps(task, indent=2) + "\n")


def append_event(task_id: str, event: dict[str, Any]) -> None:
    p = events_path(task_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def append_progress(task_id: str, line: str) -> None:
    p = progress_path(task_id)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {line}\n")


def ensure_orchestration_artifact(task: dict[str, Any]) -> dict[str, Any]:
    artifacts = task.setdefault("artifacts", [])
    for item in artifacts:
        if isinstance(item, dict) and item.get("kind") == "subagent_lines":
            item.setdefault("lines", {})
            return item
    artifact = {"kind": "subagent_lines", "lines": {}}
    artifacts.append(artifact)
    return artifact


def parse_header_block(text: str) -> tuple[dict[str, str], str]:
    headers: dict[str, str] = {}
    body_lines: list[str] = []
    in_headers = True
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if in_headers and not line.strip():
            in_headers = False
            continue
        if in_headers:
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
            if m:
                headers[m.group(1).strip()] = m.group(2).strip()
                continue
            in_headers = False
        body_lines.append(line)
    return headers, "\n".join(body_lines).strip()


def line_record(line: dict[str, Any], name: str) -> dict[str, Any]:
    return {
        "line": name,
        "status": line.get("status"),
        "goal_status": line.get("goal_status"),
        "next_role": line.get("next_role"),
        "node": line.get("node"),
        "owner": line.get("owner"),
        "controller_decision": line.get("controller_decision", "pending"),
        "last_return_tag": line.get("last_return_tag"),
        "last_return_at": line.get("last_return_at"),
    }


def classify_line(line: dict[str, Any]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    status = line.get("status")
    goal_status = line.get("goal_status")
    next_role = line.get("next_role")
    controller_decision = line.get("controller_decision", "pending")

    if status not in ALLOWED_TAGS and status != "assigned":
        reasons.append(f"unknown status: {status}")
    if goal_status and goal_status not in ALLOWED_GOAL_STATUS:
        reasons.append(f"invalid goal_status: {goal_status}")
    if next_role and next_role not in ALLOWED_NEXT_ROLES:
        reasons.append(f"invalid next_role: {next_role}")

    if status == "assigned":
        return "active", reasons

    if status == "autopilot":
        if next_role in {None, "", "none"}:
            reasons.append("autopilot line missing actionable next_role")
            return "dropped", reasons
        if controller_decision == "pending":
            reasons.append("autopilot line awaiting controller follow-through")
            return "attention", reasons
        return "active", reasons

    if status == "handoff":
        if next_role in {None, "", "none"}:
            reasons.append("handoff line missing next_role")
            return "dropped", reasons
        if controller_decision == "pending":
            reasons.append("handoff line awaiting controller resolution")
            return "attention", reasons
        return "active", reasons

    if status in RESOLVED_STATUSES:
        return "resolved", reasons

    return "attention", reasons


def validate_return(task_id: str, text: str) -> dict[str, Any]:
    headers, body = parse_header_block(text)
    missing = [k for k in REQUIRED_HEADERS if not headers.get(k)]
    if missing:
        raise SystemExit(f"missing required headers: {', '.join(missing)}")
    if headers["task_id"] != task_id:
        raise SystemExit(f"task_id mismatch: expected {task_id}, got {headers['task_id']}")
    if headers["tag"] not in ALLOWED_TAGS:
        raise SystemExit(f"invalid tag: {headers['tag']}")
    if headers["goal_status"] not in ALLOWED_GOAL_STATUS:
        raise SystemExit(f"invalid goal_status: {headers['goal_status']}")
    if headers["next_role"] not in ALLOWED_NEXT_ROLES:
        raise SystemExit(f"invalid next_role: {headers['next_role']}")
    return {"headers": headers, "body": body}


def cmd_assign(args: argparse.Namespace) -> int:
    task = load_task(args.task_id)
    artifact = ensure_orchestration_artifact(task)
    lines = artifact["lines"]
    ts = now_iso()
    line = lines.get(args.line, {})
    line.update({
        "line": args.line,
        "goal": args.goal,
        "owner": args.owner,
        "node": args.node,
        "status": "assigned",
        "goal_status": "partial",
        "next_role": args.owner,
        "assigned_at": ts,
        "updated_at": ts,
        "last_return_tag": None,
        "last_return_at": None,
        "summary": args.summary or "",
        "artifacts": [],
        "controller_decision": "pending",
        "controller_note": "",
    })
    lines[args.line] = line
    task["updated_at"] = ts
    write_task(task)
    append_event(args.task_id, {
        "ts": ts,
        "type": "subtask_assigned",
        "task_id": args.task_id,
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {
            "line": args.line,
            "owner": args.owner,
            "node": args.node,
            "goal": args.goal,
            "summary": args.summary or "",
        },
    })
    append_progress(args.task_id, f"assigned line {args.line} to {args.owner} at node {args.node}")
    print(json.dumps(line, indent=2))
    return 0


def cmd_prompt(args: argparse.Namespace) -> int:
    task = load_task(args.task_id)
    artifact = ensure_orchestration_artifact(task)
    line = artifact["lines"].get(args.line)
    if not line:
        raise SystemExit(f"line not found: {args.line}")
    text = f"""You are a worker for durable-task-runner.

Return using exactly these headers first:
tag: autopilot | done | idle | blocked | handoff | need_user
task_id: {args.task_id}
line: {args.line}
node: {line.get('node', 'n/a')}
goal_status: partial | complete | waiting | blocked
next_role: main | verify | research | worker | user | none

Worker goal:
{line.get('goal', '')}

Task title:
{task.get('title', args.task_id)}

Task phase:
{task.get('phase', '')}

Line summary:
{line.get('summary', '') or 'n/a'}

Current next step from controller:
{task.get('next_step', '') or 'n/a'}

Keep the body short and include:
1. Goal
2. Completed
3. Changed artifacts/files
4. Current status
5. Next step
6. Risk
"""
    print(text.rstrip())
    return 0


def cmd_ingest(args: argparse.Namespace) -> int:
    task = load_task(args.task_id)
    artifact = ensure_orchestration_artifact(task)
    payload = Path(args.file).read_text() if args.file else sys.stdin.read()
    parsed = validate_return(args.task_id, payload)
    headers = parsed["headers"]
    line_name = headers["line"]
    line = artifact["lines"].setdefault(line_name, {"line": line_name})
    ts = now_iso()
    line.update({
        "line": line_name,
        "node": headers["node"],
        "status": headers["tag"],
        "goal_status": headers["goal_status"],
        "next_role": headers["next_role"],
        "last_return_tag": headers["tag"],
        "last_return_at": ts,
        "updated_at": ts,
        "last_body": parsed["body"],
        "controller_decision": "pending",
        "controller_note": "",
    })
    task["updated_at"] = ts
    write_task(task)
    classification, reasons = classify_line(line)
    append_event(args.task_id, {
        "ts": ts,
        "type": "subagent_return_ingested",
        "task_id": args.task_id,
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {
            "line": line_name,
            "tag": headers["tag"],
            "goal_status": headers["goal_status"],
            "next_role": headers["next_role"],
            "node": headers["node"],
            "classification": classification,
            "reasons": reasons,
        },
    })
    append_progress(args.task_id, f"ingested worker return for {line_name}: {headers['tag']} / {headers['goal_status']} -> {headers['next_role']} ({classification})")
    print(json.dumps({
        "ok": True,
        "line": line_name,
        "headers": headers,
        "classification": classification,
        "reasons": reasons,
    }, indent=2))
    return 0


def cmd_decide(args: argparse.Namespace) -> int:
    task = load_task(args.task_id)
    artifact = ensure_orchestration_artifact(task)
    line = artifact["lines"].get(args.line)
    if not line:
        raise SystemExit(f"line not found: {args.line}")
    ts = now_iso()
    line["controller_decision"] = args.decision
    line["controller_note"] = args.note or ""
    line["updated_at"] = ts
    if args.next_role is not None:
        line["next_role"] = args.next_role
    if args.status is not None:
        line["status"] = args.status
    task["updated_at"] = ts
    write_task(task)
    append_event(args.task_id, {
        "ts": ts,
        "type": "controller_decision_recorded",
        "task_id": args.task_id,
        "phase": task.get("phase", ""),
        "status": "ok",
        "details": {
            "line": args.line,
            "decision": args.decision,
            "note": args.note or "",
            "next_role": line.get("next_role"),
            "status_value": line.get("status"),
        },
    })
    append_progress(args.task_id, f"controller decision for {args.line}: {args.decision} ({line.get('status')} -> {line.get('next_role')})")
    print(json.dumps(line_record(line, args.line), indent=2))
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    task = load_task(args.task_id)
    artifact = ensure_orchestration_artifact(task)
    dropped: list[dict[str, Any]] = []
    attention: list[dict[str, Any]] = []
    active: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    for name, line in sorted(artifact["lines"].items()):
        record = line_record(line, name)
        classification, reasons = classify_line(line)
        if reasons:
            record["reasons"] = reasons
        if classification == "dropped":
            dropped.append(record)
        elif classification == "attention":
            attention.append(record)
        elif classification == "resolved":
            resolved.append(record)
        else:
            active.append(record)
    result = {
        "ok": len(dropped) == 0,
        "dropped": dropped,
        "attention": attention,
        "active": active,
        "resolved": resolved,
    }
    print(json.dumps(result, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Subagent/controller helper for durable tasks")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("assign")
    a.add_argument("task_id")
    a.add_argument("line")
    a.add_argument("goal")
    a.add_argument("--owner", default="worker")
    a.add_argument("--node", default="start")
    a.add_argument("--summary")
    a.set_defaults(func=cmd_assign)

    pr = sub.add_parser("prompt")
    pr.add_argument("task_id")
    pr.add_argument("line")
    pr.set_defaults(func=cmd_prompt)

    ing = sub.add_parser("ingest")
    ing.add_argument("task_id")
    ing.add_argument("--file")
    ing.set_defaults(func=cmd_ingest)

    dec = sub.add_parser("decide")
    dec.add_argument("task_id")
    dec.add_argument("line")
    dec.add_argument("decision", choices=["dispatch", "verify", "park", "wait_user", "complete", "blocked"])
    dec.add_argument("--note")
    dec.add_argument("--next-role", choices=sorted(ALLOWED_NEXT_ROLES))
    dec.add_argument("--status", choices=sorted(ALLOWED_TAGS | {"assigned"}))
    dec.set_defaults(func=cmd_decide)

    ck = sub.add_parser("check")
    ck.add_argument("task_id")
    ck.set_defaults(func=cmd_check)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
