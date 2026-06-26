#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any


class ValidationError(ValueError):
    pass


def _to_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [part.strip() for part in re.split(r"[\n,;；|]+", value) if part.strip()]
    return []


def _payment_url(user_id: str) -> str:
    template = os.getenv("SKILLPAY_PAYMENT_URL_TEMPLATE", "").strip()
    if template:
        return template.format(user_id=user_id)
    base = os.getenv("SKILLPAY_TOPUP_BASE_URL", "https://skillpay.me/pay").strip()
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}user_id={user_id}"


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    user_id = str(payload.get("user_id", "")).strip()
    product_name = str(payload.get("product_name", "")).strip()
    target_audience = str(payload.get("target_audience", "")).strip()
    selling_points = _to_list(payload.get("selling_points"))

    if not user_id:
        raise ValidationError("`user_id` is required")
    if len(product_name) < 2 or len(product_name) > 80:
        raise ValidationError("`product_name` length must be 2-80")
    if len(target_audience) < 2 or len(target_audience) > 120:
        raise ValidationError("`target_audience` length must be 2-120")
    if not selling_points:
        raise ValidationError("`selling_points` cannot be empty")

    return {
        "user_id": user_id,
        "product_name": product_name,
        "target_audience": target_audience,
        "selling_points": selling_points[:6],
    }


def _free_copies(product_name: str, points: list[str], audience: str) -> list[dict[str, str]]:
    first = points[0]
    second = points[1] if len(points) > 1 else points[0]
    third = points[2] if len(points) > 2 else points[0]
    return [
        {
            "platform": "Facebook",
            "headline": f"{product_name}：{audience}都在关注",
            "body": f"主打{first}与{second}，更适合{audience}快速起量。",
            "cta": "立即查看",
        },
        {
            "platform": "Google",
            "headline": f"{product_name}｜{first}",
            "body": f"聚焦{second}和{third}，帮助{audience}更快拿到结果。",
            "cta": "获取方案",
        },
        {
            "platform": "TikTok",
            "headline": f"{product_name} 上新",
            "body": f"{audience}冲！{first}+{second}直接拉满。",
            "cta": "点我开冲",
        },
    ]


def run(payload: dict[str, Any]) -> dict[str, Any]:
    validated = validate_payload(payload)
    tier = str(payload.get("tier", "free")).strip().lower()

    upgrade = {
        "premium_available": True,
        "price_usdt": "0.10",
        "payment_url": _payment_url(validated["user_id"]),
        "premium_features": [
            "从3条扩展到10条广告文案",
            "自动A/B测试版本",
            "多语种文案输出",
        ],
    }

    if tier == "premium":
        return {
            "success": False,
            "error": "PREMIUM_UPGRADE_REQUIRED",
            "message": "当前仅开放免费基础版，付费高级版接口已预留。",
            "upgrade": upgrade,
        }

    return {
        "success": True,
        "tier": "free",
        "input": validated,
        "copies": _free_copies(
            validated["product_name"],
            validated["selling_points"],
            validated["target_audience"],
        ),
        "upgrade": upgrade,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ecommerce ad copy generator (free tier)")
    parser.add_argument("--input-json")
    parser.add_argument("--input-file")
    parser.add_argument("--user-id")
    parser.add_argument("--product-name")
    parser.add_argument("--selling-points", nargs="*")
    parser.add_argument("--target-audience")
    parser.add_argument("--tier", default="free")
    return parser.parse_args()


def _payload_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.input_json:
        return json.loads(args.input_json)
    if args.input_file:
        with open(args.input_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return {
        "user_id": args.user_id,
        "product_name": args.product_name,
        "selling_points": args.selling_points,
        "target_audience": args.target_audience,
        "tier": args.tier,
    }


def main() -> int:
    args = _parse_args()
    try:
        result = run(_payload_from_args(args))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get("success") else 3
    except ValidationError as err:
        print(json.dumps({"success": False, "error": "VALIDATION_ERROR", "message": str(err)}, ensure_ascii=False))
        return 2
    except json.JSONDecodeError as err:
        print(json.dumps({"success": False, "error": "INVALID_JSON", "message": str(err)}, ensure_ascii=False))
        return 5


if __name__ == "__main__":
    sys.exit(main())
