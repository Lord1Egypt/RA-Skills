#!/usr/bin/env python3
"""
customer-pulse 共享工具模块

提供客户数据管理、订阅校验、数据格式化等通用功能。
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

DEFAULT_DATA_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-bdi", "customer-pulse")

STAGES = ["初步接触", "需求确认", "方案报价", "谈判", "成交", "流失"]

STAGE_COLORS = {
    "初步接触": "blue",
    "需求确认": "cyan",
    "方案报价": "yellow",
    "谈判": "orange",
    "成交": "green",
    "流失": "red",
}


# ============================================================
# 数据目录管理
# ============================================================

def get_data_dir() -> str:
    """获取数据存储目录路径。

    优先读取环境变量 CP_DATA_DIR，若未设置则使用默认路径
    ~/.openclaw-bdi/customer-pulse/。
    自动创建目录（若不存在）。

    Returns:
        数据目录的绝对路径。
    """
    data_dir = os.environ.get("CP_DATA_DIR", DEFAULT_DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_data_file(filename: str) -> str:
    """获取数据文件的完整路径。

    Args:
        filename: 文件名（如 "customers.json"）。

    Returns:
        数据文件的绝对路径。
    """
    return os.path.join(get_data_dir(), filename)


# ============================================================
# JSON 输入输出
# ============================================================

def read_json_file(filepath: str) -> Any:
    """读取 JSON 文件并返回解析后的数据。

    Args:
        filepath: JSON 文件路径。

    Returns:
        解析后的数据对象。若文件不存在，返回空列表。
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def write_json_file(filepath: str, data: Any) -> None:
    """将数据写入 JSON 文件。

    Args:
        filepath: 目标文件路径。
        data: 待写入的数据。
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)


def output_json(data: Any) -> None:
    """将数据以 JSON 格式输出到标准输出。

    Args:
        data: 待输出的数据。
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
# 命令行参数解析
# ============================================================

def parse_common_args(description: str = "customer-pulse 客户管理工具") -> argparse.ArgumentParser:
    """创建通用命令行参数解析器。

    Args:
        description: 工具描述文本。

    Returns:
        配置好通用参数的 ArgumentParser 实例。
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "--action",
        required=True,
        help="操作类型",
    )
    parser.add_argument(
        "--data",
        default=None,
        help="JSON 格式的数据字符串",
    )
    parser.add_argument(
        "--data-file",
        default=None,
        help="JSON 数据文件路径",
    )
    return parser


def load_input_data(args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    """从命令行参数加载输入数据。

    优先使用 --data 参数，其次尝试 --data-file 参数。

    Args:
        args: 解析后的命令行参数。

    Returns:
        解析后的字典数据，若无输入数据则返回 None。

    Raises:
        ValueError: 当 JSON 解析失败或文件读取失败时抛出。
    """
    if args.data:
        try:
            data = json.loads(args.data)
            if not isinstance(data, dict):
                raise ValueError(f"期望 JSON 对象，实际类型为 {type(data).__name__}")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析失败: {e}")

    if args.data_file:
        if not os.path.exists(args.data_file):
            raise ValueError(f"数据文件不存在: {args.data_file}")
        try:
            with open(args.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError(f"期望 JSON 对象，实际类型为 {type(data).__name__}")
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"数据文件 JSON 解析失败: {e}")

    return None


# ============================================================
# 订阅校验
# ============================================================

_SUBSCRIPTION_TIERS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": "free",
        "max_customers": 50,
        "followup_reminder": "fixed",
        "reminder_days": 3,
        "features": ["customer_crud", "followup_record", "basic_list", "csv_export", "csv_import"],
    },
    "paid": {
        "tier": "paid",
        "max_customers": 500,
        "followup_reminder": "custom",
        "reminder_days": None,
        "features": [
            "customer_crud",
            "followup_record",
            "basic_list",
            "csv_export",
            "csv_import",
            "bulk_import",
            "funnel_chart",
            "heatmap",
            "churn_prediction",
            "customer_profile",
            "conversion_analysis",
            "custom_reminder",
            "mermaid_chart",
        ],
    },
}


def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 CP_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典。

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get("CP_SUBSCRIPTION_TIER", "free")

    tier = tier.strip().lower()

    if tier not in _SUBSCRIPTION_TIERS:
        valid = ", ".join(_SUBSCRIPTION_TIERS.keys())
        raise ValueError(f"无效的订阅等级: {tier!r}，有效等级: {valid}")

    return dict(_SUBSCRIPTION_TIERS[tier])


def require_paid_feature(feature_name: str, display_name: str) -> bool:
    """检查当前订阅是否支持指定功能。

    若不支持，输出升级提示并返回 False。

    Args:
        feature_name: 功能内部名称。
        display_name: 功能显示名称（用于提示信息）。

    Returns:
        True 表示功能可用，False 表示不可用（已输出错误信息）。
    """
    sub = check_subscription()
    if feature_name not in sub["features"]:
        output_error(
            f"「{display_name}」为付费版功能。当前为免费版，请升级至付费版（¥99/月）以使用此功能。",
            code="SUBSCRIPTION_REQUIRED",
        )
        return False
    return True


# ============================================================
# CRM 专用工具函数
# ============================================================

def stage_display_name(stage: str) -> str:
    """获取销售阶段的显示名称。

    Args:
        stage: 阶段标识。

    Returns:
        阶段显示名称，若未知则返回原始值。
    """
    if stage in STAGES:
        return stage
    return stage


def validate_stage(stage: str) -> str:
    """校验销售阶段是否合法。

    Args:
        stage: 待校验的阶段名称。

    Returns:
        合法的阶段名称。

    Raises:
        ValueError: 当阶段名称不合法时抛出。
    """
    if stage not in STAGES:
        valid = "、".join(STAGES)
        raise ValueError(f"无效的销售阶段: {stage!r}，有效阶段: {valid}")
    return stage


def calculate_days_since(date_str: str) -> int:
    """计算从指定日期到今天的天数。

    Args:
        date_str: 日期字符串，格式为 YYYY-MM-DD 或 ISO 格式。

    Returns:
        距今天数（正数表示过去，负数表示未来）。
    """
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            dt = dt.replace(tzinfo=None)
        else:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - dt
        return delta.days
    except (ValueError, TypeError):
        return 0


def mask_phone(phone: str) -> str:
    """对手机号进行脱敏处理。

    将手机号中间 4 位替换为 ****。

    Args:
        phone: 原始手机号。

    Returns:
        脱敏后的手机号，如 138****8000。
        若格式不符合，返回原始值。
    """
    if not phone:
        return phone
    phone = phone.strip()
    if re.match(r"^1[3-9]\d{9}$", phone):
        return phone[:3] + "****" + phone[7:]
    return phone


def generate_id(prefix: str = "C") -> str:
    """生成唯一 ID。

    基于时间戳生成，格式为 前缀+时间戳。

    Args:
        prefix: ID 前缀，默认为 "C"（客户）。

    Returns:
        唯一 ID 字符串。
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{prefix}{timestamp}"


def format_currency(value: float) -> str:
    """将数值格式化为人民币金额显示。

    Args:
        value: 金额数值。

    Returns:
        格式化后的金额字符串，如 "¥10.00万" 或 "¥5,000"。
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        return str(value)

    abs_num = abs(num)
    sign = "-" if num < 0 else ""

    if abs_num >= 1e8:
        return f"{sign}¥{abs_num / 1e8:.2f}亿"
    elif abs_num >= 1e4:
        return f"{sign}¥{abs_num / 1e4:.2f}万"
    else:
        return f"{sign}¥{abs_num:,.0f}"


def now_iso() -> str:
    """返回当前时间的 ISO 格式字符串。

    Returns:
        ISO 格式时间字符串，如 "2026-03-19T10:30:00"。
    """
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def today_str() -> str:
    """返回今天的日期字符串。

    Returns:
        日期字符串，格式为 "YYYY-MM-DD"。
    """
    return datetime.now().strftime("%Y-%m-%d")
