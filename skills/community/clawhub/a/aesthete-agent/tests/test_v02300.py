# -*- coding: utf-8 -*-
"""0.23.0 回归:发布闸(release_check C1-C5)。"""
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RC = os.path.join(ROOT, "scripts", "release_check.py")


class TestReleaseCheck(unittest.TestCase):
    """发布闸:在开发树上一键 PASS(0.18-0.20 SH 三版静默失败的机制化防线)。"""

    def test_release_check_pass(self):
        if os.environ.get("AESTHETE_RC_CHILD"):
            self.skipTest("release_check 子进程内,防递归套娃")
        r = subprocess.run([sys.executable, RC], capture_output=True, text=True,
                           timeout=600, cwd=ROOT, env=dict(os.environ, AESTHETE_RC_CHILD="1"))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("裁决: PASS", r.stdout)

    def test_sh_collector_guard(self):
        """SH 收集器必须保留 woff2 排除(防回归)。"""
        sh = os.environ.get("AESTHETE_SH_RELEASE",
                            r"C:\Users\SeALove\ZCodeProject\aesthete-work\_sh_release_local.py")
        src = None
        for cand in (sh, os.path.expanduser("~/release_tools/aesthete_sh_release.py")):
            try:
                src = open(cand, encoding="utf-8").read()
                break
            except OSError:
                continue
        if src is None:
            self.skipTest("本机无 SH 收集器副本(82 发布环境专测)")
        self.assertIn('".woff2"', src)

    def test_c5_semantics(self):
        """C5 只查未排除的字体扩展(woff2 已被收集器排除不算)。"""
        src = open(RC, encoding="utf-8").read()
        self.assertIn('".ttf", ".otf"', src)  # C5 黑名单=收集器未排的字体扩展
        self.assertIn('".woff2"', src)  # C5 校验 SH 收集器保留 woff2 排除
        self.assertIn("woff2", src)  # 收集器校验引用


if __name__ == "__main__":
    unittest.main()
