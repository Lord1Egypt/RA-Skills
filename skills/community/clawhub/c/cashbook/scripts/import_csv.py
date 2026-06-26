#!/usr/bin/env python3
"""cashbook CSV 账单导入（支付宝 / 微信）"""

import argparse
import csv
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import get_conn

# ── 分类映射规则 ──────────────────────────────────────────────
CATEGORY_RULES = [
    (["餐饮", "外卖", "美团", "饿了么", "咖啡", "奶茶", "星巴克", "麦当劳", "肯德基"], "餐饮"),
    (["滴滴", "出行", "地铁", "公交", "打车", "加油"], "交通"),
    (["超市", "便利店", "盒马", "京东", "淘宝", "天猫", "拼多多"], "购物"),
    (["电影", "游戏", "娱乐", "KTV", "旅行", "酒店"], "娱乐"),
    (["医院", "药店", "医疗"], "医疗"),
    (["房租", "物业", "水电"], "住房"),
    (["学费", "培训", "书", "课程"], "教育"),
    (["工资", "薪资", "salary"], "工资"),
    (["奖金", "bonus"], "奖金"),
]


def match_category(text, tx_type):
    """根据文本匹配分类名"""
    for keywords, cat_name in CATEGORY_RULES:
        for kw in keywords:
            if kw in text:
                return cat_name
    return "其他"


def parse_amount(raw):
    """清理金额字符串，去掉 ¥ 符号和空格"""
    return float(raw.replace("¥", "").replace(",", "").strip())


def parse_date(raw):
    """将时间字符串转为 YYYY-MM-DD"""
    raw = raw.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw[:10]


def detect_format(rows):
    """根据列名自动检测支付宝/微信格式，返回 'alipay' | 'wechat' | None"""
    if not rows:
        return None
    header = [h.strip() for h in rows[0]]
    joined = ",".join(header)
    if "交易订单号" in joined:
        return "alipay"
    if "交易单号" in joined:
        return "wechat"
    return None


def read_csv_rows(filepath):
    """读取 CSV 文件，尝试不同的跳行数来检测格式"""
    encodings = ["utf-8-sig", "gbk", "gb18030"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                all_lines = f.readlines()
            break
        except (UnicodeDecodeError, UnicodeError):
            continue
    else:
        print(f"❌ 无法识别文件编码：{filepath}")
        sys.exit(1)

    # 尝试支付宝（跳过前 4 行）和微信（跳过前 16 行）
    for skip in (4, 16, 0):
        if skip >= len(all_lines):
            continue
        lines = all_lines[skip:]
        reader = csv.reader(lines)
        rows = list(reader)
        fmt = detect_format(rows)
        if fmt:
            return fmt, rows

    # 无法识别，原样返回
    reader = csv.reader(all_lines)
    rows = list(reader)
    return None, rows


def parse_alipay(rows):
    """解析支付宝 CSV 记录"""
    records = []
    header = [h.strip() for h in rows[0]]
    for row in rows[1:]:
        if len(row) < len(header):
            continue
        item = {h: v.strip() for h, v in zip(header, row)}

        # 只导入交易成功的
        status = item.get("交易状态", "")
        if "交易成功" not in status:
            records.append(("skip_status", item))
            continue

        direction = item.get("收/支", "").strip()
        if direction == "支出":
            tx_type = "expense"
        elif direction == "收入":
            tx_type = "income"
        else:
            records.append(("skip_status", item))
            continue

        amount = parse_amount(item.get("金额", item.get("金额(元)", "0")))
        date = parse_date(item.get("交易时间", ""))
        merchant = item.get("交易对方", "")
        note = item.get("商品说明", item.get("商品", ""))
        category_text = item.get("交易分类", "") + " " + note + " " + merchant
        cat_name = match_category(category_text, tx_type)

        records.append(("ok", {
            "amount": amount,
            "type": tx_type,
            "date": date,
            "merchant": merchant,
            "note": note,
            "category": cat_name,
        }))

    return records


def parse_wechat(rows):
    """解析微信 CSV 记录"""
    records = []
    header = [h.strip() for h in rows[0]]
    for row in rows[1:]:
        if len(row) < len(header):
            continue
        item = {h: v.strip() for h, v in zip(header, row)}

        status = item.get("当前状态", "")
        if status not in ("支付成功", "已存入零钱"):
            records.append(("skip_status", item))
            continue

        direction = item.get("收/支", "").strip()
        if direction == "支出":
            tx_type = "expense"
        elif direction == "收入":
            tx_type = "income"
        else:
            records.append(("skip_status", item))
            continue

        amount = parse_amount(item.get("金额(元)", item.get("金额", "0")))
        date = parse_date(item.get("交易时间", ""))
        merchant = item.get("交易对方", "")
        note = item.get("商品", "")
        category_text = item.get("交易类型", "") + " " + note + " " + merchant
        cat_name = match_category(category_text, tx_type)

        records.append(("ok", {
            "amount": amount,
            "type": tx_type,
            "date": date,
            "merchant": merchant,
            "note": note,
            "category": cat_name,
        }))

    return records


def ensure_category(conn, name, tx_type):
    """确保分类存在，返回 category_id"""
    cat = conn.execute(
        "SELECT id FROM categories WHERE name = ? AND type = ?",
        (name, tx_type),
    ).fetchone()
    if cat:
        return cat["id"]
    conn.execute(
        "INSERT INTO categories (name, type, icon, builtin) VALUES (?, ?, '📦', 0)",
        (name, tx_type),
    )
    conn.commit()
    return conn.execute(
        "SELECT id FROM categories WHERE name = ? AND type = ?",
        (name, tx_type),
    ).fetchone()["id"]


def is_duplicate(conn, date, amount, merchant):
    """检查是否已有相同日期+金额+商户的记录"""
    row = conn.execute(
        "SELECT COUNT(*) FROM transactions WHERE date = ? AND amount = ? AND merchant = ?",
        (date, amount, merchant),
    ).fetchone()
    return row[0] > 0


def do_import(filepath, account_name, dry_run=False):
    fmt, rows = read_csv_rows(filepath)
    if not fmt:
        print("❌ 无法识别 CSV 格式（支持支付宝/微信账单）")
        sys.exit(1)

    if fmt == "alipay":
        records = parse_alipay(rows)
        print(f"检测到支付宝账单格式")
    else:
        records = parse_wechat(rows)
        print(f"检测到微信账单格式")

    conn = get_conn()

    # 查找账户
    account_id = None
    if account_name:
        acc = conn.execute(
            "SELECT id FROM accounts WHERE nickname = ?", (account_name,)
        ).fetchone()
        if not acc:
            print(f"❌ 未找到账户：{account_name}")
            conn.close()
            return
        account_id = acc["id"]

    imported = 0
    skipped_dup = 0
    skipped_status = 0

    for status, item in records:
        if status == "skip_status":
            skipped_status += 1
            continue

        rec = item
        # 重复检测
        if is_duplicate(conn, rec["date"], rec["amount"], rec["merchant"]):
            skipped_dup += 1
            continue

        if dry_run:
            imported += 1
            continue

        cat_id = ensure_category(conn, rec["category"], rec["type"])
        conn.execute(
            "INSERT INTO transactions (amount, type, category_id, account_id, note, merchant, date, source) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, 'import')",
            (rec["amount"], rec["type"], cat_id, account_id, rec["note"], rec["merchant"], rec["date"]),
        )

        # 更新账户余额
        if account_id:
            if rec["type"] == "expense":
                conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (rec["amount"], account_id))
            elif rec["type"] == "income":
                conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (rec["amount"], account_id))

        imported += 1

    if not dry_run:
        conn.commit()
    conn.close()

    total = imported + skipped_dup + skipped_status
    mode = "（预览模式，未写入）" if dry_run else ""
    print(f"\n解析完成：共 {total} 条记录{mode}")
    print(f"  导入：{imported} 条")
    print(f"  跳过（重复）：{skipped_dup} 条")
    print(f"  跳过（非成功状态）：{skipped_status} 条")


def main():
    parser = argparse.ArgumentParser(
        description="导入支付宝/微信账单 CSV 文件",
        epilog=(
            "示例:\n"
            "  python3 scripts/import_csv.py --file ~/Downloads/alipay_record.csv --account 支付宝\n"
            "  python3 scripts/import_csv.py --file ~/Downloads/wechat_record.csv --account 微信钱包\n"
            "  python3 scripts/import_csv.py --file xx.csv --dry-run\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file", required=True, help="CSV 文件路径")
    parser.add_argument("--account", help="导入到的账户昵称")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不写入数据库")
    args = parser.parse_args()

    filepath = os.path.expanduser(args.file)
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在：{filepath}")
        sys.exit(1)

    do_import(filepath, args.account, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
