#!/usr/bin/env python3
"""
aim-trade-news: 查询最新外贸资讯（AI 摘要版）
数据源：AEP Gateway trending_hub 服务
凭据：从 .env 或环境变量读取 AEP 配置
"""
import sys
import json
import os
import argparse

# Windows: 确保 stdout 用 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

import requests


API_URL = "https://aep.vemic.com/trending_hub/ai_collection"


def load_dotenv():
    """Load .env from skill root (parent of scripts/). Env vars take precedence."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
    if os.path.isfile(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key, val = key.strip(), val.strip()
                if key and key not in os.environ:
                    os.environ[key] = val


def get_aep_headers():
    """Read AEP credentials and return request headers."""
    load_dotenv()
    authorization = os.environ.get("AEP_AUTHORIZATION", "").strip()

    if not authorization:
        print(json.dumps({
            "success": False,
            "message": "AEP_AUTHORIZATION 未配置。请运行 --check-config 检查，或联系管理员获取凭证。"
        }, ensure_ascii=False))
        sys.exit(1)

    if not authorization.startswith(("Bearer ", "Basic ")):
        authorization = f"Bearer {authorization}"

    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": authorization,
    }


def check_config():
    """Check if AEP credentials are configured. Returns JSON status."""
    had_in_env = "AEP_AUTHORIZATION" in os.environ
    load_dotenv()
    authorization = os.environ.get("AEP_AUTHORIZATION", "").strip()

    if not authorization:
        print(json.dumps({
            "configured": False,
            "message": "AEP_AUTHORIZATION 未配置。请参考 references/aep-setup.md 进行配置。"
        }, ensure_ascii=False))
    else:
        source = "file:.env" if not had_in_env else "env:AEP_AUTHORIZATION"
        print(json.dumps({
            "configured": True,
            "source": source
        }, ensure_ascii=False))


TRENDING_HUB_OPEN_ID = "wGRriu8EVmsi4lBeYP"


def fetch_aim_trade_news(headers, open_id, days):
    """Call the AEP Gateway trending_hub ai_collection API."""
    payload = {
        "open_id": open_id,
        "category": "foreign_trade",
        "recentDays": days,
    }

    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"网络请求失败: {e}"
        }

    if resp.status_code != 200:
        return {
            "success": False,
            "message": f"API 请求失败 (HTTP {resp.status_code}): {resp.text[:300]}"
        }

    data = resp.json()

    if data.get("code") != 200 or not data.get("data"):
        return {
            "success": False,
            "message": data.get("message", "未知错误")
        }

    info = data["data"]
    items = info.get("dataInfo", [])

    return {
        "success": True,
        "dataUpdateTime": info.get("dataUpdateTime"),
        "dataSize": info.get("dataSize", len(items)),
        "items": [
            {
                "aiTitle": item.get("aiTitle", ""),
                "title": item.get("title", ""),
                "publishDate": item.get("publishDate", ""),
                "url": item.get("url", ""),
                "summary": item.get("summary", ""),
            }
            for item in items
        ]
    }


def main():
    parser = argparse.ArgumentParser(description="查询最新外贸资讯")
    parser.add_argument(
        "--days", type=int, default=3, choices=[1, 2, 3],
        help="查询最近几天的资讯（1/2/3，默认 3）"
    )
    parser.add_argument(
        "--check-config", action="store_true",
        help="检查 AEP 凭证是否已配置"
    )
    args = parser.parse_args()

    if args.check_config:
        check_config()
        return

    headers = get_aep_headers()
    result = fetch_aim_trade_news(headers, TRENDING_HUB_OPEN_ID, args.days)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
