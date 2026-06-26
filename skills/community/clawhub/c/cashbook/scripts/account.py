#!/usr/bin/env python3
"""cashbook 账户管理"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_conn

TYPE_CHOICES = ["debit", "credit", "wallet"]
TYPE_LABELS = {"debit": "储蓄卡", "credit": "信用卡", "wallet": "钱包"}


def fmt_table(headers, rows):
    """简单的 ASCII 对齐表格"""
    widths = [len(h) for h in headers]
    str_rows = []
    for row in rows:
        cells = [str(c) if c is not None else "" for c in row]
        str_rows.append(cells)
        for i, c in enumerate(cells):
            # 中文字符占 2 宽度
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


def cmd_add(args):
    conn = get_conn()
    balance = args.balance if args.balance is not None else 0.0

    conn.execute(
        "INSERT INTO accounts (nickname, type, last4, balance) VALUES (?, ?, ?, ?)",
        (args.nickname, args.type, args.last4, balance),
    )
    conn.commit()
    acc_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    print(f"✅ 已添加账户：{args.nickname}（ID: {acc_id}）")


def cmd_list(args):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, nickname, type, last4, balance FROM accounts ORDER BY id"
    ).fetchall()
    conn.close()

    if not rows:
        print("暂无账户，请先添加：python3 scripts/account.py add")
        return

    headers = ["ID", "昵称", "类型", "尾号", "余额"]
    data = [
        (str(r["id"]), r["nickname"], TYPE_LABELS.get(r["type"], r["type"]),
         r["last4"] or "-", f'{r["balance"]:.2f}')
        for r in rows
    ]
    fmt_table(headers, data)


def cmd_edit(args):
    if not args.id:
        print("❌ 请指定账户 ID：--id")
        return

    conn = get_conn()
    acc = conn.execute("SELECT * FROM accounts WHERE id = ?", (args.id,)).fetchone()
    if not acc:
        print(f"❌ 未找到 ID 为 {args.id} 的账户")
        conn.close()
        return

    updates = []
    params = []
    if args.nickname:
        updates.append("nickname = ?")
        params.append(args.nickname)
    if args.last4:
        updates.append("last4 = ?")
        params.append(args.last4)
    if args.balance is not None:
        updates.append("balance = ?")
        params.append(args.balance)

    if not updates:
        print("❌ 请指定要修改的字段：--nickname / --last4 / --balance")
        conn.close()
        return

    params.append(args.id)
    conn.execute(f"UPDATE accounts SET {', '.join(updates)} WHERE id = ?", params)
    conn.commit()
    conn.close()
    print(f"✅ 账户 {args.id} 已更新")


def cmd_delete(args):
    if not args.id:
        print("❌ 请指定账户 ID：--id")
        return

    conn = get_conn()
    tx_count = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE account_id = ?", (args.id,)
    ).fetchone()[0]

    if tx_count > 0:
        print(f"❌ 账户 {args.id} 有 {tx_count} 条流水记录，无法删除。请先删除相关流水。")
        conn.close()
        return

    deleted = conn.execute("DELETE FROM accounts WHERE id = ?", (args.id,)).rowcount
    conn.commit()
    conn.close()
    if deleted:
        print(f"✅ 账户 {args.id} 已删除")
    else:
        print(f"❌ 未找到 ID 为 {args.id} 的账户")


def cmd_default(args):
    if not args.id:
        print("❌ 请指定账户 ID：--id")
        return

    conn = get_conn()
    acc = conn.execute("SELECT * FROM accounts WHERE id = ?", (args.id,)).fetchone()
    if not acc:
        print(f"❌ 未找到 ID 为 {args.id} 的账户")
        conn.close()
        return

    conn.execute(
        "INSERT OR REPLACE INTO config (key, value) VALUES ('default_account_id', ?)",
        (str(args.id),),
    )
    conn.commit()
    conn.close()
    print(f"✅ 已将默认账户设为：{acc['nickname']}（ID: {args.id}）")


def main():
    parser = argparse.ArgumentParser(description="cashbook 账户管理")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="添加账户")
    p_add.add_argument("--nickname", required=True, help="账户昵称")
    p_add.add_argument("--type", required=True, choices=TYPE_CHOICES, help="账户类型")
    p_add.add_argument("--last4", help="卡号尾号")
    p_add.add_argument("--balance", type=float, help="初始余额")

    sub.add_parser("list", help="列出所有账户")

    p_edit = sub.add_parser("edit", help="编辑账户")
    p_edit.add_argument("--id", type=int, required=True, help="账户 ID")
    p_edit.add_argument("--nickname", help="新昵称")
    p_edit.add_argument("--last4", help="新尾号")
    p_edit.add_argument("--balance", type=float, help="新余额")

    p_del = sub.add_parser("delete", help="删除账户")
    p_del.add_argument("--id", type=int, required=True, help="账户 ID")

    p_def = sub.add_parser("default", help="设置默认账户")
    p_def.add_argument("--id", type=int, required=True, help="账户 ID")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    {"add": cmd_add, "list": cmd_list, "edit": cmd_edit,
     "delete": cmd_delete, "default": cmd_default}[args.command](args)


if __name__ == "__main__":
    main()
