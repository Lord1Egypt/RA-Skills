from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "verify-release.py"


def run_verify_release(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(ROOT), *args],
        capture_output=True,
        text=True,
        timeout=30,
    )


def test_verify_release_script_exists_and_reports_default_plan():
    assert SCRIPT.exists(), "scripts/verify-release.py should exist"

    result = run_verify_release("--dry-run", "--format", "json")
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    assert [step["name"] for step in payload["steps"]] == [
        "pytest",
        "skill-evals",
    ]
    assert any("python -m pytest scripts/tests -q" in step["command"] for step in payload["steps"])
    skill_step = next(step for step in payload["steps"] if step["name"] == "skill-evals")
    assert "scripts/run-skill-evals.py" in skill_step["command"]
    assert "--runner fixture" in skill_step["command"]
    assert "--normalized-trace" not in skill_step["command"]


def test_verify_release_respects_skip_flags():
    result = run_verify_release("--dry-run", "--format", "json", "--skip-pytest")
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    assert [step["name"] for step in payload["steps"]] == ["skill-evals"]


def test_verify_release_trace_skill_evals_accept_normalized_trace(tmp_path: Path):
    trace = tmp_path / "trace.json"
    trace.write_text("{}", encoding="utf-8")
    result = run_verify_release(
        "--dry-run",
        "--format",
        "json",
        "--skill-evals-runner",
        "trace",
        "--skill-evals-case-id",
        "negative-report",
        "--skill-evals-normalized-trace",
        str(trace),
    )
    assert result.returncode == 0, result.stdout + result.stderr

    payload = json.loads(result.stdout)
    skill_step = next(step for step in payload["steps"] if step["name"] == "skill-evals")
    assert "--runner trace" in skill_step["command"]
    assert "--normalized-trace" in skill_step["command"]


def test_verify_release_rejects_trace_runner_without_normalized_trace():
    result = run_verify_release(
        "--dry-run",
        "--format",
        "json",
        "--skill-evals-runner",
        "trace",
    )

    assert result.returncode != 0
    assert "--skill-evals-runner 'trace' requires --skill-evals-normalized-trace and --skill-evals-case-id" in result.stderr
