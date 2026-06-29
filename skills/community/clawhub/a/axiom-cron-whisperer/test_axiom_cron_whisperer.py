"""
🧪 Tests — axiom-cron-whisperer 
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from axiom_cron_whisperer import (
    explain,
    is_valid,
    parse_cron,
    parse_field,
)


class TestParseField(unittest.TestCase):
    """Tests de parse_field()."""

    def test_01_wildcard(self):
        """* = tous les valeurs."""
        self.assertEqual(parse_field("*", 0, 5), [0, 1, 2, 3, 4, 5])

    def test_02_exact(self):
        """N = valeur exacte."""
        self.assertEqual(parse_field("5", 0, 59), [5])

    def test_03_list(self):
        """N,M = liste."""
        self.assertEqual(parse_field("1,3,5", 0, 10), [1, 3, 5])

    def test_04_range(self):
        """N-M = range."""
        self.assertEqual(parse_field("1-5", 0, 10), [1, 2, 3, 4, 5])

    def test_05_step_wildcard(self):
        """*/N = step."""
        self.assertEqual(parse_field("*/15", 0, 59), [0, 15, 30, 45])

    def test_06_step_range(self):
        """N-M/S = step within range."""
        self.assertEqual(parse_field("0-30/10", 0, 59), [0, 10, 20, 30])


class TestParseCron(unittest.TestCase):
    """Tests de parse_cron()."""

    def test_07_valid_5_fields(self):
        """5 fields OK."""
        result = parse_cron("0 9 * * 1-5")
        self.assertEqual(result["minute"], [0])
        self.assertEqual(result["hour"], [9])
        self.assertEqual(result["day"], list(range(1, 32)))
        self.assertEqual(result["month"], list(range(1, 13)))
        self.assertEqual(result["dow"], [1, 2, 3, 4, 5])

    def test_08_invalid_field_count(self):
        """Doit rejeter si pas 5 fields."""
        with self.assertRaises(ValueError):
            parse_cron("0 9 * *")
        with self.assertRaises(ValueError):
            parse_cron("0 9 * * 1-5 extra")

    def test_09_invalid_value(self):
        """Doit rejeter valeur hors limites."""
        with self.assertRaises(ValueError):
            parse_cron("60 9 * * *")  # minute 60 invalide


class TestExplain(unittest.TestCase):
    """Tests d'explain()."""

    def test_10_weekdays_9am(self):
        """'0 9 * * 1-5' = 9am weekdays."""
        result = explain("0 9 * * 1-5", lang="en")
        self.assertIn("9", result)
        self.assertIn("Monday", result)
        self.assertIn("Friday", result)

    def test_11_every_15_min(self):
        """'*/15 * * * *' = every 15 minutes."""
        result = explain("*/15 * * * *", lang="en")
        self.assertIn("15", result)
        self.assertIn("minute", result.lower())

    def test_12_midnight(self):
        """'0 0 * * *' = midnight every day."""
        result = explain("0 0 * * *", lang="en")
        self.assertIn("0", result)
        self.assertIn("day", result.lower())

    def test_13_french(self):
        """Support du français."""
        result = explain("0 9 * * 1-5", lang="fr")
        self.assertIn("lundi", result.lower())
        self.assertIn("vendredi", result.lower())

    def test_14_january_only(self):
        """'0 0 1 1 *' = 1er janvier minuit."""
        result = explain("0 0 1 1 *", lang="en")
        self.assertIn("January", result)
        self.assertIn("1", result)


class TestValidate(unittest.TestCase):
    """Tests de is_valid()."""

    def test_15_valid(self):
        """Expressions valides."""
        self.assertTrue(is_valid("0 9 * * 1-5"))
        self.assertTrue(is_valid("*/5 * * * *"))
        self.assertTrue(is_valid("0 0 1 1 *"))

    def test_16_invalid(self):
        """Expressions invalides."""
        self.assertFalse(is_valid("0 9 * *"))  # 4 fields
        self.assertFalse(is_valid("0 9 * * 1-5 extra"))  # 6 fields
        self.assertFalse(is_valid("60 0 * * *"))  # minute invalide


class TestDeterminism(unittest.TestCase):
    """Tests de déterminisme."""

    def test_17_1000_runs_same(self):
        """1000 exécutions = même output."""
        expr = "0 9 * * 1-5"
        first = explain(expr)
        for _ in range(1000):
            self.assertEqual(explain(expr), first)


if __name__ == "__main__":
    unittest.main(verbosity=2)
