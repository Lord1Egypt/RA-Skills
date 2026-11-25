#!/usr/bin/env python3
"""Offline business and failure-boundary regression tests; no live AI calls."""

import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from analyze import InputError, analyze  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze.py"


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def fixture():
    return load("examples/success/input.json")


def controlled():
    # Only an in-memory test of the observed branch. Never saved as live evidence.
    data = fixture()
    for r in data["records"]:
        r["status"] = "observed"
        r["source"] = "Controlled test fixture, not a live observation"
        r["captured_at"] = "2026-10-18T09:00:00+08:00"
    return data


class EvidenceTests(unittest.TestCase):
    def test_synthetic_is_never_measured(self):
        result = analyze(fixture())
        self.assertEqual(result["status_counts"], {"observed": 0, "query_failed": 0, "missing": 0, "not_run": 0, "simulated": 4})
        self.assertEqual(result["measured"]["valid_answers"], 0)
        for metric in result["measured"]["metrics"].values():
            self.assertIsNone(metric["percent"])
            self.assertIsNone(metric["numerator"])
            self.assertEqual(metric["denominator"], 0)
        self.assertTrue(all(not r["included_in_measured_metrics"] for r in result["records"]))

    def test_four_answer_business_results(self):
        result = analyze(controlled())
        measured = result["measured"]
        self.assertEqual(measured["valid_answers"], 4)
        for name, hits, n, percent in (("mention_rate", 3, 4, 75.0),
                                      ("recommendation_rate", 1, 4, 25.0),
                                      ("native_brand_citation_rate", 1, 4, 25.0),
                                      ("fact_match_rate", 3, 5, 60.0),
                                      ("intent_coverage", 3, 4, 75.0)):
            self.assertEqual(measured["metrics"][name], {"numerator": hits, "denominator": n, "percent": percent, "unknown": 0})
        absent = [q["question_id"] for q in measured["questions"] if q["unmentioned_in_all_valid_answers"]]
        self.assertEqual(absent, ["Q3"])
        conflicts = [(r["id"], f["fact_id"]) for r in result["records"]
                     for f in r["review"]["fact_checks"] if f["verdict"] == "contradiction"]
        self.assertEqual(conflicts, [("r2", "f-platform"), ("r2", "f-price")])
        self.assertEqual(measured["tone"]["counts"], {"positive": 1, "neutral": 2, "negative": 0, "mixed": 0})
        self.assertEqual(measured["tone"]["unknown_answers"], 1)
        self.assertEqual(len(measured["fact_review_disagreements"]), 2)
        self.assertEqual(len(measured["by_platform_model_search"]), 2)

    def test_failures_missing_unrun_excluded_and_separate(self):
        data = controlled()
        unavailable = load("examples/failure/mixed-status.json")["records"][:3]
        for i, r in enumerate(unavailable):
            r["question_id"] = f"unavailable-{i}"
        data["records"].extend(unavailable)
        result = analyze(data)
        self.assertEqual(result["measured"]["metrics"]["mention_rate"]["denominator"], 4)
        for state in ("query_failed", "missing", "not_run"):
            self.assertEqual(result["status_counts"][state], 1)
        self.assertTrue(all(r["brand_native_cited"] is None for r in result["records"][-3:]))
        self.assertTrue(all(q["unmentioned_in_all_valid_answers"] is None for q in result["measured"]["questions"][-3:]))

    def test_no_valid_samples_stay_unknown(self):
        result = analyze(load("examples/failure/mixed-status.json"))
        self.assertEqual(result["measured"]["valid_answers"], 0)
        self.assertIsNone(result["measured"]["metrics"]["native_brand_citation_rate"]["numerator"])
        self.assertIsNone(result["measured"]["tone"]["counts"]["positive"])

    def test_no_links_and_inline_are_not_native_citations(self):
        records = analyze(controlled())["records"]
        self.assertEqual([r["native_brand_citation_count"] for r in records], [1, 0, 0, 0])
        self.assertEqual(records[3]["citations"][0]["kind"], "inline")

    def test_incomplete_sources_unknown_not_zero(self):
        for capture in ("partial", "not_captured"):
            data = controlled()
            data["records"][1]["citations_capture"] = capture
            result = analyze(data)
            self.assertIsNone(result["records"][1]["brand_native_cited"])
            self.assertEqual(result["measured"]["metrics"]["native_brand_citation_rate"],
                             {"numerator": 1, "denominator": 3, "percent": 33.3, "unknown": 1})

    def test_partial_with_known_link_is_not_complete_total(self):
        data = controlled()
        data["records"][0]["citations_capture"] = "partial"
        result = analyze(data)
        self.assertEqual(len(result["records"][0]["native_brand_urls"]), 1)
        self.assertIsNone(result["records"][0]["native_brand_citation_count"])
        self.assertEqual(result["measured"]["metrics"]["native_brand_citation_rate"]["denominator"], 3)

    def test_inline_links_retained_without_native_source_capture(self):
        data = controlled()
        data["records"][3]["citations_capture"] = "not_captured"
        result = analyze(data)
        record = result["records"][3]
        self.assertEqual(record["citations"][0]["kind"], "inline")
        self.assertIsNone(record["brand_native_cited"])
        self.assertEqual(result["measured"]["metrics"]["native_brand_citation_rate"]["unknown"], 1)

    def test_native_links_require_at_least_partial_capture(self):
        data = controlled()
        data["records"][0]["citations_capture"] = "not_captured"
        with self.assertRaisesRegex(InputError, "native links require"):
            analyze(data)

    def test_unreviewed_citation_relation_unknown(self):
        data = controlled()
        data["records"][0]["citations"][0]["relation"] = "unreviewed"
        result = analyze(data)
        self.assertIsNone(result["records"][0]["brand_native_cited"])
        self.assertEqual(result["measured"]["metrics"]["native_brand_citation_rate"]["unknown"], 1)

    def test_other_native_source_does_not_cite_brand(self):
        data = controlled()
        data["records"][0]["citations"][0]["relation"] = "other"
        data["records"][0]["citations"][0]["relation_evidence"] = "Controlled unrelated source"
        metric = analyze(data)["measured"]["metrics"]["native_brand_citation_rate"]
        self.assertEqual((metric["numerator"], metric["denominator"], metric["percent"]), (0, 4, 0.0))

    def test_links_deduplicate_documents(self):
        data = controlled()
        link = copy.deepcopy(data["records"][0]["citations"][0])
        link["url"] += "#details"
        data["records"][0]["citations"].append(link)
        self.assertEqual(analyze(data)["records"][0]["native_brand_citation_count"], 1)

    def test_conflicting_duplicate_links_rejected(self):
        data = controlled()
        link = copy.deepcopy(data["records"][0]["citations"][0])
        link["relation"] = "other"
        data["records"][0]["citations"].append(link)
        with self.assertRaises(InputError):
            analyze(data)

    def test_unreviewed_text_never_inferred_from_keywords(self):
        data = controlled()
        data["records"][0]["review"] = {}
        result = analyze(data)
        self.assertEqual(result["records"][0]["literal_candidates"], ["青禾工具"])
        self.assertIsNone(result["records"][0]["review"]["mention"]["value"])
        self.assertEqual(result["measured"]["metrics"]["mention_rate"]["denominator"], 3)
        self.assertEqual(result["measured"]["metrics"]["recommendation_rate"]["unknown"], 1)
        self.assertEqual(result["measured"]["metrics"]["intent_coverage"]["denominator"], 3)
        self.assertIsNone(result["measured"]["questions"][0]["unmentioned_in_all_valid_answers"])

    def test_same_name_can_be_reviewed_as_other_entity(self):
        data = controlled()
        r = data["records"][0]
        r["review"] = {"mention": {"value": False, "reason": "Controlled same-name ambiguity, different entity"}}
        result = analyze(data)
        self.assertIs(result["records"][0]["review"]["mention"]["value"], False)
        self.assertEqual(result["measured"]["metrics"]["mention_rate"]["numerator"], 2)

    def test_invented_quote_rejected(self):
        with self.assertRaisesRegex(InputError, "exact substring"):
            analyze(load("examples/failure/invalid-quote.json"))

    def test_recommendation_requires_mention(self):
        data = controlled()
        data["records"][0]["review"]["mention"] = {"value": False, "reason": "Controlled conflicting labels"}
        with self.assertRaisesRegex(InputError, "recommendation requires"):
            analyze(data)

    def test_unknown_fact_does_not_lower_accuracy(self):
        data = controlled()
        check = data["records"][0]["review"]["fact_checks"][0]
        check["verdict"], check["fact_id"] = "unverified", None
        metric = analyze(data)["measured"]["metrics"]["fact_match_rate"]
        self.assertEqual(metric, {"numerator": 2, "denominator": 4, "percent": 50.0, "unknown": 1})

    def test_fact_requires_source_and_known_id(self):
        data = controlled()
        del data["brand"]["facts"][0]["source"]
        with self.assertRaises(InputError):
            analyze(data)
        data = controlled()
        data["records"][0]["review"]["fact_checks"][0]["fact_id"] = "invented"
        with self.assertRaises(InputError):
            analyze(data)

    def test_duplicate_record_and_run_rejected(self):
        for new_id in ("r1", "new-id-same-run"):
            data = controlled()
            duplicate = copy.deepcopy(data["records"][0])
            duplicate["id"] = new_id
            data["records"].append(duplicate)
            with self.assertRaisesRegex(InputError, "duplicate"):
                analyze(data)

    def test_genuine_repeat_does_not_invent_another_intent(self):
        data = controlled()
        repeat = copy.deepcopy(data["records"][0])
        repeat["id"], repeat["run_id"] = "r1-repeat", "second-test-run"
        data["records"].append(repeat)
        measured = analyze(data)["measured"]
        self.assertEqual(measured["valid_answers"], 5)
        self.assertEqual(measured["metrics"]["mention_rate"]["numerator"], 4)
        self.assertEqual(measured["metrics"]["intent_coverage"]["denominator"], 4)

    def test_missing_time_visible_and_invalid_time_rejected(self):
        data = controlled()
        data["records"][0]["captured_at"] = None
        self.assertEqual(analyze(data)["measured"]["missing_capture_time_ids"], ["r1"])
        for bad in ("2026-10-18T09:00:00", "yesterday"):
            data["records"][0]["captured_at"] = bad
            with self.assertRaises(InputError):
                analyze(data)

    def test_missing_brand_and_blank_observed_answer_rejected(self):
        for mutate in (lambda d: d["brand"].update(name=" "),
                       lambda d: d["records"][0].update(answer="")):
            data = controlled()
            mutate(data)
            with self.assertRaises(InputError):
                analyze(data)

    def test_failed_record_cannot_carry_assessed_evidence(self):
        data = controlled()
        data["records"][0].update(status="query_failed", reason="Controlled failure")
        with self.assertRaises(InputError):
            analyze(data)

    def test_urls_reject_credentials_and_unsafe_schemes(self):
        for bad in ("javascript:alert(1)", "https://name:secret@example.org/a", "relative/file", "https://example.org/a b"):
            data = controlled()
            data["records"][0]["citations"][0]["url"] = bad
            with self.assertRaises(InputError):
                analyze(data)

    def test_whitelist_keeps_evidence_but_drops_extensions(self):
        data = controlled()
        data["arbitrary_extension"] = "discard this extension"
        data["records"][0]["unused_extension"] = "discard this too"
        result = analyze(data)
        self.assertNotIn("arbitrary_extension", result)
        self.assertNotIn("unused_extension", result["records"][0])
        self.assertEqual(result["records"][0]["answer"], data["records"][0]["answer"])
        self.assertEqual(len(result["records"][0]["answer_sha256"]), 64)

    def test_empty_input_scope_is_valid_but_unmeasured(self):
        data = {"schema_version": "1.0", "brand": {"name": "No listing needed"}, "records": []}
        self.assertIsNone(analyze(data)["measured"]["metrics"]["mention_rate"]["percent"])

    def test_expected_outputs_match_actual_aggregations(self):
        self.assertEqual(analyze(fixture()), load("examples/success/逐问题证据表.json"))
        self.assertEqual(analyze(load("examples/failure/mixed-status.json")), load("examples/failure/expected.json"))


class CliTests(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=cwd,
                              capture_output=True, text=True, encoding="utf-8", timeout=10)

    def test_cli_works_outside_skill_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "evidence.json"
            result = self.run_cli(ROOT / "examples/success/input.json", "--output", target, cwd=directory)
            self.assertEqual((result.returncode, result.stdout, result.stderr), (0, "", ""))
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), analyze(fixture()))

    def test_cli_invalid_evidence_has_no_success_output(self):
        result = self.run_cli(ROOT / "examples/failure/invalid-quote.json")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(result.stderr), load("examples/failure/expected-error.json"))

    def test_cli_bad_json_duplicate_keys_and_nan(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.json"
            target = Path(directory) / "out.json"
            for body in ("", "{", "[]", '{"x":1,"x":2}', '{"x":NaN}'):
                source.write_text(body, encoding="utf-8")
                result = self.run_cli(source, "--output", target)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertEqual(json.loads(result.stderr)["status"], "error")
                self.assertFalse(target.exists())

    def test_cli_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "keep.json"
            target.write_text("original", encoding="utf-8")
            result = self.run_cli(ROOT / "examples/success/input.json", "--output", target)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(target.read_text(encoding="utf-8"), "original")


class PackageTests(unittest.TestCase):
    def test_document_relative_links_resolve(self):
        for document in ROOT.rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                target = target.split("#", 1)[0]
                self.assertTrue((document.parent / target).is_file(), f"Broken link in {document.name}: {target}")

    def test_required_metadata(self):
        manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
        fields = dict(re.findall(r"^([a-z_]+):(?:[ \t]*(.*))?$", manifest, re.M))
        self.assertEqual(fields["name"], "aimegeo-brand-visibility")
        self.assertEqual(fields["slug"], "aimegeo-brand-visibility")
        self.assertEqual(fields["version"], "1.0.3")
        self.assertEqual(fields["self_test"], "python3 scripts/self_test.py")
        self.assertRegex(
            fields["repository"].strip('"'),
            rf"\Ahttps://github\.com/[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/{re.escape(fields['slug'])}\Z",
        )
        self.assertTrue(set(("display_name", "description", "icon", "license", "tags", "trigger_words")) <= fields.keys())

    def test_bundled_icon(self):
        manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
        icon_name = re.search(r"^icon:[ \t]*(.+)$", manifest, re.M).group(1).strip('"\'')
        icon_path = ROOT / icon_name
        if not icon_path.exists():
            self.skipTest("SkillHub hosts its listing icon separately; no icon is needed by the business CLI")
        icon = icon_path.read_bytes()
        self.assertEqual(icon[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual((int.from_bytes(icon[16:20], "big"), int.from_bytes(icon[20:24], "big")), (512, 512))


if __name__ == "__main__":
    unittest.main(verbosity=2)
