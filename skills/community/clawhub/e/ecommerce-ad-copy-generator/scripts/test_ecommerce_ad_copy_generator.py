#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ecommerce_ad_copy_generator import (
    BillingError,
    ChargeResult,
    InsufficientBalanceError,
    SkillPayClient,
    ValidationError,
    run_generation,
    validate_payload,
)


class FakeSkillPayClient(SkillPayClient):
    def __init__(self, scripted_results: list[ChargeResult]):
        super().__init__(endpoint="http://test.local/billing/charge")
        self.scripted_results = scripted_results
        self.calls = 0

    def charge(self, *, user_id: str, amount_usdt: Decimal, metadata: dict):  # type: ignore[override]
        self.calls += 1
        if self.scripted_results:
            return self.scripted_results.pop(0)
        return ChargeResult(success=True, transaction_id=f"tx-{self.calls}")


BASE_PAYLOAD = {
    "user_id": "user_001",
    "product_name": "CloudBoost 智能投放器",
    "selling_points": ["智能出价", "多平台同步", "分钟级报表"],
    "target_audience": "跨境电商运营团队",
}


class EcommerceAdCopyGeneratorTest(unittest.TestCase):
    def test_validate_payload_success(self):
        result = validate_payload(BASE_PAYLOAD)
        self.assertEqual(result["user_id"], "user_001")
        self.assertEqual(len(result["selling_points"]), 3)

    def test_validate_payload_accepts_string_selling_points(self):
        payload = dict(BASE_PAYLOAD)
        payload["selling_points"] = "智能出价, 多平台同步;分钟级报表"
        result = validate_payload(payload)
        self.assertEqual(result["selling_points"], ["智能出价", "多平台同步", "分钟级报表"])

    def test_validate_payload_missing_user_id(self):
        payload = dict(BASE_PAYLOAD)
        payload["user_id"] = ""
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_validate_payload_rejects_bad_product_name(self):
        payload = dict(BASE_PAYLOAD)
        payload["product_name"] = "A"
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_validate_payload_rejects_empty_selling_points(self):
        payload = dict(BASE_PAYLOAD)
        payload["selling_points"] = []
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_run_generation_success(self):
        billing = FakeSkillPayClient([ChargeResult(success=True, transaction_id="tx-100")])
        result = run_generation(BASE_PAYLOAD, billing_client=billing)
        self.assertTrue(result["success"])
        self.assertEqual(result["pricing"]["amount"], "0.10")
        self.assertEqual(len(result["copies"]), 5)
        self.assertEqual({copy["platform"] for copy in result["copies"]}, {"Facebook", "Google", "TikTok"})

    def test_run_generation_insufficient_balance(self):
        billing = FakeSkillPayClient(
            [
                ChargeResult(
                    success=False,
                    error_code="INSUFFICIENT_BALANCE",
                    payment_url="https://skillpay.me/pay?user_id=user_001",
                )
            ]
        )
        with self.assertRaises(InsufficientBalanceError) as context:
            run_generation(BASE_PAYLOAD, billing_client=billing)
        self.assertIn("余额不足", str(context.exception))
        self.assertEqual(context.exception.payment_url, "https://skillpay.me/pay?user_id=user_001")

    def test_run_generation_billing_error(self):
        billing = FakeSkillPayClient([ChargeResult(success=False, error_code="SERVICE_UNAVAILABLE")])
        with self.assertRaises(BillingError):
            run_generation(BASE_PAYLOAD, billing_client=billing)

    def test_end_to_end_ten_samples(self):
        samples = [
            {
                "user_id": f"user_{index:03d}",
                "product_name": f"产品{index}",
                "selling_points": [f"卖点{index}A", f"卖点{index}B", f"卖点{index}C"],
                "target_audience": "独立站卖家",
            }
            for index in range(1, 11)
        ]
        billing = FakeSkillPayClient([ChargeResult(success=True, transaction_id=f"tx-{i}") for i in range(10)])

        passed = 0
        for sample in samples:
            result = run_generation(sample, billing_client=billing)
            self.assertTrue(result["success"])
            self.assertEqual(len(result["copies"]), 5)
            passed += 1

        self.assertEqual(passed, 10)
        self.assertEqual(billing.calls, 10)

    def test_conversion_targets_simulation(self):
        billing = FakeSkillPayClient(
            [ChargeResult(success=True, transaction_id=f"tx-{i}") for i in range(8)]
            + [
                ChargeResult(
                    success=False,
                    error_code="INSUFFICIENT_BALANCE",
                    payment_url="https://skillpay.me/pay?user_id=topup-1",
                ),
                ChargeResult(success=True, transaction_id="tx-topup-1"),
                ChargeResult(
                    success=False,
                    error_code="INSUFFICIENT_BALANCE",
                    payment_url="https://skillpay.me/pay?user_id=topup-2",
                ),
                ChargeResult(success=True, transaction_id="tx-topup-2"),
            ]
        )

        payment_triggered = 0
        recharge_success = 0

        for index in range(8):
            payload = dict(BASE_PAYLOAD)
            payload["user_id"] = f"ok_{index}"
            result = run_generation(payload, billing_client=billing)
            self.assertTrue(result["success"])
            payment_triggered += 1

        for user in ["topup-1", "topup-2"]:
            payload = dict(BASE_PAYLOAD)
            payload["user_id"] = user
            with self.assertRaises(InsufficientBalanceError) as context:
                run_generation(payload, billing_client=billing)
            self.assertIn("https://skillpay.me/pay", context.exception.payment_url or "")
            payment_triggered += 1

            result = run_generation(payload, billing_client=billing)
            self.assertTrue(result["success"])
            recharge_success += 1
            payment_triggered += 1

        self.assertGreaterEqual(payment_triggered, 8)
        self.assertGreaterEqual(recharge_success, 2)


if __name__ == "__main__":
    unittest.main()
