#!/usr/bin/env python3
"""Offline business regression tests. Run from any working directory."""

import copy
import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_table as tool

ROOT = Path(__file__).resolve().parents[1]
SUCCESS = ROOT / "examples" / "success"
FAILURE = ROOT / "examples" / "failure"


class EvidenceBusinessTests(unittest.TestCase):
    def setUp(self):
        self.ledger = tool.read_ledger(SUCCESS / "evidence.json")

    def rows(self, files):
        return list(csv.DictReader(io.StringIO(files["论点与信源表.csv"].lstrip("\ufeff"))))

    def summary(self, files):
        return json.loads(files["校验汇总.json"])

    def run_cli(self, input_path, output_path, cwd):
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "scripts" / "evidence_table.py"),
             "--input", str(input_path), "--out-dir", str(output_path)],
            cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def rejects(self, ledger):
        with self.assertRaises(tool.EvidenceError):
            tool.render(ledger)

    def media_repost(self):
        # A controlled supplied-text fixture, not an observed media webpage.
        ledger = copy.deepcopy(self.ledger)
        ledger["claims"] = ledger["claims"][:1]
        ledger["sources"] = ledger["sources"][:1]
        ledger["evidence"] = ledger["evidence"][:1]
        source = ledger["sources"][0]
        source.update(publisher="受控媒体转载夹具", source_type="media", url="https://example.org/repost",
                      access_status="supplied", input_ref="in-memory-controlled-fixture",
                      access_note="受控离线回归，模拟用户给定的转载摘录；没有访问此示例域名。")
        source["trace"] = {"status": "not_attempted", "original_url": "", "attempts": []}
        return ledger

    def test_export_preserves_five_claim_source_decisions(self):
        files = tool.render(self.ledger)
        rows = self.rows(files)
        self.assertEqual(len(rows), 5)
        self.assertEqual([(r["论点ID"], r["信源ID"], r["使用决定"]) for r in rows],
                         [("C1", "S1", "cite"), ("C2", "S2", "cite"), ("C3", "S1", "reject"),
                          ("C3", "S2", "reject"), ("C3", "S3", "pending")])
        self.assertEqual(rows[0]["精确页面"], self.ledger["sources"][0]["url"])
        self.assertEqual(rows[1]["原文摘录"], self.ledger["sources"][1]["excerpt"])
        self.assertEqual(rows[0]["独立摘要"], self.ledger["sources"][0]["summary"])
        self.assertEqual(rows[1]["独立摘要"], self.ledger["sources"][1]["summary"])
        self.assertEqual(rows[0]["可引用句"], self.ledger["evidence"][0]["citation_text"])
        self.assertTrue(all(r["可引用句"] == "" for r in rows[2:]))

    def test_background_and_vendor_material_do_not_become_direct_proof(self):
        stats = self.summary(tool.render(self.ledger))
        self.assertEqual(stats["claims_total"], 3)
        self.assertEqual(stats["claims_with_usable_material"], 2)
        self.assertEqual(stats["claims_with_direct_support"], 0)
        self.assertEqual(stats["claims_without_usable_material"], ["C3"])
        self.assertEqual(stats["decisions"], {"cite": 2, "pending": 1, "reject": 2})
        self.assertEqual(stats["access_statuses"], {"fetched": 2, "supplied": 1})

    def test_checked_in_exports_are_exact_reproducible_results(self):
        for name, content in tool.render(self.ledger).items():
            self.assertEqual((SUCCESS / name).read_bytes(), content.encode("utf-8"), name)

    def test_cli_runs_outside_skill_folder_and_leaves_agent_prose_untouched(self):
        with tempfile.TemporaryDirectory(prefix="cn-source-test-") as tmp:
            folder = Path(tmp)
            output = folder / "result"
            output.mkdir()
            prose = output / "可直接使用的出处段落.md"
            prose.write_text("由Agent独立写作的正文。", encoding="utf-8")
            proc = self.run_cli(SUCCESS / "evidence.json", output, folder)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["result"], "ok")
            for name, content in tool.render(self.ledger).items():
                self.assertEqual((output / name).read_bytes(), content.encode("utf-8"))
            self.assertEqual(prose.read_text(encoding="utf-8"), "由Agent独立写作的正文。")

    def test_failure_examples_have_no_export_and_stable_actual_errors(self):
        expected = json.loads((FAILURE / "expected-errors.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(prefix="cn-source-test-") as tmp:
            for name, recorded in expected.items():
                output = Path(tmp) / name
                proc = self.run_cli(FAILURE / name, output, tmp)
                self.assertEqual(proc.returncode, recorded["exit_code"])
                self.assertEqual(proc.stderr.strip(), recorded["stderr"])
                self.assertFalse(output.exists())
                self.assertEqual(proc.stdout, "")

    def test_vendor_cannot_prove_industry_need(self):
        self.rejects(tool.read_ledger(FAILURE / "company-as-industry.json"))

    def test_vendor_cannot_support_another_products_fact(self):
        self.ledger["claims"][1]["subject"] = "另一产品"
        self.rejects(self.ledger)

    def test_vendor_statement_cannot_be_relabelled_direct(self):
        self.ledger["evidence"][1]["support"] = "direct"
        self.rejects(self.ledger)

    def test_unknown_date_remains_empty_with_an_explicit_note(self):
        row = self.rows(tool.render(self.ledger))[1]
        self.assertEqual(row["发布日期"], "")
        self.assertEqual(row["日期说明"], self.ledger["sources"][1]["publication_date_note"])
        self.ledger["sources"][1]["publication_date_note"] = ""
        self.rejects(self.ledger)

    def test_fetched_sources_accept_summary_without_redistributing_source_text(self):
        files = tool.render(self.ledger)
        rows = self.rows(files)
        self.assertEqual(rows[0]["原文摘录"], "")
        self.assertEqual(rows[1]["原文摘录"], "")
        self.assertIn("独立摘要", rows[0])
        self.assertTrue(rows[0]["独立摘要"])
        self.assertTrue(rows[1]["独立摘要"])

    def test_fetched_source_needs_excerpt_or_summary(self):
        self.ledger["sources"][0]["summary"] = ""
        self.rejects(self.ledger)

    def test_supplied_material_is_usable_with_its_offline_limit(self):
        source = self.ledger["sources"][1]
        source.update(access_status="supplied", url="", input_ref="provided-product-excerpt.txt")
        files = tool.render(self.ledger)
        self.assertEqual(self.rows(files)[1]["采集状态"], "supplied")
        self.assertIn("仅核对用户提供材料，未在线核验页面", files["未核实清单.md"])
        source["input_ref"] = ""
        self.rejects(self.ledger)

    def test_unrun_failed_and_simulated_cannot_be_cited(self):
        for state in ("unrun", "failed", "simulated"):
            with self.subTest(state=state):
                ledger = copy.deepcopy(self.ledger)
                ledger["sources"][1]["access_status"] = state
                self.rejects(ledger)

    def test_observation_states_stay_separate_and_do_not_infer_zero_citations(self):
        for state in ("unrun", "failed", "simulated"):
            ledger = copy.deepcopy(self.ledger)
            ledger["sources"][1].update(access_status=state, excerpt="")
            ledger["evidence"][1].update(use="pending", support="none", citation_text="",
                                         next_step="补充可核对的实际页面，当前状态不能计为成功观测。")
            files = tool.render(ledger)
            self.assertEqual(self.summary(files)["access_statuses"], {"fetched": 1, "supplied": 1, state: 1})
            self.assertEqual(self.rows(files)[1]["采集状态"], state)
            self.assertEqual(self.rows(files)[1]["可引用句"], "")
            self.assertNotIn("citation_count", self.summary(files))

    def test_failed_attempt_needs_actual_attempt_date(self):
        self.ledger["sources"][1].update(access_status="failed", accessed_on=None)
        self.ledger["evidence"][1].update(use="pending", citation_text="", next_step="稍后重试原页。")
        self.rejects(self.ledger)

    def test_only_media_repost_requires_original_search(self):
        ledger = self.media_repost()
        self.rejects(ledger)
        ledger["sources"][0]["trace"]["status"] = "not_found"
        self.rejects(ledger)

    def test_media_original_not_located_allows_limited_attributed_background(self):
        ledger = self.media_repost()
        ledger["sources"][0]["trace"].update(status="not_found", attempts=[{
            "query": "受控测试中的报告标题与发布者查询", "outcome": "受控失败结果：未定位原文；不代表真实联网检索。"}])
        edge = ledger["evidence"][0]
        edge.update(reason="仅据所供媒体转述作背景，未定位原文，不作为独立统计。",
                    citation_text="据所供媒体转载摘录，相关指南涉及轻量化应用；原文尚未定位。")
        files = tool.render(ledger)
        row = self.rows(files)[0]
        self.assertEqual(row["原文溯源状态"], "not_found")
        self.assertEqual(row["支撑关系"], "background")
        self.assertEqual(row["判断理由"], edge["reason"])
        self.assertIn("not_found", files["未核实清单.md"])
        self.assertEqual(self.summary(files)["claims_with_direct_support"], 0)

    def test_original_link_alone_does_not_make_repost_direct_evidence(self):
        ledger = self.media_repost()
        ledger["sources"][0]["trace"].update(status="original_found", original_url="https://example.org/original",
            attempts=[{"query": "受控链接定位", "outcome": "仅获得链接，未读取原文。"}])
        ledger["evidence"][0]["support"] = "direct"
        self.rejects(ledger)

    def test_unverified_figure_rejected_then_retained_only_as_pending(self):
        ledger = tool.read_ledger(FAILURE / "unverified-statistic.json")
        self.rejects(ledger)
        ledger["evidence"][0].update(use="pending", support="none", citation_text="",
                                     next_step="定位真实报告和原表，复核年份、单位与统计范围。")
        files = tool.render(ledger)
        row = self.rows(files)[0]
        self.assertEqual(row["使用决定"], "pending")
        self.assertEqual(row["可引用句"], "")
        self.assertEqual(row["采集状态"], "unrun")
        self.assertEqual(self.summary(files)["claims_with_usable_material"], 0)
        self.assertEqual(self.summary(files)["claims_without_usable_material"], ["C4"])

    def test_pending_and_rejected_rows_cannot_leak_ready_citation_text(self):
        for use in ("pending", "reject"):
            ledger = copy.deepcopy(self.ledger)
            ledger["evidence"][0].update(use=use, next_step="补充原文。")
            self.rejects(ledger)

    def test_future_or_noncanonical_dates_are_rejected(self):
        for value in ("2027-01-01", "2026-02-30", "20221109"):
            ledger = copy.deepcopy(self.ledger)
            ledger["sources"][0]["published_on"] = value
            self.rejects(ledger)

    def test_duplicate_ids_edges_and_unknown_references_rejected(self):
        ledger = copy.deepcopy(self.ledger)
        ledger["sources"].append(copy.deepcopy(ledger["sources"][0]))
        self.rejects(ledger)
        ledger = copy.deepcopy(self.ledger)
        ledger["evidence"].append(copy.deepcopy(ledger["evidence"][0]))
        self.rejects(ledger)
        ledger = copy.deepcopy(self.ledger)
        ledger["evidence"][0]["source_id"] = "unknown"
        self.rejects(ledger)

    def test_missing_claim_coverage_or_source_fields_rejected(self):
        ledger = copy.deepcopy(self.ledger)
        ledger["evidence"] = ledger["evidence"][:2]
        self.rejects(ledger)
        for key in ("published_on", "accessed_on", "scope", "locator"):
            ledger = copy.deepcopy(self.ledger)
            del ledger["sources"][0][key]
            self.rejects(ledger)

    def test_empty_input_and_nonobject_records_rejected(self):
        for value in (None, [], {}, {"schema_version": 1, "task": "x", "claims": [None]}):
            self.rejects(value)

    def test_wrong_enum_types_are_validation_errors(self):
        for group, key in (("claims", "kind"), ("sources", "source_type"), ("sources", "access_status"),
                           ("sources", "relationship"), ("evidence", "support"), ("evidence", "use")):
            for value in ([], {}, None, True):
                ledger = copy.deepcopy(self.ledger)
                ledger[group][0][key] = value
                self.rejects(ledger)

    def test_spreadsheet_formulas_are_escaped_without_mutating_input(self):
        self.ledger["sources"][1]["title"] = '=HYPERLINK("https://example.org","x")'
        original = copy.deepcopy(self.ledger)
        row = self.rows(tool.render(self.ledger))[1]
        self.assertEqual(row["材料标题"], "'" + original["sources"][1]["title"])
        self.assertEqual(self.ledger, original)

    def test_invalid_json_and_duplicate_json_keys_write_nothing(self):
        with tempfile.TemporaryDirectory(prefix="cn-source-test-") as tmp:
            path = Path(tmp) / "input.json"
            output = Path(tmp) / "result"
            for value in ('{broken', '{"schema_version":1,"schema_version":2}'):
                path.write_text(value, encoding="utf-8")
                proc = self.run_cli(path, output, tmp)
                self.assertEqual(proc.returncode, 2)
                self.assertFalse(output.exists())

    def test_existing_file_as_output_directory_has_clean_failure(self):
        with tempfile.TemporaryDirectory(prefix="cn-source-test-") as tmp:
            output = Path(tmp) / "result"
            output.write_text("keep", encoding="utf-8")
            proc = self.run_cli(SUCCESS / "evidence.json", output, tmp)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep")

    def test_symlink_output_target_is_not_followed(self):
        with tempfile.TemporaryDirectory(prefix="cn-source-test-") as tmp:
            folder = Path(tmp)
            output = folder / "result"
            output.mkdir()
            protected = folder / "protected"
            protected.write_text("keep", encoding="utf-8")
            (output / "论点与信源表.csv").symlink_to(protected)
            proc = self.run_cli(SUCCESS / "evidence.json", output, tmp)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(protected.read_text(encoding="utf-8"), "keep")
            self.assertFalse((output / "校验汇总.json").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
