#!/usr/bin/env python3
"""
Interruption queue helper for durable-task-runner.

Attribution note:
- This script is closely inspired by the ClawHub skill `task-resume`, especially its
  small JSON-backed queue helper pattern.
- This file is a fresh local adaptation for durable-task-runner, with slightly different
  naming and intent, and should remain explicitly credited.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / "state" / "tasks" / "interrupt-queue.json"
MAX_ITEMS = 100


def jprint(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def load_queue() -> list[dict[str, Any]]:
    if not QUEUE_PATH.exists():
        return []
    try:
        data = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_queue(items: list[dict[str, Any]]) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def norm(s: str | None) -> str:
    return " ".join((s or "").strip().lower().split())


def add_item(task_id: str, title: str, context: str, acceptance: str, source: str, session: str) -> None:
    now = int(time.time())
    q = load_queue()
    tnorm = norm(title)
    cnorm = norm(context)

    for item in q:
        if norm(item.get("title")) == tnorm and norm(item.get("context")) == cnorm:
            item["updated_at"] = now
            if task_id:
                item["task_id"] = task_id
            if source:
                item["source"] = source
            if session:
                item["session"] = session
            save_queue(q)
            jprint({"status": "updated", "item": item})
            return

    item = {
        "id": f"irq_{now}_{len(q)+1}",
        "task_id": task_id,
        "title": title,
        "context": context,
        "acceptance": acceptance,
        "source": source,
        "session": session,
        "created_at": now,
        "updated_at": now,
    }
    q.append(item)
    dropped = []
    if len(q) > MAX_ITEMS:
        dropped = q[:-MAX_ITEMS]
        q = q[-MAX_ITEMS:]
    save_queue(q)
    jprint({"status": "added", "item": item, "dropped": dropped})


def pop_item() -> None:
    q = load_queue()
    if not q:
        jprint({"status": "empty"})
        return
    item = q.pop(0)
    save_queue(q)
    jprint({"status": "popped", "item": item})


def list_items() -> None:
    q = load_queue()
    jprint({"status": "ok", "count": len(q), "items": q})


def status_items() -> None:
    q = load_queue()
    by_source: dict[str, int] = {}
    by_session: dict[str, int] = {}
    for item in q:
        src = item.get("source") or "unknown"
        ses = item.get("session") or "unknown"
        by_source[src] = by_source.get(src, 0) + 1
        by_session[ses] = by_session.get(ses, 0) + 1
    jprint({"status": "ok", "count": len(q), "by_source": by_source, "by_session": by_session})


def clear_items() -> None:
    save_queue([])
    jprint({"status": "cleared"})


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--task-id", default="")
    a.add_argument("--title", required=True)
    a.add_argument("--context", required=True)
    a.add_argument("--acceptance", default="")
    a.add_argument("--source", default="")
    a.add_argument("--session", default="")

    sub.add_parser("pop")
    sub.add_parser("list")
    sub.add_parser("status")
    sub.add_parser("clear")

    args = p.parse_args()
    if args.cmd == "add":
        add_item(args.task_id, args.title, args.context, args.acceptance, args.source, args.session)
    elif args.cmd == "pop":
        pop_item()
    elif args.cmd == "list":
        list_items()
    elif args.cmd == "status":
        status_items()
    elif args.cmd == "clear":
        clear_items()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
