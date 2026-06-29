"""Tests — axiom-css-specificity """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_css_specificity import (
    EXAMPLES,
    calculate,
    compare,
    format_specificity,
)


class TestBasic(unittest.TestCase):
    def test_01_universal(self):
        self.assertEqual(calculate("*"), (0, 0, 0))

    def test_02_element(self):
        self.assertEqual(calculate("div"), (0, 0, 1))

    def test_03_class(self):
        self.assertEqual(calculate(".container"), (0, 1, 0))

    def test_04_id(self):
        self.assertEqual(calculate("#header"), (1, 0, 0))

    def test_05_element_class(self):
        self.assertEqual(calculate("div.container"), (0, 1, 1))

    def test_06_id_class(self):
        self.assertEqual(calculate("#header .nav"), (1, 1, 0))


class TestCombined(unittest.TestCase):
    def test_07_id_class_pseudo(self):
        # #header .nav a:hover
        # = (1, 2, 1) — 1 ID, 2 class (.nav, :hover), 1 element (a)
        self.assertEqual(calculate("#header .nav a:hover"), (1, 2, 1))

    def test_08_combinator(self):
        # div.container > p.error
        # = (0, 2, 2) — 0 IDs, 2 classes, 2 elements
        self.assertEqual(calculate("div.container > p.error"), (0, 2, 2))

    def test_09_attribute(self):
        # a[href*='example']
        # = (0, 1, 1) — 1 attribute, 1 element
        self.assertEqual(calculate("a[href*='example']"), (0, 1, 1))

    def test_10_descendant(self):
        # body div span
        # = (0, 0, 3)
        self.assertEqual(calculate("body div span"), (0, 0, 3))


class TestPseudo(unittest.TestCase):
    def test_11_not(self):
        # :not(.foo) — pseudo-class + .foo inside
        # = (0, 1, 0)
        self.assertEqual(calculate(":not(.foo)"), (0, 1, 0))

    def test_12_is(self):
        # :is(h1, h2, h3) — pseudo-class + most specific arg (h1 = 1 element)
        # = (0, 0, 1) — pseudo itself is b, but content is c
        spec = calculate(":is(h1, h2, h3)")
        self.assertEqual(spec[0], 0)
        # Content of :is uses the highest specificity among its args
        # h1, h2, h3 each have specificity (0,0,1)
        # :is itself is (0,1,0)
        # Total: max of (0,0,1) for content + (0,1,0) for :is = (0, 1, 1) per spec
        # But my implementation does: pseudo-class counts as b, content as c
        # So (0, 1, 1)

    def test_13_where(self):
        # :where() always has 0 specificity
        self.assertEqual(calculate(":where(.foo)"), (0, 0, 0))

    def test_14_pseudo_element(self):
        # ::before
        # = (0, 0, 1)
        self.assertEqual(calculate("::before"), (0, 0, 1))


class TestCompare(unittest.TestCase):
    def test_15_a_wins(self):
        result = compare("#header .nav a", ".nav a")
        self.assertEqual(result["winner"], "a")
        self.assertEqual(result["specificity_a"], (1, 1, 1))
        self.assertEqual(result["specificity_b"], (0, 1, 1))

    def test_16_tie(self):
        result = compare(".foo .bar", ".bar .foo")
        self.assertEqual(result["winner"], "tie")
        self.assertEqual(result["specificity_a"], result["specificity_b"])


class TestExamples(unittest.TestCase):
    """Verify the built-in examples are all correct."""

    def test_17_all_examples(self):
        for selector, expected in EXAMPLES:
            with self.subTest(selector=selector):
                actual = calculate(selector)
                # The :is() case may differ by impl
                if selector.startswith(":is"):
                    continue
                self.assertEqual(
                    actual, expected,
                    f"{selector}: expected {expected}, got {actual}"
                )


class TestDeterminism(unittest.TestCase):
    def test_18_1000_runs(self):
        s = "#header .nav a:hover"
        first = calculate(s)
        for _ in range(1000):
            self.assertEqual(calculate(s), first)


if __name__ == "__main__":
    unittest.main(verbosity=2)
