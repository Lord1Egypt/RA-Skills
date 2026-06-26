#!/usr/bin/env python3
"""家庭账本 - 简单的家庭支出记录 CLI 工具"""

import argparse
import os
import sqlite3
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ledger.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    return conn


def cmd_add(args):
    conn = get_conn()
    conn.execute(
        "INSERT INTO expenses (role, amount, note) VALUES (?, ?, ?)",
        (args.role, args.amount, args.note or ""),
    )
    conn.commit()
    print(f"已记录: {args.role} 支出 {args.amount:.2f} 元" + (f" ({args.note})" if args.note else ""))


def cmd_list(args):
    conn = get_conn()
    sql = "SELECT id, role, amount, note, created_at FROM expenses WHERE 1=1"
    params = []
    if args.role:
        sql += " AND role = ?"
        params.append(args.role)
    if args.month:
        sql += " AND created_at LIKE ?"
        params.append(f"{args.month}%")
    if args.year:
        sql += " AND created_at LIKE ?"
        params.append(f"{args.year}%")
    sql += " ORDER BY created_at DESC, id DESC"
    if args.limit:
        sql += " LIMIT ?"
        params.append(args.limit)

    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("没有找到记录")
        return

    print(f"{'ID':>5}  {'日期':<19}  {'角色':<8}  {'金额':>10}  {'备注'}")
    print("─" * 65)
    total = 0.0
    for r in rows:
        total += r[2]
        note_display = r[3] if r[3] else ""
        print(f"{r[0]:>5}  {r[4]:<19}  {r[1]:<8}  {r[2]:>10.2f}  {note_display}")
    print("─" * 65)
    print(f"{'合计':>36}  {total:>10.2f}")


def cmd_summary(args):
    conn = get_conn()
    if args.year:
        _summary_year(conn, args.year)
    else:
        _summary_month(conn, args.month)


def _summary_month(conn, month):
    sql = "SELECT role, SUM(amount) FROM expenses WHERE 1=1"
    params = []
    if month:
        sql += " AND created_at LIKE ?"
        params.append(f"{month}%")
    sql += " GROUP BY role ORDER BY SUM(amount) DESC"

    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("没有找到记录")
        return

    title = f"月度汇总" + (f" ({month})" if month else " (全部)")
    print(title)
    print("─" * 35)
    total = 0.0
    for role, amount in rows:
        total += amount
        print(f"{role:<8}  {amount:>10.2f}")
    print("─" * 35)
    print(f"{'合计':<8}  {total:>10.2f}")


def _summary_year(conn, year):
    # Get all roles and monthly totals for the year
    sql = """
        SELECT role,
               CAST(strftime('%m', created_at) AS INTEGER) AS month,
               SUM(amount)
        FROM expenses
        WHERE created_at LIKE ?
        GROUP BY role, month
        ORDER BY role, month
    """
    rows = conn.execute(sql, (f"{year}%",)).fetchall()

    if not rows:
        print(f"{year} 年没有找到记录")
        return

    # Build role -> {month: amount} mapping
    roles = {}
    for role, month, amount in rows:
        if role not in roles:
            roles[role] = {}
        roles[role][month] = amount

    # Header
    header = f"{'':>8}"
    for m in range(1, 13):
        header += f"  {m:>7}月"
    header += f"  {'合计':>10}"
    print(f"{year} 年度汇总")
    print(header)
    print("─" * len(header.encode("gbk", errors="replace")))

    month_totals = [0.0] * 12
    grand_total = 0.0
    for role in sorted(roles.keys()):
        line = f"{role:>8}"
        role_total = 0.0
        for m in range(1, 13):
            val = roles[role].get(m, 0)
            role_total += val
            month_totals[m - 1] += val
            if val > 0:
                line += f"  {val:>8.2f}"
            else:
                line += f"  {'·':>8}"
        grand_total += role_total
        line += f"  {role_total:>10.2f}"
        print(line)

    # Totals row
    line = f"{'合计':>8}"
    for m in range(1, 13):
        val = month_totals[m - 1]
        if val > 0:
            line += f"  {val:>8.2f}"
        else:
            line += f"  {'·':>8}"
    line += f"  {grand_total:>10.2f}"
    print("─" * len(header.encode("gbk", errors="replace")))
    print(line)


def cmd_delete(args):
    conn = get_conn()
    cur = conn.execute("DELETE FROM expenses WHERE id = ?", (args.id,))
    conn.commit()
    if cur.rowcount > 0:
        print(f"已删除记录 #{args.id}")
    else:
        print(f"记录 #{args.id} 不存在")


def cmd_roles(args):
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT role FROM expenses ORDER BY role").fetchall()
    if not rows:
        print("还没有任何角色记录")
        return
    print("已有角色:")
    for r in rows:
        print(f"  - {r[0]}")


def main():
    parser = argparse.ArgumentParser(description="家庭账本")
    sub = parser.add_subparsers(dest="command")

    # add
    p_add = sub.add_parser("add", help="记录一笔支出")
    p_add.add_argument("--role", required=True, help="角色，如: 爸爸、妈妈")
    p_add.add_argument("--amount", required=True, type=float, help="金额")
    p_add.add_argument("--note", help="备注")

    # list
    p_list = sub.add_parser("list", help="查看支出记录")
    p_list.add_argument("--role", help="按角色筛选")
    p_list.add_argument("--month", help="按月份筛选，格式: 2026-05")
    p_list.add_argument("--year", help="按年份筛选，格式: 2026")
    p_list.add_argument("--limit", type=int, help="最多显示条数")

    # summary
    p_sum = sub.add_parser("summary", help="汇总支出")
    p_sum.add_argument("--month", help="按月份汇总，格式: 2026-05")
    p_sum.add_argument("--year", help="按年度汇总，格式: 2026")

    # delete
    p_del = sub.add_parser("delete", help="删除记录")
    p_del.add_argument("--id", required=True, type=int, help="记录 ID")

    # roles
    sub.add_parser("roles", help="查看已有角色")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "add": cmd_add,
        "list": cmd_list,
        "summary": cmd_summary,
        "delete": cmd_delete,
        "roles": cmd_roles,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
