#!/usr/bin/env python3
"""将用户在重置页复制的新 API Key 写入 fosun.env 并尝试 finalize。

用法:
  $REAL_PY update_api_key.py --api-key <页面 API Key> --server-public-key '<页面服务端公钥 PEM>'
  或
  python3 fosun-env-setup/code/ensure_fosun_env.py --api-key ... --server-public-key '...'
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SETUP_CODE = Path(__file__).resolve().parent.parent.parent / "fosun-env-setup" / "code"
if str(_SETUP_CODE) not in sys.path:
    sys.path.insert(0, str(_SETUP_CODE))

from ensure_fosun_env import update_api_key
from _client import run


def main():
    parser = argparse.ArgumentParser(
        description="更新 fosun.env 中的 FSOPENAPI_API_KEY（重置扫码后由用户提供）"
    )
    parser.add_argument("--api-key", required=True, help="页面复制的 API Key")
    parser.add_argument(
        "--server-public-key",
        required=True,
        help="页面复制的服务端公钥 PEM 全文（与 apikey 必填）",
    )
    args = parser.parse_args()

    payload = update_api_key(
        args.api_key,
        server_public_key=args.server_public_key,
        finalize=True,
    )
    if payload.get("status") == "valid":
        payload.setdefault("ok", True)
        payload.setdefault(
            "message",
            "API Key 已写入并完成验证，可继续之前的业务操作。",
        )
    else:
        payload.setdefault("ok", payload.get("status") != "error")
        payload.setdefault(
            "message",
            "API Key 已写入；若仍未 valid，请按 operation_guide 完成页面步骤后再运行 ensure_fosun_env.py。",
        )
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run(main)
