#!/usr/bin/env python3
"""
统一输出工具

所有 cmd.py 通过此模块输出 JSON，保证格式一致。
"""

import argparse
import json

from _errors import AuthError, RateLimitError, ServiceError, SkillError


class JsonArgumentParser(argparse.ArgumentParser):
    """将 argparse 参数错误纳入 CLI 的 JSON 输出与退出码约定。"""

    def error(self, message):
        print_output(False, f"❌ 参数错误：{message}", {})
        raise SystemExit(1)

def make_output(success: bool, markdown: str, data: dict) -> dict:
    return {"success": success, "markdown": markdown, "data": data}


def unwrap_payload(result):
    """解包网关多层 data 信封，返回最内层业务负载（dict 或 list）。

    网关响应形如 {"data": {"data": <payload>, "success": true}, ...}，
    payload 可能是 dict（统计/配置）或 list（属性列表）。
    逐层下钻 `data` 直至取到不再嵌套 `data` 的实际负载。
    """
    node = result.get("data") if isinstance(result, dict) else result
    while isinstance(node, dict) and isinstance(node.get("data"), (dict, list)):
        node = node["data"]
    return node

def print_output(success: bool, markdown: str, data: dict):
    """打印标准 JSON 输出"""
    print(json.dumps(make_output(success, markdown, data), ensure_ascii=False, indent=2))

def print_error(e: Exception, default_data: dict = None):
    """将异常转为标准错误输出并打印，返回约定的进程退出码。"""
    if isinstance(e, AuthError):
        msg = f"❌ {e.message}"
    elif isinstance(e, SkillError):
        msg = f"❌ {e.message}"
    elif isinstance(e, ValueError):
        msg = f"❌ 参数错误：{e}"
    else:
        msg = f"❌ 操作失败：{e}"
    print_output(False, msg, default_data or {})
    if isinstance(e, AuthError):
        return 2
    if isinstance(e, (RateLimitError, ServiceError)):
        return 3
    return 1
