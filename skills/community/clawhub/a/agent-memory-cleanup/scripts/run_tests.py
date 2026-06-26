#!/usr/bin/env python3
"""Regression tests for agent-memory-cleanup."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "scripts" / "audit_memory.py"
FIXTURES = ROOT / "test-fixtures"


def run_cli(*args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(AUDIT), *args],
        cwd=str(ROOT),
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    return result.stdout


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_secret_redaction() -> None:
    output = run_cli(str(FIXTURES / "secret-memory.md"), "--json")
    assert_true("abc123-super-secret-value" not in output, "api key leaked in JSON output")
    assert_true("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in output, "bearer token leaked in JSON output")
    assert_true("glpat-abcdefghijklmnop" not in output, "gitlab token leaked in JSON output")
    assert_true("pypi-AgEIcHlwaS5vcmcCMTIzNDU2Nzg5" not in output, "pypi token leaked in JSON output")
    assert_true("npm_abcdefghijklmnopqrstuvwxyz" not in output, "npm token leaked in JSON output")
    assert_true("jfrog_abcdEFGHijklMNOP" not in output, "jfrog token leaked in JSON output")
    assert_true("[REDACTED_SECRET]" in output, "secret was not redacted")
    payload = json.loads(output)
    assert_true(payload[0]["findings"][1]["classification"] == "remove", "secret finding was not removed")


def test_clean_memory_no_diff() -> None:
    output = run_cli(str(FIXTURES / "clean-memory.md"), "--mode", "propose-patch", "--include-diff")
    assert_true("```diff" not in output, "clean memory produced unnecessary diff")
    assert_true("No cleanup needed" in output, "clean memory did not report no-op")


def test_noisy_memory_classification() -> None:
    output = run_cli(str(FIXTURES / "noisy-memory.md"), "--summary-json")
    assert_true("proposed_markdown" not in output, "summary-json should not include proposal payload")
    assert_true("```diff" not in output, "summary-json should not include diff payload")
    payload = json.loads(output)
    counts = payload["counts"]
    assert_true(counts["keep"] >= 3, "expected durable memories to be kept")
    assert_true(counts["condense"] >= 1, "expected duplicates or mixed entries to condense")
    assert_true(counts["remove"] >= 3, "expected stale task/secret entries to be removed")


def test_propose_patch_still_outputs_diff() -> None:
    output = run_cli(str(FIXTURES / "noisy-memory.md"), "--mode", "propose-patch", "--include-diff")
    assert_true("```diff" in output, "propose-patch no longer outputs diff")
    assert_true("Do not store secrets" in output, "propose-patch lost cleanup proposal")


def test_apply_approved_creates_backup() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "memory.md"
        shutil.copy2(FIXTURES / "noisy-memory.md", target)
        output = run_cli(str(target), "--mode", "apply-approved")
        backups = list(Path(tmp).glob("memory.md.bak-*"))
        cleaned = target.read_text(encoding="utf-8")
        assert_true(len(backups) == 1, "apply-approved did not create exactly one backup")
        assert_true("tomorrow" not in cleaned, "transient tomorrow note survived cleanup")
        assert_true("REDACTED_SECRET" not in cleaned, "redacted placeholder was written back to memory")
        assert_true("Backups created:" in output, "apply report did not include backup path")


def test_apply_approved_removes_real_secret_patterns() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "memory.md"
        shutil.copy2(FIXTURES / "secret-memory.md", target)
        run_cli(str(target), "--mode", "apply-approved")
        cleaned = target.read_text(encoding="utf-8")
        blocked = [
            "abc123-super-secret-value",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "glpat-abcdefghijklmnop",
            "pypi-AgEIcHlwaS5vcmcCMTIzNDU2Nzg5",
            "npm_abcdefghijklmnopqrstuvwxyz",
            "jfrog_abcdEFGHijklMNOP",
            "REDACTED_SECRET",
        ]
        assert_true(not any(value in cleaned for value in blocked), "apply-approved left secret material in final file")


def test_project_policy_skipped() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        policy = Path(tmp) / "AGENTS.md"
        policy.write_text("# Project Policy\n\n- Do not treat this as user memory.\n", encoding="utf-8")
        output = run_cli(str(policy), "--summary-json")
        payload = json.loads(output)
        assert_true(payload["files"][0]["status"].startswith("skipped"), "project policy file was not skipped")


def test_short_polluted_memory_intervenes() -> None:
    output = run_cli(str(FIXTURES / "short-polluted-memory.md"), "--summary-json")
    payload = json.loads(output)
    quality = payload["quality"]
    assert_true(quality["secret_count"] == 1, "short polluted fixture did not detect secret")
    assert_true(quality["task_state_count"] >= 1, "short polluted fixture did not detect task state")
    assert_true(quality["pollution_score"] >= 0.2, "short polluted fixture did not produce pollution score")
    assert_true(quality["intervention"] == "prompt_cleanup_now_secret_detected", "short polluted fixture did not trigger cleanup")


def test_candidate_lint_blocks_task_state() -> None:
    output = run_cli("--candidate", "Current task: tomorrow retry PR #302 on branch fix-memory", "--summary-json")
    payload = json.loads(output)
    quality = payload["quality"]
    assert_true(payload["files"][0]["status"].startswith("candidate"), "candidate lint did not create candidate report")
    assert_true(quality["intervention"] == "do_not_write_candidate_to_global_memory", "candidate task state was not blocked")


def test_conflict_fixture_intervenes() -> None:
    output = run_cli(str(FIXTURES / "conflicting-memory.md"), "--summary-json")
    payload = json.loads(output)
    quality = payload["quality"]
    assert_true(quality["conflict_count"] >= 1, "conflicting fixture did not detect conflicts")
    assert_true(
        quality["intervention"] == "prompt_user_review_conflicting_memory",
        "conflicting fixture did not request user review",
    )


def test_skill_prompt_is_lightweight() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    assert_true(len(skill_text) <= 6000, "SKILL.md is too large for lightweight use")
    assert_true("lightweight and low-noise" in skill_text, "skill does not preserve low-noise UX")
    assert_true("clear memory-state prompts" in skill_text, "skill does not preserve explicit user-facing prompts")


def test_unsupported_extensions_are_skipped() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_file = Path(tmp) / "memory.db"
        db_file.write_bytes(b"not markdown memory")
        output = run_cli(str(db_file), "--summary-json")
        payload = json.loads(output)
        assert_true(payload["files"][0]["status"].startswith("skipped: unsupported"), "unsupported extension was not skipped")


def test_skill_files_are_ascii_only() -> None:
    ignored_parts = {"__pycache__"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        data = path.read_bytes()
        assert_true(all(byte < 128 for byte in data), f"non-ASCII byte found in {path}")


def test_description_scope_is_narrow() -> None:
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"^description:\s*(.+)$", skill_text, flags=re.MULTILINE)
    assert_true(match is not None, "SKILL.md is missing description")
    description = match.group(1)
    assert_true(len(description) <= 750, "description is too long and may over-trigger")
    assert_true("explicitly asks" in description, "description should prefer explicit user memory cleanup requests")
    assert_true("memory write/update fails" in description, "description should preserve memory failure trigger")
    assert_true("Do not trigger for ordinary project docs" in description, "description should contain negative trigger guidance")
    too_broad = ["other agents", "repair", "periodically maintain"]
    for phrase in too_broad:
        assert_true(phrase not in description, f"description contains too-broad phrase: {phrase}")


def main() -> int:
    tests = [
        test_secret_redaction,
        test_clean_memory_no_diff,
        test_noisy_memory_classification,
        test_propose_patch_still_outputs_diff,
        test_apply_approved_creates_backup,
        test_apply_approved_removes_real_secret_patterns,
        test_project_policy_skipped,
        test_short_polluted_memory_intervenes,
        test_candidate_lint_blocks_task_state,
        test_conflict_fixture_intervenes,
        test_skill_prompt_is_lightweight,
        test_unsupported_extensions_are_skipped,
        test_skill_files_are_ascii_only,
        test_description_scope_is_narrow,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print("ALL_TESTS_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
