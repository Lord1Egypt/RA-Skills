#!/usr/bin/env python3
"""Tests for judge implementations."""

import sys
from pathlib import Path

# Add interfaces/ to path for imports
_SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SKILL_ROOT / "interfaces"))

import pytest
from judges import ContainsJudge, PytestJudge, LLMRubricJudge, get_judge


class TestContainsJudge:
    def test_all_keywords_found(self):
        judge = ContainsJudge()
        result = judge.evaluate(
            "Found use-after-free and dangling pointer",
            {"judge": {"expected": ["use-after-free", "dangling"]}},
        )
        assert result["passed"] is True
        assert result["score"] == 1.0

    def test_missing_keyword(self):
        judge = ContainsJudge()
        result = judge.evaluate(
            "Code looks fine",
            {"judge": {"expected": ["use-after-free", "dangling"]}},
        )
        assert result["passed"] is False
        assert result["score"] == 0.0

    def test_case_insensitive(self):
        judge = ContainsJudge()
        result = judge.evaluate(
            "USE-AFTER-FREE detected",
            {"judge": {"expected": ["use-after-free"]}},
        )
        assert result["passed"] is True

    def test_partial_match(self):
        judge = ContainsJudge()
        result = judge.evaluate(
            "Found use-after-free",
            {"judge": {"expected": ["use-after-free", "buffer overflow"]}},
        )
        assert result["passed"] is False
        assert result["score"] == 0.5

    def test_empty_output_with_expected(self):
        judge = ContainsJudge()
        result = judge.evaluate(
            "",
            {"judge": {"expected": ["something"]}},
        )
        assert result["passed"] is False
        assert result["score"] == 0.0

    def test_single_keyword_found(self):
        judge = ContainsJudge()
        result = judge.evaluate(
            "This has the keyword POWERFUL in it",
            {"judge": {"expected": ["POWERFUL"]}},
        )
        assert result["passed"] is True
        assert result["score"] == 1.0


class TestLLMRubricJudge:
    def test_mock_mode_passes(self):
        judge = LLMRubricJudge(mock=True)
        result = judge.evaluate(
            "some output",
            {"judge": {"rubric": "test", "pass_threshold": 0.7}},
        )
        assert result["passed"] is True
        assert result["score"] >= 0.7

    def test_mock_mode_high_threshold_fails(self):
        judge = LLMRubricJudge(mock=True)
        result = judge.evaluate(
            "some output",
            {"judge": {"rubric": "test", "pass_threshold": 0.9}},
        )
        # Mock returns 0.8, so threshold 0.9 should fail
        assert result["passed"] is False

    def test_mock_mode_default_threshold(self):
        judge = LLMRubricJudge(mock=True)
        result = judge.evaluate(
            "some output",
            {"judge": {"rubric": "test"}},
        )
        # Default threshold is 0.7, mock score is 0.8
        assert result["passed"] is True

    def test_mock_attribute(self):
        judge = LLMRubricJudge(mock=True)
        assert judge.mock is True
        judge2 = LLMRubricJudge(mock=False)
        assert judge2.mock is False


class TestPytestJudge:
    def test_security_rejects_non_fixture_path(self):
        judge = PytestJudge()
        result = judge.evaluate(
            "some output",
            {"judge": {"test_file": "../../../etc/passwd"}},
        )
        assert result["passed"] is False
        assert "SECURITY" in result["details"]

    def test_security_rejects_absolute_path(self):
        judge = PytestJudge()
        result = judge.evaluate(
            "some output",
            {"judge": {"test_file": "/tmp/evil.py"}},
        )
        assert result["passed"] is False
        assert "SECURITY" in result["details"]

    def test_nonexistent_test_file(self):
        judge = PytestJudge()
        result = judge.evaluate(
            "some output",
            {"judge": {"test_file": "fixtures/nonexistent_test.py"}},
        )
        assert result["passed"] is False
        assert "not found" in result["details"]


class TestGetJudge:
    def test_factory_contains(self):
        j = get_judge({"type": "contains"})
        assert isinstance(j, ContainsJudge)

    def test_factory_pytest(self):
        j = get_judge({"type": "pytest"})
        assert isinstance(j, PytestJudge)

    def test_factory_llm_rubric(self):
        j = get_judge({"type": "llm-rubric"})
        assert isinstance(j, LLMRubricJudge)
        assert j.mock is False

    def test_factory_llm_rubric_mock(self):
        j = get_judge({"type": "llm-rubric"}, mock=True)
        assert isinstance(j, LLMRubricJudge)
        assert j.mock is True

    def test_factory_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown judge type"):
            get_judge({"type": "unknown"})
