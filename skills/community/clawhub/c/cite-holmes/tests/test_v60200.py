#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.2.0 测试：MCP wheel 完整性（F54）+独立留出评测集（F55）。

F54=v6.1.0 评测实锤修复：mcp/pyproject.toml wheel include 漏七层 ch_*.py
→uvx/pip 独立安装后壳动态加载全部 FileNotFound、MCP 无法启动。三闸=include
⊇ 实际文件（本锁）+sync_engine.sh 清单门+真 wheel venv 安装冒烟（发车前人工）。
F55=回应「内置基准仅公开设计性夹具」评语：examples/holdout_real.json 独立
留出集（16 条，clean 条目真网逐条核验后入集——凭记忆书写的 8 条 DOI 因真网
核验不过被全部剔除），offline capture 100%/false_kill 0% 为可复现登记口径。
全部 sealed（offline/tmpdir，零网络）。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(SK, "scripts"))


class F54_WheelManifest(unittest.TestCase):
    def test_include_superset_of_actual_files(self):
        # 机制锁：pyproject wheel include ⊇ mcp/ 全部 py 文件
        import tomllib
        d = tomllib.load(open(os.path.join(SK, "mcp", "pyproject.toml"), "rb"))
        inc = set(d["tool"]["hatch"]["build"]["targets"]["wheel"]["include"])
        actual = {fn for fn in os.listdir(os.path.join(SK, "mcp"))
                  if fn.endswith(".py")}
        missing = actual - inc
        self.assertFalse(missing,
                         f"wheel include 缺 {sorted(missing)}——uvx/pip 独立"
                         "安装将崩（F54 教训：新模块必须同步清单）")

    def test_seven_layers_in_include(self):
        import tomllib
        d = tomllib.load(open(os.path.join(SK, "mcp", "pyproject.toml"), "rb"))
        inc = set(d["tool"]["hatch"]["build"]["targets"]["wheel"]["include"])
        for layer in ("ch_text", "ch_netio", "ch_registry", "ch_semantic",
                      "ch_verify", "ch_reports", "ch_cli"):
            self.assertIn(f"{layer}.py", inc)

    def test_holdout_ships_in_examples(self):
        self.assertTrue(os.path.isfile(
            os.path.join(SK, "examples", "holdout_real.json")))


class F55_HoldoutSet(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.load(open(os.path.join(SK, "examples",
                                              "holdout_real.json"),
                                 encoding="utf-8"))
        cls.expected = {int(k): v for k, v in cls.doc["expected"].items()}

    def test_planted_notes_cover_expected(self):
        notes = {int(k) for k in (self.doc.get("planted_notes") or {})}
        planted = {i for i, v in self.expected.items() if v == "planted"}
        self.assertEqual(notes, planted,
                         "每个预埋条目必须有形态说明（公开可查）")

    def test_offline_capture_100_no_false_kill(self):
        # 可复现登记口径（benchmark.md 独立留出集节）：offline 真跑
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "holdout.md")
            rc = subprocess.run(
                [sys.executable,
                 os.path.join(SK, "tools", "run_eval.py"),
                 "--refs", os.path.join(SK, "examples", "holdout_real.json"),
                 "--json-out", os.path.join(td, "h.json"),
                 "--md-out", os.path.join(td, "h.md")],
                capture_output=True, text=True, timeout=300)
            self.assertEqual(rc.returncode, 0, rc.stderr[-300:])
            m = json.load(open(os.path.join(td, "h.json"), encoding="utf-8"))
        self.assertEqual(m["capture_rate"], 1.0,
                         "预埋伪造全部非 verified（capture 100%）")
        self.assertEqual(m["false_kill_rate"], 0.0,
                         "clean 条目零误杀（真实数据铁律的判定面体现）")
        # v6.5.0 F57 准入判据③：条数断言动态化（留出集扩容 16→36 不破锁）
        self.assertEqual(m["n"], len(self.doc["refs"]))
        self.assertGreaterEqual(m["n"], 16, "留出集规模不得缩水")

    def test_clean_entries_carry_verifiable_ids(self):
        # clean 条目必须带可核验标识符或可达 URL（真实数据铁律的静态面）
        for i, r in enumerate(self.doc["refs"], 1):
            if self.expected[i] == "clean":
                has_id = any(str(r.get(k) or "").strip()
                             for k in ("doi", "pmid", "arxiv", "url"))
                self.assertTrue(has_id, f"clean #{i} 无可核验标识符")
                if r.get("doi"):
                    self.assertTrue(r["doi"].startswith("10."),
                                    f"clean #{i} DOI 前缀异常")

    def test_benchmark_registers_holdout(self):
        bm = open(os.path.join(SK, "docs", "benchmark.md"),
                  encoding="utf-8").read()
        self.assertIn("holdout_real.json", bm)
        self.assertIn("独立留出集", bm)
        self.assertIn("真实数据铁律", bm)


if __name__ == "__main__":
    unittest.main()
