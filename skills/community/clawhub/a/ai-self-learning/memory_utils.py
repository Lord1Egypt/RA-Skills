#!/usr/bin/env python3
"""
Self-Improving Agent - 共享工具函数
提供记忆存储、去重、索引管理等公共能力
"""

import json
import os
from datetime import datetime

MEMORY_DIR = os.path.expanduser("~/.openclaw/memory/self-improving")


def ensure_dir():
    os.makedirs(MEMORY_DIR, exist_ok=True)


def get_filepath(filename):
    return os.path.join(MEMORY_DIR, filename)


def load_entries(filename):
    """加载JSONL文件的所有条目"""
    filepath = get_filepath(filename)
    if not os.path.exists(filepath):
        return []
    entries = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return entries


def save_entries(filename, entries):
    """将所有条目写回JSONL文件"""
    ensure_dir()
    filepath = get_filepath(filename)
    with open(filepath, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def append_entry(filename, entry):
    """追加单条记忆"""
    ensure_dir()
    filepath = get_filepath(filename)
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def upsert_entry(filename, entry, match_fields):
    """插入或更新记忆。如果match_fields指定的字段值都相同，则更新而非追加。
    返回 (is_new, entry)。
    """
    entries = load_entries(filename)

    for i, existing in enumerate(entries):
        if all(existing.get(f) == entry.get(f) for f in match_fields):
            # 合并：保留旧条目的某些字段，用新条目覆盖
            merged = {**existing, **entry}
            # 保留首次记录时间
            if "first_seen" in existing:
                merged["first_seen"] = existing["first_seen"]
            else:
                merged["first_seen"] = existing.get("timestamp", entry["timestamp"])
            entries[i] = merged
            save_entries(filename, entries)
            return False, merged

    # 新条目
    entry["first_seen"] = entry["timestamp"]
    entries.append(entry)
    save_entries(filename, entries)
    return True, entry


def update_index(entry_type, keywords):
    """更新快速索引"""
    ensure_dir()
    index_path = get_filepath("index.json")

    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            try:
                index = json.load(f)
            except json.JSONDecodeError:
                index = {}
    else:
        index = {}

    if "keywords" not in index:
        index["keywords"] = {}

    for kw in keywords:
        kw = kw.lower().strip()
        if not kw:
            continue
        if kw not in index["keywords"]:
            index["keywords"][kw] = []
        if entry_type not in index["keywords"][kw]:
            index["keywords"][kw].append(entry_type)

    index["last_updated"] = datetime.now().isoformat()
    index["counts"] = {}
    for fname_key, fname in [("errors", "errors.jsonl"), ("corrections", "corrections.jsonl"),
                              ("best_practices", "best_practices.jsonl"),
                              ("knowledge_gaps", "knowledge_gaps.jsonl")]:
        index["counts"][fname_key] = len(load_entries(fname))

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
