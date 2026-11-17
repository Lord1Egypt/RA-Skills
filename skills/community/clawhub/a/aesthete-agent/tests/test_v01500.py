# -*- coding: utf-8 -*-
"""0.15.0 回归:derive 角色引擎(ink2 霓虹排除/PALE 浅度钳制)+多板矩阵。"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import scaffold_kit  # noqa: E402


def _sat(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    return 0 if mx == mn else (mx - mn) / (2 - mx - mn) if l > 0.5 else (mx - mn) / (mx + mn)


def _neon(h):
    s = _sat(h)
    l = sum(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) / 3
    return s >= 0.60 and l > 0.45


BOARD = {
    "野莓(暖粉)": ["EA526F", "E76B74", "D7AF70", "937D64", "585B56"],
    "夜松(冷深)": ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"],
    "晨柔(暖浅)": ["EA526F", "D7AF70", "937D64", "585B56", "F3E7D4"],
    "靛蓝(冷中)": ["1E293B", "3B82F6", "93C5FD", "DBEAFE", "0F172A"],
    "苔绿(中性)": ["3F4E4F", "A8B5A2", "E8E4D8", "C2B280", "556B2F"],
    "酒红(深暖)": ["5C1A2E", "8B3A52", "D4A5A5", "F2E8E4", "3D1522"],
    "糖果(高饱)": ["FF6B9D", "FFD93D", "6BCB77", "4D96FF", "FF6B6B"],
    "墨黑(极深)": ["111111", "333333", "666666", "999999", "EEEEEE"],
}


class TestDeriveRoles(unittest.TestCase):
    """derive 角色引擎矩阵:每板验证 ink2 非霓虹/PALE 够浅/角色不撞。"""

    def test_matrix(self):
        for name, pal in BOARD.items():
            with self.subTest(board=name):
                tk = scaffold_kit.derive({"hexes": pal}, name, "X", "")
                ink2, pale, night = tk["INK2"], tk["PALE"], tk["NIGHT"]
                self.assertFalse(_neon(ink2),
                                 f"{name}: ink2 #{ink2} 在霓虹区(刺眼)")
                self.assertGreaterEqual(scaffold_kit._lum_lin(pale), 0.75,
                                        f"{name}: PALE #{pale} 不够浅(显脏)")
                self.assertNotEqual(ink2, night, f"{name}: ink2 与 night 同色")

    def test_wildberry_regression(self):
        tk = scaffold_kit.derive({"hexes": BOARD["野莓(暖粉)"]}, "野莓", "WB", "")
        self.assertEqual(tk["INK2"], "937D64", "灰褐回归(非粉)")

    def test_nightpine_regression(self):
        tk = scaffold_kit.derive({"hexes": BOARD["夜松(冷深)"]}, "夜松", "NP", "")
        self.assertEqual(tk["INK2"], "124559", "钢蓝回归")


if __name__ == "__main__":
    unittest.main()
