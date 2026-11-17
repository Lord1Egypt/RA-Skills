#!/usr/bin/env python3
"""Offline business regressions; no icon, license-file, network or host checks."""

import copy
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
import repair_bundle as bundle

ROOT = Path(__file__).resolve().parents[1]


def fixture(name="success"):
    return bundle.load(ROOT / "examples" / name / "input.json")


def controlled_actual():
    """Construct field-state regression data, not evidence of a live query."""
    data = fixture()
    data["mode"] = "case"
    for source in data["sources"]:
        source["provenance"] = "user_provided"
    for observation in data["observations"]:
        observation["status"] = "provided"
    return data


class RepairTests(unittest.TestCase):
    def assert_invalid(self, data, code):
        with self.assertRaises(bundle.Invalid) as caught:
            bundle.validate(data)
        self.assertEqual(caught.exception.code, code)

    def test_success_has_three_distinct_decisions_without_sentiment_score(self):
        result = bundle.validate(fixture())
        self.assertEqual(result["claims"], 3)
        self.assertEqual(result["verdict_counts"], {"accurate": 1, "contradicted": 1, "outdated": 1})
        self.assertEqual(result["baseline"], {
            "actual_ai_answers": 0, "status_counts": {"simulated": 2},
            "native_citations": None, "citation_coverage": "no_actual_answers"})

    def test_exported_csv_preserves_claim_evidence_and_real_limit(self):
        data = fixture()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "delivery"
            bundle.export(data, output)
            with (output / bundle.FILES[0]).open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual([r["判定"] for r in rows], ["已过时", "与当前事实不符", "事实正确"])
            self.assertEqual([r["公开答复"] for r in rows], [c["public_answer"] for c in data["claims"]])
            self.assertEqual(rows[2]["原话摘录"], "switching is manual; automatic account rotation is not supported")
            self.assertEqual(rows[2]["修改位置"], "英文账号帮助中的切换步骤与账号FAQ")
            self.assertIn("historical_support", rows[0]["事实证据"])
            faq = (output / bundle.FILES[1]).read_text(encoding="utf-8")
            self.assertIn(data["claims"][2]["public_answer"], faq)
            plan = json.loads((output / bundle.FILES[2]).read_text(encoding="utf-8"))
            self.assertEqual(plan["baseline_observations"], data["observations"])
            for planned, original in zip(plan["questions"], data["retests"]):
                self.assertEqual(planned["question"], original["question"])
                self.assertEqual((planned["status"], planned["answer"], planned["native_citations"]),
                                 ("not_run", None, None))

    def test_insufficient_facts_remain_unconfirmed_and_request_key_information(self):
        data = fixture("insufficient-facts")
        result = bundle.validate(data)
        self.assertEqual(result["verdict_counts"], {"unconfirmed": 1})
        self.assertEqual(data["sources"], [])
        self.assertEqual(data["claims"][0]["evidence"], [])
        self.assertEqual(data["retests"][0]["kind"], "follow_up")
        self.assertEqual(len(data["claims"][0]["needed_information"]), 2)
        self.assertIsNone(result["baseline"]["native_citations"])

    def test_unconfirmed_requires_actionable_missing_information(self):
        data = fixture("insufficient-facts")
        data["claims"][0]["needed_information"] = []
        self.assert_invalid(data, "invalid_list")

    def test_one_supplied_customer_question_is_not_an_ai_measurement(self):
        data = fixture("insufficient-facts")
        data["mode"] = "case"
        data["observations"][0]["status"] = "provided"
        result = bundle.validate(data)
        self.assertEqual(result["verdict_counts"], {"unconfirmed": 1})
        self.assertEqual(result["baseline"], {
            "actual_ai_answers": 0, "status_counts": {"provided": 1},
            "native_citations": None, "citation_coverage": "no_actual_answers"})

    def test_no_evidence_cannot_become_positive_correction(self):
        data = fixture("failure")
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "must-not-exist"
            with self.assertRaises(bundle.Invalid) as caught:
                bundle.export(data, output)
            self.assertEqual(caught.exception.as_dict(), bundle.load(ROOT / "examples/failure/expected-error.json"))
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_outdated_requires_history_and_current_contradiction(self):
        for remaining in ([0], [1]):
            with self.subTest(remaining=remaining):
                data = fixture()
                data["claims"][0]["evidence"] = [data["claims"][0]["evidence"][i] for i in remaining]
                self.assert_invalid(data, "evidence_required")

    def test_correct_limitation_requires_current_support(self):
        data = fixture()
        data["claims"][2]["evidence"][0]["relation"] = "contradicts"
        self.assert_invalid(data, "evidence_required")

    def test_unknown_source_is_not_accepted(self):
        data = fixture()
        data["claims"][0]["evidence"][0]["source_id"] = "missing"
        self.assert_invalid(data, "unknown_source")

    def test_fabricated_answer_quote_is_rejected(self):
        data = fixture()
        data["claims"][0]["quote"] = "青禾拥有百万客户"
        self.assert_invalid(data, "quote_mismatch")

    def test_fabricated_evidence_quote_is_rejected(self):
        data = fixture()
        data["claims"][0]["evidence"][1]["quote"] = "青禾支持自动轮换账号。"
        self.assert_invalid(data, "evidence_quote_mismatch")

    def test_current_evidence_cannot_be_expired_or_future(self):
        for key, value, code in (("effective_to", "2026-10-18", "expired_evidence"),
                                 ("effective_from", "2026-10-20", "future_evidence")):
            with self.subTest(key=key):
                data = fixture()
                data["sources"][0][key] = value
                self.assert_invalid(data, code)

    def test_current_statement_does_not_require_invented_start_date(self):
        data = fixture()
        data["sources"][0]["effective_from"] = None
        self.assertEqual(bundle.validate(data)["verdict_counts"]["contradicted"], 1)

    def test_historical_evidence_cannot_start_in_the_future(self):
        data = fixture()
        data["sources"][2].update(effective_from="2026-10-20", effective_to=None)
        self.assert_invalid(data, "future_evidence")

    def test_conflicting_current_facts_require_unconfirmed(self):
        data = fixture()
        source = copy.deepcopy(data["sources"][1])
        source.update(id="F4", title="冲突费用版本的账号说明（测试）", content="青禾当前只支持一个账号。")
        data["sources"].append(source)
        data["claims"][0]["evidence"].append({
            "source_id": "F4", "quote": "青禾当前只支持一个账号。", "relation": "supports"})
        self.assert_invalid(data, "conflicting_evidence")
        data["claims"][0].update(verdict="unconfirmed", needed_information=["两个当前说明各自适用的套餐或版本"])
        data["claims"][0]["public_answer"] = "当前资料互相冲突，尚不能确认适用版本的账号上限。请先核对两个说明的套餐与版本。"
        self.assertEqual(bundle.validate(data)["verdict_counts"]["unconfirmed"], 1)

    def test_simulated_answers_cannot_become_live_measurements(self):
        data = fixture()
        data["observations"][0]["status"] = "provided"
        self.assert_invalid(data, "simulation_as_actual")
        data = controlled_actual()
        data["sources"][0]["provenance"] = "illustrative"
        self.assert_invalid(data, "illustrative_evidence")

    def test_unknown_citations_are_null_and_not_zero(self):
        data = controlled_actual()
        summary = bundle.validate(data)["baseline"]
        self.assertEqual(summary["actual_ai_answers"], 2)
        self.assertIsNone(summary["native_citations"])
        self.assertEqual(summary["citation_coverage"], "incomplete")
        data["observations"][0]["native_citations"] = []
        self.assert_invalid(data, "unknown_citations")

    def test_only_complete_actual_capture_can_report_zero_citations(self):
        data = controlled_actual()
        for obs in data["observations"]:
            obs.update(citation_capture="complete", native_citations=[])
        summary = bundle.validate(data)["baseline"]
        self.assertEqual(summary["native_citations"], 0)
        self.assertEqual(summary["citation_coverage"], "complete")

    def test_partial_citations_do_not_become_complete_total(self):
        data = controlled_actual()
        data["observations"][0].update(citation_capture="partial", native_citations=[
            {"label": "controlled test citation", "url": "https://example.invalid/native-reference"}])
        summary = bundle.validate(data)["baseline"]
        self.assertIsNone(summary["native_citations"])
        data["observations"][0]["native_citations"] = []
        self.assert_invalid(data, "invalid_list")

    def test_failed_unrun_and_simulated_queries_are_separate(self):
        data = controlled_actual()
        for id, status, text, error in (("O3", "not_run", None, None),
                                         ("O4", "query_failed", None, "超时：未取得回答"),
                                         ("O5", "simulated", "测试模拟回答", None)):
            obs = copy.deepcopy(data["observations"][0])
            obs.update(id=id, status=status, text=text, error=error)
            data["observations"].append(obs)
        summary = bundle.validate(data)["baseline"]
        self.assertEqual(summary["actual_ai_answers"], 2)
        self.assertEqual(summary["status_counts"], {"provided": 2, "not_run": 1, "query_failed": 1, "simulated": 1})
        self.assertIsNone(summary["native_citations"])
        data["observations"][3]["native_citations"] = []
        self.assert_invalid(data, "unknown_citations")

    def test_failed_query_cannot_supply_an_answer_or_claim(self):
        data = controlled_actual()
        data["observations"][0].update(status="query_failed", error="timeout")
        self.assert_invalid(data, "invalid_state")
        data["observations"][0]["text"] = None
        self.assert_invalid(data, "quote_mismatch")

    def test_collected_answer_needs_collection_context(self):
        data = controlled_actual()
        data["observations"][0]["status"] = "collected"
        self.assert_invalid(data, "collection_metadata")
        data["observations"][0].update(platform="受控状态测试", observed_at="2026-10-19")
        self.assertEqual(bundle.validate(data)["baseline"]["status_counts"], {"collected": 1, "provided": 1})

    def test_same_question_cannot_be_rewritten_or_invented(self):
        data = fixture()
        data["retests"][0]["question"] = "青禾是最好的免费工具吗？"
        self.assert_invalid(data, "same_question_mismatch")
        data = fixture("insufficient-facts")
        data["retests"][0]["kind"] = "same_question"
        self.assert_invalid(data, "same_question_mismatch")

    def test_every_claim_needs_verification(self):
        data = fixture()
        data["retests"] = data["retests"][:1]
        self.assert_invalid(data, "retest_coverage")

    def test_no_silent_sentiment_or_unsupported_result_fields(self):
        data = fixture()
        data["sentiment_score"] = 10
        self.assert_invalid(data, "invalid_fields")

    def test_csv_formula_is_escaped_without_damaging_authored_faq(self):
        data = fixture("insufficient-facts")
        data["observations"][0]["text"] = '=HYPERLINK("test")'
        data["claims"][0]["quote"] = data["observations"][0]["text"]
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "delivery"
            bundle.export(data, output)
            with (output / bundle.FILES[0]).open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["原话摘录"], "'" + data["observations"][0]["text"])
            self.assertEqual(row["公开答复"], data["claims"][0]["public_answer"])

    def test_existing_delivery_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "existing"
            output.mkdir()
            marker = output / "keep.txt"
            marker.write_text("existing user delivery", encoding="utf-8")
            with self.assertRaises(bundle.Invalid) as caught:
                bundle.export(fixture(), output)
            self.assertEqual(caught.exception.code, "output_exists")
            self.assertEqual(marker.read_text(encoding="utf-8"), "existing user delivery")
            self.assertEqual(list(output.iterdir()), [marker])

    def test_cli_rejects_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "ambiguous.json"
            path.write_text('{"schema_version":1,"schema_version":2}', encoding="utf-8")
            run = subprocess.run([sys.executable, str(ROOT / "scripts/repair_bundle.py"),
                                  "check", "--input", str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(json.loads(run.stderr)["code"], "duplicate_key")
            self.assertEqual(run.stdout, "")

    def test_checked_in_outputs_equal_actual_export(self):
        for name in ("success", "insufficient-facts"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / "delivery"
                bundle.export(fixture(name), output)
                for filename in bundle.FILES:
                    self.assertEqual((output / filename).read_bytes(),
                                     (ROOT / "examples" / name / "output" / filename).read_bytes())

    def test_relocated_cli_works_outside_skill_without_host_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            relocated = Path(temporary) / "standalone"
            shutil.copytree(ROOT / "scripts", relocated / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(ROOT / "examples", relocated / "examples")
            output = Path(temporary) / "outside-delivery"
            run = subprocess.run([sys.executable, str(relocated / "scripts/repair_bundle.py"), "export",
                                  "--input", str(relocated / "examples/success/input.json"),
                                  "--output-dir", str(output)], cwd=temporary, capture_output=True, text=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(json.loads(run.stdout)["verdict_counts"], {"accurate": 1, "contradicted": 1, "outdated": 1})
            plan = json.loads((output / bundle.FILES[2]).read_text(encoding="utf-8"))
            self.assertIsNone(plan["baseline_summary"]["native_citations"])
            self.assertEqual(plan["questions"][1]["status"], "not_run")
            failure_output = Path(temporary) / "rejected-delivery"
            failed = subprocess.run([sys.executable, str(relocated / "scripts/repair_bundle.py"), "export",
                                     "--input", str(relocated / "examples/failure/input.json"),
                                     "--output-dir", str(failure_output)], cwd=temporary, capture_output=True, text=True)
            self.assertEqual(failed.returncode, 2)
            self.assertEqual(json.loads(failed.stderr)["code"], "evidence_required")
            self.assertFalse(failure_output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
