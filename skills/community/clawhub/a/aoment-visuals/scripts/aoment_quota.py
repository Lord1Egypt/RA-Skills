#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
# ]
# ///
"""
aoment-quota CLI
查询当前 Agent API Key 的剩余可用生成次数

需要 Agent API Key 进行身份验证，通过 aoment_register.py 注册获取。
"""

import argparse
import json
import sys

import requests

API_BASE = "https://www.aoment.com"
REQUEST_TIMEOUT = 15


def query_quota(api_base: str, api_key: str) -> dict:
    """查询当前 API Key 的剩余可用次数"""
    url = f"{api_base}/api/skills/aoment-visuals/quota"
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    result = response.json()

    if not result.get("success"):
        return {"success": False, "error": result.get("error", "查询限额失败")}

    data = result["data"]
    return {
        "success": True,
        "data": {
            "remaining": data["remaining"],
            "quota": data["quota"],
            "used": data["used"],
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="aoment-quota: 查询 API Key 剩余可用生成次数"
    )
    parser.add_argument(
        "--api-key", "-k",
        required=True,
        help="Agent API Key（通过 aoment_register.py 注册获取）",
    )
    args = parser.parse_args()

    try:
        result = query_quota(API_BASE, args.api_key)
    except requests.exceptions.Timeout:
        result = {"success": False, "error": "请求超时"}
    except requests.exceptions.RequestException as e:
        result = {"success": False, "error": f"网络请求失败: {str(e)}"}
    except Exception as e:
        result = {"success": False, "error": f"内部错误: {str(e)}"}

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
