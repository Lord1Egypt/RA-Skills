"""Tests — axiom-iban-validator """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_iban_validator import (
    IBAN_LENGTHS,
    _format_iban,
    _mod97,
    validate,
)


class TestValidate(unittest.TestCase):
    def test_01_valid_fr(self):
        result = validate("FR76 3000 6000 0112 3456 7890 189")
        self.assertTrue(result["valid"])
        self.assertEqual(result["country"], "FR")
        self.assertEqual(result["length"], 27)

    def test_02_valid_de(self):
        result = validate("DE89370400440532013000")
        self.assertTrue(result["valid"])
        self.assertEqual(result["country"], "DE")

    def test_03_valid_gb(self):
        result = validate("GB82 WEST 1234 5698 7654 32")
        self.assertTrue(result["valid"])
        self.assertEqual(result["country"], "GB")

    def test_04_valid_be(self):
        result = validate("BE68539007547034")
        self.assertTrue(result["valid"])
        self.assertEqual(result["country"], "BE")

    def test_05_invalid_checksum(self):
        result = validate("FR7630006000011234567890188")  # bad check
        self.assertFalse(result["valid"])

    def test_06_wrong_length(self):
        result = validate("FR1234")  # too short
        self.assertFalse(result["valid"])
        self.assertIn("length", result.get("error", "").lower() or "short")

    def test_07_unknown_country(self):
        result = validate("XX1234567890123456789012")
        self.assertFalse(result["valid"])
        self.assertIn("Unknown", result.get("error", ""))

    def test_08_empty(self):
        result = validate("")
        self.assertFalse(result["valid"])

    def test_09_not_string(self):
        result = validate(123)
        self.assertFalse(result["valid"])


class TestMod97(unittest.TestCase):
    def test_10_mod97_rearranged(self):
        # Test internal: FR76... rearranged, mod 97 should be 1
        self.assertTrue(_mod97("FR7630006000011234567890189"))

    def test_11_mod97_bad(self):
        self.assertFalse(_mod97("FR7630006000011234567890188"))


class TestFormat(unittest.TestCase):
    def test_12_format(self):
        result = validate("DE89370400440532013000")
        self.assertIn(" ", result["formatted"])

    def test_13_strip_whitespace(self):
        result = validate("  DE89 3704 0044 0532 0130 00  ")
        self.assertTrue(result["valid"])


class TestDeterminism(unittest.TestCase):
    def test_14_1000_runs(self):
        i = "FR7630006000011234567890189"
        first = validate(i)
        for _ in range(1000):
            self.assertEqual(validate(i)["valid"], first["valid"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
