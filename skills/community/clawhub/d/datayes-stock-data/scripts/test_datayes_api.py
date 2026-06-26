#!/usr/bin/env python3
"""Regression tests for Datayes parameter normalization."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datayes_api import DatayesError, _normalize_params, _validate_http_url


class NormalizeParamsTests(unittest.TestCase):
    def test_optional_defaults_are_not_injected(self) -> None:
        spec = {
            "data": {
                "nameEn": "fdmt_is_new_lt",
                "parametersInput": [
                    {"nameEn": "ticker", "mandatory": True, "defaultValue": None},
                    {"nameEn": "field", "mandatory": False, "defaultValue": "601988"},
                    {"nameEn": "reportType", "mandatory": False, "defaultValue": "Q3"},
                ],
            }
        }

        normalized, _ = _normalize_params(spec, {"ticker": "601988"})

        self.assertEqual(normalized, {"ticker": "601988"})

    def test_required_defaults_are_injected(self) -> None:
        spec = {
            "data": {
                "nameEn": "stock_search",
                "parametersInput": [
                    {"nameEn": "query", "mandatory": True, "defaultValue": None},
                    {"nameEn": "dataType", "mandatory": True, "defaultValue": "1"},
                    {"nameEn": "topK", "mandatory": True, "defaultValue": "10"},
                ],
            }
        }

        normalized, _ = _normalize_params(spec, {"query": "比亚迪"})

        self.assertEqual(normalized, {"query": "比亚迪", "dataType": 1, "topK": 10})

    def test_required_params_without_defaults_still_fail(self) -> None:
        spec = {
            "data": {
                "nameEn": "fdmt_is_new_q",
                "parametersInput": [
                    {"nameEn": "ticker", "mandatory": True, "defaultValue": None},
                    {"nameEn": "field", "mandatory": True, "defaultValue": None},
                ],
            }
        }

        with self.assertRaisesRegex(DatayesError, "Missing required parameters"):
            _normalize_params(spec, {"ticker": "601988"})


class ValidateHttpUrlTests(unittest.TestCase):
    def test_allows_trusted_datayes_host(self) -> None:
        url = "https://gw.datayes.com/stock/api/snapshot"

        self.assertEqual(_validate_http_url(url), url)

    def test_rejects_untrusted_host(self) -> None:
        with self.assertRaisesRegex(DatayesError, "is not trusted"):
            _validate_http_url("https://evil.example.com/stock/api/snapshot")

    def test_rejects_non_https_url(self) -> None:
        with self.assertRaisesRegex(DatayesError, "must use https"):
            _validate_http_url("http://gw.datayes.com/stock/api/snapshot")


if __name__ == "__main__":
    unittest.main()
