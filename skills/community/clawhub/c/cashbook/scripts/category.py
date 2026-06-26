#!/usr/bin/env python3
"""cashbook 分类管理"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_conn


def cmd_list(args):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, name, type, icon, builtin FROM categories ORDER BY type, builtin DESC, id"
    ).fetchall()
    conn.close()

    if not rows:
        print("暂无分类")
        return

    expense = [r for r in rows if r["type"] == "expense"]
    income = [r for r in rows if r["type"] == "income"]

    for label, group in [("📤 支出分类", expense), ("📥 收入分类", income)]:
        if not group:
            continue
        print(f"\n{label}")
        print("-" * 40)
        for r in group:
            icon = r["icon"] or " "
            tag = "  [预置]" if r["builtin"] else ""
            print(f"  {r['id']:>3}  {icon}  {r['name']}{tag}")
    print()


def cmd_add(args):
    if not args.name:
        print("❌ 请指定分类名：--name")
        return
    if args.type not in ("expense", "income"):
        print("❌ 类型必须为 expense 或 income")
        return

    conn = get_conn()
    existing = conn.execute(
        "SELECT id FROM categories WHERE name = ? AND type = ?",
        (args.name, args.type),
    ).fetchone()
    if existing:
        print(f"❌ 分类 \"{args.name}\"（{args.type}）已存在")
        conn.close()
        return

    conn.execute(
        "INSERT INTO categories (name, type, icon, builtin) VALUES (?, ?, ?, 0)",
        (args.name, args.type, args.icon),
    )
    conn.commit()
    conn.close()
    print(f"✅ 已添加分类：{args.name}（{args.type}）")


def cmd_delete(args):
    if not args.id:
        print("❌ 请指定分类 ID：--id")
        return

    conn = get_conn()
    cat = conn.execute("SELECT * FROM categories WHERE id = ?", (args.id,)).fetchone()
    if not cat:
        print(f"❌ 未找到 ID 为 {args.id} 的分类")
        conn.close()
        return

    if cat["builtin"]:
        print(f"❌ 预置分类「{cat['name']}」不可删除")
        conn.close()
        return

    conn.execute("DELETE FROM categories WHERE id = ?", (args.id,))
    conn.commit()
    conn.close()
    print(f"✅ 分类「{cat['name']}」已删除")


def main():
    parser = argparse.ArgumentParser(description="cashbook 分类管理")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="列出所有分类")

    p_add = sub.add_parser("add", help="添加自定义分类")
    p_add.add_argument("--name", required=True, help="分类名称")
    p_add.add_argument("--type", required=True, choices=["expense", "income"], help="类型")
    p_add.add_argument("--icon", help="Emoji 图标（可选）")

    p_del = sub.add_parser("delete", help="删除自定义分类")
    p_del.add_argument("--id", type=int, required=True, help="分类 ID")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    {"list": cmd_list, "add": cmd_add, "delete": cmd_delete}[args.command](args)


if __name__ == "__main__":
    main()
