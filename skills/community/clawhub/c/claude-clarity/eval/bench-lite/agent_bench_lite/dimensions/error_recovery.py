"""
Error Recovery dimension.

Evaluates whether the agent can gracefully handle errors from tool calls
and API failures, recover, and still accomplish the task.  Tasks simulate
tool failures and check that the agent retries or takes an alternative path.
"""

from __future__ import annotations

import json
from typing import Any

from agent_bench_lite.adapters.base import BaseAdapter
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult


class ErrorRecoveryDimension(BaseDimension):
    """Can the agent handle and recover from errors?"""

    name = "error_recovery"
    display_name = "Error Recovery"
    description = (
        "Measures the agent's ability to detect errors from tool calls or "
        "invalid operations and recover gracefully — by retrying, using "
        "alternative tools, or informing the user constructively."
    )

    TOOLS: list[dict[str, Any]] = [
        {
            "name": "read_file",
            "description": "Read the contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"},
                },
                "required": ["path"],
            },
        },
        {
            "name": "write_file",
            "description": "Write content to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
        },
        {
            "name": "http_get",
            "description": "Make an HTTP GET request to a URL.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to fetch"},
                },
                "required": ["url"],
            },
        },
        {
            "name": "http_post",
            "description": "Make an HTTP POST request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL to post to"},
                    "body": {"type": "string", "description": "Request body (JSON string)"},
                },
                "required": ["url", "body"],
            },
        },
    ]

    def get_tasks(self) -> list[Task]:
        return [
            # 1. File not found — agent should acknowledge and adapt.
            Task(
                task_id="err_file_not_found",
                description="Handle file-not-found error",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Read the config file at /etc/app/config.yaml and summarize it."
                        ),
                    },
                ],
                expected={
                    "error_on_tool": "read_file",
                    "error_message": "FileNotFoundError: /etc/app/config.yaml does not exist",
                    "recovery_indicators": [
                        "not found", "does not exist", "couldn't",
                        "unable", "error", "cannot",
                    ],
                },
                tools=self.TOOLS,
            ),
            # 2. Network timeout — agent should retry or report.
            Task(
                task_id="err_http_timeout",
                description="Handle HTTP timeout gracefully",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Fetch the data from https://api.example.com/data "
                            "and show me the results."
                        ),
                    },
                ],
                expected={
                    "error_on_tool": "http_get",
                    "error_message": "TimeoutError: Request timed out after 30 seconds",
                    "max_retries": 3,
                    "recovery_indicators": [
                        "timeout", "timed out", "retry", "retri",
                        "failed", "unable", "error",
                    ],
                },
                tools=self.TOOLS,
            ),
            # 3. Permission denied — agent should inform user.
            Task(
                task_id="err_permission_denied",
                description="Handle permission denied on file write",
                input_messages=[
                    {
                        "role": "user",
                        "content": "Write 'hello world' to /etc/system/protected.txt",
                    },
                ],
                expected={
                    "error_on_tool": "write_file",
                    "error_message": "PermissionError: Write access denied for /etc/system/protected.txt",
                    "recovery_indicators": [
                        "permission", "denied", "access",
                        "cannot write", "unable", "error",
                    ],
                },
                tools=self.TOOLS,
            ),
            # 4. Malformed API response — agent should handle gracefully.
            Task(
                task_id="err_malformed_response",
                description="Handle a malformed API response",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Post the user data to https://api.example.com/users "
                            "with body {\"name\": \"Alice\"}"
                        ),
                    },
                ],
                expected={
                    "error_on_tool": "http_post",
                    "error_message": "Error 422: Unprocessable Entity — missing required field 'email'",
                    "recovery_indicators": [
                        "422", "missing", "email", "required",
                        "error", "failed", "unprocessable",
                    ],
                },
                tools=self.TOOLS,
            ),
        ]

    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        """Inject errors into tool calls and evaluate the agent's recovery."""
        error_tool: str = task.expected["error_on_tool"]
        error_msg: str = task.expected["error_message"]
        max_retries: int = task.expected.get("max_retries", 2)
        recovery_indicators: list[str] = task.expected["recovery_indicators"]

        call_log: list[dict[str, Any]] = []
        call_count = 0

        async def _tool_handler(name: str, params: dict[str, Any]) -> str:
            nonlocal call_count
            call_count += 1
            call_log.append({"name": name, "params": params, "call_number": call_count})

            if name == error_tool:
                # Always return an error for the designated tool.
                return json.dumps({"error": error_msg})

            # Other tools succeed normally.
            return json.dumps({"status": "ok", "result": "mock_result"})

        response = await adapter.send_message_with_tools(
            messages=task.input_messages,
            tools=task.tools,
            tool_handler=_tool_handler,
        )
        text = response.lower()

        score = 0.0

        # 1. Did the agent attempt the tool at all? (0.2)
        attempted = any(c["name"] == error_tool for c in call_log)
        if attempted:
            score += 0.2

        # 2. Did the agent mention the error / show awareness? (0.4)
        recovery_hits = sum(1 for ind in recovery_indicators if ind.lower() in text)
        awareness = min(recovery_hits / max(len(recovery_indicators) // 2, 1), 1.0)
        score += 0.4 * awareness

        # 3. Did the agent NOT loop excessively? (0.2)
        error_calls = sum(1 for c in call_log if c["name"] == error_tool)
        if error_calls <= max_retries:
            score += 0.2
        else:
            score += 0.1  # partial credit for trying

        # 4. Did the agent provide some kind of helpful fallback or explanation? (0.2)
        helpfulness_terms = [
            "suggest", "alternative", "instead", "try",
            "recommend", "sorry", "unfortunately", "let me",
        ]
        helpfulness = sum(1 for t in helpfulness_terms if t in text)
        score += 0.2 * min(helpfulness / 2, 1.0)

        score = min(score, 1.0)
        message = f"Calls: {len(call_log)}, error calls: {error_calls}, recovery signals: {recovery_hits}"

        return TaskResult(
            task_id=task.task_id,
            score=round(score, 4),
            passed=score >= 0.5,
            message=message,
            raw_response=response,
        )
