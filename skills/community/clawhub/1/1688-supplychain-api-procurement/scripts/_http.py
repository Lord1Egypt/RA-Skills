#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post(path, body) 调用网关 API。
网关地址：https://skills-gateway.1688.com
"""

import json
import sys
import time
from functools import wraps

import requests

from _auth import get_auth_headers
from _errors import AuthError, ParamError, RateLimitError, ServiceError, TimeoutError

BASE_URL = "https://skills-gateway.1688.com"
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1


class _RetryableError(Exception):
    """内部重试信号，不对外暴露"""
    pass


def _with_retry(max_retries: int = MAX_RETRIES):
    """重试 ConnectionError / Timeout / _RetryableError，其余异常直接传播"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (requests.exceptions.ConnectionError,
                        _RetryableError) as e:
                    last_exc = e
                    delay = min(RETRY_DELAY_BASE * (2 ** attempt), 10)
                    print("请求异常(尝试{}/{}): {}, {}s后重试".format(
                        attempt + 1, max_retries, e, delay), file=sys.stderr)
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            # 重试耗尽，区分超时和其他错误
            if "超时" in str(last_exc):
                raise TimeoutError("请求超时，已重试{}次".format(max_retries))
            raise ServiceError("请求异常，已重试{}次: {}".format(max_retries, last_exc))
        return wrapper
    return decorator


def _handle_http_error(e: requests.exceptions.HTTPError):
    """HTTP 状态码 -> SkillError，502/504 触发重试"""
    status = e.response.status_code if e.response is not None else None
    if status == 401:
        raise AuthError("签名无效或已过期（401）")
    if status == 429:
        raise RateLimitError("请求被限流（429），请稍后重试")
    if status == 400:
        raise ParamError("请求参数不合法（400）")
    if status in (502, 504):
        raise _RetryableError("网关超时（{}），将自动重试".format(status))
    raise ServiceError("HTTP 错误 {}".format(status))


def _handle_biz_error(result: dict):
    """业务错误（HTTP 200 但 success=false）-> SkillError"""
    msg = result.get("msgInfo") or result.get("message") or "未知业务错误"
    raise ServiceError(str(msg))


@_with_retry()
def _api_post_impl(path: str, body: dict = None, timeout: int = 30, raw_body: str = None) -> dict:
    """内部实现，带重试"""
    return _do_post(path, body, timeout, raw_body)


def _do_post(path: str, body: dict = None, timeout: int = 30, raw_body: str = None) -> dict:
    """
    POST 请求网关 API 核心逻辑

    Args:
        path:    API 路径（拼接到 BASE_URL 后面）
        body:    请求体 dict（与 raw_body 二选一）
        timeout: 超时秒数
        raw_body: 已序列化的请求体字符串（跳过 json.dumps）

    Returns:
        API 响应 dict

    Raises:
        ParamError / RateLimitError / ServiceError
    """
    url = "{}{}".format(BASE_URL, path)
    body_str = raw_body if raw_body is not None else json.dumps(body or {}, ensure_ascii=False)

    # AK 签名认证
    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")

    try:
        resp = requests.post(url, headers=headers, data=body_str.encode('utf-8') if isinstance(body_str, str) else body_str, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)
    except requests.exceptions.Timeout:
        raise _RetryableError("请求超时({}s)".format(timeout))

    try:
        result = resp.json()
    except json.JSONDecodeError:
        raise ServiceError("响应格式异常，无法解析 JSON")

    # 业务层错误检测
    if isinstance(result, dict) and result.get("success") is False:
        _handle_biz_error(result)

    return result


def api_post(path: str, body: dict = None, timeout: int = 30, raw_body: str = None, retry: bool = True) -> dict:
    """
    POST 请求网关 API

    Args:
        path:    API 路径（拼接到 BASE_URL 后面）
        body:    请求体 dict（与 raw_body 二选一）
        timeout: 超时秒数
        raw_body: 已序列化的请求体字符串（跳过 json.dumps）
        retry:   是否启用自动重试（默认 True）

    Returns:
        API 响应 dict
    """
    if retry:
        return _api_post_impl(path=path, body=body, timeout=timeout, raw_body=raw_body)
    return _do_post(path=path, body=body, timeout=timeout, raw_body=raw_body)

