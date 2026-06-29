"""
Tool Calling Accuracy dimension.

Evaluates whether the agent can select the correct tool and provide accurate
parameters.  Tasks present the agent with a set of available tools and a user
request that should be fulfilled by calling a specific tool with specific
arguments.
"""

from __future__ import annotations

import json
from typing import Any

from agent_bench_lite.adapters.base import BaseAdapter
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult


def _normalize(value: Any) -> Any:
    """Normalize a value for comparison (lowercase strings, sort lists)."""
    if isinstance(value, str):
        return value.strip().lower()
    if isinstance(value, list):
        return sorted(_normalize(v) for v in value)
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    return value


class ToolCallingDimension(BaseDimension):
    """Can the agent call the right tools with correct parameters?"""

    name = "tool_calling"
    display_name = "Tool Calling Accuracy"
    description = (
        "Measures the agent's ability to select the correct tool from a set "
        "of candidates and provide accurate, well-formed parameters."
    )

    # ── Tool definitions used across tasks ───────────────────────────

    TOOLS: list[dict[str, Any]] = [
        {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"},
                    "units": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature units",
                    },
                },
                "required": ["city"],
            },
        },
        {
            "name": "search_database",
            "description": "Search a database table by query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "table": {"type": "string", "description": "Table name"},
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {
                        "type": "integer",
                        "description": "Max results to return",
                        "default": 10,
                    },
                },
                "required": ["table", "query"],
            },
        },
        {
            "name": "send_email",
            "description": "Send an email to a recipient.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body text"},
                },
                "required": ["to", "subject", "body"],
            },
        },
        {
            "name": "calculate",
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate, e.g. '2 + 2'",
                    },
                },
                "required": ["expression"],
            },
        },
        {
            "name": "create_calendar_event",
            "description": "Create a new calendar event.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Event title"},
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                    "time": {"type": "string", "description": "Time in HH:MM format"},
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Duration in minutes",
                    },
                },
                "required": ["title", "date", "time"],
            },
        },
    ]

    def get_tasks(self) -> list[Task]:
        return [
            # 1. Simple single-tool selection with required param.
            Task(
                task_id="tc_select_weather",
                description="Select the weather tool with correct city",
                input_messages=[
                    {"role": "user", "content": "What's the weather like in Tokyo?"},
                ],
                expected={
                    "tool_name": "get_weather",
                    "required_params": {"city": "tokyo"},
                },
                tools=self.TOOLS,
            ),
            # 2. Tool with optional parameter.
            Task(
                task_id="tc_weather_units",
                description="Select weather tool with explicit units",
                input_messages=[
                    {
                        "role": "user",
                        "content": "Tell me the temperature in Berlin in fahrenheit.",
                    },
                ],
                expected={
                    "tool_name": "get_weather",
                    "required_params": {"city": "berlin", "units": "fahrenheit"},
                },
                tools=self.TOOLS,
            ),
            # 3. Database search.
            Task(
                task_id="tc_db_search",
                description="Search the users table",
                input_messages=[
                    {
                        "role": "user",
                        "content": "Find all users named Alice in the users table, limit to 5 results.",
                    },
                ],
                expected={
                    "tool_name": "search_database",
                    "required_params": {"table": "users", "query": "alice", "limit": 5},
                },
                tools=self.TOOLS,
            ),
            # 4. Email composition.
            Task(
                task_id="tc_send_email",
                description="Send email with all required fields",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Send an email to bob@example.com with subject 'Meeting Tomorrow' "
                            "and body 'Hi Bob, let's meet at 3pm.'"
                        ),
                    },
                ],
                expected={
                    "tool_name": "send_email",
                    "required_params": {
                        "to": "bob@example.com",
                        "subject": "meeting tomorrow",
                        "body": "hi bob, let's meet at 3pm.",
                    },
                },
                tools=self.TOOLS,
            ),
            # 5. Math calculation.
            Task(
                task_id="tc_calculate",
                description="Use the calculate tool for arithmetic",
                input_messages=[
                    {"role": "user", "content": "What is (15 * 4) + 23?"},
                ],
                expected={
                    "tool_name": "calculate",
                    "required_params": {},  # any expression mentioning the numbers is fine
                    "must_contain_in_expression": ["15", "4", "23"],
                },
                tools=self.TOOLS,
            ),
            # 6. Calendar event creation.
            Task(
                task_id="tc_calendar_event",
                description="Create a calendar event with all fields",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Schedule a meeting called 'Project Review' on 2026-04-15 "
                            "at 14:00 for 90 minutes."
                        ),
                    },
                ],
                expected={
                    "tool_name": "create_calendar_event",
                    "required_params": {
                        "title": "project review",
                        "date": "2026-04-15",
                        "time": "14:00",
                        "duration_minutes": 90,
                    },
                },
                tools=self.TOOLS,
            ),
        ]

    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        """Send the task and check that the adapter chose the right tool + params."""
        tool_calls: list[dict[str, Any]] = []

        async def _tool_handler(name: str, params: dict[str, Any]) -> str:
            tool_calls.append({"name": name, "params": params})
            return json.dumps({"status": "ok", "result": "mock_result"})

        await adapter.send_message_with_tools(
            messages=task.input_messages,
            tools=task.tools,
            tool_handler=_tool_handler,
        )

        if not tool_calls:
            return TaskResult(
                task_id=task.task_id,
                score=0.0,
                passed=False,
                message="Agent did not call any tool.",
            )

        call = tool_calls[0]
        expected_tool = task.expected["tool_name"]

        # Check tool name.
        if _normalize(call["name"]) != _normalize(expected_tool):
            return TaskResult(
                task_id=task.task_id,
                score=0.1,
                passed=False,
                message=f"Wrong tool: expected '{expected_tool}', got '{call['name']}'.",
            )

        # Check required parameters.
        score = 0.5  # correct tool selection = half credit
        required = task.expected.get("required_params", {})
        if required:
            matched = 0
            for key, expected_val in required.items():
                actual_val = call["params"].get(key)
                if _normalize(actual_val) == _normalize(expected_val):
                    matched += 1
            param_score = matched / len(required)
            score += 0.5 * param_score
        else:
            score = 0.9  # no specific param check; bonus for correct tool

        # Extra check: must_contain_in_expression (for the calculate task).
        must_contain = task.expected.get("must_contain_in_expression", [])
        if must_contain:
            expr = str(call["params"].get("expression", ""))
            all_present = all(tok in expr for tok in must_contain)
            if all_present:  # noqa: SIM108
                score = max(score, 0.9)
            else:
                score = max(score - 0.2, 0.3)

        passed = score >= 0.5
        return TaskResult(
            task_id=task.task_id,
            score=round(score, 4),
            passed=passed,
            message=f"Tool: {call['name']}, params: {call['params']}",
            raw_response=tool_calls,
        )
