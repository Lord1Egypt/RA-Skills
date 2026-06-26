#!/usr/bin/env python3
"""
Discord Task Tracker - Manage tasks via Discord chat commands.
Reads command from stdin/args, manages tasks in tasks.json, outputs response.
"""

import sys
import json
import os
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SKILL_DIR = Path(__file__).parent.parent
TASKS_FILE = SKILL_DIR / "tasks.json"


def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def cmd_add(text):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "text": text.strip(), "done": False})
    save_tasks(tasks)
    print(f"✅ Task added (#{task_id}): {text.strip()}")


def cmd_list():
    tasks = load_tasks()
    if not tasks:
        print("📋 No tasks yet. Say 'add task <description>' to create one.")
        return
    lines = ["**📋 Your Tasks:**"]
    for t in tasks:
        status = "✅" if t["done"] else "⬜"
        lines.append(f"  {status} `[{t['id']}]` {t['text']}")
    print("\n".join(lines))


def cmd_complete(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == int(task_id)), None)
    if not task:
        print(f"❌ Task #{task_id} not found.")
        return
    task["done"] = True
    save_tasks(tasks)
    # Remove completed task
    tasks = [t for t in tasks if not (t["id"] == int(task_id))]
    save_tasks(tasks)
    print(f"✅ Task #{task_id} completed and removed: {task['text']}")


def cmd_delete(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == int(task_id)), None)
    if not task:
        print(f"❌ Task #{task_id} not found.")
        return
    tasks = [t for t in tasks if t["id"] != int(task_id)]
    save_tasks(tasks)
    print(f"🗑️ Task #{task_id} deleted: {task['text']}")


def main():
    # Read full input (can be passed via stdin or args)
    raw = ""
    if len(sys.argv) > 1:
        raw = " ".join(sys.argv[1:])
    else:
        raw = sys.stdin.read().strip()

    raw = raw.strip()
    if not raw:
        print("Usage: task_manager.py <command>")
        sys.exit(1)

    lower = raw.lower()

    # add task <text>
    if lower.startswith("add task ") or lower.startswith("track task ") or lower.startswith("todo "):
        text = raw.split(" ", 2)[-1]
        cmd_add(text)
    # list tasks / my tasks / task list
    elif lower in ("list tasks", "my tasks", "task list", "list", "tasks"):
        cmd_list()
    # complete task <id>
    elif lower.startswith("complete task ") or lower.startswith("task done ") or lower.startswith("done "):
        parts = raw.split()
        if len(parts) >= 2:
            cmd_complete(parts[-1])
        else:
            print("❌ Usage: complete task <task number>")
    # delete task <id>
    elif lower.startswith("delete task "):
        parts = raw.split()
        if len(parts) >= 2:
            cmd_delete(parts[-1])
        else:
            print("❌ Usage: delete task <task number>")
    else:
        print("Unknown command. Use: add task <text>, list tasks, complete task <#>, delete task <#>")


if __name__ == "__main__":
    main()
