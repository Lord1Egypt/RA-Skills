#!/usr/bin/env python3
"""Unit tests for quote parsing (mock HTTP). Run: python3 test_quote.py."""

import json
import os
import sys
import unittest

# Run from scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Ensure no cache for tests
os.environ.pop("OPENCLAW_QUOTE_CACHE_TTL", None)


class TestQuoteParsing(unittest.TestCase):
    def test_parse_chart(self):
        import quote as m
        data = {
            "chart": {
                "result": [{
                    "meta": {
                        "symbol": "AAPL",
                        "shortName": "Apple Inc.",
                        "currency": "USD",
                        "regularMarketPrice": 175.5,
                        "previousClose": 174.0,
                        "regularMarketVolume": 50_000_000,
                        "fiftyTwoWeekHigh": 200.0,
                        "fiftyTwoWeekLow": 120.0,
                    }
                }]
            }
        }
        out = m._parse_chart(data, "AAPL")
        self.assertIsNotNone(out)
        self.assertEqual(out["symbol"], "AAPL")
        self.assertEqual(out["price"], 175.5)
        self.assertEqual(out["previousClose"], 174.0)
        self.assertAlmostEqual(out["change"], 1.5)
        self.assertAlmostEqual(out["changePercent"], 100 * 1.5 / 174.0)

    def test_parse_chart_invalid(self):
        import quote as m
        self.assertIsNone(m._parse_chart({}, "X"))
        self.assertIsNone(m._parse_chart({"chart": {}}, "X"))
        self.assertIsNone(m._parse_chart({"chart": {"result": []}}, "X"))

    def test_parse_finnhub(self):
        import quote as m
        data = {"c": 100.0, "pc": 98.0, "d": 2.0, "dp": 2.04}
        out = m._parse_finnhub(data, "AAPL")
        self.assertIsNotNone(out)
        self.assertEqual(out["symbol"], "AAPL")
        self.assertEqual(out["price"], 100.0)
        self.assertEqual(out["previousClose"], 98.0)
        self.assertEqual(out["change"], 2.0)
        self.assertAlmostEqual(out["changePercent"], 2.04)

    def test_parse_finnhub_inferred(self):
        import quote as m
        data = {"c": 100.0, "pc": 98.0}
        out = m._parse_finnhub(data, "MSFT")
        self.assertIsNotNone(out)
        self.assertEqual(out["change"], 2.0)
        self.assertAlmostEqual(out["changePercent"], 100 * 2.0 / 98.0)

    def test_format_quote(self):
        import quote as m
        info = {
            "symbol": "AAPL",
            "shortName": "Apple",
            "currency": "USD",
            "price": 175.5,
            "change": 1.5,
            "changePercent": 0.86,
        }
        s = m.format_quote(info)
        self.assertIn("Apple", s)
        self.assertIn("175.50", s)
        self.assertIn("+1.50", s)

    def test_format_quote_error(self):
        import quote as m
        s = m.format_quote({"symbol": "X", "error": "No data"})
        self.assertIn("X", s)
        self.assertIn("No data", s)

    def test_is_cn_hk_symbol(self):
        import quote as m
        self.assertTrue(m._is_cn_hk_symbol("600519.SS"))
        self.assertTrue(m._is_cn_hk_symbol("0700.HK"))
        self.assertTrue(m._is_cn_hk_symbol("000001.SZ"))
        self.assertTrue(m._is_cn_hk_symbol("SH600519"))
        self.assertTrue(m._is_cn_hk_symbol("600519"))
        self.assertFalse(m._is_cn_hk_symbol("AAPL"))
        self.assertFalse(m._is_cn_hk_symbol("MSFT"))


class TestCnQuoteParseSymbol(unittest.TestCase):
    def test_parse_symbol(self):
        import cn_quote as m
        self.assertEqual(m._parse_symbol("600519.SS"), ("sh", "600519", "600519.SS"))
        self.assertEqual(m._parse_symbol("000001.SZ"), ("sz", "000001", "000001.SZ"))
        self.assertEqual(m._parse_symbol("0700.HK"), ("hk", "00700", "0700.HK"))
        self.assertEqual(m._parse_symbol("HK00700"), ("hk", "00700", "HK00700"))
        self.assertEqual(m._parse_symbol("600519"), ("sh", "600519", "600519"))
        self.assertEqual(m._parse_symbol("000001"), ("sz", "000001", "000001"))


if __name__ == "__main__":
    unittest.main()
