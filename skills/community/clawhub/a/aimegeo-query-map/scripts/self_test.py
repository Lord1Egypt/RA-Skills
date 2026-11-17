#!/usr/bin/env python3
"""Business regression tests using local fixtures and isolated CLI outputs."""

import copy
import csv
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import map_queries as mapper

ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8-sig"))


class QueryMapTests(unittest.TestCase):
    def setUp(self):
        self.data = load("examples/success/input.json")

    def fail_with(self, data, code):
        with self.assertRaises(mapper.MapError) as caught:
            mapper.build_map(data)
        self.assertEqual(caught.exception.code, code)

    def record(self, status):
        return {"id": "R1", "merge_key": "free-limits", "status": status,
                "platform": "本地状态测试夹具（未查询平台）", "prompt": "免费额度是多少？",
                "answer": None, "source": "", "captured_at": None,
                "native_citations": None, "mentions": None, "error": None}

    def cli(self, source, output, cwd):
        return subprocess.run([sys.executable, str(ROOT / "scripts/map_queries.py"), str(source),
                               "--output-dir", str(output)], cwd=cwd, capture_output=True, text=True)

    def test_reference_business_counts_and_every_original_id(self):
        report = mapper.build_map(self.data)
        self.assertEqual(report["summary"], {
            "input_questions": 12, "canonical_questions": 10, "merged_questions": 2,
            "coverage": {"gap": 5, "partial": 2, "covered": 3},
            "priorities": {"P0": 2, "P1": 5, "P2": 3}})
        all_ids = [id for group in report["groups"] for id in group["source_ids"]]
        self.assertCountEqual(all_ids, [q["id"] for q in self.data["questions"]])
        self.assertEqual(len(all_ids), len(set(all_ids)))
        originals = [origin for group in report["groups"] for origin in group["origins"]]
        self.assertCountEqual(originals, [
            {"question_id": q["id"], "question": q["question"], **q["origin"]}
            for q in self.data["questions"]])

    def test_semantic_and_literal_merges_keep_provenance(self):
        groups = {g["merge_key"]: g for g in mapper.build_map(self.data)["groups"]}
        self.assertEqual(groups["free-limits"]["source_ids"], ["Q01", "Q02"])
        self.assertEqual(len(groups["free-limits"]["variants"]), 2)
        self.assertEqual([o["kind"] for o in groups["free-limits"]["origins"]], ["user_question", "agent_hypothesis"])
        self.assertEqual(groups["connect-account"]["source_ids"], ["Q03", "Q04"])
        self.assertEqual(groups["connect-account"]["question"], "如何添加第一个账号？")

    def test_repeated_wordings_remain_linked_to_each_id_and_origin(self):
        wordings = ("免费版能管理几个账号？", "免费工具支持的账号数量上限是多少？")
        for kind in sorted(mapper.ORIGINS):
            reports, csv_outputs = [], []
            for pattern in ((0, 0, 1), (0, 1, 1)):
                with self.subTest(kind=kind, pattern=pattern):
                    data = copy.deepcopy(self.data)
                    data["questions"] = []
                    for index, wording in enumerate(pattern, 1):
                        question = copy.deepcopy(self.data["questions"][0])
                        question.update(id=f"Q{index:02}", question=wordings[wording],
                                        origin={"kind": kind, "source": "同一份本地回归资料，非平台实测"})
                        data["questions"].append(question)
                    report = mapper.build_map(data)
                    group = report["groups"][0]
                    self.assertEqual(group["source_ids"], ["Q01", "Q02", "Q03"])
                    self.assertEqual(group["variants"], list(wordings))
                    reports.append(report)
                    csv_outputs.append(mapper.render_csv(report))
                    self.assertEqual(group["origins"], [
                        {"question_id": q["id"], "question": q["question"], **q["origin"]}
                        for q in data["questions"]])
            self.assertEqual(reports[0]["summary"], reports[1]["summary"])
            self.assertNotEqual(reports[0], reports[1])
            self.assertNotEqual(csv_outputs[0], csv_outputs[1])

    def test_original_text_and_distinct_sources_survive_normalization(self):
        data = copy.deepcopy(self.data)
        data["questions"] = []
        texts = ("  Ａ账号，怎么添加？\n", "A账号怎么添加", "A账号怎么添加")
        for index, (text, kind) in enumerate(zip(texts, sorted(mapper.ORIGINS)), 1):
            question = copy.deepcopy(self.data["questions"][0])
            question.update(id=f"Q{index:02}", question=text,
                            origin={"kind": kind, "source": f"本地原始记录第{index}条"})
            data["questions"].append(question)
        self.assertEqual(len({mapper.normalized(text) for text in texts}), 1)
        group = mapper.build_map(data)["groups"][0]
        self.assertEqual(group["origins"], [
            {"question_id": q["id"], "question": q["question"], **q["origin"]}
            for q in data["questions"]])
        self.assertEqual(group["variants"], list(texts[:2]))

    def test_same_theme_different_answer_stays_separate(self):
        groups = {g["merge_key"]: g for g in mapper.build_map(self.data)["groups"]}
        self.assertEqual(groups["team-permissions"]["theme"], groups["revoke-access"]["theme"])
        self.assertNotEqual(groups["team-permissions"]["scope"], groups["revoke-access"]["scope"])
        self.assertEqual(groups["team-permissions"]["source_ids"], ["Q08"])
        self.assertEqual(groups["revoke-access"]["source_ids"], ["Q09"])

    def test_missing_facts_block_production_and_covered_items_are_reused(self):
        groups = {g["merge_key"]: g for g in mapper.build_map(self.data)["groups"]}
        self.assertEqual({g["merge_key"] for g in groups.values() if g["priority"] == "P0"}, {"compare-manual", "pilot-checklist"})
        self.assertFalse(groups["free-limits"]["facts_ready"])
        self.assertEqual(groups["free-limits"]["priority"], "P1")
        self.assertEqual(groups["connect-account"]["priority"], "P2")
        self.data["questions"][2]["facts"][0].update(status="missing", source="")
        self.data["questions"][3]["facts"][0].update(status="missing", source="")
        changed = {g["merge_key"]: g for g in mapper.build_map(self.data)["groups"]}
        self.assertEqual(changed["connect-account"]["priority"], "P1")

    def test_manual_comparison_stays_with_the_provided_recording_information(self):
        question = next(q for q in self.data["questions"] if q["id"] == "Q10")
        self.assertIn("三人团队目前用表格记录账号与发布计划", self.data["business"]["description"])
        self.assertEqual(question["scope"], "表格记录事项与工具账号及计划信息对照")
        self.assertEqual(question["facts"][0]["need"], "表格目前记录账号与发布计划")
        self.assertEqual(question["facts"][1]["source"], "教程 A1、A3 正文")
        group = next(g for g in mapper.build_map(self.data)["groups"] if g["merge_key"] == "compare-manual")
        self.assertTrue(group["facts_ready"])
        self.assertEqual(group["priority"], "P0")
        self.assertEqual(group["formats"], ["账号与发布计划信息对照表"])
        plan = (ROOT / "examples/success/output/本周优先选题.md").read_text(encoding="utf-8")
        comparison = plan.split("1. **Q10", 1)[1].split("2. **Q11", 1)[0]
        self.assertIn("没有现有表格的具体字段、操作步骤或耗时资料", comparison)
        self.assertIn("不延伸比较素材迁移、定时执行或回执检查流程", comparison)
        self.assertNotIn("逐步比较账号管理、素材迁移、定时任务和回执检查", comparison)

    def test_partial_inventory_does_not_claim_new_gaps(self):
        self.data["business"]["inventory_status"] = "partial"
        report = mapper.build_map(self.data)
        self.assertNotIn("gap", report["summary"]["coverage"])
        self.assertEqual(report["summary"]["coverage"]["unknown"], 5)
        self.assertEqual(report["summary"]["coverage"]["covered"], 3)
        self.assertNotIn("P0", report["summary"]["priorities"])

    def test_brief_only_map_is_usable_and_honest(self):
        report = mapper.build_map(load("examples/minimal-input.json"))
        self.assertGreaterEqual(len(report["groups"]), 5)
        self.assertGreaterEqual(len({g["intent"] for g in report["groups"]}), 3)
        for group in report["groups"]:
            self.assertEqual(group["coverage"], "unknown")
            self.assertEqual(group["priority"], "P1")
            self.assertIsNone(group["search_volume"])
            self.assertEqual(group["answer_statuses"], ["not_run"])
            self.assertEqual(group["origins"][0]["kind"], "agent_hypothesis")
            self.assertTrue(group["facts"] and group["formats"] and group["next_steps"])

    def test_only_titles_cannot_prove_coverage(self):
        self.data["business"]["inventory_status"] = "partial"
        self.data["articles"][0].update(material="title", text="")
        self.fail_with(self.data, "TITLE_ONLY_COVERAGE")
        for q in self.data["questions"]:
            for link in q["article_links"]:
                if link["article_id"] == "A1":
                    link.update(coverage="unknown", evidence="", reason="只有标题，没有正文")
        group = next(g for g in mapper.build_map(self.data)["groups"] if g["merge_key"] == "connect-account")
        self.assertEqual((group["coverage"], group["priority"]), ("unknown", "P1"))

    def test_reviewed_inventory_rejects_excerpts(self):
        self.data["articles"][0]["material"] = "excerpt"
        self.fail_with(self.data, "INVENTORY_STATE")

    def test_full_coverage_requires_literal_evidence(self):
        self.data["questions"][2]["article_links"][0]["evidence"] = "此句未出现在教程中"
        self.fail_with(self.data, "COVERAGE_EVIDENCE")

    def test_unknown_article_is_not_silently_ignored(self):
        self.data["questions"][2]["article_links"][0]["article_id"] = "A999"
        self.fail_with(self.data, "UNKNOWN_ARTICLE")

    def test_cross_audience_failure_fixture(self):
        self.fail_with(load("examples/failure/cross-audience.json"), "MERGE_CONFLICT")

    def test_conflicting_intent_or_scope_is_not_merged(self):
        for field, value in (("intent", "information"), ("scope", "撤销账号授权")):
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data["questions"][1][field] = value
                self.fail_with(data, "MERGE_CONFLICT")

    def test_literal_duplicate_split_is_reported(self):
        self.data["questions"][3]["merge_key"] = "another-group"
        self.fail_with(self.data, "DUPLICATE_SPLIT")

    def test_conflicting_fact_states_require_resolution(self):
        self.data["questions"][1]["facts"][0].update(status="available", source="另一份资料")
        self.fail_with(self.data, "FACT_CONFLICT")

    def test_missing_fact_cannot_have_an_available_source(self):
        self.data["questions"][0]["facts"][0]["source"] = "并未读取的规则"
        self.fail_with(self.data, "FACT_STATE")

    def test_question_and_article_ids_are_unique(self):
        data = copy.deepcopy(self.data)
        data["questions"][1]["id"] = data["questions"][0]["id"]
        self.fail_with(data, "DUPLICATE_ID")
        self.data["articles"].append(copy.deepcopy(self.data["articles"][0]))
        self.fail_with(self.data, "DUPLICATE_ID")

    def test_simulated_unrun_and_failed_records_remain_distinct(self):
        records = []
        for index, status in enumerate(("simulated", "not_run", "query_failed")):
            record = self.record(status)
            record["id"] = f"R{index}"
            if status == "simulated":
                record["answer"] = "假设回答可能要求先确认免费权益。"
            elif status == "query_failed":
                record["error"] = "测试夹具中的失败说明，不是实际平台查询"
            records.append(record)
        self.data["answer_records"] = records
        report = mapper.build_map(self.data)
        group = next(g for g in report["groups"] if g["merge_key"] == "free-limits")
        self.assertEqual(group["answer_statuses"], ["simulated", "not_run", "query_failed"])
        for record in report["answer_records"]:
            self.assertIsNone(record["native_citations"])
            self.assertIsNone(record["mentions"])
        self.assertIsNone(report["groups"][0]["search_volume"])

    def test_nonobserved_citations_cannot_be_zeroed(self):
        for status in ("simulated", "not_run", "query_failed"):
            with self.subTest(status=status):
                record = self.record(status)
                record["native_citations"] = []
                self.data["answer_records"] = [record]
                self.fail_with(self.data, "RECORD_STATE")

    def test_observed_record_preserves_unknown_vs_inspected_empty(self):
        for citations in (None, []):
            record = self.record("observed")
            record.update(answer="本地测试工具用于内容管理。", source="本地测试记录，无网络测量", captured_at="2026-10-19T10:00:00+08:00", native_citations=citations, mentions=["本地测试工具"])
            self.data["answer_records"] = [record]
            result = mapper.build_map(self.data)["answer_records"][0]
            self.assertEqual(result["native_citations"], citations)
            self.assertEqual(result["mentions"], ["本地测试工具"])

    def test_observed_record_needs_time_and_literal_mentions(self):
        record = self.record("observed")
        record.update(answer="测试原文", source="本地夹具")
        self.data["answer_records"] = [record]
        self.fail_with(self.data, "RECORD_STATE")
        record["captured_at"] = "2026-10-19T10:00:00"
        self.fail_with(self.data, "RECORD_STATE")
        record.update(captured_at="2026-10-19T10:00:00+08:00", mentions=["未出现的品牌"])
        self.fail_with(self.data, "MENTION_EVIDENCE")

    def test_native_citation_url_validation(self):
        record = self.record("observed")
        record.update(answer="测试原文", source="本地夹具", captured_at="2026-10-19T10:00:00Z", native_citations=[{"url": "javascript:alert(1)", "label": "测试标签"}])
        self.data["answer_records"] = [record]
        self.fail_with(self.data, "CITATION_URL")
        record["native_citations"][0]["url"] = "https://example.org/reference"
        self.assertEqual(mapper.build_map(self.data)["answer_records"][0]["native_citations"], record["native_citations"])

    def test_no_search_volume_is_invented_or_silently_imported(self):
        report = mapper.build_map(self.data)
        self.assertTrue(all(g["search_volume"] is None for g in report["groups"]))
        self.data["questions"][0]["search_volume"] = 10000
        self.fail_with(self.data, "SCHEMA")

    def test_invalid_root_and_empty_questions_fail(self):
        for invalid in ([], {}, {**self.data, "questions": []}, {**self.data, "questions": ["not an object"]}):
            with self.subTest(invalid_type=type(invalid).__name__):
                self.fail_with(invalid, "SCHEMA")

    def test_csv_roundtrip_and_formula_escaping(self):
        for prefix in ("=", "+", "-", "@", "\t", "\r", "\n", "  ="):
            self.assertTrue(mapper.safe_cell(prefix + "formula").startswith("'"))
        self.data["questions"][0]["question"] = '=HYPERLINK("https://example.org", "演示")\n第二行'
        report = mapper.build_map(self.data)
        rows = list(csv.DictReader(io.StringIO(mapper.render_csv(report))))
        self.assertEqual(len(rows), 10)
        target = next(r for r in rows if r["归并键"] == "free-limits")
        self.assertTrue(target["用户问题"].startswith("'="))
        self.assertIn("\n第二行", target["用户问题"])
        self.assertEqual(target["原题ID"], "Q01；Q02")
        self.assertIn('Q01 输入原题（演示输入的问题清单第1条）：=HYPERLINK("https://example.org", "演示")\n第二行', target["问题依据"])
        self.assertIn("Q02 待验证假设（Agent 根据演示业务资料推导，需求待验证）：免费多账号工具的账号数量和平台限制是什么？", target["问题依据"])
        self.assertEqual(target["搜索量"], "未知（未提供测量）")

    def test_success_cli_is_portable_and_matches_saved_results(self):
        with tempfile.TemporaryDirectory(prefix="query-map-test-") as tmp:
            result = self.cli(ROOT / "examples/success/input.json", Path(tmp) / "out", tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            self.assertEqual(json.loads(result.stdout)["canonical_questions"], 10)
            actual = Path(tmp) / "out"
            self.assertTrue((actual / mapper.CSV_NAME).read_bytes().startswith(b"\xef\xbb\xbf"))
            self.assertEqual(json.loads((actual / mapper.AUDIT_NAME).read_text()), load("examples/success/output/map-audit.json"))
            with (actual / mapper.CSV_NAME).open(encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream))
            with (ROOT / "examples/success/output" / mapper.CSV_NAME).open(encoding="utf-8-sig", newline="") as stream:
                self.assertEqual(rows, list(csv.reader(stream)))

    def test_failure_cli_returns_saved_error_and_writes_nothing(self):
        with tempfile.TemporaryDirectory(prefix="query-map-test-") as tmp:
            output = Path(tmp) / "failed"
            result = self.cli(ROOT / "examples/failure/cross-audience.json", output, tmp)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertEqual(json.loads(result.stderr), load("examples/failure/error.json"))
            self.assertFalse(output.exists())

    def test_existing_output_is_not_overwritten(self):
        with tempfile.TemporaryDirectory(prefix="query-map-test-") as tmp:
            output = Path(tmp) / "out"
            output.mkdir()
            target = output / mapper.CSV_NAME
            target.write_bytes(b"keep this previous result")
            result = self.cli(ROOT / "examples/success/input.json", output, tmp)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)["code"], "OUTPUT_EXISTS")
            self.assertEqual(target.read_bytes(), b"keep this previous result")
            self.assertFalse((output / mapper.AUDIT_NAME).exists())

    def test_malformed_json_duplicate_keys_and_missing_input_fail(self):
        with tempfile.TemporaryDirectory(prefix="query-map-test-") as tmp:
            source = Path(tmp) / "input.json"
            output = Path(tmp) / "out"
            for raw in ('{"business":', '{"business": {}, "business": {}}'):
                source.write_text(raw)
                result = self.cli(source, output, tmp)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(json.loads(result.stderr)["ok"])
                self.assertFalse(output.exists())
            result = self.cli(Path(tmp) / "missing.json", output, tmp)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())

    def test_unprovided_inventory_cannot_hide_supplied_articles(self):
        self.data["business"]["inventory_status"] = "unprovided"
        self.fail_with(self.data, "INVENTORY_STATE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
