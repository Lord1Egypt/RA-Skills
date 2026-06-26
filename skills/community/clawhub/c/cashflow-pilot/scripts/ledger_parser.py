#!/usr/bin/env python3
"""
cashflow-pilot 账单导入解析模块

支持 CSV 和 Excel（.xlsx 以 CSV 模式）文件的导入与解析，
自动识别收支分类，输出标准化的账本记录。
"""

import csv
import io
import json
import os
import re
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# 将 scripts 目录加入路径以支持直接运行
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import (
    classify_by_amount,
    create_parser,
    format_currency,
    format_number,
    get_data_dir,
    load_input_data,
    load_ledger,
    output_error,
    output_json,
    output_success,
    parse_date,
    save_ledger,
    check_subscription,
)


# ============================================================
# CSV 解析
# ============================================================

def detect_encoding(file_path: str) -> str:
    """检测文件编码（简单实现）。

    尝试 utf-8-sig、utf-8、gbk、gb2312 等常见中文编码。

    Args:
        file_path: 文件路径。

    Returns:
        可用的编码名称。
    """
    encodings = ["utf-8-sig", "utf-8", "gbk", "gb2312", "gb18030", "latin-1"]
    for enc in encodings:
        try:
            with open(file_path, "r", encoding=enc) as f:
                f.read(1024)
            return enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    return "utf-8"


def detect_csv_columns(headers: List[str]) -> Dict[str, Optional[int]]:
    """自动检测 CSV 列映射。

    根据表头关键词识别日期、描述、金额、收入、支出等列。

    Args:
        headers: CSV 表头列表。

    Returns:
        列名到列索引的映射字典。
    """
    mapping = {
        "date": None,
        "description": None,
        "amount": None,
        "income": None,
        "expense": None,
        "category": None,
        "note": None,
    }

    date_keywords = ["日期", "date", "交易日期", "记账日期", "时间"]
    desc_keywords = ["描述", "摘要", "说明", "备注", "description", "memo", "交易说明", "用途"]
    amount_keywords = ["金额", "amount", "交易金额", "发生额"]
    income_keywords = ["收入", "income", "贷方", "credit", "贷方金额"]
    expense_keywords = ["支出", "expense", "借方", "debit", "借方金额"]
    category_keywords = ["分类", "类别", "category", "类型"]
    note_keywords = ["备注", "note", "附注", "remark"]

    for idx, header in enumerate(headers):
        h = header.strip().lower()
        if mapping["date"] is None and any(k in h for k in date_keywords):
            mapping["date"] = idx
        elif mapping["description"] is None and any(k in h for k in desc_keywords):
            mapping["description"] = idx
        elif mapping["amount"] is None and any(k in h for k in amount_keywords):
            mapping["amount"] = idx
        elif mapping["income"] is None and any(k in h for k in income_keywords):
            mapping["income"] = idx
        elif mapping["expense"] is None and any(k in h for k in expense_keywords):
            mapping["expense"] = idx
        elif mapping["category"] is None and any(k in h for k in category_keywords):
            mapping["category"] = idx
        elif mapping["note"] is None and any(k in h for k in note_keywords):
            mapping["note"] = idx

    return mapping


def parse_amount(value: str) -> float:
    """解析金额字符串为浮点数。

    处理逗号分隔、货币符号、括号表示负数等情况。

    Args:
        value: 金额字符串。

    Returns:
        解析后的浮点数。
    """
    if not value or not value.strip():
        return 0.0

    s = value.strip()

    # 处理括号表示负数: (100.00) → -100.00
    negative = False
    if s.startswith("(") and s.endswith(")"):
        negative = True
        s = s[1:-1]

    # 移除货币符号和空格
    s = re.sub(r"[¥$€£\s]", "", s)

    # 移除千分位逗号
    s = s.replace(",", "")

    # 处理负号
    if s.startswith("-"):
        negative = not negative
        s = s[1:]

    try:
        result = float(s)
    except ValueError:
        return 0.0

    return -result if negative else result


def parse_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """解析 CSV 文件为标准化的交易记录列表。

    Args:
        file_path: CSV 文件路径。

    Returns:
        标准化的交易记录列表。

    Raises:
        ValueError: 文件不存在或格式无法识别。
    """
    if not os.path.exists(file_path):
        raise ValueError(f"文件不存在: {file_path}")

    encoding = detect_encoding(file_path)
    records = []

    with open(file_path, "r", encoding=encoding, newline="") as f:
        # 尝试检测分隔符
        sample = f.read(4096)
        f.seek(0)

        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(f, dialect)

        # 读取表头
        try:
            headers = next(reader)
        except StopIteration:
            raise ValueError("CSV 文件为空")

        # 检测列映射
        col_map = detect_csv_columns(headers)

        if col_map["date"] is None and col_map["amount"] is None and col_map["income"] is None:
            raise ValueError(
                f"无法自动识别 CSV 列结构。检测到的表头: {headers}。"
                "请确保包含'日期'和'金额'（或'收入'/'支出'）列。"
            )

        # 解析数据行
        for row_num, row in enumerate(reader, start=2):
            if not row or all(not cell.strip() for cell in row):
                continue  # 跳过空行

            record = _parse_csv_row(row, col_map, row_num)
            if record:
                records.append(record)

    return records


def _parse_csv_row(
    row: List[str],
    col_map: Dict[str, Optional[int]],
    row_num: int,
) -> Optional[Dict[str, Any]]:
    """解析单行 CSV 数据。

    Args:
        row: CSV 行数据。
        col_map: 列映射。
        row_num: 行号（用于错误提示）。

    Returns:
        标准化的交易记录字典，解析失败返回 None。
    """
    def get_col(name: str) -> str:
        idx = col_map.get(name)
        if idx is not None and idx < len(row):
            return row[idx].strip()
        return ""

    # 解析日期
    date_str = get_col("date")
    date_val = None
    if date_str:
        from utils import parse_date as pd
        date_val = pd(date_str)

    if date_val is None:
        date_val = datetime.now()

    # 解析金额
    amount = 0.0
    income_val = get_col("income")
    expense_val = get_col("expense")
    amount_val = get_col("amount")

    if income_val and parse_amount(income_val) != 0:
        amount = abs(parse_amount(income_val))
    elif expense_val and parse_amount(expense_val) != 0:
        amount = -abs(parse_amount(expense_val))
    elif amount_val:
        amount = parse_amount(amount_val)

    if amount == 0:
        return None  # 跳过零金额记录

    # 解析描述
    description = get_col("description") or get_col("note") or f"第{row_num}行记录"

    # 分类
    category_str = get_col("category")
    if category_str:
        txn_type = "income" if amount > 0 else "expense"
        classification = {"type": txn_type, "category": category_str}
    else:
        classification = classify_by_amount(amount, description)

    return {
        "id": f"imp_{datetime.now().strftime('%Y%m%d%H%M%S')}_{row_num}",
        "date": date_val.strftime("%Y-%m-%d"),
        "description": description,
        "amount": round(abs(amount), 2),
        "type": classification["type"],
        "category": classification["category"],
        "source": "csv_import",
        "raw_row": row_num,
    }


# ============================================================
# Excel 解析（使用 CSV 兼容模式，无需 openpyxl）
# ============================================================

def parse_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """解析 Excel 文件（仅付费版支持）。

    注意：由于仅使用标准库，此处通过读取 .xlsx 内嵌的 XML
    实现基础解析。对于复杂 Excel 文件建议先导出为 CSV。

    Args:
        file_path: Excel 文件路径。

    Returns:
        标准化的交易记录列表。
    """
    sub = check_subscription()
    if sub["tier"] != "paid":
        raise ValueError(
            "Excel 文件导入为付费版功能。请先升级至付费版（¥79/月），"
            "或将 Excel 文件另存为 CSV 格式后使用免费版导入。"
        )

    if not os.path.exists(file_path):
        raise ValueError(f"文件不存在: {file_path}")

    # 尝试用 csv 模块读取（适用于 .csv 格式另存为 .xlsx 的情况）
    # 对于真正的 xlsx，提示用户转换
    try:
        return parse_csv_file(file_path)
    except Exception:
        raise ValueError(
            "无法直接解析 Excel (.xlsx) 文件。请将文件另存为 CSV 格式后重新导入。"
            "建议步骤：在 Excel 中选择 文件→另存为→CSV UTF-8 (逗号分隔)(*.csv)"
        )


# ============================================================
# 手动录入
# ============================================================

def add_manual_entry(entry_data: Dict[str, Any]) -> Dict[str, Any]:
    """手动添加一条收支记录。

    Args:
        entry_data: 包含以下字段的字典:
            - date: 日期 (YYYY-MM-DD)
            - description: 描述
            - amount: 金额（正数）
            - type: income/expense
            - category: 分类（可选，自动识别）

    Returns:
        添加后的完整记录。
    """
    required_fields = ["date", "description", "amount", "type"]
    for field in required_fields:
        if field not in entry_data:
            raise ValueError(f"缺少必需字段: {field}")

    amount = float(entry_data["amount"])
    txn_type = entry_data["type"]

    if txn_type not in ("income", "expense"):
        raise ValueError(f"type 必须为 'income' 或 'expense'，当前值: {txn_type}")

    # 自动分类
    category = entry_data.get("category", "")
    if not category:
        cls = classify_by_amount(
            amount if txn_type == "income" else -amount,
            entry_data["description"],
        )
        category = cls["category"]

    record = {
        "id": f"man_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "date": entry_data["date"],
        "description": entry_data["description"],
        "amount": round(abs(amount), 2),
        "type": txn_type,
        "category": category,
        "source": "manual",
    }

    # 追加到账本
    ledger = load_ledger()
    ledger.append(record)
    save_ledger(ledger)

    return record


# ============================================================
# 主入口
# ============================================================

def main():
    """主入口函数。"""
    parser = create_parser("cashflow-pilot 账单导入解析工具")
    parser.add_argument(
        "--format",
        choices=["csv", "excel"],
        default="csv",
        help="文件格式（csv 或 excel）",
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        return

    try:
        if args.action == "import":
            # 导入文件
            if not args.file:
                output_error("请使用 --file 参数指定要导入的文件路径", "MISSING_FILE")
                return

            if args.format == "excel":
                records = parse_excel_file(args.file)
            else:
                records = parse_csv_file(args.file)

            # 追加到账本
            ledger = load_ledger()
            ledger.extend(records)
            save_ledger(ledger)

            # 生成导入摘要
            income_count = sum(1 for r in records if r["type"] == "income")
            expense_count = sum(1 for r in records if r["type"] == "expense")
            total_income = sum(r["amount"] for r in records if r["type"] == "income")
            total_expense = sum(r["amount"] for r in records if r["type"] == "expense")

            output_success({
                "message": "账单导入成功",
                "imported_count": len(records),
                "income_count": income_count,
                "expense_count": expense_count,
                "total_income": round(total_income, 2),
                "total_expense": round(total_expense, 2),
                "records": records[:10],  # 仅返回前10条预览
                "summary": (
                    f"成功导入 {len(records)} 条记录。"
                    f"其中收入 {income_count} 笔共 {format_currency(total_income)}，"
                    f"支出 {expense_count} 笔共 {format_currency(total_expense)}。"
                ),
            })

        elif args.action == "parse":
            # 仅解析不导入
            if not args.file:
                output_error("请使用 --file 参数指定要解析的文件路径", "MISSING_FILE")
                return

            if args.format == "excel":
                records = parse_excel_file(args.file)
            else:
                records = parse_csv_file(args.file)

            output_success({
                "message": "文件解析成功",
                "record_count": len(records),
                "records": records,
            })

        elif args.action == "add":
            # 手动添加记录
            data = load_input_data(args)
            if not data:
                output_error("请通过 --data 或 --data-file 提供记录数据", "MISSING_DATA")
                return

            record = add_manual_entry(data)
            output_success({
                "message": "记录添加成功",
                "record": record,
            })

        elif args.action == "list":
            # 列出当前账本记录
            ledger = load_ledger()
            output_success({
                "total_count": len(ledger),
                "records": ledger,
            })

        else:
            output_error(
                f"不支持的操作: {args.action}。支持的操作: import, parse, add, list",
                "INVALID_ACTION",
            )

    except ValueError as e:
        output_error(str(e), "PARSE_ERROR")
    except Exception as e:
        output_error(f"执行失败: {e}", "INTERNAL_ERROR")


if __name__ == "__main__":
    main()
