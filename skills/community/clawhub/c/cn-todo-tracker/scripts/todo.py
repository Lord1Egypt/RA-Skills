#!/usr/bin/env python3
"""中文待办事项 - cn-todo-tracker"""

import json, os, sys, argparse
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.qclaw/workspace")
DATA_FILE = os.path.join(WORKSPACE, "todos.json")

PRIORITIES = {"high": "🔴", "medium": "🟡", "low": "🟢"}

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"todos": [], "next_id": 1}

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_todo(text, priority="medium"):
    data = load()
    todo = {
        "id": data["next_id"],
        "text": text,
        "priority": priority,
        "done": False,
        "created": datetime.now().isoformat(),
        "completed": None
    }
    data["todos"].append(todo)
    data["next_id"] += 1
    save(data)
    emoji = PRIORITIES.get(priority, "🟡")
    print(f"\n✅ {emoji} [{todo['id']}] {text}")

def done_todo(todo_id):
    data = load()
    for t in data["todos"]:
        if t["id"] == todo_id and not t["done"]:
            t["done"] = True
            t["completed"] = datetime.now().isoformat()
            save(data)
            print(f"\n🎉 完成待办 [{todo_id}] {t['text']}")
            return
    print(f"\n⚠️ 未找到待办 #{todo_id}")

def list_todos(show="all"):
    data = load()
    todos = data["todos"]
    if show == "today":
        today = datetime.now().strftime("%Y-%m-%d")
        todos = [t for t in todos if t["created"].startswith(today)]
    elif show == "pending":
        todos = [t for t in todos if not t["done"]]

    if not todos:
        print("\n📭 没有待办事项")
        return

    # 按优先级排序
    order = {"high": 0, "medium": 1, "low": 2}
    todos.sort(key=lambda t: (t["done"], order.get(t["priority"], 1)))

    print("\n✅ 待办事项")
    print("=" * 40)
    for t in todos:
        emoji = PRIORITIES.get(t["priority"], "🟡")
        status = "☑️" if t["done"] else "☐"
        print(f"  {status} {emoji} [{t['id']}] {t['text']}")

def stats():
    data = load()
    todos = data["todos"]
    total = len(todos)
    done = sum(1 for t in todos if t["done"])
    pending = total - done
    rate = done / total * 100 if total else 0
    bar = "▓" * int(rate / 10) + "░" * (10 - int(rate / 10))
    print(f"\n📊 待办统计")
    print(f"  总计: {total} | 完成: {done} | 待做: {pending}")
    print(f"  完成率: {rate:.0f}% {bar}")

def main():
    parser = argparse.ArgumentParser(description="✅ 中文待办事项")
    parser.add_argument("--add", help="添加待办")
    parser.add_argument("--priority", "-p", default="medium", choices=["high", "medium", "low"])
    parser.add_argument("--done", type=int, help="完成待办（ID）")
    parser.add_argument("--list", action="store_true", help="全部待办")
    parser.add_argument("--today", action="store_true", help="今日待办")
    parser.add_argument("--stats", action="store_true", help="统计")
    args = parser.parse_args()

    if args.add:
        add_todo(args.add, args.priority)
    elif args.done:
        done_todo(args.done)
    elif args.today:
        list_todos("today")
    elif args.stats:
        stats()
    else:
        list_todos("pending")

if __name__ == "__main__":
    main()