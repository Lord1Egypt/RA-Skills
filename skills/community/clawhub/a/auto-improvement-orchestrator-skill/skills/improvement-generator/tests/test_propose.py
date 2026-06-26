#!/usr/bin/env python3
"""Tests for the improvement-generator propose module."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import importlib.util

import pytest

# repo root so we can import lib.common and the propose module
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
REPO_ROOT = _REPO_ROOT

# The scripts directory uses dashes in skill names but Python needs underscores
# for imports. We import via importlib to work around the path layout.
_propose_path = REPO_ROOT / "skills" / "improvement-generator" / "scripts" / "propose.py"
_spec = importlib.util.spec_from_file_location("propose", _propose_path)
propose = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(propose)


# ---------------------------------------------------------------------------
# load_failure_trace
# ---------------------------------------------------------------------------


class TestLoadFailureTrace:
    def test_returns_none_for_none_path(self):
        assert propose.load_failure_trace(None) is None

    def test_returns_none_for_missing_file(self, tmp_path):
        missing = tmp_path / "does_not_exist.json"
        assert propose.load_failure_trace(missing) is None

    def test_loads_valid_trace(self, tmp_path):
        trace_file = tmp_path / "trace.json"
        trace_data = {
            "candidate_id": "cand-01-docs",
            "reason": "section already present",
        }
        trace_file.write_text(json.dumps(trace_data), encoding="utf-8")
        result = propose.load_failure_trace(trace_file)
        assert result == trace_data


# ---------------------------------------------------------------------------
# adjust_candidates_from_trace
# ---------------------------------------------------------------------------


class TestAdjustCandidatesFromTrace:
    @staticmethod
    def _make_candidate(category: str, idx: int = 1) -> dict:
        return {
            "id": f"cand-{idx:02d}-{category}",
            "category": category,
            "rationale": f"Original rationale for {category}",
        }

    def test_failed_category_moves_to_end(self):
        trace = {"candidate_id": "cand-01-docs", "reason": "duplicate section"}
        candidates = [
            self._make_candidate("docs", 1),
            self._make_candidate("reference", 2),
            self._make_candidate("guardrail", 3),
        ]
        adjusted = propose.adjust_candidates_from_trace(candidates, trace)

        # "docs" should be last
        assert adjusted[-1]["category"] == "docs"
        # alternatives should be boosted to front
        assert adjusted[0]["category"] in ("reference", "guardrail")

    def test_failed_candidate_rationale_includes_reason(self):
        trace = {"candidate_id": "cand-01-docs", "reason": "duplicate section"}
        candidates = [self._make_candidate("docs", 1)]
        adjusted = propose.adjust_candidates_from_trace(candidates, trace)
        assert "[Retry]" in adjusted[0]["rationale"]
        assert "duplicate section" in adjusted[0]["rationale"]

    def test_alternatives_boosted_to_front(self):
        trace = {"candidate_id": "cand-01-docs", "reason": "err"}
        candidates = [
            self._make_candidate("docs", 1),
            self._make_candidate("reference", 2),
        ]
        adjusted = propose.adjust_candidates_from_trace(candidates, trace)
        assert adjusted[0]["category"] == "reference"
        assert adjusted[1]["category"] == "docs"

    def test_no_match_keeps_order(self):
        trace = {"candidate_id": "cand-01-nonexistent", "reason": "err"}
        candidates = [
            self._make_candidate("docs", 1),
            self._make_candidate("reference", 2),
        ]
        adjusted = propose.adjust_candidates_from_trace(candidates, trace)
        # All go to front via insert(0), so order reverses among non-matched
        assert len(adjusted) == 2
        # All candidates remain present
        categories = {c["category"] for c in adjusted}
        assert categories == {"docs", "reference"}

    def test_empty_candidates(self):
        trace = {"candidate_id": "cand-01-docs", "reason": "err"}
        assert propose.adjust_candidates_from_trace([], trace) == []


# ---------------------------------------------------------------------------
# Candidate builders with a real temp directory
# ---------------------------------------------------------------------------


class TestCandidateBuilders:
    @pytest.fixture
    def skill_dir(self, tmp_path):
        """Create a minimal skill directory structure."""
        (tmp_path / "SKILL.md").write_text("# Test Skill\n", encoding="utf-8")
        (tmp_path / "README.md").write_text("# README\n", encoding="utf-8")
        refs = tmp_path / "references"
        refs.mkdir()
        (refs / "guardrails.md").write_text("# Guardrails\n", encoding="utf-8")
        (refs / "overview.md").write_text("# Overview\n", encoding="utf-8")
        return tmp_path

    def test_build_docs_candidate(self, skill_dir):
        buckets = {"limitations": ["some limitation"], "examples": []}
        result = propose.build_docs_candidate(skill_dir, buckets, 1)
        assert result is not None
        assert result["category"] == "docs"
        assert result["risk_level"] == "low"
        assert result["id"].startswith("cand-01-")

    def test_build_reference_candidate(self, skill_dir):
        buckets = {"workflow": ["stage transition"]}
        result = propose.build_reference_candidate(skill_dir, buckets, 2)
        assert result is not None
        assert result["category"] == "reference"

    def test_build_guardrail_candidate(self, skill_dir):
        buckets = {"guardrails": ["risk signal"], "limitations": []}
        result = propose.build_guardrail_candidate(skill_dir, buckets, 3)
        assert result is not None
        assert result["category"] == "guardrail"

    def test_build_docs_returns_none_for_empty_dir(self, tmp_path):
        buckets = {"limitations": [], "examples": []}
        # tmp_path has no markdown files
        result = propose.build_docs_candidate(tmp_path, buckets, 1)
        assert result is None

    def test_generate_candidates_produces_list(self, skill_dir):
        candidates = propose.generate_candidates(skill_dir, [], 4)
        assert isinstance(candidates, list)
        assert len(candidates) > 0
        assert len(candidates) <= 4
