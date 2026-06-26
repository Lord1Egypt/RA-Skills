#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post() 调用 1688 API，
不再各自处理 HTTP / 重试 / 错误解析。
"""

import json
import re
import time
import logging
from functools import wraps

import requests

from _auth import get_auth_headers
from _errors import AuthError, ParamError, RateLimitError, ServiceError, GatewayAuthError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('1688_http')

BASE_URL = "https://skills-gateway.1688.com"
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1
# 网关瞬态错误（可重试的 HTTP 状态码）
RETRIABLE_STATUS_CODES = {500, 502, 503, 504}

# 1688 网关返回的 Token 相关错误码（需要 Agent 重新授权）
_GATEWAY_AUTH_ERROR_CODES = {
    "1688_token_expired",
    "1688_invalid_token",
    "1688_token_revoked",
    "1688_token_unauthorized",
    "1688_no_scope_specified",
    "1688_invalid_scope",
}

# ── 重试 ─────────────────────────────────────────────────────────────────────

class _RetriableHTTPError(Exception):
    """可重试的 HTTP 网关错误（500/502/503/504）"""
    def __init__(self, status_code: int):
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}")


def _with_retry(max_retries: int = MAX_RETRIES):
    """重试 ConnectionError / Timeout / 网关瞬态错误(502/503/504)，其余异常直接传播"""

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
                except _RetriableHTTPError as e:
                    last_exc = e
                    delay = min(RETRY_DELAY_BASE * (2 ** attempt), 10)
                    logger.warning("网关超时(尝试%d/%d): HTTP %d, %ds后重试",
                                   attempt + 1, max_retries, e.status_code, delay)
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

    # 检查 1688 网关 Token 相关错误码（Agent 可自动恢复）
    if msg_code in _GATEWAY_AUTH_ERROR_CODES:
        required_scope = result.get("requiredScope", "")
        raise GatewayAuthError(
            error_code=msg_code,
            message=msg_info or f"授权错误：{msg_code}",
            required_scope=required_scope,
        )

    # 标准 HTTP 状态码映射
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
def api_post(path: str, body: dict = None, timeout: int = 30) -> dict:
    """
    POST 请求 1688 API（自动签名 + 重试 + 错误映射）

    Args:
        path:    API 路径，如 /1688claw/skill/searchoffer
        body:    请求体 dict（会 json.dumps）
        timeout: 超时秒数

    Returns:
        API 响应中的 model 字段（dict）

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {}, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")

    try:
        resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status in RETRIABLE_STATUS_CODES:
            raise _RetriableHTTPError(status)
        _handle_http_error(e)

    result = resp.json()
    if result.get("success") is False:
        _handle_biz_error(result)

    # 优先返回 model 字段，如果不存在则返回 data 字段
    model = result.get("model")
    if model is not None and isinstance(model, dict):
        return model

    data = result.get("data")
    if data is not None and isinstance(data, dict):
        return data

    # 如果都不是 dict，抛出异常
    raise ServiceError("API 返回结构异常（model 和 data 都不是对象）")


# ── 商品搜索公共接口 ─────────────────────────────────────────────────────────

FIND_PRODUCT_API = "/api/find_product/1.0.0"


def _parse_product_item(item: dict) -> dict:
    """将 API 返回的单个商品条目映射为统一商品结构"""
    product_id = str(item.get("itemId", ""))
    detail_url = item.get("detailUrl") or (
        f"https://detail.1688.com/offer/{product_id}.html" if product_id else ""
    )
    return {
        "product_id": product_id,
        "title": item.get("title", ""),
        "image_url": item.get("imageUrl", ""),
        "detail_url": detail_url,
        "similarity_score": float(item.get("score", 0)),
        "price": item.get("currentPrice"),
        "sku_id": item.get("skuId", ""),
        "sku_title": item.get("skuTitle", ""),
        "yx_index": item.get("yxIndex"),
        "quantity_begin": item.get("quantityBegin"),
        "unit": item.get("unit", ""),
        "supplier": item.get("company", ""),
        "sold_count": item.get("soldOut", 0),
        "stock_amount": item.get("storeAmount", 0),
        "user_id": str(item.get("userId", "")),
        "member_id": item.get("memberId", ""),
        "category_id": item.get("cateId"),
        "promotion_tags": item.get("promotionTags", []),
        "service_infos": item.get("serviceInfos", []),
        "selling_points": item.get("sellingPoints", []),
    }


def search_products(request_body: dict) -> list:
    """
    调用商品搜索 API 并返回统一商品结构列表。

    Args:
        request_body: 请求体（平层 JSON，直接包含搜索参数）

    Returns:
        统一商品结构的列表

    Raises:
        ServiceError: API 返回格式异常
    """
    resp = api_post(FIND_PRODUCT_API, request_body)
    data = resp.get("data")
    if not isinstance(data, list):
        raise ServiceError("格式异常，请稍后重试")
    return [_parse_product_item(item) for item in data]
