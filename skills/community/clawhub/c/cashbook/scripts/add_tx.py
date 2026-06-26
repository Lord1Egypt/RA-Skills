#!/usr/bin/env python3
"""cashbook 记录交易"""

import argparse
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_conn

# 多语言分类别名 → 中文分类名
CATEGORY_ALIASES = {
    # English → Chinese
    "food": "餐饮", "dining": "餐饮", "meals": "餐饮", "restaurant": "餐饮", "eating": "餐饮",
    "transport": "交通", "transportation": "交通", "taxi": "交通", "commute": "交通",
    "shopping": "购物", "groceries": "购物", "supermarket": "购物",
    "entertainment": "娱乐", "fun": "娱乐", "games": "娱乐", "movies": "娱乐",
    "medical": "医疗", "health": "医疗", "hospital": "医疗", "pharmacy": "医疗",
    "housing": "住房", "rent": "住房", "utilities": "住房", "mortgage": "住房",
    "education": "教育", "study": "教育", "tuition": "教育", "books": "教育", "course": "教育",
    "travel": "旅行", "trip": "旅行", "vacation": "旅行", "hotel": "旅行",
    "other": "其他", "misc": "其他", "miscellaneous": "其他",
    "salary": "工资", "wage": "工资", "pay": "工资",
    "bonus": "奖金",
    "freelance": "副业", "sidejob": "副业", "side-job": "副业", "gig": "副业",
    # 日本語
    "食費": "餐饮", "交通費": "交通", "買い物": "购物", "娯楽": "娱乐",
    "医療": "医疗", "住居": "住房", "教育費": "教育", "旅行費": "旅行",
    "給料": "工资", "ボーナス": "奖金",
}


def resolve_category(conn, name, tx_type):
    """查找分类，支持多语言别名"""
    # 先直接匹配
    cat = conn.execute(
        "SELECT id, name FROM categories WHERE name = ? AND type = ?",
        (name, tx_type),
    ).fetchone()
    if cat:
        return cat

    # 回退：按名称查找（transfer 类型无对应分类）
    cat = conn.execute(
        "SELECT id, name FROM categories WHERE name = ?", (name,)
    ).fetchone()
    if cat:
        return cat

    # 别名查找（大小写不敏感）
    alias_key = name.lower().strip()
    if alias_key in CATEGORY_ALIASES:
        zh_name = CATEGORY_ALIASES[alias_key]
        cat = conn.execute(
            "SELECT id, name FROM categories WHERE name = ? AND type = ?",
            (zh_name, tx_type),
        ).fetchone()
        if not cat:
            cat = conn.execute(
                "SELECT id, name FROM categories WHERE name = ?", (zh_name,)
            ).fetchone()
        return cat

    return None


def resolve_date(date_str):
    """解析日期字符串，支持 today/yesterday/YYYY-MM-DD"""
    today = datetime.now().date()
    if date_str == "today":
        return today.isoformat()
    if date_str == "yesterday":
        return (today - timedelta(days=1)).isoformat()
    # 尝试解析 YYYY-MM-DD
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        print(f"❌ 无法识别的日期格式：{date_str}，请使用 today/yesterday/YYYY-MM-DD")
        sys.exit(1)


def check_budget(conn, category_id, tx_date):
    """检查预算是否超支，超支时输出警告"""
    if not category_id:
        return

    cat = conn.execute("SELECT name FROM categories WHERE id = ?", (category_id,)).fetchone()
    cat_name = cat["name"] if cat else "未知"

    # 查月度预算
    monthly = conn.execute(
        "SELECT amount FROM budgets WHERE category_id = ? AND period = 'monthly' AND active = 1",
        (category_id,),
    ).fetchone()
    if monthly:
        month_start = tx_date[:7] + "-01"
        month_end = tx_date[:7] + "-31"
        spent = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions "
            "WHERE category_id = ? AND type = 'expense' AND date BETWEEN ? AND ?",
            (category_id, month_start, month_end),
        ).fetchone()[0]
        if spent > monthly["amount"]:
            print(f"⚠️ 本月{cat_name}已超支，当前 ¥{spent:.2f} / 预算 ¥{monthly['amount']:.2f}")

    # 查周度预算
    weekly = conn.execute(
        "SELECT amount FROM budgets WHERE category_id = ? AND period = 'weekly' AND active = 1",
        (category_id,),
    ).fetchone()
    if weekly:
        from datetime import date as date_cls
        d = date_cls.fromisoformat(tx_date)
        week_start = (d - timedelta(days=d.weekday())).isoformat()
        week_end = (d - timedelta(days=d.weekday()) + timedelta(days=6)).isoformat()
        spent_w = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions "
            "WHERE category_id = ? AND type = 'expense' AND date BETWEEN ? AND ?",
            (category_id, week_start, week_end),
        ).fetchone()[0]
        if spent_w > weekly["amount"]:
            print(f"⚠️ 本周{cat_name}已超支，当前 ¥{spent_w:.2f} / 预算 ¥{weekly['amount']:.2f}")

    # 查总预算（monthly）
    total_budget = conn.execute(
        "SELECT amount FROM budgets WHERE category_id IS NULL AND period = 'monthly' AND active = 1",
    ).fetchone()
    if total_budget:
        month_start = tx_date[:7] + "-01"
        month_end = tx_date[:7] + "-31"
        total_spent = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions "
            "WHERE type = 'expense' AND date BETWEEN ? AND ?",
            (month_start, month_end),
        ).fetchone()[0]
        if total_spent > total_budget["amount"]:
            print(f"⚠️ 本月总支出已超预算，当前 ¥{total_spent:.2f} / 预算 ¥{total_budget['amount']:.2f}")


def main():
    parser = argparse.ArgumentParser(description="记录一笔交易")
    parser.add_argument("--amount", type=float, required=True, help="金额")
    parser.add_argument("--type", required=True, choices=["expense", "income", "transfer"], help="类型")
    parser.add_argument("--category", required=True, help="分类名称")
    parser.add_argument("--account", help="账户昵称（不填用默认账户）")
    parser.add_argument("--date", default="today", help="日期：today/yesterday/YYYY-MM-DD")
    parser.add_argument("--note", help="备注")
    parser.add_argument("--merchant", help="商户")
    parser.add_argument("--source", default="nlp", help="来源（默认 nlp）")
    args = parser.parse_args()

    conn = get_conn()

    # 查找分类（支持多语言别名）
    cat = resolve_category(conn, args.category, args.type)
    if not cat:
        print(f"❌ 未找到分类：{args.category}")
        conn.close()
        return
    category_id = cat["id"]

    # 查找账户
    if args.account:
        acc = conn.execute(
            "SELECT id, nickname FROM accounts WHERE nickname = ?", (args.account,)
        ).fetchone()
        if not acc:
            print(f"❌ 未找到账户：{args.account}")
            conn.close()
            return
        account_id = acc["id"]
        account_name = acc["nickname"]
    else:
        # 使用默认账户
        cfg = conn.execute(
            "SELECT value FROM config WHERE key = 'default_account_id'"
        ).fetchone()
        if cfg:
            acc = conn.execute(
                "SELECT id, nickname FROM accounts WHERE id = ?", (int(cfg["value"]),)
            ).fetchone()
            if acc:
                account_id = acc["id"]
                account_name = acc["nickname"]
            else:
                print("❌ 默认账户不存在，请重新设置")
                conn.close()
                return
        else:
            print("❌ 未设置默认账户，请通过 --account 指定或先设置默认账户")
            conn.close()
            return

    tx_date = resolve_date(args.date)

    # 写入交易
    conn.execute(
        "INSERT INTO transactions (amount, type, category_id, account_id, note, merchant, date, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (args.amount, args.type, category_id, account_id, args.note, args.merchant, tx_date, args.source),
    )

    # 更新账户余额
    if args.type == "expense":
        conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (args.amount, account_id))
    elif args.type == "income":
        conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (args.amount, account_id))

    conn.commit()

    type_labels = {"expense": "支出", "income": "收入", "transfer": "转账"}
    cat_display = cat["name"] if cat["name"] != args.category else args.category
    print(f"✅ 已记录：{type_labels.get(args.type, args.type)} ¥{args.amount:.2f} / {cat_display} / {account_name} / {tx_date}")

    # 检查预算
    if args.type == "expense":
        check_budget(conn, category_id, tx_date)

    conn.close()


if __name__ == "__main__":
    main()
