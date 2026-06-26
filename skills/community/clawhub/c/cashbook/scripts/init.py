#!/usr/bin/env python3
"""cashbook 数据库初始化"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_db_path, get_conn

TABLES_SQL = """
CREATE TABLE IF NOT EXISTS accounts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nickname    TEXT NOT NULL,
    type        TEXT NOT NULL,
    last4       TEXT,
    currency    TEXT DEFAULT 'CNY',
    balance     REAL DEFAULT 0,
    created_at  TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS categories (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    type      TEXT NOT NULL,
    icon      TEXT,
    builtin   INTEGER DEFAULT 0,
    UNIQUE(name, type)
);

CREATE TABLE IF NOT EXISTS transactions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    amount       REAL NOT NULL,
    type         TEXT NOT NULL,
    category_id  INTEGER REFERENCES categories(id),
    account_id   INTEGER REFERENCES accounts(id),
    note         TEXT,
    merchant     TEXT,
    date         TEXT NOT NULL,
    created_at   TEXT DEFAULT (datetime('now','localtime')),
    source       TEXT DEFAULT 'manual'
);

CREATE TABLE IF NOT EXISTS budgets (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER REFERENCES categories(id),
    amount      REAL NOT NULL,
    period      TEXT NOT NULL,
    active      INTEGER DEFAULT 1,
    created_at  TEXT DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS config (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""

PRESET_CATEGORIES = [
    # (name, type, icon)
    ("餐饮", "expense", "🍜"),
    ("交通", "expense", "🚗"),
    ("购物", "expense", "🛒"),
    ("娱乐", "expense", "🎮"),
    ("医疗", "expense", "💊"),
    ("住房", "expense", "🏠"),
    ("教育", "expense", "📚"),
    ("旅行", "expense", "✈️"),
    ("其他", "expense", "📦"),
    ("工资", "income", "💰"),
    ("奖金", "income", "🎁"),
    ("副业", "income", "💼"),
    ("其他", "income", "📥"),
]

DEFAULT_CONFIG = {
    "currency": "CNY",
    "timezone": "Asia/Shanghai",
    "db_version": "1",
}


def init_db(force=False):
    db_path = get_db_path()

    if force and os.path.exists(db_path):
        os.remove(db_path)
        print(f"已删除旧数据库：{db_path}")

    conn = get_conn()
    cur = conn.cursor()

    # 建表
    cur.executescript(TABLES_SQL)

    # 插入预置分类（跳过已存在的）
    for name, ctype, icon in PRESET_CATEGORIES:
        cur.execute(
            "INSERT OR IGNORE INTO categories (name, type, icon, builtin) "
            "VALUES (?, ?, ?, 1)",
            (name, ctype, icon),
        )

    # 写入默认配置（跳过已存在的）
    for key, value in DEFAULT_CONFIG.items():
        cur.execute(
            "INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)",
            (key, value),
        )

    conn.commit()
    conn.close()
    print(f"✅ 数据库初始化成功：{db_path}")


def main():
    parser = argparse.ArgumentParser(description="初始化 cashbook 数据库")
    parser.add_argument("--force", action="store_true", help="删除并重建数据库")
    args = parser.parse_args()
    init_db(force=args.force)


if __name__ == "__main__":
    main()
