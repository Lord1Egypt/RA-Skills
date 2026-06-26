#!/usr/bin/env python3
"""update_memory — 跨平台持久化记忆管理"""
import sys, os, json, time, uuid
from datetime import datetime
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from common import *


def get_memory_path(params):
    """获取记忆目录路径"""
    base = get_param(params, "memory_dir")
    if base:
        return resolve_path(base, must_exist=False)
    return memory_dir()


def ensure_memory_dir(memory_path):
    """确保记忆目录存在"""
    memory_path.mkdir(parents=True, exist_ok=True)


def generate_id():
    """生成唯一 ID"""
    return str(uuid.uuid4())[:8]


def get_today():
    """获取今日日期字符串"""
    return datetime.now().strftime("%Y-%m-%d")


def load_memory_index(memory_path):
    """加载记忆索引文件"""
    index_path = memory_path / "MEMORY.md"
    if index_path.exists():
        try:
            return index_path.read_text(encoding="utf-8")
        except Exception:
            return ""
    return ""


def append_daily(memory_path, entry_text):
    """追加到每日日志"""
    daily_path = memory_path / f"{get_today()}.md"
    ensure_memory_dir(memory_path)
    timestamp = datetime.now().strftime("%H:%M")
    entry = f"\n## [{timestamp}] {entry_text}\n"
    try:
        with open(daily_path, "a", encoding="utf-8") as f:
            f.write(entry)
        return True
    except Exception as e:
        return False


def search_memories(memory_path, query, limit=20):
    """搜索记忆文件"""
    ensure_memory_dir(memory_path)
    results = []
    query_lower = query.lower()

    for md_file in sorted(memory_path.glob("*.md"), reverse=True):
        if len(results) >= limit:
            break
        try:
            content = md_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    results.append({
                        "file": md_file.name,
                        "line": i + 1,
                        "text": line.strip()[:200],
                    })
                    if len(results) >= limit:
                        break
        except Exception:
            continue

    return results


def main():
    params = parse_input()
    action = get_param(params, "action", "list").lower()

    memory_path = get_memory_path(params)

    if action == "create":
        title = get_param(params, "title", required=True)
        content = get_param(params, "content", "")
        category = get_param(params, "category", "general")
        mem_id = generate_id()

        ensure_memory_dir(memory_path)
        entry_text = f"[{category}] {title}: {content}"
        success = append_daily(memory_path, entry_text)

        if success:
            output_ok({
                "action": "created",
                "id": mem_id,
                "title": title,
                "category": category,
                "file": f"{get_today()}.md",
                "dir": str(memory_path),
            })
        else:
            output_error("写入失败", EXIT_EXEC_ERROR)

    elif action == "update":
        # 更新：追加到每日日志，标记为更新
        title = get_param(params, "title", required=True)
        content = get_param(params, "content", required=True)
        existing_id = get_param(params, "id")

        ensure_memory_dir(memory_path)
        entry_text = f"[update:{existing_id or ''}] {title}: {content}"
        success = append_daily(memory_path, entry_text)

        if success:
            output_ok({
                "action": "updated",
                "id": existing_id or generate_id(),
                "title": title,
                "file": f"{get_today()}.md",
            })
        else:
            output_error("写入失败", EXIT_EXEC_ERROR)

    elif action == "delete":
        # 删除：在日志中标记（不物理删除，保持审计）
        title = get_param(params, "title", "deleted item")
        existing_id = get_param(params, "id", "")

        ensure_memory_dir(memory_path)
        entry_text = f"[deleted:{existing_id}] {title}"
        success = append_daily(memory_path, entry_text)

        if success:
            output_ok({"action": "deleted", "id": existing_id})
        else:
            output_error("写入失败", EXIT_EXEC_ERROR)

    elif action == "search":
        query = get_param(params, "query", required=True)
        limit = get_param(params, "limit", 20)
        results = search_memories(memory_path, query, limit)
        output_ok({
            "action": "search",
            "query": query,
            "results": results,
            "total": len(results),
            "dir": str(memory_path),
        })

    elif action == "list":
        # 列出所有记忆文件
        ensure_memory_dir(memory_path)
        files = []
        for md_file in sorted(memory_path.glob("*.md"), reverse=True):
            try:
                stat = md_file.stat()
                files.append({
                    "name": md_file.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
            except Exception:
                files.append({"name": md_file.name})

        output_ok({
            "action": "list",
            "dir": str(memory_path),
            "files": files,
            "total": len(files),
        })

    elif action == "read":
        # 读取指定记忆文件
        filename = get_param(params, "file", required=True)
        file_path = memory_path / filename
        if not file_path.exists():
            # 尝试今日文件
            file_path = memory_path / f"{get_today()}.md"
        if not file_path.exists():
            output_error(f"文件不存在: {filename}", EXIT_EXEC_ERROR)

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            output_error(f"读取失败: {e}", EXIT_EXEC_ERROR)

        output_ok({
            "action": "read",
            "file": file_path.name,
            "content": content,
            "lines": len(content.splitlines()),
        })

    else:
        output_error(
            f"未知操作: {action}（支持: create, update, delete, search, list, read）",
            EXIT_PARAM_ERROR,
        )


if __name__ == "__main__":
    main()
