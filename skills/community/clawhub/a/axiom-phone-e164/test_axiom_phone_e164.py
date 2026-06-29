"""Tests — axiom-phone-e164 """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_phone_e164 import (
    COUNTRY_DATA,
    is_valid,
    parse,
)


class TestParse(unittest.TestCase):
    def test_01_fr_with_plus(self):
        result = parse("+33 6 12 34 56 78")
        self.assertTrue(result["valid"])
        self.assertEqual(result["e164"], "+33612345678")
        self.assertEqual(result["country_code"], "33")

    def test_02_fr_no_plus(self):
        result = parse("06 12 34 56 78", default_country="33")
        self.assertTrue(result["valid"])
        self.assertEqual(result["e164"], "+33612345678")

    def test_02b_us_no_plus(self):
        result = parse("(514) 555-1234", default_country="1")
        self.assertTrue(result["valid"])
        self.assertEqual(result["e164"], "+15145551234")

    def test_03_us_with_plus(self):
        result = parse("+1 555 123 4567")
        self.assertTrue(result["valid"])
        self.assertEqual(result["e164"], "+15551234567")

    def test_04_uk_with_plus(self):
        result = parse("+44 20 7946 0958")
        self.assertTrue(result["valid"])
        self.assertEqual(result["e164"], "+442079460958")
        self.assertEqual(result["country_code"], "44")

    def test_05_de(self):
        result = parse("+49 30 12345678")
        self.assertTrue(result["valid"])

    def test_06_wrong_length(self):
        result = parse("+33 6 12 34 56")
        self.assertFalse(result["valid"])
        self.assertIn("Wrong length", result.get("error", ""))

    def test_07_unknown_country(self):
        result = parse("+999 123 456")
        self.assertFalse(result["valid"])

    def test_08_empty(self):
        result = parse("")
        self.assertFalse(result["valid"])

    def test_09_not_string(self):
        result = parse(12345)
        self.assertFalse(result["valid"])

    def test_10_jp(self):
        result = parse("+81 3 1234 5678")
        self.assertTrue(result["valid"])
        self.assertEqual(result["country_code"], "81")


class TestIsValid(unittest.TestCase):
    def test_11_valid(self):
        self.assertTrue(is_valid("+33 6 12 34 56 78"))

    def test_12_invalid(self):
        self.assertFalse(is_valid("+33 123"))


class TestDeterminism(unittest.TestCase):
    def test_13_1000_runs(self):
        p = "+33612345678"
        first = parse(p)
        for _ in range(1000):
            self.assertEqual(parse(p)["valid"], first["valid"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
