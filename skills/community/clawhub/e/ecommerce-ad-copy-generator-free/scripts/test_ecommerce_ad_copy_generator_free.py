#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ecommerce_ad_copy_generator_free import ValidationError, run, validate_payload


BASE_PAYLOAD = {
    "user_id": "u001",
    "product_name": "CloudBoost",
    "selling_points": ["智能出价", "多平台同步", "分钟级报表"],
    "target_audience": "跨境电商运营",
}


class EcommerceAdCopyGeneratorFreeTest(unittest.TestCase):
    def test_validate_payload_success(self):
        result = validate_payload(BASE_PAYLOAD)
        self.assertEqual(result["user_id"], "u001")
        self.assertEqual(len(result["selling_points"]), 3)

    def test_validate_payload_missing_points(self):
        payload = dict(BASE_PAYLOAD)
        payload["selling_points"] = []
        with self.assertRaises(ValidationError):
            validate_payload(payload)

    def test_run_free_success(self):
        result = run(BASE_PAYLOAD)
        self.assertTrue(result["success"])
        self.assertEqual(result["tier"], "free")
        self.assertEqual(len(result["copies"]), 3)
        self.assertTrue(result["upgrade"]["premium_available"])

    def test_run_premium_upgrade_required(self):
        payload = dict(BASE_PAYLOAD)
        payload["tier"] = "premium"
        result = run(payload)
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "PREMIUM_UPGRADE_REQUIRED")


if __name__ == "__main__":
    unittest.main()
