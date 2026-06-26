#!/usr/bin/env python3
"""
用户管理：Bootstrap 注册总监、添加负责人、列出用户。

用法：
    python3 scripts/manage_users.py --bootstrap --user-id <id> --name <name>
    python3 scripts/manage_users.py --add --caller-id <director_id> --user-id <id> --name <name> [--contact <c>]
    python3 scripts/manage_users.py --list [--role <role>]
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
    conn.row_factory = sqlite3.Row
    return conn


def cmd_bootstrap(user_id: str, name: str):
    """Bootstrap 模式：注册首位总监。幂等，同 userid 返回 ok；不同 userid 且已有总监则报错。"""
    conn = get_conn()
    try:
        cur = conn.execute("SELECT * FROM users WHERE role = 'director'")
        existing = cur.fetchone()

        if existing:
            if existing['wecom_userid'] == user_id:
                print(json.dumps({"status": "ok", "message": f"总监已存在：{existing['name']}"}))
                sys.exit(0)
            else:
                print(json.dumps({"error": "系统已初始化，总监已存在且非当前用户", "code": 1}, ensure_ascii=False), file=sys.stderr)
                sys.exit(1)

        conn.execute(
            "INSERT INTO users (wecom_userid, name, role) VALUES (?, ?, 'director')",
            (user_id, name))
        conn.commit()
        print(json.dumps({"status": "ok", "message": f"总监注册成功：{name}"}))
        sys.exit(0)
    finally:
        conn.close()


def cmd_add(caller_id: str, user_id: str, name: str, contact: str | None):
    """添加负责人：验证 caller 是总监，再插入。"""
    conn = get_conn()
    try:
        cur = conn.execute("SELECT role FROM users WHERE wecom_userid = ?", (caller_id,))
        caller_row = cur.fetchone()

        if not caller_row or caller_row['role'] != 'director':
            print(json.dumps({"error": "权限不足：仅总监可添加用户", "code": 1}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        cur2 = conn.execute("SELECT id FROM users WHERE wecom_userid = ?", (user_id,))
        if cur2.fetchone():
            print(json.dumps({"error": f"用户 {user_id} 已存在", "code": 1}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        conn.execute(
            "INSERT INTO users (wecom_userid, name, role, contact) VALUES (?, ?, 'manager', ?)",
            (user_id, name, contact))
        conn.commit()
        print(json.dumps({"status": "ok", "message": f"用户添加成功：{name} (manager)"}))
        sys.exit(0)
    finally:
        conn.close()


def cmd_list(role: str | None):
    """列出用户，可选按 role 过滤。"""
    conn = get_conn()
    try:
        if role:
            cur = conn.execute(
                "SELECT id, wecom_userid, name, role, contact, created_at "
                "FROM users WHERE role = ? ORDER BY id",
                (role,))
        else:
            cur = conn.execute(
                "SELECT id, wecom_userid, name, role, contact, created_at "
                "FROM users ORDER BY id")
        rows = cur.fetchall()
        result = [dict(r) for r in rows]
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='用户管理')
    parser.add_argument('--bootstrap', action='store_true')
    parser.add_argument('--add', action='store_true')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--user-id', help='企业微信 userid')
    parser.add_argument('--name', help='用户显示名称')
    parser.add_argument('--caller-id', help='调用者的 wecom_userid（--add 模式必填）')
    parser.add_argument('--contact', help='联系方式')
    parser.add_argument('--role', choices=['director', 'manager'], help='按角色过滤（--list 模式）')
    args = parser.parse_args()

    mode = sum([args.bootstrap, args.add, args.list])
    if mode != 1:
        print(json.dumps({"error": "必须指定 --bootstrap、--add 或 --list 其一", "code": 1}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    if args.bootstrap:
        if not args.user_id or not args.name:
            print(json.dumps({"error": "--bootstrap 模式需要 --user-id 和 --name", "code": 1}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        cmd_bootstrap(args.user_id, args.name)

    elif args.add:
        if not args.caller_id or not args.user_id or not args.name:
            print(json.dumps({"error": "--add 模式需要 --caller-id、--user-id 和 --name", "code": 1}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        cmd_add(args.caller_id, args.user_id, args.name, args.contact)

    elif args.list:
        cmd_list(args.role)


if __name__ == '__main__':
    main()
