# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import re
from typing import Any, Optional, Tuple


def parse_numeric_with_unit(value: Any) -> Tuple[Optional[float], Optional[str]]:
    """
    解析带单位的数值

    Args:
        value: 输入值，如 "5mV", "12.5V", 100等

    Returns:
        (数值, 单位) 元组，如 (5.0, "mV") 或 (100.0, None)
    """
    if isinstance(value, (int, float)):
        return float(value), None

    value_str = str(value).strip()

    # 如果为空
    if not value_str:
        return None, None

    # 尝试直接转换为数值
    try:
        return float(value_str), None
    except ValueError:
        pass

    # 匹配数值和单位
    # 支持格式: 5mV, 12.5V, -3.14uA, +5kHz
    pattern = r'^([+-]?\d+\.?\d*)\s*([a-zA-Zμµ]+)?$'
    match = re.match(pattern, value_str)

    if match:
        numeric_part = float(match.group(1))
        unit_part = match.group(2) if match.group(2) else None
        return numeric_part, unit_part

    return None, None


def normalize_unit(unit: Optional[str]) -> str:
    """
    标准化单位表示

    Args:
        unit: 原始单位

    Returns:
        标准化后的单位
    """
    if not unit:
        return ""

    # 统一微米符号
    unit = unit.replace('μ', 'u').replace('µ', 'u')

    # 常见单位标准化映射
    unit_mapping = {
        'mV': 'mV',
        'V': 'V',
        'mA': 'mA',
        'A': 'A',
        'uA': 'μA',
        'μA': 'μA',
        'nA': 'nA',
        'kHz': 'kHz',
        'MHz': 'MHz',
        'GHz': 'GHz',
        'Hz': 'Hz',
        'ohm': 'Ω',
        'Ohm': 'Ω',
        'OHM': 'Ω',
    }

    return unit_mapping.get(unit, unit)


def format_value(value: float, precision: int = 2) -> str:
    """
    格式化数值显示

    Args:
        value: 数值
        precision: 小数位数

    Returns:
        格式化后的字符串
    """
    if value == int(value):
        return str(int(value))
    return f"{value:.{precision}f}"


def truncate_string(s: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    截断过长的字符串

    Args:
        s: 原始字符串
        max_length: 最大长度
        suffix: 截断后缀

    Returns:
        截断后的字符串
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def validate_file_path(file_path: str, extensions: Optional[Tuple[str, ...]] = None) -> bool:
    """
    验证文件路径是否有效

    Args:
        file_path: 文件路径
        extensions: 允许的扩展名元组，如 ('.xls', '.xlsx')

    Returns:
        是否有效
    """
    import os

    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False

    # 检查是否为文件
    if not os.path.isfile(file_path):
        return False

    # 检查扩展名
    if extensions:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in extensions:
            return False

    return True
