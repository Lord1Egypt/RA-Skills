#!/usr/bin/env python3
"""Tests for the task runner."""

import sys
from pathlib import Path

# Add paths for imports
_SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_SKILL_ROOT / "scripts"))
sys.path.insert(0, str(_SKILL_ROOT / "interfaces"))

import pytest
from task_runner import TaskRunner, TaskResult


class TestTaskRunner:
    def test_mock_execution_contains(self):
        runner = TaskRunner(mock=True)
        result = runner.run(
            "# Test Skill\nDo X",
            {
                "id": "t1",
                "prompt": "test",
                "judge": {
                    "type": "contains",
                    "expected": ["hello"],
                },
            },
        )
        assert isinstance(result, TaskResult)
        # The mock response includes "hello world"
        assert result.passed is True

    def test_mock_execution_missing_keyword(self):
        runner = TaskRunner(mock=True)
        result = runner.run(
            "# Test Skill",
            {
                "id": "t1",
                "prompt": "test",
                "judge": {
                    "type": "contains",
                    "expected": ["nonexistent_keyword_xyz"],
                },
            },
        )
        assert isinstance(result, TaskResult)
        assert result.passed is False

    def test_mock_execution_llm_rubric(self):
        runner = TaskRunner(mock=True)
        result = runner.run(
            "# Test Skill",
            {
                "id": "t1",
                "prompt": "test",
                "judge": {
                    "type": "llm-rubric",
                    "rubric": "test rubric",
                    "pass_threshold": 0.7,
                },
            },
        )
        assert isinstance(result, TaskResult)
        assert result.passed is True  # mock returns 0.8

    def test_task_result_dataclass(self):
        result = TaskResult(
            passed=True,
            judge_output={"passed": True, "details": "ok", "score": 1.0},
            raw_output="test output",
            duration_ms=100,
        )
        assert result.passed is True
        assert result.duration_ms == 100
        assert result.cost_usd == 0.0
        assert result.error == ""

    def test_pass_k_returns_on_first_pass(self):
        runner = TaskRunner(mock=True)
        result = runner.run(
            "# Test Skill",
            {
                "id": "t1",
                "prompt": "test",
                "judge": {
                    "type": "contains",
                    "expected": ["hello"],
                },
            },
            pass_k=3,
        )
        assert result.passed is True

    def test_pass_k_all_fail(self):
        runner = TaskRunner(mock=True)
        result = runner.run(
            "# Test Skill",
            {
                "id": "t1",
                "prompt": "test",
                "judge": {
                    "type": "contains",
                    "expected": ["impossible_keyword_that_wont_match"],
                },
            },
            pass_k=2,
        )
        assert result.passed is False

    def test_build_prompt(self):
        runner = TaskRunner(mock=True)
        prompt = runner._build_prompt("# My Skill", {"prompt": "Do the thing"})
        assert "---BEGIN SKILL.MD---" in prompt
        assert "# My Skill" in prompt
        assert "---END SKILL.MD---" in prompt
        assert "Do the thing" in prompt

    def test_duration_tracked(self):
        runner = TaskRunner(mock=True)
        result = runner.run(
            "# Test Skill",
            {
                "id": "t1",
                "prompt": "test",
                "judge": {"type": "contains", "expected": ["hello"]},
            },
        )
        assert result.duration_ms >= 0
