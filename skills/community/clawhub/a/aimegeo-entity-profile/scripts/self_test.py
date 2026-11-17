#!/usr/bin/env python3
"""Offline business tests. Illustrative inputs are never evidence of live GEO measurements."""

import copy
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import entity_profile as ep

ROOT = Path(__file__).resolve().parents[1]


class EntityProfileTests(unittest.TestCase):
    def setUp(self):
        self.profile = ep.load_profile(ROOT / "examples/qinghe/品牌实体档案.json")

    def rejected(self, profile, code, function=ep.validate):
        with self.assertRaises(ep.InvalidProfile) as result:
            function(profile)
        self.assertEqual(result.exception.issue["code"], code)
        return result.exception.issue

    def add_response(self, profile, oid, mentioned=True, citations=None, complete=False):
        # Controlled synthetic raw record, used only inside a profile marked illustrative.
        answer = "离线回归回答：青禾工具是表格与文本整理软件。" if mentioned else "离线回归回答：没有讨论目标产品。"
        query = "离线测试问题 " + oid
        capture = "complete" if complete else "not_captured"
        sid = "R-" + oid
        source = {"id": sid, "kind": "ai_response", "locator": "provided:offline-regression-" + oid,
                  "acquisition": "user_supplied", "captured_on": "2026-10-19",
                  "subject_entity_ids": ["product-qinghe-tools"], "excerpt": answer,
                  "platform": "offline-test", "query": query, "citation_capture": capture,
                  "native_citations": citations}
        obs = {"id": oid, "entity_id": "product-qinghe-tools", "platform": "offline-test", "query": query,
               "status": "observed", "observed_on": "2026-10-19", "source_id": sid, "answer": answer,
               "mentioned": mentioned, "citation_capture": capture, "native_citations": citations, "error": None}
        profile["sources"].append(source)
        profile["observations"].append(obs)
        return obs

    def conflict_profile(self):
        p = copy.deepcopy(self.profile)
        alternatives = []
        for sid, value in (("D1", "2020"), ("D2", "2021")):
            quote = "青禾科技有限公司成立于" + value + "年。"
            p["sources"].append({"id": sid, "kind": "official_site", "locator": "provided:冲突演示-" + sid,
                                 "acquisition": "user_supplied", "captured_on": "2026-10-19",
                                 "subject_entity_ids": ["org-qinghe"], "excerpt": quote})
            alternatives.append({"value": value, "evidence": [{"source_id": sid, "quote": quote}]})
        p["entities"][0]["facts"]["founding_date"] = {
            "status": "conflicting", "value": None, "evidence": [], "reason": "两份演示来源日期不同。", "alternatives": alternatives}
        return p

    def test_company_product_separation_and_typed_schema(self):
        result = ep.validate(self.profile)
        self.assertEqual(result["entity_count"], 2)
        self.assertEqual(result["relationship_count"], 1)
        graph = ep.schema_graph(self.profile)["@graph"]
        self.assertEqual(len(graph), 2)
        org, product = graph
        self.assertEqual((org["@type"], product["@type"]), ("Organization", "SoftwareApplication"))
        self.assertNotEqual(org["@id"], product["@id"])
        self.assertEqual(product["creator"], [{"@id": org["@id"]}])
        self.assertNotIn("sameAs", product)
        self.assertEqual(product["alternateName"], ["Qinghe Tools"])
        self.assertNotIn("Qinghe Tools", org.get("alternateName", []))

    def test_unknown_founding_date_stays_null_and_is_not_exported(self):
        before = copy.deepcopy(self.profile)
        date_fact = self.profile["entities"][0]["facts"]["founding_date"]
        self.assertIsNone(date_fact["value"])
        self.assertNotIn("foundingDate", ep.schema_graph(self.profile)["@graph"][0])
        self.assertEqual(self.profile, before)

    def test_user_only_can_finish_without_api_or_website(self):
        p = ep.load_profile(ROOT / "examples/user-only.json")
        result = ep.validate(p)
        self.assertEqual(result["entity_count"], 2)
        self.assertEqual(result["fact_status_counts"], {"reported": 5, "unknown": 9})
        self.assertEqual(p["relationships"], [])
        self.assertEqual(p["entities"][1]["type"], "Product")

    def test_schema_refuses_unverified_primary_identity(self):
        p = ep.load_profile(ROOT / "examples/user-only.json")
        self.rejected(p, "schema_identity_unverified", ep.schema_graph)

    def test_unsupported_claim_needs_evidence(self):
        self.profile["entities"][1]["facts"]["description"]["evidence"] = []
        self.rejected(self.profile, "evidence_required")

    def test_missing_source_is_rejected(self):
        self.profile["entities"][1]["facts"]["name_en"]["evidence"][0]["source_id"] = "missing"
        self.rejected(self.profile, "source_missing")

    def test_exact_quote_must_be_in_captured_source(self):
        self.profile["entities"][1]["facts"]["name_en"]["evidence"][0]["quote"] = "编造的官网原文"
        self.rejected(self.profile, "quote_not_found")

    def test_company_only_evidence_cannot_prove_product_fact(self):
        self.profile["entities"][1]["facts"]["name_en"]["evidence"] = [{"source_id": "S2", "quote": "青禾科技有限公司"}]
        self.rejected(self.profile, "source_subject")

    def test_known_company_website_is_not_product_same_as(self):
        bad = ep.load_profile(ROOT / "examples/failures/mixed-identity.json")
        actual = self.rejected(bad, "same_as_cross_entity")
        expected = ep.load_profile(ROOT / "examples/failures/expected-error.json")
        self.assertEqual({"ok": False, "errors": [actual]}, expected)

    def test_unresolved_namesake_cannot_be_same_as(self):
        self.profile["disambiguation"][0]["resolution"] = "unresolved"
        self.profile["entities"][1]["same_as"] = [{"url": "https://qinghe-hardware.example/", "entity_id": "product-qinghe-tools",
            "status": "supported", "evidence": self.profile["disambiguation"][0]["evidence"]}]
        self.rejected(self.profile, "same_as_candidate")

    def test_namesake_cannot_be_canonical_website(self):
        self.profile["entities"][1]["facts"]["website"]["value"] = "https://qinghe-hardware.example/"
        self.rejected(self.profile, "candidate_as_website")

    def test_wrong_relationship_direction_is_rejected(self):
        r = self.profile["relationships"][0]
        r["subject_id"], r["object_id"] = r["object_id"], r["subject_id"]
        self.rejected(self.profile, "relation_direction")

    def test_same_display_name_does_not_merge_separate_entities(self):
        # Same names are allowed. Identity comes from IDs, type, provenance and relationships.
        for key in ("canonical_name", "name_zh"):
            self.profile["entities"][0]["facts"][key] = copy.deepcopy(self.profile["entities"][1]["facts"][key])
        graph = ep.schema_graph(self.profile)["@graph"]
        self.assertEqual(graph[0]["name"], graph[1]["name"])
        self.assertEqual(len({node["@id"] for node in graph}), 2)

    def test_unknown_date_cannot_hide_a_guessed_value(self):
        self.profile["entities"][0]["facts"]["founding_date"]["value"] = "2026-10-19"
        self.rejected(self.profile, "unknown_value")

    def test_product_date_cannot_be_company_founding_date(self):
        f = self.profile["entities"][1]["facts"]["founding_date"]
        f.update(status="supported", value="2020")
        self.rejected(self.profile, "date_subject")

    def test_conflicting_dates_are_preserved_and_not_exported(self):
        p = self.conflict_profile()
        result = ep.validate(p)
        fact = p["entities"][0]["facts"]["founding_date"]
        self.assertEqual(result["fact_status_counts"]["conflicting"], 1)
        self.assertIsNone(fact["value"])
        self.assertEqual([v["value"] for v in fact["alternatives"]], ["2020", "2021"])
        self.assertNotIn("foundingDate", ep.schema_graph(p)["@graph"][0])

    def test_conflicting_date_needs_multiple_sourced_candidates(self):
        p = self.conflict_profile()
        p["entities"][0]["facts"]["founding_date"]["alternatives"].pop()
        self.rejected(p, "conflict_alternatives")

    def test_invalid_calendar_date_is_rejected(self):
        p = self.conflict_profile()
        p["entities"][0]["facts"]["founding_date"]["alternatives"][0]["value"] = "2025-02-29"
        self.rejected(p, "date")

    def test_reported_description_is_not_silently_promoted_to_schema(self):
        p = self.profile
        p["sources"].append({"id": "U1", "kind": "user_material", "locator": "provided:演示口述",
            "acquisition": "user_supplied", "captured_on": "2026-10-19", "subject_entity_ids": ["product-qinghe-tools"], "excerpt": "用户说该产品可以整理表格。"})
        p["entities"][1]["facts"]["description"] = {"status": "reported", "value": "该产品可以整理表格。",
            "evidence": [{"source_id": "U1", "quote": "用户说该产品可以整理表格。"}]}
        self.assertNotIn("description", ep.schema_graph(p)["@graph"][1])

    def test_unrun_summary_is_unknown_not_zero(self):
        summary = ep.summarize(self.profile)
        self.assertEqual(summary["status_counts"], {"observed": 0, "not_run": 1, "query_failed": 0, "simulated": 0})
        self.assertIsNone(summary["mentioned_count"])
        self.assertIsNone(summary["mention_rate"])
        self.assertIsNone(summary["native_citation_count"])
        self.assertFalse(summary["usable_as_live_measurement"])

    def test_denominators_exclude_failed_unrun_and_simulated_records(self):
        p = self.profile
        self.add_response(p, "R1", True, ["https://qinghe-tools.example/tools"], True)
        self.add_response(p, "R2", False)
        for oid, status in (("F1", "query_failed"), ("SIM1", "simulated")):
            obs = copy.deepcopy(p["observations"][0])
            obs.update(id=oid, status=status, error="离线测试网络错误" if status == "query_failed" else None,
                       answer="这是模拟回答，不是实际采集。" if status == "simulated" else None)
            p["observations"].append(obs)
        summary = ep.summarize(p)
        self.assertEqual(summary["status_counts"], {"observed": 2, "not_run": 1, "query_failed": 1, "simulated": 1})
        self.assertEqual((summary["observed_samples"], summary["mentioned_count"], summary["mention_rate"]), (2, 1, 0.5))
        self.assertEqual((summary["citation_complete_samples"], summary["citation_uncaptured_samples"], summary["native_citation_count"]), (1, 1, 1))
        self.assertEqual(summary["data_mode"], "illustrative")
        self.assertFalse(summary["usable_as_live_measurement"])

    def test_complete_zero_citations_differs_from_uncaptured(self):
        self.add_response(self.profile, "R1", False, [], True)
        summary = ep.summarize(self.profile)
        self.assertEqual(summary["native_citation_count"], 0)
        self.assertEqual(summary["mentioned_count"], 0)
        self.assertEqual(summary["citation_complete_samples"], 1)
        p = copy.deepcopy(self.profile)
        p["sources"][-1].update(citation_capture="not_captured", native_citations=None)
        p["observations"][-1].update(citation_capture="not_captured", native_citations=None)
        summary = ep.summarize(p)
        self.assertIsNone(summary["native_citation_count"])
        self.assertEqual(summary["citation_uncaptured_samples"], 1)

    def test_unmeasured_statuses_cannot_claim_zero_metrics(self):
        for status in ("not_run", "query_failed", "simulated"):
            with self.subTest(status=status):
                p = copy.deepcopy(self.profile)
                p["observations"][0].update(status=status, mentioned=False, native_citations=[],
                                            error="离线失败" if status == "query_failed" else None)
                self.rejected(p, "unmeasured_metrics")

    def test_failed_query_requires_error_detail(self):
        self.profile["observations"][0]["status"] = "query_failed"
        self.rejected(self.profile, "type")

    def test_response_source_and_query_must_match(self):
        obs = self.add_response(self.profile, "R1")
        obs["query"] = "另一个问题"
        self.rejected(self.profile, "observation_source")

    def test_native_citations_must_match_source_capture(self):
        obs = self.add_response(self.profile, "R1", True, [], True)
        obs["native_citations"] = ["https://not-captured.example/"]
        self.rejected(self.profile, "citation_source_mismatch")

    def test_ai_answer_cannot_become_company_fact_evidence(self):
        self.add_response(self.profile, "R1")
        source = self.profile["sources"][-1]
        self.profile["entities"][1]["facts"]["description"]["evidence"] = [{"source_id": source["id"], "quote": source["excerpt"]}]
        self.rejected(self.profile, "ai_as_fact")

    def test_observed_response_needs_capture_source(self):
        obs = self.add_response(self.profile, "R1")
        obs["source_id"] = None
        self.rejected(self.profile, "observation_source")

    def test_future_source_is_not_current_evidence(self):
        self.profile["sources"][0]["captured_on"] = "2027-01-01"
        self.rejected(self.profile, "future_source")

    def test_cli_from_an_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory(prefix="entity-profile-cli-") as tmp:
            result = subprocess.run([sys.executable, str(ROOT / "scripts/entity_profile.py"), "schema",
                                     str(ROOT / "examples/qinghe/品牌实体档案.json")], cwd=tmp, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), ep.schema_graph(self.profile))

    def test_cli_failure_is_structured_and_cannot_be_schema(self):
        out = io.StringIO()
        with redirect_stdout(out):
            status = ep.main(["schema", str(ROOT / "examples/user-only.json")])
        result = json.loads(out.getvalue())
        self.assertEqual(status, 2)
        self.assertFalse(result["ok"])
        self.assertNotIn("@graph", result)

    def test_malformed_duplicate_and_non_json_numeric_input(self):
        for raw, code in (("{", "input"), ('{"entities": [], "entities": []}', "duplicate_key"), ('{"value": NaN}', "input")):
            with self.subTest(raw=raw), tempfile.TemporaryDirectory(prefix="entity-profile-bad-") as tmp:
                path = Path(tmp) / "bad.json"
                path.write_text(raw, encoding="utf-8")
                out = io.StringIO()
                with redirect_stdout(out):
                    status = ep.main(["validate", str(path)])
                result = json.loads(out.getvalue())
                self.assertEqual(status, 2)
                self.assertEqual(result["errors"][0]["code"], code)

    def test_malformed_field_types_are_business_errors(self):
        variants = [None, [], {"schema_version": "1.0"}]
        for field, bad in (("entities", {}), ("sources", None), ("primary_entity_id", [])):
            p = copy.deepcopy(self.profile)
            p[field] = bad
            variants.append(p)
        for p in variants:
            with self.subTest(value=type(p).__name__):
                with self.assertRaises(ep.InvalidProfile):
                    ep.validate(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
