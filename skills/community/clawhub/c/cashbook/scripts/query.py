#!/usr/bin/env python3
"""cashbook 查询与统计"""

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


def get_period_range(period):
    """返回时间段的起止日期"""
    today = datetime.now().date()
    if period == "today":
        return today.isoformat(), today.isoformat()
    if period == "week":
        start = today - timedelta(days=today.weekday())
        return start.isoformat(), today.isoformat()
    elif period == "month":
        start = today.replace(day=1)
        return start.isoformat(), today.isoformat()
    elif period == "year":
        start = today.replace(month=1, day=1)
        return start.isoformat(), today.isoformat()
    elif period == "all":
        return "1970-01-01", today.isoformat()
    return None, None


def query_detail(conn, args):
    """明细模式"""
    sql = (
        "SELECT t.date, t.amount, t.type, c.name as category, a.nickname as account, t.note "
        "FROM transactions t "
        "LEFT JOIN categories c ON t.category_id = c.id "
        "LEFT JOIN accounts a ON t.account_id = a.id "
        "WHERE 1=1 "
    )
    params = []

    if args.category:
        sql += "AND c.name = ? "
        params.append(args.category)
    if args.account:
        sql += "AND a.nickname = ? "
        params.append(args.account)
    if getattr(args, "from_date", None):
        sql += "AND t.date >= ? "
        params.append(args.from_date)
    if getattr(args, "to_date", None):
        sql += "AND t.date <= ? "
        params.append(args.to_date)

    sql += "ORDER BY t.date DESC, t.id DESC LIMIT ?"
    params.append(args.last)

    rows = conn.execute(sql, params).fetchall()
    if not rows:
        print("暂无流水记录")
        return

    type_labels = {"expense": "支出", "income": "收入", "transfer": "转账"}
    headers = ["日期", "类型", "金额", "分类", "账户", "备注"]
    data = [
        (r["date"], type_labels.get(r["type"], r["type"]),
         f'¥{r["amount"]:.2f}', r["category"] or "-",
         r["account"] or "-", r["note"] or "-")
        for r in rows
    ]
    fmt_table(headers, data)


def query_summary(conn, args):
    """汇总模式"""
    if args.from_date and args.to_date:
        date_from, date_to = args.from_date, args.to_date
    else:
        date_from, date_to = get_period_range(args.period)

    period_labels = {"today": "今日", "week": "本周", "month": "本月", "year": "本年", "all": "全部"}
    label = period_labels.get(args.period, f"{date_from} ~ {date_to}")

    sql_base = (
        "SELECT t.type, t.amount, c.name as category "
        "FROM transactions t "
        "LEFT JOIN categories c ON t.category_id = c.id "
        "LEFT JOIN accounts a ON t.account_id = a.id "
        "WHERE t.date BETWEEN ? AND ? "
    )
    params = [date_from, date_to]

    if args.category:
        sql_base += "AND c.name = ? "
        params.append(args.category)
    if args.account:
        sql_base += "AND a.nickname = ? "
        params.append(args.account)

    rows = conn.execute(sql_base, params).fetchall()
    if not rows:
        print(f"{label}暂无流水记录")
        return

    total_income = sum(r["amount"] for r in rows if r["type"] == "income")
    total_expense = sum(r["amount"] for r in rows if r["type"] == "expense")
    net = total_income - total_expense

    print(f"\n📊 {label}汇总（{date_from} ~ {date_to}）")
    print("=" * 40)
    print(f"  总收入：¥{total_income:.2f}")
    print(f"  总支出：¥{total_expense:.2f}")
    print(f"  净  额：¥{net:.2f}")

    # 分类分布 top5（仅支出）
    cat_totals = {}
    for r in rows:
        if r["type"] == "expense":
            cat_name = r["category"] or "未分类"
            cat_totals[cat_name] = cat_totals.get(cat_name, 0) + r["amount"]

    if cat_totals:
        print(f"\n  支出分类 TOP 5：")
        sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (name, amount) in enumerate(sorted_cats, 1):
            pct = amount / total_expense * 100 if total_expense else 0
            print(f"    {i}. {name:<8} ¥{amount:.2f}  ({pct:.1f}%)")
    print()


def main():
    parser = argparse.ArgumentParser(description="cashbook 查询与统计")
    parser.add_argument("--last", type=int, default=10, help="最近 N 条流水（默认 10）")
    parser.add_argument("--period", choices=["today", "week", "month", "year", "all"], help="按时间段汇总")
    parser.add_argument("--category", help="按分类筛选")
    parser.add_argument("--account", help="按账户筛选")
    parser.add_argument("--from", dest="from_date", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--to", dest="to_date", help="截止日期 YYYY-MM-DD")
    args = parser.parse_args()

    conn = get_conn()

    if args.period:
        query_summary(conn, args)
    else:
        query_detail(conn, args)

    conn.close()


if __name__ == "__main__":
    main()
