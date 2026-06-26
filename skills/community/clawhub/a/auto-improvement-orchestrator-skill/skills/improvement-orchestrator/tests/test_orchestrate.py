#!/usr/bin/env python3
"""Tests for the orchestrator dispatch pipeline."""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
REPO_ROOT = _REPO_ROOT

# ---------------------------------------------------------------------------
# Import the module directly via importlib (scripts dir is not a package).
# ---------------------------------------------------------------------------

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "orchestrate",
    REPO_ROOT / "skills" / "improvement-orchestrator" / "scripts" / "orchestrate.py",
)
orchestrate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(orchestrate)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_state(tmp_path):
    """Create a minimal state tree for testing."""
    for sub in ("candidate_versions", "rankings", "executions", "state", "receipts", "traces"):
        (tmp_path / sub).mkdir()
    # Seed state files so ensure_tree doesn't fail
    (tmp_path / "state" / "current_state.json").write_text("{}")
    (tmp_path / "state" / "pending_promote.json").write_text('{"pending":[], "last_updated":null}')
    (tmp_path / "state" / "veto.json").write_text('{"vetoes":[], "last_updated":null}')
    (tmp_path / "state" / "last_run.json").write_text("{}")
    return tmp_path


def _make_ranking_artifact(candidates: list[dict]) -> dict:
    """Build a minimal ranking artifact with scored_candidates."""
    return {
        "run_id": "test-run-001",
        "target": {"path": "/fake/target"},
        "scored_candidates": candidates,
        "truth_anchor": "/fake/ranking.json",
    }


def _make_execution_artifact(
    candidate_id: str = "cand-01-docs",
    status: str = "success",
    modified: bool = True,
    diff: str = "--- a\n+++ b\n@@ -1 +1,2 @@\n+new line",
) -> dict:
    return {
        "run_id": "test-run-001",
        "candidate_id": candidate_id,
        "result": {
            "status": status,
            "modified": modified,
            "diff": diff,
        },
        "truth_anchor": "/fake/execution.json",
    }


def _make_receipt(
    candidate_id: str = "cand-01-docs",
    decision: str = "keep",
    reason: str = "low-risk docs candidate",
    run_id: str = "test-run-001",
    blockers: list | None = None,
) -> dict:
    return {
        "run_id": run_id,
        "candidate_id": candidate_id,
        "decision": decision,
        "reason": reason,
        "blockers": blockers or [],
        "truth_anchor": "/fake/receipt.json",
    }


# ---------------------------------------------------------------------------
# Tests: find_best_accepted
# ---------------------------------------------------------------------------


class TestFindBestAccepted:
    def test_returns_first_accepted(self):
        ranking = _make_ranking_artifact([
            {"id": "cand-01", "score": 8.0, "recommendation": "accept_for_execution"},
            {"id": "cand-02", "score": 7.0, "recommendation": "accept_for_execution"},
            {"id": "cand-03", "score": 6.0, "recommendation": "hold"},
        ])
        best = orchestrate.find_best_accepted(ranking)
        assert best is not None
        assert best["id"] == "cand-01"

    def test_returns_none_when_no_accepted(self):
        ranking = _make_ranking_artifact([
            {"id": "cand-01", "score": 5.0, "recommendation": "hold"},
            {"id": "cand-02", "score": 3.0, "recommendation": "reject"},
        ])
        best = orchestrate.find_best_accepted(ranking)
        assert best is None

    def test_returns_none_for_empty_candidates(self):
        ranking = _make_ranking_artifact([])
        best = orchestrate.find_best_accepted(ranking)
        assert best is None

    def test_skips_non_accepted(self):
        ranking = _make_ranking_artifact([
            {"id": "cand-01", "score": 9.0, "recommendation": "hold"},
            {"id": "cand-02", "score": 7.5, "recommendation": "accept_for_execution"},
        ])
        best = orchestrate.find_best_accepted(ranking)
        assert best["id"] == "cand-02"


# ---------------------------------------------------------------------------
# Tests: extract_failure_trace
# ---------------------------------------------------------------------------


class TestExtractFailureTrace:
    def test_writes_trace_file(self, tmp_state):
        receipt = _make_receipt(
            decision="revert",
            reason="execution failed validation",
            blockers=["risk_medium"],
        )
        execution = _make_execution_artifact(status="error", diff="some diff")

        trace_path = orchestrate.extract_failure_trace(
            receipt, execution, str(tmp_state),
        )

        path = Path(trace_path)
        assert path.exists()
        assert path.suffix == ".json"

        trace = json.loads(path.read_text())
        assert trace["type"] == "failure_trace"
        assert trace["candidate_id"] == "cand-01-docs"
        assert trace["decision"] == "revert"
        assert trace["reason"] == "execution failed validation"
        assert trace["execution_status"] == "error"
        assert trace["diff"] == "some diff"
        assert trace["gate_blockers"] == ["risk_medium"]
        assert "timestamp" in trace

    def test_trace_path_uses_run_id(self, tmp_state):
        receipt = _make_receipt(run_id="my-special-run-42", decision="revert")
        execution = _make_execution_artifact()

        trace_path = orchestrate.extract_failure_trace(
            receipt, execution, str(tmp_state),
        )
        assert "my-special-run-42" in trace_path

    def test_handles_missing_fields_gracefully(self, tmp_state):
        receipt = {"run_id": "run-x"}
        execution = {}

        trace_path = orchestrate.extract_failure_trace(
            receipt, execution, str(tmp_state),
        )

        trace = json.loads(Path(trace_path).read_text())
        assert trace["type"] == "failure_trace"
        assert trace["candidate_id"] is None
        assert trace["decision"] is None
        assert trace["execution_status"] is None


# ---------------------------------------------------------------------------
# Tests: run_pipeline (with mocked subprocesses)
# ---------------------------------------------------------------------------


def _mock_subprocess_side_effects(
    tmp_state: Path,
    decisions: list[str],
    *,
    has_accepted: bool = True,
):
    """Build a subprocess.run side-effect function that simulates
    the full pipeline across multiple attempts.

    Each call to subprocess.run returns a CompletedProcess with stdout
    pointing to a temporary artifact file.

    ``decisions`` controls what the gate returns on each attempt.
    """
    call_counter = {"n": 0, "attempt": 0}

    def side_effect(cmd, **kwargs):
        script_name = cmd[1] if len(cmd) > 1 else ""

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stderr = ""

        if "propose.py" in script_name:
            attempt = call_counter["attempt"]
            artifact_path = tmp_state / "candidate_versions" / f"run-attempt-{attempt}.json"
            artifact = {
                "run_id": f"run-attempt-{attempt}",
                "stage": "proposed",
                "status": "success",
                "target": {"path": "/fake/target"},
                "candidates": [
                    {
                        "id": "cand-01-docs",
                        "category": "docs",
                        "risk_level": "low",
                        "executor_support": True,
                        "target_path": "/fake/target/README.md",
                    },
                ],
                "truth_anchor": str(artifact_path),
            }
            artifact_path.write_text(json.dumps(artifact))
            mock_result.stdout = str(artifact_path)

        elif "score.py" in script_name:
            attempt = call_counter["attempt"]
            artifact_path = tmp_state / "rankings" / f"run-attempt-{attempt}.json"
            rec = "accept_for_execution" if has_accepted else "hold"
            artifact = {
                "run_id": f"run-attempt-{attempt}",
                "stage": "ranked",
                "status": "success",
                "target": {"path": "/fake/target"},
                "scored_candidates": [
                    {
                        "id": "cand-01-docs",
                        "score": 8.5,
                        "recommendation": rec,
                        "category": "docs",
                        "risk_level": "low",
                        "target_path": "/fake/target/README.md",
                    },
                ],
                "truth_anchor": str(artifact_path),
            }
            artifact_path.write_text(json.dumps(artifact))
            mock_result.stdout = str(artifact_path)

        elif "execute.py" in script_name:
            attempt = call_counter["attempt"]
            artifact_path = tmp_state / "executions" / f"run-attempt-{attempt}.json"
            artifact = {
                "run_id": f"run-attempt-{attempt}",
                "candidate_id": "cand-01-docs",
                "stage": "executed",
                "status": "success",
                "result": {
                    "status": "success",
                    "modified": True,
                    "diff": "+new line",
                },
                "truth_anchor": str(artifact_path),
            }
            artifact_path.write_text(json.dumps(artifact))
            mock_result.stdout = str(artifact_path)

        elif "gate.py" in script_name:
            attempt = call_counter["attempt"]
            decision = decisions[attempt] if attempt < len(decisions) else "reject"
            artifact_path = tmp_state / "receipts" / f"gate-run-attempt-{attempt}.json"
            receipt = {
                "run_id": f"run-attempt-{attempt}",
                "candidate_id": "cand-01-docs",
                "decision": decision,
                "reason": f"test decision: {decision}",
                "blockers": [],
                "truth_anchor": str(artifact_path),
            }
            artifact_path.write_text(json.dumps(receipt))
            mock_result.stdout = str(artifact_path)
            call_counter["attempt"] += 1

        return mock_result

    return side_effect


class TestRunPipeline:
    # Patch EVALUATOR_SCRIPT to a non-existent path so run_evaluator() skips
    # (the evaluator is optional and returns None when script doesn't exist).
    _no_evaluator = patch.object(
        orchestrate, "EVALUATOR_SCRIPT", Path("/nonexistent/evaluate.py"),
    )

    def test_keep_on_first_attempt(self, tmp_state):
        side_effect = _mock_subprocess_side_effects(tmp_state, ["keep"])

        with self._no_evaluator, patch("subprocess.run", side_effect=side_effect):
            summary = orchestrate.run_pipeline(
                target="/fake/target",
                sources=[],
                state_root=str(tmp_state),
                max_retries=3,
            )

        assert summary["final_decision"] == "keep"
        assert summary["attempts"] == 1
        assert summary["final_candidate_id"] == "cand-01-docs"

    def test_revert_then_keep(self, tmp_state):
        side_effect = _mock_subprocess_side_effects(
            tmp_state, ["revert", "keep"],
        )

        with self._no_evaluator, patch("subprocess.run", side_effect=side_effect):
            summary = orchestrate.run_pipeline(
                target="/fake/target",
                sources=[],
                state_root=str(tmp_state),
                max_retries=3,
            )

        assert summary["final_decision"] == "keep"
        assert summary["attempts"] == 2

        # Verify trace file was created for the revert
        traces = list((tmp_state / "traces").glob("trace-*.json"))
        assert len(traces) == 1

    def test_pending_promote_stops_loop(self, tmp_state):
        side_effect = _mock_subprocess_side_effects(
            tmp_state, ["pending_promote"],
        )

        with self._no_evaluator, patch("subprocess.run", side_effect=side_effect):
            summary = orchestrate.run_pipeline(
                target="/fake/target",
                sources=[],
                state_root=str(tmp_state),
                max_retries=3,
            )

        assert summary["final_decision"] == "pending_promote"
        assert summary["attempts"] == 1

    def test_reject_stops_loop(self, tmp_state):
        side_effect = _mock_subprocess_side_effects(
            tmp_state, ["reject"],
        )

        with self._no_evaluator, patch("subprocess.run", side_effect=side_effect):
            summary = orchestrate.run_pipeline(
                target="/fake/target",
                sources=[],
                state_root=str(tmp_state),
                max_retries=3,
            )

        assert summary["final_decision"] == "reject"
        assert summary["attempts"] == 1

    def test_max_retries_exhausted(self, tmp_state):
        side_effect = _mock_subprocess_side_effects(
            tmp_state, ["revert", "revert", "revert"],
        )

        with self._no_evaluator, patch("subprocess.run", side_effect=side_effect):
            summary = orchestrate.run_pipeline(
                target="/fake/target",
                sources=[],
                state_root=str(tmp_state),
                max_retries=3,
            )

        # After 3 reverts the loop ends; last decision is "revert"
        assert summary["final_decision"] == "revert"
        assert summary["attempts"] == 3

        # All 3 traces should exist
        traces = list((tmp_state / "traces").glob("trace-*.json"))
        assert len(traces) == 3

    def test_no_accepted_candidates_exits_early(self, tmp_state):
        side_effect = _mock_subprocess_side_effects(
            tmp_state, ["keep"], has_accepted=False,
        )

        with patch("subprocess.run", side_effect=side_effect):
            summary = orchestrate.run_pipeline(
                target="/fake/target",
                sources=[],
                state_root=str(tmp_state),
                max_retries=3,
            )

        assert summary["final_decision"] == "no_accepted_candidates"
        # Pipeline retries up to max_retries before giving up
        assert summary["attempts"] == 3

    def test_failure_trace_fed_back_as_source(self, tmp_state):
        """Verify that after a revert the trace path is passed via --trace."""
        call_log = {"proposer_calls": []}

        original_side_effect = _mock_subprocess_side_effects(
            tmp_state, ["revert", "keep"],
        )

        def tracking_side_effect(cmd, **kwargs):
            script_name = cmd[1] if len(cmd) > 1 else ""
            if "propose.py" in script_name:
                # Capture --source and --trace args
                sources_in_cmd = []
                trace_in_cmd = None
                for i, arg in enumerate(cmd):
                    if arg == "--source" and i + 1 < len(cmd):
                        sources_in_cmd.append(cmd[i + 1])
                    if arg == "--trace" and i + 1 < len(cmd):
                        trace_in_cmd = cmd[i + 1]
                call_log["proposer_calls"].append({
                    "sources": sources_in_cmd,
                    "trace": trace_in_cmd,
                })
            return original_side_effect(cmd, **kwargs)

        with self._no_evaluator, patch("subprocess.run", side_effect=tracking_side_effect):
            orchestrate.run_pipeline(
                target="/fake/target",
                sources=["/original/source.md"],
                state_root=str(tmp_state),
                max_retries=3,
            )

        # First call: only original source, no trace
        assert call_log["proposer_calls"][0]["sources"] == ["/original/source.md"]
        assert call_log["proposer_calls"][0]["trace"] is None

        # Second call: same source, plus a --trace pointing to trace file
        second_call = call_log["proposer_calls"][1]
        assert second_call["sources"] == ["/original/source.md"]
        assert second_call["trace"] is not None
        assert "trace-" in second_call["trace"]


# ---------------------------------------------------------------------------
# Tests: _run_script error handling
# ---------------------------------------------------------------------------


class TestRunScript:
    def test_raises_on_nonzero_exit(self):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = "some output"
        mock_result.stderr = "some error"

        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(RuntimeError, match="proposer failed"):
                orchestrate._run_script(["python3", "fake.py"], "proposer")



class TestRunScriptNew:
    """Tests for the new run_script function."""

    def test_raises_on_nonzero_exit(self):
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "traceback: something broke"
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(RuntimeError, match="executor failed"):
                orchestrate.run_script(Path("fake.py"), [], "executor")

    def test_raises_on_empty_stdout(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "   \n  \n  "
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(RuntimeError, match="produced no output"):
                orchestrate.run_script(Path("fake.py"), [], "scorer")

    def test_returns_absolute_path_when_exists(self, tmp_path):
        artifact = tmp_path / "artifact.json"
        artifact.write_text("{}")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = f"  \n{artifact}\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            result = orchestrate.run_script(Path("fake.py"), ["--flag"], "proposer")
        assert result == artifact

    def test_resolves_relative_path_via_cwd(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        artifact = tmp_path / "out" / "result.json"
        artifact.parent.mkdir()
        artifact.write_text("{}")
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "out/result.json\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            result = orchestrate.run_script(Path("fake.py"), [], "gate")
        assert result.exists()
        assert result.name == "result.json"

    def test_stderr_included_in_error_message(self):
        mock_result = MagicMock()
        mock_result.returncode = 2
        mock_result.stdout = ""
        mock_result.stderr = "ImportError: no module named foo"
        with patch("subprocess.run", return_value=mock_result):
            with pytest.raises(RuntimeError) as exc_info:
                orchestrate.run_script(Path("fake.py"), [], "proposer")
        assert "ImportError: no module named foo" in str(exc_info.value)

    def test_returns_path_even_when_nonexistent(self):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "/nonexistent/artifact.json\n"
        mock_result.stderr = ""
        with patch("subprocess.run", return_value=mock_result):
            result = orchestrate.run_script(Path("fake.py"), [], "executor")
        assert result == Path("/nonexistent/artifact.json")

# ---------------------------------------------------------------------------
# Tests: CLI parse_args
# ---------------------------------------------------------------------------


class TestParseArgs:
    def test_required_args(self):
        args = orchestrate.parse_args([
            "--target", "/some/skill",
            "--state-root", "/some/state",
        ])
        assert args.target == "/some/skill"
        assert args.state_root == "/some/state"
        assert args.max_retries == 3
        assert args.auto is False
        assert args.source == []

    def test_all_args(self):
        args = orchestrate.parse_args([
            "--target", "/some/skill",
            "--source", "/a.md",
            "--source", "/b.md",
            "--state-root", "/some/state",
            "--max-retries", "5",
            "--auto",
        ])
        assert args.source == ["/a.md", "/b.md"]
        assert args.max_retries == 5
        assert args.auto is True
