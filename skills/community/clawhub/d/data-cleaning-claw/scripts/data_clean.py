#!/usr/bin/env python3
"""
data_clean.py - 数据自动化清洗脚本
依赖：pandas, numpy, openpyxl, beautifulsoup4
安装：pip install pandas numpy openpyxl beautifulsoup4
"""

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd


# ── 工具函数 ──────────────────────────────────────────────

def load_data(path: str) -> pd.DataFrame:
    p = Path(path)
    ext = p.suffix.lower()
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path, dtype=str)
    elif ext == ".csv":
        return pd.read_csv(path, dtype=str)
    elif ext == ".json":
        return pd.read_json(path, dtype=str)
    else:
        raise ValueError(f"不支持的文件格式：{ext}，请使用 CSV/Excel/JSON")


def save_data(df: pd.DataFrame, path: str):
    p = Path(path)
    ext = p.suffix.lower()
    if ext in (".xlsx", ".xls"):
        df.to_excel(path, index=False)
    elif ext == ".csv":
        df.to_csv(path, index=False, encoding="utf-8-sig")
    elif ext == ".json":
        df.to_json(path, orient="records", force_ascii=False, indent=2)
    else:
        df.to_csv(path, index=False, encoding="utf-8-sig")


def strip_html(text: str) -> str:
    """去除 HTML 标签，转换常见 HTML 实体"""
    try:
        from bs4 import BeautifulSoup
        return BeautifulSoup(text, "html.parser").get_text(separator=" ")
    except ImportError:
        text = re.sub(r"<[^>]+>", " ", text)
        entities = {"&nbsp;": " ", "&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"'}
        for k, v in entities.items():
            text = text.replace(k, v)
        return text


def clean_text(text: str) -> str:
    """通用文本清洗：去首尾空格、控制字符、零宽字符、全角空格"""
    if not isinstance(text, str):
        return text
    # 零宽字符 & 控制字符（保留 \n \t）
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f\u200b\u200c\u200d\ufeff\u3000]", "", text)
    text = text.strip()
    return text


def normalize_date(val: str) -> str:
    """尝试将各种日期格式统一为 YYYY-MM-DD"""
    if not isinstance(val, str) or not val.strip():
        return val
    try:
        parsed = pd.to_datetime(val, dayfirst=False, errors="raise")
        return parsed.strftime("%Y-%m-%d")
    except Exception:
        return val  # 无法解析，原样返回（后续标记为异常）


def normalize_amount(val: str) -> str:
    """去除货币符号、千分位，统一为数值字符串"""
    if not isinstance(val, str) or not val.strip():
        return val
    cleaned = re.sub(r"[¥$€£￥,\s]", "", val)
    # 处理括号负数 (1200) → -1200
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = "-" + cleaned[1:-1]
    try:
        return str(float(cleaned))
    except ValueError:
        return val


def normalize_phone(val: str) -> str:
    """统一手机号为 11 位纯数字"""
    if not isinstance(val, str) or not val.strip():
        return val
    digits = re.sub(r"[\s\-\(\)\+]", "", val)
    if digits.startswith("86") and len(digits) == 13:
        digits = digits[2:]
    return digits


def is_null(val) -> bool:
    if val is None:
        return True
    if isinstance(val, float) and np.isnan(val):
        return True
    if isinstance(val, str) and val.strip().lower() in ("", "null", "n/a", "nan", "none", "-", "na"):
        return True
    return False


# ── 清洗步骤 ──────────────────────────────────────────────

def step_deduplicate(df: pd.DataFrame, key_fields=None) -> tuple[pd.DataFrame, dict]:
    before = len(df)
    if key_fields:
        fields = [f.strip() for f in key_fields.split(",") if f.strip() in df.columns]
        df = df.drop_duplicates(subset=fields, keep="first")
    else:
        df = df.drop_duplicates(keep="first")
    removed = before - len(df)
    return df.reset_index(drop=True), {"去重删除行数": removed}


def step_fill_missing(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    log = {}
    for col in df.columns:
        null_mask = df[col].apply(is_null)
        count = null_mask.sum()
        if count == 0:
            continue
        # 尝试判断列类型
        non_null = df.loc[~null_mask, col]
        try:
            numeric = pd.to_numeric(non_null, errors="raise")
            fill_val = str(round(numeric.median(), 4))
            df.loc[null_mask, col] = fill_val
            log[col] = f"填充中位数 {fill_val}（{count} 处）"
        except Exception:
            df.loc[null_mask, col] = "未知"
            log[col] = f"填充'未知'（{count} 处）"
    return df, {"缺失值处理": log}


def step_standardize(df: pd.DataFrame, date_fields=None, amount_fields=None, phone_fields=None) -> tuple[pd.DataFrame, dict]:
    log = {}

    def auto_detect(col_name: str, sample: pd.Series) -> str:
        name = col_name.lower()
        if any(k in name for k in ("日期", "date", "time", "时间")):
            return "date"
        if any(k in name for k in ("金额", "amount", "price", "费用", "价格", "收入", "支出")):
            return "amount"
        if any(k in name for k in ("手机", "电话", "phone", "mobile", "tel")):
            return "phone"
        return "text"

    for col in df.columns:
        dtype = auto_detect(col, df[col])
        if date_fields and col in date_fields.split(","):
            dtype = "date"
        if amount_fields and col in amount_fields.split(","):
            dtype = "amount"
        if phone_fields and col in phone_fields.split(","):
            dtype = "phone"

        if dtype == "date":
            df[col] = df[col].apply(normalize_date)
            log[col] = "日期格式标准化"
        elif dtype == "amount":
            df[col] = df[col].apply(normalize_amount)
            log[col] = "金额格式标准化"
        elif dtype == "phone":
            df[col] = df[col].apply(normalize_phone)
            log[col] = "电话号码标准化"
        else:
            df[col] = df[col].apply(clean_text)

    return df, {"格式标准化": log}


def step_strip_html(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    count = 0
    for col in df.columns:
        mask = df[col].apply(lambda v: isinstance(v, str) and bool(re.search(r"<[a-zA-Z/]", v)))
        if mask.any():
            df.loc[mask, col] = df.loc[mask, col].apply(strip_html)
            count += mask.sum()
    return df, {"HTML去噪处理列数": int(count)}


def step_validate(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    flags = pd.Series([""] * len(df), index=df.index)
    issues = {}

    for col in df.columns:
        name = col.lower()
        if any(k in name for k in ("手机", "phone", "mobile")):
            bad = df[col].apply(lambda v: isinstance(v, str) and v.strip() and not re.fullmatch(r"1[3-9]\d{9}", v.strip()))
            if bad.any():
                flags[bad] += f"[{col}格式异常]"
                issues[col] = f"{bad.sum()} 条手机号格式异常"
        if any(k in name for k in ("邮箱", "email", "mail")):
            bad = df[col].apply(lambda v: isinstance(v, str) and v.strip() and not re.fullmatch(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", v.strip(), re.I))
            if bad.any():
                flags[bad] += f"[{col}格式异常]"
                issues[col] = f"{bad.sum()} 条邮箱格式异常"
        if any(k in name for k in ("年龄", "age")):
            try:
                nums = pd.to_numeric(df[col], errors="coerce")
                bad = (nums < 0) | (nums > 150)
                if bad.any():
                    flags[bad] += f"[{col}异常值]"
                    issues[col] = f"{bad.sum()} 条年龄异常"
            except Exception:
                pass

    if flags.str.strip().any():
        df["_数据质量标记"] = flags
    return df, {"数据验证": issues}


# ── 主流程 ────────────────────────────────────────────────

def run_clean(args):
    print(f"📂 读取数据：{args.input}")
    df = load_data(args.input)
    total_rows = len(df)
    print(f"   共 {total_rows} 行，{len(df.columns)} 列")

    report = {"原始行数": total_rows, "原始列数": len(df.columns), "操作日志": {}}

    rules = [r.strip() for r in args.rules.split(",")]

    if "strip-html" in rules:
        df, log = step_strip_html(df)
        report["操作日志"].update(log)
        print(f"✅ HTML去噪完成")

    if "standardize" in rules:
        df, log = step_standardize(df, args.date_fields, args.amount_fields, args.phone_fields)
        report["操作日志"].update(log)
        print(f"✅ 格式标准化完成")

    if "deduplicate" in rules:
        df, log = step_deduplicate(df, args.key_fields)
        report["操作日志"].update(log)
        print(f"✅ 去重完成，删除 {log['去重删除行数']} 行")

    if "fill-missing" in rules:
        df, log = step_fill_missing(df)
        report["操作日志"].update(log)
        print(f"✅ 缺失值处理完成")

    if "validate" in rules:
        df, log = step_validate(df)
        report["操作日志"].update(log)
        print(f"✅ 数据验证完成")

    report["清洗后行数"] = len(df)
    report["清洗后列数"] = len(df.columns)
    report["数据质量提升"] = f"删除 {total_rows - len(df)} 行脏数据"

    save_data(df, args.output)
    print(f"\n💾 已保存清洗结果：{args.output}")

    # 输出报告
    report_path = Path(args.output).with_suffix(".report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"📊 清洗报告：{report_path}")
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="数据自动化清洗脚本")
    parser.add_argument("--input", required=True, help="输入文件路径（CSV/Excel/JSON）")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument(
        "--rules",
        default="strip-html,deduplicate,fill-missing,standardize,validate",
        help="清洗规则，逗号分隔：strip-html,deduplicate,fill-missing,standardize,validate"
    )
    parser.add_argument("--key-fields", default=None, help="去重关键字段，逗号分隔（不填则全字段去重）")
    parser.add_argument("--date-fields", default=None, help="强制指定为日期字段，逗号分隔")
    parser.add_argument("--amount-fields", default=None, help="强制指定为金额字段，逗号分隔")
    parser.add_argument("--phone-fields", default=None, help="强制指定为电话字段，逗号分隔")
    args = parser.parse_args()
    run_clean(args)


if __name__ == "__main__":
    main()
