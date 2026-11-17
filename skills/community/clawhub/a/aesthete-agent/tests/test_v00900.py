# -*- coding: utf-8 -*-
"""0.9.0 回归:tokens 令牌表 + audit 外部页面审计。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import token_sheet  # noqa: E402
import page_audit  # noqa: E402
import scaffold_kit  # noqa: E402

DP = ["01161E", "124559", "598392", "AEC3B0", "EFF6E0"]  # Deep Pine(用户点名板)


class TestTokensSheet(unittest.TestCase):
    """tokens 命令:角色派生+调墨+双 token 分离+指纹确定性。"""

    def test_roles_and_contrast(self):
        t, ratios, problems = token_sheet.build_tokens(DP, "Deep Pine")
        self.assertEqual(problems, [])
        self.assertGreaterEqual(ratios["ink/bg"], 4.5)
        self.assertGreaterEqual(ratios["on_night/night"], 4.5)
        self.assertGreaterEqual(ratios["on_night_muted/night"], 4.5)
        self.assertGreaterEqual(ratios["accent_ink/bg"], 4.5)
        # accent 图形/文字双 token 分离:文字档必须 ≥ 图形档
        self.assertGreaterEqual(ratios["accent_ink/bg"], ratios["accent/bg(图形≥3)"])

    def test_dark_flip(self):
        t, ratios, problems = token_sheet.build_tokens(DP, "Deep Pine", dark=True)
        self.assertEqual(problems, [])
        self.assertEqual(t["bg"], t["night"])

    def test_emit_files_and_fingerprint(self):
        with tempfile.TemporaryDirectory() as td:
            base = os.path.join(td, "tokens")
            p1, rc = token_sheet.emit(DP, "Deep Pine", out_base=base)
            p2, _ = token_sheet.emit(DP, "Deep Pine", out_base=base)
            self.assertEqual(rc, 0)
            with open(base + ".css", encoding="utf-8") as f:
                css = f.read()
            for k in ("--ink-muted:", "--accent-ink:", "--on-night:", "--s1:", "--r-md:", "--dur-2:"):
                self.assertIn(k, css)
            self.assertEqual(p1["fingerprint"], p2["fingerprint"])
            with open(base + ".json", encoding="utf-8") as f:
                j = json.load(f)
            self.assertEqual(j["verdict"], "PASS")
            self.assertEqual(len(j["fingerprint"]), 64)

    def test_tune_rescues_weak_ink(self):
        # 全浅色板:最深色也不够当主字 → 调墨后必须达标
        weak = ["EFF6E0", "DDE8C9", "AEC3B0", "89B0AE", "8A9BA5"]
        t, ratios, problems = token_sheet.build_tokens(weak, "pale-weak")
        self.assertGreaterEqual(ratios["ink/bg"], 4.5)
        self.assertNotEqual(t["ink"], "8A9BA5")


class TestAuditPage(unittest.TestCase):
    """audit 命令:坏页全指标命中/好页 PASS/修复值真实达标。"""

    BAD = ("<!doctype html><html><head><style>"
           "body{background:#8B5CF6;color:#DDD6FE}"
           "h1{background:linear-gradient(90deg,#8B5CF6,#C084FC);font-family:Inter,sans-serif}"
           ".card{backdrop-filter:blur(12px);font-size:9px;border-radius:36px}"
           ".chip{border-radius:32px}.pill{border-radius:36px}.blob{border-radius:44px}.ico::after{content:'🚀'}"
           "</style></head><body><h1>Hero 🚀</h1><div class='card'>x</div></body></html>")

    def _write(self, td, name, text):
        p = os.path.join(td, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return p

    def test_bad_page_fail(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "bad.html", self.BAD)
            payload = page_audit.run(p, DP)
            self.assertEqual(payload["verdict"], "FAIL")
            checks = {f["check"] for f in payload["findings"]}
            for c in ("gradient", "purple_background", "glassmorphism",
                      "font_floor", "emoji", "default_font", "radius_inflation"):
                self.assertIn(c, checks)
            self.assertEqual(payload["counts"]["P0"], 1)

    def test_good_page_pass(self):
        tokens = scaffold_kit.derive({"hexes": DP}, "夜松", "Night Pine", "")
        good = scaffold_kit.build(tokens)
        with tempfile.TemporaryDirectory() as td:
            p = self._write(td, "good.html", good)
            declared = tokens["PALETTE_DECL"].split(",")
            payload = page_audit.run(p, declared)
            self.assertEqual(payload["verdict"], "PASS", json.dumps(payload["findings"], ensure_ascii=False))
            self.assertEqual(payload["counts"]["P0"], 0)
            self.assertEqual(payload["counts"]["P1"], 0)

    def test_fix_values_actually_pass(self):
        # 修复值必须真达标:对可达对给出达标色;对不可达对如实说"换底色"
        rep, dE = page_audit.nearest("7C5CFF", DP)
        self.assertEqual(rep, "124559")
        self.assertGreater(dE, 0)
        fixed, r = page_audit.fix_contrast("DDD6FE", "01161E", 4.5)
        self.assertGreaterEqual(r, 4.5)
        fixed2, r2 = page_audit.fix_contrast("B9A8FF", "7C5CFF", 4.5)
        self.assertTrue(r2 >= 4.5 or fixed2 == "B9A8FF")  # 白方向不可达时如实返回原色

    def test_normalize_formats(self):
        for tok in ("#abc", "rgb(124, 92, 255)", "hsl(258, 90%, 66%)", "oklch(0.55 0.15 290)"):
            h = page_audit.normalize(tok)
            self.assertTrue(h and len(h) == 6 and all(c in "0123456789ABCDEF" for c in h), tok)


class TestCliEndToEnd(unittest.TestCase):
    """CLI 端到端:tokens 出文件 exit 0;audit 坏页 exit 1。"""

    def test_tokens_cli(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        with tempfile.TemporaryDirectory() as td:
            r = subprocess.run(
                [sys.executable, engine, "tokens", "--palette", ",".join(DP),
                 "--name", "Deep Pine", "--out", os.path.join(td, "t")],
                capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.exists(os.path.join(td, "t.css")))
            self.assertTrue(os.path.exists(os.path.join(td, "t.json")))

    def test_audit_cli_exitcodes(self):
        engine = os.path.join(ROOT, "scripts", "palette_forge.py")
        with tempfile.TemporaryDirectory() as td:
            bad = self._write(td, "bad.html", TestAuditPage.BAD)
            r = subprocess.run(
                [sys.executable, engine, "audit", bad, "--palette", ",".join(DP)],
                capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 1)
            self.assertIn("FAIL", r.stdout)

    def _write(self, td, name, text):
        p = os.path.join(td, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return p


if __name__ == "__main__":
    unittest.main()
