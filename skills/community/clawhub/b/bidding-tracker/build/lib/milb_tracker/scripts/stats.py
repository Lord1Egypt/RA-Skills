#!/usr/bin/env python3
"""
统计招投标项目表现，输出 JSON。

用法：
    python3 scripts/stats.py                          # 全局统计
    python3 scripts/stats.py --by-manager             # 按负责人分组统计
    python3 scripts/stats.py --by-month                # 按月度趋势统计
    python3 scripts/stats.py --period 2026-Q1         # 指定季度
    python3 scripts/stats.py --period 2026-03         # 指定月份
    python3 scripts/stats.py --manager 张经理         # 指定负责人
"""

import argparse
import json
import os
import re
import sqlite3
import sys

from milb_tracker.config import get_db_path

DB_PATH = get_db_path()


def get_conn():
    conn = sqlite3.connect(os.path.abspath(DB_PATH), timeout=10.0)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def parse_period(period: str | None) -> tuple[str, str] | None:
    """将 period 转为 (start, end) 日期范围字符串。"""
    if not period:
        return None
    if re.match(r'^\d{4}-Q[1-4]$', period):
        year = int(period[:4])
        quarter = int(period[-1])
        start_month = (quarter - 1) * 3 + 1
        start = f"{year}-{start_month:02d}-01"
        end_month = start_month + 2
        if end_month in (1, 3, 5, 7, 8, 10, 12):
            end = f"{year}-{end_month:02d}-31"
        elif end_month in (4, 6, 9, 11):
            end = f"{year}-{end_month:02d}-30"
        else:
            end = f"{year}-{end_month:02d}-28"
        return start, end
    elif re.match(r'^\d{4}-\d{2}$', period):
        start = f"{period}-01"
        year, month = int(period[:4]), int(period[5:7])
        if month == 12:
            end = f"{year + 1}-01-01"
        else:
            end = f"{year}-{month + 1:02d}-01"
        return start, end
    else:
        print(json.dumps({"error": "无效的 period 格式，支持 YYYY-MM 或 YYYY-QN", "code": 1}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


def stats_global(period: str | None) -> dict:
    """全局统计：总数、中标数、胜率、平均报价差。"""
    conn = get_conn()
    try:
        date_filter, params = "", []
        date_range = parse_period(period)
        if date_range:
            date_filter = " AND p.bid_opening_time >= ? AND p.bid_opening_time < ?"
            params = list(date_range)

        sql = f"""
        SELECT
            COUNT(DISTINCT p.id) AS total,
            COUNT(DISTINCT CASE WHEN r.is_winner = 1 THEN p.id END) AS won,
            COUNT(DISTINCT CASE WHEN r.is_winner = 0 THEN p.id END) AS lost,
            COUNT(DISTINCT CASE WHEN r.id IS NOT NULL AND p.status NOT IN ('won', 'lost', 'cancelled') THEN p.id END) AS active,
            AVG(p.budget) AS avg_budget,
            AVG(r.our_bid_price - r.winning_price) AS avg_price_diff
        FROM projects p
        LEFT JOIN bid_results r ON r.project_id = p.id
        WHERE r.id IS NOT NULL
        {date_filter}
        """
        row = conn.execute(sql, params).fetchone()
        total = row[0] or 0
        won = row[1] or 0
        lost = row[2] or 0
        active = row[3] or 0
        win_rate = round(won / (won + lost), 3) if (won + lost) > 0 else 0.0

        return {
            "total": total,
            "won": won,
            "lost": lost,
            "active": active,
            "win_rate": win_rate,
            "avg_budget": row[4],
            "avg_price_diff": row[5],
        }
    finally:
        conn.close()


def stats_by_manager(period: str | None) -> list:
    """按项目负责人分组统计。"""
    conn = get_conn()
    try:
        date_filter, params = "", []
        date_range = parse_period(period)
        if date_range:
            date_filter = " AND p.bid_opening_time >= ? AND p.bid_opening_time < ?"
            params = list(date_range)

        sql = f"""
        SELECT
            p.project_manager AS manager,
            COUNT(DISTINCT p.id) AS total,
            COUNT(DISTINCT CASE WHEN r.is_winner = 1 THEN p.id END) AS won,
            COUNT(DISTINCT CASE WHEN r.is_winner = 0 THEN p.id END) AS lost,
            COUNT(DISTINCT CASE WHEN p.status NOT IN ('won', 'lost', 'cancelled') THEN p.id END) AS active
        FROM projects p
        LEFT JOIN bid_results r ON r.project_id = p.id
        WHERE r.id IS NOT NULL
        {date_filter}
        GROUP BY p.project_manager
        ORDER BY won DESC
        """
        rows = conn.execute(sql, params).fetchall()
        result = []
        for row in rows:
            won = row[2] or 0
            lost = row[3] or 0
            result.append({
                "manager": row[0] or "(未指派)",
                "total": row[1] or 0,
                "won": won,
                "lost": lost,
                "active": row[4] or 0,
                "win_rate": round(won / (won + lost), 3) if (won + lost) > 0 else 0.0,
            })
        return result
    finally:
        conn.close()


def stats_by_month(period: str | None) -> list:
    """按月度统计趋势（可选 period 过滤）。"""
    conn = get_conn()
    try:
        date_filter, params = "", []
        date_range = parse_period(period)
        if date_range:
            date_filter = " AND p.bid_opening_time >= ? AND p.bid_opening_time < ?"
            params = list(date_range)

        sql = f"""
        SELECT
            STRFTIME('%Y-%m', p.bid_opening_time) AS month,
            COUNT(DISTINCT p.id) AS total,
            COUNT(DISTINCT CASE WHEN r.is_winner = 1 THEN p.id END) AS won,
            COUNT(DISTINCT CASE WHEN r.is_winner = 0 THEN p.id END) AS lost
        FROM projects p
        LEFT JOIN bid_results r ON r.project_id = p.id
        WHERE p.bid_opening_time IS NOT NULL
        {date_filter}
        GROUP BY month
        ORDER BY month ASC
        """
        rows = conn.execute(sql, params).fetchall()
        result = []
        for row in rows:
            if row[0] is None:
                continue
            won = row[2] or 0
            lost = row[3] or 0
            result.append({
                "month": row[0],
                "total": row[1] or 0,
                "won": won,
                "lost": lost,
                "win_rate": round(won / (won + lost), 3) if (won + lost) > 0 else 0.0,
            })
        return result
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='招投标统计分析')
    parser.add_argument('--by-manager', action='store_true', help='按负责人分组统计')
    parser.add_argument('--by-month', action='store_true', help='按月度趋势统计')
    parser.add_argument('--period', help='指定时间范围，格式 YYYY-MM 或 YYYY-QN')
    args = parser.parse_args()

    if args.by_month:
        result = stats_by_month(args.period)
    elif args.by_manager:
        result = stats_by_manager(args.period)
    else:
        result = stats_global(args.period)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == '__main__':
    main()
