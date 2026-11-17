#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.5.0 测试：随包可复验与留出集规模化（F57 随包 sealed 测试子集/
F58 留出集 v2 扩容 36+半自动管线/F59 --held-out 真网闸门/F60 N5 跨库探针）。

四件均系针对前版缺陷与不足的建设性反馈的机制化落地（随包可复验缺口/
评测面规模缺口/跨注册库验证缺口）。全部 sealed（mock/tmpdir，零网络；
真网面由 run_tests.sh --held-out 与 netcheck 在发车链执行）。"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(SK, "scripts"))
import verify_refs as vr  # noqa: E402

LEAK_PATTERNS = ("192." + "168.", "ub" + "sea@", "StrictHost" + "KeyChecking",
                 "归" + "墟", "note_" + "1", "agent" + "ops",
                 "relea" + "se_v", "/ho" + "me/", "82 " + "机")


class F57_ShippedSubset(unittest.TestCase):
    def setUp(self):
        self.mf_path = os.path.join(HERE, "shipped_manifest.json")
        self.mf = json.load(open(self.mf_path, encoding="utf-8"))

    def test_manifest_files_exist_and_clean(self):
        files = self.mf.get("files") or []
        self.assertGreaterEqual(len(files), 8, "随包子集不得缩水")
        for fn in files:
            p = os.path.join(HERE, fn)
            self.assertTrue(os.path.isfile(p), f"清单文件缺失: {fn}")
            text = open(p, encoding="utf-8").read()
            for pat in LEAK_PATTERNS:
                self.assertNotIn(pat, text, f"{fn} 含泄漏模式 {pat}")

    def test_manifest_self_inclusive(self):
        # 清单必须收录本测试（锁自身随包——否则包内丢失本锁无人知）
        self.assertIn("test_v60500.py", self.mf["files"])

    def test_runner_and_selfcheck_wiring(self):
        rt = open(os.path.join(SK, "tools", "run_tests.sh"),
                  encoding="utf-8").read()
        self.assertIn("--shipped", rt)
        self.assertIn("shipped_manifest.json", rt)
        sc = open(os.path.join(SK, "tools", "selfcheck.py"),
                  encoding="utf-8").read()
        self.assertIn("--tests", sc)
        self.assertIn("t_shipped_tests", sc)

    def test_adr_registers_decision(self):
        adr = open(os.path.join(SK, "docs", "adr",
                                "0011-shipped-sealed-test-subset.md"),
                   encoding="utf-8").read()
        self.assertIn("shipped_manifest.json", adr)
        self.assertIn("ADR-0010", adr)


class F58_HoldoutV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.load(open(os.path.join(SK, "examples",
                                              "holdout_real.json"),
                                 encoding="utf-8"))
        cls.expected = {int(k): v for k, v in cls.doc["expected"].items()}

    def test_scale_and_internal_consistency(self):
        # 规模锁：v2 下限（动态化判据③——未来扩容不破锁；内部一致断言防漂移）
        self.assertEqual(len(self.doc["refs"]), len(self.expected))
        self.assertGreaterEqual(len(self.doc["refs"]), 36, "留出集规模不得缩水")
        n_clean = sum(1 for v in self.expected.values() if v == "clean")
        n_planted = sum(1 for v in self.expected.values() if v == "planted")
        self.assertEqual(n_clean + n_planted, len(self.expected))
        self.assertGreaterEqual(n_clean, 21)
        self.assertGreaterEqual(n_planted, 15)

    def test_doi_uniqueness_batch_cache_discipline(self):
        # M5 教训入库为集合纪律：批内 DOI 唯一（CLI 批内缓存按 DOI 复用判定）
        dois = [str(r.get("doi") or "").strip().lower()
                for r in self.doc["refs"]]
        dois = [d for d in dois if d]
        self.assertEqual(len(dois), len(set(dois)), "批内 DOI 冲突")

    def test_domain_diversity(self):
        # 多域覆盖锁：clean 条目 DOI 注册商前缀 ≥8 家（与 benchmark.md 声称同源）
        prefixes = set()
        for i, r in enumerate(self.doc["refs"], 1):
            if self.expected[i] == "clean" and r.get("doi"):
                prefixes.add(r["doi"].split("/")[0].lower())
        self.assertGreaterEqual(len(prefixes), 8, f"注册商前缀仅 {prefixes}")

    def test_static_discipline(self):
        for i, r in enumerate(self.doc["refs"], 1):
            if self.expected[i] == "clean":
                self.assertTrue(
                    any(str(r.get(k) or "").strip()
                        for k in ("doi", "pmid", "arxiv", "url")),
                    f"clean #{i} 无可核验标识符")
        notes = {int(k) for k in self.doc.get("planted_notes") or {}}
        planted = {i for i, v in self.expected.items() if v == "planted"}
        self.assertEqual(notes, planted, "planted_notes 必须全覆盖")

    def test_pipeline_tool_and_benchmark_registration(self):
        src = open(os.path.join(SK, "tools", "build_holdout.py"),
                   encoding="utf-8").read()
        for marker in ("--freeze", "reviewed", "DOI 唯一"):
            self.assertIn(marker, src)
        bm = open(os.path.join(SK, "docs", "benchmark.md"),
                  encoding="utf-8").read()
        self.assertIn("build_holdout.py", bm)
        self.assertIn("36 条", bm)

    def test_pipeline_freeze_requires_reviewed(self):
        # 冻结闸：未拍板（无 reviewed 字段）→ 拦截 rc=2（草案不得直通入集）
        with tempfile.TemporaryDirectory() as td:
            draft = os.path.join(td, "d.json")
            json.dump({"entries": [{"index": 1, "ref": {"title": "t"},
                                    "verdict": "verified", "suggest": "clean"}]},
                      open(draft, "w", encoding="utf-8"))
            r = subprocess.run(
                [sys.executable, os.path.join(SK, "tools", "build_holdout.py"),
                 "--draft", draft, "--freeze", os.path.join(td, "f.json")],
                capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 2, "未拍板草案必须被冻结闸拦截")


class F59_HeldOutGate(unittest.TestCase):
    def test_fidelity_label_parser(self):
        from importlib import util
        spec = util.spec_from_file_location(
            "run_eval_mod", os.path.join(SK, "tools", "run_eval.py"))
        m = util.module_from_spec(spec)
        spec.loader.exec_module(m)
        self.assertEqual(m._FID_TAG.search("[元数据漂移:minor] x").group(1),
                         "minor")
        self.assertEqual(m._FID_TAG.search("[元数据漂移:major] y").group(1),
                         "major")
        self.assertEqual(m._fidelity_label("无标签 note"), "exact")

    def test_gate_check_thresholds(self):
        from importlib import util
        spec = util.spec_from_file_location(
            "run_eval_mod", os.path.join(SK, "tools", "run_eval.py"))
        m = util.module_from_spec(spec)
        spec.loader.exec_module(m)
        self.assertEqual(m.gate_check({"capture_rate": 1.0,
                                       "false_kill_rate": 0.0}), [])
        self.assertEqual(m.gate_check({"capture_rate": 1.0,
                                       "false_kill_rate": 0.0,
                                       "fidelity_hit_rate": 1.0}), [])
        self.assertTrue(m.gate_check({"capture_rate": 0.9,
                                      "false_kill_rate": 0.0}))
        self.assertTrue(m.gate_check({"capture_rate": 1.0,
                                      "false_kill_rate": 0.1}))
        self.assertTrue(m.gate_check({"capture_rate": 1.0,
                                      "false_kill_rate": 0.0,
                                      "fidelity_hit_rate": 0.83}))
        self.assertTrue(m.gate_check({}), "无判据必须 FAIL")
        # 内容绑定（审计 P2）：全批不可达=判据无证据面，闸门拒绝放行
        self.assertTrue(m.gate_check({"capture_rate": 1.0,
                                      "false_kill_rate": 0.0,
                                      "network_liveness": False}),
                        "全批不可达必须拦停（假满防护）")
        self.assertEqual(m.gate_check({"capture_rate": 1.0,
                                       "false_kill_rate": 0.0,
                                       "network_liveness": True}), [])

    def test_fidelity_requires_net(self):
        # 标签产自注册库元数据——offline 必须拒跑（rc=2 用法错）
        r = subprocess.run(
            [sys.executable, os.path.join(SK, "tools", "run_eval.py"),
             "--refs", os.path.join(SK, "examples", "holdout_fidelity.json"),
             "--fidelity", "--json-out", "/tmp/x.json", "--md-out", "/tmp/x.md"],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 2)

    def test_runner_wiring(self):
        rt = open(os.path.join(SK, "tools", "run_tests.sh"),
                  encoding="utf-8").read()
        self.assertIn("--held-out", rt)
        self.assertIn("--gate", rt)
        self.assertIn("holdout_fidelity.json", rt)


class F60_N5CrossRegistry(unittest.TestCase):
    def test_probe_registered_with_honest_skip(self):
        src = open(os.path.join(SK, "tools", "netcheck.py"),
                   encoding="utf-8").read()
        self.assertIn("def n5_cross_registry", src)
        self.assertIn("10.1542/peds.2006-2223", src)   # 真网核验过的锚点 DOI
        self.assertIn("17015575", src)                 # 同源 PMID
        self.assertIn("N5 三库登记题名一致", src)       # main 接线
        self.assertIn("0.85", src)                     # 一致性阈值
        self.assertIn("三库齐才可比", src)              # SKIP 诚实边界
        self.assertIn("api.openalex.org/works/doi:", src)

    def test_two_tier_docs_updated(self):
        vd = open(os.path.join(SK, "references", "verification-details.md"),
                  encoding="utf-8").read()
        self.assertIn("N5", vd)


if __name__ == "__main__":
    unittest.main()
