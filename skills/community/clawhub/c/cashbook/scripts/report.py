#!/usr/bin/env python3
"""cashbook 周报/月报"""

import argparse
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_conn


def get_week_range(dt=None):
    """返回指定日期所在周的起止（周一~周日）"""
    if dt is None:
        dt = datetime.now().date()
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return start, end


def get_month_range(year, month):
    """返回指定月份的起止日期"""
    from calendar import monthrange
    start = datetime(year, month, 1).date()
    _, last_day = monthrange(year, month)
    end = datetime(year, month, last_day).date()
    return start, end


def make_bar(pct, width=10):
    """生成 ASCII 进度条"""
    if pct <= 100:
        filled = round(pct / 100 * width)
        return "█" * filled + "░" * (width - filled)
    else:
        over = round((pct - 100) / 100 * width)
        over = min(over, width)
        return "█" * width + "▓" * over


def format_amount(val):
    """格式化金额"""
    return f"¥{val:,.2f}"


def fetch_transactions(conn, date_start, date_end):
    """获取指定日期范围内的交易"""
    rows = conn.execute(
        "SELECT t.amount, t.type, t.date, t.merchant, t.note, c.name as category "
        "FROM transactions t "
        "LEFT JOIN categories c ON t.category_id = c.id "
        "WHERE t.date BETWEEN ? AND ?",
        (date_start.isoformat(), date_end.isoformat()),
    ).fetchall()
    return rows


def fetch_budgets(conn):
    """获取所有活跃预算"""
    return conn.execute(
        "SELECT b.id, b.category_id, b.amount, b.period, c.name as cat_name "
        "FROM budgets b LEFT JOIN categories c ON b.category_id = c.id "
        "WHERE b.active = 1",
    ).fetchall()


def calc_category_totals(rows, tx_type="expense"):
    """按分类汇总"""
    totals = {}
    for r in rows:
        if r["type"] == tx_type:
            cat = r["category"] or "未分类"
            totals[cat] = totals.get(cat, 0) + r["amount"]
    return totals


def find_top_tx(rows, tx_type="expense"):
    """找到最高单笔"""
    top = None
    for r in rows:
        if r["type"] == tx_type:
            if top is None or r["amount"] > top["amount"]:
                top = r
    return top


def print_category_ranking(cat_totals, total_expense):
    """打印分类排行"""
    print("\n支出分类排行：")
    sorted_cats = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
    for i, (name, amount) in enumerate(sorted_cats, 1):
        pct = (amount / total_expense * 100) if total_expense > 0 else 0
        bar = make_bar(pct)
        print(f"  {i}. {name:<8} {format_amount(amount):>12}  {pct:>5.1f}%  {bar}")


def report_week(conn, dt=None):
    """生成周报"""
    if dt is None:
        dt = datetime.now().date()
    start, end = get_week_range(dt)

    rows = fetch_transactions(conn, start, end)

    total_income = sum(r["amount"] for r in rows if r["type"] == "income")
    total_expense = sum(r["amount"] for r in rows if r["type"] == "expense")
    net = total_income - total_expense
    net_str = f"+¥{net:,.2f}" if net >= 0 else f"-¥{abs(net):,.2f}"

    print(f"📊 本周账单（{start} ~ {end}）")
    print("═" * 35)
    print(f"总支出：{format_amount(total_expense)}    总收入：{format_amount(total_income)}    净额：{net_str}")

    cat_totals = calc_category_totals(rows, "expense")
    if cat_totals:
        print_category_ranking(cat_totals, total_expense)

    top = find_top_tx(rows, "expense")
    if top:
        print(f"\n最高单笔：{format_amount(top['amount'])} / {top['category'] or '未分类'} / {top['date']} / {top['merchant'] or top['note'] or '-'}")

    if not rows:
        print("\n本周暂无交易记录")


def report_month(conn, year=None, month=None):
    """生成月报"""
    today = datetime.now().date()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    start, end = get_month_range(year, month)

    rows = fetch_transactions(conn, start, end)

    total_income = sum(r["amount"] for r in rows if r["type"] == "income")
    total_expense = sum(r["amount"] for r in rows if r["type"] == "expense")
    net = total_income - total_expense
    net_str = f"+¥{net:,.2f}" if net >= 0 else f"-¥{abs(net):,.2f}"

    print(f"📊 {year}年{month}月账单")
    print("═" * 35)
    print(f"总支出：{format_amount(total_expense)}    总收入：{format_amount(total_income)}    净额：{net_str}")

    cat_totals = calc_category_totals(rows, "expense")
    if cat_totals:
        print_category_ranking(cat_totals, total_expense)

    # 预算执行情况
    budgets = fetch_budgets(conn)
    cat_budgets = [b for b in budgets if b["category_id"] is not None and b["period"] == "monthly"]
    if cat_budgets:
        print("\n预算执行情况：")
        for b in cat_budgets:
            cat_name = b["cat_name"] or "未知"
            budget_amt = b["amount"]
            spent = cat_totals.get(cat_name, 0)
            pct = (spent / budget_amt * 100) if budget_amt > 0 else 0

            if pct > 100:
                status = "⚠️ 超支"
            elif pct >= 80:
                status = "⚡ 注意"
            else:
                status = "✅ 正常"

            print(f"  {cat_name:<8} ¥{spent:>,.0f} / ¥{budget_amt:>,.0f}   {pct:>5.1f}%  {status}")

    top = find_top_tx(rows, "expense")
    if top:
        print(f"\n最高单笔：{format_amount(top['amount'])} / {top['category'] or '未分类'} / {top['date']} / {top['merchant'] or top['note'] or '-'}")

    if not rows:
        print("\n本月暂无交易记录")


def main():
    parser = argparse.ArgumentParser(description="cashbook 周报/月报")
    parser.add_argument("--period", required=True, choices=["week", "month"], help="报告类型")
    parser.add_argument("--year", type=int, help="年份（月报用）")
    parser.add_argument("--month", type=int, help="月份（月报用）")
    args = parser.parse_args()

    conn = get_conn()

    if args.period == "week":
        report_week(conn)
    elif args.period == "month":
        report_month(conn, args.year, args.month)

    conn.close()


if __name__ == "__main__":
    main()
