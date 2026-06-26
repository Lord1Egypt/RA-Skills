#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一体化脚本共享模块
提供 API 调用和数据处理的共享工具函数
"""

import hashlib
import random
import time
import requests
from typing import Dict, Any, List, Optional

# API 配置 - 从环境变量获取
import os

UID = os.environ.get('CHINADAAS_UID')
KEY = os.environ.get('CHINADAAS_KEY')
BASE_URL = os.environ.get('CHINADAAS_BASE_URL')

# 调试开关
DEBUG = False


def debug_print(*args, **kwargs):
    """调试打印函数"""
    if DEBUG:
        print(*args, **kwargs)


# ============ API 调用相关函数 ============

def encrypt(text: str) -> str:
    """
    SHA1 加密函数

    Args:
        text: 待加密的字符串

    Returns:
        加密后的十六进制字符串
    """
    try:
        sha1 = hashlib.sha1()
        sha1.update(text.encode())
        message_digest = sha1.digest()
        hex_string = ""
        for byte in message_digest:
            sha_hex = hex(byte & 0xFF)[2:]
            if len(sha_hex) < 2:
                hex_string += '0'
            hex_string += sha_hex
        return hex_string
    except Exception as e:
        debug_print(f"加密函数出错: {str(e)}")
        return ""


def get_headers() -> dict:
    """
    生成 API 请求头

    Returns:
        包含认证信息的请求头字典
    """
    timestamp = str(int(time.time() * 1000))
    nonce = str(random.randint(0, 999999))
    signature = encrypt(f"{nonce};{KEY};{timestamp};{UID};")

    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Uid': UID,
        'X-Nonce': nonce,
        'X-Timestamp': timestamp,
        'X-Signature': signature
    }


def call_api(endpoint: str, params: dict = None, method: str = 'GET') -> dict:
    """
    统一 API 调用函数

    Args:
        endpoint: API 端点路径 (如 '/entinfo')
        params: 请求参数
        method: 请求方法 ('GET' 或 'POST')

    Returns:
        API 响应的 JSON 数据
    """
    url = BASE_URL + endpoint
    headers = get_headers()
    params = params or {}

    try:
        if method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=params, timeout=30)
        else:
            response = requests.get(url, headers=headers, params=params, timeout=30)

        return response.json()
    except requests.exceptions.Timeout:
        debug_print(f"API 请求超时: {endpoint}")
        return {'code': -1, 'message': '请求超时'}
    except requests.exceptions.RequestException as e:
        debug_print(f"API 请求异常: {str(e)}")
        return {'code': -1, 'message': f'请求异常: {str(e)}'}
    except Exception as e:
        debug_print(f"API 调用失败: {str(e)}")
        return {'code': -1, 'message': f'调用失败: {str(e)}'}


# ============ 数据处理相关函数 ============

def format_number(value: str) -> str:
    """
    格式化数字，去除无意义的小数位

    Args:
        value: 数字字符串，可能包含 % 符号

    Returns:
        格式化后的数字字符串

    Example:
        >>> format_number("100.00")
        '100'
        >>> format_number("3.50%")
        '3.5%'
    """
    if not value:
        return value

    try:
        clean_value = value.strip().rstrip('%')
        num = float(clean_value)

        if num == int(num):
            result = str(int(num))
        else:
            result = str(num).rstrip('0').rstrip('.')

        if value.strip().endswith('%'):
            return result + '%'
        return result
    except (ValueError, TypeError):
        return value


def safe_get(data: dict, path: str, default: Any = '') -> Any:
    """
    安全获取嵌套字典中的值

    Args:
        data: 目标字典
        path: 用点分隔的路径，如 "level1.level2.key"
        default: 默认值

    Returns:
        获取到的值或默认值
    """
    if not data or not isinstance(data, dict):
        return default

    keys = path.split('.')
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current if current is not None else default


def filter_empty_values(data: dict) -> dict:
    """
    过滤字典中的空值

    Args:
        data: 目标字典

    Returns:
        过滤后的字典
    """
    if not isinstance(data, dict):
        return data

    return {
        k: v for k, v in data.items()
        if v is not None and v != '' and v != [] and v != {}
    }


def to_markdown_section(title: str, content: str) -> str:
    """
    将内容格式化为 Markdown 章节

    Args:
        title: 章节标题
        content: 章节内容

    Returns:
        格式化的 Markdown 字符串
    """
    if not content or content.strip() == '':
        return f"### {title}\n暂无数据"
    return f"### {title}\n{content}"


def truncate_text(text: str, max_length: int = 200, suffix: str = '...') -> str:
    """
    截断过长的文本

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后的后缀

    Returns:
        截断后的文本
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length] + suffix


def format_list_to_string(items: List[str], separator: str = '、', max_items: int = 10) -> str:
    """
    将列表格式化为字符串

    Args:
        items: 字符串列表
        separator: 分隔符
        max_items: 最多显示的项目数

    Returns:
        格式化后的字符串
    """
    if not items:
        return ''

    filtered = [str(item) for item in items if item]

    if len(filtered) > max_items:
        filtered = filtered[:max_items]

    return separator.join(filtered)


def extract_money_amount(value: str, unit: str = '万元') -> str:
    """
    提取并格式化金额

    Args:
        value: 金额字符串
        unit: 金额单位

    Returns:
        格式化后的金额字符串
    """
    formatted = format_number(value)
    if formatted and formatted != '0':
        return f"{formatted}{unit}"
    return ''


__all__ = [
    # API 相关
    'UID', 'KEY', 'BASE_URL',
    'encrypt', 'get_headers', 'call_api',
    # 数据处理相关
    'format_number', 'safe_get', 'filter_empty_values',
    'to_markdown_section', 'truncate_text',
    'format_list_to_string', 'extract_money_amount',
    # 调试
    'debug_print', 'DEBUG',
]
