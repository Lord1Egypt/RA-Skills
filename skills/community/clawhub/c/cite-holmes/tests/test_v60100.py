#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v6.1.0 测试：投稿前审计包（F51 --check-paper）+随包自检（F52 selfcheck）
+同步锁（F53 MCP 工具枚举）。

F51=--check-paper 一条命令组合（check_document 通路复用+audit-mode+strict+
GB/T/BibTeX 导出强制+INDEX 就绪总览）；submission_readiness 判据与 audit
分级同源；组合旗标不改判定语义。F52=tools/selfcheck.py 随包安装验证。
F53=SKILL 工具枚举与 server.py 实际公开面一致锁（评测「示例与工具数量未
同步」病灶机制化）。全部 sealed（offline/tmpdir 桩，零网络）。"""
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
from _mocks import fresh_engine_state  # noqa: E402


def _row(idx, verdict, **kw):
    r = {"index": idx, "verdict": verdict, "title": f"T{idx}",
         "note": "", "checks": {}}
    r.update(kw)
    return r


class F51_Readiness(unittest.TestCase):
    def test_ready_when_clean(self):
        rs = [_row(1, "verified"), _row(2, "partial")]
        rd = vr.submission_readiness(rs)
        self.assertTrue(rd["ready"])
        self.assertEqual((rd["p0"], rd["p1"]), (0, 0))
        self.assertTrue(rd["todos"])  # partial 进待办不阻断

    def test_not_ready_on_invalid(self):
        rs = [_row(1, "verified"), _row(2, "invalid", error_codes=["E03"])]
        rd = vr.submission_readiness(rs)
        self.assertFalse(rd["ready"])
        self.assertEqual(rd["p0"], 1)
        self.assertTrue(any("P0" in b for b in rd["blockers"]))

    def test_not_ready_on_retracted_and_unreachable(self):
        retr = _row(1, "partial",
                    checks={"retraction": {"retracted": True}})
        unreach = _row(2, "unreachable")
        rd = vr.submission_readiness([retr, unreach])
        self.assertFalse(rd["ready"])
        self.assertEqual(rd["p1"], 2)
        self.assertTrue(any("撤稿" in b for b in rd["blockers"]))
        self.assertTrue(any("不可达" in b for b in rd["blockers"]))

    def test_retracted_invalid_not_double_counted(self):
        # 与 audit 分级同口径：invalid 优先归 P0，不再进 P1（防同条双计）
        rs = [_row(1, "invalid", checks={"retraction": {"retracted": True}})]
        rd = vr.submission_readiness(rs)
        self.assertEqual((rd["p0"], rd["p1"]), (1, 0))

    def test_completeness_todos(self):
        cd = {"n_unbound": 2, "n_uncited": 1, "n_citations": 5,
              "n_low_anchor": 0, "coverage": 0.8, "anchor_threshold": 0.34}
        rd = vr.submission_readiness([_row(1, "verified")], cd)
        self.assertTrue(rd["ready"])
        self.assertTrue(any("未绑定" in t for t in rd["todos"]))
        self.assertTrue(any("未在正文引用" in t or "列而未引" in t
                            for t in rd["todos"]))


class F51_IndexRender(unittest.TestCase):
    def test_ready_index_content(self):
        rs = [_row(1, "verified")]
        sc = vr.compute_scorecard(rs)
        md = vr.build_submission_index(rs, None, sc,
                                       artifacts=["rpt.md", "rpt.bib"])
        self.assertIn("READY", md)
        self.assertIn("这不是学术就绪声明", md)
        self.assertIn("rpt.bib", md)
        self.assertIn("机械层口径", md)

    def test_not_ready_index_blockers(self):
        rs = [_row(1, "invalid"), _row(2, "verified")]
        sc = vr.compute_scorecard(rs)
        md = vr.build_submission_index(rs, None, sc)
        self.assertIn("NOT READY", md)
        self.assertIn("P0 编造嫌疑 1 条", md)

    def test_index_never_invents_verdicts(self):
        # 宪法：INDEX 只装配 results/cd/scorecard——无判定写权限
        import inspect
        src = inspect.getsource(vr.build_submission_index)
        for forbidden in ('"verdict"] =', "'verdict'] =", "verdict\":"):
            self.assertNotIn(forbidden, src)


class F51_CliWiring(unittest.TestCase):
    def _run_check_paper(self, doc_text):
        """跑 --check-paper 并在 tmpdir 存活期内收集断言素材（返回 rc+素材 dict）。"""
        doc = ("## 参考文献\n\n"
               "[1] Equipping agents for the real world with Agent Skills. "
               "https://www.anthropic.com/engineering/equipping-agents-for-"
               "the-real-world-with-agent-skills\n") if doc_text is None else doc_text
        with tempfile.TemporaryDirectory() as td:
            doc_path = os.path.join(td, "paper.md")
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(doc)
            out = os.path.join(td, "rpt.md")
            rc = vr.main_with_args(["--check-paper", doc_path, "--offline",
                                    "--out", out])
            idx_path = out.rsplit(".", 1)[0] + ".INDEX.md"
            audit_path = out.rsplit(".", 1)[0] + ".audit.md"
            json_path = out.rsplit(".", 1)[0] + ".json"
            return {
                "rc": rc,
                "index_exists": os.path.exists(idx_path),
                "audit_exists": os.path.exists(audit_path),
                "index_content": (open(idx_path, encoding="utf-8").read()
                                  if os.path.exists(idx_path) else ""),
                "results": (json.load(open(json_path, encoding="utf-8"))["results"]
                            if os.path.exists(json_path) else []),
                "doc_text": doc,
            }

    def test_package_files_and_index(self):
        got = self._run_check_paper(None)
        self.assertEqual(got["rc"], 0)
        self.assertTrue(got["index_exists"], "INDEX 未生成")
        self.assertTrue(got["audit_exists"],
                        "audit 报告未生成（--check-paper 必组合 audit-mode）")
        self.assertIn("投稿前审计包 INDEX", got["index_content"])
        self.assertIn("结论：", got["index_content"])

    def test_combination_matches_manual_flags(self):
        # 组合旗标不改判定语义：--check-paper 与 --check-document 判定一致
        got = self._run_check_paper(None)
        with tempfile.TemporaryDirectory() as td2:
            out2 = os.path.join(td2, "rpt2.md")
            doc2 = os.path.join(td2, "paper.md")
            with open(doc2, "w", encoding="utf-8") as f:
                f.write(got["doc_text"])
            vr.main_with_args(["--check-document", doc2,
                               "--offline", "--out", out2])
            d2 = json.load(open(out2.rsplit(".", 1)[0] + ".json",
                                encoding="utf-8"))
            self.assertEqual(
                [(r["index"], r["verdict"]) for r in got["results"]],
                [(r["index"], r["verdict"]) for r in d2["results"]])

    def test_help_documents_flag(self):
        from _mocks import engine_full_text
        src = engine_full_text()
        self.assertIn('"--check-paper"', src)


class F52_Selfcheck(unittest.TestCase):
    def test_selfcheck_runs_green(self):
        r = subprocess.run([sys.executable,
                            os.path.join(SK, "tools", "selfcheck.py")],
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(r.returncode, 0, r.stdout[-400:] + r.stderr[-200:])
        self.assertIn("自检通过", r.stdout)

    def test_selfcheck_ships_in_package(self):
        self.assertTrue(os.path.isfile(os.path.join(SK, "tools",
                                                    "selfcheck.py")))


class F53_McpToolEnumSync(unittest.TestCase):
    def test_skill_enumeration_matches_server(self):
        # 评测「示例与工具数量未随版本同步」病灶机制化：SKILL 枚举的 MCP
        # 工具名与 server.py 实际公开面（2 impl+3 handler）完全一致
        server_src = open(os.path.join(SK, "mcp", "server.py"),
                          encoding="utf-8").read()
        impls = [n for n in ("verify_references_impl", "explain_verdict_impl")
                 if f"def {n}" in server_src]
        handlers = [n for n in ("check_document", "discover_references",
                                "build_review_kit")
                    if f"def {n}(" in server_src]
        self.assertEqual(len(impls) + len(handlers), 5,
                         f"server.py 公开面变化（{len(impls)}+{len(handlers)}）"
                         "——同步更新 SKILL 枚举与本锁")
        # v6.5.0 F57 包态自足：随包子集会进发布包，而包内无 SKILL_ZH.md
        # （打包器排除；SH 包 SKILL.md 即中文版）——仓库态查双语文案，
        # 包态回退单 SKILL.md 查一遍
        skill_en = open(os.path.join(SK, "SKILL.md"), encoding="utf-8").read()
        zh_path = os.path.join(SK, "SKILL_ZH.md")
        skill_zh = (open(zh_path, encoding="utf-8").read()
                    if os.path.isfile(zh_path) else skill_en)
        for n in ("verify_references", "discover_references", "check_document",
                  "build_review_kit", "explain_verdict"):
            self.assertIn(f"`{n}`", skill_zh, n)
            self.assertIn(f"`{n}`", skill_en, n)


if __name__ == "__main__":
    unittest.main()
