#!/usr/bin/env python3
"""
统一输出工具

所有 cmd.py 通过此模块输出 JSON，保证格式一致。
"""

import io
import json
import sys

from _errors import SkillError, AuthError


def _force_utf8_stdout():
    """强制 stdout 使用 UTF-8 编码。

    Windows 下 stdout 被重定向或被父进程捕获时，Python 会退回
    locale.getpreferredencoding()（中文环境为 cp936/GBK），此时输出中文或 emoji
    会抛 UnicodeEncodeError，导致命令非零退出且没有任何有效输出。这里统一改写为
    UTF-8，并用 errors="replace" 兜底：最坏情况只是个别字符降级为 ?，而不是整条命令失败。
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        # Python < 3.7 无 reconfigure：包一层 TextIOWrapper 达到同样效果
        try:
            sys.stdout = io.TextIOWrapper(
                sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True
            )
        except Exception:
            pass


_force_utf8_stdout()


def make_output(success: bool, markdown: str, data: dict) -> dict:
    return {"success": success, "markdown": markdown, "data": data}

def print_output(success: bool, markdown: str, data: dict):
    """打印标准 JSON 输出（紧凑格式，减少 token 消耗）

    正常情况按 UTF-8 原样输出中文（体积最小）；若极端环境仍无法输出非 ASCII 字符，
    退化为 \\uXXXX 转义（纯 ASCII，任何 code page 都能输出），保证内容一定送得出去。
    """
    payload = make_output(success, markdown, data)
    try:
        print(json.dumps(payload, ensure_ascii=False, separators=(',', ':')))
    except UnicodeEncodeError:
        print(json.dumps(payload, ensure_ascii=True, separators=(',', ':')))

def print_error(e: Exception, default_data: dict = None):
    """将异常转为标准错误输出并打印"""
    if isinstance(e, AuthError):
        msg = f"❌ {e.message}\n\n请运行: `cli.py configure YOUR_AK`"
    elif isinstance(e, SkillError):
        msg = f"❌ {e.message}"
    elif isinstance(e, ValueError):
        msg = f"❌ 参数错误：{e}"
    else:
        msg = f"❌ 操作失败：{e}"
    print_output(False, msg, default_data or {})
