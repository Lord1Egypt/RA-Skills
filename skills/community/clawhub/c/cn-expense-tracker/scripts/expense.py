#!/usr/bin/env python3
"""
中文个人记账助手 - cn-expense-tracker
随手记、查统计、设预算、看趋势

用法:
  python3 expense.py --add "午餐" 25 --category 餐饮
  python3 expense.py --month
  python3 expense.py --budget 3000
  python3 expense.py --compare
  python3 expense.py --interactive
"""

import json
import os
import sys
import csv
import argparse
import re
from datetime import datetime, timedelta
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.expanduser("~/.qclaw/workspace")
DATA_FILE = os.path.join(WORKSPACE, "expenses.json")
BUDGET_FILE = os.path.join(WORKSPACE, "budget.json")

CATEGORIES = {
    "餐饮": "🍽️", "交通": "🚗", "购物": "🛒", "娱乐": "🎬",
    "居住": "🏠", "医疗": "🏥", "教育": "📚", "通讯": "📱",
    "服饰": "👔", "护肤": "💄", "饮品": "☕", "咖啡": "☕",
    "零食": "🍪", "水果": "🍎", "健身": "💪", "旅行": "✈️",
    "宠物": "🐱", "人情": "🎁", "其他": "📌"
}

CATEGORY_ALIASES = {
    "吃": "餐饮", "外卖": "餐饮", "饭": "餐饮", "午饭": "餐饮",
    "车": "交通", "打车": "交通", "地铁": "交通", "公交": "交通",
    "买": "购物", "衣服": "服饰", "包包": "购物",
    "玩": "娱乐", "电影": "娱乐", "游戏": "娱乐",
    "住": "居住", "房租": "居住", "水电": "居住",
    "医": "医疗", "药": "医疗",
    "学": "教育", "书": "教育", "课": "教育",
    "话": "通讯", "网": "通讯",
    "化": "护肤", "美": "护肤",
}


# ========== 数据操作 ==========

def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_expenses(expenses):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=2)


def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_budget(budget):
    with open(BUDGET_FILE, "w", encoding="utf-8") as f:
        json.dump(budget, f, ensure_ascii=False, indent=2)


def normalize_category(cat):
    """规范化类别名称"""
    if cat in CATEGORIES:
        return cat
    if cat in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[cat]
    # 模糊匹配
    for key, alias in CATEGORY_ALIASES.items():
        if key in cat:
            return alias
    return "其他"


def add_expense(desc, amount, category, note=""):
    """添加一笔支出"""
    expenses = load_expenses()
    expense = {
        "id": len(expenses) + 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "datetime": datetime.now().isoformat(),
        "desc": desc,
        "amount": float(amount),
        "category": normalize_category(category),
        "note": note
    }
    expenses.append(expense)
    save_expenses(expenses)
    return expense


def delete_expense(expense_id):
    """删除一笔支出"""
    expenses = load_expenses()
    before = len(expenses)
    expenses = [e for e in expenses if e["id"] != int(expense_id)]
    if len(expenses) == before:
        return False
    # 重新编号
    for i, e in enumerate(expenses):
        e["id"] = i + 1
    save_expenses(expenses)
    return True


# ========== 统计分析 ==========

def get_month_range(year, month):
    """获取月份起止日期"""
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(seconds=1)
    return start, end


def month_expenses(year, month):
    """获取指定月份的支出"""
    expenses = load_expenses()
    start, end = get_month_range(year, month)
    return [
        e for e in expenses
        if start <= datetime.fromisoformat(e["datetime"]) <= end
    ]


def month_report(year, month):
    """生成本月报告"""
    expenses = month_expenses(year, month)
    if not expenses:
        print("\n📭 暂无记录")
        return

    total = sum(e["amount"] for e in expenses)
    budget = load_budget()
    budget_amount = budget.get(f"{year}-{month:02d}", 0)

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]

    sorted_cat = sorted(by_category.items(), key=lambda x: x[1], reverse=True)

    y, m = year, month
    if m == 1:
        prev_y, prev_m = y - 1, 12
    else:
        prev_y, prev_m = y, m - 1
    prev_expenses = month_expenses(prev_y, prev_m)
    prev_total = sum(e["amount"] for e in prev_expenses)
    prev_by_cat = defaultdict(float)
    for e in prev_expenses:
        prev_by_cat[e["category"]] += e["amount"]

    # 输出报告
    print("\n💰 {}年{}月支出报告".format(y, m))
    print("=" * 40)
    print("总支出：{:,.1f} 元".format(total))
    if budget_amount:
        pct = total / budget_amount * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        if pct > 100:
            status = "🔴 超支！"
        elif pct > 80:
            status = "🟡 警戒"
        else:
            status = "🟢 正常"
        print("预算：{:,} 元（{}{:.1f}%）{}".format(
            budget_amount, bar, min(pct, 100), status))
    print()
    print("📊 分类明细：")
    for cat, amount in sorted_cat:
        pct = amount / total * 100
        emoji = CATEGORIES.get(cat, "📌")
        bar = "▓" * int(pct / 5)
        print("  {} {} {:>8} ({:>5.1f}%) {}".format(
            emoji, cat.ljust(4), "{:.1f}".format(amount), pct, bar))

    # 月度对比
    if prev_total > 0:
        print("\n📈 对比上月（{}年{}月）：".format(prev_y, prev_m))
        change = (total - prev_total) / prev_total * 100
        emoji = "📈" if change > 0 else "📉"
        print("  {} 总支出 {:+.1f}%（{:,.1f} → {:,.1f}）".format(
            emoji, change, prev_total, total))
        for cat, amount in sorted_cat[:5]:
            prev_amt = prev_by_cat.get(cat, 0)
            if prev_amt > 0:
                cat_change = (amount - prev_amt) / prev_amt * 100
                emoji = "+" if cat_change > 0 else ""
                print("  {} {} {:+.0f}%".format(
                    CATEGORIES.get(cat, "📌"), cat, cat_change))
            elif amount > 0:
                print("  🆕 {} {} 新增支出 {:.1f}".format(
                    CATEGORIES.get(cat, "📌"), cat, amount))

    print()


def compare_months(months=6):
    """月度趋势对比"""
    expenses = load_expenses()
    if not expenses:
        print("\n📭 暂无记录")
        return

    # 获取最近N个月
    by_month = defaultdict(float)
    for e in expenses:
        dt = datetime.fromisoformat(e["datetime"])
        key = (dt.year, dt.month)
        by_month[key] += e["amount"]

    sorted_months = sorted(by_month.keys(), reverse=True)[:months]

    print("\n📈 支出趋势（近{}个月）".format(len(sorted_months)))
    print("=" * 44)
    print("  月份        支出       变化")
    print("-" * 44)

    prev = None
    for y, m in sorted(sorted_months):
        amount = by_month[(y, m)]
        if prev:
            change = (amount - prev) / prev * 100
            arrow = "↑" if change > 0 else "↓"
            print("  {}-{:02d}   {:>9,.1f}  {} {:.0f}%".format(
                y, m, amount, arrow, abs(change)))
        else:
            print("  {}-{:02d}   {:>9,.1f}  ──".format(y, m, amount))
        prev = amount
    print()


def list_expenses(limit=20, category=None):
    """列出最近记录"""
    expenses = load_expenses()
    if category:
        expenses = [e for e in expenses if normalize_category(category) == e["category"]]

    if not expenses:
        print("\n📭 暂无记录")
        return

    expenses.sort(key=lambda x: x["datetime"], reverse=True)
    print("\n📋 最近{}笔记录".format(min(limit, len(expenses))))
    print("-" * 60)
    for e in expenses[:limit]:
        emoji = CATEGORIES.get(e["category"], "📌")
        note_str = " | {}".format(e["note"]) if e.get("note") else ""
        print("  {}. {} {} {:>8,.1f}元  {}{}".format(
            e["id"], e["date"], emoji, e["amount"], e["desc"], note_str))
    print()


def export_csv():
    """导出CSV"""
    expenses = load_expenses()
    if not expenses:
        print("\n📭 暂无记录可导出")
        return

    csv_file = os.path.join(WORKSPACE, "expenses_export.csv")
    with open(csv_file, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "日期", "时间", "描述", "金额", "类别", "备注"])
        for e in expenses:
            writer.writerow([
                e["id"], e["date"], e["datetime"].split("T")[1][:8],
                e["desc"], e["amount"], e["category"], e.get("note", "")
            ])

    print("\n✅ 已导出 {} 笔记录 → {}".format(len(expenses), csv_file))
    print("   路径：{}".format(csv_file))
    print("   可直接用 Excel 打开")


def set_budget(amount, month=None):
    """设置月度预算"""
    budget = load_budget()
    now = datetime.now()
    key = month or f"{now.year}-{now.month:02d}"
    budget[str(key)] = float(amount)
    save_budget(budget)
    print("\n✅ 预算已设置为 {:,.0f} 元（{}）".format(
        float(amount), key))


def interactive():
    """交互记账模式"""
    print("\n💰 记账助手（输入 q 退出）")
    print("  格式：金额 类别 [描述] [备注]")
    print("  例如：25 餐饮 午餐 外卖")
    print("  快捷：25 吃 午饭")
    while True:
        try:
            line = input("\n> ").strip()
            if not line:
                continue
            if line.lower() == "q":
                break

            parts = line.split()
            if len(parts) < 2:
                print("  ⚠️ 格式：金额 类别 [描述]")
                continue

            amount = float(parts[0])
            cat = normalize_category(parts[1])
            desc = parts[2] if len(parts) > 2 else cat
            note = parts[3] if len(parts) > 3 else ""

            e = add_expense(desc, amount, cat, note)
            emoji = CATEGORIES.get(cat, "📌")
            print("  ✅ {} {} {:,.1f}元".format(e["date"], emoji, e["amount"]))

        except (ValueError, EOFError, KeyboardInterrupt):
            print("\n\n✅ 记账完成！")
            break


# ========== 主入口 ==========

def main():
    parser = argparse.ArgumentParser(description="💰 中文个人记账助手")
    parser.add_argument("--add", nargs="+",
                        help="记一笔：金额 描述 [类别] [备注]")
    parser.add_argument("--category", "-c",
                        help="指定类别")
    parser.add_argument("--note",
                        help="备注")
    parser.add_argument("--month", action="store_true",
                        help="本月报告")
    parser.add_argument("--budget", type=float,
                        help="设置月度预算")
    parser.add_argument("--compare", action="store_true",
                        help="月度趋势对比")
    parser.add_argument("--list", action="store_true",
                        help="列出最近记录")
    parser.add_argument("--delete", type=int, metavar="ID",
                        help="删除指定ID的记录")
    parser.add_argument("--export", action="store_true",
                        help="导出CSV")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="交互记账模式")
    parser.add_argument("--limit", type=int, default=20,
                        help="列出记录数量（默认20）")
    parser.add_argument("--year", type=int,
                        help="指定年份（默认今年）")
    parser.add_argument("--month-num", type=int, metavar="M",
                        help="指定月份（默认当月）")
    args = parser.parse_args()

    now = datetime.now()
    year = args.year or now.year
    month = args.month_num or now.month

    if args.interactive:
        interactive()
    elif args.add:
        try:
            amount = float(args.add[0])
            desc = args.add[1] if len(args.add) > 1 else "支出"
            cat = args.category or (args.add[2] if len(args.add) > 2 else "其他")
            note = args.note or (args.add[3] if len(args.add) > 3 else "")
            e = add_expense(desc, amount, cat, note)
            emoji = CATEGORIES.get(e["category"], "📌")
            print("\n✅ {} {} {:,.1f}元（{}）".format(
                e["date"], emoji, e["amount"], e["category"]))
        except ValueError:
            print("\n⚠️ 金额必须是数字")
    elif args.delete:
        if delete_expense(args.delete):
            print("\n✅ 记录 {} 已删除".format(args.delete))
        else:
            print("\n⚠️ 未找到记录 {}".format(args.delete))
    elif args.month:
        month_report(year, month)
    elif args.budget:
        set_budget(args.budget)
    elif args.compare:
        compare_months()
    elif args.list:
        list_expenses(args.limit, args.category)
    elif args.export:
        export_csv()
    else:
        # 默认显示当月报告
        month_report(year, month)


if __name__ == "__main__":
    main()
