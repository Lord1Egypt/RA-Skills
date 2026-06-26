#!/usr/bin/env python3
"""
Send a compact status line using the task's bound delivery metadata.

Kinds:
- timed: recurring due-based status tick
- immediate: event-driven breadcrumb after meaningful task changes

Delivery methods:
- openclaw (default): send via `openclaw message send`
- stdout: print the rendered message only
- noop: render, but intentionally do not deliver
- log-only: record the send attempt in task history without external delivery
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "state" / "tasks"
SCRIPT_DIR = ROOT / "scripts"


def load_task(task_id: str) -> dict[str, Any]:
    path = STATE_DIR / f"{task_id}.json"
    if not path.exists():
        raise SystemExit(f"task not found: {task_id}")
    return json.loads(path.read_text())


def delivery_binding(task: dict[str, Any]) -> dict[str, Any]:
    for item in task.get("artifacts", []):
        if isinstance(item, dict) and item.get("kind") == "delivery_binding":
            return item
    raise SystemExit("no delivery_binding artifact found")


def run(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def extract_json_object(raw: str) -> dict[str, Any]:
    raw = raw.strip()
    starts = [i for i, ch in enumerate(raw) if ch == "{"]
    best: dict[str, Any] | None = None
    for start in starts:
        depth = 0
        in_string = False
        escape = False
        for idx in range(start, len(raw)):
            ch = raw[idx]
            if in_string:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_string = False
                continue
            if ch == '"':
                in_string = True
                continue
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    candidate = raw[start:idx + 1]
                    try:
                        value = json.loads(candidate)
                    except json.JSONDecodeError:
                        break
                    if isinstance(value, dict):
                        best = value
                    break
    if best is not None:
        return best
    raise SystemExit(f"could not parse JSON payload from openclaw output: {raw}")


def build_line(task_id: str, kind: str, reason: str | None) -> tuple[str, dict[str, Any]]:
    snapshot_raw = run("python3", str(SCRIPT_DIR / "task_status_snapshot.py"), task_id)
    snapshot = json.loads(snapshot_raw)
    ticker = run("python3", str(SCRIPT_DIR / "task_ticker.py"), task_id)
    if kind == "immediate":
        prefix = f"update:{reason}" if reason else "update"
        return f"{prefix} | {ticker}", snapshot
    return ticker, snapshot


def perform_delivery(binding: dict[str, Any], line: str) -> dict[str, Any]:
    method = binding.get("method", "openclaw")
    if method == "stdout":
        print(line)
        return {"method": method, "delivered": True, "target": "stdout"}
    if method == "noop":
        return {"method": method, "delivered": False, "reason": "noop_mode"}
    if method == "log-only":
        return {"method": method, "delivered": False, "reason": "log_only"}
    if method != "openclaw":
        raise SystemExit(f"unsupported delivery method: {method}")

    cmd = [
        "openclaw", "message", "send",
        "--channel", binding["channel"],
        "--target", binding["target"],
        "--account", binding.get("account_id", "default"),
        "--message", line,
        "--json",
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True, check=True)
    combined_output = "\n".join(part for part in [proc.stdout.strip(), proc.stderr.strip()] if part).strip()
    delivery = extract_json_object(combined_output) if combined_output else {"raw": ""}
    return {
        "method": method,
        "delivered": True,
        "target": binding.get("target", ""),
        "payload": delivery,
        "raw_output": combined_output,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("task_id")
    ap.add_argument("--kind", choices=["timed", "immediate"], default="timed")
    ap.add_argument("--reason", default="")
    args = ap.parse_args()

    task_id = args.task_id
    task = load_task(task_id)
    binding = delivery_binding(task)
    line, snapshot = build_line(task_id, args.kind, args.reason or None)
    delivery = perform_delivery(binding, line)

    log_line = f"status sent ({args.kind}{':' + args.reason if args.reason else ''}, method={delivery['method']}): {line}"
    subprocess.run([
        "python3", str(SCRIPT_DIR / "task_ctl.py"), "progress", task_id, log_line,
        "--report-kind", "internal",
    ], check=True, stdout=subprocess.DEVNULL)
    print(json.dumps({
        "sent": True,
        "kind": args.kind,
        "reason": args.reason,
        "line": line,
        "snapshot": snapshot,
        "delivery": delivery,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
