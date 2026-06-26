#!/usr/bin/env python3
"""cashbook 删除交易记录"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_conn


def main():
    parser = argparse.ArgumentParser(description="删除一笔交易记录")
    parser.add_argument("--id", type=int, help="交易 ID（精确删除）")
    parser.add_argument("--last", type=int, metavar="N", help="删除最近第 N 条（1=最新）")
    parser.add_argument("--yes", "-y", action="store_true", help="跳过确认提示")
    args = parser.parse_args()

    if not args.id and not args.last:
        parser.print_help()
        print("\n提示：用 `python3 scripts/query.py --last 10` 查看最近记录的 ID")
        sys.exit(1)

    conn = get_conn()

    # 找目标记录
    if args.id:
        tx = conn.execute(
            """SELECT t.id, t.amount, t.type, t.date, t.note, t.merchant,
                      c.name AS category, a.nickname AS account, a.id AS account_id
               FROM transactions t
               LEFT JOIN categories c ON t.category_id = c.id
               LEFT JOIN accounts a ON t.account_id = a.id
               WHERE t.id = ?""",
            (args.id,),
        ).fetchone()
        if not tx:
            print(f"❌ 未找到 ID={args.id} 的记录")
            conn.close()
            sys.exit(1)
    else:
        tx = conn.execute(
            """SELECT t.id, t.amount, t.type, t.date, t.note, t.merchant,
                      c.name AS category, a.nickname AS account, a.id AS account_id
               FROM transactions t
               LEFT JOIN categories c ON t.category_id = c.id
               LEFT JOIN accounts a ON t.account_id = a.id
               ORDER BY t.created_at DESC
               LIMIT 1 OFFSET ?""",
            (args.last - 1,),
        ).fetchone()
        if not tx:
            print(f"❌ 未找到最近第 {args.last} 条记录")
            conn.close()
            sys.exit(1)

    type_labels = {"expense": "支出", "income": "收入", "transfer": "转账"}
    desc = tx["merchant"] or tx["note"] or ""
    print(f"将删除：ID={tx['id']} | {type_labels.get(tx['type'], tx['type'])} ¥{tx['amount']:.2f} | {tx['category']} | {tx['account']} | {tx['date']}" + (f" | {desc}" if desc else ""))

    if not args.yes:
        confirm = input("确认删除？(y/N) ").strip().lower()
        if confirm != "y":
            print("已取消")
            conn.close()
            return

    # 回滚账户余额
    if tx["account_id"] and tx["type"] in ("expense", "income"):
        if tx["type"] == "expense":
            conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (tx["amount"], tx["account_id"]))
        elif tx["type"] == "income":
            conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (tx["amount"], tx["account_id"]))

    conn.execute("DELETE FROM transactions WHERE id = ?", (tx["id"],))
    conn.commit()
    conn.close()

    print(f"✅ 已删除记录 ID={tx['id']}")


if __name__ == "__main__":
    main()
