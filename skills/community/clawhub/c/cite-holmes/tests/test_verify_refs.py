#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cite-holmes verify_refs.py 回归测试套件（v1.3.0 起）。

离线为主（快、稳定）；E-utilities 在线核验单列一组，网络不可达时跳过。
"""
import json
import os
import sys
import tempfile
import unittest
import unittest.mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import verify_refs as vr  # noqa: E402

EXAMPLES = os.path.join(HERE, "..", "examples")
DEMO = os.path.join(EXAMPLES, "demo_refs.json")
# v1.4：offline 只做结构核验，verified 封顶为 partial（诚实优先）
GOLDEN_OFFLINE = ["partial", "partial", "partial", "partial",
                  "partial", "partial", "partial", "invalid"]


def run_offline(refs):
    results = []
    for i, ref in enumerate(refs, 1):
        results.append(vr.verify_one(ref, i, True, 5.0))
    vr.mark_duplicates(results)
    return results


class TestOfflineBaseline(unittest.TestCase):
    """demo_refs.json（3 个埋雷 + 5 条真实）的判定金样本，自 v1.0 冻结。"""

    def test_demo_refs_golden_sequence(self):
        refs = json.load(open(DEMO, encoding="utf-8"))
        results = run_offline(refs)
        self.assertEqual([r["verdict"] for r in results], GOLDEN_OFFLINE)

    def test_scorecard_baseline(self):
        results = run_offline(json.load(open(DEMO, encoding="utf-8")))
        sc = vr.compute_scorecard(results)
        self.assertEqual(sc["counts"]["verified"], 0)
        self.assertEqual(sc["counts"]["partial"], 7)
        self.assertEqual(sc["counts"]["invalid"], 1)
        self.assertEqual(sc["score"], 25)
        self.assertEqual(sc["grade"], "D")


class TestScorecard(unittest.TestCase):
    def test_all_verified_is_100A(self):
        # 纯评分卡单元测试：直接构造 verified 结果（离线封顶另由 verify_one 测试覆盖）
        results = [{"index": i, "verdict": "verified", "title": f"s{i}"} for i in range(1, 10)]
        sc = vr.compute_scorecard(results)
        self.assertEqual((sc["score"], sc["grade"]), (100, "A"))

    def test_all_invalid_is_0D(self):
        refs = [{"title": f"x{i}"} for i in range(5)]
        sc = vr.compute_scorecard(run_offline(refs))
        self.assertEqual((sc["score"], sc["grade"]), (0, "D"))

    def test_empty(self):
        sc = vr.compute_scorecard([])
        self.assertEqual(sc["score"], 0)
        self.assertEqual(sc["total"], 0)

    def test_render_md_contains_scorecard(self):
        md = vr.render_md(run_offline(json.load(open(DEMO, encoding="utf-8"))), True)
        self.assertIn("CiteScore", md)
        self.assertIn("25 / 100 · D 级", md)


class TestDedupThreeKey(unittest.TestCase):
    def test_url_doi_pmid_dedup(self):
        # v3.4 语义:判重键=标识符+归一化标题指纹(同标识+同标题=真重复;
        # 同标识+不同标题=拼接变体,须独立判定——T2/T7 外部独测场景)
        results = [
            {"index": 1, "title": "Alpha Paper", "url": "https://x.com/", "doi": "10.1000/a",
             "pmid": "36443570", "verdict": "verified", "note": ""},
            {"index": 2, "title": "alpha  paper!", "url": "https://x.com", "doi": "", "pmid": "",
             "verdict": "verified", "note": ""},   # 同URL同标题(归一化后) → 重复
            {"index": 3, "title": "Alpha Paper", "url": "https://y.com", "doi": "10.1000/A",
             "pmid": "", "verdict": "verified", "note": ""},   # 同DOI同标题 → 重复
            {"index": 4, "title": "Alpha Paper", "url": "https://z.com", "doi": "",
             "pmid": "36443570", "verdict": "verified", "note": ""},   # 同PMID同标题 → 重复
            {"index": 5, "title": "Beta Paper", "url": "https://x.com", "doi": "", "pmid": "",
             "verdict": "verified", "note": ""},   # 同URL不同标题 → 独立判定(v3.4)
        ]
        vr.mark_duplicates(results)
        self.assertIn("与 #1 重复（同URL）", results[1]["note"])
        self.assertIn("与 #1 重复（同DOI）", results[2]["note"])
        self.assertIn("与 #1 重复（同PMID）", results[3]["note"])
        for r in results[1:4]:
            self.assertEqual(r["verdict"], "partial")
        self.assertEqual(results[0]["verdict"], "verified")
        # 不同标题不吞并:保持独立 verified
        self.assertNotIn("重复", results[4]["note"])
        self.assertEqual(results[4]["verdict"], "verified")


class TestMissingFields(unittest.TestCase):
    def test_doi_satisfies_url(self):
        self.assertNotIn("url", vr.missing_fields(
            {"title": "t", "source": "s", "year": 2024, "doi": "10.1000/abc"}))

    def test_pmid_satisfies_url(self):
        self.assertNotIn("url", vr.missing_fields(
            {"title": "t", "source": "s", "year": 2024, "pmid": "36443570"}))

    def test_nothing_satisfies(self):
        miss = vr.missing_fields({"title": "t", "source": "s", "year": 2024})
        self.assertTrue(any("url" in m for m in miss), miss)

    def test_error_notes_are_chinese(self):
        # 异常处理 4.3 评测项：错误提示必须中文可读
        ok, status, note = vr.check_url("https://nonexistent-domain-xyz-12345.example/x", 3)
        self.assertFalse(ok)
        self.assertTrue(any(ch in note for ch in "网络异常连接失败"),
                        f"错误信息应中文化: {note}")


class TestMedicalProfile(unittest.TestCase):
    def test_medical_tier_expansion(self):
        # v4.2.0：中文医学注册库无条件按期刊层识别（注册库地位与模式无关——
        # 万方在任何模式下都是学术注册库，非医学场景同样不该按 blog 计分）
        url = "https://d.wanfangdata.com.cn/periodical/example"
        self.assertEqual(vr.classify_tier(url, False), "journal")
        self.assertEqual(vr.classify_tier(url, True), "journal")
        # 非注册库的升级型信号仍由 medical 模式驱动（原有语义不回退）
        self.assertEqual(vr.classify_tier("https://example.org/x", False), "blog")

    def test_medical_offline_capped_at_partial(self):
        ref = {"title": "万方文献", "url": "https://d.wanfangdata.com.cn/periodical/x",
               "source": "期刊", "year": 2024}
        r = vr.verify_one(ref, 1, True, 5.0, medical=True)
        # v1.4 离线封顶：可信层 + 字段完整也不再给 verified
        self.assertEqual(r["verdict"], "partial")
        self.assertEqual(r["tier"], "journal")

    def test_medical_community_caveat(self):
        ref = {"title": "知乎讨论", "url": "https://zhuanlan.zhihu.com/p/123",
               "source": "community", "year": 2024}
        r = vr.verify_one(ref, 1, True, 5.0, medical=True)
        self.assertIn("不得支撑医学结论", r["note"])


class TestExports(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_test_")

    def _sample_results(self):
        return [
            {"index": 1, "title": "Real Study", "verdict": "verified", "tier": "journal",
             "http_status": 200, "needs_human_check": False, "year": 2023,
             "source": "Journal", "url": "https://a.b/c", "doi": "", "pmid": "36443570", "note": ""},
            {"index": 2, "title": "Fake Study", "verdict": "invalid", "tier": "-",
             "http_status": None, "needs_human_check": True, "year": 2023,
             "source": "", "url": "", "doi": "", "pmid": "99999999", "note": "编造"},
        ]

    def test_bibtex_verified_only(self):
        p = os.path.join(self.tmp, "out.bib")
        n = vr.export_bibtex(self._sample_results(), p)
        self.assertEqual(n, 1)
        content = open(p, encoding="utf-8").read()
        self.assertIn("@misc{", content)
        self.assertIn("Real Study", content)
        self.assertIn("PMID: 36443570", content)
        self.assertNotIn("Fake", content)

    def test_csv_full_ledger(self):
        p = os.path.join(self.tmp, "out.csv")
        vr.export_csv(self._sample_results(), p)
        lines = open(p, encoding="utf-8-sig").read().strip().splitlines()
        self.assertEqual(len(lines), 3)  # header + 2 rows
        self.assertIn("verdict", lines[0])

    def test_main_export_via_cli(self):
        refs_path = os.path.join(self.tmp, "refs.json")
        with open(refs_path, "w", encoding="utf-8") as f:
            json.dump([{"title": "t", "url": "https://www.nature.com/x",
                        "source": "journal", "year": 2025}], f)
        out = os.path.join(self.tmp, "r.md")
        code = vr.main_with_args(["--refs", refs_path, "--out", out,
                                  "--offline", "--export", "bibtex,csv"])
        self.assertEqual(code, 0)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "r.bib")))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "r.csv")))


class TestPubMedEUtilities(unittest.TestCase):
    """在线核验（依赖网络；不可达时跳过）。"""

    def setUp(self):
        try:
            ok, _ = vr.pubmed_pmid_exists("36443570", 8.0)
        except Exception:
            ok = None
        if ok is not True:
            self.skipTest("E-utilities 不可达")

    def test_real_pmid_exists(self):
        ok, note = vr.pubmed_pmid_exists("36443570", 8.0)
        self.assertTrue(ok)
        if "断路器" in note or "按可达处理" in note:
            self.skipTest("网络降级(断路器/超时)按可达处理=设计行为")
        self.assertIn("核实存在", note)

    def test_fake_pmid_rejected(self):
        ok, note = vr.pubmed_pmid_exists("99999999", 8.0)
        if "断路器" in note or "按可达处理" in note:
            self.skipTest("网络降级按可达处理=设计行为(勿当回归)")
        self.assertFalse(ok)
        self.assertIn("编造", note)


class TestV140(unittest.TestCase):
    """v1.4.0：DOI 元数据交叉验证 + --easy 傻瓜模式。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v140_")
        vr._net_reset()

    def _mock_urlopen(self, csl):
        """构造一个假的 urlopen 返回 CSL JSON。"""
        import io
        body = json.dumps(csl).encode("utf-8")

        class FakeResp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return body
        return FakeResp()

    def test_doi_metadata_match_ok(self):
        real = {"title": ["A landmark study about X"], "issued": {"date-parts": [[2023]]}}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self._mock_urlopen(real)):
            adjust, note, matched, _csl = vr.doi_metadata_match("10.1000/real", "a landmark study about x", 2023, 5)
        self.assertEqual(adjust, "")
        self.assertTrue(matched)
        self.assertIn("一致", note)

    def test_doi_metadata_mismatch_is_invalid(self):
        real = {"title": ["A completely different paper about Y"], "issued": {"date-parts": [[2019]]}}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self._mock_urlopen(real)):
            adjust, note, matched, _csl = vr.doi_metadata_match("10.1000/real", "a landmark study about x", 2023, 5)
        self.assertEqual(adjust, "invalid")
        self.assertTrue(matched)
        self.assertIn("编造或错引", note)

    def test_verify_one_flags_wrong_doi_paper(self):
        real = {"title": ["Some other unrelated paper"], "issued": {"date-parts": [[2020]]}}
        ref = {"title": "A landmark study about X", "doi": "10.1000/real",
               "url": f"https://doi.org/10.1000/real", "source": "journal", "year": 2020}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self._mock_urlopen(real)):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "invalid")
        self.assertTrue(r["needs_human_check"])

    def test_easy_mode_auto_medical_and_export(self):
        refs_path = os.path.join(self.tmp, "refs.json")
        with open(refs_path, "w", encoding="utf-8") as f:
            json.dump([{"title": "real study", "pmid": "36443570",
                        "source": "journal", "year": 2023}], f)
        out = os.path.join(self.tmp, "r.md")
        code = vr.main_with_args(["--refs", refs_path, "--out", out,
                                  "--easy", "--timeout", "10"])
        self.assertEqual(code, 0, "easy 模式应成功")
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "r.bib")), "easy 应自动导出 bibtex")
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "r.csv")), "easy 应自动导出 csv")

    def test_version_bumped(self):
        self.assertEqual(vr.VERSION, "6.9.0")


class TestHardening(unittest.TestCase):
    """评审加固项：非字符串标量、SSRF 防护、导出注入中和、offline 封顶。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_hard_")
        vr._net_reset()

    def test_non_string_scalars_do_not_crash_batch(self):
        refs = [{"title": 123, "url": 456, "source": "N", "year": 2024},
                {"title": "ok", "url": "https://www.nature.com/x", "source": "j", "year": 2024}]
        results = run_offline(refs)
        self.assertEqual(results[0]["verdict"], "invalid")
        self.assertEqual(results[1]["verdict"], "partial")

    def test_ssrf_guard_blocks_internal(self):
        reachable, status, note = vr.check_url("http://127.0.0.1:9/x", 3)
        self.assertFalse(reachable)
        self.assertIn("SSRF", note)

    def test_offline_never_awards_verified(self):
        refs = json.load(open(DEMO, encoding="utf-8"))
        results = run_offline(refs)
        self.assertNotIn("verified", [r["verdict"] for r in results])

    def test_bib_brace_stripped_and_keys_unique(self):
        results = [
            {"index": 1, "title": "study } one", "verdict": "verified", "year": 2024,
             "source": "j", "url": "https://a", "pmid": "", "doi": "", "note": ""},
            {"index": 2, "title": "🎉🎉🎉", "verdict": "verified", "year": 2024,
             "source": "j", "url": "https://b", "pmid": "", "doi": "", "note": ""},
            {"index": 3, "title": "🎉🎉🎉", "verdict": "verified", "year": 2024,
             "source": "j", "url": "https://c", "pmid": "", "doi": "", "note": ""},
        ]
        p = os.path.join(self.tmp, "o.bib")
        vr.export_bibtex(results, p)
        content = open(p, encoding="utf-8").read()
        self.assertEqual(content.count("@misc{"), 3)
        self.assertNotIn("} }", content.replace("}}", ""))  # 无逃逸花括号残留
        keys = [ln.split("{")[1].split(",")[0] for ln in content.splitlines() if ln.startswith("@misc")]
        self.assertEqual(len(keys), len(set(keys)), f"citation key 重复: {keys}")

    def test_csv_formula_neutralized(self):
        results = [{"index": 1, "title": "=HYPERLINK(\"https://evil.example\",\"x\")",
                    "verdict": "invalid", "tier": "-", "http_status": None,
                    "needs_human_check": False, "year": 2025, "source": "",
                    "url": "", "doi": "", "pmid": "", "note": ""}]
        p = os.path.join(self.tmp, "o.csv")
        vr.export_csv(results, p)
        row = open(p, encoding="utf-8-sig").read().splitlines()[1]
        self.assertTrue(row.startswith("'\"=H") or "\"'=H" in row or "\"=H" in row,
                        f"公式未中和: {row[:60]}")

    def test_md_note_escaped(self):
        results = [{"index": 1, "title": "t", "url": "a|b", "doi": "", "pmid": "",
                    "source": "", "year": 2025, "tier": "blog", "semantic": "",
                    "verdict": "partial", "http_status": None,
                    "note": "url 非 http(s) 格式: a|b", "needs_human_check": False}]
        md = vr.render_md(results, True)
        self.assertNotIn(" | a|b", md.splitlines()[4] if len(md.splitlines()) > 4 else md)
        self.assertIn("a\|b", md)


class TestV150(unittest.TestCase):
    """v1.5.0：arXiv 元数据校验 + Wayback 存档兜底 + arXiv 字段解析。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v150_")
        vr._net_reset()  # 断路器状态不跨测试泄漏
        vr._ARXIV_LAST[0] = 0.0  # 关掉 3 秒控频，保持套件快速

    def _fake_urlopen(self, body: bytes):
        class FakeResp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return body
        return unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                          return_value=FakeResp())

    @staticmethod
    def _atom(entries_xml: str, total: str = "1") -> bytes:
        return ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
                "<feed xmlns=\"http://www.w3.org/2005/Atom\">"
                "<title>ArXiv Query</title>"
                "<opensearch:totalResults xmlns:opensearch="
                "\"http://a9.com/-/spec/opensearch/1.1/\">"
                + total + "</opensearch:totalResults>"
                + entries_xml + "</feed>").encode("utf-8")

    # ---- ID 提取与字段解析 ----

    def test_arxiv_id_extract_forms(self):
        self.assertEqual(vr.extract_arxiv_id({"arxiv": "2310.10631v2"}), "2310.10631v2")
        self.assertEqual(vr.extract_arxiv_id({"arxiv": "arXiv:2106.09685"}), "2106.09685")
        self.assertEqual(vr.extract_arxiv_id(
            {"url": "https://arxiv.org/abs/1706.03762"}), "1706.03762")
        self.assertEqual(vr.extract_arxiv_id(
            {"url": "https://arxiv.org/pdf/hep-th/9901001v1"}), "hep-th/9901001v1")
        self.assertEqual(vr.extract_arxiv_id({"url": "https://www.nature.com/x"}), "")
        self.assertEqual(vr.extract_arxiv_id({"arxiv": "not-an-id"}), "")

    def test_arxiv_satisfies_url_and_resolves(self):
        self.assertEqual(vr.ref_to_url({"arxiv": "2106.09685"}),
                         "https://arxiv.org/abs/2106.09685")
        miss = vr.missing_fields({"title": "t", "source": "s", "year": 2024,
                                  "arxiv": "2106.09685"})
        self.assertNotIn("url", miss)

    # ---- arXiv 元数据校验（mock 官方 Atom API） ----

    def test_arxiv_metadata_match_verified(self):
        atom = self._atom(
            "<entry><title>Attention Is All\n   You Need</title>"
            "<published>2017-06-12T17:57:34Z</published></entry>")
        with self._fake_urlopen(atom):
            adjust, note, matched = vr.arxiv_metadata_match(
                "1706.03762", "Attention Is All You Need", 2017, 5)
        self.assertEqual(adjust, "")
        self.assertTrue(matched)
        self.assertIn("一致", note)

    def test_arxiv_metadata_mismatch_is_invalid(self):
        atom = self._atom(
            "<entry><title>Some totally different quantum gravity paper</title>"
            "<published>2019-03-01T00:00:00Z</published></entry>")
        with self._fake_urlopen(atom):
            adjust, note, matched = vr.arxiv_metadata_match(
                "1706.03762", "Attention Is All You Need", 2017, 5)
        self.assertEqual(adjust, "invalid")
        self.assertTrue(matched)
        self.assertIn("编造或错引", note)

    def test_arxiv_id_not_found_is_invalid(self):
        with self._fake_urlopen(self._atom("", total="0")):
            adjust, note, matched = vr.arxiv_metadata_match(
                "0704.99999", "Whatever Title", 2007, 5)
        self.assertEqual(adjust, "invalid")
        self.assertFalse(matched)
        self.assertIn("查无记录", note)

    def test_arxiv_error_entry_is_invalid(self):
        atom = self._atom(
            "<entry><title>Error</title>"
            "<summary>incorrect id format for garbage</summary>"
            "<arxiv:error xmlns:arxiv=\"http://arxiv.org/schemas/atom\">"
            "incorrect id format for garbage</arxiv:error></entry>")
        with self._fake_urlopen(atom):
            adjust, note, _ = vr.arxiv_metadata_match("garbage", "T", 2020, 5)
        self.assertEqual(adjust, "invalid")

    def test_verify_one_fake_arxiv_not_unreachable(self):
        # v1.4 教训的 arXiv 版：假 ID 必须判 invalid，不许漏成 unreachable
        ref = {"title": "A fabricated paper title", "arxiv": "0704.99999",
               "source": "preprint", "year": 2007}
        with self._fake_urlopen(self._atom("", total="0")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "invalid")
        self.assertTrue(r["needs_human_check"])
        self.assertEqual(r["url"], "https://arxiv.org/abs/0704.99999")

    def test_arxiv_malformed_month_rejected(self):
        # 月份段 99 语义非法（arXiv 语法 MM∈01-12）：客户端直接拒，绝不发出
        # 必然挂起的 API 查询，且报错要说清格式
        self.assertEqual(vr.extract_arxiv_id({"arxiv": "2099.12345"}), "")
        r = vr.verify_one({"title": "t", "arxiv": "2099.12345",
                           "source": "s", "year": 2099}, 1, True, 5.0)
        self.assertEqual(r["verdict"], "invalid")
        self.assertIn("arxiv", r["note"])

    def test_arxiv_resolver_404_invalid_when_api_down(self):
        # 官方 API 被墙（获取失败）+ 官方站 abs 页 404 → 仍判 invalid：
        # 存在性由官方解析器裁决，不因 API 不可达漏成 unreachable
        ref = {"title": "A fabricated paper title", "arxiv": "0704.99999",
               "source": "preprint", "year": 2007}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=vr.urllib.error.URLError("conn reset")), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(False, 404, "HTTP 404（站点拒绝或页面不存在）")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "invalid")
        self.assertIn("404", r["note"])
        self.assertTrue(r["needs_human_check"])

    def test_arxiv_api_down_page_200_still_verified(self):
        # 官方 API 被墙 + 官方站 abs 页 200 → 存在性已由官方站确认，判 verified
        # （备注注明 API 未核验内容）——与 DOI 元数据获取失败的处理对称
        ref = {"title": "Attention Is All You Need", "arxiv": "1706.03762",
               "source": "preprint", "year": 2017}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=vr.urllib.error.URLError("conn reset")), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "verified")
        self.assertIn("获取失败", r["note"])

    def test_arxiv_endpoint_url_wellformed(self):
        # 评审加固：捕获实际请求 URL，防止 endpoint/参数写错被"获取失败→SKIP"掩盖
        # v1.11 修正：旧版返回裸 bytes（with bytes 抛 TypeError 恰被吞成获取失败，
        # 单次调用掩盖了 mock 缺陷）；fallback 链引入后二次调用会覆盖 captured——
        # mock 必须返回真响应对象，且断言 API URL 为「首个」请求
        captured = {}

        class FakeResp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return atom_body

        atom_body = self._atom(
            "<entry><title>Attention Is All You Need</title>"
            "<published>2017-06-12T17:57:34Z</published></entry>")
        resp = FakeResp()

        def fake_urlopen(req, timeout=None):
            if not captured:
                captured["url"] = req.full_url
            return resp

        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=fake_urlopen):
            vr.arxiv_metadata_match("1706.03762", "Attention Is All You Need", 2017, 5)
        u = captured["url"]
        self.assertIn("export.arxiv.org/api/query", u)
        self.assertIn("id_list=1706.03762", u)

    def test_resolver_404_never_overrides_matched_metadata(self):
        # P0 评审修正：官方 API 已确认存在 + 脏 URL（尾点多一个句点）404
        # → 不许反转成 invalid，落 unreachable 转人工复核
        atom = self._atom(
            "<entry><title>Real Paper About X</title>"
            "<published>2020-01-01T00:00:00Z</published></entry>")
        ref = {"title": "Real Paper About X", "arxiv": "2001.99999",
               "url": "https://arxiv.org/abs/2001.99999.", "source": "preprint",
               "year": 2020}
        with self._fake_urlopen(atom), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(False, 404, "HTTP 404")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertNotEqual(r["verdict"], "invalid")
        self.assertEqual(r["verdict"], "unreachable")

    def test_rescue_respects_tier_gating(self):
        # P1 评审修正：真 arXiv ID + 403 博客链接 → 反爬救回不再无条件 verified，
        # blog 层封顶 partial
        atom = self._atom(
            "<entry><title>Real Paper About X</title>"
            "<published>2020-01-01T00:00:00Z</published></entry>")
        ref = {"title": "Real Paper About X", "arxiv": "2001.99999",
               "url": "https://some-blog.example/post", "source": "blog", "year": 2020}
        with self._fake_urlopen(atom), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(False, 403, "HTTP 403")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "partial")
        self.assertIn("存在性已确认", r["note"])

    def test_rescue_partial_metadata_stays_partial(self):
        # 二轮评审 P1：元数据相似度落在 0.50-0.82（partial 带）时，403 救回
        # 不得给 verified——403 的判定不得好于 200（200 路径同样降 partial）
        atom = self._atom(
            "<entry><title>Real Paper About X</title>"
            "<published>2020-01-01T00:00:00Z</published></entry>")
        ref = {"title": "Real Paper About Momentum", "arxiv": "2001.99999",
               "url": "https://www.nature.com/x", "source": "journal", "year": 2020}
        with self._fake_urlopen(atom), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(False, 403, "HTTP 403")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "partial")

    def test_arxiv_error_title_not_miskilled(self):
        # 二轮评审 P2：真实论文标题恰好叫 "Error" 时不得被误判 invalid
        # （判据以 ax:error 元素为准，标题等值仅辅助且需 summary 坐实）
        atom = self._atom(
            "<entry><title>Error</title>"
            "<summary>We study the propagation of rounding errors in numerical"
            " linear algebra.</summary>"
            "<published>2019-05-01T00:00:00Z</published></entry>")
        with self._fake_urlopen(atom):
            adjust, note, matched = vr.arxiv_metadata_match("1905.99999", "error", 2019, 5)
        self.assertEqual(adjust, "")
        self.assertTrue(matched)
        self.assertIn("一致", note)

    def test_bibtex_year_sanitized(self):
        # P1 评审修正：恶意 year 不得逃逸 @entry 注入假条目
        results = [{"index": 1, "title": "t", "verdict": "verified",
                    "year": "2020\n@x{y}", "source": "j", "url": "https://a",
                    "pmid": "", "doi": "", "note": ""}]
        p = os.path.join(self.tmp, "y.bib")
        vr.export_bibtex(results, p)
        content = open(p, encoding="utf-8").read()
        self.assertEqual(content.count("@misc{"), 1)
        self.assertNotIn("@x", content)
        self.assertIn("year = {2020}", content)

    def test_verify_one_arxiv_offline_capped_partial(self):
        ref = {"title": "Attention Is All You Need", "arxiv": "1706.03762",
               "source": "preprint", "year": 2017}
        r = vr.verify_one(ref, 1, True, 5.0)
        self.assertEqual(r["verdict"], "partial")
        self.assertEqual(r["tier"], "official")

    # ---- Wayback 存档兜底 ----

    def test_wayback_archived_attaches_link(self):
        wb = json.dumps({"archived_snapshots": {"closest": {
            "available": True,
            "url": "https://web.archive.org/web/20230512000000/https://example.com/dead",
            "timestamp": "20230512000000"}}}).encode("utf-8")
        ref = {"title": "dead but archived", "url": "https://example.com/dead-page",
               "source": "blog", "year": 2020}
        with unittest.mock.patch.object(
                vr, "check_url",
                return_value=(False, 404, "HTTP 404（站点拒绝或页面不存在）")), \
                self._fake_urlopen(wb):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "unreachable")
        self.assertTrue(r["needs_human_check"])
        self.assertIn("web.archive.org", r["note"])
        self.assertIn("2023-05-12", r["note"])

    def test_wayback_missing_stays_quiet(self):
        wb = json.dumps({"archived_snapshots": {}}).encode("utf-8")
        ref = {"title": "dead and gone", "url": "https://example.org/never-archived",
               "source": "blog", "year": 2021}
        with unittest.mock.patch.object(
                vr, "check_url",
                return_value=(False, None, "网络异常：timed out")), \
                self._fake_urlopen(wb):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "unreachable")
        self.assertNotIn("web.archive.org", r["note"])

    def test_wayback_ssrf_never_phones_home(self):
        m = unittest.mock.MagicMock()
        ref = {"title": "internal", "url": "http://127.0.0.1:9/x",
               "source": "s", "year": 2024}
        with unittest.mock.patch.object(
                vr, "check_url",
                return_value=(False, None, "连接失败")), \
                unittest.mock.patch.object(vr.urllib.request, "urlopen", m):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "unreachable")
        m.assert_not_called()  # 内网地址不得外发到 archive.org

    def test_wayback_url_param_minimally_encoded(self):
        # 实测：archive.org 对全量百分号编码不匹配 → url 参数必须保持 :// 原文
        captured = {}

        class EmptySnap:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return json.dumps({"archived_snapshots": {}}).encode()

        def fake_urlopen(req, timeout=None):
            captured["url"] = req.full_url
            return EmptySnap()

        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=fake_urlopen):
            vr.wayback_available("https://www.geocities.com/SiliconValley/a b/", 5)
        u = captured["url"]
        self.assertIn("://www.geocities.com", u)
        self.assertNotIn("%3A%2F", u)
        self.assertIn("%20", u)  # 空格仍需编码


class TestArxivLive(unittest.TestCase):
    """真实网络 arXiv 校验（网络分叉自适应：官方 API 可达走元数据路径；
    API 被墙但官方站可达走 404 解析器路径；两者皆不通则跳过）。"""

    def setUp(self):
        vr._net_reset()
        vr._ARXIV_LAST[0] = 0.0

    def test_real_arxiv_id_verified(self):
        vr._ARXIV_LAST[0] = 0.0
        try:
            adjust, note, matched = vr.arxiv_metadata_match(
                "1706.03762", "Attention Is All You Need", 2017, 8)
        except Exception:
            self.skipTest("export.arxiv.org 不可达")
        if not matched and "获取失败" in note:
            self.skipTest("export.arxiv.org 不可达")
        self.assertEqual(adjust, "")
        self.assertTrue(matched)

    def test_wellformed_fake_arxiv_id_invalid(self):
        import time
        ref = {"title": "Any Plausible Sounding Title", "arxiv": "0704.99999",
               "source": "preprint", "year": 2007}
        verdict, note = "", ""
        # API 偶发瞬态失败会走降级分支，重试一次再裁决
        for _ in range(2):
            vr._ARXIV_LAST[0] = 0.0
            r = vr.verify_one(dict(ref), 1, False, 8.0)
            verdict, note = r["verdict"], r["note"]
            if verdict == "invalid":
                break
            time.sleep(3)
        if verdict == "unreachable" and "获取失败" in note:
            self.skipTest("arXiv API 与官方站在本网络均不可达")
        self.assertEqual(verdict, "invalid")
        self.assertTrue(("查无记录" in note) or ("404" in note), note)


class TestV160(unittest.TestCase):
    """v1.6.0：主机断路器 + 可操作报错 + DOI↔PMID 交叉 + 期刊名核查。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v160_")
        vr._net_reset()
        vr._ARXIV_LAST[0] = 0.0

    class _FakeOpener:
        """check_url 走 build_opener().open()，mock 整个 opener。"""

        def __init__(self, exc):
            self.exc = exc
            self.calls = 0

        def open(self, req, timeout=None):
            self.calls += 1
            raise self.exc

    # ---- F1 主机断路器 ----

    def test_breaker_opens_after_two_transport_failures(self):
        url = "https://deadhost.example/x"
        op1 = self._FakeOpener(vr.urllib.error.URLError("timed out"))
        with unittest.mock.patch.object(vr.urllib.request, "build_opener",
                                        return_value=op1):
            ok1, _, note1 = vr.check_url(url, 5)
        self.assertFalse(ok1)
        self.assertFalse(vr._cb_open(url), "第一次失败只计数，不熔断")
        self.assertIn("--timeout 20", note1, "超时话术要给可操作建议")
        op2 = self._FakeOpener(vr.urllib.error.URLError("timed out"))
        with unittest.mock.patch.object(vr.urllib.request, "build_opener",
                                        return_value=op2):
            vr.check_url(url, 5)
        self.assertTrue(vr._cb_open(url), "连续两次传输失败应熔断")
        op3 = self._FakeOpener(AssertionError("熔断后不得再发外呼"))
        with unittest.mock.patch.object(vr.urllib.request, "build_opener",
                                        return_value=op3):
            ok3, _, note3 = vr.check_url(url, 5)
        op3_calls = op3.calls
        self.assertFalse(ok3)
        self.assertIn("断路器", note3)
        self.assertEqual(op3_calls, 0, "熔断后 opener 不得被调用")

    def test_breaker_http_failures_do_not_trigger(self):
        url = "https://http404host.example/x"
        exc = vr.urllib.error.HTTPError(url, 404, "Not Found", None, None)
        op = self._FakeOpener(exc)
        with unittest.mock.patch.object(vr.urllib.request, "build_opener",
                                        return_value=op):
            vr.check_url(url, 5)
            vr.check_url(url, 5)
        self.assertFalse(vr._cb_open(url), "HTTP 层失败（404）是站点响应，不得熔断")
        with unittest.mock.patch.object(vr.urllib.request, "build_opener",
                                        return_value=op):
            vr.check_url(url, 5)
        self.assertGreaterEqual(op.calls, 3, "HTTP 失败后仍应继续正常外呼")

    def test_breaker_dns_wording(self):
        url = "https://nodns-acc.example/x"
        op = self._FakeOpener(vr.urllib.error.URLError(
            "[Errno -2] Name or service not known"))
        with unittest.mock.patch.object(vr.urllib.request, "build_opener",
                                        return_value=op):
            _, _, note = vr.check_url(url, 5)
        self.assertIn("域名无法解析", note)

    def test_breaker_success_resets_counter(self):
        url = "https://flakyhost.example/x"
        host_key = vr._cb_host(url)
        op = self._FakeOpener(vr.urllib.error.URLError("timed out"))
        with unittest.mock.patch.object(vr.urllib.request, "build_opener",
                                        return_value=op):
            vr.check_url(url, 5)
        self.assertEqual(vr._CB[host_key]["fails"], 1)
        vr._cb_record(url, False)
        self.assertEqual(vr._CB[host_key]["fails"], 0, "成功/HTTP 响应应清零计数")

    # ---- F3 DOI↔PMID 交叉 ----

    @staticmethod
    def _esummary_body(doi_value):
        return json.dumps({"result": {"36443570": {
            "uid": "36443570",
            "articleids": [{"idtype": "doi", "value": doi_value}]}}}).encode()

    def test_pmid_doi_crosscheck_match_and_splice(self):
        class FakeResp:
            def __init__(self, body):
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return self.body

        with unittest.mock.patch.object(
                vr.urllib.request, "urlopen",
                return_value=FakeResp(self._esummary_body("10.1000/real"))):
            adj, note = vr.pmid_doi_crosscheck("36443570", "10.1000/Real", 5)
        self.assertEqual(adj, "")
        self.assertIn("交叉一致", note)
        with unittest.mock.patch.object(
                vr.urllib.request, "urlopen",
                return_value=FakeResp(self._esummary_body("10.1000/real"))):
            adj, note = vr.pmid_doi_crosscheck("36443570", "10.1000/other", 5)
        self.assertEqual(adj, "invalid")
        self.assertIn("拼接伪造", note)

    def test_verify_one_spliced_ids_caught_end_to_end(self):
        # 双键各自真实但互相拼接：DOI 的 CSL 与标题一致（单看 DOI 全过），
        # 但 PMID 登记的是另一个 DOI → 必须判 invalid
        csl = json.dumps({"title": ["A Real Paper About X"],
                          "issued": {"date-parts": [[2023]]}}).encode()
        esum = self._esummary_body("10.1000/the-other-real-doi")

        class DispatchResp:
            def __init__(self, url):
                self.body = esum if "esummary" in url else csl

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return self.body

        def fake_urlopen(req, timeout=None):
            return DispatchResp(req.full_url)

        ref = {"title": "A Real Paper About X", "doi": "10.1000/claimed-doi",
               "pmid": "36443570", "source": "journal", "year": 2023}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=fake_urlopen):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "invalid")
        self.assertIn("拼接伪造", r["note"])

    def test_breaker_skips_crosscheck_and_doi_metadata(self):
        vr._CB["https://eutils.ncbi.nlm.nih.gov"] = {"fails": 2, "open": True}
        m = unittest.mock.MagicMock()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m):
            adj, note = vr.pmid_doi_crosscheck("36443570", "10.1000/x", 5)
        m.assert_not_called()
        self.assertEqual(adj, "")
        self.assertIn("断路器", note)
        vr._CB["https://doi.org"] = {"fails": 2, "open": True}
        m2 = unittest.mock.MagicMock()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m2):
            adj2, note2, _c2, _csl_extra = vr.doi_metadata_match("10.1000/real", "t", 2024, 5)
        m2.assert_not_called()
        self.assertIn("断路器", note2)

    # ---- F4 期刊名核查 ----

    def test_doi_journal_mismatch_downgrades(self):
        csl = {"title": ["A Real Paper About X"], "issued": {"date-parts": [[2023]]},
               "container-title": "Journal of Totally Different Things"}

        class FakeResp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return json.dumps(csl).encode()

        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=FakeResp()):
            adj, note, matched, _csl = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                source="Completely Other Journal")
        self.assertEqual(adj, "partial")
        self.assertTrue(matched)
        self.assertIn("期刊名不符", note)
        # 期刊改名/包含关系容错
        csl["container-title"] = "The Lancet"
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=FakeResp()):
            adj2, note2, _c2, _csl_extra = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5, source="Lancet")
        self.assertEqual(adj2, "")
        self.assertNotIn("期刊名不符", note2)

    # ---- F2 待人工复核建议动作 ----

    def test_render_md_suggested_actions(self):
        results = [
            {"index": 1, "title": "bad", "url": "", "doi": "", "pmid": "",
             "source": "", "year": 2025, "tier": "-", "semantic": "",
             "verdict": "invalid", "http_status": None, "note": "无 url",
             "needs_human_check": True},
            {"index": 2, "title": "dead", "url": "https://x.example", "doi": "",
             "pmid": "", "source": "", "year": 2025, "tier": "blog",
             "semantic": "", "verdict": "unreachable", "http_status": None,
             "note": "HTTP 404", "needs_human_check": True},
        ]
        md = vr.render_md(results, False)
        self.assertIn("建议：删除或更换信源", md)
        self.assertIn("建议：人工打开原链复核", md)

    # ---- 二轮评审修复项 ----

    def test_wayback_breaker_gates_archive_org_not_target(self):
        # P1 修正：断路器只看真正的外呼对象 archive.org；目标主机熔断
        # 不影响存档查询（死站查存档正是本函数主用例）
        vr._CB["https://archive.org"] = {"fails": 2, "open": True}
        m = unittest.mock.MagicMock()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m):
            self.assertEqual(vr.wayback_available("https://dead.example/x", 5), "")
        m.assert_not_called()
        # 目标主机熔断：仍应发起 archive.org 查询
        vr._net_reset()
        vr._CB["https://dead.example"] = {"fails": 2, "open": True}
        m2 = unittest.mock.MagicMock()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m2):
            vr.wayback_available("https://dead.example/x", 5)
        m2.assert_called()

    def test_crosscheck_skips_when_no_registered_doi(self):
        body = json.dumps({"result": {"36443570": {
            "uid": "36443570",
            "articleids": [{"idtype": "pmid", "value": "36443570"}]}}}).encode()

        class FakeResp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return body

        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=FakeResp()):
            adj, note = vr.pmid_doi_crosscheck("36443570", "10.1000/whatever", 5)
        self.assertEqual(adj, "")
        self.assertIn("未登记 DOI", note)

    # ---- v1.8 前置回归：--easy 医学误触发修复 ----

    def test_easy_wanfang_alone_stays_general(self):
        refs_path = os.path.join(self.tmp, "wf.json")
        with open(refs_path, "w", encoding="utf-8") as f:
            json.dump([{"title": "技术趋势观察", "url": "https://d.wanfangdata.com.cn/periodical/x",
                        "source": "期刊", "year": 2026}], f)
        out = os.path.join(self.tmp, "e.md")
        vr.main_with_args(["--refs", refs_path, "--out", out, "--easy", "--offline"])
        d = json.load(open(out[:-3] + ".json", encoding="utf-8"))
        self.assertEqual(d["profile"], "general", "单条万方来源不应误触发医学预设")

    def test_easy_two_medical_hits_still_trigger(self):
        refs_path = os.path.join(self.tmp, "wf2.json")
        with open(refs_path, "w", encoding="utf-8") as f:
            json.dump([
                {"title": "a", "url": "https://d.wanfangdata.com.cn/periodical/x", "source": "s", "year": 2026},
                {"title": "b", "url": "https://rs.yiigle.com/c/article/x", "source": "s", "year": 2026},
            ], f)
        out = os.path.join(self.tmp, "e2.md")
        vr.main_with_args(["--refs", refs_path, "--out", out, "--easy", "--offline"])
        d = json.load(open(out[:-3] + ".json", encoding="utf-8"))
        self.assertEqual(d["profile"], "medical", "≥2 条医学域命中仍应触发医学预设")

    def test_journal_nlm_abbreviation_not_mismatch(self):
        # P1 修正：NLM 缩写（可跳过虚词、词首匹配）不得误报期刊名不符
        csl = {"title": ["A Real Paper About X"], "issued": {"date-parts": [[2023]]},
               "container-title": "New England Journal of Medicine"}

        class FakeResp:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                return json.dumps(csl).encode()

        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=FakeResp()):
            adj, note, _c1, _csl_extra = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                source="N Engl J Med")
        self.assertEqual(adj, "")
        self.assertNotIn("期刊名不符", note)
        # 真不符依旧要抓
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=FakeResp()):
            adj2, note2, _c2, _csl_extra = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                source="Lancet Neurology")
        self.assertEqual(adj2, "partial")
        self.assertIn("期刊名不符", note2)


class TestV170(unittest.TestCase):
    """v1.7.0：作者名核查 + 能力边界矩阵 + HTML 单文件报告。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v170_")
        vr._net_reset()
        vr._ARXIV_LAST[0] = 0.0

    class FakeResp:
        def __init__(self, body):
            self.body = body

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return self.body

    @staticmethod
    def _csl(authors=None):
        m = {"title": ["A Real Paper About X"], "issued": {"date-parts": [[2023]]}}
        if authors is not None:
            m["author"] = authors
        return m

    # ---- F2 作者名核查 ----

    def test_author_first_author_match_consistent(self):
        csl = self._csl([{"family": "Smith", "given": "J"},
                         {"family": "Zhang", "given": "W"}])
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, note, _c1, _csl_extra = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                authors="Smith J, Wang L")
        self.assertEqual(adj, "")
        self.assertNotIn("作者不符", note)

    def test_author_case_variant_tolerant(self):
        csl = self._csl([{"family": "MacQueen", "given": "J."}])
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, _, _, _csl_x = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                authors="macqueen j")
        self.assertEqual(adj, "")

    def test_author_all_missing_downgrades_partial(self):
        csl = self._csl([{"family": "Smith", "given": "J"}])
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, note, _c1, _csl_extra = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                authors="Yan C, Zhao M")
        self.assertEqual(adj, "partial")
        self.assertIn("作者不符", note)

    def test_author_apa_initials_do_not_rescue_mismatch(self):
        # 二轮评审 P1：APA "Torvalds, L." 的单字母缩写不得子串命中无关作者——
        # 换掉全部作者的拼接伪造必须仍被抓
        csl = self._csl([{"family": "Chen", "given": "Liwei"}])
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, note, _c1, _csl_extra = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                authors="Torvalds, L.")
        self.assertEqual(adj, "partial")
        self.assertIn("作者不符", note)

    def test_author_long_list_initials_no_false_hit(self):
        # 二轮评审 P1：长作者列表的 given initial（"G."）不得让任意姓氏命中
        authors_csl = [{"family": f"Auth{i}", "given": chr(65 + i % 26) + "."}
                       for i in range(20)]
        csl = self._csl(authors_csl)
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, _, _, _csl_x = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5, authors="Wang")
        self.assertEqual(adj, "partial")

    def test_author_cjk_vs_pinyin_skipped(self):
        # 二轮评审 P2：中文译名 vs 拼音登记不可比 → 跳过判定（与期刊核查同守卫）
        csl = self._csl([{"family": "Wang", "given": "Wu"}])
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, _, _, _csl_x = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5, authors="王五")
        self.assertEqual(adj, "")

    def test_author_punct_only_skipped(self):
        # 二轮评审 P3：规范化后为空的声称 token 不得触发假"作者不符"
        csl = self._csl([{"family": "Smith", "given": "J"}])
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, _, _, _csl_x = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5, authors="!!!")
        self.assertEqual(adj, "")

    def test_author_check_skips_without_registered_list(self):
        csl = self._csl()  # 无 author 字段 → 跳过判定
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.FakeResp(json.dumps(csl).encode())):
            adj, _, _, _csl_x = vr.doi_metadata_match(
                "10.1000/real", "a real paper about x", 2023, 5,
                authors="Nobody A")
        self.assertEqual(adj, "")

    # ---- F2 能力边界矩阵 ----

    def test_capability_matrix_in_md_report(self):
        results = [{"index": 1, "title": "t", "url": "https://x.example", "doi": "",
                    "pmid": "", "source": "", "year": 2025, "tier": "blog",
                    "semantic": "", "verdict": "partial", "http_status": None,
                    "note": "", "needs_human_check": False}]
        md = vr.render_md(results, False)
        self.assertIn("能力边界矩阵", md)
        self.assertIn("假 DOI", md)
        self.assertIn("语义层把关", md)

    # ---- F1 HTML 报告 ----

    def test_render_html_self_contained_and_escaped(self):
        results = [{"index": 1, "title": "t<script>alert(1)</script>",
                    "url": "https://x.example", "doi": "", "pmid": "",
                    "source": "", "year": 2025, "tier": "blog", "semantic": "",
                    "verdict": "partial", "http_status": 200,
                    "note": "备注含 <b>标签</b> 与 Wayback 存档可用（2023-05-12）："
                            "https://web.archive.org/web/1/x",
                    "needs_human_check": True}]
        h = vr.render_html(results, False)
        self.assertTrue(h.lstrip().lower().startswith("<!doctype html"))
        self.assertNotIn("<script", h)                      # 动态内容被转义
        self.assertNotIn("<script src=", h)                 # 零外链脚本
        self.assertNotIn("<link ", h)                       # 零外链样式
        self.assertIn("alert(1)", h)                        # 内容仍在（已转义）
        self.assertIn("能力边界矩阵", h)
        self.assertIn("建议：", h)                           # 复核区带建议动作
        self.assertIn('<a href="https://web.archive.org/web/1/x">', h)  # 存档链可点

    def test_cli_format_html_end_to_end(self):
        refs_path = os.path.join(self.tmp, "refs.json")
        with open(refs_path, "w", encoding="utf-8") as f:
            json.dump([{"title": "t", "url": "https://www.nature.com/x",
                        "source": "journal", "year": 2025}], f)
        out = os.path.join(self.tmp, "report.html")
        code = vr.main_with_args(["--refs", refs_path, "--out", out,
                                  "--offline", "--format", "html"])
        self.assertEqual(code, 0)
        content = open(out, encoding="utf-8").read()
        self.assertTrue(content.lstrip().lower().startswith("<!doctype html"))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "report.json")) is False)

    def test_version_bumped_170(self):
        self.assertEqual(vr.VERSION, "6.9.0")


class TestV180(unittest.TestCase):
    """v1.8.0：撤稿检测 + OpenAlex 书目核查 + UA 轮换。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v180_")
        vr._net_reset()
        vr._ARXIV_LAST[0] = 0.0

    class Resp:
        def __init__(self, body):
            self.body = body

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return self.body

    def test_crossref_retraction_detected(self):
        body = json.dumps({"message": {"updated-by": [
            {"DOI": "10.1111/x", "type": "correction", "label": "Correction"},
            {"DOI": "10.1111/retract", "type": "retraction", "label": "Retraction",
             "updated": {"date-time": "2020-02-06T00:00:00Z"}},
        ]}}).encode()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.Resp(body)):
            ret = vr.crossref_retraction_check("10.1000/retracted", 5)
        self.assertTrue(ret["retracted"])
        self.assertEqual(ret["nature"], "retraction")
        self.assertEqual(ret["notice_doi"], "10.1111/retract")
        note = vr._retraction_nature_note(ret["nature"], ret["when"],
                                          ret["notice_doi"], "Crossref/Retraction Watch")
        self.assertIn("已撤稿", note)
        self.assertIn("不得作为有效证据", note)

    def test_crossref_correction_only_not_retracted(self):
        body = json.dumps({"message": {"updated-by": [
            {"DOI": "10.1111/x", "type": "correction", "label": "Correction"},
        ]}}).encode()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.Resp(body)):
            ret = vr.crossref_retraction_check("10.1000/corrected", 5)
        self.assertFalse(ret["retracted"])
        # v4.1.0：更正通告分档可见（原二元判定静默丢弃）
        self.assertEqual(ret["nature"], "correction")

    def test_crossref_failure_silent(self):
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=vr.urllib.error.HTTPError(
                                            "u", 500, "boom", None, None)):
            ret = vr.crossref_retraction_check("10.1000/x", 5)
        self.assertFalse(ret["retracted"])
        self.assertFalse(ret["check_failed"])  # HTTPError 不算传输失败

    def test_verify_one_retracted_doi_capped_partial(self):
        # 撤稿论文真实存在（可达+权威层+字段全）但必须封顶 partial 转人工复核
        csl = json.dumps({"title": ["A Retracted Paper About X"],
                          "issued": {"date-parts": [[2020]]}}).encode()
        cr = json.dumps({"message": {"updated-by": [
            {"DOI": "10.1111/retract", "type": "retraction"}]}}).encode()
        bodies = [csl, cr]

        class Dispatch:
            def __init__(self, bodies):
                self.i = 0
                self.bodies = bodies

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                b = self.bodies[min(self.i, len(self.bodies) - 1)]
                self.i += 1
                return b

        seq = Dispatch(bodies)
        ref = {"title": "A Retracted Paper About X", "doi": "10.1000/ret",
               "source": "journal", "year": 2020}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=lambda req, timeout=None: seq),                 unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "partial")
        self.assertTrue(r["needs_human_check"])
        self.assertIn("已撤稿", r["note"])

    def test_openalex_confirms_doi_less_ref(self):
        # Nature 真实案例：声称短标题 vs 登记全标题（前缀关系）→ 确认存在
        body = json.dumps({"results": [{"display_name":
            "Hallucinated citations are polluting the scientific literature. What can be done?",
            "publication_year": 2026}]}).encode()
        ref = {"title": "Hallucinated citations are polluting the scientific literature",
               "url": "https://www.nature.com/articles/d41586-026-00969-z",
               "source": "Nature News", "year": 2026}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.Resp(body)),                 unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertIn("OpenAlex 书目确认存在", r["note"])

    def test_openalex_no_result_neutral_note(self):
        body = json.dumps({"results": []}).encode()
        ref = {"title": "A Very Obscure Preprint About Nothing Much At All Really",
               "url": "https://obscure.example/post", "source": "blog", "year": 2026}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.Resp(body)),                 unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertNotEqual(r["verdict"], "invalid")
        self.assertIn("不作为编造依据", r["note"])

    def test_openalex_skipped_for_short_title(self):
        m = unittest.mock.MagicMock()
        ref = {"title": "短标题", "url": "https://x.example/a", "source": "s", "year": 2026}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m),                 unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            vr.verify_one(ref, 1, False, 5.0)
        m.assert_not_called()

    def test_arxiv_ua_rotation_on_406(self):
        # 406 时第二次尝试换浏览器 UA（韧性回归）
        uas = []

        class Resp406Then200:
            def __init__(self, uas):
                self.uas = uas
                self.n = 0

        def fake_urlopen(req, timeout=None):
            uas.append(req.headers.get("User-agent") or req.headers.get("User-Agent"))
            if len(uas) == 1:
                raise vr.urllib.error.HTTPError(req.full_url, 406, "Not Acceptable", None, None)
            return TestV180.Resp(TestV180._atom_static())

        atom = ('<?xml version="1.0" encoding="UTF-8"?>'
                '<feed xmlns="http://www.w3.org/2005/Atom">'
                '<entry><title>Attention Is All You Need</title>'
                '<published>2017-06-12T17:57:34Z</published></entry></feed>').encode()
        TestV180._atom_static = lambda: atom
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=fake_urlopen):
            adjust, note, matched = vr.arxiv_metadata_match(
                "1706.03762", "Attention Is All You Need", 2017, 5)
        self.assertEqual(adjust, "")
        self.assertTrue(matched)
        self.assertTrue(any("Mozilla/5.0" in (u or "") for u in uas),
                        f"重试应换浏览器 UA: {uas}")

    def test_capability_matrix_has_retraction(self):
        cap = vr.capability_matrix()
        self.assertTrue(any("撤稿" in x for x in cap["caught"]))

    def test_crossref_openalex_breaker_wired(self):
        # 评审 P1 修复：两个新端点接入主机断路器（熔断后零外呼）
        vr._CB["https://api.crossref.org"] = {"fails": 2, "open": True}
        m = unittest.mock.MagicMock()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m):
            vr.crossref_retraction_check("10.1000/x", 5)
        m.assert_not_called()
        vr._net_reset()
        vr._CB["https://api.openalex.org"] = {"fails": 2, "open": True}
        m2 = unittest.mock.MagicMock()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m2):
            vr.openalex_title_check("A Long Enough Title For The Check To Run", 5)
        m2.assert_not_called()

    def test_doi_ua_rotation_on_403(self):
        # 评审 P1 修复：doi.org 元数据请求 403/406 时第二次尝试换浏览器 UA
        uas = []
        atom = json.dumps({"title": ["A Retracted Paper About X"],
                           "issued": {"date-parts": [[2020]]}}).encode()

        def fake_urlopen(req, timeout=None):
            uas.append(req.headers.get("User-agent") or req.headers.get("User-Agent"))
            if len(uas) == 1:
                raise vr.urllib.error.HTTPError(req.full_url, 406, "Not Acceptable", None, None)
            return TestV180.Resp(atom)

        vr._ARXIV_LAST[0] = 0.0
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=fake_urlopen):
            adjust, note, matched, _csl = vr.doi_metadata_match(
                "10.1000/real", "a retracted paper about x", 2020, 5)
        self.assertEqual(adjust, "")
        self.assertTrue(matched)
        self.assertTrue(any("Mozilla/5.0" in (u or "") for u in uas),
                        f"重试应换浏览器 UA: {uas}")

    def test_retracted_partial_also_flagged(self):
        # 评审 P2 修复：撤稿 + 因层级降级（非 verified）也置人工复核
        csl = json.dumps({"title": ["A Retracted Paper About X"],
                          "issued": {"date-parts": [[2020]]}}).encode()
        cr = json.dumps({"message": {"updated-by": [
            {"DOI": "10.1111/retract", "type": "retraction"}]}}).encode()

        class Dispatch:
            def __init__(self):
                self.i = 0

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                b = [csl, cr][min(self.i, 1)]
                self.i += 1
                return b

        ref = {"title": "A Retracted Paper About X", "doi": "10.1000/ret",
               "url": "https://some-blog.example/post", "source": "blog", "year": 2020}
        shared = Dispatch()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=lambda req, timeout=None: shared),                 unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "partial")
        self.assertTrue(r["needs_human_check"])

    def test_version_bumped_180(self):
        self.assertEqual(vr.VERSION, "6.9.0")


class TestV190(unittest.TestCase):
    """v1.9.0：S2 第三源交叉确认 + BibTeX 导入 + OpenAlex key + mailto polite pool
    + 429 Retry-After + 投稿前结论 + auditjson 透明工作底稿。"""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="ch_v190_")
        vr._net_reset()
        vr._S2_LAST[0] = 0.0
        vr._OPTS.update({"openalex_key": "", "s2_key": "", "mailto": ""})

    def tearDown(self):
        vr._OPTS.update({"openalex_key": "", "s2_key": "", "mailto": ""})

    class Resp:
        def __init__(self, body):
            self.body = body

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return self.body

    @staticmethod
    def _seq(bodies):
        """按序消费响应体/异常的 urlopen 替身（耗尽后重复最后一项）。"""

        class Dispatch:
            def __init__(self, items):
                self.i = 0
                self.items = items

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

            def read(self):
                b = self.items[min(self.i, len(self.items) - 1)]
                self.i += 1
                if isinstance(b, Exception):
                    raise b
                return b.body if hasattr(b, "body") else b

        return Dispatch(bodies)

    # ---------- S2 第三源交叉确认 ----------

    def test_version_bumped_190(self):
        self.assertEqual(vr.VERSION, "6.9.0")

    def test_s2_confirms_and_rescues_403_landing(self):
        # DOI.org 元数据获取失败（传输错误×2）→ S2 确认存在 → 着陆页 403 救回 verified
        transport_err = vr.urllib.error.URLError("timed out")
        s2 = json.dumps({"title": "A Verified Paper About Topic X",
                         "year": 2026}).encode()
        cr = json.dumps({"message": {}}).encode()
        seq = self._seq([transport_err, transport_err, transport_err,
                         self.Resp(s2), self.Resp(cr)])
        ref = {"title": "A Verified Paper About Topic X", "doi": "10.1000/good",
               "source": "Journal of Good Things", "year": 2026}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=lambda req, timeout=None: seq), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(False, 403, "HTTP 403")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "verified")
        self.assertIn("Semantic Scholar 交叉确认存在", r["note"])
        self.assertTrue(r["checks"]["s2"]["matched"])
        self.assertFalse(r["checks"]["doi_metadata"]["matched"])

    def test_s2_mismatch_silent_no_downgrade(self):
        # S2 登记标题不一致（实测 S2 有把正式论文记成目录页的情况）→ 静默，绝不下调
        transport_err = vr.urllib.error.URLError("reset")
        s2 = json.dumps({"title": "Some Other Unrelated Record Entirely",
                         "year": 2019}).encode()
        cr = json.dumps({"message": {}}).encode()
        seq = self._seq([transport_err, transport_err, transport_err,
                         self.Resp(s2), self.Resp(cr)])
        ref = {"title": "A Verified Paper About Topic X", "doi": "10.1000/good",
               "source": "Journal of Good Things", "year": 2026}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=lambda req, timeout=None: seq), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "verified")
        self.assertNotIn("Semantic Scholar", r["note"])
        self.assertFalse(r["checks"]["s2"]["matched"])

    def test_s2_404_silent_skip(self):
        # S2 查无/限流 → 静默跳过（收录不全，查无 ≠ 编造），不产生任何负面判据
        transport_err = vr.urllib.error.URLError("reset")
        not_found = vr.urllib.error.HTTPError("u", 404, "nf", None, None)
        cr = json.dumps({"message": {}}).encode()
        seq = self._seq([transport_err, transport_err, transport_err, not_found, self.Resp(cr)])
        ref = {"title": "A Verified Paper About Topic X", "doi": "10.1000/good",
               "source": "Journal of Good Things", "year": 2026}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=lambda req, timeout=None: seq), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "verified")
        self.assertNotIn("Semantic Scholar", r["note"])

    def test_s2_rescue_still_gated_by_fields(self):
        # S2 救回与 DOI/arXiv 救回同门槛：缺字段时降 partial，不放水 verified
        transport_err = vr.urllib.error.URLError("reset")
        s2 = json.dumps({"title": "A Verified Paper About Topic X"}).encode()
        cr = json.dumps({"message": {}}).encode()
        seq = self._seq([transport_err, transport_err, transport_err,
                         self.Resp(s2), self.Resp(cr)])
        ref = {"title": "A Verified Paper About Topic X", "doi": "10.1000/good",
               "year": 2026}  # 缺 source
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=lambda req, timeout=None: seq), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(False, 403, "HTTP 403")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "partial")

    def test_s2_not_called_when_doi_metadata_confirmed(self):
        # DOI.org 已确认时不多打 S2（省限速池）——用 MagicMock 断言 urlopen 调用次数
        csl = json.dumps({"title": ["A Verified Paper About Topic X"],
                          "issued": {"date-parts": [[2026]]}}).encode()
        cr = json.dumps({"message": {}}).encode()
        seq = self._seq([self.Resp(csl), self.Resp(cr)])
        m = unittest.mock.MagicMock(side_effect=lambda req, timeout=None: seq)
        ref = {"title": "A Verified Paper About Topic X", "doi": "10.1000/good",
               "source": "Journal of Good Things", "year": 2026}
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", m), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertEqual(r["verdict"], "verified")
        # v3.0.0 起 verified DOI 会追加 L3 引文语境调用(第 3 次外呼=S2 citations),
        # 但 S2 存在性确认(confirm)仍不调用——语义变了,断言随更新
        self.assertGreaterEqual(m.call_count, 2)
        self.assertNotIn("s2", r["checks"], "S2 存在性确认仍不调(L3 语境是另一端点)")

    def test_s2_key_header_and_param(self):
        vr._OPTS["s2_key"] = "SECRET"
        captured = {}

        def cap(req, timeout=None):
            captured["url"] = req.full_url
            captured["headers"] = dict(req.headers)
            return self.Resp(json.dumps(
                {"title": "A Verified Paper About Topic X"}).encode())

        with unittest.mock.patch.object(vr.urllib.request, "urlopen", cap):
            matched, note = vr.s2_doi_confirm("10.1000/good",
                                              "A Verified Paper About Topic X", 5.0)
        self.assertTrue(matched)
        # key 只走 x-api-key 头——query 参数会进代理/服务器日志，是泄露面
        self.assertNotIn("SECRET", captured["url"])
        self.assertEqual(captured["headers"].get("X-api-key"), "SECRET")

    def test_s2_skips_titleless_refs_without_network_call(self):
        calls = []

        def cap(req, timeout=None):
            calls.append(req.full_url)
            return self.Resp(json.dumps({"title": "x"}).encode())

        with unittest.mock.patch.object(vr.urllib.request, "urlopen", cap):
            matched, note = vr.s2_doi_confirm("10.1000/good", "   ", 5.0)
        self.assertFalse(matched)
        self.assertEqual(calls, [], "无标题引用不应发起 S2 调用（省限速池）")

    def test_s2_rate_pacing_enforced(self):
        vr._S2_LAST[0] = vr.time.time()  # 刚打过一次
        slept = []
        body = json.dumps({"title": "A Verified Paper About Topic X"}).encode()

        def cap(req, timeout=None):
            return self.Resp(body)

        orig_sleep = vr.time.sleep
        with unittest.mock.patch.object(vr.urllib.request, "urlopen", cap), \
                unittest.mock.patch.object(vr.time, "sleep",
                                           lambda s: (slept.append(s), orig_sleep(0))):
            vr.s2_doi_confirm("10.1000/good", "A Verified Paper About Topic X", 5.0)
        self.assertTrue(slept, "共享限速池下应有客户端串行化等待")
        self.assertGreaterEqual(slept[0], 1.0)

    # ---------- BibTeX 导入 ----------

    def test_bibtex_parse_basic(self):
        bib = """
@article{kim2026,
  title = {Deep Research Agents: A Survey},
  author = {Kim, Sun and Park, Ji},
  journal = {Nature Machine Intelligence},
  year = {2026},
  doi = {10.1038/s42256-026-00999-0},
  url = {https://www.nature.com/articles/x}
}
"""
        refs = vr.parse_bibtex(bib)
        self.assertEqual(len(refs), 1)
        r = refs[0]
        self.assertEqual(r["title"], "Deep Research Agents: A Survey")
        self.assertEqual(r["authors"], "Kim, Sun, Park, Ji")
        self.assertEqual(r["source"], "Nature Machine Intelligence")
        self.assertEqual(r["year"], "2026")
        self.assertEqual(r["doi"], "10.1038/s42256-026-00999-0")

    def test_bibtex_nested_braces_multiline(self):
        bib = """
@article{a1,
  title = {Study of {Deep {RL}} and
           Agents},
  journal = {J {of} Things},
  year = {2025}
}
"""
        refs = vr.parse_bibtex(bib)
        self.assertEqual(refs[0]["title"], "Study of Deep RL and Agents")
        self.assertEqual(refs[0]["source"], "J of Things")

    def test_bibtex_quoted_values_and_bare_year(self):
        bib = '@article{q1, title = "Quoted Title Here", year = 2024, doi = 10.1000/q}'
        refs = vr.parse_bibtex(bib)
        self.assertEqual(refs[0]["title"], "Quoted Title Here")
        self.assertEqual(refs[0]["year"], "2024")
        self.assertEqual(refs[0]["doi"], "10.1000/q")

    def test_bibtex_eprint_maps_to_arxiv(self):
        bib = """
@misc{ax1,
  title = {An ArXiv Preprint About Testing},
  eprint = {2401.12345},
  archivePrefix = {arXiv},
  year = {2024}
}
"""
        refs = vr.parse_bibtex(bib)
        self.assertEqual(refs[0].get("arxiv"), "2401.12345")

    def test_bibtex_url_macro_extracted(self):
        bib = """
@misc{m1,
  title = {A Web Publication About Something},
  howpublished = {\\url{https://example.com/pub}},
  year = {2026}
}
"""
        refs = vr.parse_bibtex(bib)
        self.assertEqual(refs[0]["url"], "https://example.com/pub")
        self.assertNotIn("urlhttp", refs[0].get("source", ""),
                         "\\url 宏不应污染 source 字段")

    def test_bibtex_comment_preamble_skipped(self):
        bib = """
@comment{this is not an entry}
@preamble{"\\newcommand"}
@string{js = "Journal of Things"}
@article{real1, title = {Real Entry About Things}, journal = js, year = {2025}}
"""
        refs = vr.parse_bibtex(bib)
        self.assertEqual(len(refs), 1)
        self.assertEqual(refs[0]["title"], "Real Entry About Things")

    def test_bib_end_to_end_offline(self):
        bib = """@article{g1,
  title = {Good Entry With Everything},
  journal = {Journal of Things},
  year = {2026},
  doi = {10.1000/exists}
}
@misc{bad1, title = {Bare Entry Without Any Identifier}}
"""
        p = os.path.join(self.tmp, "refs.bib")
        open(p, "w", encoding="utf-8").write(bib)
        out = os.path.join(self.tmp, "r.md")
        code = vr.main_with_args(["--refs", p, "--out", out, "--offline"])
        self.assertEqual(code, 0)
        j = json.load(open(out.rsplit(".", 1)[0] + ".json", encoding="utf-8"))
        verdicts = [r["verdict"] for r in j["results"]]
        self.assertEqual(verdicts[0], "partial", "offline 封顶 partial")
        self.assertEqual(verdicts[1], "invalid", "无标识符条目判 invalid")

    def test_bib_extensionless_autodetect(self):
        p = os.path.join(self.tmp, "refs.txt")
        open(p, "w", encoding="utf-8").write(
            "@article{x1, title = {Some Title About Things}, year = {2026}}")
        refs = vr.load_refs_file(p)
        self.assertEqual(len(refs), 1)

    def test_bib_empty_file_actionable_error(self):
        p = os.path.join(self.tmp, "empty.bib")
        open(p, "w", encoding="utf-8").write("not a bib file at all\n")
        out = os.path.join(self.tmp, "r.md")
        code = vr.main_with_args(["--refs", p, "--out", out, "--offline"])
        self.assertEqual(code, 2, "解析到 0 条应报错退出")

    def test_bib_entry_missing_fields_flagged(self):
        bib = "@article{m2, title = {Only Title Present Here}}"
        refs = vr.parse_bibtex(bib)
        miss = vr.missing_fields(refs[0])
        self.assertTrue(any("年份" in x for x in miss))
        self.assertTrue(any("来源" in x for x in miss))

    # ---------- OpenAlex key / mailto / 429 ----------

    def test_openalex_key_appended(self):
        vr._OPTS["openalex_key"] = "KEY123"
        captured = {}

        def cap(req, timeout=None):
            captured["url"] = req.full_url
            return self.Resp(json.dumps({"results": []}).encode())

        with unittest.mock.patch.object(vr.urllib.request, "urlopen", cap):
            vr.openalex_title_check("A Long Enough Title About Testing Things", 5.0)
        self.assertIn("api_key=KEY123", captured["url"])

    def test_openalex_403_gives_actionable_hint(self):
        def boom(req, timeout=None):
            raise vr.urllib.error.HTTPError("u", 403, "forbidden", None, None)

        with unittest.mock.patch.object(vr.urllib.request, "urlopen", boom):
            note = vr.openalex_title_check("A Long Enough Title About Testing Things", 5.0)
        self.assertIn("API key", note)

    def test_mailto_appended_to_doi_and_crossref(self):
        vr._OPTS["mailto"] = "lab@example.edu"
        captured = []

        def cap(req, timeout=None):
            captured.append((req.full_url, dict(req.headers)))
            if "doi.org" in req.full_url:
                return self.Resp(json.dumps(
                    {"title": ["A Verified Paper About Topic X"],
                     "issued": {"date-parts": [[2026]]}}).encode())
            return self.Resp(json.dumps({"message": {}}).encode())

        with unittest.mock.patch.object(vr.urllib.request, "urlopen", cap):
            vr.verify_one({"title": "A Verified Paper About Topic X",
                           "doi": "10.1000/good", "source": "J", "year": 2026},
                          1, False, 5.0)
        doi = [(u, h) for u, h in captured if "doi.org" in u]
        cr = [(u, h) for u, h in captured if "api.crossref.org" in u]
        # doi.org：联系方式走 UA（不加 query 参数，避免干扰 DOI 解析）
        # 注意 urllib 将头键规范化为 "User-agent"，对整个 headers 字典匹配
        self.assertTrue(doi and any("mailto:lab@example.edu" in str(h)
                                    for _, h in doi))
        self.assertFalse(any("mailto=" in u for u, _ in doi))
        # api.crossref.org：?mailto= polite pool 约定
        self.assertTrue(cr and "mailto=lab@example.edu" in cr[0][0])

    def test_bibtex_paren_entries(self):
        bib = ('@article(p1, title = {Paren Entry About Things}, year = 2025)\n'
               '@misc(p2, title = {Second Paren Entry About Things})')
        refs = vr.parse_bibtex(bib)
        self.assertEqual(len(refs), 2, "圆括号条目不得吞并后续条目")
        self.assertEqual(refs[0]["title"], "Paren Entry About Things")
        self.assertEqual(refs[1]["title"], "Second Paren Entry About Things")

    def test_429_retry_after_respected(self):
        ra = {"Retry-After": "3"}
        e429 = vr.urllib.error.HTTPError("u", 429, "slow down", ra, None)
        csl = json.dumps({"title": ["A Verified Paper About Topic X"],
                          "issued": {"date-parts": [[2026]]}}).encode()
        seq = self._seq([e429, self.Resp(csl)])
        slept = []
        orig_sleep = vr.time.sleep
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        side_effect=lambda req, timeout=None: seq), \
                unittest.mock.patch.object(vr.time, "sleep",
                                           lambda s: (slept.append(s), orig_sleep(0))):
            adj, note, matched, _csl = vr.doi_metadata_match(
                "10.1000/good", "A Verified Paper About Topic X", 2026, 5.0)
        self.assertTrue(matched)
        self.assertEqual(adj, "")
        self.assertTrue(any(abs(s - 3.0) < 0.01 for s in slept), "应按 Retry-After 退避 3 秒")

    # ---------- 投稿前结论 + auditjson ----------

    @staticmethod
    def _r(idx, verdict, **kw):
        base = {"index": idx, "title": f"Ref {idx}", "tier": "journal",
                "http_status": 200, "note": "", "needs_human_check": False}
        base.update(verdict=verdict)
        base.update(kw)
        return base

    def test_precheck_md_clean(self):
        results = [self._r(1, "verified")]
        md = vr.render_md(results, False)
        self.assertIn("✅ 投稿前结论：全部 verified——可进入投稿流程", md)

    def test_precheck_md_not_submittable(self):
        results = [self._r(1, "verified"), self._r(2, "invalid"),
                   self._r(3, "unreachable")]
        md = vr.render_md(results, False)
        self.assertIn("不建议直接提交", md)
        self.assertIn("1 条 invalid", md)
        self.assertIn("1 条 unreachable", md)

    def test_precheck_md_partial_only(self):
        results = [self._r(1, "partial")]
        md = vr.render_md(results, False)
        self.assertIn("可提交", md)
        self.assertIn("1 条 partial", md)

    def test_precheck_html_present(self):
        results = [self._r(1, "verified")]
        html = vr.render_html(results, False)
        self.assertIn("投稿前结论", html)

    def test_auditjson_export(self):
        ref = {"title": "A Verified Paper About Topic X", "doi": "10.1000/good",
               "source": "Journal of Good Things", "year": 2026}
        csl = json.dumps({"title": ["A Verified Paper About Topic X"],
                          "issued": {"date-parts": [[2026]]}}).encode()
        cr = json.dumps({"message": {}}).encode()
        with unittest.mock.patch.object(vr, "check_url",
                                        return_value=(True, 200, "GET 200")), \
                unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                           side_effect=lambda req, timeout=None: self._seq(
                                               [self.Resp(csl), self.Resp(cr)])):
            r = vr.verify_one(ref, 1, False, 5.0)
        p = os.path.join(self.tmp, "r.audit.json")
        vr.export_audit([r], p, False, "general")
        doc = json.load(open(p, encoding="utf-8"))
        self.assertIn("generated_at", doc)
        self.assertIn("checks_catalog", doc)
        self.assertTrue(doc["results"][0]["checks"]["doi_metadata"]["matched"])
        self.assertEqual(doc["results"][0]["verdict"], "verified")

    def test_checks_recorded_in_json_report(self):
        ref = {"title": "Obscure Web Title About Nothing Much At All Really",
               "url": "https://plain.example/post", "source": "blog", "year": 2026}
        body = json.dumps({"results": []}).encode()
        with unittest.mock.patch.object(vr.urllib.request, "urlopen",
                                        return_value=self.Resp(body)), \
                unittest.mock.patch.object(vr, "check_url",
                                           return_value=(True, 200, "GET 200")):
            r = vr.verify_one(ref, 1, False, 5.0)
        self.assertTrue(r["checks"]["openalex"]["ran"])
        self.assertFalse(r["checks"]["openalex"]["confirmed"])




if __name__ == "__main__":
    unittest.main(verbosity=2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
