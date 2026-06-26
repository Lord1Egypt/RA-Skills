#!/usr/bin/env python3
"""Judge implementations for task evaluation.

Three judge types:
- ContainsJudge: deterministic keyword check
- PytestJudge: run pytest on AI output
- LLMRubricJudge: LLM scores against rubric (mock mode available)
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseJudge(ABC):
    """Abstract base for all judge types."""

    @abstractmethod
    def evaluate(self, output: str, task: dict) -> dict:
        """Returns {passed: bool, details: str, score: float}"""


class ContainsJudge(BaseJudge):
    """Check that output contains all expected keywords (case-insensitive)."""

    def evaluate(self, output: str, task: dict) -> dict:
        expected: list[str] = task["judge"]["expected"]
        output_lower = output.lower()
        found = [kw for kw in expected if kw.lower() in output_lower]
        missing = [kw for kw in expected if kw.lower() not in output_lower]
        passed = len(missing) == 0
        score = len(found) / len(expected) if expected else 0.0
        return {
            "passed": passed,
            "details": f"Found: {found}, Missing: {missing}",
            "score": round(score, 4),
        }


class PytestJudge(BaseJudge):
    """Write AI output to temp file, run pytest with the specified test file.

    SECURITY: test_file must start with "fixtures/" to prevent path traversal.
    """

    def evaluate(self, output: str, task: dict) -> dict:
        test_file = task["judge"]["test_file"]
        # Security: validate test_file is within fixtures/
        if not test_file.startswith("fixtures/"):
            return {
                "passed": False,
                "details": f"SECURITY: test_file must start with 'fixtures/', got: {test_file}",
                "score": 0.0,
            }

        skill_root = Path(__file__).resolve().parents[1]
        test_path = skill_root / "tests" / test_file
        # Security: resolve symlinks and prevent traversal (e.g. fixtures/../../)
        resolved = test_path.resolve()
        fixtures_root = (skill_root / "tests" / "fixtures").resolve()
        if not str(resolved).startswith(str(fixtures_root)):
            return {
                "passed": False,
                "details": "SECURITY: path traversal detected",
                "score": 0.0,
            }
        if not test_path.exists():
            return {
                "passed": False,
                "details": f"Test file not found: {test_path}",
                "score": 0.0,
            }

        tmpdir = None
        try:
            tmpdir = tempfile.mkdtemp(prefix="evaluator_pytest_")
            output_file = Path(tmpdir) / "ai_output.txt"
            output_file.write_text(output, encoding="utf-8")

            result = subprocess.run(
                ["python3", "-m", "pytest", str(test_path), "-v",
                 "--tb=short", f"--rootdir={tmpdir}"],
                capture_output=True,
                text=True,
                timeout=60,
                env={
                    **__import__("os").environ,
                    "AI_OUTPUT_FILE": str(output_file),
                },
            )
            passed = result.returncode == 0
            details = result.stdout[-500:] if result.stdout else result.stderr[-500:]
            return {
                "passed": passed,
                "details": details.strip(),
                "score": 1.0 if passed else 0.0,
            }
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "details": "pytest timed out after 60s",
                "score": 0.0,
            }
        except Exception as exc:
            return {
                "passed": False,
                "details": f"pytest execution error: {exc}",
                "score": 0.0,
            }
        finally:
            if tmpdir:
                import shutil
                shutil.rmtree(tmpdir, ignore_errors=True)


class LLMRubricJudge(BaseJudge):
    """Score AI output against a rubric via LLM (or mock).

    Pass threshold comes from task["judge"]["pass_threshold"].
    """

    def __init__(self, mock: bool = False):
        self.mock = mock

    def evaluate(self, output: str, task: dict) -> dict:
        rubric = task["judge"].get("rubric", "")
        pass_threshold = task["judge"].get("pass_threshold", 0.7)

        if self.mock:
            score = 0.8
            return {
                "passed": score >= pass_threshold,
                "details": f"[mock] score={score}, threshold={pass_threshold}",
                "score": score,
            }

        # Real LLM evaluation via claude -p
        prompt = (
            f"You are a judge evaluating AI output quality.\n\n"
            f"## Rubric\n{rubric}\n\n"
            f"## AI Output\n{output[:3000]}\n\n"
            f"Score the output from 0.0 to 1.0 based on the rubric.\n"
            f"Respond with ONLY a JSON object: {{\"score\": <float>, \"reasoning\": \"<str>\"}}"
        )
        try:
            result = subprocess.run(
                ["claude", "-p", "--output-format", "json"],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode != 0:
                return {
                    "passed": False,
                    "details": f"claude -p failed: {result.stderr[:300]}",
                    "score": 0.0,
                }
            # Parse claude JSON output to get the text result
            try:
                claude_output = json.loads(result.stdout)
                text_result = claude_output.get("result", result.stdout)
            except (json.JSONDecodeError, TypeError):
                text_result = result.stdout

            # Parse the judge's JSON response from the text
            parsed = json.loads(text_result) if isinstance(text_result, str) else text_result
            score = float(parsed.get("score", 0.0))
            reasoning = parsed.get("reasoning", "")
            return {
                "passed": score >= pass_threshold,
                "details": f"score={score}, threshold={pass_threshold}, reasoning={reasoning}",
                "score": score,
            }
        except json.JSONDecodeError:
            return {
                "passed": False,
                "details": "Failed to parse LLM judge response as JSON",
                "score": 0.0,
            }
        except subprocess.TimeoutExpired:
            return {
                "passed": False,
                "details": "LLM judge timed out after 120s",
                "score": 0.0,
            }
        except FileNotFoundError:
            return {
                "passed": False,
                "details": "claude CLI not found",
                "score": 0.0,
            }


def get_judge(judge_config: dict, mock: bool = False) -> BaseJudge:
    """Factory function to create the appropriate judge."""
    judge_type = judge_config["type"]
    if judge_type == "contains":
        return ContainsJudge()
    if judge_type == "pytest":
        return PytestJudge()
    if judge_type == "llm-rubric":
        return LLMRubricJudge(mock=mock)
    raise ValueError(f"Unknown judge type: {judge_type}")
