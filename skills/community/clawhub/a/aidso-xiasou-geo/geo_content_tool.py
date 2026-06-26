#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2026 Beijing Aisou Quanyu (Beijing) Technology Co., Ltd. and/or its affiliates.
# Licensed under the Apache License, Version 2.0.

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import requests

ENV_KEY = "AIDSO_GEO_API_KEY"
ENV_FILE = Path(__file__).resolve().parent / ".env"

CONTENT_URL = "https://api.aidso.com/openapi/skills/run_realtime_report"
POINT_COST = 6

SUPPORTED_PLATFORMS = {
    "DB": "豆包",
    "DP": "Deepseek",
    "TXYB": "腾讯元宝",
    "WXYY": "文心一言",
    "TYQW": "通义千问",
    "KIMI": "KIMI",
    "DYAI": "抖音AI",
    "BDAI": "百度AI",
}

PLATFORM_ALIASES = {
    "豆包": "DB",
    "DB": "DB",
    "Deepseek": "DP",
    "deepseek": "DP",
    "DeepSeek": "DP",
    "DP": "DP",
    "腾讯元宝": "TXYB",
    "TXYB": "TXYB",
    "文心一言": "WXYY",
    "WXYY": "WXYY",
    "通义千问": "TYQW",
    "TYQW": "TYQW",
    "KIMI": "KIMI",
    "kimi": "KIMI",
    "抖音AI": "DYAI",
    "DYAI": "DYAI",
    "百度AI": "BDAI",
    "BDAI": "BDAI",
}


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False))


def load_env_file() -> Dict[str, str]:
    result: Dict[str, str] = {}
    if not ENV_FILE.exists():
        return result
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def get_api_key() -> Tuple[Optional[str], Optional[str]]:
    api_key = os.getenv(ENV_KEY)
    if api_key:
        return api_key.strip(), "environment"
    env_data = load_env_file()
    api_key = env_data.get(ENV_KEY)
    if api_key:
        return api_key.strip(), ".env"
    return None, None


def request_post(url: str, api_key: str, payload: Dict[str, Any], timeout: int = 180) -> Dict[str, Any]:
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            timeout=timeout,
        )
        try:
            data = response.json()
        except Exception:
            return {"code": -1, "msg": "response is not json", "data": response.text, "http_status": response.status_code}
        if response.status_code < 200 or response.status_code >= 300:
            return {"code": -1, "msg": "http status error", "data": data, "http_status": response.status_code}
        return data
    except requests.Timeout:
        return {"code": -1, "msg": "request timeout", "data": None}
    except requests.RequestException as e:
        return {"code": -1, "msg": f"request error: {e}", "data": None}


def normalize_platform(ai_platform: str) -> Tuple[Optional[str], Optional[str]]:
    text = str(ai_platform or "").strip()
    if not text:
        return None, None
    code = PLATFORM_ALIASES.get(text)
    if not code:
        return None, None
    return code, SUPPORTED_PLATFORMS[code]


def unsupported_platform_result(ai_platform: str) -> Dict[str, Any]:
    return {
        "ok": False,
        "unsupported_ai_platform": True,
        "ai_platform": ai_platform,
        "supported_platforms": list(SUPPORTED_PLATFORMS.values()),
        "supported_platform_codes": SUPPORTED_PLATFORMS,
        "msg": "当前目标优化平台不支持。请选择：豆包、Deepseek、腾讯元宝、文心一言、通义千问、KIMI、抖音AI、百度AI。",
    }


def extract_final_article(result: Dict[str, Any]) -> Optional[str]:
    data = result.get("data")

    if not isinstance(data, dict):
        return None

    final_article = data.get("final_article")

    if isinstance(final_article, str) and final_article.strip():
        return final_article.strip()

    return None


def is_content_success(result: Dict[str, Any]) -> bool:
    return (
        result.get("code") == 200
        and result.get("msg") == "success"
        and extract_final_article(result) is not None
    )


def is_content_processing(result: Dict[str, Any]) -> bool:
    return result.get("code") == 200 and "处理中" in str(result.get("msg", ""))


def call_content_api(brand: str, issue: str, platform_code: str) -> Dict[str, Any]:
    api_key, source = get_api_key()
    if not api_key:
        return {
            "ok": False,
            "need_bind_api_key": True,
            "env_key": ENV_KEY,
            "msg": "还没有绑定 API Key，请先发送：绑定 api-key：你的_api_key",
        }
    payload = {"brand": brand, "issue": issue, "platform": platform_code}
    result = request_post(CONTENT_URL, api_key, payload, timeout=180)
    result["_api_key_source"] = source
    return result


def generate_content(
    brand: str,
    issue: str,
    ai_platform: str,
    confirmed: bool = False,
    poll_interval: int = 90,
    max_poll_times: int = 5,
) -> Dict[str, Any]:
    brand = brand.strip()
    issue = issue.strip()
    if not brand:
        return {"ok": False, "msg": "brand 不能为空"}
    if not issue:
        return {"ok": False, "msg": "issue 不能为空"}
    platform_code, platform_label = normalize_platform(ai_platform)
    if not platform_code:
        return unsupported_platform_result(ai_platform)
    api_key, _source = get_api_key()
    if not api_key:
        return {
            "ok": False,
            "need_bind_api_key": True,
            "env_key": ENV_KEY,
            "msg": "还没有绑定 API Key，请先发送：绑定 api-key：你的_api_key",
        }
    if not confirmed:
        return {
            "ok": False,
            "need_points_confirmation": True,
            "point_cost": POINT_COST,
            "brand": brand,
            "issue": issue,
            "ai_platform": platform_label,
            "platform_code": platform_code,
            "msg": f"本次 GEO 内容生产将消耗 {POINT_COST} 积分。目标优化平台为 {platform_label}。确认后才会发起内容生产请求。",
        }
    if poll_interval <= 0:
        poll_interval = 90
    if max_poll_times <= 0:
        max_poll_times = 5

    last_result: Optional[Dict[str, Any]] = None
    task_id: Optional[str] = None
    api_key_source: Optional[str] = None
    for index in range(1, max_poll_times + 1):
        result = call_content_api(brand, issue, platform_code)
        last_result = result
        if result.get("ok") is False and result.get("need_bind_api_key"):
            return result
        api_key_source = result.get("_api_key_source")
        if is_content_success(result):
            return {
                "ok": True,
                "msg": "success",
                "brand": brand,
                "issue": issue,
                "ai_platform": platform_label,
                "platform_code": platform_code,
                "final_article": extract_final_article(result),
                "poll_times": index,
                "api_key_source": api_key_source,
            }
        if is_content_processing(result):
            if isinstance(result.get("data"), str):
                task_id = result.get("data")
            if index < max_poll_times:
                time.sleep(poll_interval)
            continue
        return {
            "ok": False,
            "msg": "内容生产失败",
            "brand": brand,
            "issue": issue,
            "ai_platform": platform_label,
            "platform_code": platform_code,
            "raw": result,
        }
    return {
        "ok": False,
        "msg": "内容仍在生成中，请稍后发送「继续」或「查询结果」再次查看。",
        "brand": brand,
        "issue": issue,
        "ai_platform": platform_label,
        "platform_code": platform_code,
        "task_id": task_id,
        "poll_times": max_poll_times,
        "raw": last_result,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="AIDSO GEO Content Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    platforms_parser = subparsers.add_parser("platforms", help="查看支持的目标优化平台")

    generate_parser = subparsers.add_parser("generate", help="根据品牌、AI问题和目标优化平台生成 GEO 内容")
    generate_parser.add_argument("--brand", required=True, help="品牌名称，例如 欧莱雅小蜜罐")
    generate_parser.add_argument("--issue", required=True, help="AI问题，例如 30岁左右抗老面霜推荐有哪些？")
    generate_parser.add_argument("--platform","--ai-platform",dest="platform",required=True,help="目标优化平台，例如 豆包、Deepseek、腾讯元宝、文心一言、通义千问、KIMI、抖音AI、百度AI")
    generate_parser.add_argument("--confirmed", "--confirm", dest="confirmed", action="store_true", help="确认消耗6积分后发起内容生产")
    generate_parser.add_argument("--poll-interval", type=int, default=90, help="轮询间隔秒数，默认 90 秒")
    generate_parser.add_argument("--max-poll-times", type=int, default=5, help="最大轮询次数，默认 5 次")

    args = parser.parse_args()
    if args.command == "platforms":
        print_json({"ok": True, "supported_platforms": SUPPORTED_PLATFORMS})
        return
    if args.command == "generate":
        result = generate_content(args.brand, args.issue, args.platform, args.confirmed, args.poll_interval, args.max_poll_times)
        print_json(result)
        if not result.get("ok"):
            sys.exit(1)
        return


if __name__ == "__main__":
    main()
