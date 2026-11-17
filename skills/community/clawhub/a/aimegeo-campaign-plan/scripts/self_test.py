#!/usr/bin/env python3
"""Offline business regressions. Controlled fixtures are not live GEO evidence."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from check_campaign import validate


ROOT = Path(__file__).resolve().parent.parent
GOOD = ROOT / "examples" / "qinghe" / "campaign.json"
BAD = ROOT / "examples" / "failure" / "campaign.json"


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(GOOD.read_text(encoding="utf-8"))

    def reject(self, data, code):
        result = validate(data)
        self.assertFalse(result["ok"], result)
        self.assertIn(code, {x["code"] for x in result["errors"]}, result)
        return result

    def cli(self, path, cwd=None, script=None):
        proc = subprocess.run([sys.executable, str(script or ROOT / "scripts" / "check_campaign.py"), str(path)],
                              cwd=cwd, capture_output=True, text=True, encoding="utf-8", check=False)
        self.assertEqual(proc.stderr, "", proc.stderr)
        return proc.returncode, json.loads(proc.stdout)

    def test_qinghe_business_result(self):
        result = validate(self.data)
        self.assertTrue(result["ok"], result)
        summary = result["summary"]
        self.assertEqual((summary["topics"], summary["drafts"], summary["shots"], summary["staff"]), (9, 9, 7, 2))
        self.assertEqual(summary["scheduled_person_minutes"], 48)
        person_minutes = {p["id"]: sum((s["end_minute"] - s["start_minute"]) for s in self.data["shots"] if p["id"] in s["people"]) for p in self.data["event"]["staff"]}
        self.assertEqual(person_minutes, {"A": 16, "B": 32})
        self.assertEqual(summary["time_raw"], "下周")
        self.assertTrue(all(n == 1 for row in summary["coverage"].values() for n in row.values()))
        self.assertEqual(summary["draft_statuses"], {"ready_for_review": 3, "awaiting_facts": 0, "awaiting_capture": 6})
        self.assertEqual(summary["pending_fact_keys"], ["audience", "booth", "business", "event_dates", "exhibition_name", "goal"])
        self.assertEqual(summary["geo"]["observed_answers"], 0)
        self.assertIsNone(summary["geo"]["native_citations"])
        self.assertIsNone(summary["geo"]["brand_mentions"])

    def test_original_request_needs_no_profile_or_drafts(self):
        self.data["scope"]["mode"] = "plan"
        self.data["scope"].pop("authorization")
        self.data["drafts"] = []
        result = validate(self.data)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["summary"]["drafts"], 0)

    def test_full_batch_has_no_three_item_limit(self):
        self.assertEqual(len(self.data["drafts"]), 9)
        self.assertTrue(validate(self.data)["ok"])
        self.data["drafts"] = self.data["drafts"][:3]
        self.reject(self.data, "DRAFT_COVERAGE")

    def test_four_selected_ids_are_all_written(self):
        self.data["scope"]["mode"] = "selected"
        self.data["scope"]["selected_ids"] = ["01", "02", "03", "04"]
        self.data["drafts"] = self.data["drafts"][:4]
        result = validate(self.data)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["summary"]["drafts"], 4)
        self.data["drafts"].append(copy.deepcopy(self.data["drafts"][0]))
        self.reject(self.data, "DUPLICATE_ID")

    def test_unselected_draft_is_not_silently_accepted(self):
        self.data["scope"]["mode"] = "selected"
        self.data["scope"]["selected_ids"] = ["01"]
        self.reject(self.data, "DRAFT_COVERAGE")

    def test_time_original_is_preserved(self):
        self.data["event"]["time"]["raw"] = "这周末"
        self.reject(self.data, "TIME_RAW_CHANGED")

    def test_exact_dates_need_separate_evidence(self):
        self.data["event"]["time"].update(start_date="2026-10-27", end_date="2026-10-29")
        self.reject(self.data, "DATE_WITHOUT_EVIDENCE")
        self.data["facts"][5].update(status="confirmed", value={"start_date": "2026-10-27", "end_date": "2026-10-29"},
                                     source={"ref": "controlled-test", "excerpt": "测试日期证据：2026-10-27 至 2026-10-29"})
        self.assertTrue(validate(self.data)["ok"])

    def test_invalid_date_range_rejected_even_with_matching_fact(self):
        dates = {"start_date": "2026-10-29", "end_date": "2026-10-27"}
        self.data["event"]["time"].update(dates)
        self.data["facts"][5].update(status="confirmed", value=dates, source={"ref": "controlled-test", "excerpt": "逆序测试日期"})
        self.reject(self.data, "DATE_RANGE")

    def test_staff_cannot_be_invented(self):
        self.data["event"]["staff"].append({"id": "C", "role": "虚增人员的失败测试"})
        self.reject(self.data, "STAFF_COUNT")

    def test_overlapping_same_person_is_a_conflict(self):
        self.data["shots"][1]["start_minute"] = 3
        self.reject(self.data, "SHOOT_CONFLICT")

    def test_back_to_back_shots_are_valid(self):
        self.assertEqual(self.data["shots"][0]["end_minute"], self.data["shots"][1]["start_minute"])
        self.assertTrue(validate(self.data)["ok"])

    def test_different_people_may_shoot_in_parallel(self):
        self.data["shots"][0]["people"] = ["A"]
        self.data["shots"][1]["people"] = ["B"]
        self.data["shots"][1]["start_minute"] = 0
        self.assertTrue(validate(self.data)["ok"])

    def test_boolean_is_not_a_minute(self):
        self.data["shots"][0]["end_minute"] = True
        self.reject(self.data, "SHOT_INTERVAL")

    def test_shot_must_link_back_to_topic(self):
        self.data["topics"][3]["shot_ids"].remove("S01")
        self.reject(self.data, "SHOT_LINK")

    def test_requested_coverage_cannot_disappear(self):
        self.data["topics"].pop()
        self.reject(self.data, "COVERAGE")

    def test_user_can_request_one_channel_only(self):
        self.data["scope"]["channels"] = ["public"]
        self.data["scope"]["mode"] = "plan"
        self.data["drafts"] = []
        self.data["shots"] = []
        self.data["topics"] = [t for t in self.data["topics"] if t["channel"] == "public"]
        for t in self.data["topics"]:
            t["shot_ids"] = []
        result = validate(self.data)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["summary"]["topics"], 3)

    def test_missing_customer_story_cannot_be_cited_as_fact(self):
        self.data["facts"].append({"id": "F11", "key": "customer_story", "status": "missing", "value": None, "source": None})
        self.data["drafts"][0]["fact_ids"].append("F11")
        self.reject(self.data, "UNKNOWN_REF")
        self.data["drafts"][0]["fact_ids"].remove("F11")
        result = validate(self.data)
        self.assertTrue(result["ok"], result)
        self.assertIn("customer_story", result["summary"]["pending_fact_keys"])

    def test_confirmed_fact_needs_a_source(self):
        self.data["facts"][0]["source"] = None
        self.reject(self.data, "SCHEMA")

    def test_missing_fact_blocks_ready_draft(self):
        self.data["drafts"][0]["required_fact_ids"] = ["F07"]
        self.reject(self.data, "DRAFT_FACT_GATE")
        self.data["drafts"][0]["status"] = "awaiting_facts"
        self.assertTrue(validate(self.data)["ok"])

    def test_planned_shots_block_ready_draft(self):
        self.data["drafts"][3]["status"] = "ready_for_review"
        self.reject(self.data, "DRAFT_SHOT_GATE")
        for shot in self.data["shots"]:
            shot["status"] = "captured"  # Controlled state transition, no claim of real capture.
        self.assertTrue(validate(self.data)["ok"])

    def test_optional_s05_does_not_block_ready_drafts(self):
        for optional_status in ("planned", "unavailable"):
            with self.subTest(s05_status=optional_status):
                data = copy.deepcopy(self.data)
                # Controlled fixture: required materials reviewed and sending
                # conditions checked; the optional supporting image is absent.
                for shot in data["shots"]:
                    if shot["id"] in ("S03", "S04"):
                        shot["status"] = "captured"
                    elif shot["id"] == "S05":
                        shot["status"] = optional_status
                for draft in data["drafts"]:
                    if draft["topic_id"] in ("05", "06"):
                        draft["status"] = "ready_for_review"
                result = validate(data)
                self.assertTrue(result["ok"], result)
                self.assertEqual(result["summary"]["draft_statuses"],
                                 {"ready_for_review": 5, "awaiting_facts": 0, "awaiting_capture": 4})

    def test_captured_s05_does_not_replace_required_materials(self):
        for topic_id, required_shots in (("05", ("S03", "S04")), ("06", ("S03",))):
            for missing_status in ("planned", "unavailable", "available"):
                with self.subTest(topic_id=topic_id, shots=required_shots, status=missing_status):
                    data = copy.deepcopy(self.data)
                    for shot in data["shots"]:
                        if shot["id"] in ("S03", "S04", "S05"):
                            shot["status"] = missing_status if shot["id"] in required_shots else "captured"
                    for draft in data["drafts"]:
                        if draft["topic_id"] == topic_id:
                            draft["status"] = "ready_for_review"
                    result = self.reject(data, "DRAFT_SHOT_GATE")
                    self.assertEqual({e["path"] for e in result["errors"] if e["code"] == "DRAFT_SHOT_GATE"},
                                     {"drafts." + topic_id})

    def test_s03_or_s04_captured_satisfies_actual_handoff_alternative(self):
        for captured in ("S03", "S04"):
            with self.subTest(captured=captured):
                data = copy.deepcopy(self.data)
                draft = next(d for d in data["drafts"] if d["topic_id"] == "05")
                self.assertEqual(draft["required_shot_ids"], [])
                self.assertEqual(draft["required_shot_any_of"], [["S03", "S04"]])
                draft["status"] = "ready_for_review"
                for shot in data["shots"]:
                    if shot["id"] in ("S03", "S04", "S05"):
                        shot["status"] = "captured" if shot["id"] == captured else "unavailable"
                result = validate(data)
                self.assertTrue(result["ok"], result)
                self.assertEqual(result["summary"]["draft_statuses"],
                                 {"ready_for_review": 4, "awaiting_facts": 0, "awaiting_capture": 5})

    def test_all_required_shots_and_each_any_of_group_must_be_satisfied(self):
        draft = next(d for d in self.data["drafts"] if d["topic_id"] == "05")
        draft.update(status="ready_for_review", required_shot_ids=["S01"],
                     required_shot_any_of=[["S03", "S04"], ["S06", "S07"]])
        topic = next(t for t in self.data["topics"] if t["id"] == "05")
        for shot in self.data["shots"]:
            if shot["id"] in ("S01", "S06", "S07"):
                topic["shot_ids"].append(shot["id"])
                shot["topic_ids"].append("05")
            shot["status"] = "captured" if shot["id"] in ("S01", "S04", "S06") else "unavailable"
        self.assertTrue(validate(self.data)["ok"])
        next(s for s in self.data["shots"] if s["id"] == "S01")["status"] = "planned"
        self.reject(self.data, "DRAFT_SHOT_GATE")
        next(s for s in self.data["shots"] if s["id"] == "S01")["status"] = "captured"
        next(s for s in self.data["shots"] if s["id"] == "S06")["status"] = "planned"
        self.reject(self.data, "DRAFT_SHOT_GATE")

    def test_missing_any_of_field_preserves_legacy_all_required_semantics(self):
        draft = next(d for d in self.data["drafts"] if d["topic_id"] == "05")
        draft.pop("required_shot_any_of")
        draft.update(status="ready_for_review", required_shot_ids=["S03", "S04"])
        for shot in self.data["shots"]:
            if shot["id"] in ("S03", "S04"):
                shot["status"] = "captured"
        self.assertTrue(validate(self.data)["ok"])
        next(s for s in self.data["shots"] if s["id"] == "S03")["status"] = "unavailable"
        self.reject(self.data, "DRAFT_SHOT_GATE")

    def test_any_of_groups_reject_unknown_empty_and_malformed_data(self):
        for groups, code in (([["UNKNOWN"]], "UNKNOWN_REF"), ([[]], "DRAFT_SHOT_GROUP"),
                             (None, "SCHEMA"), ("S03", "SCHEMA"), ({"one": ["S03"]}, "SCHEMA"),
                             (["S03"], "SCHEMA"), ([[None]], "SCHEMA"), ([[["S03"]]], "SCHEMA"),
                             ([["S03", "S03"]], "DUPLICATE_REF")):
            with self.subTest(groups=groups):
                data = copy.deepcopy(self.data)
                next(d for d in data["drafts"] if d["topic_id"] == "05")["required_shot_any_of"] = groups
                self.reject(data, code)

    def test_faq_without_business_fact_has_no_invented_answer(self):
        self.assertIsNone(self.data["faqs"][2]["answer"])
        self.data["faqs"][2]["answer"] = "错误测试：把未知业务当作确定答案"
        self.reject(self.data, "FAQ_STATUS")

    def test_complete_faq_cannot_keep_a_gap(self):
        self.data["faqs"][0]["status"] = "supported"
        self.reject(self.data, "FAQ_STATUS")

    def test_repeated_body_is_not_a_complete_batch(self):
        self.data["drafts"][1]["text"] = self.data["drafts"][0]["text"]
        self.reject(self.data, "REPEATED_DRAFT")

    def observation(self, status, identifier="O1"):
        return {"id": identifier, "status": status, "question": "受控测试问题，非真实查询", "platform": "controlled-test",
                "brand_mentioned": None, "native_citations": None, "error": "测试查询失败" if status == "query_failed" else None}

    def controlled_answer(self):
        # Synthetic input exercises the observed-data branch only. It is not exported
        # as a real answer, citation record, customer case, or live GEO test result.
        answer = self.observation("observed")
        answer.update(answer="受控测试输入中出现青禾。", origin="provided_answer",
                      captured_at="2026-10-19T12:00:00+08:00", evidence="controlled unit-test input; no live query",
                      brand_mentioned=True, native_citations=[{"url": "https://example.com/test-only", "native_ref": "controlled native field 1"}])
        return answer

    def test_unmeasured_statuses_remain_null_and_separate(self):
        self.data["observations"] = [self.observation(s, str(n)) for n, s in enumerate(("simulated", "not_run", "query_failed"))]
        result = validate(self.data)
        self.assertTrue(result["ok"], result)
        geo = result["summary"]["geo"]
        self.assertEqual(geo["status_counts"], {"observed": 0, "simulated": 1, "not_run": 1, "query_failed": 1})
        self.assertIsNone(geo["brand_mentions"])
        self.assertIsNone(geo["native_citations"])

    def test_unmeasured_statuses_cannot_be_zero_citations(self):
        for status in ("simulated", "not_run", "query_failed"):
            with self.subTest(status=status):
                self.data["observations"] = [self.observation(status)]
                self.data["observations"][0]["native_citations"] = []
                self.reject(self.data, "GEO_UNMEASURED")

    def test_only_observed_answers_enter_the_denominator(self):
        self.data["observations"] = [self.controlled_answer(), self.observation("simulated", "O2"), self.observation("query_failed", "O3")]
        result = validate(self.data)
        self.assertTrue(result["ok"], result)
        geo = result["summary"]["geo"]
        self.assertEqual((geo["observed_answers"], geo["brand_mentions"], geo["native_citations"]), (1, 1, 1))

    def test_valid_answer_can_have_confirmed_zero_results(self):
        answer = self.controlled_answer()
        answer.update(answer="受控输入，没有目标品牌名。", brand_mentioned=False, native_citations=[])
        self.data["observations"] = [answer]
        geo = validate(self.data)["summary"]["geo"]
        self.assertEqual((geo["observed_answers"], geo["brand_mentions"], geo["native_citations"]), (1, 0, 0))

    def test_mention_requires_brand_in_answer(self):
        answer = self.controlled_answer()
        answer["answer"] = "没有品牌的受控输入"
        self.data["observations"] = [answer]
        self.reject(self.data, "GEO_MENTION")

    def test_explicit_brand_cannot_be_reported_as_unmentioned(self):
        answer = self.controlled_answer()
        answer["brand_mentioned"] = False
        self.data["observations"] = [answer]
        self.reject(self.data, "GEO_MENTION")

    def test_native_citation_requires_native_location(self):
        answer = self.controlled_answer()
        answer["native_citations"][0].pop("native_ref")
        self.data["observations"] = [answer]
        self.reject(self.data, "SCHEMA")

    def test_malformed_citation_url_is_a_business_error(self):
        answer = self.controlled_answer()
        answer["native_citations"][0]["url"] = "http://[broken"
        self.data["observations"] = [answer]
        self.reject(self.data, "GEO_CITATION")

    def test_observed_answer_requires_evidence_and_timezone(self):
        answer = self.controlled_answer()
        answer["captured_at"] = "2026-10-19T12:00:00"
        answer["evidence"] = ""
        self.data["observations"] = [answer]
        result = self.reject(self.data, "GEO_TIME")
        self.assertIn("SCHEMA", {e["code"] for e in result["errors"]})

    def test_failure_example_and_repair(self):
        data = json.loads(BAD.read_text(encoding="utf-8"))
        result = validate(data)
        self.assertEqual({x["code"] for x in result["errors"]}, {"TIME_RAW_CHANGED", "SHOOT_CONFLICT", "DRAFT_FACT_GATE"})
        data["event"]["time"]["raw"] = "下周"
        data["shots"][1].update(start_minute=5, end_minute=8)
        data["drafts"][0]["status"] = "awaiting_facts"
        self.assertTrue(validate(data)["ok"])

    def test_malformed_nested_data_returns_errors(self):
        for section in ("facts", "topics", "shots", "faqs", "drafts", "observations"):
            with self.subTest(section=section):
                data = copy.deepcopy(self.data)
                data[section] = [None, {"id": []}]
                self.reject(data, "SCHEMA")
        for field, value in (("owner", []), ("shot_ids", None)):
            data = copy.deepcopy(self.data)
            data["topics"][3][field] = value
            self.reject(data, "SCHEMA" if field == "shot_ids" else "UNKNOWN_REF")
        self.reject([], "SCHEMA")

    def test_cli_success_and_expected_failure(self):
        self.assertEqual(self.cli(GOOD)[0], 0)
        code, result = self.cli(BAD)
        self.assertEqual(code, 1)
        self.assertFalse(result["ok"])

    def test_cli_invalid_json_and_missing_input_exit_two(self):
        with tempfile.TemporaryDirectory(prefix="campaign-input-") as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text("{invalid", encoding="utf-8")
            for path in (p, Path(tmp) / "absent.json"):
                code, result = self.cli(path)
                self.assertEqual(code, 2)
                self.assertEqual(result["errors"][0]["code"], "INPUT_ERROR")

    def test_isolated_copy_without_host_license_or_icon(self):
        with tempfile.TemporaryDirectory(prefix="campaign-isolated-") as tmp:
            base = Path(tmp)
            (base / "scripts").mkdir()
            shutil.copy2(ROOT / "scripts" / "check_campaign.py", base / "scripts" / "check_campaign.py")
            (base / "examples").mkdir()
            shutil.copy2(GOOD, base / "examples" / "campaign.json")
            code, result = self.cli(Path("examples/campaign.json"), cwd=base, script=base / "scripts" / "check_campaign.py")
            self.assertEqual(code, 0)
            self.assertEqual(result["summary"]["drafts"], 9)

    def test_example_handoff_contains_the_actual_full_drafts(self):
        handoff = (GOOD.parent / "已选稿件及平台交接表.md").read_text(encoding="utf-8")
        for draft in self.data["drafts"]:
            self.assertIn(draft["text"], handoff, draft["topic_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
