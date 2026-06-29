"""
Instruction Following dimension.

Evaluates whether the agent follows precise formatting, structural, and
content constraints.  Tasks give the agent detailed specifications (word
limits, required sections, forbidden words, output formats) and the
evaluator checks each constraint independently.
"""

from __future__ import annotations

import json
import re

from agent_bench_lite.adapters.base import BaseAdapter
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult


class InstructionFollowingDimension(BaseDimension):
    """Does the agent follow exact specifications?"""

    name = "instruction_following"
    display_name = "Instruction Following"
    description = (
        "Measures the agent's ability to strictly adhere to formatting "
        "constraints, structural requirements, and explicit instructions."
    )

    def get_tasks(self) -> list[Task]:
        return [
            # 1. Word count constraint.
            Task(
                task_id="if_word_limit",
                description="Respond in exactly 3 sentences",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Explain what machine learning is. "
                            "Your response MUST be exactly 3 sentences. "
                            "No more, no less."
                        ),
                    },
                ],
                expected={
                    "checks": [
                        {"type": "sentence_count", "exact": 3},
                    ],
                },
            ),
            # 2. Forbidden words.
            Task(
                task_id="if_forbidden_words",
                description="Avoid specific words while explaining a topic",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Explain how the internet works. "
                            "You MUST NOT use any of these words: "
                            "network, protocol, server, data, packet. "
                            "Find alternative ways to describe the concepts."
                        ),
                    },
                ],
                expected={
                    "checks": [
                        {
                            "type": "forbidden_words",
                            "words": ["network", "protocol", "server", "data", "packet"],
                        },
                    ],
                },
            ),
            # 3. Required format: bullet points.
            Task(
                task_id="if_bullet_format",
                description="Use exactly 5 bullet points",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "List benefits of exercise. "
                            "Format: exactly 5 bullet points using '- ' prefix. "
                            "Each bullet should be one line. No intro or conclusion text."
                        ),
                    },
                ],
                expected={
                    "checks": [
                        {"type": "bullet_count", "exact": 5},
                        {"type": "no_intro", "max_lines_before_bullets": 0},
                    ],
                },
            ),
            # 4. JSON output format.
            Task(
                task_id="if_json_output",
                description="Respond with valid JSON only",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Return a JSON object with the following keys: "
                            "'name' (string), 'age' (number), 'hobbies' (array of strings). "
                            "Use these values: name='Alice', age=30, hobbies=['reading', 'hiking']. "
                            "Return ONLY the JSON, no explanation."
                        ),
                    },
                ],
                expected={
                    "checks": [
                        {"type": "valid_json"},
                        {
                            "type": "json_keys",
                            "required_keys": ["name", "age", "hobbies"],
                        },
                        {
                            "type": "json_values",
                            "expected": {"name": "Alice", "age": 30},
                        },
                    ],
                },
            ),
            # 5. Uppercase constraint.
            Task(
                task_id="if_uppercase",
                description="Respond entirely in uppercase",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Write a motivational quote about perseverance. "
                            "Your ENTIRE response must be in UPPERCASE letters. "
                            "No lowercase letters at all."
                        ),
                    },
                ],
                expected={
                    "checks": [
                        {"type": "all_uppercase"},
                    ],
                },
            ),
            # 6. Multi-constraint task.
            Task(
                task_id="if_multi_constraint",
                description="Follow multiple formatting constraints simultaneously",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Write about the color blue. Follow ALL these rules:\n"
                            "1. Exactly 4 sentences.\n"
                            "2. Each sentence must start with a different letter.\n"
                            "3. Do not use the word 'color' or 'colour'.\n"
                            "4. Include at least one number."
                        ),
                    },
                ],
                expected={
                    "checks": [
                        {"type": "sentence_count", "exact": 4},
                        {
                            "type": "forbidden_words",
                            "words": ["color", "colour"],
                        },
                        {"type": "contains_number"},
                    ],
                },
            ),
        ]

    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        """Run all constraint checks and aggregate the score."""
        response = await adapter.send_message(messages=task.input_messages)
        text = response.strip()

        checks: list[dict] = task.expected["checks"]
        results: list[tuple[str, bool, str]] = []

        for check in checks:
            ctype = check["type"]
            passed, msg = self._run_check(ctype, check, text)
            results.append((ctype, passed, msg))

        passed_count = sum(1 for _, p, _ in results if p)
        score = passed_count / len(results) if results else 0.0

        detail_str = "; ".join(
            f"{name}:{'PASS' if p else 'FAIL'}({msg})" for name, p, msg in results
        )

        return TaskResult(
            task_id=task.task_id,
            score=round(score, 4),
            passed=score >= 0.5,
            message=detail_str,
            raw_response=response,
        )

    # ── Individual constraint checkers ───────────────────────────────

    @staticmethod
    def _run_check(ctype: str, spec: dict, text: str) -> tuple[bool, str]:
        """Dispatch to the right checker.  Returns (passed, detail_message)."""
        checkers = {
            "sentence_count": InstructionFollowingDimension._check_sentence_count,
            "forbidden_words": InstructionFollowingDimension._check_forbidden_words,
            "bullet_count": InstructionFollowingDimension._check_bullet_count,
            "no_intro": InstructionFollowingDimension._check_no_intro,
            "valid_json": InstructionFollowingDimension._check_valid_json,
            "json_keys": InstructionFollowingDimension._check_json_keys,
            "json_values": InstructionFollowingDimension._check_json_values,
            "all_uppercase": InstructionFollowingDimension._check_all_uppercase,
            "contains_number": InstructionFollowingDimension._check_contains_number,
        }
        fn = checkers.get(ctype)
        if fn is None:
            return False, f"unknown check type: {ctype}"
        return fn(spec, text)

    @staticmethod
    def _check_sentence_count(spec: dict, text: str) -> tuple[bool, str]:
        expected = spec["exact"]
        # Split on sentence-ending punctuation followed by space or end.
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        # Filter out empty fragments.
        sentences = [s for s in sentences if s.strip()]
        actual = len(sentences)
        return actual == expected, f"expected {expected}, got {actual}"

    @staticmethod
    def _check_forbidden_words(spec: dict, text: str) -> tuple[bool, str]:
        words: list[str] = spec["words"]
        found = [w for w in words if re.search(r'\b' + re.escape(w) + r'\b', text, re.IGNORECASE)]
        if found:
            return False, f"found: {found}"
        return True, "none found"

    @staticmethod
    def _check_bullet_count(spec: dict, text: str) -> tuple[bool, str]:
        expected = spec["exact"]
        bullets = re.findall(r"^- .+", text, re.MULTILINE)
        actual = len(bullets)
        return actual == expected, f"expected {expected}, got {actual}"

    @staticmethod
    def _check_no_intro(spec: dict, text: str) -> tuple[bool, str]:
        max_before = spec["max_lines_before_bullets"]
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("- "):
                return i <= max_before, f"first bullet at line {i}"
        return False, "no bullets found"

    @staticmethod
    def _check_valid_json(spec: dict, text: str) -> tuple[bool, str]:
        # Try to extract JSON from potential code blocks.
        json_text = text
        md_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if md_match:
            json_text = md_match.group(1)
        try:
            json.loads(json_text)
            return True, "valid JSON"
        except json.JSONDecodeError as e:
            return False, str(e)

    @staticmethod
    def _check_json_keys(spec: dict, text: str) -> tuple[bool, str]:
        required_keys: list[str] = spec["required_keys"]
        json_text = text
        md_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if md_match:
            json_text = md_match.group(1)
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            return False, "invalid JSON"
        if not isinstance(data, dict):
            return False, "not a JSON object"
        missing = [k for k in required_keys if k not in data]
        if missing:
            return False, f"missing keys: {missing}"
        return True, "all keys present"

    @staticmethod
    def _check_json_values(spec: dict, text: str) -> tuple[bool, str]:
        expected_values: dict = spec["expected"]
        json_text = text
        md_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
        if md_match:
            json_text = md_match.group(1)
        try:
            data = json.loads(json_text)
        except json.JSONDecodeError:
            return False, "invalid JSON"
        wrong = []
        for k, v in expected_values.items():
            if data.get(k) != v:
                wrong.append(f"{k}: expected {v!r}, got {data.get(k)!r}")
        if wrong:
            return False, "; ".join(wrong)
        return True, "values match"

    @staticmethod
    def _check_all_uppercase(spec: dict, text: str) -> tuple[bool, str]:
        # Only check alphabetic characters.
        alpha_chars = [c for c in text if c.isalpha()]
        if not alpha_chars:
            return False, "no alphabetic characters"
        upper_count = sum(1 for c in alpha_chars if c.isupper())
        ratio = upper_count / len(alpha_chars)
        # Allow a small tolerance (2%) for occasional slips.
        return ratio >= 0.98, f"uppercase ratio: {ratio:.2%}"

    @staticmethod
    def _check_contains_number(spec: dict, text: str) -> tuple[bool, str]:
        if re.search(r'\d', text):
            return True, "contains number"
        return False, "no number found"
