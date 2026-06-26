#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post() 调用 1688 API，
不再各自处理 HTTP / 重试 / 错误解析。
"""

import json
import os
import sys
import re
import time
import logging
from functools import wraps

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')))

import requests

from scripts._sys._auth import build_auth_headers
from scripts._sys._errors import AuthError, ParamError, RateLimitError, ServiceError
from scripts.biz.const import BASE_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('distribute_offer_http')
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1

# ── 重试 ─────────────────────────────────────────────────────────────────────

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

# ── 错误映射 ──────────────────────────────────────────────────────────────────

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

# ── 公共请求 ──────────────────────────────────────────────────────────────────

@_with_retry()
def api_post(tool_name: str, body: dict = None, timeout: int = 30):
    """
    POST 请求 1688 API（自动签名 + 重试 + 错误映射 + 网关层解包）

    Args:
        tool_name: 工具名称，如 distribution_select_offer、shop_and_tool_info
        body:      请求体 dict（会 json.dumps）
        timeout:   超时秒数

    Returns:
        API 响应中的 data 字段（dict）

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    path = f"/api/{tool_name}/1.0.0"
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {})

    headers = build_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")

    try:
        resp = requests.post(url, headers=headers, data=body_str, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    result = resp.json()

    # 网关层结构检查
    if not isinstance(result, dict):
        raise ServiceError("接口返回格式异常：期望 dict 类型")

    # 网关层 success 检查
    if result.get("success") is False:
        msg = result.get("message") or result.get("msgInfo") or "未知业务错误"
        raise ServiceError(f"网关调用失败：{msg}")

    # 解包网关层，获取业务数据（在 data 字段中）
    # 结构：{"data": {"success": true, "model": {...}}, "success": true}
    data = result.get("data", {})
    if not isinstance(data, dict):
        raise ServiceError("接口返回格式异常：data 字段不是 dict 类型")

    # 业务层 success 检查
    if "success" in data and data.get("success") is False:
        # 尽可能多地收集错误信息
        msg = data.get("message") or data.get("msg") or data.get("bizMsg") or "业务处理失败"
        error_code = data.get("errorCode") or data.get("msgCode") or ""
        error_msg = data.get("errorMsg") or data.get("msgInfo") or ""
        parts = [msg]
        if error_code:
            parts.append(f"errorCode={error_code}")
        if error_msg and error_msg != msg:
            parts.append(error_msg)
        detail = "，".join(parts)
        raise ServiceError(f"业务处理失败：{detail}")

    return data
