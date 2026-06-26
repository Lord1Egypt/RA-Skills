#!/usr/bin/env python3
"""
cashflow-pilot 共享工具模块

提供数据格式化、输入输出处理、订阅校验、现金流专用辅助函数等通用功能。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


# ============================================================
# 常量定义
# ============================================================

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-bdi", "cashflow-pilot")

# 收支分类关键词映射
INCOME_KEYWORDS: Dict[str, List[str]] = {
    "销售回款": ["销售", "回款", "货款", "收款", "营收", "revenue", "sales"],
    "服务收入": ["服务费", "咨询费", "技术服务", "顾问费", "service"],
    "投资收益": ["利息", "分红", "投资收益", "理财", "interest", "dividend"],
    "其他收入": ["退款", "补贴", "赔偿", "奖励", "返利"],
}

EXPENSE_KEYWORDS: Dict[str, List[str]] = {
    "人员工资": ["工资", "薪资", "社保", "公积金", "奖金", "salary", "payroll"],
    "房租物业": ["房租", "租金", "物业", "水电", "rent"],
    "采购成本": ["采购", "进货", "原材料", "purchase", "procurement"],
    "办公费用": ["办公", "文具", "打印", "耗材", "office"],
    "营销推广": ["广告", "推广", "营销", "市场", "marketing"],
    "差旅费用": ["差旅", "出差", "机票", "住宿", "交通", "travel"],
    "税费": ["税", "增值税", "所得税", "印花税", "tax"],
    "其他支出": ["手续费", "快递", "维修", "杂费"],
}


# ============================================================
# 数字格式化
# ============================================================

def format_number(value: float, decimals: int = 2) -> str:
    """将数字格式化为带千分位分隔符的字符串。

    Args:
        value: 待格式化的数值。
        decimals: 小数位数，默认为 2。

    Returns:
        格式化后的字符串，例如 1234567 → "1,234,567.00"

    Raises:
        TypeError: 当 value 无法转换为数字时抛出。
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"无法将 {value!r} 转换为数字")

    if decimals <= 0:
        return f"{int(round(num)):,}"
    return f"{num:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """将小数格式化为百分比字符串。

    Args:
        value: 待格式化的小数值（0.156 表示 15.6%）。
        decimals: 百分比小数位数，默认为 1。

    Returns:
        百分比字符串，例如 0.156 → "15.6%"

    Raises:
        TypeError: 当 value 无法转换为数字时抛出。
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"无法将 {value!r} 转换为数字")

    pct = num * 100
    return f"{pct:.{decimals}f}%"


def format_chinese_unit(value: float) -> str:
    """将大数字转换为中文单位表示（万、亿）。

    Args:
        value: 待转换的数值。

    Returns:
        带中文单位的字符串，例如:
        - 12345 → "1.23万"
        - 123456789 → "1.23亿"
        - 999 → "999"

    Raises:
        TypeError: 当 value 无法转换为数字时抛出。
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        raise TypeError(f"无法将 {value!r} 转换为数字")

    abs_num = abs(num)
    sign = "-" if num < 0 else ""

    if abs_num >= 1e8:
        result = abs_num / 1e8
        return f"{sign}{result:.2f}亿"
    elif abs_num >= 1e4:
        result = abs_num / 1e4
        return f"{sign}{result:.2f}万"
    else:
        if abs_num == int(abs_num):
            return f"{sign}{int(abs_num)}"
        return f"{sign}{abs_num:.2f}"


def format_currency(value: float, symbol: str = "¥") -> str:
    """将数字格式化为货币字符串。

    Args:
        value: 待格式化的金额。
        symbol: 货币符号，默认 "¥"。

    Returns:
        货币字符串，例如 12345.6 → "¥12,345.60"
    """
    return f"{symbol}{format_number(value, 2)}"


# ============================================================
# JSON 输入输出
# ============================================================

def read_json_stdin() -> Dict[str, Any]:
    """从标准输入读取 JSON 数据并解析为字典。

    Returns:
        解析后的字典对象。

    Raises:
        ValueError: 当输入为空或 JSON 格式不合法时抛出。
    """
    try:
        raw = sys.stdin.read()
    except Exception as e:
        raise ValueError(f"读取标准输入失败: {e}")

    if not raw.strip():
        raise ValueError("标准输入为空，未读取到任何数据")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")

    if not isinstance(data, dict):
        raise ValueError(f"期望输入为 JSON 对象，实际类型为 {type(data).__name__}")

    return data


def output_json(data: Any) -> None:
    """将数据以 JSON 格式输出到标准输出。

    Args:
        data: 待输出的数据（可被 JSON 序列化的任意对象）。
    """
    print(json.dumps(data, ensure_ascii=False, default=str))


def output_error(message: str, code: str = "ERROR") -> None:
    """输出标准错误响应到标准输出。

    Args:
        message: 错误描述信息。
        code: 错误代码，默认为 "ERROR"。
    """
    result = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
    output_json(result)


def output_success(data: Any) -> None:
    """输出标准成功响应到标准输出。

    Args:
        data: 成功时返回的数据负载。
    """
    result = {
        "success": True,
        "data": data,
    }
    output_json(result)


# ============================================================
# 数据目录管理
# ============================================================

def get_data_dir() -> str:
    """获取数据存储目录，若不存在则自动创建。

    优先读取 CFP_DATA_DIR 环境变量，否则使用默认路径。

    Returns:
        数据目录的绝对路径。
    """
    data_dir = os.environ.get("CFP_DATA_DIR", DEFAULT_DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def load_ledger(ledger_file: Optional[str] = None) -> List[Dict[str, Any]]:
    """加载账本数据。

    Args:
        ledger_file: 账本文件路径，默认为数据目录下的 ledger.json。

    Returns:
        账本记录列表。
    """
    if ledger_file is None:
        ledger_file = os.path.join(get_data_dir(), "ledger.json")

    if not os.path.exists(ledger_file):
        return []

    try:
        with open(ledger_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, IOError):
        return []


def save_ledger(records: List[Dict[str, Any]], ledger_file: Optional[str] = None) -> str:
    """保存账本数据。

    Args:
        records: 账本记录列表。
        ledger_file: 账本文件路径，默认为数据目录下的 ledger.json。

    Returns:
        保存的文件路径。
    """
    if ledger_file is None:
        ledger_file = os.path.join(get_data_dir(), "ledger.json")

    os.makedirs(os.path.dirname(ledger_file), exist_ok=True)

    with open(ledger_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2, default=str)

    return ledger_file


# ============================================================
# 订阅校验
# ============================================================

_SUBSCRIPTION_TIERS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": "free",
        "max_reminders": 3,
        "forecast_enabled": False,
        "anomaly_detection": False,
        "bank_statement_parse": False,
        "report_level": "basic",
        "features": ["manual_entry", "csv_import", "basic_report", "limited_reminder"],
    },
    "paid": {
        "tier": "paid",
        "max_reminders": -1,  # -1 表示无限制
        "forecast_enabled": True,
        "anomaly_detection": True,
        "bank_statement_parse": True,
        "report_level": "full",
        "features": [
            "manual_entry",
            "csv_import",
            "excel_import",
            "full_report",
            "unlimited_reminder",
            "forecast",
            "anomaly_detection",
            "bank_statement_parse",
        ],
    },
}


def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 CFP_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典。

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get("CFP_SUBSCRIPTION_TIER", "free")

    tier = tier.strip().lower()

    if tier not in _SUBSCRIPTION_TIERS:
        valid = ", ".join(_SUBSCRIPTION_TIERS.keys())
        raise ValueError(f"无效的订阅等级: {tier!r}，有效等级: {valid}")

    return dict(_SUBSCRIPTION_TIERS[tier])


def require_paid(feature_name: str) -> bool:
    """检查是否为付费用户，若非付费则输出升级提示并返回 False。

    Args:
        feature_name: 功能名称，用于提示信息。

    Returns:
        True 表示已付费可使用，False 表示未付费。
    """
    sub = check_subscription()
    if sub["tier"] != "paid":
        output_error(
            f"「{feature_name}」为付费版功能。当前为免费版，请升级至付费版（¥79/月）以使用此功能。",
            code="SUBSCRIPTION_REQUIRED",
        )
        return False
    return True


# ============================================================
# 收支分类
# ============================================================

def classify_transaction(description: str) -> Dict[str, str]:
    """根据交易描述自动分类收支。

    Args:
        description: 交易描述文本。

    Returns:
        包含 type（income/expense）和 category 的字典。
    """
    desc_lower = description.lower()

    # 先检查收入关键词
    for category, keywords in INCOME_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                return {"type": "income", "category": category}

    # 再检查支出关键词
    for category, keywords in EXPENSE_KEYWORDS.items():
        for kw in keywords:
            if kw in desc_lower:
                return {"type": "expense", "category": category}

    # 默认根据金额方向无法判断时归为其他
    return {"type": "unknown", "category": "未分类"}


def classify_by_amount(amount: float, description: str = "") -> Dict[str, str]:
    """根据金额正负和描述综合分类。

    Args:
        amount: 交易金额，正数为收入，负数为支出。
        description: 交易描述，用于细分分类。

    Returns:
        包含 type 和 category 的字典。
    """
    cls = classify_transaction(description)

    if cls["type"] == "unknown":
        if amount > 0:
            cls["type"] = "income"
            cls["category"] = "其他收入"
        elif amount < 0:
            cls["type"] = "expense"
            cls["category"] = "其他支出"

    return cls


# ============================================================
# 日期辅助
# ============================================================

def parse_date(date_str: str) -> Optional[datetime]:
    """尝试解析多种日期格式。

    支持格式: YYYY-MM-DD, YYYY/MM/DD, YYYYMMDD, DD/MM/YYYY, MM/DD/YYYY

    Args:
        date_str: 日期字符串。

    Returns:
        解析后的 datetime 对象，解析失败返回 None。
    """
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y%m%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M:%S",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]

    date_str = date_str.strip()
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    return None


def get_month_range(year: int, month: int) -> tuple:
    """获取指定月份的起止日期。

    Args:
        year: 年份。
        month: 月份（1-12）。

    Returns:
        (start_date, end_date) 元组。
    """
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(days=1)
    return start, end


# ============================================================
# 命令行参数解析
# ============================================================

def create_parser(description: str) -> argparse.ArgumentParser:
    """创建带通用参数的命令行解析器。

    Args:
        description: 工具描述。

    Returns:
        配置好的 ArgumentParser 实例。
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--action",
        required=True,
        help="执行的操作",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="JSON 格式的输入数据（直接传入字符串）",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help="JSON 数据文件路径",
    )
    parser.add_argument(
        "--file",
        default=None,
        help="待处理的文件路径",
    )
    return parser


def load_input_data(args: argparse.Namespace) -> Optional[Any]:
    """从命令行参数加载输入数据。

    优先使用 --data（JSON 字符串），其次 --data-file（文件路径），
    最后尝试从标准输入读取。

    Args:
        args: 解析后的命令行参数。

    Returns:
        解析后的数据，如果无数据返回 None。
    """
    if args.data:
        try:
            return json.loads(args.data)
        except json.JSONDecodeError as e:
            raise ValueError(f"--data 参数 JSON 解析失败: {e}")

    if args.data_file:
        if not os.path.exists(args.data_file):
            raise ValueError(f"数据文件不存在: {args.data_file}")
        with open(args.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # 检查是否有标准输入
    if not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if raw:
            return json.loads(raw)

    return None
