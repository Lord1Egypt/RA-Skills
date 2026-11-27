# -*- coding: utf-8 -*-
"""test_v03200 — 0.32.0 回归:令牌派生(母变量+暗色别名+OKLCH 伴生)。"""
import io
import os
import re
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SCRIPTS = os.path.join(ROOT, "scripts")
sys.path.insert(0, SCRIPTS)

import token_sheet  # noqa: E402
import type_kit  # noqa: E402

PAL = "01161E,124559,598392,AEC3B0,EFF6E0"
TMP = tempfile.mkdtemp(prefix="t320_")


class TestSpacingDerivation(unittest.TestCase):
    """Tailwind v4 模式:全部间距 = calc(--spacing × 倍数),改一个数全阶联动。"""

    def test_spacing_mother_var(self):
        out = os.path.join(TMP, "sp")
        token_sheet.emit([h.upper() for h in PAL.split(",")], out_base=out)
        css = io.open(out + ".css", encoding="utf-8").read()
        self.assertIn("--spacing:8px;", css)
        self.assertIn("--s1:calc(var(--spacing) * 0.5);", css)
        self.assertIn("--s10:calc(var(--spacing) * 16);", css)
        self.assertNotIn("--s1:4px;", css)               # 旧硬编码已废


class TestFontScale(unittest.TestCase):
    """--font-scale 母变量:全部字阶乘旋钮,1=默认。"""

    def test_typescale_multiplier(self):
        out = os.path.join(TMP, "fs")
        type_kit.emit("回归", out_base=out, fluid=True)
        css = io.open(out + ".css", encoding="utf-8").read()
        self.assertIn("--font-scale:1;", css)
        self.assertIn("calc(16px * var(--font-scale, 1))", css)
        self.assertIn("--text-3xl:calc(clamp(", css)  # clamp 外包 font-scale 母变量

    def test_multiplier_one_is_identity(self):
        """--font-scale=1 时取值=原值(数学恒等,防乘法漂移)。"""
        css_lines = io.open(os.path.join(SCRIPTS, "type_kit.py"),
                            encoding="utf-8").read()
        self.assertIn('var(--font-scale, 1)', css_lines)  # 缺省回退必须是 1


class TestDarkAlias(unittest.TestCase):
    """暗色别名块:六核心面/墨随系统 scheme 换幕。"""

    def test_dark_media_block(self):
        out = os.path.join(TMP, "da")
        token_sheet.emit([h.upper() for h in PAL.split(",")], out_base=out)
        css = io.open(out + ".css", encoding="utf-8").read()
        self.assertIn("@media (prefers-color-scheme: dark){", css)
        m = re.search(r"@media \(prefers-color-scheme: dark\)\{\n:root\{([^}]*)\}", css)
        self.assertIsNotNone(m)
        body = m.group(1)
        for k in ("--bg:", "--bg-raised:", "--ink:", "--ink-muted:", "--line:"):
            self.assertIn(k, body)

    def test_dark_alias_differs_from_light(self):
        out = os.path.join(TMP, "dd")
        payload, rc = token_sheet.emit([h.upper() for h in PAL.split(",")], out_base=out)
        css = io.open(out + ".css", encoding="utf-8").read()
        light_bg = payload["tokens"]["bg"]
        dark_block = re.search(r"@media \(prefers-color-scheme: dark\)\{\n:root\{([^}]*)\}", css).group(1)
        m = re.search(r"--bg:#([0-9A-F]{6})", dark_block)
        self.assertIsNotNone(m)
        self.assertNotEqual(m.group(1), light_bg, "暗幕 --bg 必须不同于浅幕")


class TestOklchCompanions(unittest.TestCase):
    """OKLCH 伴生变量:每步 -ok 后缀,感知空间直接接线。"""

    def test_ok_companions_all_steps(self):
        out = os.path.join(TMP, "ok")
        token_sheet.emit([h.upper() for h in PAL.split(",")], out_base=out)
        css = io.open(out + ".css", encoding="utf-8").read()
        companions = re.findall(r"--step-(\d+)-[\w-]+-ok: oklch\(", css)
        self.assertEqual(len(companions), 12, f"12 步全有伴生,实得 {len(companions)}")


if __name__ == "__main__":
    unittest.main()
