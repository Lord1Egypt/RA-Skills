#!/usr/bin/env python3
"""
Self-Improving Agent - 记忆管理工具
统计、清理、去重、重建索引、导出
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_utils import MEMORY_DIR, ensure_dir, load_entries, save_entries, get_filepath

FILES = {
    "errors": "errors.jsonl",
    "corrections": "corrections.jsonl",
    "best_practices": "best_practices.jsonl",
    "knowledge_gaps": "knowledge_gaps.jsonl",
}


def cmd_stats():
    """显示记忆统计"""
    ensure_dir()
    total = 0
    print("=== 记忆系统统计 ===\n")

    for name, fname in FILES.items():
        entries = load_entries(fname)
        count = len(entries)
        total += count

        filepath = get_filepath(fname)
        size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
        size_str = f"{size / 1024:.1f}KB" if size > 1024 else f"{size}B"

        print(f"  {name:20s}  {count:4d} 条  ({size_str})")

        # 类型特定统计
        if name == "errors" and entries:
            resolved = sum(1 for e in entries if e.get("status") == "resolved")
            high = sum(1 for e in entries if e.get("priority") == "high")
            print(f"    {'':20s}  已解决: {resolved}/{count}  高优: {high}")
        elif name == "corrections" and entries:
            multi = [e for e in entries if e.get("count", 1) > 1]
            if multi:
                print(f"    {'':20s}  多次纠正: {len(multi)} 条")

    print(f"\n  {'总计':20s}  {total:4d} 条")

    # 索引状态
    index_path = get_filepath("index.json")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            try:
                index = json.load(f)
                kw_count = len(index.get("keywords", {}))
                updated = index.get("last_updated", "未知")[:19]
                print(f"\n  索引: {kw_count} 个关键词, 更新于 {updated}")
            except json.JSONDecodeError:
                print("\n  索引: 损坏，请执行 reindex")
    else:
        print("\n  索引: 未创建，请执行 reindex")


def cmd_cleanup(days=30):
    """清理过期记忆"""
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff.isoformat()
    removed_total = 0

    # 只清理已解决的错误和已过时标记的知识盲区
    cleanup_rules = {
        "errors": lambda e: e.get("status") == "resolved" and e.get("timestamp", "") < cutoff_str,
        "knowledge_gaps": lambda e: e.get("status") == "archived" and e.get("timestamp", "") < cutoff_str,
    }

    for name, should_remove in cleanup_rules.items():
        fname = FILES[name]
        entries = load_entries(fname)
        before = len(entries)
        entries = [e for e in entries if not should_remove(e)]
        after = len(entries)
        removed = before - after
        if removed > 0:
            save_entries(fname, entries)
            print(f"  {name}: 清理 {removed} 条")
            removed_total += removed

    if removed_total == 0:
        print(f"  无需清理（{days}天内无过期记忆）")
    else:
        print(f"\n  共清理 {removed_total} 条")

    # 注意：corrections 和 best_practices 永不自动清理
    print("  (纠正记录和最佳实践永久保留，需手动删除)")


def cmd_deduplicate():
    """合并重复记忆"""
    dedup_rules = {
        "errors": ["command", "error"],
        "corrections": ["topic", "wrong"],
        "best_practices": ["category", "practice"],
        "knowledge_gaps": ["topic", "outdated"],
    }

    total_removed = 0

    for name, match_fields in dedup_rules.items():
        fname = FILES[name]
        entries = load_entries(fname)
        if not entries:
            continue

        seen = {}
        unique = []
        removed = 0

        for entry in entries:
            key = tuple(entry.get(f, "") for f in match_fields)
            if key in seen:
                # 合并：保留较新的，但合并count等字段
                existing = seen[key]
                existing["timestamp"] = max(existing.get("timestamp", ""), entry.get("timestamp", ""))
                if "count" in entry:
                    existing["count"] = max(existing.get("count", 1), entry.get("count", 1))
                if entry.get("fix") and not existing.get("fix"):
                    existing["fix"] = entry["fix"]
                    existing["status"] = "resolved"
                removed += 1
            else:
                seen[key] = entry
                unique.append(entry)

        if removed > 0:
            save_entries(fname, unique)
            print(f"  {name}: 合并 {removed} 条重复")
            total_removed += removed

    if total_removed == 0:
        print("  无重复记忆")
    else:
        print(f"\n  共合并 {total_removed} 条")


def cmd_reindex():
    """重建索引"""
    import re
    ensure_dir()
    index = {"keywords": {}, "counts": {}, "last_updated": datetime.now().isoformat()}

    for name, fname in FILES.items():
        entries = load_entries(fname)
        index["counts"][name] = len(entries)

        for entry in entries:
            # 提取所有文本字段的关键词
            text_parts = []
            for k, v in entry.items():
                if isinstance(v, str) and k not in ("type", "timestamp", "first_seen", "status", "priority"):
                    text_parts.append(v)

            full_text = " ".join(text_parts)
            # 英文词
            words = set(re.findall(r"[a-zA-Z0-9_\-\.]{2,}", full_text.lower()))
            # 中文词（bigram）
            cn_chars = re.findall(r"[\u4e00-\u9fff]", full_text)
            for i in range(len(cn_chars) - 1):
                words.add(cn_chars[i] + cn_chars[i + 1])

            for w in words:
                if w not in index["keywords"]:
                    index["keywords"][w] = []
                if name not in index["keywords"][w]:
                    index["keywords"][w].append(name)

    index_path = get_filepath("index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    kw_count = len(index["keywords"])
    total = sum(index["counts"].values())
    print(f"  索引重建完成: {total} 条记忆, {kw_count} 个关键词")


def cmd_export(output_path=None):
    """导出所有记忆为单个JSON文件"""
    data = {
        "exported_at": datetime.now().isoformat(),
        "memories": {},
    }
    for name, fname in FILES.items():
        data["memories"][name] = load_entries(fname)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  已导出到: {output_path}")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_search(keyword):
    """在所有记忆中搜索关键词"""
    keyword_lower = keyword.lower()
    results = []

    for name, fname in FILES.items():
        entries = load_entries(fname)
        for entry in entries:
            text = json.dumps(entry, ensure_ascii=False).lower()
            if keyword_lower in text:
                results.append((name, entry))

    if results:
        print(f"找到 {len(results)} 条包含 '{keyword}' 的记忆:\n")
        for name, entry in results[:20]:
            ts = entry.get("timestamp", "")[:10]
            # 显示第一个有意义的文本字段
            preview = ""
            for k in ["command", "topic", "practice", "error"]:
                if entry.get(k):
                    preview = f"{k}: {entry[k][:50]}"
                    break
            print(f"  [{name}] {ts}  {preview}")
    else:
        print(f"未找到包含 '{keyword}' 的记忆")


def main():
    parser = argparse.ArgumentParser(description="记忆管理工具")
    subparsers = parser.add_subparsers(dest="action", help="操作")

    subparsers.add_parser("stats", help="显示统计信息")

    p_cleanup = subparsers.add_parser("cleanup", help="清理过期记忆")
    p_cleanup.add_argument("--days", type=int, default=30, help="清理多少天前的已解决记忆")

    subparsers.add_parser("deduplicate", help="合并重复记忆")
    subparsers.add_parser("reindex", help="重建索引")

    p_export = subparsers.add_parser("export", help="导出所有记忆")
    p_export.add_argument("--output", "-o", default=None, help="输出文件路径")

    p_search = subparsers.add_parser("search", help="搜索记忆")
    p_search.add_argument("keyword", help="搜索关键词")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    actions = {
        "stats": lambda: cmd_stats(),
        "cleanup": lambda: cmd_cleanup(args.days),
        "deduplicate": lambda: cmd_deduplicate(),
        "reindex": lambda: cmd_reindex(),
        "export": lambda: cmd_export(getattr(args, "output", None)),
        "search": lambda: cmd_search(args.keyword),
    }

    actions[args.action]()


if __name__ == "__main__":
    main()
