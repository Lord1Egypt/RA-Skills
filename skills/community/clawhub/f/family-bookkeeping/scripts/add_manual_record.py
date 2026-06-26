#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WRITE_SCRIPT = SCRIPT_DIR / "write_feishu_records.py"
DEFAULT_APP_TOKEN = os.getenv("FAMILY_BOOKKEEPING_APP_TOKEN", "")
DEFAULT_TABLE_ID = os.getenv("FAMILY_BOOKKEEPING_TABLE_ID", "")


def infer_date(text: str, now: datetime) -> str:
    if "前天" in text:
        dt = now - timedelta(days=2)
    elif "昨天" in text:
        dt = now - timedelta(days=1)
    else:
        dt = now
    return dt.strftime("%Y-%m-%d")


def infer_category(note: str):
    t = note.lower()
    if any(k in note for k in ["午饭", "中午", "烧鸭饭", "米饭", "盖饭", "面", "粉", "饭"]):
        return "餐饮", "午饭"
    if any(k in note for k in ["早饭", "早餐"]):
        return "餐饮", "早饭"
    if any(k in note for k in ["晚饭", "晚餐", "夜宵"]):
        return "餐饮", "晚饭"
    if any(k in note for k in ["咖啡", "瑞幸", "库迪", "星巴克"]):
        return "餐饮", "咖啡"
    if any(k in note for k in ["停车"]):
        return "交通", "停车"
    if any(k in note for k in ["打车", "滴滴", "出租车"]):
        return "交通", "打车"
    return "其他", "暂未分类"


def main():
    parser = argparse.ArgumentParser(description="Add one manual bookkeeping record to the shared Bitable.")
    parser.add_argument("text", help="Natural-language text or note")
    parser.add_argument("--amount", required=True, type=float)
    parser.add_argument("--bookkeeper", default="张三")
    parser.add_argument("--income-expense", default="支出")
    parser.add_argument("--platform", default="手动")
    parser.add_argument("--source", default="手动记账")
    parser.add_argument("--app-token", default=DEFAULT_APP_TOKEN)
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID)
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""))
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""))
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        raise SystemExit("Need --app-id and --app-secret, or FEISHU_APP_ID / FEISHU_APP_SECRET in env")

    now = datetime.now()
    date_str = infer_date(args.text, now)
    cat1, cat2 = infer_category(args.text)
    note = args.text.strip()

    row = [{
        "日期": date_str,
        "金额": str(args.amount),
        "记账人": args.bookkeeper,
        "一级类型": cat1,
        "二级类型": cat2,
        "备注": note,
        "收支类型": args.income_expense,
        "支付平台": args.platform,
        "导入来源": args.source,
        "流水号": ""
    }]

    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as tmp:
        json.dump(row, tmp, ensure_ascii=False, indent=2)
        tmp_path = tmp.name

    cmd = [
        sys.executable,
        str(WRITE_SCRIPT),
        tmp_path,
        "--app-token", args.app_token,
        "--table-id", args.table_id,
        "--app-id", args.app_id,
        "--app-secret", args.app_secret,
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        raise SystemExit(proc.returncode)

    print(json.dumps({
        "written": True,
        "record": row[0],
        "write_result": json.loads(proc.stdout)
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
=2))


if __name__ == "__main__":
    main()
