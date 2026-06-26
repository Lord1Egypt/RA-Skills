#!/usr/bin/env python3
"""Tests for benchmark_db (hardcoded 0.85 fix) and pareto front tracking."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure repo root is on sys.path so `lib.common` resolves,
# and scripts dir so we can import benchmark_db / pareto directly
# (the parent directory uses hyphens, which is not a valid Python package name).
_REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
REPO_ROOT = _REPO_ROOT
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from benchmark_db import (  # noqa: E402
    compare_with_benchmark,
    init_db,
    add_benchmark,
)
from lib.pareto import ParetoEntry, ParetoFront  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_db(tmp_path):
    """Create an initialised temporary benchmark database with one test case."""
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    add_benchmark(db_path, "test-cat", "simple-test", "input-data", "expected-output")
    return db_path


# ---------------------------------------------------------------------------
# benchmark_db — compare_with_benchmark tests
# ---------------------------------------------------------------------------

class TestCompareWithBenchmark:
    """Verify the hardcoded 0.85 mock is gone."""

    def test_no_evaluator_raises(self, tmp_db):
        """Without an evaluator the function must refuse, not return 0.85."""
        with pytest.raises(ValueError, match="evaluator is required"):
            compare_with_benchmark(tmp_db, "/fake/skill", "test-cat", evaluator=None)

    def test_default_arg_raises(self, tmp_db):
        """Calling without the evaluator kwarg at all must also raise."""
        with pytest.raises(ValueError, match="evaluator is required"):
            compare_with_benchmark(tmp_db, "/fake/skill", "test-cat")

    def test_with_evaluator_returns_real_score(self, tmp_db):
        """A provided evaluator's score must be used — never 0.85."""
        def evaluator(test_name, test_input, expected_output, metrics):
            return {"passed": True, "score": 0.42}

        score = compare_with_benchmark(tmp_db, "/fake/skill", "test-cat", evaluator=evaluator)
        assert score == pytest.approx(0.42)
        assert score != pytest.approx(0.85)

    def test_evaluator_score_varies(self, tmp_db):
        """Score must reflect what the evaluator returns, not a constant."""
        def evaluator(test_name, test_input, expected_output, metrics):
            return {"passed": False, "score": 0.17}

        score = compare_with_benchmark(tmp_db, "/fake/skill", "test-cat", evaluator=evaluator)
        assert score == pytest.approx(0.17)

    def test_evaluator_bad_return_type_raises(self, tmp_db):
        """An evaluator returning a non-dict must raise TypeError."""
        def bad_evaluator(test_name, test_input, expected_output, metrics):
            return 0.5  # not a dict

        with pytest.raises(TypeError, match="evaluator must return a dict"):
            compare_with_benchmark(tmp_db, "/fake/skill", "test-cat", evaluator=bad_evaluator)

    def test_empty_category_returns_none(self, tmp_db):
        """Missing category returns None (no benchmarks found)."""
        def evaluator(test_name, test_input, expected_output, metrics):
            return {"passed": True, "score": 0.9}

        result = compare_with_benchmark(tmp_db, "/fake/skill", "no-such-category", evaluator=evaluator)
        assert result is None


# ---------------------------------------------------------------------------
# pareto — ParetoEntry.dominates() tests
# ---------------------------------------------------------------------------

class TestParetoEntryDominates:

    def test_strictly_dominates(self):
        a = ParetoEntry("r1", "c1", {"x": 0.9, "y": 0.8})
        b = ParetoEntry("r2", "c2", {"x": 0.7, "y": 0.6})
        assert a.dominates(b) is True
        assert b.dominates(a) is False

    def test_equal_does_not_dominate(self):
        a = ParetoEntry("r1", "c1", {"x": 0.8, "y": 0.8})
        b = ParetoEntry("r2", "c2", {"x": 0.8, "y": 0.8})
        assert a.dominates(b) is False
        assert b.dominates(a) is False

    def test_partial_better_does_not_dominate(self):
        a = ParetoEntry("r1", "c1", {"x": 0.9, "y": 0.5})
        b = ParetoEntry("r2", "c2", {"x": 0.7, "y": 0.8})
        assert a.dominates(b) is False
        assert b.dominates(a) is False

    def test_dominate_with_one_equal_dimension(self):
        a = ParetoEntry("r1", "c1", {"x": 0.9, "y": 0.8})
        b = ParetoEntry("r2", "c2", {"x": 0.9, "y": 0.6})
        assert a.dominates(b) is True
        assert b.dominates(a) is False


# ---------------------------------------------------------------------------
# pareto — ParetoFront.add() tests
# ---------------------------------------------------------------------------

class TestParetoFrontAdd:

    def test_add_to_empty_front(self):
        front = ParetoFront()
        entry = ParetoEntry("r1", "c1", {"x": 0.8, "y": 0.7})
        result = front.add(entry)
        assert result["accepted"] is True
        assert result["front_size"] == 1

    def test_add_dominated_is_rejected(self):
        front = ParetoFront()
        strong = ParetoEntry("r1", "c1", {"x": 0.9, "y": 0.9})
        front.add(strong)

        weak = ParetoEntry("r2", "c2", {"x": 0.7, "y": 0.7})
        result = front.add(weak)
        assert result["accepted"] is False
        assert result["reason"] == "dominated_by_existing"
        assert result["dominator"] == "r1"
        assert len(front.entries) == 1

    def test_add_dominator_removes_old(self):
        front = ParetoFront()
        weak = ParetoEntry("r1", "c1", {"x": 0.5, "y": 0.5})
        front.add(weak)

        strong = ParetoEntry("r2", "c2", {"x": 0.9, "y": 0.9})
        result = front.add(strong)
        assert result["accepted"] is True
        assert result["dominated_count"] == 1
        assert result["front_size"] == 1
        assert front.entries[0].run_id == "r2"

    def test_add_non_dominated_grows_front(self):
        front = ParetoFront()
        front.add(ParetoEntry("r1", "c1", {"x": 0.9, "y": 0.3}))
        result = front.add(ParetoEntry("r2", "c2", {"x": 0.3, "y": 0.9}))
        assert result["accepted"] is True
        assert result["front_size"] == 2


# ---------------------------------------------------------------------------
# pareto — ParetoFront.check_regression() tests
# ---------------------------------------------------------------------------

class TestParetoFrontCheckRegression:

    def test_no_regression(self):
        front = ParetoFront()
        front.add(ParetoEntry("r1", "c1", {"accuracy": 0.8, "speed": 0.7}))
        result = front.check_regression({"accuracy": 0.85, "speed": 0.75})
        assert result["regressed"] is False

    def test_regression_detected(self):
        front = ParetoFront()
        front.add(ParetoEntry("r1", "c1", {"accuracy": 0.9, "speed": 0.8}))
        # accuracy drops below 0.9 * 0.95 = 0.855
        result = front.check_regression({"accuracy": 0.5, "speed": 0.8})
        assert result["regressed"] is True
        assert len(result["regressions"]) == 1
        assert result["regressions"][0]["dimension"] == "accuracy"

    def test_within_tolerance(self):
        front = ParetoFront()
        front.add(ParetoEntry("r1", "c1", {"accuracy": 0.9}))
        # 0.9 * 0.95 = 0.855, so 0.86 is within tolerance
        result = front.check_regression({"accuracy": 0.86})
        assert result["regressed"] is False

    def test_empty_front_no_regression(self):
        front = ParetoFront()
        result = front.check_regression({"accuracy": 0.5})
        assert result["regressed"] is False


# ---------------------------------------------------------------------------
# pareto — Persistence (save/load round-trip) tests
# ---------------------------------------------------------------------------

class TestParetoFrontPersistence:

    def test_save_and_load_round_trip(self, tmp_path):
        storage = tmp_path / "pareto.json"

        # Write
        front1 = ParetoFront(storage_path=storage)
        front1.add(ParetoEntry("r1", "c1", {"x": 0.8, "y": 0.7}, timestamp="2026-01-01T00:00:00Z"))
        front1.add(ParetoEntry("r2", "c2", {"x": 0.3, "y": 0.95}, timestamp="2026-01-02T00:00:00Z"))
        assert storage.exists()

        # Read into a new instance
        front2 = ParetoFront(storage_path=storage)
        assert len(front2.entries) == 2
        ids = {e.run_id for e in front2.entries}
        assert ids == {"r1", "r2"}

    def test_load_nonexistent_file_is_empty(self, tmp_path):
        storage = tmp_path / "does_not_exist.json"
        front = ParetoFront(storage_path=storage)
        assert len(front.entries) == 0
