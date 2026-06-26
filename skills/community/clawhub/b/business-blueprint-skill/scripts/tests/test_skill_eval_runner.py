from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "run-skill-evals.py"
FIXTURES = ROOT / "scripts" / "tests" / "fixtures" / "skill-evals"


def run_script(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_prompt_manifest_paths_exist():
    manifest = ROOT / "evals" / "blueprint-skill-prompts.csv"
    assert manifest.exists()
    for line in manifest.read_text(encoding="utf-8").splitlines()[1:]:
        fields = line.split(",")
        assert (ROOT / fields[3]).is_file(), fields[3]


def test_fixture_runner_scores_all_cases_with_four_categories(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["summary"]["total"] == 6
    assert payload["summary"]["passed"] == 6
    assert payload["summary"]["failed"] == 0
    assert payload["summary"]["average_score"] >= 93
    for category in ["outcome", "process", "style", "efficiency"]:
        assert category in payload["summary"]["average_category_scores"]
        assert payload["summary"]["average_category_scores"][category] > 0


def test_fixture_runner_scores_success_case_and_style_fixture(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "explicit-blueprint",
        "--normalized-trace",
        str(FIXTURES / "explicit-blueprint-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    case = json.loads(result.stdout)["cases"][0]
    assert case["scores"] == {
        "outcome": 25,
        "process": 25,
        "style": 25,
        "efficiency": 25,
    }
    assert case["total_score"] == 100
    assert case["passed"] is True
    assert case["eval_complete"] is True
    assert case["style_rubric"]["source"] == "fixture"
    assert case["style_rubric"]["score"] >= 90
    assert case["metrics"]["runner"] == "fixture"
    assert "solution.blueprint.json" in "\n".join(case["metrics"]["artifact_paths"])


def test_positive_case_without_style_rubric_is_eval_incomplete(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "explicit-blueprint",
        "--normalized-trace",
        str(FIXTURES / "explicit-blueprint-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--disable-fixture-style-rubric",
        "--format",
        "json",
    )

    assert result.returncode == 1
    case = json.loads(result.stdout)["cases"][0]
    assert case["scores"]["style"] == 15
    assert case["total_score"] == 90
    assert case["passed"] is False
    assert case["eval_complete"] is False
    assert "style.rubric_missing" in case["failures"]
    assert "eval.style_rubric_missing" in case["failures"]


def test_negative_case_allows_skill_contract_read_for_routing(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "negative-report",
        "--normalized-trace",
        str(FIXTURES / "negative-report-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    case = json.loads(result.stdout)["cases"][0]
    assert case["scores"] == {
        "outcome": 25,
        "process": 25,
        "style": 25,
        "efficiency": 25,
    }
    assert case["total_score"] == 100
    assert case["passed"] is True


def test_outcome_hard_gate_prevents_clean_process_from_passing(tmp_path: Path):
    result = run_script(
        "--runner",
        "fixture",
        "--case-id",
        "explicit-blueprint",
        "--normalized-trace",
        str(FIXTURES / "thrashy-normalized.json"),
        "--artifact-dir",
        str(tmp_path),
        "--format",
        "json",
    )

    assert result.returncode == 1
    case = json.loads(result.stdout)["cases"][0]
    assert case["passed"] is False
    assert case["scores"]["outcome"] == 0
    assert "outcome.missing_blueprint_artifact" in case["failures"]
    assert "efficiency.repeated_failed_command" in case["failures"]


def test_normalized_trace_runner_is_agent_agnostic(tmp_path: Path):
    trace = tmp_path / "custom-agent-normalized.json"
    trace.write_text(
        json.dumps(
            {
                "runner": "custom-agent",
                "trace_format_version": "normalized-v1",
                "tool_calls": [],
                "shell_commands": ["custom shell read SKILL.md"],
                "failed_shell_commands": [],
                "read_paths": ["SKILL.md"],
                "write_paths": [],
                "artifact_paths": [],
                "input_tokens": 1200,
                "output_tokens": 200,
                "wall_ms": 900,
                "run_completed": True,
                "skill_evidence": {
                    "skill_contract_read": True,
                    "blueprint_flow_observed": False,
                    "validate_observed": False,
                    "export_observed": False,
                    "projection_observed": False,
                },
                "runner_warnings": [],
            }
        ),
        encoding="utf-8",
    )

    result = run_script(
        "--runner",
        "trace",
        "--case-id",
        "negative-report",
        "--normalized-trace",
        str(trace),
        "--artifact-dir",
        str(tmp_path / "artifacts"),
        "--format",
        "json",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    case = json.loads(result.stdout)["cases"][0]
    assert case["metrics"]["runner"] == "custom-agent"
    assert case["scores"] == {
        "outcome": 25,
        "process": 25,
        "style": 25,
        "efficiency": 25,
    }


def test_incomplete_run_cannot_pass_negative_case(tmp_path: Path):
    trace = tmp_path / "timeout-normalized.json"
    trace.write_text(
        json.dumps(
            {
                "runner": "custom-agent",
                "trace_format_version": "normalized-v1",
                "tool_calls": [],
                "shell_commands": [],
                "failed_shell_commands": [],
                "read_paths": [],
                "write_paths": [],
                "artifact_paths": [],
                "input_tokens": None,
                "output_tokens": None,
                "wall_ms": 120000,
                "run_completed": False,
                "skill_evidence": {
                    "skill_contract_read": False,
                    "blueprint_flow_observed": False,
                    "validate_observed": False,
                    "export_observed": False,
                },
                "runner_warnings": ["trace.timeout:120.0s"],
            }
        ),
        encoding="utf-8",
    )

    result = run_script(
        "--runner",
        "trace",
        "--case-id",
        "negative-report",
        "--normalized-trace",
        str(trace),
        "--artifact-dir",
        str(tmp_path / "artifacts"),
        "--format",
        "json",
    )

    assert result.returncode == 1
    case = json.loads(result.stdout)["cases"][0]
    assert case["passed"] is False
    assert "runner.run_incomplete" in case["failures"]
