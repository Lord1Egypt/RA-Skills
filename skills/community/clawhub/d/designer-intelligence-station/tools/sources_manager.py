#!/usr/bin/env python3
"""
设计师情报站 - 信息源数据库管理工具

功能：
- 信息源增删改查
- 批量导入/导出
- 状态管理（启用/禁用）
- 按优先级/领域筛选

使用方式:
    python sources_manager.py list          # 列出所有信息源
    python sources_manager.py add <url>     # 添加信息源
    python sources_manager.py disable <id>  # 禁用信息源
    python sources_manager.py export        # 导出为 JSON
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

# 数据库路径（workspace 根目录）
DB_PATH = Path(__file__).parent.parent / "data" / "intelligence_sources.db"
DEFAULT_SOURCES_FILE = Path(__file__).parent.parent / "data" / "default_sources.json"


def init_db():
    """初始化数据库，创建表结构"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
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
            updated_at TEXT
        )
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_domain ON sources(domain)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_status ON sources(status)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_priority ON sources(priority)
    """)
    
    conn.commit()
    conn.close()


def get_connection():
    """获取数据库连接"""
    if not DB_PATH.exists():
        init_db()
    return sqlite3.connect(DB_PATH)


def add_source(
    id: str,
    name: str,
    url: str,
    type: str,
    domain: str,
    priority: str = "中",
    status: str = "enabled",
    update_frequency: str = "日更",
    notes: str = "",
) -> bool:
    """添加信息源"""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    try:
        cursor.execute("""
            INSERT INTO sources (id, name, url, type, domain, priority, status, update_frequency, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (id, name, url, type, domain, priority, status, update_frequency, notes, now, now))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"错误：信息源 ID '{id}' 已存在")
        return False
    finally:
        conn.close()


def update_source(
    id: str,
    name: Optional[str] = None,
    url: Optional[str] = None,
    priority: Optional[str] = None,
    status: Optional[str] = None,
    notes: Optional[str] = None,
) -> bool:
    """更新信息源"""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)
    if url is not None:
        updates.append("url = ?")
        values.append(url)
    if priority is not None:
        updates.append("priority = ?")
        values.append(priority)
    if status is not None:
        updates.append("status = ?")
        values.append(status)
    if notes is not None:
        updates.append("notes = ?")
        values.append(notes)
    
    if not updates:
        print("警告：没有提供任何更新内容")
        conn.close()
        return False
    
    updates.append("updated_at = ?")
    values.append(now)
    values.append(id)
    
    cursor.execute(f"""
        UPDATE sources SET {', '.join(updates)} WHERE id = ?
    """, values)
    
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    
    if affected == 0:
        print(f"错误：未找到信息源 ID '{id}'")
        return False
    
    return True


def disable_source(id: str) -> bool:
    """禁用信息源"""
    return update_source(id, status="disabled")


def enable_source(id: str) -> bool:
    """启用信息源"""
    return update_source(id, status="enabled")


def delete_source(id: str) -> bool:
    """删除信息源"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM sources WHERE id = ?", (id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    
    return affected > 0


def get_source(id: str) -> Optional[dict]:
    """获取单个信息源"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sources WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def list_sources(
    domain: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    type: Optional[str] = None,
) -> list[dict]:
    """列出信息源（支持筛选）"""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    conditions = []
    values = []
    
    if domain:
        conditions.append("domain = ?")
        values.append(domain)
    if status:
        conditions.append("status = ?")
        values.append(status)
    if priority:
        conditions.append("priority = ?")
        values.append(priority)
    if type:
        conditions.append("type = ?")
        values.append(type)
    
    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    
    cursor.execute(f"""
        SELECT * FROM sources {where_clause}
        ORDER BY 
            CASE priority WHEN '高' THEN 1 WHEN '中' THEN 2 WHEN '低' THEN 3 END,
            id
    """, values)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_enabled_sources() -> list[dict]:
    """获取所有启用的信息源（按优先级排序）"""
    return list_sources(status="enabled")


def export_sources(format: str = "json") -> str:
    """导出信息源"""
    sources = list_sources()
    
    if format == "json":
        return json.dumps(sources, ensure_ascii=False, indent=2)
    else:
        raise ValueError(f"不支持的导出格式：{format}")


def import_sources(sources: list[dict], skip_existing: bool = True) -> dict:
    """
    批量导入信息源
    
    返回：{"added": int, "skipped": int, "failed": int}
    """
    stats = {"added": 0, "skipped": 0, "failed": 0}
    
    for source in sources:
        try:
            success = add_source(
                id=source["id"],
                name=source["name"],
                url=source["url"],
                type=source["type"],
                domain=source["domain"],
                priority=source.get("priority", "中"),
                status=source.get("status", "enabled"),
                update_frequency=source.get("update_frequency", "日更"),
                notes=source.get("notes", ""),
            )
            if success:
                stats["added"] += 1
            else:
                stats["skipped"] += 1
        except Exception as e:
            print(f"导入失败 {source.get('id', 'unknown')}: {e}")
            stats["failed"] += 1
    
    return stats


def load_default_sources():
    """从默认文件加载初始数据"""
    if not DEFAULT_SOURCES_FILE.exists():
        print(f"默认文件不存在：{DEFAULT_SOURCES_FILE}")
        return
    
    with open(DEFAULT_SOURCES_FILE, "r", encoding="utf-8") as f:
        sources = json.load(f)
    
    stats = import_sources(sources)
    print(f"导入完成：{stats}")


# CLI 入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_db()
        print("数据库初始化完成")
    
    elif command == "list":
        domain = sys.argv[2] if len(sys.argv) > 2 else None
        method = sys.argv[3] if len(sys.argv) > 3 else None
        sources = list_sources(domain=domain)
        
        # 按抓取方式筛选
        if method:
            sources = [s for s in sources if s.get('fetch_method') == method]
        
        print(f"共 {len(sources)} 个信息源:\n")
        
        # 按抓取方式分组显示
        from itertools import groupby
        sorted_sources = sorted(sources, key=lambda x: x.get('fetch_method', 'web'))
        
        for method, group in groupby(sorted_sources, key=lambda x: x.get('fetch_method', 'web')):
            method_name = {'web': 'Web 抓取', 'rss': 'RSS', 'api': 'API'}.get(method, method)
            print(f"\n📌 {method_name}:")
            for s in group:
                status_icon = "✅" if s["status"] == "enabled" else "❌"
                category = s.get('category', '媒体')
                print(f"  {status_icon} [{s['id']}] {s['name']} ({category}/{s['domain']}/{s['priority']})")
                print(f"      {s['url']}")
    
    elif command == "add":
        if len(sys.argv) < 4:
            print("用法：python sources_manager.py add <id> <name> <url> <type> <domain>")
            sys.exit(1)
        success = add_source(
            id=sys.argv[2],
            name=sys.argv[3],
            url=sys.argv[4],
            type=sys.argv[5] if len(sys.argv) > 5 else "中文媒体",
            domain=sys.argv[6] if len(sys.argv) > 6 else "AI",
        )
        print("添加成功" if success else "添加失败")
    
    elif command == "disable":
        if len(sys.argv) < 3:
            print("用法：python sources_manager.py disable <id>")
            sys.exit(1)
        success = disable_source(sys.argv[2])
        print("禁用成功" if success else "禁用失败")
    
    elif command == "enable":
        if len(sys.argv) < 3:
            print("用法：python sources_manager.py enable <id>")
            sys.exit(1)
        success = enable_source(sys.argv[2])
        print("启用成功" if success else "启用失败")
    
    elif command == "export":
        print(export_sources())
    
    elif command == "import":
        if len(sys.argv) < 3:
            print("用法：python sources_manager.py import <json_file>")
            sys.exit(1)
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            sources = json.load(f)
        stats = import_sources(sources)
        print(f"导入完成：{stats}")
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
