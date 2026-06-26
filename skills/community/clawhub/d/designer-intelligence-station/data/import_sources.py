#!/usr/bin/env python3
"""
设计师情报站 - 信息源导入脚本

使用方法:
    python import_sources.py              # 从 default_sources.json 导入
    python import_sources.py sources_export.json  # 从指定文件导入
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "intelligence_sources.db"
DEFAULT_SOURCES = Path(__file__).parent / "default_sources.json"

def import_sources(source_file=None):
    if source_file is None:
        if not DEFAULT_SOURCES.exists():
            print(f"错误：找不到 {DEFAULT_SOURCES}")
            return
        source_file = DEFAULT_SOURCES
    
    print(f"从 {source_file} 导入...")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        sources = json.load(f)
    
    # 初始化数据库
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            type TEXT NOT NULL,
            domain TEXT NOT NULL,
            priority TEXT DEFAULT '中',
            status TEXT DEFAULT 'enabled',
            update_frequency TEXT DEFAULT '日更',
            notes TEXT,
            created_at TEXT,
            updated_at TEXT,
            fetch_method TEXT DEFAULT 'web',
            category TEXT DEFAULT '媒体'
        )
    """)
    
    # 导入数据
    now = datetime.now().isoformat()
    stats = {"added": 0, "updated": 0, "failed": 0}
    
    for s in sources:
        try:
            # 检查是否存在
            cursor.execute("SELECT id FROM sources WHERE id = ?", (s["id"],))
            exists = cursor.fetchone()
            
            if exists:
                # 更新
                cursor.execute("""
                    UPDATE sources SET
                        name = ?, url = ?, type = ?, domain = ?,
                        priority = ?, status = ?, update_frequency = ?,
                        notes = ?, fetch_method = ?, category = ?,
                        updated_at = ?
                    WHERE id = ?
                """, (
                    s.get("name", ""), s.get("url", ""), 
                    s.get("type", s.get("category", "媒体")),
                    s.get("domain", ""), s.get("priority", "中"),
                    s.get("status", "enabled"), s.get("update_frequency", "日更"),
                    s.get("notes", ""), s.get("fetch_method", "web"),
                    s.get("category", "媒体"), now, s["id"]
                ))
                stats["updated"] += 1
            else:
                # 插入
                cursor.execute("""
                    INSERT INTO sources (
                        id, name, url, type, domain, priority, status,
                        update_frequency, notes, created_at, updated_at,
                        fetch_method, category
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    s["id"], s.get("name", ""), s.get("url", ""),
                    s.get("type", s.get("category", "媒体")),
                    s.get("domain", ""), s.get("priority", "中"),
                    s.get("status", "enabled"), s.get("update_frequency", "日更"),
                    s.get("notes", ""), now, now,
                    s.get("fetch_method", "web"), s.get("category", "媒体")
                ))
                stats["added"] += 1
        except Exception as e:
            print(f"  ✗ {s.get('id', 'unknown')}: {e}")
            stats["failed"] += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ 导入完成!")
    print(f"   新增：{stats['added']} 条")
    print(f"   更新：{stats['updated']} 条")
    print(f"   失败：{stats['failed']} 条")
    print(f"   总计：{stats['added'] + stats['updated'] + stats['failed']} 条")

if __name__ == '__main__':
    import sys
    source_file = sys.argv[1] if len(sys.argv) > 1 else None
    import_sources(source_file)
