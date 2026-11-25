# -*- coding: utf-8 -*-
"""test_v02400 — 0.24.0 回归:闸门有牙。

AE-N2  rc 口径改严(单条 P1 即红,--lenient 过渡) / AE-B 取板阶梯(--palette 可选+
       meta 板声明+三闸近中性判据+板外 >=2 种 P0、1 种 P1) / AE-FONT-UP 字号令牌
       唯一真源(type_tokens,产物 ≥12px,负例真 raise) / AE-FONTGHOST 幽灵规则
       静态降级 P2+覆盖面 / AE-SCAFFOLD-LEAK 雾色令牌化(MIST_RGB)+scaffold 板声明
       meta 注入 / AE-N3 剂量闸 SKIP/MEASURED 显式化+[1:] 漏判删除。
全部零浏览器;引擎产物用 subprocess 实跑。"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SCRIPTS = os.path.join(ROOT, "scripts")
LP = os.path.join(SCRIPTS, "lint_page.py")
ENGINE = os.path.join(SCRIPTS, "palette_forge.py")
TMP = tempfile.mkdtemp(prefix="t240_")
BOARD = "EFF6E0,E0E6D3,01161E,2E7D5B"
META = '<meta name="aesthete-palette" content="%s">' % BOARD


def w(name, body):
    p = os.path.join(TMP, name)
    io.open(p, "w", encoding="utf-8").write(body)
    return p


def run(args, **kw):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def lint(page, *extra):
    return run([LP, page] + list(extra))


class TestStrictRC(unittest.TestCase):
    """AE-N2:退出码是闸的牙 —— 单条 P1 即红;--lenient 过渡口径保留。"""

    def setUp(self):
        self.p1 = w("p1.html",
                    "<html><head>%s<style>body{background:#EFF6E0}"
                    ".a{color:#C1443A;font-size:13px}</style></head>"
                    "<body><div class=a>私货色一条,字号合规</div></body></html>" % META)

    def test_single_p1_red_by_default(self):
        r = lint(self.p1)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("[P1] 色板漂移[1 种板外非近中性色,P1]", r.stdout)
        self.assertIn("P1=1", r.stdout)

    def test_single_p1_green_under_lenient(self):
        r = lint(self.p1, "--lenient")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("P1=1", r.stdout)  # 仍点名,只是不计入执法

    def test_p2_only_green(self):
        p = w("p2.html",
              "<html><head>%s<style>body{background:#EFF6E0;color:#01161E;font-size:13px}</style></head>"
              "<body><p>\U0001F680 emoji 一条</p></body></html>" % META)
        r = lint(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("P2=1", r.stdout)

    def test_clean_green(self):
        p = w("clean.html",
              "<html><head>%s<style>body{background:#EFF6E0;color:#01161E}"
              "p{font-size:13px}</style></head><body><p>t</p></body></html>" % META)
        r = lint(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("[OK]", r.stdout)


class TestBoardSources(unittest.TestCase):
    """AE-B:--palette 可选+meta 板声明+三闸判据;板外 >=2 种 P0、1 种 P1。"""

    def test_meta_fuzzy_tolerance(self):
        p = w("fz.html",
              '<html><head><meta content="eff6e0, abc, 01161e;" name="AESTHETE-PALETTE">'
              '<style>body{background:#EFF6E0}</style></head><body>t</body></html>')
        r = lint(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("声明板来源=meta,共 3 色", r.stdout)

    def test_no_board_is_p1_skip(self):
        p = w("nob.html",
              "<html><head><style>body{background:#FAF9F9;color:#1E293B}"
              "p{font-size:13px}</style></head><body><p>t</p></body></html>")
        r = lint(p)
        self.assertEqual(r.returncode, 1, r.stdout)  # 默认严:声明板未知=P1=红
        self.assertIn("色板漂移闸跳过", r.stdout)

    def test_two_kinds_off_board_p0(self):
        p = w("two.html",
              "<html><head>%s<style>body{background:#EFF6E0}.a{color:#C1443A}"
              ".b{color:#D97706}</style></head><body><p class=a>x</p><p class=b>y</p></body></html>" % META)
        r = lint(p)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("[P0] 色板漂移[2 种", r.stdout)

    def test_one_kind_is_p1_not_p2(self):
        """AE-N2 裁决:默认严后 P2 永不进 rc=私货色后门,单种板外升 P1。"""
        p = w("one.html",
              "<html><head>%s<style>body{background:#EFF6E0}"
              ".a{color:#C1443A;font-size:13px}</style></head>"
              "<body><div class=a>x</div></body></html>" % META)
        r = lint(p)
        self.assertIn("[P1] 色板漂移[1 种", r.stdout)
        self.assertNotIn("[P2] 色板漂移", r.stdout)

    def test_oklab_matches_engine(self):
        """判据不许有两套实现:lint_page.oklab_lc 与引擎 oklch_from_hex 的 C* 对齐 1e-6。"""
        sys.path.insert(0, SCRIPTS)
        import lint_page as L
        import palette_forge as pf
        worst = 0.0
        for hx in ("124559", "123456", "ABCDEF", "0F766E", "9FB3BC", "7F8C8C"):
            v = [int(hx[i:i + 2], 16) for i in (0, 2, 4)]
            worst = max(worst, abs(L.oklab_lc(*v)[1] - pf.oklch_from_hex("#" + hx)[1]))
        self.assertLessEqual(worst, 1e-6)

    def test_criteria_table(self):
        sys.path.insert(0, SCRIPTS)
        import lint_page as L
        table = [("1E2028", False), ("1B2233", True), ("FAF3DD", True), ("000000", False),
                 ("FFFFFF", False), ("7F8C8C", True), ("9FB3BC", True), ("E8EEF6", False),
                 ("23272E", False), ("526871", True)]
        for hx, want in table:
            self.assertEqual(L.hex_chromatic(hx), want, hx)


class TestFontGhost(unittest.TestCase):
    """AE-FONTGHOST:静态闸只对真会渲染的声明执法;幽灵规则降级 P2+打印覆盖面。"""

    GHOST_CSS = "body{background:#EFF6E0}.wall .w-kick{font:700 8.5px system-ui}.a{color:#01161E;font-size:14px}"

    def test_ghost_downgraded_to_p2(self):
        p = w("ghost.html",
              "<html><head>%s<style>%s</style></head><body><p class=a>t</p></body></html>"
              % (META, self.GHOST_CSS))
        r = lint(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("[P2] 幽灵规则字号低于下限", r.stdout)
        self.assertIn("其中 1 条所在规则未命中本页 DOM", r.stdout)

    def test_hit_selector_stays_p1(self):
        p = w("hit.html",
              "<html><head>%s<style>%s</style></head><body><div class=wall>"
              "<span class=w-kick>t</span></div><p class=a>t</p></body></html>"
              % (META, self.GHOST_CSS))
        r = lint(p)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("[P1] 字号低于下限", r.stdout)

    def test_media_inner_conservative_used(self):
        p = w("media.html",
              "<html><head>%s<style>body{background:#EFF6E0}"
              "@media (max-width:600px){.a{font-size:9px}}</style></head>"
              "<body><p class=a>t</p></body></html>" % META)
        r = lint(p)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("[P1] 字号低于下限", r.stdout)

    def test_type_tokens_negative_raises(self):
        sys.path.insert(0, SCRIPTS)
        import type_tokens as t
        t.assert_floor()                     # 正例:默认档位全 >=12px
        with self.assertRaises(ValueError):
            t.assert_floor({"__FS_MICRO__": "11px"})
        filled = t.fill("font-size:__FS_SMALL__;padding:2px")
        self.assertIn("12.5px", filled)
        self.assertNotIn("__FS_", filled)


class TestScaffoldLeak(unittest.TestCase):
    """AE-SCAFFOLD-LEAK:雾色令牌化(MIST_RGB)+板声明 meta 注入,产物默认 lint 过闸。"""

    def test_darkfour_product_clean(self):
        out = os.path.join(TMP, "d4.html")
        r = run([ENGINE, "scaffold", "--theme", "Deep Pine", "--recipe", "DARK-FOUR-ACT",
                 "--brand", "回归自证", "--out", out])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        html = io.open(out, encoding="utf-8").read()
        self.assertIn("aesthete-palette", html)          # 板声明 meta 已注入
        self.assertNotIn("@MIST_RGB@", html)             # 雾色令牌已填
        self.assertNotIn("rgba(159,179,188", html)       # 跨主题写死雾色已废
        pal = re.search(r"主题色板\(声明\): ([0-9A-F,]+)", r.stdout).group(1)
        lint_r = run([LP, out, "--palette", pal])
        self.assertEqual(lint_r.returncode, 0, lint_r.stdout)
        # meta 取板(缺省 --palette)同样过闸 —— AE-B 取板阶梯闭环
        lint_meta = run([LP, out])
        self.assertEqual(lint_meta.returncode, 0, lint_meta.stdout)
        self.assertIn("声明板来源=meta", lint_meta.stdout)

    def test_products_min_font_floor(self):
        """AE-FONT-UP:引擎产物里不许再有 <12px 字号声明(静态扫描口径)。"""
        numdecl = re.compile(r"font(?:-size)?\s*:\s*(?:[^;\"'{}\n]*?\s)?(\d+(?:\.\d+)?)px")
        pal = "01161E,EFF6E0,124559,AEC3B0,52636E"
        for tag, args in (("scene-wallet", ["scene", "--kind", "wallet", "--palette", pal]),
                          ("scaffold-auto", ["scaffold", "--palette", pal, "--brand", "自证"])):
            out = os.path.join(TMP, "fp_%s.html" % tag)
            r = run([ENGINE] + args + ["--out", out])
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            html = io.open(out, encoding="utf-8").read()
            bad = sorted({m for m in (float(x) for x in numdecl.findall(html)) if m < 12})
            self.assertEqual(bad, [], "%s 仍有 <12px 字号 %s" % (tag, bad))


class TestDosageGate(unittest.TestCase):
    """AE-N3:剂量维度缺失绝不静默;[1:] 漏判删除;SUMMARY 带覆盖面。"""

    @staticmethod
    def _ev(colors):
        p = os.path.join(TMP, "ev.json")
        io.open(p, "w", encoding="utf-8").write(json.dumps(
            {"url": "x", "theme": "light", "bodyBg": "#FFFFFF",
             "minFont": 13, "colors": colors, "worstPairs": [], "zones": []}))
        return p

    def test_skip_is_explicit(self):
        p = w("plain.html",
              "<html><head>%s<style>body{background:#EFF6E0;color:#01161E}"
              "p{font-size:13px}</style></head><body><p>t</p></body></html>" % META)
        r = lint(p)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("[SKIP] 剂量闸 SKIP", r.stdout)
        self.assertIn("剂量闸=SKIP", r.stdout)

    def test_measured_summary_coverage(self):
        page = w("m.html",
                 "<html><head>%s<style>body{background:#EFF6E0;color:#01161E}"
                 "p{font-size:13px}</style></head><body><p>t</p></body></html>" % META)
        r = lint(page, "--render", self._ev([{"hex": "2E7D5B", "areaRatio": 0.05}]))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("剂量闸=MEASURED(扫描 1 色)", r.stdout)

    def test_first_color_not_dropped(self):
        """AE-N3b:旧 `[1:]` 无条件砍掉首位 —— accent 85.5% 大底在 MEASURED 徽章下漏判。"""
        page = w("loud.html",
                 "<html><head>%s<style>body{background:#EFF6E0;color:#01161E}"
                 "p{font-size:13px}</style></head><body><p>t</p></body></html>" % META)
        ev = self._ev([{"hex": "C1443A", "areaRatio": 0.855},
                       {"hex": "FFFFFF", "areaRatio": 0.10}])
        r = lint(page, "--render", ev)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("剂量失控(渲染实测)", r.stdout)
        self.assertIn("#C1443A 占 86%", r.stdout)


class TestAuditFamilyStrict(unittest.TestCase):
    """AE-N2 同族:page_audit 单条 P1 即 FAIL(verdict 与退出码)。"""

    def test_audit_single_p1_fails(self):
        sys.path.insert(0, SCRIPTS)
        import page_audit
        p = w("aud.html",
              "<html><head><style>body{background:#FAF9F9;font-family:system-ui}"
              ".card{background:#FFFFFF;color:#C1443A;font-size:15px;padding:18px}</style></head>"
              "<body><div class='card'><p>板外强调色一条,其余合规</p></div></body></html>")
        payload = page_audit.run(p, ["FAF9F9", "FFFFFF", "555B6E"], floor=12, out_base=None)
        self.assertEqual(payload["verdict"], "FAIL", payload["findings"])
        self.assertEqual(payload["counts"]["P1"], 1)

    def test_audit_clean_passes(self):
        sys.path.insert(0, SCRIPTS)
        import page_audit
        p = w("aud_ok.html",
              "<html><head><style>body{background:#FAF9F9;font-family:system-ui}"
              ".card{background:#FFFFFF;color:#555B6E;font-size:15px;padding:18px}</style></head>"
              "<body><div class='card'><p>全板内</p></div></body></html>")
        payload = page_audit.run(p, ["FAF9F9", "FFFFFF", "555B6E"], floor=12, out_base=None)
        self.assertEqual(payload["verdict"], "PASS", payload["findings"])


if __name__ == "__main__":
    unittest.main()
