#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
"""

import os
import json
import re
import time
import logging
from functools import wraps

import requests

from _auth import get_auth_headers
from _errors import AuthError, ParamError, RateLimitError, ServiceError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('1688_http')

# 支持通过环境变量切换预发/线上环境
# 线上: https://skills-gateway.1688.com
# 预发: https://skills-gateway.1688.com
BASE_URL = os.environ.get("1688_GATEWAY_URL", "https://skills-gateway.1688.com")
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1


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
def api_post_stream(path: str, body: dict = None, timeout: int = 60) -> str:
    """
    流式 POST 请求 1688 API（自动签名 + 重试 + 错误映射）

    Args:
        path:    API 路径，如 /api/1688_source_suppliers/1.0.0
        body:    请求体 dict（会 json.dumps）
        timeout: 超时秒数，默认60秒

    Returns:
        所有chunk数据合并后的完整字符串

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {})

    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")

    try:
        resp = requests.post(url, headers=headers, data=body_str, timeout=timeout, stream=True)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    all_chunks = []
    try:
        for chunk in resp.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                all_chunks.append(chunk)
    except Exception as e:
        logger.warning(f"流式数据读取异常: {e}")

    full_content = "".join(all_chunks)
    
    if not full_content:
        raise ServiceError("未获取到流式数据")

    return full_content
