from __future__ import annotations

import os
from typing import Any
from urllib import parse


PRINT_BASE_URL = "https://any.webprinter.cn"
SEARCH_DRIVER_URL = "https://any.webprinter.cn/openapi/cdf/_sgdv2"
API_KEY_ENV = "CDF_PRINT_API_KEY"
SKILL_TERMINAL_ID = "cdf_ai_terminal"
SKILL_TERMINAL_TYPE = "AI"


def build_print_url(path: str, query: dict[str, Any] | None = None) -> str:
    """基于统一打印服务地址拼接完整 URL。"""
    base_url = PRINT_BASE_URL.strip().rstrip("/")
    if not base_url:
        raise RuntimeError("未配置打印服务基础地址，无法调用云端接口。")
    url = f"{base_url}{path}"
    if query:
        url = f"{url}?{parse.urlencode(query)}"
    return url


def read_api_key() -> str:
    """读取可选的 Bearer Token。"""
    return os.environ.get(API_KEY_ENV, "").strip()


def build_common_headers(content_type: str | None = None) -> dict[str, str]:
    """生成通用请求头，并附带技能打印所需终端信息。"""
    headers = {
        "Accept": "application/json",
        "tid": SKILL_TERMINAL_ID,
        "ttp": SKILL_TERMINAL_TYPE,
    }
    if content_type:
        headers["Content-Type"] = content_type
    api_key = read_api_key()
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return headers
