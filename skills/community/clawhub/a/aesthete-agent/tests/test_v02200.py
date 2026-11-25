# -*- coding: utf-8 -*-
"""0.22.0 回归:渲染事实(probe v2 zones/direct --render/lint 分区复验)。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

ENGINE = os.path.join(ROOT, "scripts", "palette_forge.py")


def _ev(zones):
    return {"url": "demo", "bodyBg": zones[0]["hex"], "theme": "light",
            "zones": zones, "colors": [], "minFont": 14, "worstPairs": []}


class TestDirectRender(unittest.TestCase):
    """direct --render:渲染事实审计两案。"""

    def _run(self, zones):
        td = tempfile.mkdtemp()
        p = os.path.join(td, "ev.json")
        json.dump(_ev(zones), open(p, "w", encoding="utf-8"))
        return subprocess.run([sys.executable, ENGINE, "direct", "--render", p],
                              capture_output=True, text=True, timeout=120)

    def test_good_render(self):
        r = self._run([{"hex": "EFF6E0", "share": 0.55}, {"hex": "124559", "share": 0.10},
                       {"hex": "598392", "share": 0.05}, {"hex": "F8FBF1", "share": 0.30}])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("渲染事实审计", r.stdout)

    def test_dirty_render(self):
        r = self._run([{"hex": "D7AF70", "share": 0.40}, {"hex": "FFFFFF", "share": 0.35},
                       {"hex": "333333", "share": 0.25}])
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL", r.stdout)

    def test_missing_zones(self):
        td = tempfile.mkdtemp()
        p = os.path.join(td, "ev.json")
        json.dump({"url": "x", "colors": []}, open(p, "w", encoding="utf-8"))
        r = subprocess.run([sys.executable, ENGINE, "direct", "--render", p],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(r.returncode, 2)
        self.assertIn("zones", r.stderr)


class TestProbeV2(unittest.TestCase):
    """render_probe.js 含 zones 采集与输出。"""

    def test_probe_source(self):
        src = open(os.path.join(ROOT, "scripts", "render_probe.js"), encoding="utf-8").read()
        self.assertIn("zoneAreas", src)
        self.assertIn("zones,", src)
        self.assertIn("class*='hero'", src)


class TestLintZoneCheck(unittest.TestCase):
    """lint_page --render 分区复验(渲染事实脏底)。"""

    def test_zone_muddy(self):
        lp = os.path.join(ROOT, "scripts", "lint_page.py")
        td = tempfile.mkdtemp()
        page = os.path.join(td, "p.html")
        open(page, "w", encoding="utf-8").write(
            '<html lang="zh-CN"><head><style>body{background:#FFFFFF}</style></head><body><p>x</p></body></html>')
        ev = os.path.join(td, "ev.json")
        json.dump(_ev([{"hex": "D7AF70", "share": 0.40}, {"hex": "FFFFFF", "share": 0.35},
                       {"hex": "333333", "share": 0.25}]),
                  open(ev, "w", encoding="utf-8"))
        r = subprocess.run([sys.executable, lp, page,
                            "--palette", "FFFFFF,333333,D7AF70", "--render", ev],
                           capture_output=True, text=True, timeout=120)
        self.assertIn("渲染事实:区块大底 #D7AF70", r.stdout)


if __name__ == "__main__":
    unittest.main()
