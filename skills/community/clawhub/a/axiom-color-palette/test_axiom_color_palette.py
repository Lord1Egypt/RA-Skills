"""Tests — axiom-color-palette """

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).parent))

from axiom_color_palette import (
    HARMONIES,
    adjust_lightness,
    analogous,
    complementary,
    generate,
    hsl,
    monochromatic,
    parse_hex,
    rotate_hue,
    tetradic,
    to_hex,
    to_hsl_string,
    to_rgb_string,
    triadic,
)


class TestParseHex(unittest.TestCase):
    def test_01_6char(self):
        self.assertEqual(parse_hex("#FF5500"), (255, 85, 0))

    def test_02_no_hash(self):
        self.assertEqual(parse_hex("FF5500"), (255, 85, 0))

    def test_03_3char(self):
        self.assertEqual(parse_hex("#F50"), (255, 85, 0))

    def test_04_lowercase(self):
        self.assertEqual(parse_hex("#abcdef"), (171, 205, 239))

    def test_05_invalid(self):
        with self.assertRaises(ValueError):
            parse_hex("#GGGGGG")

    def test_06_wrong_length(self):
        with self.assertRaises(ValueError):
            parse_hex("#12345")


class TestToHex(unittest.TestCase):
    def test_07_basic(self):
        self.assertEqual(to_hex((255, 85, 0)), "#FF5500")


class TestHsl(unittest.TestCase):
    def test_08_pure_red(self):
        h, s, l = hsl((255, 0, 0))
        self.assertEqual(h, 0)

    def test_09_white(self):
        h, s, l = hsl((255, 255, 255))
        self.assertEqual(s, 0)
        self.assertEqual(l, 100)


class TestRotateHue(unittest.TestCase):
    def test_10_180(self):
        # Red → Cyan
        self.assertEqual(rotate_hue((255, 0, 0), 180), (0, 255, 255))

    def test_11_120(self):
        # Red → Green
        result = rotate_hue((255, 0, 0), 120)
        self.assertEqual(result, (0, 255, 0))


class TestHarmonies(unittest.TestCase):
    def test_12_complementary(self):
        result = complementary((255, 0, 0))
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (255, 0, 0))
        self.assertEqual(result[1], (0, 255, 255))

    def test_13_analogous(self):
        result = analogous((255, 0, 0))
        self.assertEqual(len(result), 3)

    def test_14_triadic(self):
        result = triadic((255, 0, 0))
        self.assertEqual(len(result), 3)

    def test_15_tetradic(self):
        result = tetradic((255, 0, 0))
        self.assertEqual(len(result), 4)

    def test_16_monochromatic(self):
        result = monochromatic((128, 128, 128), count=5)
        self.assertEqual(len(result), 5)


class TestGenerate(unittest.TestCase):
    def test_17_generate(self):
        result = generate("#FF5500", "complementary")
        self.assertEqual(result["base"], "#FF5500")
        self.assertEqual(len(result["palette"]), 2)

    def test_18_unknown_harmony(self):
        with self.assertRaises(ValueError):
            generate("#FF5500", "unknown")


class TestDeterminism(unittest.TestCase):
    def test_19_1000_runs(self):
        for _ in range(1000):
            self.assertEqual(generate("#FF5500", "triadic")["base"], "#FF5500")


if __name__ == "__main__":
    unittest.main(verbosity=2)
