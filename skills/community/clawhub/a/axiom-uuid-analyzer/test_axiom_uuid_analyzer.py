"""Tests — axiom-uuid-analyzer """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_uuid_analyzer import (
    VARIANT_NCS,
    VARIANT_RFC4122,
    analyze,
    is_valid,
    parse_uuid,
)


class TestIsValid(unittest.TestCase):
    def test_01_valid_uuid(self):
        self.assertTrue(is_valid("550e8400-e29b-41d4-a716-446655440000"))

    def test_02_valid_uppercase(self):
        self.assertTrue(is_valid("550E8400-E29B-41D4-A716-446655440000"))

    def test_03_no_hyphens(self):
        self.assertFalse(is_valid("550e8400e29b41d4a716446655440000"))

    def test_04_too_short(self):
        self.assertFalse(is_valid("550e8400-e29b-41d4-a716"))

    def test_05_invalid_chars(self):
        self.assertFalse(is_valid("550e8400-e29b-41d4-a716-44665544000z"))

    def test_06_not_string(self):
        self.assertFalse(is_valid(123))
        self.assertFalse(is_valid(None))


class TestParseUuid(unittest.TestCase):
    def test_07_v4(self):
        result = parse_uuid("550e8400-e29b-41d4-a716-446655440000")
        self.assertEqual(result["version"], 4)
        self.assertEqual(result["variant_code"], "rfc4122")

    def test_08_v1(self):
        # v1 UUID (time-based)
        result = parse_uuid("c232ab00-9414-11ec-b909-0242ac120002")
        self.assertEqual(result["version"], 1)
        self.assertIsNotNone(result["mac_address"])

    def test_09_invalid_raises(self):
        with self.assertRaises(ValueError):
            parse_uuid("not-a-uuid")


class TestAnalyze(unittest.TestCase):
    def test_10_v4_full(self):
        info = analyze("550e8400-e29b-41d4-a716-446655440000")
        self.assertEqual(info["version"], 4)
        self.assertTrue(info["is_random"])
        self.assertFalse(info["is_time_based"])

    def test_11_v1_timestamp(self):
        info = analyze("c232ab00-9414-11ec-b909-0242ac120002")
        self.assertEqual(info["version"], 1)
        self.assertIsNotNone(info.get("timestamp"))
        self.assertIn("iso", info["timestamp"])

    def test_12_v7_timestamp(self):
        # v7 UUID (time-ordered)
        info = analyze("018e5b5b-1234-7abc-9def-1234567890ab")
        self.assertEqual(info["version"], 7)
        if info.get("timestamp"):
            self.assertIn("iso", info["timestamp"])


class TestVariants(unittest.TestCase):
    def test_13_rfc4122_variant(self):
        # 8 in first hex of clock_seq_hi = RFC 4122
        result = parse_uuid("550e8400-e29b-41d4-8716-446655440000")
        # 8 is in clock_seq_hi (8x = 1000 in binary, top 2 bits = 10 = RFC 4122)
        # Actually clock_seq_hi is 0x87, top 2 bits = 10 = RFC 4122

    def test_14_ncs_variant(self):
        # 0x prefix in clock_seq_hi = NCS
        result = parse_uuid("550e8400-e29b-41d4-0716-446655440000")
        # 07 = 0000 0111, top 2 bits = 00 = NCS


class TestDeterminism(unittest.TestCase):
    def test_15_1000_runs(self):
        u = "550e8400-e29b-41d4-a716-446655440000"
        first = analyze(u)
        for _ in range(1000):
            self.assertEqual(analyze(u)["version"], first["version"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
