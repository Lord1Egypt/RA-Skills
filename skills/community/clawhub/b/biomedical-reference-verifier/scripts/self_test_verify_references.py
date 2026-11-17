#!/usr/bin/env python3
"""Offline smoke tests for verify_references.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("verify_references.py")
CONVERTER = Path(__file__).with_name("convert_reference_artifact.py")
HTML_GENERATOR = Path(__file__).with_name("generate_html_report.py")
HTML_TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "reference-audit-report-template.html"


def write_records(path: Path) -> None:
    payload = {
        "schema": "biomedical-reference-verifier.records.v1",
        "records": [
            {
                "index": 1,
                "source": {
                    "original_text": "John Smith. DNA methylation in human embryos. Journal Name. 2024.",
                    "title": "DNA methylation in human embryos",
                    "authors": ["John Smith"],
                    "year": "2024",
                    "journal": "Journal Name",
                    "volume": "",
                    "issue": "",
                    "pages": "",
                    "identifiers": {"doi": "", "pmid": "", "urls": []},
                },
            }
        ],
    }
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def run_verifier(records: Path, output_dir: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(SCRIPT),
        str(records),
        "--input-mode",
        "records",
        "--pipeline",
        "format-only",
        "--citation-style",
        "ama",
        "--output-dir",
        str(output_dir),
        *extra,
    ]
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    if result.returncode != 0:
        raise AssertionError(f"command failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")


def test_default_outputs() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        out = root / "out"
        write_records(records)
        stale_json = out / "reference-audit.json"
        out.mkdir()
        stale_json.write_text("stale", encoding="utf-8")

        result = run_verifier(records, out)
        assert_ok(result)
        assert (out / "reference-audit-summary.md").exists()
        assert (out / "reference-audit-detail.md").exists()
        assert (out / "reference-audit-report.html").exists()
        assert (out / "references.auto-fixed.md").exists()
        assert (out / "reference-normalized-records.json").exists()
        assert not (out / "reference-normalized-input.md").exists()
        assert not (out / "references.extracted.md").exists()
        assert stale_json.read_text() == "stale"
        fixed = (out / "references.auto-fixed.md").read_text(encoding="utf-8")
        assert ".." not in fixed
        assert "Smith J. DNA methylation in human embryos. Journal Name. 2024." in fixed
        html_report = (out / "reference-audit-report.html").read_text(encoding="utf-8")
        assert "/*__REFERENCE_AUDIT_DATA__*/" not in html_report
        assert '"report_category":"unchecked"' in html_report
        assert "仅格式整理" in html_report


def test_cleanup_all() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        out = root / "out"
        write_records(records)
        result = run_verifier(records, out, "--cleanup-process-files", "all")
        assert_ok(result)
        assert (out / "reference-audit-summary.md").exists()
        assert (out / "reference-audit-detail.md").exists()
        assert (out / "references.auto-fixed.md").exists()
        assert not (out / "reference-normalized-records.json").exists()
        assert not (out / "reference-normalized-input.md").exists()
        assert not (out / "references.extracted.md").exists()


def test_keep_process_json() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        out = root / "out"
        write_records(records)
        result = run_verifier(records, out, "--keep-process-json")
        assert_ok(result)
        assert (out / "reference-audit.json").exists()


def test_bad_cleanup_label() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        out = root / "out"
        write_records(records)
        result = run_verifier(records, out, "--cleanup-process-files", "unknown_label")
        assert result.returncode == 2
        assert "Unknown process file label" in result.stderr


def test_modes_and_runtime_summary() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        out = root / "out"
        write_records(records)
        result = run_verifier(records, out, "--mode", "fast")
        assert_ok(result)
        summary = (out / "reference-audit-summary.md").read_text(encoding="utf-8")
        assert "## Runtime performance" in summary
        assert "Mode: `fast`" in summary


def test_explicit_prior_result_reuse() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        first = root / "first"
        second = root / "second"
        write_records(records)
        initial = run_verifier(records, first, "--keep-process-json")
        assert_ok(initial)
        reused = run_verifier(records, second, "--reuse-results", str(first / "reference-audit.json"))
        assert_ok(reused)
        summary = (second / "reference-audit-summary.md").read_text(encoding="utf-8")
        assert "Reused prior results: `1`" in summary


def test_audit_index_round_trip_and_index_reuse() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        audit_dir = root / "audit"
        reused_dir = root / "reused"
        index = root / "reference-index.json"
        round_trip = root / "round-trip-audit.json"
        write_records(records)
        initial = run_verifier(records, audit_dir, "--keep-process-json")
        assert_ok(initial)
        audit = audit_dir / "reference-audit.json"
        to_index = subprocess.run([sys.executable, str(CONVERTER), str(audit), "--to", "index", "--output", str(index)], text=True, capture_output=True)
        assert_ok(to_index)
        to_audit = subprocess.run([sys.executable, str(CONVERTER), str(index), "--to", "audit", "--output", str(round_trip)], text=True, capture_output=True)
        assert_ok(to_audit)
        original_payload = json.loads(audit.read_text(encoding="utf-8"))
        round_payload = json.loads(round_trip.read_text(encoding="utf-8"))
        assert round_payload == original_payload
        reused = run_verifier(records, reused_dir, "--reuse-results", str(index))
        assert_ok(reused)
        summary = (reused_dir / "reference-audit-summary.md").read_text(encoding="utf-8")
        assert "Reused prior results: `1`" in summary


def test_modified_artifact_tolerance() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        first = root / "first"
        second = root / "second"
        modified = root / "modified.json"
        malformed = root / "malformed.json"
        write_records(records)
        initial = run_verifier(records, first, "--keep-process-json")
        assert_ok(initial)
        payload = json.loads((first / "reference-audit.json").read_text(encoding="utf-8"))
        payload["results"].insert(0, "user note")
        payload["results"].append({"original": "incomplete user-edited row"})
        modified.write_text(json.dumps(payload), encoding="utf-8")
        tolerant = run_verifier(records, second, "--reuse-results", str(modified))
        assert_ok(tolerant)
        assert "Ignored 2 incomplete prior result row(s)" in tolerant.stderr
        malformed.write_text("{broken", encoding="utf-8")
        rejected = run_verifier(records, root / "rejected", "--reuse-results", str(malformed))
        assert rejected.returncode == 2
        assert "Cannot read prior artifact" in rejected.stderr


def test_field_level_prior_reuse_after_punctuation_change() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        first = root / "first"
        second = root / "second"
        write_records(records)
        initial = run_verifier(records, first, "--keep-process-json")
        assert_ok(initial)
        payload = json.loads(records.read_text(encoding="utf-8"))
        payload["records"][0]["source"]["original_text"] = "John Smith — DNA methylation in human embryos; Journal Name (2024)."
        records.write_text(json.dumps(payload), encoding="utf-8")
        reused = run_verifier(records, second, "--reuse-results", str(first / "reference-audit.json"))
        assert_ok(reused)
        summary = (second / "reference-audit-summary.md").read_text(encoding="utf-8")
        assert "Reused prior results: `1`" in summary


def test_optional_index_output() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        records = root / "records.json"
        out = root / "out"
        reused_out = root / "reused"
        write_records(records)
        generated = run_verifier(records, out, "--write-index")
        assert_ok(generated)
        index = out / "reference-index.json"
        assert index.exists()
        payload = json.loads(index.read_text(encoding="utf-8"))
        assert payload["schema"] == "biomedical-reference-verifier.index.v1"
        reused = run_verifier(records, reused_out, "--reuse-results", str(index))
        assert_ok(reused)
        assert "Reused prior results: `1`" in (reused_out / "reference-audit-summary.md").read_text(encoding="utf-8")


def test_html_report_preserves_order_and_escapes_script_text() -> None:
    with tempfile.TemporaryDirectory(prefix="bioverifier-test-") as tmp:
        root = Path(tmp)
        audit = root / "audit.json"
        output = root / "report.html"
        payload = {
            "input": "records.json",
            "format_consistency": {"majority_format": "ama"},
            "runtime": {"mode": "balanced", "elapsed_seconds": 1.2},
            "results": [
                {"index": 20, "status": "verified", "severity": "none", "original": "SECOND-SOURCE-ORDER", "parsed_title": "Second", "canonical": None},
                {"index": 3, "status": "total_fabrication", "severity": "high", "original": "FIRST-SOURCE-ORDER</script><script>alert(1)</script>", "parsed_title": "First", "canonical": None},
            ],
        }
        audit.write_text(json.dumps(payload), encoding="utf-8")
        generated = subprocess.run(
            [sys.executable, str(HTML_GENERATOR), str(audit), "--output", str(output)],
            text=True,
            capture_output=True,
            check=False,
        )
        assert_ok(generated)
        html_report = output.read_text(encoding="utf-8")
        assert html_report.index("SECOND-SOURCE-ORDER") < html_report.index("FIRST-SOURCE-ORDER")
        assert "</script><script>alert(1)</script>" not in html_report
        assert "\\u003c/script\\u003e" in html_report
        assert '"correct":1' in html_report
        assert '"blocked":1' in html_report


def test_html_template_keeps_color_scoped_to_confidence_groups() -> None:
    template = HTML_TEMPLATE.read_text(encoding="utf-8")
    assert "<script src=" not in template
    assert '<link rel="stylesheet"' not in template
    assert "<details" not in template
    assert 'id="search"' in template and 'id="status"' in template
    assert 'id="field"' in template and 'id="reset"' in template
    assert 'aria-live="polite"' in template


def main() -> int:
    tests = [
        test_default_outputs,
        test_cleanup_all,
        test_keep_process_json,
        test_bad_cleanup_label,
        test_modes_and_runtime_summary,
        test_explicit_prior_result_reuse,
        test_audit_index_round_trip_and_index_reuse,
        test_modified_artifact_tolerance,
        test_field_level_prior_reuse_after_punctuation_change,
        test_optional_index_output,
        test_html_report_preserves_order_and_escapes_script_text,
        test_html_template_keeps_color_scoped_to_confidence_groups,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
