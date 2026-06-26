"""cashbook 公共数据库模块"""

import os
import sqlite3

_initialized = False


def get_db_path():
    """返回数据库路径，优先读环境变量 CASHBOOK_DB"""
    return os.environ.get("CASHBOOK_DB",
                          os.path.expanduser("~/.local/share/cashbook/cashbook.db"))


def _auto_init(conn):
    """首次连接时自动建表+预置数据，跳过已有数据库"""
    global _initialized
    if _initialized:
        return
    _initialized = True

    # 检查是否已初始化（categories 表有数据）
    try:
        row = conn.execute("SELECT COUNT(*) FROM categories").fetchone()
        if row and row[0] > 0:
            return
    except sqlite3.OperationalError:
        pass  # 表不存在，继续初始化

    from init import TABLES_SQL, PRESET_CATEGORIES, DEFAULT_CONFIG

    conn.executescript(TABLES_SQL)
    for name, ctype, icon in PRESET_CATEGORIES:
        conn.execute(
            "INSERT OR IGNORE INTO categories (name, type, icon, builtin) "
            "VALUES (?, ?, ?, 1)",
            (name, ctype, icon),
        )
    for key, value in DEFAULT_CONFIG.items():
        conn.execute(
            "INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)",
            (key, value),
        )
    conn.commit()


def get_conn():
    """返回 sqlite3 connection，首次调用自动初始化"""
    path = get_db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    _auto_init(conn)
    return conn
