#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
aoment-register CLI
Agent Bot 自动注册工具 - 由 Aoment AI 提供支持

通过提供昵称（不超过16字符）自动注册 Agent 专用账号并获取 API Key。
"""

import argparse
import json
import sys

import requests

API_BASE = "https://www.aoment.com"
REGISTER_ENDPOINT = "/api/skills/aoment-visuals/register-agent"
TIMEOUT = 30


def register_agent(api_base: str, nickname: str) -> dict:
    """注册 Agent 账号并获取 API Key"""
    url = f"{api_base}{REGISTER_ENDPOINT}"
    payload = {"nickname": nickname}

    resp = requests.post(url, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser(
        description="Aoment AI Agent Bot 注册工具 - 自动注册并获取 API Key"
    )
    parser.add_argument(
        "--nickname", "-n",
        required=True,
        help="Agent 昵称（不超过16个字符）",
    )
    parser.add_argument(
        "--api-base",
        default=API_BASE,
        help=f"API 基础地址（默认: {API_BASE}）",
    )
    args = parser.parse_args()

    nickname = args.nickname.strip()
    if not nickname:
        print(json.dumps({"success": False, "error": "nickname 不能为空"}))
        sys.exit(1)
    if len(nickname) > 16:
        print(json.dumps({"success": False, "error": "nickname 长度不能超过16个字符"}))
        sys.exit(1)

    try:
        result = register_agent(args.api_base, nickname)

        if result.get("success"):
            data = result.get("data", {})
            output = {
                "success": True,
                "data": {
                    "username": data.get("username"),
                    "nickname": data.get("nickname"),
                    "api_key": data.get("apiKey"),
                },
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"success": False, "error": result.get("error", "未知错误")}))
            sys.exit(1)

    except requests.exceptions.HTTPError as e:
        try:
            err_body = e.response.json()
            error_msg = err_body.get("error", str(e))
        except Exception:
            error_msg = str(e)
        print(json.dumps({"success": False, "error": error_msg}))
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(json.dumps({"success": False, "error": f"网络请求失败: {e}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
