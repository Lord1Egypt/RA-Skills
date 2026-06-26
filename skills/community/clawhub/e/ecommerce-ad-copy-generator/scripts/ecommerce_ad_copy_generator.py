#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from urllib import error, request

PRICE_USDT = Decimal("0.10")
DEFAULT_TIMEOUT_SECONDS = 10


class ValidationError(ValueError):
    pass


class BillingError(RuntimeError):
    pass


class InsufficientBalanceError(BillingError):
    def __init__(self, message: str, payment_url: str | None = None):
        super().__init__(message)
        self.payment_url = payment_url


@dataclass
class ChargeResult:
    success: bool
    transaction_id: str | None = None
    payment_url: str | None = None
    status_code: int | None = None
    error_code: str | None = None
    raw_response: dict[str, Any] | None = None


def _to_list(raw_selling_points: Any) -> list[str]:
    if isinstance(raw_selling_points, list):
        points = [str(item).strip() for item in raw_selling_points if str(item).strip()]
    elif isinstance(raw_selling_points, str):
        parts = re.split(r"[\n,;；|]+", raw_selling_points)
        points = [item.strip() for item in parts if item.strip()]
    else:
        points = []
    return points


def validate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    user_id = str(payload.get("user_id", "")).strip()
    product_name = str(payload.get("product_name", "")).strip()
    target_audience = str(payload.get("target_audience", "")).strip()
    selling_points = _to_list(payload.get("selling_points"))

    if not user_id:
        raise ValidationError("`user_id` is required.")
    if len(user_id) > 64:
        raise ValidationError("`user_id` length must be <= 64.")

    if len(product_name) < 2 or len(product_name) > 80:
        raise ValidationError("`product_name` length must be between 2 and 80.")

    if len(target_audience) < 2 or len(target_audience) > 120:
        raise ValidationError("`target_audience` length must be between 2 and 120.")

    if not selling_points:
        raise ValidationError("`selling_points` is required and cannot be empty.")
    if len(selling_points) > 6:
        raise ValidationError("`selling_points` can contain up to 6 items.")

    for point in selling_points:
        if len(point) < 2 or len(point) > 120:
            raise ValidationError("Each selling point length must be between 2 and 120.")

    return {
        "user_id": user_id,
        "product_name": product_name,
        "target_audience": target_audience,
        "selling_points": selling_points,
    }


def _safe_json_load(raw: bytes) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}


def _normalize_payment_url(data: dict[str, Any], user_id: str) -> str | None:
    payment_url = data.get("payment_url") or data.get("pay_url")
    if payment_url:
        return str(payment_url)

    template = os.getenv("SKILLPAY_PAYMENT_URL_TEMPLATE", "").strip()
    if template:
        return template.format(user_id=user_id)

    base = os.getenv("SKILLPAY_TOPUP_BASE_URL", "https://skillpay.me/pay").strip()
    if not base:
        return None

    separator = "&" if "?" in base else "?"
    return f"{base}{separator}user_id={user_id}"


def _extract_error_code(data: dict[str, Any]) -> str:
    fields = ["code", "error_code", "status", "error", "message"]
    values = [str(data.get(field, "")) for field in fields]
    merged = " ".join(values).lower()
    if any(token in merged for token in ["insufficient", "balance", "not_enough", "low_balance", "402"]):
        return "INSUFFICIENT_BALANCE"
    return str(data.get("code") or data.get("error_code") or "BILLING_ERROR").upper()


class SkillPayClient:
    def __init__(
        self,
        *,
        endpoint: str | None = None,
        api_key: str | None = None,
        timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.endpoint = endpoint or os.getenv("SKILLPAY_CHARGE_ENDPOINT", "https://skillpay.me/billing/charge")
        self.api_key = api_key if api_key is not None else os.getenv("SKILLPAY_API_KEY")
        self.timeout_seconds = timeout_seconds

    def charge(self, *, user_id: str, amount_usdt: Decimal, metadata: dict[str, Any]) -> ChargeResult:
        payload = {
            "user_id": user_id,
            "amount": f"{amount_usdt:.2f}",
            "currency": "USDT",
            "item": "ecommerce-ad-copy-generator",
            "metadata": metadata,
            "trace_id": str(uuid.uuid4()),
        }
        body = json.dumps(payload).encode("utf-8")

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = request.Request(self.endpoint, data=body, headers=headers, method="POST")

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                response_data = _safe_json_load(response.read())
                status = getattr(response, "status", 200)
                success = bool(response_data.get("success", True)) and status < 300
                return ChargeResult(
                    success=success,
                    transaction_id=str(response_data.get("transaction_id", "")) or None,
                    payment_url=_normalize_payment_url(response_data, user_id),
                    status_code=status,
                    error_code=None if success else _extract_error_code(response_data),
                    raw_response=response_data,
                )
        except error.HTTPError as http_err:
            data = _safe_json_load(http_err.read())
            code = _extract_error_code(data)
            payment_url = _normalize_payment_url(data, user_id)
            if http_err.code == 402 or code == "INSUFFICIENT_BALANCE":
                return ChargeResult(
                    success=False,
                    payment_url=payment_url,
                    status_code=http_err.code,
                    error_code="INSUFFICIENT_BALANCE",
                    raw_response=data,
                )
            return ChargeResult(
                success=False,
                payment_url=payment_url,
                status_code=http_err.code,
                error_code=code,
                raw_response=data,
            )
        except error.URLError as network_err:
            raise BillingError(f"Billing network error: {network_err}") from network_err


def _build_copies(product_name: str, selling_points: list[str], target_audience: str) -> list[dict[str, str]]:
    focus = selling_points[:3] + [selling_points[0]] * (3 - len(selling_points[:3]))
    point_a, point_b, point_c = focus[:3]

    copies = [
        {
            "platform": "Facebook",
            "headline": f"{product_name}：把{target_audience}想要的体验一次给到",
            "body": f"还在为{point_a}烦恼？{product_name}主打{point_a}、{point_b}，帮助{target_audience}更快看到结果。",
            "cta": "立即查看",
        },
        {
            "platform": "Facebook",
            "headline": f"为什么{target_audience}都在换用{product_name}",
            "body": f"核心卖点：{point_a} / {point_b} / {point_c}。现在试用{product_name}，降低决策成本，提升转化效率。",
            "cta": "马上体验",
        },
        {
            "platform": "Google",
            "headline": f"{product_name}｜{point_a}",
            "body": f"为{target_audience}设计，突出{point_b}。立即了解{product_name}，快速验证增长效果。",
            "cta": "立即咨询",
        },
        {
            "platform": "Google",
            "headline": f"{product_name} - {point_b}",
            "body": f"聚焦{point_a}与{point_c}，帮助{target_audience}用更低成本获得更高广告回报。",
            "cta": "获取方案",
        },
        {
            "platform": "TikTok",
            "headline": f"{product_name}上新⚡",
            "body": f"{target_audience}冲！{product_name}把{point_a}+{point_b}直接拉满，{point_c}也稳住。#电商增长 #广告投放 #效率提升",
            "cta": "点我开冲",
        },
    ]
    return copies


def run_generation(payload: dict[str, Any], billing_client: SkillPayClient | None = None) -> dict[str, Any]:
    validated = validate_payload(payload)
    client = billing_client or SkillPayClient()

    billing_result = client.charge(
        user_id=validated["user_id"],
        amount_usdt=PRICE_USDT,
        metadata={
            "product_name": validated["product_name"],
            "target_audience": validated["target_audience"],
        },
    )

    if not billing_result.success:
        if billing_result.error_code == "INSUFFICIENT_BALANCE":
            message = "余额不足，请先充值后重试。"
            raise InsufficientBalanceError(message=message, payment_url=billing_result.payment_url)
        raise BillingError(
            f"Billing charge failed: {billing_result.error_code or 'UNKNOWN_ERROR'}"
        )

    copies = _build_copies(
        validated["product_name"],
        validated["selling_points"],
        validated["target_audience"],
    )

    return {
        "success": True,
        "pricing": {
            "amount": f"{PRICE_USDT:.2f}",
            "currency": "USDT",
            "charged": True,
            "transaction_id": billing_result.transaction_id,
        },
        "input": validated,
        "copies": copies,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ecommerce ad copy generator with SkillPay billing.")
    parser.add_argument("--input-json", help="Full JSON payload string.")
    parser.add_argument("--input-file", help="Path to JSON payload file.")
    parser.add_argument("--user-id", help="User id for billing.")
    parser.add_argument("--product-name", help="Product name.")
    parser.add_argument("--selling-points", nargs="*", help="Selling points list.")
    parser.add_argument("--target-audience", help="Target audience.")
    return parser


def _parse_payload(args: argparse.Namespace) -> dict[str, Any]:
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
    }


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    try:
        payload = _parse_payload(args)
        result = run_generation(payload)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except ValidationError as err:
        print(json.dumps({"success": False, "error": "VALIDATION_ERROR", "message": str(err)}, ensure_ascii=False))
        return 2
    except InsufficientBalanceError as err:
        print(
            json.dumps(
                {
                    "success": False,
                    "error": "INSUFFICIENT_BALANCE",
                    "message": str(err),
                    "payment_url": err.payment_url,
                },
                ensure_ascii=False,
            )
        )
        return 3
    except BillingError as err:
        print(json.dumps({"success": False, "error": "BILLING_ERROR", "message": str(err)}, ensure_ascii=False))
        return 4
    except json.JSONDecodeError as err:
        print(json.dumps({"success": False, "error": "INVALID_JSON", "message": str(err)}, ensure_ascii=False))
        return 5


if __name__ == "__main__":
    sys.exit(main())
