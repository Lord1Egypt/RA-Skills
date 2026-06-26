#!/usr/bin/env python3
"""
seed-facts-db.py — 初始化 facts.db 结构化知识图谱

从 ARCHIVE.md / MEMORY.md 提取可结构化信息（版本号、端口、地址、哈希等）
写入 facts.db，为精确查找和 activation/decay 提供基础设施。

用法:
  python3 seed-facts-db.py [--dry-run]

Schema:
  facts(entity, key, value, category, source, permanent)
  aliases(alias, entity)
"""

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path.home() / ".openclaw" / "workspace"
FACTS_DB = Path.home() / ".openclaw" / "memory" / "facts.sqlite"
ARCHIVE_MD = WORKSPACE / "ARCHIVE.md"
MEMORY_MD = WORKSPACE / "MEMORY.md"


def init_schema(conn: sqlite3.Connection):
    """创建 facts.db 表结构"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entity TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            category TEXT NOT NULL,
            source TEXT,
            permanent BOOLEAN DEFAULT 0,
            activation REAL DEFAULT 0.5,
            access_count INTEGER DEFAULT 0,
            last_accessed TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            UNIQUE(entity, key)
        );

        CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
            entity, key, value, content=facts, content_rowid=id
        );

        CREATE TABLE IF NOT EXISTS aliases (
            alias TEXT NOT NULL,
            entity TEXT NOT NULL,
            PRIMARY KEY (alias, entity)
        );

        CREATE TABLE IF NOT EXISTS seed_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seeded_at TEXT DEFAULT (datetime('now')),
            entities_count INTEGER,
            facts_count INTEGER,
            source_file TEXT
        );
    """)
    conn.commit()


def extract_from_archive() -> list:
    """从 ARCHIVE.md 提取可结构化事实"""
    facts = []
    try:
        content = ARCHIVE_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        return facts

    # ── 模式匹配规则 ────────────────────────────────────────────────────────

    # 表格行: | 名称 | 值 |
    for m in re.finditer(r"\|\s*(.+?)\s*\|\s*(.+?)\s*\|", content):
        key_raw = m.group(1).strip()
        val_raw = m.group(2).strip()
        if key_raw in ("项", "值", "类型", "字段", "---", "----", ""):
            continue
        if len(val_raw) > 200:
            continue
        # 确定 entity 上下文
        entity = "system"
        before = content[:m.start()]
        last_section = re.findall(r"^## (.+)", before, re.MULTILINE)
        if last_section:
            section = last_section[-1]
            if "Emby" in section:
                entity = "Emby"
            elif "iStoreOS" in section or "设备" in section:
                entity = "iStoreOS"
            elif "哈希" in section:
                entity = "security"
            elif "人际关系" in section:
                entity = "Victor"
        facts.append({
            "entity": entity,
            "key": key_raw,
            "value": val_raw,
            "category": "配置" if entity != "Victor" else "个人信息",
            "source": f"ARCHIVE.md (table)",
            "permanent": "哈希" in (last_section[-1] if last_section else ""),
        })

    # 特定模式: **key**: value
    for m in re.finditer(r"\*\*(.+?)\*\*:\s*(.+)", content):
        key = m.group(1).strip()
        value = m.group(2).strip()
        if len(value) > 150:
            continue
        before = content[:m.start()]
        last_section = re.findall(r"^## (.+)", before, re.MULTILINE)
        entity = "system"
        if last_section:
            section = last_section[-1]
            if any(w in section for w in ["Emby", "设备", "iStoreOS"]):
                entity = "设备"
            elif "人际关系" in section or "USER" in section:
                entity = "Victor"
        if entity == "system" and any(w in key for w in ["姓名", "年龄", "职业", "血型"]):
            entity = "Victor"
        facts.append({
            "entity": entity,
            "key": key,
            "value": value,
            "category": "个人信息" if entity == "Victor" else "配置",
            "source": "ARCHIVE.md",
            "permanent": False,
        })

    # IP/URL 模式
    for m in re.finditer(r"(https?://[^\s\)]+|192\.168\.\d+\.\d+)", content):
        val = m.group(1)
        before = content[:m.start()]
        last_section = re.findall(r"^## (.+)", before, re.MULTILINE)
        entity = "network"
        if last_section:
            section = last_section[-1]
            if "Emby" in section:
                entity = "Emby"
            elif "设备" in section or "iStoreOS" in section:
                entity = "iStoreOS"
        key = "url" if val.startswith("http") else "ip"
        facts.append({
            "entity": entity,
            "key": key,
            "value": val,
            "category": "网络",
            "source": "ARCHIVE.md",
            "permanent": True,
        })

    return facts


def seed_aliases(conn: sqlite3.Connection):
    """写入别名映射"""
    aliases = [
        # 人物
        ("维克多", "Victor"), ("victor", "Victor"),
        ("软路由", "iStoreOS"), ("istoreos", "iStoreOS"), ("路由器", "iStoreOS"),
        ("nas", "NAS_E"), ("NAS", "NAS_E"),
        ("小爱", "卧室小爱音箱"), ("小爱同学", "卧室小爱音箱"),
        ("emby", "Emby"), ("Emby服务器", "Emby"),
        ("workspace", "/home/victor/.openclaw/workspace"),
        ("memory-hub", "anamnesis-hub"), ("hub", "anamnesis-hub"),
    ]
    for alias, entity in aliases:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO aliases (alias, entity) VALUES (?, ?)",
                (alias, entity),
            )
        except Exception:
            pass
    conn.commit()


def upsert_facts(conn: sqlite3.Connection, facts: list) -> int:
    """写入或更新事实，返回新增数量"""
    count = 0
    for f in facts:
        try:
            conn.execute("""
                INSERT INTO facts (entity, key, value, category, source, permanent)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(entity, key) DO UPDATE SET
                    value = excluded.value,
                    source = excluded.source,
                    last_accessed = datetime('now')
            """, (f["entity"], f["key"], f["value"], f["category"],
                  f.get("source", ""), f.get("permanent", False)))
            count += 1
        except Exception as e:
            print(f"  ⚠️ skip: {f.get('entity')}.{f.get('key')}: {e}", file=sys.stderr)
    conn.commit()
    return count


def main():
    parser = argparse.ArgumentParser(description="facts.db seed script")
    parser.add_argument("--dry-run", action="store_true", help="预览不写入")
    args = parser.parse_args()

    print(f"📊 facts.db seed — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   数据库: {FACTS_DB}")

    conn = sqlite3.connect(str(FACTS_DB))
    init_schema(conn)

    # 从 ARCHIVE.md 提取
    facts = extract_from_archive()
    print(f"   从 ARCHIVE.md 提取: {len(facts)} 条候选事实")

    if args.dry_run:
        print("\n   [dry-run] 预览 (前20条):")
        for f in facts[:20]:
            print(f"   {f['entity']}.{f['key']} = {f['value'][:60]}")
        conn.close()
        return 0

    # 写入
    added = upsert_facts(conn, facts)
    seed_aliases(conn)

    # 日志
    conn.execute("""
        INSERT INTO seed_log (entities_count, facts_count, source_file)
        VALUES (?, ?, ?)
    """, (len(set(f["entity"] for f in facts)), added, "ARCHIVE.md"))
    conn.commit()

    # 统计
    total = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
    entities = conn.execute("SELECT COUNT(DISTINCT entity) FROM facts").fetchone()[0]
    aliases = conn.execute("SELECT COUNT(*) FROM aliases").fetchone()[0]

    print(f"   写入: {added} 条")
    print(f"   总计: {total} 条事实 / {entities} 个实体 / {aliases} 个别名")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
