#!/usr/bin/env python3
"""
面包屑小本本 (Breadcrumb Notebook)
- 知识条目的增删查改
- 每一条关联原文文件路径
- 内嵌复习记录（review_count, last_reviewed_at, next_review_at）
- 数据存储：~/.everything_search/breadcrumb.json
"""

import argparse
import base64
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "everything-search-breadmemory" / "data"
BREADCRUMB_FILE = DATA_DIR / "breadcrumb.json"


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _get_next_backup_index():
    """计算下一个备份索引，循环 1-9"""
    existing = sorted([
        int(f.stem.rsplit('_', 1)[-1])
        for f in DATA_DIR.glob("breadcrumb_backup_*.bat")
        if f.stem.rsplit('_', 1)[-1].isdigit()
    ])
    if not existing:
        return 1
    last = existing[-1]
    if last < 9:
        return last + 1
    return 1  # 循环回到 1


def backup_disaster_recovery(entries=None):
    """
    容灾备份机制：在每次写入操作前，生成 .bat 备份文件。
    最多保留 9 个备份（breadcrumb_backup_01 ~ 09），循环覆盖。
    
    Args:
        entries: 当前（修改前）的面包屑条目列表。None 则加载当前文件。
    
    Returns:
        str: 生成的 .bat 文件路径，None 表示跳过（空数据）
    """
    if entries is None:
        entries = load_breadcrumbs()
    
    # 空数据不备份（避免无效备份文件）
    if not entries:
        return None
    
    ensure_data_dir()
    data = {"entries": entries, "updated_at": datetime.now().isoformat()}
    
    # 计算下一个备份索引（循环 1-9）
    index = _get_next_backup_index()
    
    bat_path = DATA_DIR / f"breadcrumb_backup_{index:02d}.bat"
    py_path = DATA_DIR / f"breadcrumb_backup_{index:02d}.py"
    
    # 覆盖旧的同索引文件（循环覆盖）
    for p in [bat_path, py_path]:
        if p.exists():
            p.unlink()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_count = len(entries)
    
    # 使用 base64 编码避免 JSON null/特殊字符问题
    data_json_str = json.dumps(data, ensure_ascii=False)
    data_b64 = base64.b64encode(data_json_str.encode('utf-8')).decode('ascii')
    
    # 生成 Python 恢复脚本（base64 编码数据，安全无歧义）
    py_content = f'''"""Breadcrumb Disaster Recovery - Backup #{index:02d}
Created: {timestamp}
Entries: {entry_count}
Run this script to restore breadcrumb.json to this backup point.
"""

import json
import os
import base64 as _b64

TARGET = r"{BREADCRUMB_FILE}"

DATA_B64 = "{data_b64}"
DATA = json.loads(_b64.b64decode(DATA_B64).decode('utf-8'))

# 确保目录存在
os.makedirs(os.path.dirname(TARGET), exist_ok=True)

with open(TARGET, 'w', encoding='utf-8') as f:
    json.dump(DATA, f, ensure_ascii=False, indent=2)

print(f"[OK] Restored {{len(DATA.get('entries', []))}} entries to:")
print(f"     {{TARGET}}")
print(f"Backup timestamp: {{DATA.get('updated_at', 'unknown')}}")
input("\\nPress Enter to exit...")
'''
    
    with open(py_path, 'w', encoding='utf-8') as f:
        f.write(py_content)
    
    # 生成 .bat 启动器
    bat_content = f'''@echo off
chcp 65001 >nul
echo ============================================
echo   Breadcrumb Disaster Recovery
echo   Backup #{index:02d}  |  {timestamp}
echo   Entries: {entry_count}
echo ============================================
echo.
echo Restoring breadcrumb.json from this backup...
echo.
python "%~dp0breadcrumb_backup_{index:02d}.py"
pause
'''
    
    with open(bat_path, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    return str(bat_path)


def load_breadcrumbs():
    """加载所有面包屑条目"""
    ensure_data_dir()
    if BREADCRUMB_FILE.exists():
        with open(BREADCRUMB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("entries", [])
    return []


def save_breadcrumbs(entries):
    """保存面包屑条目"""
    ensure_data_dir()
    with open(BREADCRUMB_FILE, "w", encoding="utf-8") as f:
        json.dump({"entries": entries, "updated_at": datetime.now().isoformat()},
                  f, indent=2, ensure_ascii=False)


def add_entry(title, content, source="", tags=None, auto_source=None):
    """
    添加一条知识条目

    字段：
    - id: 唯一标识符
    - title: 标题
    - content: 知识内容（摘要/归纳）
    - source: 原文文件路径
    - auto_source: 自动关联的多个原文路径列表
    - tags: 标签列表
    - created_at: 创建时间
    - review_count: 已复习次数
    - last_reviewed_at: 上次复习时间
    - next_review_at: 下次应复习时间（艾宾浩斯间隔）
    """
    entries = load_breadcrumbs()

    # 容灾备份：保存修改前的状态
    backup_disaster_recovery(entries)

    now = datetime.now().isoformat()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "content": content,
        "source": source,
        "auto_source": auto_source or [],
        "tags": tags or [],
        "created_at": now,
        "review_count": 0,
        "last_reviewed_at": None,
        "next_review_at": (datetime.now() + timedelta(days=1)).isoformat()  # 首次复习：1天后
    }
    entries.append(entry)
    save_breadcrumbs(entries)
    return entry


def list_entries(tag=None, limit=50, offset=0):
    """列出条目，支持按标签过滤"""
    entries = load_breadcrumbs()
    if tag:
        entries = [e for e in entries if tag in e.get("tags", [])]
    entries = sorted(entries, key=lambda e: e.get("created_at", ""), reverse=True)
    total = len(entries)
    entries = entries[offset:offset + limit]
    return {"total": total, "entries": entries}


def search_entries(keyword):
    """按关键词搜索条目（标题和内容）"""
    entries = load_breadcrumbs()
    kw = keyword.lower()
    results = [e for e in entries
               if kw in e.get("title", "").lower() or kw in e.get("content", "").lower()]
    results = sorted(results, key=lambda e: e.get("created_at", ""), reverse=True)
    return {"total": len(results), "entries": results}


def show_entry(entry_id):
    """查看单条详情"""
    entries = load_breadcrumbs()
    for e in entries:
        if e["id"] == entry_id:
            return e
    return None


def delete_entry(entry_id):
    """删除条目"""
    entries = load_breadcrumbs()

    # 容灾备份：保存删除前的状态
    backup_disaster_recovery(entries)

    new_entries = [e for e in entries if e["id"] != entry_id]
    deleted = len(entries) - len(new_entries)
    if deleted > 0:
        save_breadcrumbs(new_entries)
    return deleted > 0


def update_entry(entry_id, title=None, content=None, tags=None, add_source=None):
    """更新条目"""
    entries = load_breadcrumbs()

    # 容灾备份：保存更新前的状态
    backup_disaster_recovery(entries)

    for e in entries:
        if e["id"] == entry_id:
            if title is not None:
                e["title"] = title
            if content is not None:
                e["content"] = content
            if tags is not None:
                e["tags"] = tags
            if add_source is not None and add_source not in e.get("auto_source", []):
                if "auto_source" not in e:
                    e["auto_source"] = []
                e["auto_source"].append(add_source)
            save_breadcrumbs(entries)
            return e
    return None


def get_review_records():
    """获取所有条目的复习记录（供 ebbinghaus 引擎使用）"""
    entries = load_breadcrumbs()
    records = []
    for e in entries:
        records.append({
            "id": e["id"],
            "title": e["title"],
            "created_at": e.get("created_at"),
            "review_count": e.get("review_count", 0),
            "last_reviewed_at": e.get("last_reviewed_at"),
            "next_review_at": e.get("next_review_at")
        })
    return records


def update_review_record(entry_id, review_count, last_reviewed_at, next_review_at):
    """更新复习记录（供 ebbinghaus 引擎调用）"""
    entries = load_breadcrumbs()

    # 容灾备份：保存更新前的状态
    backup_disaster_recovery(entries)

    for e in entries:
        if e["id"] == entry_id:
            e["review_count"] = review_count
            e["last_reviewed_at"] = last_reviewed_at
            e["next_review_at"] = next_review_at
            save_breadcrumbs(entries)
            return True
    return False


def stats():
    """统计信息"""
    entries = load_breadcrumbs()
    now = datetime.now()
    total = len(entries)
    reviewed_today = sum(1 for e in entries
                         if e.get("last_reviewed_at") and
                         e["last_reviewed_at"].startswith(now.strftime("%Y-%m-%d")))
    pending_review = sum(1 for e in entries
                         if e.get("next_review_at") and e["next_review_at"] <= now.isoformat())
    tags_count = {}
    for e in entries:
        for t in e.get("tags", []):
            tags_count[t] = tags_count.get(t, 0) + 1

    return {
        "total_entries": total,
        "reviewed_today": reviewed_today,
        "pending_review": pending_review,
        "top_tags": sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10]
    }


def main():
    parser = argparse.ArgumentParser(description="面包屑小本本 - 知识管理")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # add
    add_parser = subparsers.add_parser("add", help="添加知识条目")
    add_parser.add_argument("--title", required=True, help="标题")
    add_parser.add_argument("--content", required=True, help="知识内容")
    add_parser.add_argument("--source", default="", help="原文文件路径")
    add_parser.add_argument("--tags", help="标签，逗号分隔")

    # list
    list_parser = subparsers.add_parser("list", help="列出条目")
    list_parser.add_argument("--tag", help="按标签过滤")
    list_parser.add_argument("--limit", type=int, default=50, help="返回条数")
    list_parser.add_argument("--offset", type=int, default=0, help="偏移量")

    # search
    search_parser = subparsers.add_parser("search", help="搜索条目")
    search_parser.add_argument("keyword", help="搜索关键词")

    # show
    show_parser = subparsers.add_parser("show", help="查看条目详情")
    show_parser.add_argument("--id", required=True, help="条目ID")

    # delete
    delete_parser = subparsers.add_parser("delete", help="删除条目")
    delete_parser.add_argument("--id", required=True, help="条目ID")

    # update
    update_parser = subparsers.add_parser("update", help="更新条目")
    update_parser.add_argument("--id", required=True, help="条目ID")
    update_parser.add_argument("--title", help="新标题")
    update_parser.add_argument("--content", help="新内容")
    update_parser.add_argument("--tags", help="新标签，逗号分隔")
    update_parser.add_argument("--add-source", help="追加关联原文路径")

    # stats
    subparsers.add_parser("stats", help="统计信息")

    # review-records (内部使用，供 ebbinghaus 引擎)
    subparsers.add_parser("review-records", help="输出所有复习记录")

    args = parser.parse_args()

    if args.command == "add":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        entry = add_entry(args.title, args.content, args.source, tags)
        result = {"status": "added", "entry": entry}

    elif args.command == "list":
        result = list_entries(tag=args.tag, limit=args.limit, offset=args.offset)

    elif args.command == "search":
        result = search_entries(args.keyword)

    elif args.command == "show":
        entry = show_entry(args.id)
        result = entry if entry else {"error": f"条目 {args.id} 不存在"}

    elif args.command == "delete":
        ok = delete_entry(args.id)
        result = {"status": "deleted" if ok else "not_found", "id": args.id}

    elif args.command == "update":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        entry = update_entry(args.id, title=args.title, content=args.content,
                            tags=tags, add_source=args.add_source)
        result = {"status": "updated", "entry": entry} if entry else {"error": f"条目 {args.id} 不存在"}

    elif args.command == "stats":
        result = stats()

    elif args.command == "review-records":
        result = {"records": get_review_records()}

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
