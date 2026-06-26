#!/usr/bin/env python3
"""Simple CLI task/project board (kanban)."""

import argparse
import json
import os
import sys
from datetime import datetime


DEFAULT_DB = ".tasks.json"
STATUSES = ["todo", "doing", "done"]
PRIORITY_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}
STATUS_ICONS = {"todo": "📋", "doing": "🔨", "done": "✅"}


def load_tasks(db_path):
    """Load tasks from JSON file."""
    if not os.path.exists(db_path):
        return {"next_id": 1, "tasks": []}
    with open(db_path) as f:
        return json.load(f)


def save_tasks(db_path, data):
    """Save tasks to JSON file."""
    with open(db_path, "w") as f:
        json.dump(data, f, indent=2)


def add_task(db_path, title, priority="medium"):
    """Add a new task."""
    data = load_tasks(db_path)
    task = {
        "id": data["next_id"],
        "title": title,
        "status": "todo",
        "priority": priority,
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
    }
    data["tasks"].append(task)
    data["next_id"] += 1
    save_tasks(db_path, data)

    icon = PRIORITY_ICONS.get(priority, "⚪")
    print(f"✅ Task #{task['id']} added: {title} {icon} [{priority}]")


def move_task(db_path, task_id, new_status):
    """Move a task to a new status."""
    if new_status not in STATUSES:
        print(f"❌ Invalid status: {new_status}. Use: {', '.join(STATUSES)}")
        sys.exit(1)

    data = load_tasks(db_path)
    for task in data["tasks"]:
        if task["id"] == task_id:
            old_status = task["status"]
            task["status"] = new_status
            task["updated"] = datetime.now().isoformat()
            save_tasks(db_path, data)
            icon = STATUS_ICONS.get(new_status, "⚪")
            print(f"✅ Task #{task_id}: {old_status} → {new_status} {icon}")
            print(f"   {task['title']}")
            return

    print(f"❌ Task #{task_id} not found")


def list_tasks(db_path, status_filter=None):
    """List tasks."""
    data = load_tasks(db_path)
    tasks = data["tasks"]

    if status_filter:
        tasks = [t for t in tasks if t["status"] == status_filter]

    if not tasks:
        print("📭 No tasks found")
        return

    # Sort: high priority first, then by ID
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: (priority_order.get(t["priority"], 1), t["id"]))

    print(f"📋 Tasks ({len(tasks)}):\n")
    print(f"  {'ID':<5} {'Status':<8} {'Pri':<6} {'Title'}")
    print(f"  {'─' * 5} {'─' * 8} {'─' * 6} {'─' * 40}")

    for task in tasks:
        p_icon = PRIORITY_ICONS.get(task["priority"], "⚪")
        s_icon = STATUS_ICONS.get(task["status"], "⚪")
        title = task["title"][:50]
        print(f"  #{task['id']:<4} {s_icon} {task['status']:<5} {p_icon:<3} {title}")

    print()
    for status in STATUSES:
        count = len([t for t in data["tasks"] if t["status"] == status])
        print(f"  {STATUS_ICONS[status]} {status}: {count}", end="  ")
    print()


def show_board(db_path):
    """Show kanban board view."""
    data = load_tasks(db_path)

    # Group by status
    columns = {s: [] for s in STATUSES}
    for task in data["tasks"]:
        columns[task["status"]].append(task)

    max_items = max(len(v) for v in columns.values()) if data["tasks"] else 0

    print(f"{'─' * 60}")
    print(f"  🗂️  TASK BOARD")
    print(f"{'─' * 60}\n")

    # Column headers
    for status in STATUSES:
        icon = STATUS_ICONS[status]
        count = len(columns[status])
        print(f"  {icon} {status.upper()} ({count})", end="")
    print()
    print(f"  {'─' * 20}  {'─' * 20}  {'─' * 20}")

    # Rows
    for i in range(max_items):
        for status in STATUSES:
            tasks = columns[status]
            if i < len(tasks):
                task = tasks[i]
                p_icon = PRIORITY_ICONS.get(task["priority"], "⚪")
                title = task["title"][:18]
                cell = f"#{task['id']} {p_icon} {title}"
            else:
                cell = ""
            print(f"  {cell:<20}", end="  ")
        print()

    print()


def remove_task(db_path, task_id):
    """Remove a task."""
    data = load_tasks(db_path)
    for i, task in enumerate(data["tasks"]):
        if task["id"] == task_id:
            removed = data["tasks"].pop(i)
            save_tasks(db_path, data)
            print(f"🗑️  Removed task #{task_id}: {removed['title']}")
            return

    print(f"❌ Task #{task_id} not found")


def main():
    parser = argparse.ArgumentParser(description="📋 Task Board — CLI kanban board")
    parser.add_argument("--db", default=DEFAULT_DB, help="Database file path")

    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("--priority", choices=["low", "medium", "high"], default="medium", help="Priority")

    p_move = sub.add_parser("move", help="Move task to new status")
    p_move.add_argument("id", type=int, help="Task ID")
    p_move.add_argument("status", choices=STATUSES, help="New status")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", choices=STATUSES, help="Filter by status")

    sub.add_parser("board", help="Show kanban board view")

    p_remove = sub.add_parser("remove", help="Remove a task")
    p_remove.add_argument("id", type=int, help="Task ID")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.db, args.title, args.priority)
    elif args.command == "move":
        move_task(args.db, args.id, args.status)
    elif args.command == "list":
        list_tasks(args.db, args.status)
    elif args.command == "board":
        show_board(args.db)
    elif args.command == "remove":
        remove_task(args.db, args.id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
