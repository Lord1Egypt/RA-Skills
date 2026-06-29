"""Tests — axiom-regex-visualizer """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_regex_visualizer import explain, tokenize, visualize


class TestTokenize(unittest.TestCase):
    def test_01_literals(self):
        tokens = tokenize("abc")
        self.assertEqual([(t, v) for t, v in tokens if t == "literal"], [("literal", "a"), ("literal", "b"), ("literal", "c")])

    def test_02_digit(self):
        tokens = tokenize(r"\d")
        self.assertEqual(tokens[0][0], "predefined")

    def test_03_quantifier_star(self):
        tokens = tokenize("a*")
        self.assertEqual(tokens[1][0], "quantifier_star")

    def test_04_quantifier_plus(self):
        tokens = tokenize("a+")
        self.assertEqual(tokens[1][0], "quantifier_plus")

    def test_05_quantifier_question(self):
        tokens = tokenize("a?")
        self.assertEqual(tokens[1][0], "quantifier_question")

    def test_06_quantifier_exact(self):
        tokens = tokenize("a{3}")
        self.assertEqual(tokens[1][0], "quantifier_exact")

    def test_07_quantifier_range(self):
        tokens = tokenize("a{2,5}")
        self.assertEqual(tokens[1][0], "quantifier_range")

    def test_08_group_capture(self):
        tokens = tokenize("(abc)")
        self.assertEqual(tokens[0][0], "group_capture")

    def test_09_group_noncapture(self):
        tokens = tokenize("(?:abc)")
        self.assertEqual(tokens[0][0], "group_noncapture")

    def test_10_anchors(self):
        tokens = tokenize("^abc$")
        self.assertEqual(tokens[0][0], "anchor_start")
        self.assertEqual(tokens[-1][0], "anchor_end")

    def test_11_dot(self):
        tokens = tokenize("a.b")
        self.assertEqual(tokens[1][0], "dot")

    def test_12_alternation(self):
        tokens = tokenize("a|b")
        self.assertIn(("alternation", "| (OR)"), tokens)


class TestVisualize(unittest.TestCase):
    def test_13_email(self):
        out = visualize(r"^[a-z]+@[a-z]+\.[a-z]+$")
        self.assertIn("(start)", out)
        self.assertIn("(end)", out)

    def test_14_doesnt_crash(self):
        # Various complex patterns shouldn't crash
        for pat in [r"\d{3}-\d{4}", r"[A-Z][a-z]+", r"(foo|bar)+", r"^\s*#.*$"]:
            visualize(pat)  # just check no exception


class TestExplain(unittest.TestCase):
    def test_15_simple(self):
        text = explain(r"abc")
        self.assertIn("'a'", text)
        self.assertIn("'b'", text)
        self.assertIn("'c'", text)

    def test_16_quantifier(self):
        text = explain(r"a+")
        self.assertIn("one or more", text)


class TestDeterminism(unittest.TestCase):
    def test_17_1000_runs(self):
        p = r"^[a-z]+@[a-z]+\.[a-z]+$"
        first = tokenize(p)
        for _ in range(1000):
            self.assertEqual(tokenize(p), first)


if __name__ == "__main__":
    unittest.main(verbosity=2)
