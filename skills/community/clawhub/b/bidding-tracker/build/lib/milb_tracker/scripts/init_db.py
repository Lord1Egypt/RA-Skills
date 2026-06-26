#!/usr/bin/env python3
"""
初始化 SQLite 数据库，创建所有表结构。
幂等运行：多次执行安全，不会重复建表或丢失数据。

用法：python3 scripts/init_db.py
"""

import json
import sqlite3
import os
import sys

from milb_tracker.config import get_db_path, get_attachments_dir

DB_PATH = get_db_path()
ATTACHMENTS_DIR = get_attachments_dir()


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(os.path.abspath(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


DDL = """
CREATE TABLE IF NOT EXISTS projects (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    project_no              TEXT NOT NULL UNIQUE,
    project_name            TEXT NOT NULL,
    budget                  REAL,
    procurer                TEXT,
    bid_agency              TEXT,
    project_manager         TEXT,
    manager_contact         TEXT,
    registration_deadline   TEXT,
    registration_location   TEXT,
    doc_purchase_location   TEXT,
    doc_purchase_price      REAL,
    doc_purchase_deadline   TEXT,
    doc_required_materials  TEXT,
    doc_purchased_at        TEXT,
    doc_attachment_path     TEXT,
    bid_opening_time        TEXT,
    bid_opening_location    TEXT,
    travel_days             INTEGER DEFAULT 0,
    suggested_seal_time     TEXT,
    actual_seal_time        TEXT,
    announcement_path       TEXT,
    status                  TEXT NOT NULL DEFAULT 'registered',
    created_at              TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at              TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS bid_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      INTEGER NOT NULL REFERENCES projects(id),
    our_bid_price   REAL,
    winning_price   REAL,
    winner          TEXT,
    is_winner       INTEGER NOT NULL DEFAULT 0,
    notes           TEXT,
    recorded_at     TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS reminders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id      INTEGER NOT NULL REFERENCES projects(id),
    reminder_type   TEXT NOT NULL,
    sent_at         TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    recipient_role  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    wecom_userid    TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    role            TEXT NOT NULL,
    contact         TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);
"""


def main():
    try:
        os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
        db_path = os.path.abspath(DB_PATH)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = get_conn()
        conn.executescript(DDL)
        conn.commit()
        conn.close()

        print(f"数据库初始化完成：{db_path}")
    except Exception as e:
        print(json.dumps({"error": f"数据库初始化失败: {e}", "code": 1}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
