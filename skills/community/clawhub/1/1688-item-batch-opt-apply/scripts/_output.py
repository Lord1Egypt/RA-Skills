#!/usr/bin/env python3
"""
统一输出工具

所有 cmd.py 通过此模块输出 JSON，保证格式一致：
    {"success": bool, "markdown": str, "data": {...}}
"""

import json
import sys

from _errors import SkillError


def make_output(success: bool, markdown: str, data: dict) -> dict:
    return {"success": success, "markdown": markdown, "data": data}


def print_output(success: bool, markdown: str, data: dict):
    """打印标准 JSON 输出"""
    print(json.dumps(make_output(success, markdown, data), ensure_ascii=False, indent=2))


def print_error(e: Exception, default_data: dict = None):
    """将异常转为标准错误输出并打印"""
    if isinstance(e, SkillError):
        msg = "❌ {}".format(e.message)
    elif isinstance(e, ValueError):
        msg = "❌ 参数错误：{}".format(e)
    else:
        msg = "❌ 操作失败：{}".format(e)
    print_output(False, msg, default_data or {})


def configure_windows_stdio():
    """Windows 控制台默认 GBK，强制 UTF-8 输出，避免中文 markdown 乱码。"""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")  # py3.7+
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
