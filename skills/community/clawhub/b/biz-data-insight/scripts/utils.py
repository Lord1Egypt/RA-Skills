#!/usr/bin/env python3
"""
biz-data-insight 共享工具模块

提供数据格式化、输入输出处理、数据源连接、订阅校验等通用功能。
"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse


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
        # 亿级别
        result = abs_num / 1e8
        return f"{sign}{result:.2f}亿"
    elif abs_num >= 1e4:
        # 万级别
        result = abs_num / 1e4
        return f"{sign}{result:.2f}万"
    else:
        # 不足万，直接返回
        if abs_num == int(abs_num):
            return f"{sign}{int(abs_num)}"
        return f"{sign}{abs_num:.2f}"


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

    使用 ensure_ascii=False 以保留中文等非 ASCII 字符。

    Args:
        data: 待输出的数据（可被 JSON 序列化的任意对象）。
    """
    print(json.dumps(data, ensure_ascii=False, default=str))


def output_error(message: str, code: str = "ERROR") -> None:
    """输出标准错误响应到标准输出。

    输出格式:
        {"success": false, "error": {"code": "<code>", "message": "<message>"}}

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

    输出格式:
        {"success": true, "data": <data>}

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

def parse_common_args() -> argparse.Namespace:
    """创建并解析通用命令行参数。

    支持的参数:
        --type      数据源类型（如 mysql、postgresql、csv、excel、json）
        --uri       数据源连接 URI 或文件路径
        --password  数据源密码（可选）

    Returns:
        解析后的参数命名空间。
    """
    parser = argparse.ArgumentParser(
        description="biz-data-insight 数据分析工具",
    )
    parser.add_argument(
        "--type",
        required=True,
        help="数据源类型，例如: mysql, postgresql, csv, excel, json",
    )
    parser.add_argument(
        "--uri",
        required=True,
        help="数据源连接 URI 或文件路径",
    )
    parser.add_argument(
        "--password",
        default=None,
        help="数据源密码（可选）",
    )
    return parser.parse_args()


# ============================================================
# 数据源连接
# ============================================================

def get_datasource_connection(
    ds_type: str,
    uri: str,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """根据数据源类型和 URI 解析连接参数。

    支持的类型:
        - mysql:      mysql://host:port/db
        - postgresql:  postgresql://host:port/db
        - csv/excel/json: 本地文件路径

    Args:
        ds_type: 数据源类型。
        uri: 连接 URI 或文件路径。
        password: 可选密码，会覆盖 URI 中的密码。

    Returns:
        包含连接参数的字典。

    Raises:
        ValueError: 当类型不支持或 URI 格式无效时抛出。
    """
    ds_type = ds_type.strip().lower()

    # 数据库类型
    if ds_type in ("mysql", "postgresql", "postgres"):
        parsed = urlparse(uri)

        host = parsed.hostname
        port = parsed.port
        database = parsed.path.lstrip("/") if parsed.path else None
        user = parsed.username

        if not host:
            raise ValueError(f"无法从 URI 中解析主机地址: {uri}")
        if not database:
            raise ValueError(f"无法从 URI 中解析数据库名称: {uri}")

        # 设置默认端口
        default_ports = {"mysql": 3306, "postgresql": 5432, "postgres": 5432}
        if port is None:
            port = default_ports.get(ds_type, None)

        # 规范化类型名称
        canonical_type = "postgresql" if ds_type == "postgres" else ds_type

        # 密码优先使用参数传入的，其次使用 URI 中的
        effective_password = password if password is not None else parsed.password

        return {
            "type": canonical_type,
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": effective_password,
        }

    # 文件类型
    elif ds_type in ("csv", "excel", "json"):
        file_path = uri

        if not os.path.exists(file_path):
            raise ValueError(f"文件不存在: {file_path}")

        return {
            "type": ds_type,
            "file_path": os.path.abspath(file_path),
        }

    else:
        supported = "mysql, postgresql, csv, excel, json"
        raise ValueError(f"不支持的数据源类型: {ds_type!r}，支持的类型: {supported}")


# ============================================================
# 订阅校验
# ============================================================

# 订阅等级配置
_SUBSCRIPTION_TIERS: Dict[str, Dict[str, Any]] = {
    "free": {
        "tier": "free",
        "max_datasources": 1,
        "max_rows": 100,
        "daily_questions": 5,
        "features": ["basic_query", "simple_chart"],
    },
    "paid": {
        "tier": "paid",
        "max_datasources": 5,
        "max_rows": 10000,
        "daily_questions": -1,  # -1 表示无限制
        "features": [
            "basic_query",
            "simple_chart",
            "advanced_analysis",
            "export",
            "scheduled_report",
        ],
    },
}


def check_subscription(tier: Optional[str] = None) -> Dict[str, Any]:
    """检查当前订阅等级并返回对应的限制配置。

    优先使用传入的 tier 参数，否则读取环境变量 BDI_SUBSCRIPTION_TIER。
    若都未设置，默认为 "free" 等级。

    Args:
        tier: 订阅等级（"free" 或 "paid"），可选。

    Returns:
        包含订阅限制信息的字典，例如:
        {
            "tier": "free",
            "max_datasources": 1,
            "max_rows": 100,
            "daily_questions": 5,
            "features": ["basic_query", "simple_chart"]
        }

    Raises:
        ValueError: 当传入的等级无效时抛出。
    """
    if tier is None:
        tier = os.environ.get("BDI_SUBSCRIPTION_TIER", "free")

    tier = tier.strip().lower()

    if tier not in _SUBSCRIPTION_TIERS:
        valid = ", ".join(_SUBSCRIPTION_TIERS.keys())
        raise ValueError(f"无效的订阅等级: {tier!r}，有效等级: {valid}")

    # 返回副本，避免外部修改影响全局配置
    return dict(_SUBSCRIPTION_TIERS[tier])


# ============================================================
# SQL 安全校验
# ============================================================

# 禁止的 SQL 关键字模式（DDL / DML / 管理语句）
_FORBIDDEN_SQL_PATTERNS: List[str] = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bTRUNCATE\b",
    r"\bREPLACE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bCALL\b",
    r"\bMERGE\b",
    r"\bRENAME\b",
    r"\bLOAD\b",
    r"\bIMPORT\b",
    r"\bCOPY\b",
]


def validate_sql_readonly(sql: str) -> None:
    """校验 SQL 语句是否为只读查询（仅允许 SELECT）。

    检测并拒绝所有 DDL（数据定义）、DML（数据操作）及管理语句，
    仅允许 SELECT 查询通过。

    Args:
        sql: 待校验的 SQL 语句。

    Raises:
        ValueError: 当检测到非只读操作时抛出，错误信息包含被拦截的关键字。
    """
    if not sql or not sql.strip():
        raise ValueError("SQL 语句不能为空")

    # 移除 SQL 注释（单行 -- 和多行 /* */）
    cleaned = re.sub(r"--[^\n]*", " ", sql)
    cleaned = re.sub(r"/\*.*?\*/", " ", cleaned, flags=re.DOTALL)
    cleaned = cleaned.strip()

    # 检查是否以 SELECT 或 WITH（CTE）开头
    upper = cleaned.upper().lstrip()
    if not (upper.startswith("SELECT") or upper.startswith("WITH") or upper.startswith("(")):
        raise ValueError(
            f"仅允许 SELECT 查询，当前语句以 {cleaned.split()[0]!r} 开头"
        )

    # 检查是否包含禁止的关键字
    for pattern in _FORBIDDEN_SQL_PATTERNS:
        match = re.search(pattern, cleaned, re.IGNORECASE)
        if match:
            keyword = match.group(0).upper()
            raise ValueError(
                f"检测到禁止的 SQL 操作: {keyword}，仅允许只读 SELECT 查询"
            )
