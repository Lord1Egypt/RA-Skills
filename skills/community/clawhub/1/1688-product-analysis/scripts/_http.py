#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：调用 1688 skills 网关的 MCP 工具接口、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post() 调用 MCP 工具，
不再各自处理 HTTP / 重试 / 错误解析。

约定：
    POST {BASE_URL}/api/{tool_name}/1.0.0
    body: {"__userId__": <int>, ...其他工具入参}
    response: {"success": bool, "msgInfo": str, "data": <JSON 字符串或对象>}
"""

import json
import re
import time
import logging
from functools import wraps

import requests

from _auth import get_auth_headers
from _const import get_runtime_user_id
from _errors import ParamError, RateLimitError, ServiceError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('1688_pa_http')

BASE_URL = "https://skills-gateway.1688.com"
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
    if status == 429:
        raise RateLimitError("请求被限流（429），请稍后重试")
    if status == 400:
        raise ParamError("请求参数不合法（400）")
    raise ServiceError(f"HTTP 错误 {status}")

def _handle_biz_error(result: dict):
    """业务错误（HTTP 200 但 success=false）→ SkillError"""
    msg_code = str(result.get("msgCode") or "")
    msg_info = result.get("msgInfo")
    code_match = re.search(r"\b(400|429|500)\b", msg_code)
    normalized = code_match.group(1) if code_match else ""

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
def api_post(path: str, body: dict = None, timeout: int = 30):
    """
    POST 请求 1688 skills 网关 MCP 工具（自动注入 __userId__ + 重试 + 错误映射）

    Args:
        path:    API 路径，如 /api/get_offer_data/1.0.0
        body:    请求体 dict（除 __userId__ 外的工具入参；__userId__ 由本方法自动注入）
        timeout: 超时秒数

    Returns:
        API 响应中的 data 字段。
        若 data 是 JSON 字符串（MCP 工具的标准返回格式），自动 json.loads 为 list/dict。

    Raises:
        ParamError / RateLimitError / ServiceError
    """
    url = f"{BASE_URL}{path}"
    payload = {"__userId__": get_runtime_user_id()}
    if body:
        payload.update(body)
    body_str = json.dumps(payload, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if headers is None:
        raise ServiceError(
            "AK 未配置：请确认平台已下发 ALI_1688_AK，或本地 ~/.openclaw/openclaw.json 已注册 1688-product-analysis"
        )

    try:
        resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    result = resp.json()
    if result.get("success") is False:
        _handle_biz_error(result)

    data = result.get("data")

    # 网关返回的 data 可能是 JSON 字符串，先反序列化一层
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ServiceError("API 返回的 data 字段不是合法 JSON")

    # MCP 工具普遍存在「双层封装」：外层 data 是 dict 且仍含 success/data 字段，
    # 真正的业务数据在内层 data（同样可能是 JSON 字符串）。这里再剥一层。
    if isinstance(data, dict) and "success" in data and "data" in data:
        if data.get("success") is False:
            _handle_biz_error(data)
        inner = data.get("data")
        if isinstance(inner, str):
            try:
                inner = json.loads(inner)
            except json.JSONDecodeError:
                raise ServiceError("API 返回的内层 data 字段不是合法 JSON")
        data = inner

    return data
