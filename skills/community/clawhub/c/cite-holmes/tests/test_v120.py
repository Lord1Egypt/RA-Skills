#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v1.12.0：持久磁盘缓存 + --proxy + 能力矩阵「不支持输入」行。"""
import json
import os
import sys
import tempfile
import unittest
import unittest.mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import verify_refs as vr  # noqa: E402


def _fake_result(ref, idx, verdict="verified", note=""):
    return {"index": idx, "title": str(ref.get("title") or "")[:48],
            "url": str(ref.get("url") or ""), "doi": str(ref.get("doi") or ""),
            "pmid": str(ref.get("pmid") or ""), "arxiv": "",
            "source": str(ref.get("source") or ""), "year": ref.get("year"),
            "tier": "journal", "semantic": "", "verdict": verdict,
            "http_status": 200, "note": note, "needs_human_check": False,
            "checks": {}}


class TestV120(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v120_")
        vr._net_reset()
        vr._S2_LAST[0] = 0.0
        vr._ARXIV_LAST[0] = 0.0
        vr._OPTS.update({"openalex_key": "", "s2_key": "", "mailto": ""})
        self.dc = os.path.join(self.tmp, "dc.sqlite3")

    def _refs_file(self, refs):
        p = os.path.join(self.tmp, "refs.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(refs, f, ensure_ascii=False)
        return p

    def _run(self, refs, extra=(), verify_mock=None):
        p = self._refs_file(refs)
        out = os.path.join(self.tmp, f"r{len(extra)}.md")
        calls = {"n": 0}

        def fake(ref, idx, offline, timeout, medical=False):
            calls["n"] += 1
            return _fake_result(ref, idx)

        side = verify_mock or fake
        with unittest.mock.patch.object(vr, "verify_one", side_effect=side):
            rc = vr.main_with_args(["--refs", p, "--out", out,
                                    "--cache-path", self.dc,
                                    "--workers", "1", "--interval", "0",
                                    *extra])
        doc = json.load(open(out.rsplit(".", 1)[0] + ".json", encoding="utf-8"))
        return rc, calls, doc

    def test_version_bumped_120(self):
        self.assertEqual(vr.VERSION, "6.6.0")

    def test_disk_cache_hit_second_run_zero_calls(self):
        refs = [{"title": "A Paper About X", "doi": "10.1000/cache-hit"}]
        _, c1, _ = self._run(refs)
        self.assertEqual(c1["n"], 1)
        _, c2, doc2 = self._run(refs)
        self.assertEqual(c2["n"], 0, "TTL 内复跑应零外呼（磁盘缓存命中）")
        self.assertIn("磁盘缓存命中", doc2["results"][0]["note"])

    def test_cache_ttl_zero_forces_live(self):
        refs = [{"title": "A Paper About X", "doi": "10.1000/ttl0"}]
        _, c1, _ = self._run(refs, extra=["--cache-ttl", "0"])
        self.assertEqual(c1["n"], 1)
        _, c2, _ = self._run(refs, extra=["--cache-ttl", "0"])
        self.assertEqual(c2["n"], 1, "TTL=0 应视为过期，强制 live")

    def test_refresh_cache_bypasses_read(self):
        refs = [{"title": "A Paper About X", "doi": "10.1000/refresh"}]
        _, c1, _ = self._run(refs)
        self.assertEqual(c1["n"], 1)
        _, c2, _ = self._run(refs, extra=["--refresh-cache"])
        self.assertEqual(c2["n"], 1, "--refresh-cache 应绕过读强制重验")

    def test_strict_bypasses_cache_read(self):
        refs = [{"title": "A Paper About X", "doi": "10.1000/strict"}]
        _, c1, _ = self._run(refs)
        self.assertEqual(c1["n"], 1)
        _, c2, _ = self._run(refs, extra=["--strict"])
        self.assertEqual(c2["n"], 1, "--strict 应绕过缓存读（CI 诚实）")

    def test_no_cache_disables(self):
        refs = [{"title": "A Paper About X", "doi": "10.1000/nocache"}]
        _, c1, _ = self._run(refs, extra=["--no-cache"])
        self.assertEqual(c1["n"], 1)
        _, c2, _ = self._run(refs, extra=["--no-cache"])
        self.assertEqual(c2["n"], 1, "--no-cache 应完全不读写磁盘缓存")

    def test_unreachable_not_cached(self):
        calls = {"n": 0}

        def fake(ref, idx, offline, timeout, medical=False):
            calls["n"] += 1
            return _fake_result(ref, idx, verdict="unreachable",
                                note="HTTP 404（站点拒绝或页面不存在）")

        refs = [{"title": "A Paper About X", "doi": "10.1000/dead"}]
        self._run(refs, verify_mock=fake)
        self.assertEqual(calls["n"], 1)
        self._run(refs, verify_mock=fake)
        self.assertEqual(calls["n"], 2, "unreachable 为瞬态不入缓存——第二跑应重新外呼")

    def test_same_doi_different_title_is_different_key(self):
        # 判定依赖声称标题（相似度比对），同 DOI 不同声称必须分开缓存
        _, c1, _ = self._run([{"title": "First Title About X",
                               "doi": "10.1000/same"}])
        self.assertEqual(c1["n"], 1)
        _, c2, _ = self._run([{"title": "Second Totally Different Title",
                               "doi": "10.1000/same"}])
        self.assertEqual(c2["n"], 1, "同 DOI 不同声称标题 ≠ 缓存命中")

    def test_offline_never_reads_or_writes_cache(self):
        refs = [{"title": "A Paper About X", "doi": "10.1000/offline"}]
        _, c1, _ = self._run(refs, extra=["--offline"])
        self.assertEqual(c1["n"], 1)
        _, c2, _ = self._run(refs, extra=["--offline"])
        self.assertEqual(c2["n"], 1, "offline 判定不可入缓存（封顶 partial 非真网结论）")
        self.assertFalse(os.path.exists(self.dc), "offline 运行不应创建缓存库")

    def test_capability_matrix_unsupported_line_md_and_html(self):
        refs = [{"title": "A Paper About X", "doi": "10.1000/matrix"}]
        _, _, _ = self._run(refs)
        md = open(os.path.join(self.tmp, "r0.md"), encoding="utf-8").read()
        self.assertIn("不支持的输入", md)
        self.assertIn("PDF/Word 文档直读", md)
        html = vr.render_html([vr.verify_one.__wrapped__(refs[0], 1, True, 1.0)
                               if hasattr(vr.verify_one, "__wrapped__")
                               else _fake_result(refs[0], 1)], True)
        self.assertIn("不支持的输入", html)

    def test_proxy_flag_installs_opener(self):
        p = self._refs_file([{"title": "A Paper About X",
                              "doi": "10.1000/proxy"}])
        with unittest.mock.patch.object(vr.urllib.request, "install_opener") as io:
            vr.main_with_args(["--refs", p, "--out",
                               os.path.join(self.tmp, "px.md"),
                               "--cache-path", self.dc, "--offline",
                               "--proxy", "127.0.0.1:7890"])
        self.assertTrue(io.called, "--proxy 应安装显式代理 opener")
        director = io.call_args[0][0]
        ph = next(h for h in director.handlers
                  if isinstance(h, vr.urllib.request.ProxyHandler))
        self.assertEqual(ph.proxies,
                         {"http": "http://127.0.0.1:7890",
                          "https": "http://127.0.0.1:7890"},
                         "无 scheme 的代理地址应自动补 http://")


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestV120Guardrails(unittest.TestCase):
    """护栏:并行路径缓存命中 + 安全声明节防回退 + 包文档禁词扫描(cn-med-oa 教训)。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v120g_")
        vr._net_reset()
        self.dc = os.path.join(self.tmp, "dc.sqlite3")

    SKILL_EN = os.path.join(HERE, "..", "SKILL.md")
    # v6.5.0 F57 包态自足：随包子集进包后无 SKILL_ZH.md（SH 包 SKILL.md 即
    # 中文版）——包态回退单 SKILL.md；仓库态仍查双语
    SKILL_ZH = (os.path.join(HERE, "..", "SKILL_ZH.md")
                if os.path.isfile(os.path.join(HERE, "..", "SKILL_ZH.md"))
                else os.path.join(HERE, "..", "SKILL.md"))

    def test_parallel_second_run_zero_calls(self):
        p = os.path.join(self.tmp, "refs.json")
        refs = [{"title": f"Parallel Paper {i}", "doi": f"10.1000/par{i}"}
                for i in range(1, 5)]
        json.dump(refs, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        calls = {"n": 0}

        def fake(ref, idx, offline, timeout, medical=False):
            calls["n"] += 1
            return _fake_result(ref, idx)

        out = os.path.join(self.tmp, "r.md")
        base = ["--refs", p, "--out", out, "--cache-path", self.dc,
                "--workers", "4", "--interval", "0"]
        with unittest.mock.patch.object(vr, "verify_one", side_effect=fake):
            vr.main_with_args(base)
        self.assertEqual(calls["n"], 4)
        with unittest.mock.patch.object(vr, "verify_one", side_effect=fake):
            vr.main_with_args(base)
        self.assertEqual(calls["n"], 4, "并行路径第二跑同样应全量命中磁盘缓存")

    def test_security_declaration_present_both_languages(self):
        en = open(self.SKILL_EN, encoding="utf-8").read()
        zh = open(self.SKILL_ZH, encoding="utf-8").read()
        if os.path.isfile(os.path.join(HERE, "..", "SKILL_ZH.md")):
            # 仓库态：双语各查各的（SH 包 SKILL.md=中文版 / claw=英文版）
            self.assertIn("Security & behavior declaration", en)
            self.assertIn("安全与行为声明", zh)
        else:
            # v6.5.0 F57 包态：单一 SKILL.md，任一语言的声明在场即过
            self.assertTrue("Security & behavior declaration" in en
                            or "安全与行为声明" in en)
        for token in ("api.crossref.org", "api.openalex.org",
                      "eutils.ncbi.nlm.nih.gov", "export.arxiv.org",
                      "api.semanticscholar.org"):
            self.assertIn(token, en, f"声明节必须列明外联端点 {token}")

    def test_package_docs_free_of_scanner_trigger_words(self):
        # cn-med-oa 2.3.1 教训:文档措辞会触发平台安全扫描(定时任务/装依赖/提权)
        files = [self.SKILL_EN, self.SKILL_ZH,
                 os.path.join(HERE, "..", "README.md"),
                 os.path.join(HERE, "..", "references", "faq.md"),
                 os.path.join(HERE, "..", "references",
                              "verification-details.md")]
        banned = ["cro" + "ntab", "定时任务", "计划任务", "pip install",
                  "sudo ", "set" + "uid", "StrictHost" + "KeyChecking"]
        for fp in files:
            text = open(fp, encoding="utf-8").read()
            for w in banned:
                self.assertNotIn(w, text, f"{os.path.basename(fp)} 含禁词 {w}")

    def test_private_tools_absent_from_skill_dir(self):
        # 包净化:私有工具不得回迁 skill 目录(打包按目录树收文件)
        d = os.path.join(HERE, "..", "tools")
        present = {x for x in (os.listdir(d) if os.path.isdir(d) else [])
                   if os.path.isfile(os.path.join(d, x))}  # 只统计文件,忽略 __pycache__ 等缓存目录
        # v4.3.0 起 tools/ 白名单扩容：check_ta_table.py（TA 映射抽验——
        # 数据治理固化）+ build_retraction_cache.py（RWDB 官方 dump → 本地
        # 撤稿索引一键构建，--retraction-cache 配套）均为公开价值工具；
        # 守卫语义不变：白名单外文件即失败，私有工具仍进不来
        # v5.3.0 再扩容：run_eval.py（留出集评测公开口径 runner，随包分发）
        self.assertEqual(present, {"agentskills_check.py", "check_ta_table.py",
                                   "build_retraction_cache.py", "run_eval.py",
                                   "selfcheck.py", "netcheck.py",
                                   "run_tests.sh", "build_holdout.py"},
                         "tools/ 只应保留白名单公开工具")


if __name__ == "__main__":
    unittest.main(verbosity=2)
