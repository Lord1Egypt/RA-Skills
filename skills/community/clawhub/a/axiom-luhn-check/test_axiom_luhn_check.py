"""Tests — axiom-luhn-check """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_luhn_check import (
    detect_type,
    format_credit_card,
    luhn_check,
    validate,
)


class TestLuhnCheck(unittest.TestCase):
    """Tests de l'algo Luhn."""

    def test_01_valid_visa(self):
        # Test Visa number (valid Luhn)
        self.assertTrue(luhn_check("4532015112830366"))

    def test_02_valid_amex(self):
        # Test Amex
        self.assertTrue(luhn_check("378282246310005"))

    def test_03_valid_mastercard(self):
        # Test Mastercard
        self.assertTrue(luhn_check("5555555555554444"))

    def test_04_invalid(self):
        self.assertFalse(luhn_check("4532015112830367"))  # bad checksum

    def test_05_empty(self):
        self.assertFalse(luhn_check(""))

    def test_06_with_spaces(self):
        # Spaces should be stripped
        self.assertTrue(luhn_check("4532 0151 1283 0366"))


class TestDetectType(unittest.TestCase):
    def test_07_visa(self):
        self.assertEqual(detect_type("4532015112830366"), "credit_card_visa")

    def test_08_amex(self):
        self.assertEqual(detect_type("378282246310005"), "credit_card_amex")

    def test_09_mastercard(self):
        self.assertEqual(detect_type("5555555555554444"), "credit_card_mastercard")

    def test_10_imei(self):
        # IMEI 15 digits
        self.assertEqual(detect_type("490154203237518"), "imei")

    def test_11_siret(self):
        # SIRET 14 digits
        self.assertEqual(detect_type("73282932000074"), "siret")


class TestValidate(unittest.TestCase):
    def test_12_valid_visa(self):
        result = validate("4532015112830366")
        self.assertTrue(result["valid"])
        self.assertTrue(result["luhn_ok"])
        self.assertEqual(result["type"], "credit_card_visa")

    def test_13_invalid_checksum(self):
        result = validate("4532015112830367")
        self.assertFalse(result["valid"])
        self.assertFalse(result["luhn_ok"])

    def test_14_with_spaces(self):
        result = validate("4532 0151 1283 0366")
        self.assertTrue(result["valid"])

    def test_15_force_type(self):
        # Even if detected as visa, force as mastercard → mismatch
        result = validate("4532015112830366", expected_type="credit_card_mastercard")
        self.assertFalse(result["valid"])  # type mismatch
        self.assertTrue(result["luhn_ok"])


class TestFormat(unittest.TestCase):
    def test_16_format_visa(self):
        formatted = format_credit_card("4532015112830366")
        self.assertEqual(formatted, "4532 0151 1283 0366")

    def test_17_format_amex(self):
        formatted = format_credit_card("378282246310005")
        self.assertEqual(formatted, "3782 822463 10005")


class TestDeterminism(unittest.TestCase):
    def test_18_1000_runs(self):
        n = "4532015112830366"
        first = validate(n)
        for _ in range(1000):
            self.assertEqual(validate(n)["valid"], first["valid"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
