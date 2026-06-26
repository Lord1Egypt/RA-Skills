#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据映射器

功能：根据配置映射字段并应用数据转换（含验证）
"""

import re
from datetime import datetime
from typing import Any, Optional


def map_fields(source_row, field_mappings) -> Any:
    """映射字段

    Args:
        source_row: 源数据行字典
        field_mappings: 字段映射配置

    Returns:
        dict: 映射后的数据
    """
    mapped_data = {}

    for mapping in field_mappings:
        source_field = mapping["source"]
        target_field = mapping["target"]

        value = source_row.get(source_field)

        if value is None and "default" in mapping:
            value = mapping["default"]

        if value is not None and "transform" in mapping:
            params = mapping.get("transform_params", {})
            value = apply_transforms(value, mapping["transform"], params)

        mapped_data[target_field] = value

    return mapped_data


def apply_transforms(value: Any, transform_type: str, params: Optional[dict] = None) -> Any:
    """应用数据转换

    Args:
        value: 原始值
        transform_type: 转换类型（strip/upper/lower/title/int/float/date）
        params: 转换参数（如日期格式的 input_format/output_format）

    Returns:
        转换后的值
    """
    if value is None:
        return None

    params = params or {}

    # 字符串转换
    if isinstance(value, str):
        if transform_type == "strip":
            return value.strip()
        elif transform_type == "upper":
            return value.upper()
        elif transform_type == "lower":
            return value.lower()
        elif transform_type == "title":
            return value.title()
        elif transform_type == "int":
            try:
                return int(float(str(value).strip().replace(",", "")))
            except (ValueError, TypeError):
                return value
        elif transform_type == "float":
            try:
                return float(str(value).strip().replace(",", ""))
            except (ValueError, TypeError):
                return value
        elif transform_type == "date":
            return _transform_date(value, params)
        elif transform_type == "date_to_excel":
            """将日期字符串转为 Excel 日期数值"""
            result = _parse_date(value, params)
            return result if result is not None else value
    # 数值转字符串
    elif isinstance(value, (int, float)):
        if transform_type == "str":
            return str(value)
        elif transform_type == "int":
            return int(value)
        elif transform_type == "float":
            return float(value)

    return value


def _parse_date(value: str, params: dict) -> Any:
    """解析日期字符串

    Args:
        value: 日期字符串
        params: {"input_format": "%Y-%m-%d", "output_format": "%Y年%m月%d日"}

    Returns:
        解析后的值（取决于参数）
    """
    input_format = params.get("input_format", "%Y-%m-%d")

    # 常见格式自动尝试
    formats_to_try = [
        input_format,
        "%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日",
        "%Y%m%d", "%d/%m/%Y", "%m/%d/%Y",
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
    ]

    for fmt in formats_to_try:
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            continue

    # 尝试 Excel 日期数值（整数，代表从1900-01-01起的天数）
    try:
        num = float(str(value))
        if 1 <= num <= 100000:
            from datetime import timedelta
            return datetime(1899, 12, 30) + timedelta(days=num)
    except (ValueError, TypeError):
        pass

    return value


def _transform_date(value: str, params: dict) -> Any:
    """日期格式转换

    Args:
        value: 日期字符串
        params: {
            "input_format": "%Y-%m-%d",
            "output_format": "%Y年%m月%d日"
        }

    Returns:
        格式化后的日期字符串，解析失败返回原值
    """
    parsed = _parse_date(value, params)

    if isinstance(parsed, datetime):
        output_format = params.get("output_format", "%Y-%m-%d")
        return parsed.strftime(output_format)

    return value


# ============================================================
# 验证引擎
# ============================================================

# 身份证号正则（18位）
_ID_CARD_18 = re.compile(r'^[1-9]\d{5}(19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$')
# 身份证号正则（15位旧版）
_ID_CARD_15 = re.compile(r'^[1-9]\d{5}\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}$')
# 手机号正则
_PHONE = re.compile(r'^1[3-9]\d{9}$')
# 邮箱正则
_EMAIL = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def validate_field(value: Any, validate_type: str, params: Optional[dict] = None) -> tuple:
    """验证单个字段

    Args:
        value: 字段值
        validate_type: 验证规则名
        params: 验证参数

    Returns:
        (is_valid: bool, error_message: str or None)
    """
    params = params or {}

    if validate_type == "required" or validate_type == "not_empty":
        if value is None or (isinstance(value, str) and value.strip() == ""):
            msg = params.get("message", "此字段为必填项")
            return False, msg
        return True, None

    if value is None or (isinstance(value, str) and value.strip() == ""):
        # 非必填字段为空时跳过验证
        return True, None

    str_value = str(value).strip()

    if validate_type == "id_card":
        if _ID_CARD_18.match(str_value) or _ID_CARD_15.match(str_value):
            return True, None
        msg = params.get("message", f"身份证号格式错误: {str_value}")
        return False, msg

    elif validate_type == "phone":
        clean = re.sub(r'[\s\-+]', '', str_value)
        if _PHONE.match(clean):
            return True, None
        msg = params.get("message", f"手机号格式错误: {str_value}")
        return False, msg

    elif validate_type == "email":
        if _EMAIL.match(str_value):
            return True, None
        msg = params.get("message", f"邮箱格式错误: {str_value}")
        return False, msg

    elif validate_type == "numeric":
        try:
            float(str_value.replace(",", ""))
            return True, None
        except ValueError:
            msg = params.get("message", f"数值格式错误: {str_value}")
            return False, msg

    elif validate_type == "range":
        try:
            num = float(str_value.replace(",", ""))
            min_val = params.get("min")
            max_val = params.get("max")
            if min_val is not None and num < min_val:
                msg = params.get("message", f"值 {num} 小于最小值 {min_val}")
                return False, msg
            if max_val is not None and num > max_val:
                msg = params.get("message", f"值 {num} 大于最大值 {max_val}")
                return False, msg
            return True, None
        except ValueError:
            msg = params.get("message", f"范围验证失败，非数值: {str_value}")
            return False, msg

    elif validate_type == "regex":
        pattern = params.get("pattern")
        if pattern and re.match(pattern, str_value):
            return True, None
        msg = params.get("message", f"格式不匹配: {str_value}")
        return False, msg

    elif validate_type == "length":
        min_len = params.get("min", 0)
        max_len = params.get("max")
        if min_len and len(str_value) < min_len:
            msg = params.get("message", f"长度不能少于 {min_len} 个字符")
            return False, msg
        if max_len and len(str_value) > max_len:
            msg = params.get("message", f"长度不能超过 {max_len} 个字符")
            return False, msg
        return True, None

    # 未知验证类型，跳过
    return True, None
