#!/usr/bin/env python3
"""Task execution engine for the improvement evaluator.

Runs a single task with SKILL.md content prepended to the prompt,
evaluates the output with the configured judge, and returns a TaskResult.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sys

_SKILL_ROOT = Path(__file__).resolve().parents[1]
_INTERFACES_DIR = str(_SKILL_ROOT / "interfaces")
if _INTERFACES_DIR not in sys.path:
    sys.path.insert(0, _INTERFACES_DIR)

from judges import get_judge


@dataclass
class TaskResult:
    """Result of running a single task."""
    passed: bool
    judge_output: dict
    raw_output: str
    cost_usd: float = 0.0
    duration_ms: int = 0
    error: str = ""
    input_tokens: int = 0
    output_tokens: int = 0


class TaskRunner:
    """Runs a single task with SKILL.md context."""

    def __init__(self, mock: bool = False, timeout: int = 300, model: str | None = None):
        self.mock = mock
        self.timeout = timeout
        self.model = model  # e.g. "claude-sonnet-4-6", "claude-haiku-4-5"
        self._last_token_usage: dict[str, int] = {}

    def run(self, skill_content: str, task: dict, pass_k: int = 1) -> TaskResult:
        """Run a task pass_k times and return the best result.

        Args:
            skill_content: SKILL.md text to prepend to the prompt
            task: Task dict with id, prompt, judge config
            pass_k: Number of attempts; passes if any attempt passes
        """
        prompt = self._build_prompt(skill_content, task)
        timeout = task.get("timeout_seconds", self.timeout)

        best_result: TaskResult | None = None
        for attempt in range(pass_k):
            start = time.monotonic()
            try:
                if self.mock:
                    raw_output = self._mock_execute(prompt)
                else:
                    raw_output = self._execute_claude(prompt, timeout)
            except Exception as exc:
                duration_ms = int((time.monotonic() - start) * 1000)
                result = TaskResult(
                    passed=False,
                    judge_output={"passed": False, "details": str(exc), "score": 0.0},
                    raw_output="",
                    duration_ms=duration_ms,
                    error=str(exc),
                )
                if best_result is None:
                    best_result = result
                continue

            duration_ms = int((time.monotonic() - start) * 1000)

            # Evaluate with judge
            judge = get_judge(task["judge"], mock=self.mock)
            judge_output = judge.evaluate(raw_output, task)

            # Extract token usage from last execution
            token_usage = getattr(self, "_last_token_usage", {})
            result = TaskResult(
                passed=judge_output.get("passed", False),
                judge_output=judge_output,
                raw_output=raw_output[:2000],  # truncate for storage
                duration_ms=duration_ms,
                input_tokens=token_usage.get("input_tokens", 0),
                output_tokens=token_usage.get("output_tokens", 0),
            )

            if result.passed:
                return result
            if best_result is None or result.judge_output.get("score", 0) > best_result.judge_output.get("score", 0):
                best_result = result

        return best_result  # type: ignore[return-value]

    def _build_prompt(self, skill_content: str, task: dict) -> str:
        """Prepend SKILL.md content to the task prompt."""
        return (
            f"You have been given the following skill documentation to guide your work:\n\n"
            f"---BEGIN SKILL.MD---\n{skill_content}\n---END SKILL.MD---\n\n"
            f"Task: {task['prompt']}"
        )

    def _execute_claude(self, prompt: str, timeout: int) -> str:
        """Call claude -p subprocess and return the text output."""
        tmpdir = None
        try:
            tmpdir = tempfile.mkdtemp(prefix="evaluator_task_")
            prompt_file = Path(tmpdir) / "prompt.txt"
            prompt_file.write_text(prompt, encoding="utf-8")

            cmd = ["claude", "-p", "--output-format", "json"]
            if self.model:
                cmd.extend(["--model", self.model])
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            if result.returncode != 0:
                raise RuntimeError(f"claude -p exited {result.returncode}: {result.stderr[:300]}")

            # Parse claude JSON output, extract token usage if available
            try:
                parsed = json.loads(result.stdout)
                # Store token usage for cost tracking
                usage = parsed.get("usage", {})
                if usage:
                    self._last_token_usage = {
                        "input_tokens": usage.get("input_tokens", 0),
                        "output_tokens": usage.get("output_tokens", 0),
                    }
                return parsed.get("result", result.stdout)
            except (json.JSONDecodeError, TypeError):
                return result.stdout

        except subprocess.TimeoutExpired:
            raise RuntimeError(f"claude -p timed out after {timeout}s")
        finally:
            if tmpdir:
                shutil.rmtree(tmpdir, ignore_errors=True)

    def _mock_execute(self, prompt: str) -> str:
        """Return a mock response for testing without claude CLI."""
        # Return a generic response that includes common keywords
        # for basic ContainsJudge tests
        return (
            "Based on the skill documentation, here is my analysis:\n\n"
            "The quality tier is POWERFUL based on the high accuracy and coverage scores.\n"
            "This indicates strong performance across multiple dimensions.\n\n"
            "Regarding the Pareto front, if accuracy regressed significantly, "
            "we should reject the change as it represents a regression in a key metric. "
            "The coverage improvement does not compensate for the accuracy loss.\n"
            "hello world"
        )
