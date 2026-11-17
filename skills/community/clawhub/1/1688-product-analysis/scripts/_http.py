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
import os
import time
import logging
import inspect
from functools import wraps
import uuid

import requests

from _auth import get_auth_headers
from _const import get_runtime_user_id, SKILL_NAME, SKILL_VERSION
from _errors import AuthError, DeadlineExceededError, ParamError, RateLimitError, ServiceError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('1688_pa_http')


def _resolve_base_url() -> str:
    """默认走预发，仅在 SKILL_ENV=prod 时切换生产网关。"""
    env = os.environ.get("SKILL_ENV", "pre").strip().lower()
    if env == "prod":
        return "https://gateway.1688.com"
    return "https://gateway.1688.com"


BASE_URL = _resolve_base_url()
CHANNEL = "clawhubai"
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1

# ── 重试 ─────────────────────────────────────────────────────────────────────

def _with_retry(max_retries: int = MAX_RETRIES):
    """仅重试 ConnectionError / Timeout，其余异常直接传播"""

    def decorator(func):
        signature = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            call_kwargs = dict(kwargs)
            deadline = call_kwargs.pop("_deadline", None)
            last_exc = None
            for attempt in range(max_retries):
                bound = signature.bind_partial(*args, **call_kwargs)
                timeout = bound.arguments.get("timeout", signature.parameters["timeout"].default)
                if deadline is not None:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise DeadlineExceededError()
                    bound.arguments["timeout"] = min(timeout, remaining)
                try:
                    return func(*bound.args, **bound.kwargs)
                except (requests.exceptions.ConnectionError,
                        requests.exceptions.Timeout) as e:
                    last_exc = e
                    if deadline is not None:
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            raise DeadlineExceededError()
                    delay = min(RETRY_DELAY_BASE * (2 ** attempt), 10)
                    logger.warning("网络异常(尝试%d/%d): %s, %ds后重试",
                                   attempt + 1, max_retries, e, delay)
                    if attempt < max_retries - 1:
                        if deadline is not None:
                            if remaining <= delay:
                                raise DeadlineExceededError()
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
def api_post(path: str, body: dict = None, timeout: int = 30, _deadline=None):
    """
    POST 请求 1688 skills 网关 MCP 工具（自动注入 __userId__ + 重试 + 错误映射）

    Args:
        path:    API 路径，如 /api/alibaba.1688.get.offer.data/1.0.0
        body:    请求体 dict（除 __userId__ 外的工具入参；__userId__ 由本方法自动注入）
        timeout: 超时秒数
        _deadline: 可选的 time.monotonic() 绝对截止时间。

    Returns:
        API 响应中的 data 字段。
        若 data 是 JSON 字符串（MCP 工具的标准返回格式），自动 json.loads 为 list/dict。

    Raises:
        ParamError / RateLimitError / ServiceError
    """
    # path 末尾追加渠道码: /api/xxx/1.0.0 → /api/xxx/1.0.0/{CHANNEL}
    path = f"{path}/{CHANNEL}"
    url = f"{BASE_URL}{path}"
    payload = {"__userId__": get_runtime_user_id()}
    if body:
        payload.update(body)
    body_str = json.dumps(payload, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if headers is None:
        raise AuthError(
            "AK 未配置：请确认平台已下发 ALI_1688_AK，或本地 ~/.openclaw/openclaw.json 已注册 1688-product-analysis"
        )
    headers["x-skill-code"] = SKILL_NAME
    headers["x-skill-version"] = SKILL_VERSION
    headers["x-request-id"] = uuid.uuid4().hex

    resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)

    if resp.status_code != 200:
        raise ServiceError(f"网关异常（HTTP {resp.status_code}）")

    result = resp.json()
    if result.get("success") is False:
        _handle_biz_error(result)

    data = result.get("data")

    # ── 循环剥壳：兼容预发(3层)和生产(2层)的嵌套封装 ──────────────────────
    # 包装层特征：dict 且 key 集合只包含网关结果字段
    # 终止条件：data 是 list / None / str(纯文本) / 非包装 dict
    _WRAPPER_KEYS = {"data", "success", "message", "msgCode", "msgInfo", "extInfo"}
    _MAX_DEPTH = 5

    def _try_parse_json(value):
        """若 value 是 JSON 字符串则解析，否则原样返回。"""
        if not isinstance(value, str):
            return value
        try:
            return json.loads(value)
        except (json.JSONDecodeError, ValueError):
            return value

    data = _try_parse_json(data)

    for _ in range(_MAX_DEPTH):
        if not isinstance(data, dict) or "data" not in data:
            break
        if not set(data.keys()) <= _WRAPPER_KEYS:
            break
        if data.get("success") is False:
            _handle_biz_error(data)
        data = _try_parse_json(data.get("data"))

    return data
