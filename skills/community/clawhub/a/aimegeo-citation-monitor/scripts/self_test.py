#!/usr/bin/env python3
"""Controlled offline regression tests; no platform queries or authentic user data."""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
import citation_monitor as monitor

ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def controlled_observed_shape():
    """Exercise observed accounting with synthetic records, only inside the tests."""
    data = load("examples/success/six-questions.json")
    data["dataset_kind"] = "observed"
    data["note"] = "Controlled synthetic test of the observed schema; never a live result."
    for run in data["runs"]:
        for record in run["records"]:
            record["status"] = "success"
            record["source"]["kind"] = "export"
            record["source"]["executor"] = "controlled-test-export"
    return data


def controlled_not_run_shape():
    data = load("examples/failure/all-failed.json")
    data["runs"][0]["records"] = [{
        "platform": data["platforms"][0], "query_id": data["queries"][0]["id"],
        "status": "not_run", "reason": "Controlled unrun sample; no collection performed",
    }]
    return data


class BusinessTests(unittest.TestCase):
    def test_01_separate_mention_and_native_citation_denominators(self):
        result = monitor.analyze(controlled_observed_shape(), "before", "after")
        before, after = result["history"]
        self.assertEqual((before["planned"], before["effective_answers"]), (6, 6))
        self.assertEqual((before["mentioned_answers"], after["mentioned_answers"]), (3, 5))
        self.assertEqual((before["citation_observed_answers"], after["citation_observed_answers"]), (5, 6))
        self.assertEqual((before["native_cited_answers"], after["native_cited_answers"]), (1, 3))
        self.assertEqual(before["citation_unknown_answers"], 1)
        self.assertAlmostEqual(after["native_citation_rate"], 0.5)

    def test_02_paired_changes_use_same_denominator(self):
        comparison = monitor.analyze(controlled_observed_shape(), "before", "after")["comparison"]
        mention, citation = comparison["mention"], comparison["native_citation"]
        self.assertEqual((mention["paired"], mention["gained"], mention["lost"]), (6, 3, 1))
        self.assertAlmostEqual(mention["delta_percentage_points"], 100 / 3)
        self.assertEqual((citation["paired"], citation["before_count"], citation["after_count"]), (5, 1, 2))
        self.assertEqual(citation["delta_percentage_points"], 20)
        self.assertEqual(citation["gained"], 1)

    def test_03_domain_boundaries_and_citation_positions(self):
        brand = {"name": "Example", "domains": ["example.com"]}
        links = ["https://evil-example.com/", "https://example.com.evil.invalid/",
                 "https://other.invalid/example.com", "https://other.invalid/?host=example.com",
                 "https://DOCS.EXAMPLE.COM.:443/guide", "https://example.com/"]
        result = monitor.inspect_answer({"answer": "no target name", "citations": links}, brand)
        self.assertEqual([r["position"] for r in result["matched_native_citations"]], [5, 6])
        self.assertEqual(result["first_native_position"], 5)
        brand["include_subdomains"] = False
        result = monitor.inspect_answer({"answer": "no target name", "citations": links}, brand)
        self.assertEqual([r["position"] for r in result["matched_native_citations"]], [6])

    def test_04_alias_boundaries_unicode_and_configuration(self):
        self.assertTrue(monitor.alias_in_answer("Qinghe Tools", "推荐 Ｑｉｎｇｈｅ Ｔｏｏｌｓ。"))
        self.assertFalse(monitor.alias_in_answer("Qinghe", "FastQingheTools"))
        self.assertTrue(monitor.alias_in_answer("青禾", "可考虑青禾工具。"))
        data = controlled_observed_shape()
        data["brand"] = {"name": "不同品牌", "aliases": ["NeverSeen"], "domains": ["unrelated.invalid"]}
        result = monitor.analyze(data)
        self.assertEqual(result["overall"]["mentioned_answers"], 0)
        self.assertEqual(result["overall"]["native_cited_answers"], 0)

    def test_05_all_failed_no_rates_or_false_zero_citations(self):
        data = load("examples/failure/all-failed.json")
        data["dataset_kind"] = "observed"
        result = monitor.analyze(data)
        s = result["overall"]
        self.assertEqual((s["planned"], s["effective_answers"]), (6, 0))
        self.assertEqual(s["status_counts"], {"success": 0, "error": 1, "timeout": 1, "not_run": 4, "simulated": 0})
        for key in ("mentioned_answers", "native_cited_answers", "mention_rate", "native_citation_rate"):
            self.assertIsNone(s[key])
        self.assertNotIn("0.0%", monitor.report_text(result))
        self.assertEqual(s["critical_native_gaps"], [])

    def test_06_simulations_never_enter_observed_results(self):
        data = load("examples/success/six-questions.json")
        # Both simulated status and simulated dataset protect the denominator.
        data["runs"][0]["records"][0]["status"] = "success"
        result = monitor.analyze(data, "before", "after")
        self.assertEqual(result["overall"]["status_counts"]["simulated"], 12)
        self.assertEqual(result["overall"]["effective_answers"], 0)
        self.assertIsNone(result["overall"]["native_cited_answers"])
        self.assertTrue(result["results"][0]["simulation_preview"]["native_cited"])
        self.assertIsNone(result["results"][0]["native_cited"])
        self.assertEqual(result["comparison"]["native_citation"]["paired"], 0)

    def test_07_missing_record_and_timeout_remain_in_plan(self):
        data = controlled_observed_shape()
        data["runs"][1]["records"].pop()
        record = data["runs"][1]["records"][1]
        record.update(status="timeout", reason="Controlled timeout")
        record.pop("answer")
        record.pop("citations")
        result = monitor.analyze(data, "before", "after")
        s = result["history"][1]
        self.assertEqual((s["planned"], s["effective_answers"]), (6, 4))
        self.assertEqual((s["status_counts"]["not_run"], s["status_counts"]["timeout"]), (1, 1))
        self.assertEqual(result["comparison"]["mention"]["paired"], 4)

    def test_08_changed_query_model_search_context_or_source_excluded(self):
        for field in ("query", "model", "search_mode", "context", "source"):
            with self.subTest(field=field):
                data = controlled_observed_shape()
                record = data["runs"][1]["records"][0]
                if field == "query":
                    record["query"] += " 请举例。"
                elif field == "source":
                    record["source"]["executor"] = "another-executor"
                else:
                    record["conditions"][field] = "changed"
                comparison = monitor.analyze(data, "before", "after")["comparison"]
                self.assertEqual(comparison["mention"]["paired"], 5)
                self.assertTrue(comparison["pairs"][0]["mention_exclusions"])

    def test_09_unknown_conditions_block_pairing_but_keep_history(self):
        data = controlled_observed_shape()
        for run in data["runs"]:
            run["records"][0]["conditions"]["model"] = " unknown "
        result = monitor.analyze(data, "before", "after")
        self.assertEqual(result["overall"]["effective_answers"], 12)
        self.assertEqual(result["comparison"]["mention"]["paired"], 5)
        for run in data["runs"]:
            run["records"][1]["source"]["executor"] = "unknown"
        self.assertEqual(monitor.analyze(data, "before", "after")["comparison"]["mention"]["paired"], 4)

    def test_10_null_citations_are_unknown_empty_list_is_zero(self):
        data = controlled_observed_shape()
        for run in data["runs"]:
            for record in run["records"]:
                record["citations"] = None
        result = monitor.analyze(data, "before", "after")
        self.assertIsNone(result["overall"]["native_citation_rate"])
        self.assertEqual(result["comparison"]["mention"]["paired"], 6)
        self.assertEqual(result["comparison"]["native_citation"]["paired"], 0)
        data["runs"][0]["records"][0]["citations"] = []
        s = monitor.analyze(data)["overall"]
        self.assertEqual((s["native_cited_answers"], s["citation_observed_answers"]), (0, 1))
        self.assertEqual(s["native_citation_rate"], 0)

    def test_11_duplicate_and_unplanned_samples_rejected(self):
        for mutation in ("duplicate", "platform", "query", "invalid_query_type"):
            data = controlled_observed_shape()
            if mutation == "duplicate":
                data["runs"][0]["records"].append(copy.deepcopy(data["runs"][0]["records"][0]))
            elif mutation == "platform":
                data["runs"][0]["records"][0]["platform"] = "unplanned"
            elif mutation == "query":
                data["runs"][0]["records"][0]["query_id"] = "unplanned"
            else:
                data["runs"][0]["records"][0]["query_id"] = []
            with self.subTest(mutation=mutation), self.assertRaises(monitor.InputError):
                monitor.analyze(data)

    def test_12_absent_citations_and_empty_answer_rejected(self):
        with self.assertRaises(monitor.InputError):
            monitor.analyze(load("examples/failure/missing-citations.json"))
        data = controlled_observed_shape()
        data["runs"][0]["records"][0]["answer"] = " "
        with self.assertRaises(monitor.InputError):
            monitor.analyze(data)

    def test_13_bad_domains_urls_and_missing_provenance_rejected(self):
        for domain in ("https://example.com", "evil..com", "*.example.com", "example.com/path"):
            with self.subTest(domain=domain), self.assertRaises(monitor.InputError):
                monitor.domain_name(domain)
        for url in ("javascript:alert(1)", "https://example.com@evil.invalid/", "https://example.com:bad/", "example.com"):
            with self.subTest(url=url), self.assertRaises(monitor.InputError):
                monitor.url_host(url)
        data = controlled_observed_shape()
        del data["runs"][0]["records"][0]["source"]
        with self.assertRaises(monitor.InputError):
            monitor.analyze(data)

    def test_14_history_order_and_platform_category_accounting(self):
        data = controlled_observed_shape()
        data["runs"].reverse()
        data["platforms"].append("second-platform")
        result = monitor.analyze(data)
        self.assertEqual([r["run_id"] for r in result["history"]], ["before", "after"])
        self.assertEqual(result["overall"]["planned"], 24)
        self.assertEqual(result["overall"]["status_counts"]["not_run"], 12)
        self.assertEqual(sum(r["planned"] for r in result["by_category"]), 24)
        self.assertEqual(sum(r["effective_answers"] for r in result["by_platform"]), 12)

    def test_15_critical_gaps_are_observed_negatives_only(self):
        data = controlled_observed_shape()
        data["runs"][0]["records"][0]["citations"] = []
        result = monitor.analyze(data)
        self.assertEqual(result["history"][0]["critical_native_gaps"],
                         [{"run_id": "before", "platform": "demo-platform", "query_id": "q1"}])

    def test_16_raw_answer_and_native_metadata_preserved(self):
        data = controlled_observed_shape()
        raw = data["runs"][1]["records"][0]
        result = monitor.analyze(data)
        row = next(r for r in result["results"] if r["run_id"] == "after" and r["query_id"] == "q1")
        self.assertEqual(row["raw_record"], raw)
        self.assertEqual(row["raw_record"]["citations"][0]["title"], "模拟说明页")

    def test_17_no_pair_no_false_delta_and_bad_run_selection_rejected(self):
        data = controlled_observed_shape()
        data["runs"][1]["records"] = []
        comparison = monitor.analyze(data, "before", "after")["comparison"]
        self.assertIsNone(comparison["mention"]["delta_percentage_points"])
        for before, after in (("before", None), ("missing", "after"), ("after", "before")):
            with self.subTest(before=before, after=after), self.assertRaises(monitor.InputError):
                monitor.analyze(data, before, after)

    def test_20_modern_idna_keeps_distinct_domains_separate(self):
        self.assertEqual(monitor.domain_name("faß.de"), "xn--fa-hia.de")
        self.assertEqual(monitor.domain_name("FAẞ.DE."), "xn--fa-hia.de")
        self.assertEqual(monitor.domain_name("xn--fa-hia.de"), "xn--fa-hia.de")
        self.assertNotEqual(monitor.domain_name("βόλος.com"), monitor.domain_name("βόλοσ.com"))
        links = ["https://fass.de/", "https://docs.fass.de/",
                 "https://xn--fa-hia.de.evil.invalid/", "https://evil-xn--fa-hia.de/",
                 "https://faß.de/", "https://xn--fa-hia.de/", "https://docs.faß.de./"]
        record = {"answer": "Controlled domain test", "citations": links}
        for domain in ("faß.de", "xn--fa-hia.de"):
            with self.subTest(domain=domain):
                brand = {"name": "Example", "domains": [domain]}
                hits = monitor.inspect_answer(record, brand)["matched_native_citations"]
                self.assertEqual([hit["position"] for hit in hits], [5, 6, 7])
                self.assertEqual([hit["host"] for hit in hits],
                                 ["xn--fa-hia.de", "xn--fa-hia.de", "docs.xn--fa-hia.de"])
                brand["include_subdomains"] = False
                hits = monitor.inspect_answer(record, brand)["matched_native_citations"]
                self.assertEqual([hit["position"] for hit in hits], [5, 6])
        for domain in ("xn--a.de", "ab\u200dcd.de"):
            with self.subTest(domain=domain), self.assertRaises(monitor.InputError):
                monitor.domain_name(domain)

    def test_21_not_run_optional_source_is_validated_and_remains_unmeasured(self):
        full_source = {"kind": "export", "executor": "unknown", "reference": "fixture:unrun/q1"}
        for fields in ({}, {"source": None}, {"source": full_source}):
            with self.subTest(fields=fields):
                data = controlled_not_run_shape()
                data["runs"][0]["records"][0].update(fields)
                result = monitor.analyze(data)
                self.assertEqual(result["overall"]["status_counts"]["not_run"], 6)
                self.assertEqual(result["overall"]["effective_answers"], 0)
                self.assertIsNone(result["overall"]["native_citation_rate"])
                row = result["results"][0]
                self.assertEqual(row["source"], fields.get("source"))
                self.assertIsNone(row["native_cited"])
                report = monitor.report_text(result)
                self.assertNotIn("0.0%", report)
                self.assertIn("export / unknown / fixture:unrun/q1" if fields.get("source")
                              else "无采集来源", report)

    def test_25_nested_nonfinite_numbers_rejected_by_analysis(self):
        for value in (float("inf"), float("-inf"), float("nan")):
            for location in ("citation", "record", "unused_input"):
                with self.subTest(value=value, location=location):
                    data = controlled_observed_shape()
                    metadata = {"nested": [None, {"score": value}]}
                    if location == "citation":
                        data["runs"][0]["records"][0]["citations"] = [
                            {"url": "https://example.com/guide", "metadata": metadata}]
                    elif location == "record":
                        data["runs"][0]["records"][0]["metadata"] = metadata
                    else:
                        data["unused_input"] = metadata
                    with self.assertRaisesRegex(monitor.InputError, "non-finite JSON number"):
                        monitor.analyze(data)

    def test_26_finite_metadata_preserved_without_changing_statistics(self):
        data = controlled_observed_shape()
        baseline = monitor.analyze(data, "before", "after")
        metadata = {"scores": [1e308, -1e308, 0.0, 1e-308, 17, True, None]}
        data["runs"][0]["records"][0]["metadata"] = metadata
        data["unused_input"] = {"nested": [metadata]}
        result = monitor.analyze(data, "before", "after")
        for key in ("overall", "history", "by_platform", "by_category", "comparison"):
            self.assertEqual(result[key], baseline[key])
        self.assertEqual(result["results"][0]["raw_record"]["metadata"], metadata)
        json.dumps(result, allow_nan=False)


class CliTests(unittest.TestCase):
    def run_cli(self, input_file, output, cwd, script=None, extra=()):
        return subprocess.run([sys.executable, str(script or ROOT / "scripts/citation_monitor.py"),
                               "--input", str(input_file), "--output", str(output), *extra],
                              cwd=cwd, capture_output=True, text=True, check=False)

    def test_18_portable_cli_matches_shipped_business_outputs(self):
        with tempfile.TemporaryDirectory(prefix="citation-monitor-selftest-") as tmp:
            tmp = Path(tmp)
            # Deliberately copy only executable/data, without host dirs, icons or LICENSE.
            script = tmp / "portable/scripts/citation_monitor.py"
            script.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "scripts/citation_monitor.py", script)
            for sample, input_name, extra in (
                ("success", "six-questions.json", ("--before", "before", "--after", "after")),
                ("failure", "all-failed.json", ())
            ):
                input_file = tmp / input_name
                shutil.copyfile(ROOT / "examples" / sample / input_name, input_file)
                out = tmp / sample
                completed = self.run_cli(input_file, out, tmp, script, extra)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                for name in ("前后对照报告.md", "逐平台问题结果.json", "未成功采集清单.md"):
                    self.assertEqual((out / name).read_text(encoding="utf-8"),
                                     (ROOT / "examples" / sample / "output" / name).read_text(encoding="utf-8"))
                repeated = self.run_cli(input_file, out, tmp, script, extra)
                self.assertEqual(repeated.returncode, 2)
                self.assertIn("new or empty", repeated.stderr)

    def test_19_invalid_cli_input_rejected_without_partial_report(self):
        with tempfile.TemporaryDirectory(prefix="citation-monitor-selftest-") as tmp:
            tmp = Path(tmp)
            completed = self.run_cli(ROOT / "examples/failure/missing-citations.json", tmp / "out", tmp)
            self.assertEqual(completed.returncode, 2)
            self.assertIn("citations required", completed.stderr)
            self.assertFalse((tmp / "out").exists())
            for text in ('{"schema_version":1,"schema_version":1}', '{"x":NaN}'):
                invalid = tmp / "invalid.json"
                invalid.write_text(text, encoding="utf-8")
                completed = self.run_cli(invalid, tmp / "out", tmp)
                self.assertEqual(completed.returncode, 2)
                self.assertNotIn("Traceback", completed.stderr)

    def test_22_idna_cli_counts_only_the_owned_domain(self):
        data = controlled_observed_shape()
        data["brand"]["domains"] = ["faß.de"]
        data["queries"] = data["queries"][:2]
        data["runs"] = data["runs"][:1]
        data["runs"][0]["records"] = data["runs"][0]["records"][:2]
        data["runs"][0]["records"][0]["citations"] = ["https://fass.de/"]
        data["runs"][0]["records"][1]["citations"] = ["https://xn--fa-hia.de/"]
        with tempfile.TemporaryDirectory(prefix="citation-monitor-selftest-") as tmp:
            tmp = Path(tmp)
            input_file = tmp / "idna.json"
            input_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            completed = self.run_cli(input_file, tmp / "out", tmp)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads((tmp / "out/逐平台问题结果.json").read_text(encoding="utf-8"))
            self.assertEqual(result["overall"]["native_cited_answers"], 1)
            self.assertEqual(result["overall"]["native_citation_rate"], 0.5)
            self.assertEqual([row["native_cited"] for row in result["results"]], [False, True])
            self.assertEqual(result["results"][1]["matched_native_citations"][0]["host"], "xn--fa-hia.de")

    def test_23_invalid_not_run_source_exits_two_without_reports(self):
        valid = {"kind": "export", "executor": "unknown", "reference": "fixture:unrun/q1"}
        invalid_sources = ["export", [], False, {}, {"kind": "export"}]
        for key in valid:
            missing = dict(valid)
            del missing[key]
            invalid_sources.append(missing)
            for value in (None, "", " ", [], 1):
                invalid_sources.append({**valid, key: value})
        invalid_sources.append({**valid, "kind": "unrecognized"})
        with tempfile.TemporaryDirectory(prefix="citation-monitor-selftest-") as tmp:
            tmp = Path(tmp)
            input_file = tmp / "unrun.json"
            for source in invalid_sources:
                with self.subTest(source=source):
                    data = controlled_not_run_shape()
                    data["runs"][0]["records"][0]["source"] = source
                    with self.assertRaises(monitor.InputError):
                        monitor.analyze(data)
                    input_file.write_text(json.dumps(data), encoding="utf-8")
                    completed = self.run_cli(input_file, tmp / "out", tmp)
                    self.assertEqual(completed.returncode, 2, completed.stderr)
                    self.assertIn("source", completed.stderr)
                    self.assertNotIn("Traceback", completed.stderr)
                    self.assertFalse((tmp / "out").exists())

    def test_24_not_run_source_defaults_and_complete_source_deliver_reports(self):
        cases = ({}, {"source": None}, {"source": {
            "kind": "export", "executor": "unknown", "reference": "fixture:unrun/q1"}})
        with tempfile.TemporaryDirectory(prefix="citation-monitor-selftest-") as tmp:
            tmp = Path(tmp)
            input_file = tmp / "unrun.json"
            for index, fields in enumerate(cases):
                with self.subTest(fields=fields):
                    data = controlled_not_run_shape()
                    data["runs"][0]["records"][0].update(fields)
                    input_file.write_text(json.dumps(data), encoding="utf-8")
                    out = tmp / str(index)
                    completed = self.run_cli(input_file, out, tmp)
                    self.assertEqual(completed.returncode, 0, completed.stderr)
                    result = json.loads((out / "逐平台问题结果.json").read_text(encoding="utf-8"))
                    self.assertEqual(result["overall"]["planned"], 6)
                    self.assertEqual(result["overall"]["effective_answers"], 0)
                    self.assertIsNone(result["overall"]["native_citation_rate"])
                    self.assertEqual(result["results"][0]["source"], fields.get("source"))
                    report = (out / "前后对照报告.md").read_text(encoding="utf-8")
                    self.assertIn("无采集来源", report)
                    self.assertNotIn("0.0%", report)
                    gaps = (out / "未成功采集清单.md").read_text(encoding="utf-8")
                    self.assertIn(data["runs"][0]["records"][0]["reason"], gaps)

    def test_27_nested_nonfinite_json_exits_two_without_touching_outputs(self):
        with tempfile.TemporaryDirectory(prefix="citation-monitor-selftest-") as tmp:
            tmp = Path(tmp)
            input_file = tmp / "nonfinite.json"
            for token in ("1e309", "-1e309", "NaN", "Infinity", "-Infinity"):
                for location in ("citation", "record", "unused_input"):
                    data = controlled_observed_shape()
                    metadata = {"nested": [None, {"score": "NONFINITE_TOKEN"}]}
                    if location == "citation":
                        data["runs"][0]["records"][0]["citations"] = [
                            {"url": "https://example.com/guide", "metadata": metadata}]
                    elif location == "record":
                        data["runs"][0]["records"][0]["metadata"] = metadata
                    else:
                        data["unused_input"] = metadata
                    text = json.dumps(data).replace('"NONFINITE_TOKEN"', token)
                    input_file.write_text(text, encoding="utf-8")
                    for state in ("missing", "empty", "prior_reports"):
                        with self.subTest(token=token, location=location, output=state):
                            out = tmp / "out"
                            if state != "missing":
                                out.mkdir()
                            if state == "prior_reports":
                                (out / "逐平台问题结果.json").write_bytes(b"prior evidence\n")
                            before = {p.name: p.read_bytes() for p in out.iterdir()} if out.exists() else None
                            completed = self.run_cli(input_file, out, tmp)
                            self.assertEqual(completed.returncode, 2, completed.stderr)
                            self.assertIn("non-finite JSON number", completed.stderr)
                            self.assertNotIn("Traceback", completed.stderr)
                            after = {p.name: p.read_bytes() for p in out.iterdir()} if out.exists() else None
                            self.assertEqual(after, before)
                            if out.exists():
                                shutil.rmtree(out)

    def test_28_finite_json_extremes_roundtrip_without_changing_statistics(self):
        data = controlled_observed_shape()
        baseline = monitor.analyze(data, "before", "after")
        values = [1e308, -1e308, 1e-308, 0.0, 17, True, None]
        data["runs"][0]["records"][0]["metadata"] = {"scores": values}
        with tempfile.TemporaryDirectory(prefix="citation-monitor-selftest-") as tmp:
            tmp = Path(tmp)
            input_file = tmp / "finite.json"
            input_file.write_text(json.dumps(data), encoding="utf-8")
            completed = self.run_cli(input_file, tmp / "out", tmp,
                                     extra=("--before", "before", "--after", "after"))
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads((tmp / "out/逐平台问题结果.json").read_text(encoding="utf-8"))
            for key in ("overall", "history", "by_platform", "by_category", "comparison"):
                self.assertEqual(result[key], baseline[key])
            self.assertEqual(result["results"][0]["raw_record"]["metadata"]["scores"], values)


if __name__ == "__main__":
    print("Offline controlled regression tests; no live AI collection.", flush=True)
    unittest.main(verbosity=2)
