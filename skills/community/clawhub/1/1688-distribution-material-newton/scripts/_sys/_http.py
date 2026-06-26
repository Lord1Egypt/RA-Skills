#!/usr/bin/env python3
"""
通用 HTTP 客户端

职责：签名注入、自动重试、统一错误映射。
所有 capability 的 service 层通过 api_post() 调用 1688 API，
不再各自处理 HTTP / 重试 / 错误解析。

支持两种调用方式：
  - api_post(path="/api/xxx/1.0.0", body={...})         # 传完整路径（兼容旧 capabilities）
  - api_post(tool_name="fx_xxx", body={...})             # 传工具名（新 biz 模块推荐）
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

from scripts._sys._auth import get_auth_headers
from scripts._sys._errors import AuthError, ParamError, RateLimitError, ServiceError
from scripts.biz.const import BASE_URL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('1688_material_http')
MAX_RETRIES = 3
RETRY_DELAY_BASE = 1


def _get_proxy():
    """
    从 /etc/environment 读取 https_proxy。
    若文件不存在或变量未设置，返回 None。
    """
    env_file = "/etc/environment"
    try:
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "https_proxy" in line or "HTTPS_PROXY" in line:
                        if "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            if key in ("https_proxy", "HTTPS_PROXY"):
                                value = value.strip().strip('"').strip("'")
                                return value
    except Exception:
        pass
    return None


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
    msg_info = result.get("msgInfo") or result.get("message")
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


# ── 响应解析 ──────────────────────────────────────────────────────────────────

def parse_data_field(data):
    """
    解析 API 返回的 data 字段。
    data 可能是 JSON 字符串或 dict，统一返回 dict / list / str。
    """
    if isinstance(data, str):
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return data
    return data


# ── 公共请求 ──────────────────────────────────────────────────────────────────

@_with_retry()
def api_post(path: str = None, body: dict = None, timeout: int = 60, tool_name: str = None):
    """
    POST 请求 1688 API（自动签名 + 重试 + 错误映射）

    支持两种调用方式：
        api_post(path="/api/distribution_material_xxx/1.0.0", body={...})
        api_post(tool_name="fx_xxx", body={...})

    Args:
        path:      API 路径，如 /api/distribution_material_xxx/1.0.0
        body:      请求体 dict
        timeout:   超时秒数
        tool_name: 工具名称，如 fx_xxx（自动构建路径为 /api/{tool_name}/1.0.0）

    Returns:
        API 网关层返回的 data 字段（dict）

    Raises:
        AuthError / ParamError / RateLimitError / ServiceError
    """
    # 支持 tool_name 方式调用
    if tool_name and not path:
        path = f"/api/{tool_name}/1.0.0"

    if not path:
        raise ParamError("必须提供 path 或 tool_name 参数")

    url = f"{BASE_URL}{path}"
    body_str = json.dumps(body or {}, ensure_ascii=False)

    headers = get_auth_headers("POST", path, body_str)
    if not headers:
        raise AuthError("AK 未配置")
    headers["Content-Type"] = "application/json; charset=utf-8"

    proxies = None
    proxy_url = _get_proxy()
    if proxy_url:
        logger.info("[proxy] 使用代理: %s", proxy_url)
        proxies = {"https": proxy_url, "http": proxy_url}

    try:
        resp = requests.post(url, headers=headers, data=body_str.encode("utf-8"), timeout=timeout, proxies=proxies)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        _handle_http_error(e)

    result = resp.json()

    # 网关层 success 检查
    if result.get("success") is False:
        _handle_biz_error(result)

    # 提取网关层 data
    gateway_data = result.get("data", result)

    # 1688 素材优化 API 特殊处理：
    # 1. 如果 data 是字符串（JSON 序列化），解析它
    # 2. 检查 __success__ 字段
    if isinstance(gateway_data, str):
        try:
            gateway_data = json.loads(gateway_data)
        except (json.JSONDecodeError, TypeError):
            pass

    # 业务层 __success__ 检查
    if isinstance(gateway_data, dict):
        if gateway_data.get("__success__") is False:
            msg = gateway_data.get("message") or gateway_data.get("msg") or "业务处理失败"
            raise ServiceError(f"业务处理失败：{msg}")
        # 业务层 success 检查（兼容 biz 模块返回格式）
        if "success" in gateway_data and gateway_data.get("success") is False:
            msg = gateway_data.get("message") or gateway_data.get("msg") or "业务处理失败"
            raise ServiceError(f"业务处理失败：{msg}")
        # 如果还有嵌套的 data 字段（字符串），再解析一层
        inner_data = gateway_data.get("data")
        if isinstance(inner_data, str):
            try:
                inner_data = json.loads(inner_data)
                gateway_data["data"] = inner_data
            except (json.JSONDecodeError, TypeError):
                pass
        return gateway_data

    return gateway_data
