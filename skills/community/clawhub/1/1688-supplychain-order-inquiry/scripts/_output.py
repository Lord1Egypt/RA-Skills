#!/usr/bin/env python3
"""
统一输出工具

所有 cmd.py 通过此模块输出 JSON，保证格式一致。
输出格式：{"success": bool, "markdown": str, "data": {...}}
"""

import json

from _errors import SkillError, AuthError, ParamError, RateLimitError, TimeoutError


def make_output(success: bool, markdown: str, data: dict) -> dict:
    return {"success": success, "markdown": markdown, "data": data}


def print_output(success: bool, markdown: str, data: dict):
    """打印标准 JSON 输出"""
    print(json.dumps(make_output(success, markdown, data), ensure_ascii=False, indent=2))


# 错误类型 -> 行动建议
_ERROR_HINTS = {
    AuthError: "请检查 ALI_1688_AK 环境变量是否已配置，或确认 AK 是否有效。",
    ParamError: "请检查传入的参数是否正确。",
    RateLimitError: "请等待 1-2 分钟后重试。",
    TimeoutError: "接口响应较慢，已内置自动重试。如仍失败，请稍后再试。",
}


def print_error(e: Exception, default_data: dict = None):
    """将异常转为标准错误输出并打印，自动附加行动建议"""
    if isinstance(e, SkillError):
        msg = "{}".format(e.message)
        # 按异常子类匹配行动建议
        for err_type, hint in _ERROR_HINTS.items():
            if isinstance(e, err_type):
                msg += "\n\n**建议**: {}".format(hint)
                break
    elif isinstance(e, ValueError):
        msg = "参数错误：{}".format(e)
    else:
        msg = "操作失败：{}\n\n**建议**: 如反复出现，请检查网络连接或稍后重试。".format(e)
    print_output(False, msg, default_data or {})
