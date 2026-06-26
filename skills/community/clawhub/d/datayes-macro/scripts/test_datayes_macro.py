#!/usr/bin/env python3
"""Regression tests for Datayes macro helpers."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from datayes_macro import DatayesError, validate_http_url


class ValidateHttpUrlTests(unittest.TestCase):
    def test_allows_trusted_datayes_host(self) -> None:
        url = "https://gw.datayes.com/macro/api/search"

        self.assertEqual(validate_http_url(url), url)

    def test_rejects_untrusted_host(self) -> None:
        with self.assertRaisesRegex(DatayesError, "is not trusted"):
            validate_http_url("https://evil.example.com/macro/api/search")

    def test_rejects_non_https_url(self) -> None:
        with self.assertRaisesRegex(DatayesError, "must use https"):
            validate_http_url("http://gw.datayes.com/macro/api/search")


if __name__ == "__main__":
    unittest.main()
