#!/usr/bin/env python3
"""
查询项目列表或项目详情，按角色过滤，输出 JSON。

用法：
    python3 scripts/query_projects.py --user-id WangDirector --active-only
    python3 scripts/query_projects.py --user-id ZhangManager --active-only
    python3 scripts/query_projects.py --user-id WangDirector --keyword "2026-001"
    python3 scripts/query_projects.py --user-id ZhangManager --keyword "网安"
    python3 scripts/query_projects.py --id 1
    python3 scripts/query_projects.py --user-id WangDirector --status preparing
    python3 scripts/query_projects.py --user-id WangDirector --upcoming-days 7
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta

from milb_tracker.config import get_db_path

DB_PATH = get_db_path()

ACTIVE_STATUSES = ('registered', 'doc_pending', 'doc_purchased', 'preparing', 'sealed')


def get_conn():
    conn = sqlite3.connect(os.path.abspath(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def query_all(user_id: str | None,
              keyword: str | None,
              status: str | None,
              active_only: bool,
              upcoming_days: int | None) -> list:
    """
    按用户身份和条件查询项目列表。
    无 --user-id 时默认只返回活跃项目（向后兼容）。
    """
    conn = get_conn()
    try:
        role, name = None, None

        # 从 users 表解析角色和姓名
        if user_id:
            row = conn.execute(
                "SELECT role, name FROM users WHERE wecom_userid = ?",
                (user_id,)).fetchone()
            if not row:
                print(json.dumps({"error": "用户不存在", "code": 1}, ensure_ascii=False), file=sys.stderr)
                sys.exit(1)
            role, name = row['role'], row['name']

        sql = "SELECT * FROM projects WHERE 1=1"
        params = []

        # --keyword：先精确匹配 project_no，再模糊匹配 project_name
        if keyword:
            exact = conn.execute(
                "SELECT * FROM projects WHERE project_no = ?", (keyword,)).fetchone()
            if exact:
                cols = list(exact.keys())
                return [dict(zip(cols, exact))]
            sql += " AND project_name LIKE ?"
            params.append(f"%{keyword}%")

        # 角色过滤：manager 只看本人项目
        if role == 'manager' and name:
            sql += " AND project_manager = ?"
            params.append(name)

        # 状态过滤
        if status:
            sql += " AND status = ?"
            params.append(status)
        elif active_only or not status:
            # 默认只返回活跃项目（active_only=True 或无 status 参数时）
            placeholders = ','.join(['?'] * len(ACTIVE_STATUSES))
            sql += f" AND status IN ({placeholders})"
            params.extend(ACTIVE_STATUSES)

        # 近期关键节点过滤
        if upcoming_days is not None:
            now_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            cutoff = (datetime.now() + timedelta(days=upcoming_days)).strftime("%Y-%m-%dT%H:%M:%S")
            sql += (" AND (bid_opening_time BETWEEN ? AND ?"
                    " OR doc_purchase_deadline BETWEEN ? AND ?"
                    " OR suggested_seal_time BETWEEN ? AND ?)")
            params.extend([now_str, cutoff, now_str, cutoff, now_str, cutoff])

        sql += " ORDER BY bid_opening_time ASC"

        cur = conn.execute(sql, params)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        return [dict(zip(cols, row)) for row in rows]
    finally:
        conn.close()


def query_by_id(project_id: int) -> dict | None:
    """查询单个项目详情。"""
    conn = get_conn()
    try:
        cur = conn.execute("SELECT * FROM projects WHERE id=?", (project_id,))
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        return dict(zip(cols, row)) if row else None
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='查询招投标项目')
    parser.add_argument('--user-id', help='当前用户 wecom_userid（从 users 表查角色）')
    parser.add_argument('--keyword', help='搜索关键词：先精确匹配 project_no，再模糊匹配 project_name')
    parser.add_argument('--id', type=int, help='查询指定项目详情')
    parser.add_argument('--status', help='按状态过滤')
    parser.add_argument('--active-only', action='store_true', help='仅返回活跃项目')
    parser.add_argument('--upcoming-days', type=int, help='返回 N 天内有关键节点的项目')
    args = parser.parse_args()

    if args.id:
        result = query_by_id(args.id)
    else:
        result = query_all(args.user_id, args.keyword, args.status,
                           args.active_only, args.upcoming_days)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == '__main__':
    main()
