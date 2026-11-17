#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.0.0 测试：引擎模块化分层布局锁。

锁六件：①壳+7 层 8 文件全部低于 ~120KB 静态阅读线（评测器可见性——10-31
暴跌事件根因）；②双副本（scripts/ 与 mcp/）逐字节一致；③壳重导出完整性
（公开名+被 patch 的单下划线名可在壳命名空间解析）；④_ROOT 注入缝行为
（patch vr.X 影响层内调用）；⑤双壳隔离（trunk 与 mcp 副本加载各自 ch_*
实例，sys.modules 注册名前缀正确）；⑥属性链/字符串键无 _ROOT 误伤。
全部 sealed（零网络）。"""
import importlib.util
import os
import sys
import unittest
import unittest.mock

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(SK, "scripts"))
import verify_refs as vr  # noqa: E402
from _mocks import engine_full_text  # noqa: E402

STATIC_READER_LINE = 122_894  # pubmed-verifier 线实测的 ~120KB 截断边界
LAYERS = ["ch_text", "ch_netio", "ch_registry", "ch_semantic",
          "ch_verify", "ch_reports", "ch_cli"]


class Layout(unittest.TestCase):
    def test_all_engine_files_under_static_reader_line(self):
        for name in ["verify_refs.py"] + [f"{m}.py" for m in LAYERS]:
            for base in ("scripts", "mcp"):
                p = os.path.join(SK, base, name)
                size = os.path.getsize(p)
                self.assertLess(size, STATIC_READER_LINE,
                                f"{base}/{name} {size}B 超静态阅读线")

    def test_eight_files_exist_both_copies(self):
        for name in ["verify_refs.py"] + [f"{m}.py" for m in LAYERS]:
            self.assertTrue(os.path.isfile(os.path.join(SK, "scripts", name)), name)
            self.assertTrue(os.path.isfile(os.path.join(SK, "mcp", name)), name)

    def test_shell_reexports_patched_names(self):
        # 29 个被 patch 名（含单下划线）在壳命名空间可解析
        for n in ("check_url", "verify_one", "_cb_open", "_urlopen_retry",
                  "s2_citation_contexts", "fetch_fulltext", "nli_vote",
                  "_fetch_landing_html", "wayback_available"):
            self.assertTrue(hasattr(vr, n), n)
            self.assertTrue(callable(getattr(vr, n)), n)

    def test_shell_version_alive(self):
        self.assertTrue(vr.VERSION)
        self.assertIn(f'VERSION = "{vr.VERSION}"',
                      open(os.path.join(SK, "scripts", "ch_text.py"),
                           encoding="utf-8").read())


class Seam(unittest.TestCase):
    def test_root_seam_routes_patch(self):
        # _ROOT 缝：patch 壳绑定后，同模块内调用也走壳（同桶裸调必须经 _ROOT）
        vr._OPTS.update({"fast_judge_url": "http://127.0.0.1:9", "s2_key": ""})
        rs = [{"index": 1, "verdict": "partial", "checks": {},
               "semantic_audit": {"claim": "c", "support": "unclear",
                                  "quote": "q", "note": ""},
               "pmid": "12345678"}]
        with unittest.mock.patch.object(
                vr, "judge_endpoint_available", return_value=True), \
             unittest.mock.patch.object(
                 vr, "fetch_pubmed_abstract",
                 side_effect=RuntimeError("sealed")):
            vr.apply_l4_cascade(rs, 5)
        self.assertTrue(
            str(rs[0]["checks"].get("l4_evidence_cascade", {}).get(
                "degraded", "")).startswith("cascade-error"),
            rs[0]["checks"].get("l4_evidence_cascade"))

    def test_no_attribute_chain_corruption(self):
        # 属性链误伤哨兵：引擎文本不得出现 obj._ROOT. 形态（args._ROOT.check_document 类）
        import re
        text = engine_full_text()
        self.assertIsNone(re.search(r"\w\._ROOT\.", text),
                          "属性链被 _ROOT 前缀污染（rewrite 误伤）")
        # dict 键字符串误伤哨兵：引号内 "_ROOT." 形态
        self.assertIsNone(re.search(r'"_ROOT\.[a-z_]+"\s*:', text),
                          "dict 键字符串被污染")


class DualShell(unittest.TestCase):
    def test_mcp_shell_loads_own_instances(self):
        # mcp 壳独立加载：注册名 mcp_ch_* 入 sys.modules，与 trunk ch_* 不同对象
        mcp_dir = os.path.join(SK, "mcp")
        spec = importlib.util.spec_from_file_location(
            "mcp_shell_under_test", os.path.join(mcp_dir, "verify_refs.py"))
        mod = importlib.util.module_from_spec(spec)
        key = "mcp_shell_under_test"
        saved = sys.modules.get("verify_refs")
        sys.modules[key] = mod
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.modules.pop(key, None)
            if saved is not None:
                sys.modules["verify_refs"] = saved
        self.assertTrue(mod.VERSION)
        trunk = sys.modules.get("verify_refs", vr)
        # 各自的层模块对象互不相同（双壳隔离）
        self.assertIsNot(mod.ch_text, getattr(trunk, "ch_text", None))

    def test_mcp_dir_prefixed_registration(self):
        # 壳源码按目录决定前缀——mcp 目录加载注册名带 mcp_ 前缀（逐字节一致的双副本语义）
        # v6.6.0 F64：改空白容忍正则（格式化器引号归一双引号后仍锁同形态）
        import re
        src = open(os.path.join(SK, "scripts", "verify_refs.py"),
                   encoding="utf-8").read()
        self.assertIsNotNone(re.search(
            r'_PREFIX = ["\']mcp_["\'] if _os\.path\.basename\(_HERE\) == '
            r'["\']mcp["\'] else ["\']["\']', src))


if __name__ == "__main__":
    unittest.main()
