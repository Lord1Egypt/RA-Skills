#!/usr/bin/env python3
"""todo_write — 任务列表管理"""
import sys, os, json
from datetime import datetime
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *

VALID_STATUSES = {"pending", "in_progress", "completed", "cancelled"}


def get_todo_path(params):
    """获取任务存储路径"""
    custom = get_param(params, "path")
    if custom:
        return resolve_path(custom, must_exist=False)
    return Path.cwd() / ".builtin-tools" / "todos.json"


def load_todos(todo_path):
    """加载任务列表"""
    if todo_path.exists():
        try:
            return json.loads(todo_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, Exception):
            return []
    return []


def save_todos(todo_path, todos):
    """保存任务列表"""
    todo_path.parent.mkdir(parents=True, exist_ok=True)
    todo_path.write_text(
        json.dumps(todos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def validate_todos(todos):
    """验证任务列表格式"""
    if not isinstance(todos, list):
        return False, "todos 必须是数组"
    if not todos:
        return False, "todos 不能为空"
    seen_ids = set()
    in_progress_count = 0
    for todo in todos:
        if not isinstance(todo, dict):
            return False, f"无效的任务项: {todo}"
        if "id" not in todo:
            return False, "每个任务必须有 id"
        if "content" not in todo:
            return False, f"任务 {todo['id']} 缺少 content"
        if "status" not in todo:
            return False, f"任务 {todo['id']} 缺少 status"
        if todo["status"] not in VALID_STATUSES:
            return False, f"任务 {todo['id']} 状态无效: {todo['status']}"
        if todo["id"] in seen_ids:
            return False, f"重复的 id: {todo['id']}"
        seen_ids.add(todo["id"])
        if todo["status"] == "in_progress":
            in_progress_count += 1
    if in_progress_count > 1:
        return False, f"只能有一个 in_progress 任务，当前有 {in_progress_count} 个"
    return True, None


def format_todos(todos):
    """格式化任务列表为控制台可读"""
    status_icons = {
        "pending": "⬜",
        "in_progress": "🔄",
        "completed": "✅",
        "cancelled": "❌",
    }
    lines = []
    for todo in todos:
        icon = status_icons.get(todo["status"], "?")
        lines.append(f"  {icon} [{todo['id']}] {todo['status']}: {todo['content']}")
    return "\n".join(lines)


def main():
    params = parse_input()
    merge = get_param(params, "merge", False)
    todos = get_param(params, "todos", required=True)

    # 兼容：如果 todos 是字符串（JSON），解析它
    if isinstance(todos, str):
        try:
            todos = json.loads(todos)
        except json.JSONDecodeError:
            output_error("todos JSON 解析失败", EXIT_PARAM_ERROR)

    valid, error = validate_todos(todos)
    if not valid:
        output_error(error, EXIT_PARAM_ERROR)

    todo_path = get_todo_path(params)

    if merge:
        existing = load_todos(todo_path)
        existing_map = {t["id"]: t for t in existing}
        for todo in todos:
            existing_map[todo["id"]] = todo
        # 保持原始顺序
        merged = []
        seen = set()
        for t in existing + todos:
            if t["id"] not in seen:
                merged.append(existing_map[t["id"]])
                seen.add(t["id"])
        todos = merged

    save_todos(todo_path, todos)

    # 统计
    stats = {}
    for s in VALID_STATUSES:
        stats[s] = sum(1 for t in todos if t["status"] == s)

    output_ok({
        "path": str(todo_path),
        "total": len(todos),
        "stats": stats,
        "todos": todos,
        "display": format_todos(todos),
    })


if __name__ == "__main__":
    main()
