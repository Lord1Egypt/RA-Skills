#!/usr/bin/env python3
"""
更新项目字段，含状态机合法性验证。

用法：
    python3 scripts/update_project.py --id 1 --field status --value doc_purchased
    python3 scripts/update_project.py --id 1 --field actual_seal_time --value "2026-04-08T15:00:00"

状态流转（合法路径）：
    registered → doc_pending / doc_purchased / cancelled
    doc_pending → doc_purchased / cancelled
    doc_purchased → preparing / sealed / cancelled
    preparing → sealed / cancelled
    sealed → opened / cancelled
    opened → won / lost
    任意终态（won/lost/cancelled）不可流转
"""

import argparse
import json
import os
import sqlite3
import sys

from milb_tracker.config import get_db_path

DB_PATH = get_db_path()


def get_conn():
    conn = sqlite3.connect(os.path.abspath(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# 合法的状态流转路径（按 api-interfaces.md §5 修复）
VALID_TRANSITIONS = {
    'registered':    {'doc_pending', 'doc_purchased', 'cancelled'},
    'doc_pending':   {'doc_purchased', 'cancelled'},
    'doc_purchased': {'preparing', 'sealed', 'cancelled'},
    'preparing':     {'sealed', 'cancelled'},
    'sealed':        {'opened', 'cancelled'},
    'opened':        {'won', 'lost'},
    'won':           set(),
    'lost':          set(),
    'cancelled':     set(),
}

# 允许通过此脚本更新的字段白名单（防止字段名 SQL 注入）
UPDATABLE_FIELDS = {
    'status', 'doc_purchased_at', 'doc_attachment_path',
    'actual_seal_time', 'project_manager', 'manager_contact',
    'bid_opening_time', 'bid_opening_location', 'suggested_seal_time',
    'announcement_path',
}


def validate_status_transition(current: str, new: str) -> bool:
    """验证状态流转是否合法。"""
    return new in VALID_TRANSITIONS.get(current, set())


def update(project_id: int, field: str, value: str):
    """更新指定项目的指定字段。"""
    if field not in UPDATABLE_FIELDS:
        print(json.dumps({"error": f"不支持更新字段：{field}", "code": 1}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    conn = get_conn()
    try:
        row = conn.execute(
            "SELECT status FROM projects WHERE id=?", (project_id,)).fetchone()
        if row is None:
            print(json.dumps({"error": f"项目不存在：{project_id}", "code": 1}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        if field == 'status':
            current_status = row[0]
            if not validate_status_transition(current_status, value):
                print(json.dumps({"error": f"非法状态流转：{current_status} → {value}", "code": 1}, ensure_ascii=False), file=sys.stderr)
                sys.exit(1)
            # 自动记录封标时间
            if value == 'sealed':
                conn.execute(
                    "UPDATE projects SET actual_seal_time=datetime('now','localtime') WHERE id=?",
                    (project_id,))

        conn.execute(
            f"UPDATE projects SET {field}=?, updated_at=datetime('now','localtime')"
            f" WHERE id=?",
            (value, project_id))
        conn.commit()
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='更新项目字段')
    parser.add_argument('--id', type=int, required=True, help='项目 ID')
    parser.add_argument('--field', required=True, help='要更新的字段名')
    parser.add_argument('--value', required=True, help='新值')
    args = parser.parse_args()

    update(args.id, args.field, args.value)
    print(json.dumps({"status": "ok", "message": f"项目 {args.id} 的 {args.field} 已更新为：{args.value}"}, ensure_ascii=False))
    sys.exit(0)


if __name__ == '__main__':
    main()
