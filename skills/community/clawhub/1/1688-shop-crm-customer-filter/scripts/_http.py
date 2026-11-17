#!/usr/bin/env python3
"""
通用 HTTP 客户端（1688 网关）

职责：签名注入、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post() 调用后端 API。

网关地址：
  预发：https://gateway.1688.com/api/{toolCode}/{version}
  线上：https://gateway.1688.com/api/{toolCode}/{version}

鉴权：
  HMAC-SHA256 签名（由 _auth.py 生成），AK 由框架通过环境变量 ALI_1688_AK 注入。
  user_id 由网关联动 Session 自动注入，Skill 代码无需处理。
"""

import json
import os
import sys
import time
import logging
from functools import wraps
import uuid

import requests

from _auth import get_auth_headers
from _const import SKILL_NAME, SKILL_VERSION
from _errors import AuthError, ParamError, RateLimitError, ServiceError, SkillError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('crm_http')

# 环境判断：
# - Windows / macOS 平台默认走线上（因桌面客户端通常由正式环境触发）
# - 其他平台默认预发
# - 统一可通过环境变量 SKILL_ENV=pre/prod 强制覆盖
_env = os.environ.get("SKILL_ENV", "prod" if sys.platform in ("win32", "darwin") else "pre")
if _env == "prod":
    BASE_URL = "https://gateway.1688.com"
else:
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


def _find_nested_biz_error(obj) -> dict:
    """
    在多层 data 信封中查找业务失败的 PageResult 节点。

    网关对「字段不支持」这类错误会返回外层 success=true，但把失败埋在内层
    data.data 里（success=false + errorCode/errorInfo，如 PARAM_ERROR「字段错误: city」）。
    只检查外层 success 会把它当成空结果集，静默渲染成「暂无匹配客户」。
    这里向下钻取，命中「success is False 且带 errorCode」的节点即返回。
    """
    if not isinstance(obj, dict):
        return None
    if obj.get("success") is False and obj.get("errorCode"):
        return obj
    inner = obj.get("data")
    if isinstance(inner, dict):
        return _find_nested_biz_error(inner)
    return None


def _handle_nested_biz_error(node: dict):
    """内层 PageResult 业务错误（errorCode/errorInfo）→ SkillError"""
    code = str(node.get("errorCode") or "")
    detail = str(node.get("errorInfo") or code or "未知业务错误")
    if len(detail) > 300:
        detail = detail[:300] + "…（已截断）"
    if code == "PARAM_ERROR":
        raise ParamError(detail)
    raise ServiceError(detail)


# ── 公共请求 ──────────────────────────────────────────────────────────────────

@_with_retry()
def api_post(path: str, body: dict = None, timeout: int = 30) -> dict:
    """
    POST 请求 1688 API（自动签名 + 重试 + 错误映射）

    Args:
        path:    API 路径，如 /api/alibaba.1688.customer.list/1.0.0
        body:    请求体 dict（会 json.dumps）
        timeout: 超时秒数

    Returns:
        完整网关响应（dict），包含 success / data 等顶层字段

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    # path 末尾追加渠道码: /api/xxx/1.0.0 → /api/xxx/1.0.0/{CHANNEL}
    path = f"{path}/{CHANNEL}"
    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {}, ensure_ascii=False)
    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置，请检查框架环境变量 ALI_1688_AK 是否已配置")
    headers["x-skill-code"] = SKILL_NAME
    headers["x-skill-version"] = SKILL_VERSION
    headers["x-request-id"] = uuid.uuid4().hex
    logger.info("POST %s", url)

    resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout)

    if resp.status_code != 200:
        raise ServiceError(f"网关异常（HTTP {resp.status_code}）")

    try:
        result = resp.json()
    except Exception:
        # 响应正文可能含有网关调试信息或业务数据，不能输出到用户/模型上下文。
        ctype = str(resp.headers.get("Content-Type", ""))[:100]
        raise ServiceError(
            f"API 返回非法 JSON（HTTP {resp.status_code}, Content-Type: {ctype}）"
        )

    if not isinstance(result, dict):
        raise ServiceError("API 返回结构异常（响应不是对象）")

    if result.get("success") is False:
        _handle_biz_error(result)

    # 外层 success=true 时，仍需下钻检查内层 PageResult 是否为业务失败
    # （如未知/不支持字段：内层 success=false + errorCode=PARAM_ERROR）
    nested_err = _find_nested_biz_error(result)
    if nested_err is not None:
        _handle_nested_biz_error(nested_err)

    return result
