#!/usr/bin/env python3
"""cashbook 预算管理"""

import argparse
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_conn


def fmt_table(headers, rows):
    """简单的 ASCII 对齐表格"""
    widths = [len(h) for h in headers]
    str_rows = []
    for row in rows:
        cells = [str(c) if c is not None else "" for c in row]
        str_rows.append(cells)
        for i, c in enumerate(cells):
            w = sum(2 if ord(ch) > 127 else 1 for ch in c)
            widths[i] = max(widths[i], w)

    def pad(s, w):
        vis = sum(2 if ord(ch) > 127 else 1 for ch in s)
        return s + " " * (w - vis)

    hdr = "  ".join(pad(h, widths[i]) for i, h in enumerate(headers))
    sep = "  ".join("-" * w for w in widths)
    print(hdr)
    print(sep)
    for cells in str_rows:
        print("  ".join(pad(c, widths[i]) for i, c in enumerate(cells)))


def get_month_range(dt=None):
    """返回当月起止日期"""
    if dt is None:
        dt = datetime.now().date()
    start = dt.replace(day=1).isoformat()
    end = dt.isoformat()
    return start, end


def get_week_range(dt=None):
    """返回当周起止日期"""
    if dt is None:
        dt = datetime.now().date()
    start = (dt - timedelta(days=dt.weekday())).isoformat()
    end = dt.isoformat()
    return start, end


def cmd_set(args):
    conn = get_conn()

    category_id = None
    cat_label = "总"

    if args.category:
        cat = conn.execute(
            "SELECT id, name FROM categories WHERE name = ? AND type = 'expense'",
            (args.category,),
        ).fetchone()
        if not cat:
            print(f"❌ 未找到支出分类：{args.category}")
            conn.close()
            return
        category_id = cat["id"]
        cat_label = cat["name"]

    period = args.period or "monthly"
    period_label = "月度" if period == "monthly" else "周度"

    # 查找已有预算
    if category_id is not None:
        existing = conn.execute(
            "SELECT id FROM budgets WHERE category_id = ? AND period = ? AND active = 1",
            (category_id, period),
        ).fetchone()
    else:
        existing = conn.execute(
            "SELECT id FROM budgets WHERE category_id IS NULL AND period = ? AND active = 1",
            (period,),
        ).fetchone()

    if existing:
        conn.execute(
            "UPDATE budgets SET amount = ? WHERE id = ?",
            (args.amount, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO budgets (category_id, amount, period) VALUES (?, ?, ?)",
            (category_id, args.amount, period),
        )

    conn.commit()
    conn.close()
    print(f"✅ 已设置 {cat_label} {period_label}预算 ¥{args.amount:,.2f}")


def cmd_query(args):
    conn = get_conn()
    today = datetime.now().date()

    if args.all:
        # 列出所有预算进度
        budgets = conn.execute(
            "SELECT b.id, b.category_id, b.amount, b.period, c.name as cat_name "
            "FROM budgets b LEFT JOIN categories c ON b.category_id = c.id "
            "WHERE b.active = 1 ORDER BY b.category_id IS NULL, c.name",
        ).fetchall()

        if not budgets:
            print("暂未设置任何预算")
            conn.close()
            return

        for b in budgets:
            _print_budget_progress(conn, b, today)
            print()
    elif args.category:
        cat = conn.execute(
            "SELECT id, name FROM categories WHERE name = ? AND type = 'expense'",
            (args.category,),
        ).fetchone()
        if not cat:
            print(f"❌ 未找到支出分类：{args.category}")
            conn.close()
            return

        budget = conn.execute(
            "SELECT b.id, b.category_id, b.amount, b.period, c.name as cat_name "
            "FROM budgets b LEFT JOIN categories c ON b.category_id = c.id "
            "WHERE b.category_id = ? AND b.active = 1",
            (cat["id"],),
        ).fetchone()

        if not budget:
            print(f"未找到 {args.category} 的预算设置")
            conn.close()
            return

        _print_budget_progress(conn, budget, today)
    else:
        # 查全部
        budgets = conn.execute(
            "SELECT b.id, b.category_id, b.amount, b.period, c.name as cat_name "
            "FROM budgets b LEFT JOIN categories c ON b.category_id = c.id "
            "WHERE b.active = 1 ORDER BY b.category_id IS NULL, c.name",
        ).fetchall()

        if not budgets:
            print("暂未设置任何预算")
            conn.close()
            return

        for b in budgets:
            _print_budget_progress(conn, b, today)
            print()

    conn.close()


def _print_budget_progress(conn, budget, today):
    """打印单条预算进度"""
    period = budget["period"]
    period_label = "月度" if period == "monthly" else "周度"

    if period == "monthly":
        date_start, date_end = get_month_range(today)
        period_title = "本月"
    else:
        date_start, date_end = get_week_range(today)
        period_title = "本周"

    cat_name = budget["cat_name"] or "总"
    budget_amount = budget["amount"]

    # 计算已支出
    if budget["category_id"] is not None:
        spent = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions "
            "WHERE category_id = ? AND type = 'expense' AND date BETWEEN ? AND ?",
            (budget["category_id"], date_start, date_end),
        ).fetchone()[0]
    else:
        spent = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions "
            "WHERE type = 'expense' AND date BETWEEN ? AND ?",
            (date_start, date_end),
        ).fetchone()[0]

    remaining = budget_amount - spent
    pct = (spent / budget_amount * 100) if budget_amount > 0 else 0

    if spent > budget_amount:
        status = "⚠️ 已超支"
    else:
        status = "正常 ✅"

    print(f"{period_title}{cat_name}预算：¥{budget_amount:,.2f}")
    print(f"已支出：¥{spent:,.2f}（{pct:.1f}%）")
    print(f"剩余：¥{remaining:,.2f}")
    print(f"状态：{status}")


def cmd_list(args):
    conn = get_conn()
    budgets = conn.execute(
        "SELECT b.id, b.category_id, b.amount, b.period, c.name as cat_name "
        "FROM budgets b LEFT JOIN categories c ON b.category_id = c.id "
        "WHERE b.active = 1 ORDER BY b.category_id IS NULL, c.name",
    ).fetchall()

    if not budgets:
        print("暂未设置任何预算")
        conn.close()
        return

    period_labels = {"monthly": "月度", "weekly": "周度"}
    headers = ["ID", "分类", "金额", "周期"]
    rows = [
        (
            str(b["id"]),
            b["cat_name"] or "总预算",
            f'¥{b["amount"]:,.2f}',
            period_labels.get(b["period"], b["period"]),
        )
        for b in budgets
    ]

    fmt_table(headers, rows)
    conn.close()


def cmd_delete(args):
    conn = get_conn()

    if args.id:
        budget = conn.execute(
            "SELECT b.id, c.name as cat_name FROM budgets b "
            "LEFT JOIN categories c ON b.category_id = c.id "
            "WHERE b.id = ? AND b.active = 1",
            (args.id,),
        ).fetchone()
        if not budget:
            print(f"❌ 未找到 ID={args.id} 的预算")
            conn.close()
            return
        conn.execute("UPDATE budgets SET active = 0 WHERE id = ?", (args.id,))
        conn.commit()
        cat_name = budget["cat_name"] or "总"
        print(f"✅ 已删除 {cat_name} 预算")
    elif args.category:
        cat = conn.execute(
            "SELECT id, name FROM categories WHERE name = ? AND type = 'expense'",
            (args.category,),
        ).fetchone()
        if not cat:
            print(f"❌ 未找到支出分类：{args.category}")
            conn.close()
            return
        result = conn.execute(
            "UPDATE budgets SET active = 0 WHERE category_id = ? AND active = 1",
            (cat["id"],),
        )
        conn.commit()
        if result.rowcount > 0:
            print(f"✅ 已删除 {args.category} 预算")
        else:
            print(f"未找到 {args.category} 的有效预算")
    else:
        print("❌ 请指定 --id 或 --category")

    conn.close()


def main():
    parser = argparse.ArgumentParser(description="cashbook 预算管理")
    sub = parser.add_subparsers(dest="command")

    # set
    p_set = sub.add_parser("set", help="设置预算")
    p_set.add_argument("--category", help="分类名（不传=总预算）")
    p_set.add_argument("--amount", type=float, required=True, help="预算金额")
    p_set.add_argument("--period", choices=["monthly", "weekly"], default="monthly", help="周期（默认 monthly）")

    # query
    p_query = sub.add_parser("query", help="查询预算进度")
    p_query.add_argument("--category", help="分类名")
    p_query.add_argument("--all", action="store_true", help="列出所有预算进度")

    # list
    sub.add_parser("list", help="列出所有预算设置")

    # delete
    p_del = sub.add_parser("delete", help="删除预算")
    p_del.add_argument("--category", help="分类名")
    p_del.add_argument("--id", type=int, help="预算 ID")

    args = parser.parse_args()

    if args.command == "set":
        cmd_set(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "delete":
        cmd_delete(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
