#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post() 调用 1688 API，
不再各自处理 HTTP / 重试 / 错误解析。
"""

import json
import time
import logging
from functools import wraps
import uuid

import requests

from _auth import get_auth_headers
from _const import SKILL_NAME, SKILL_VERSION
from _errors import AuthError, ParamError, RateLimitError, ServiceError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('1688_http')

BASE_URL = "https://gateway.1688.com"
CHANNEL = "clawhubai"
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

def _handle_biz_error(result: dict):
    """业务错误（HTTP 200 但 success=false）→ SkillError"""
    msg_code = str(result.get("msgCode") or "")
    code = str(result.get("code") or "")
    msg_info = result.get("msgInfo")

    if code == "SignatureInvalid":
        raise AuthError("签名校验失败")
    if code == "ParamMissing":
        raise ParamError("缺少必填参数")
    if code == "APIUnsupported":
        raise ParamError("工具不存在")
    if code in ("QosAppFrequencyLimit", "QosApiFrequencyLimit"):
        raise RateLimitError("请求超限")
    if code == "ISPInvokeError":
        raise ServiceError("后端服务错误")
    if code == "ISPInvokeTimeout":
        raise ServiceError("后端服务调用超时")

    detail = msg_info or msg_code or "未知业务错误"
    raise ServiceError(str(detail))


# ── 公共请求 ──────────────────────────────────────────────────────────────────

@_with_retry()
def api_post(path: str, body: dict = None, timeout: int = 30, login_id: str = None) -> dict:
    """
    POST 请求 1688 API（自动签名 + 重试 + 错误映射）

    Args:
        path:     API 路径，如 /api/toolsCode/toolsVersion
        body:     请求体 dict（会 json.dumps）
        timeout:  超时秒数
        login_id: 可选，目标店铺的 loginId，用于多店铺场景

    Returns:
        API 响应中的 data 字段（dict）

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    payload = dict(body or {})
    if login_id:
        payload["NEWTON_SHOP_LOGIN_ID"] = login_id

    # path 末尾追加渠道码: /api/xxx/1.0.0 → /api/xxx/1.0.0/{CHANNEL}
    path = f"{path}/{CHANNEL}"
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(payload, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")
    headers["x-skill-code"] = SKILL_NAME
    headers["x-skill-version"] = SKILL_VERSION
    headers["x-request-id"] = uuid.uuid4().hex
    resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)

    if resp.status_code != 200:
        raise ServiceError(f"网关异常（HTTP {resp.status_code}）")

    result = resp.json()
    if result.get("success") is False:
        _handle_biz_error(result)

    data = result.get("data", {})
    if not isinstance(data, dict):
        raise ServiceError("API 返回结构异常（data 不是对象）")

    return data
