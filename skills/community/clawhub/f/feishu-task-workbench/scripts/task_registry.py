#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

STATUS_CHOICES = [
    "todo",
    "in_progress",
    "waiting_input",
    "blocked",
    "completed",
    "archived",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_registry() -> dict:
    return {
        "version": 1,
        "currentTaskId": None,
        "nextTaskId": 1,
        "tasks": [],
    }


def load_registry(path: Path) -> dict:
    if not path.exists():
        data = default_registry()
        save_registry(path, data)
        return data
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    data.setdefault("version", 1)
    data.setdefault("currentTaskId", None)
    data.setdefault("nextTaskId", 1)
    data.setdefault("tasks", [])
    return data


def save_registry(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find_task(data: dict, task_id: int) -> dict:
    for task in data["tasks"]:
        if task["id"] == task_id:
            return task
    raise SystemExit(f"Task #{task_id} not found")


def emit(payload: dict) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def cmd_init(args):
    path = Path(args.registry)
    data = load_registry(path)
    save_registry(path, data)
    emit({"ok": True, "registry": str(path), "data": data})


def cmd_add(args):
    path = Path(args.registry)
    data = load_registry(path)
    task_id = data["nextTaskId"]
    task = {
        "id": task_id,
        "title": args.title,
        "status": args.status,
        "sessionKey": args.session_key,
        "summary": args.summary or "",
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
        "tags": args.tags or [],
    }
    data["tasks"].append(task)
    data["nextTaskId"] = task_id + 1
    if args.make_current or data["currentTaskId"] is None:
        data["currentTaskId"] = task_id
    save_registry(path, data)
    emit({"ok": True, "action": "add", "task": task, "currentTaskId": data["currentTaskId"]})


def cmd_list(args):
    path = Path(args.registry)
    data = load_registry(path)
    tasks = data["tasks"]
    if not args.include_archived:
        tasks = [t for t in tasks if t.get("status") != "archived"]
    emit({"ok": True, "action": "list", "currentTaskId": data["currentTaskId"], "tasks": tasks})


def cmd_switch(args):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    data["currentTaskId"] = task["id"]
    task["updatedAt"] = now_iso()
    save_registry(path, data)
    emit({"ok": True, "action": "switch", "currentTaskId": data["currentTaskId"], "task": task})


def cmd_show(args):
    path = Path(args.registry)
    data = load_registry(path)
    task_id = args.task_id if args.task_id is not None else data.get("currentTaskId")
    if task_id is None:
        emit({"ok": True, "action": "show", "task": None, "currentTaskId": None})
        return
    task = find_task(data, task_id)
    emit({"ok": True, "action": "show", "task": task, "currentTaskId": data["currentTaskId"]})


def cmd_update(args):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    changed = {}
    if args.title is not None:
        task["title"] = args.title
        changed["title"] = args.title
    if args.status is not None:
        task["status"] = args.status
        changed["status"] = args.status
    if args.session_key is not None:
        task["sessionKey"] = args.session_key
        changed["sessionKey"] = args.session_key
    if args.summary is not None:
        task["summary"] = args.summary
        changed["summary"] = args.summary
    if args.tags is not None:
        task["tags"] = args.tags
        changed["tags"] = args.tags
    task["updatedAt"] = now_iso()
    save_registry(path, data)
    emit({"ok": True, "action": "update", "changed": changed, "task": task})


def cmd_close_like(args, status: str, action: str):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    task["status"] = status
    if args.summary is not None:
        task["summary"] = args.summary
    task["updatedAt"] = now_iso()
    if data.get("currentTaskId") == task["id"] and status in {"completed", "archived"}:
        active = [t for t in data["tasks"] if t["id"] != task["id"] and t.get("status") not in {"completed", "archived"}]
        data["currentTaskId"] = active[-1]["id"] if active else None
    save_registry(path, data)
    emit({"ok": True, "action": action, "task": task, "currentTaskId": data["currentTaskId"]})


def cmd_summarize(args):
    path = Path(args.registry)
    data = load_registry(path)
    task = find_task(data, args.task_id)
    emit({
        "ok": True,
        "action": "summarize",
        "task": {
            "id": task["id"],
            "title": task["title"],
            "status": task["status"],
            "summary": task.get("summary", ""),
            "updatedAt": task["updatedAt"],
            "sessionKey": task.get("sessionKey"),
        },
        "currentTaskId": data["currentTaskId"],
    })


def build_parser():
    parser = argparse.ArgumentParser(description="Manage Feishu Task Workbench JSON registry")
    parser.add_argument("--registry", required=True, help="Path to registry JSON file")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add")
    p.add_argument("title")
    p.add_argument("--status", choices=STATUS_CHOICES, default="todo")
    p.add_argument("--session-key", required=True)
    p.add_argument("--summary")
    p.add_argument("--make-current", action="store_true")
    p.add_argument("--tags", nargs="*")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list")
    p.add_argument("--include-archived", action="store_true")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("switch")
    p.add_argument("task_id", type=int)
    p.set_defaults(func=cmd_switch)

    p = sub.add_parser("show")
    p.add_argument("task_id", type=int, nargs="?")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("update")
    p.add_argument("task_id", type=int)
    p.add_argument("--title")
    p.add_argument("--status", choices=STATUS_CHOICES)
    p.add_argument("--session-key")
    p.add_argument("--summary")
    p.add_argument("--tags", nargs="*")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("close")
    p.add_argument("task_id", type=int)
    p.add_argument("--summary")
    p.set_defaults(func=lambda a: cmd_close_like(a, "completed", "close"))

    p = sub.add_parser("archive")
    p.add_argument("task_id", type=int)
    p.add_argument("--summary")
    p.set_defaults(func=lambda a: cmd_close_like(a, "archived", "archive"))

    p = sub.add_parser("summarize")
    p.add_argument("task_id", type=int)
    p.set_defaults(func=cmd_summarize)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
