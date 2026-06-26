#!/usr/bin/env python3
"""Regression tests for datayes web search helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datayes_web_search import DatayesError, normalize_scope, normalize_top, validate_http_url


class ValidateHttpUrlTests(unittest.TestCase):
    def test_allows_trusted_datayes_host(self) -> None:
        url = "https://gw.datayes.com/aladdin_info/web/gptMaterials/v2"

        self.assertEqual(validate_http_url(url), url)

    def test_rejects_untrusted_host(self) -> None:
        with self.assertRaisesRegex(DatayesError, "is not trusted"):
            validate_http_url("https://evil.example.com/aladdin_info/web/gptMaterials/v2")

    def test_rejects_non_https_url(self) -> None:
        with self.assertRaisesRegex(DatayesError, "must use https"):
            validate_http_url("http://gw.datayes.com/aladdin_info/web/gptMaterials/v2")


class NormalizeScopeTests(unittest.TestCase):
    def test_accepts_known_scope(self) -> None:
        self.assertEqual(normalize_scope("research"), "research")

    def test_blank_scope_becomes_none(self) -> None:
        self.assertIsNone(normalize_scope("   "))

    def test_rejects_unknown_scope(self) -> None:
        with self.assertRaisesRegex(DatayesError, "Invalid queryScope"):
            normalize_scope("all-news")


class NormalizeTopTests(unittest.TestCase):
    def test_caps_top_to_max(self) -> None:
        self.assertEqual(normalize_top(999), 50)

    def test_rejects_non_positive_value(self) -> None:
        with self.assertRaisesRegex(DatayesError, "positive integer"):
            normalize_top(0)


if __name__ == "__main__":
    unittest.main()
