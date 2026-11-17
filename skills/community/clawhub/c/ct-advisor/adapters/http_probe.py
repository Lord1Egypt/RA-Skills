#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""http_probe.py — ct-advisor 出站探测 helper（§16.9 出站调用收口至 adapters/）。

scripts/ 层（如 check_coze.py）不再直接持有 requests 调用；所有出站 HTTP 探测
统一走本模块，保证 scripts/ 层不直接发起网络请求、业务逻辑与外部依赖解耦（ct-base §16.9）。
"""
from __future__ import annotations

from typing import Optional

# §16.9: 出站相关常量收口至 adapters/，scripts/ 层不持有硬编码 URL
COZE_ENDPOINT = "https://ct-advisor.coze.site/run"


def probe_get(url: str, timeout: float = 8.0,
              proxies: Optional[dict] = None,
              headers: Optional[dict] = None) -> tuple:
    """小请求探测端点。返回 (ok, 状态码或错误摘要)。

    - 401 = 端点可达且鉴权生效（未带有效 token 的正常响应）；任何状态码都说明网络通
    - proxies={"http": None, "https": None} 表示绕过系统代理直连
    """
    import requests
    try:
        r = requests.get(url, timeout=timeout, proxies=proxies,
                         headers=headers or {"User-Agent": "ct-advisor-check"})
        return True, r.status_code
    except requests.exceptions.ProxyError as e:
        return False, f"ProxyError: {e}"
    except requests.exceptions.ConnectionError as e:
        return False, f"ConnectionError: {e}"
    except requests.exceptions.Timeout as e:
        return False, f"Timeout: {e}"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"
