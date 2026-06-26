
"""
辅助函数模块
包含日期、数字格式化等通用辅助函数
"""

from datetime import datetime, date
import re


def format_date(dt, fmt='%Y-%m-%d'):
    if isinstance(dt, str):
        dt = parse_date(dt)
    if isinstance(dt, (date, datetime)):
        return dt.strftime(fmt)
    return ''


def parse_date(date_str):
    if not date_str or not isinstance(date_str, str):
        return None
    date_str = date_str.strip()
    formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%Y%m%d',
        '%Y年%m月%d日',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S'
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if '%H' not in fmt and '%M' not in fmt and '%S' not in fmt:
                return dt.date()
            return dt
        except ValueError:
            continue
    return None


def format_number(num, decimal_places=2):
    num = safe_float(num)
    if num is None:
        return ''
    if isinstance(num, int) or (isinstance(num, float) and num.is_integer()):
        return '{:,}'.format(int(num))
    else:
        return '{:,.{}}'.format(num, decimal_places)


def format_percent(num, decimal_places=2):
    """将小数转换为百分比字符串，总是保留指定小数位"""
    num = safe_float(num)
    if num is None:
        return ''
    percent = num * 100
    return '{:.{}f}%'.format(percent, decimal_places)


def safe_float(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        value = value.strip().replace(',', '')
        try:
            return float(value)
        except ValueError:
            return None
    return None


def safe_int(value):
    float_val = safe_float(value)
    if float_val is None:
        return None
    return int(round(float_val))


def truncate_text(text, max_length=100, suffix='...'):
    if not text or not isinstance(text, str):
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

