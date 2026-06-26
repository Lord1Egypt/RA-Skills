#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post() 调用 1688 API，
不再各自处理 HTTP / 重试 / 错误解析。
"""

import json
import os
import re
import time
import logging
from functools import wraps

import requests

from _auth import get_auth_headers
from _errors import AuthError, ParamError, RateLimitError, ServiceError
from _const import BASE_URL, MAX_RETRIES, RETRY_DELAY_BASE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('1688_http')


def _with_retry(max_retries: int = MAX_RETRIES):
    """仅重试 ConnectionError / Timeout，其余异常直接传播"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError,
                        requests.exceptions.Timeout) as e:
                    last_exc = e
                    delay = min(RETRY_DELAY_BASE * (2 ** attempt), 10)
                    logger.warning("网络异常(尝试%d/%d): %s, %ds后重试",
                                   attempt + 1, max_retries, e, delay)
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            raise ServiceError(f"网络异常，已重试{max_retries}次: {last_exc}")
        return wrapper
    return decorator


def _handle_http_error(e: requests.exceptions.HTTPError):
    """HTTP 状态码 → SkillError"""
    status = e.response.status_code if e.response is not None else None
    if status == 401:
        raise AuthError("签名无效或已过期（401）")
    if status == 429:
        raise RateLimitError("请求被限流（429），请稍后重试")
    if status == 400:
        raise ParamError("请求参数不合法（400）")
    raise ServiceError(f"HTTP 错误 {status}")


def _handle_biz_error(result: dict):
    """业务错误（HTTP 200 但 success=false）→ SkillError"""
    msg_code = str(result.get("msgCode") or "")
    msg_info = result.get("msgInfo")
    code_match = re.search(r"\b(400|401|429|500)\b", msg_code)
    normalized = code_match.group(1) if code_match else ""

    if normalized == "401":
        raise AuthError("签名无效（401）")
    if normalized == "429":
        raise RateLimitError("请求被限流（429）")
    if normalized == "400":
        raise ParamError("请求参数不合法（400）")
    if normalized == "500":
        raise ServiceError("服务异常（500），请稍后重试")

    detail = msg_info or msg_code or "未知业务错误"
    raise ServiceError(str(detail))


@_with_retry()
def api_post(path: str, body: dict = None, timeout: int = 30) -> dict:
    """
    POST 请求 1688 API（自动签名 + 重试 + 错误映射）

    Args:
        path:    API 路径，如 /api/shop_bind_process/1.0.0
        body:    请求体 dict（会 json.dumps）
        timeout: 超时秒数

    Returns:
        API 响应中的 data 字段（dict）

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {}, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")
    headers["Content-Type"] = "application/json; charset=utf-8"

    try:
        resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    result = resp.json()

    # 外层 success 检查
    if result.get("success") is False:
        _handle_biz_error(result)

    # 兼容两种返回格式：
    # 格式A（新网关）：{"result": {"data": ..., "success": true}, "success": true}
    # 格式B（旧网关）：{"data": ..., "success": true}
    if "result" in result and isinstance(result["result"], dict):
        inner = result["result"]
    else:
        inner = result

    # 内层业务 success 检查
    if isinstance(inner, dict) and inner.get("success") is False:
        msg = inner.get("bizMsg") or inner.get("message") or "业务处理失败"
        raise ServiceError(str(msg))

    return inner if isinstance(inner, dict) else {}


def _build_tool_path(tool_name: str) -> str:
    """将工具名称转换为 API 路径。"""
    return f"/api/{tool_name}/1.0.0"


def api_post_tool(tool_name: str, body: dict = None, timeout: int = 30) -> dict:
    """
    按工具名称调用 1688 API 的便捷函数。

    自动将 tool_name 转换为 /api/{tool_name}/1.0.0 路径。
    """
    return api_post(_build_tool_path(tool_name), body, timeout)


@_with_retry()
def api_post_raw(path: str, body: dict = None, timeout: int = 30):
    """
    POST 请求 1688 API，返回 data 字段的原始值（不校验类型）。

    适用于 data 字段非 dict 的接口（如返回 Boolean 的 update 接口）。
    """
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {}, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")
    headers["Content-Type"] = "application/json; charset=utf-8"

    try:
        resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    result = resp.json()
    if result.get("success") is False:
        _handle_biz_error(result)

    # 兼容新旧网关返回格式
    if "result" in result and isinstance(result["result"], dict):
        inner = result["result"]
    else:
        inner = result

    return inner.get("data") if isinstance(inner, dict) else inner


def api_post_tool_raw(tool_name: str, body: dict = None, timeout: int = 30):
    """按工具名称调用 1688 API，返回 data 字段的原始值（不校验类型）。"""
    return api_post_raw(_build_tool_path(tool_name), body, timeout)
