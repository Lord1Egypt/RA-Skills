import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"


def run_cli(args, *, cwd=None, input_text=None):
    return subprocess.run(
        [sys.executable, *args],
        cwd=cwd or REPO_ROOT,
        input=input_text,
        text=True,
        capture_output=True,
    )


def test_grep_json_schema_and_summary_pipeline(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "service.py").write_text(
        "old_status = 'legacy'\nprint(old_status)\n",
        encoding="utf-8",
    )
    (project / "README.md").write_text(
        "This document still references old_status.\n",
        encoding="utf-8",
    )

    grep_result = run_cli([
        str(SCRIPTS_DIR / "grep_legacy.py"),
        str(project),
        "old_status",
        "--json",
    ])
    assert grep_result.returncode == 0, grep_result.stderr

    payload = json.loads(grep_result.stdout)
    assert payload["tool"] == "grep_legacy"
    assert payload["schema_version"] == "1.0"
    assert payload["summary"]["total_hits"] == 3
    assert payload["summary"]["total_files"] == 2
    assert payload["errors"] == []

    summary_result = run_cli(
        [str(SCRIPTS_DIR / "summarize_impacts.py")],
        input_text=grep_result.stdout,
    )
    assert summary_result.returncode == 0, summary_result.stderr
    assert "## Impact Summary" in summary_result.stdout
    assert "**Input type**: `grep_legacy`" in summary_result.stdout


def test_scan_json_schema_and_summary_pipeline(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "config_a.py").write_text('DB_PATH = "/tmp/a.db"\n', encoding="utf-8")
    (project / "config_b.py").write_text('DB_PATH = "/tmp/b.db"\n', encoding="utf-8")

    scan_result = run_cli([
        str(SCRIPTS_DIR / "scan_contract_drift.py"),
        str(project),
        "--json",
    ])
    assert scan_result.returncode == 0, scan_result.stderr

    payload = json.loads(scan_result.stdout)
    assert payload["tool"] == "scan_contract_drift"
    assert payload["schema_version"] == "1.0"
    assert payload["summary"]["total_findings"] == 1
    assert payload["results"][0]["category"] == "config_definition"
    assert payload["results"][0]["files"] == ["config_a.py", "config_b.py"]
    assert payload["results"][0]["evidence"][0]["filepath"] in {"config_a.py", "config_b.py"}

    summary_result = run_cli(
        [str(SCRIPTS_DIR / "summarize_impacts.py")],
        input_text=scan_result.stdout,
    )
    assert summary_result.returncode == 0, summary_result.stderr
    assert "## Contract Drift Summary" in summary_result.stdout
    assert "**Input type**: `scan_contract_drift`" in summary_result.stdout


def test_scan_does_not_flag_plain_main_functions_as_entry_point_drift(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "a.py").write_text("def main():\n    pass\n", encoding="utf-8")
    (project / "b.py").write_text("def main():\n    pass\n", encoding="utf-8")

    scan_result = run_cli([
        str(SCRIPTS_DIR / "scan_contract_drift.py"),
        str(project),
        "--json",
    ])
    assert scan_result.returncode == 0, scan_result.stderr

    payload = json.loads(scan_result.stdout)
    categories = [item["category"] for item in payload["results"]]
    assert "entry_point" not in categories
    assert payload["summary"]["total_findings"] == 0


def test_scan_ignores_reference_only_pattern_mentions(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "references").mkdir()
    (project / "references" / "risk_patterns.md").write_text(
        "lifecycle_status is an example legacy field.\n",
        encoding="utf-8",
    )
    (project / "scripts").mkdir()
    (project / "scripts" / "scan.py").write_text(
        "PATTERNS = [r'lifecycle_status']\n",
        encoding="utf-8",
    )

    scan_result = run_cli([
        str(SCRIPTS_DIR / "scan_contract_drift.py"),
        str(project),
        "--json",
    ])
    assert scan_result.returncode == 0, scan_result.stderr

    payload = json.loads(scan_result.stdout)
    assert payload["summary"]["total_findings"] == 0


def test_scan_strict_mode_counts_reference_mentions(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "references").mkdir()
    (project / "references" / "risk_patterns.md").write_text(
        "lifecycle_status is an example legacy field.\n",
        encoding="utf-8",
    )
    (project / "scripts").mkdir()
    (project / "scripts" / "scan.py").write_text(
        "PATTERNS = [r'lifecycle_status']\n",
        encoding="utf-8",
    )

    scan_result = run_cli([
        str(SCRIPTS_DIR / "scan_contract_drift.py"),
        str(project),
        "--json",
        "--mode",
        "strict",
    ])
    assert scan_result.returncode == 0, scan_result.stderr

    payload = json.loads(scan_result.stdout)
    assert payload["summary"]["total_findings"] == 1
    assert payload["results"][0]["files"] == ["references/risk_patterns.md", "scripts/scan.py"]


def test_scan_lite_mode_down_ranks_lower_risk_categories(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "service_a.py").write_text("class DemoService:\n    pass\n", encoding="utf-8")
    (project / "service_b.py").write_text("class DemoService:\n    pass\n", encoding="utf-8")

    scan_result = run_cli([
        str(SCRIPTS_DIR / "scan_contract_drift.py"),
        str(project),
        "--json",
        "--mode",
        "lite",
    ])
    assert scan_result.returncode == 0, scan_result.stderr

    payload = json.loads(scan_result.stdout)
    assert payload["summary"]["total_findings"] == 1
    assert payload["results"][0]["category"] == "entry_point"
    assert payload["results"][0]["severity"] == "low"


def test_grep_invalid_regex_returns_structured_error(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()
    (project / "file.py").write_text("value = 1\n", encoding="utf-8")

    result = run_cli([
        str(SCRIPTS_DIR / "grep_legacy.py"),
        str(project),
        "(",
        "--regex",
        "--json",
    ])
    assert result.returncode == 2

    payload = json.loads(result.stdout)
    assert payload["tool"] == "grep_legacy"
    assert payload["results"] == []
    assert payload["errors"][0]["type"] == "invalid_regex"
    assert "Invalid regular expression" in payload["errors"][0]["message"]


def test_summarize_supports_legacy_grep_payload(tmp_path):
    legacy_payload = {
        "module.py": [
            {"line": 3, "text": "legacy_name = 1", "pattern": "legacy_name"}
        ]
    }
    payload_file = tmp_path / "legacy_grep.json"
    payload_file.write_text(json.dumps(legacy_payload), encoding="utf-8")

    result = run_cli([
        str(SCRIPTS_DIR / "summarize_impacts.py"),
        "--file",
        str(payload_file),
    ])
    assert result.returncode == 0, result.stderr
    assert "## Impact Summary" in result.stdout
