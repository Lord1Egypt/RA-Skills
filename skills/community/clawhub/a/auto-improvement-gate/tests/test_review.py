#!/usr/bin/env python3
"""Tests for the human review CLI (review.py)."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

import pytest

# Load review.py by file path (hyphenated directory name).
_REVIEW_PY = Path(__file__).resolve().parents[1] / "scripts" / "review.py"
_spec = importlib.util.spec_from_file_location("review", _REVIEW_PY)
_review = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_review)

list_pending = _review.list_pending
complete_review = _review.complete_review
main = _review.main

# Also load lib helpers for setup
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import write_json
from lib.state_machine import ensure_tree


@pytest.fixture
def state_root(tmp_path):
    """Create an initialized state tree in a temp directory."""
    root = tmp_path / "state"
    ensure_tree(root)
    return root


def _write_review(state_root: Path, request_id: str, **overrides) -> Path:
    """Write a review request file to the state directory."""
    reviews_dir = state_root / "state" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)
    data = {
        "request_id": request_id,
        "candidate_id": "cand-001",
        "category": "prompt",
        "risk_level": "medium",
        "title": "Test improvement",
        "description": "A test change",
        "diff": "+ hello",
        "status": "pending",
        "requested_at": "2026-01-01T00:00:00Z",
    }
    data.update(overrides)
    path = reviews_dir / f"{request_id}.json"
    write_json(path, data)
    return path


# ===================================================================
# list_pending
# ===================================================================


class TestListPending:
    def test_empty_state(self, state_root):
        result = list_pending(state_root)
        assert result == []

    def test_one_pending(self, state_root):
        _write_review(state_root, "review-cand-001")
        result = list_pending(state_root)
        assert len(result) == 1
        assert result[0]["request_id"] == "review-cand-001"

    def test_multiple_pending(self, state_root):
        _write_review(state_root, "review-cand-001")
        _write_review(state_root, "review-cand-002", candidate_id="cand-002")
        result = list_pending(state_root)
        assert len(result) == 2

    def test_completed_not_listed(self, state_root):
        _write_review(state_root, "review-cand-001", status="completed")
        _write_review(state_root, "review-cand-002")
        result = list_pending(state_root)
        assert len(result) == 1
        assert result[0]["request_id"] == "review-cand-002"

    def test_non_review_files_ignored(self, state_root):
        """Files that don't match review-*.json pattern should be ignored."""
        reviews_dir = state_root / "state" / "reviews"
        reviews_dir.mkdir(parents=True, exist_ok=True)
        write_json(reviews_dir / "other.json", {"status": "pending"})
        _write_review(state_root, "review-cand-001")
        result = list_pending(state_root)
        assert len(result) == 1


# ===================================================================
# complete_review
# ===================================================================


class TestCompleteReview:
    def test_approve(self, state_root):
        _write_review(state_root, "review-cand-001")
        result = complete_review(state_root, "review-cand-001", "approve", reviewer="bob")
        assert result["status"] == "completed"
        assert result["decision"] == "approve"
        assert result["reviewer"] == "bob"
        assert "completed_at" in result

    def test_reject_with_reason(self, state_root):
        _write_review(state_root, "review-cand-001")
        result = complete_review(
            state_root, "review-cand-001", "reject", reason="Too risky"
        )
        assert result["decision"] == "reject"
        assert result["comments"] == "Too risky"

    def test_not_found(self, state_root):
        with pytest.raises(FileNotFoundError):
            complete_review(state_root, "review-nonexistent", "approve")

    def test_already_completed(self, state_root):
        _write_review(state_root, "review-cand-001", status="completed", decision="approve")
        with pytest.raises(ValueError, match="already completed"):
            complete_review(state_root, "review-cand-001", "approve")

    def test_invalid_decision(self, state_root):
        _write_review(state_root, "review-cand-001")
        with pytest.raises(ValueError, match="must be 'approve' or 'reject'"):
            complete_review(state_root, "review-cand-001", "maybe")

    def test_persists_to_disk(self, state_root):
        path = _write_review(state_root, "review-cand-001")
        complete_review(state_root, "review-cand-001", "approve")
        # Re-read from disk
        from lib.common import read_json

        data = read_json(path)
        assert data["status"] == "completed"
        assert data["decision"] == "approve"


# ===================================================================
# CLI main()
# ===================================================================


class TestMainCLI:
    def test_list_empty(self, state_root, capsys):
        rc = main(["--state-root", str(state_root), "--list"])
        assert rc == 0
        assert "No pending reviews" in capsys.readouterr().out

    def test_list_with_items(self, state_root, capsys):
        _write_review(state_root, "review-cand-001", title="Fix greeting")
        rc = main(["--state-root", str(state_root), "--list"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "review-cand-001" in out
        assert "Fix greeting" in out

    def test_complete_approve(self, state_root, capsys):
        _write_review(state_root, "review-cand-001")
        rc = main([
            "--state-root", str(state_root),
            "--complete", "review-cand-001",
            "--decision", "approve",
        ])
        assert rc == 0
        assert "completed" in capsys.readouterr().out.lower()

    def test_complete_reject(self, state_root, capsys):
        _write_review(state_root, "review-cand-001")
        rc = main([
            "--state-root", str(state_root),
            "--complete", "review-cand-001",
            "--decision", "reject",
            "--reason", "Not ready",
        ])
        assert rc == 0

    def test_complete_missing_decision(self, state_root, capsys):
        _write_review(state_root, "review-cand-001")
        rc = main([
            "--state-root", str(state_root),
            "--complete", "review-cand-001",
        ])
        assert rc == 1
        assert "required" in capsys.readouterr().err.lower()

    def test_complete_not_found(self, state_root, capsys):
        rc = main([
            "--state-root", str(state_root),
            "--complete", "review-nonexistent",
            "--decision", "approve",
        ])
        assert rc == 1
        assert "not found" in capsys.readouterr().err.lower()

    def test_help(self):
        """--help should print usage and exit without error."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        assert exc_info.value.code == 0
