#!/usr/bin/env python3
"""统一输出工具"""

import json
from _errors import SkillError, AuthError

def make_output(success: bool, markdown: str, data: dict) -> dict:
    return {"success": success, "markdown": markdown, "data": data}

def print_output(success: bool, markdown: str, data: dict):
    print(json.dumps(make_output(success, markdown, data), ensure_ascii=False, indent=2))

def print_error(e: Exception, default_data: dict = None):
    if isinstance(e, AuthError):
        msg = f"❌ {e.message}\n\n请运行: `cli.py configure YOUR_AK`"
    elif isinstance(e, SkillError):
        msg = f"❌ {e.message}"
    elif isinstance(e, ValueError):
        msg = f"❌ 参数错误：{e}"
    else:
        msg = f"❌ 操作失败：{e}"
    print_output(False, msg, default_data or {})
