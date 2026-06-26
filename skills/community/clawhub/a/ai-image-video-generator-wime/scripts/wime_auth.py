#!/usr/bin/env python3
"""
WIME OpenAPI 认证工具

仅支持 access-token 认证：
- 使用 WIME_ACCESS_TOKEN 环境变量
- 可选 WIME_BASE_URL 覆盖默认地址
"""

import json
import os
import argparse
from typing import Optional

BASE_URL = os.environ.get("WIME_BASE_URL", "https://wime-ai.com")
ACCESS_TOKEN = os.environ.get("WIME_ACCESS_TOKEN", "")


def get_auth(
    method: str = "POST",
    uri_path: str = "",
    body_dict: Optional[dict] = None,
    content_type: str = "application/json",
) -> dict:
    """生成 WIME access-token 请求配置。

    返回:
      - base_url: str
      - headers: dict（完整请求 headers，可直接传给 requests）
      - body_str: Optional[str]（序列化后的 body，用于 data= 发送）
    """
    if not ACCESS_TOKEN:
        raise ValueError(
            "WIME_ACCESS_TOKEN 未配置。请设置环境变量：\n"
            "  export WIME_ACCESS_TOKEN='你的token'"
        )

    headers = {"access-token": ACCESS_TOKEN}
    body_str = None

    if body_dict is not None:
        body_str = json.dumps(body_dict, separators=(",", ":"), sort_keys=True, ensure_ascii=False)
        headers["Content-Type"] = content_type

    return {
        "base_url": BASE_URL,
        "headers": headers,
        "body_str": body_str,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WIME OpenAPI 认证工具")
    parser.add_argument("--method", default="POST")
    parser.add_argument("--path", default="/waic/core/creationDesk/draw")
    parser.add_argument("--body", default="{}", help="JSON body string")
    args = parser.parse_args()

    body_dict = json.loads(args.body)
    result = get_auth(method=args.method, uri_path=args.path, body_dict=body_dict)
    print(json.dumps(result, indent=2, ensure_ascii=False))
