#!/usr/bin/env python3
"""
统一输出工具

所有 cmd.py 通过此模块输出 JSON，保证格式一致。
"""

import json
import sys

from _errors import SkillError, AuthError

# Windows 中文环境 stdout 默认为 cp936，无法编码 ¥ / 📄 / ❌ 等字符，
# 会直接抛 UnicodeEncodeError 使命令失败；强制改为 UTF-8 输出。
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass  # 旧版本或 stdout 已被替换为不支持 reconfigure 的对象


def make_output(success: bool, markdown: str, data: dict) -> dict:
    return {"success": success, "markdown": markdown, "data": data}


def print_output(success: bool, markdown: str, data: dict):
    """打印标准 JSON 输出（紧凑格式，减少 token 消耗）"""
    print(json.dumps(make_output(success, markdown, data), ensure_ascii=False, separators=(',', ':')))


def print_error(e: Exception, default_data: dict = None):
    """将异常转为标准错误输出并打印"""
    if isinstance(e, AuthError):
        msg = f"❌ {e.message}\n\n请在 Accio Desktop 环境内运行，并确认已登录、当前商家已授权后重试。"
    elif isinstance(e, SkillError):
        msg = f"❌ {e.message}"
    elif isinstance(e, ValueError):
        msg = f"❌ 参数错误：{e}"
    else:
        msg = f"❌ 操作失败：{e}"
    print_output(False, msg, default_data or {})
