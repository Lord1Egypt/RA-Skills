"""
Context Retention dimension.

Evaluates whether the agent can remember and correctly use information
provided earlier in the conversation.  Tasks are multi-turn: the first
messages establish context, and the final message asks the agent to recall
or use that context.
"""

from __future__ import annotations

from agent_bench_lite.adapters.base import BaseAdapter
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult


class ContextRetentionDimension(BaseDimension):
    """Can the agent remember and use earlier context?"""

    name = "context_retention"
    display_name = "Context Retention"
    description = (
        "Measures the agent's ability to retain facts, preferences, and "
        "constraints introduced earlier in a multi-turn conversation."
    )

    def get_tasks(self) -> list[Task]:
        return [
            # 1. Remember a stated preference.
            Task(
                task_id="ctx_remember_preference",
                description="Remember a user's dietary preference across turns",
                input_messages=[
                    {
                        "role": "user",
                        "content": "I'm vegetarian and allergic to nuts. Keep this in mind.",
                    },
                    {
                        "role": "assistant",
                        "content": "Got it! I'll remember that you're vegetarian and allergic to nuts.",
                    },
                    {
                        "role": "user",
                        "content": "Suggest a dinner recipe for me tonight.",
                    },
                ],
                expected={
                    "must_contain": ["vegetarian"],
                    "must_not_contain": [
                        "chicken", "beef", "pork", "steak",
                        "peanut", "almond", "walnut", "cashew",
                    ],
                },
            ),
            # 2. Remember a name and use it later.
            Task(
                task_id="ctx_remember_name",
                description="Remember and use someone's name",
                input_messages=[
                    {
                        "role": "user",
                        "content": "My name is Xiomara and my dog's name is Biscuit.",
                    },
                    {
                        "role": "assistant",
                        "content": "Nice to meet you, Xiomara! Biscuit sounds like a lovely dog.",
                    },
                    {
                        "role": "user",
                        "content": "Write a short birthday card for my dog.",
                    },
                ],
                expected={
                    "must_contain": ["biscuit"],
                    "must_not_contain": [],
                },
            ),
            # 3. Remember a numeric constraint.
            Task(
                task_id="ctx_remember_budget",
                description="Remember a budget constraint",
                input_messages=[
                    {
                        "role": "user",
                        "content": "My budget for the trip is exactly $1,500. I cannot go over this.",
                    },
                    {
                        "role": "assistant",
                        "content": "Understood — I'll keep everything within $1,500.",
                    },
                    {
                        "role": "user",
                        "content": (
                            "Plan a 3-day trip to Portland, Oregon for me. "
                            "Include flights, hotel, and activities with estimated costs."
                        ),
                    },
                ],
                expected={
                    "must_contain": ["1500", "1,500", "$1500", "$1,500"],
                    "must_contain_mode": "any",
                    "must_not_contain": [],
                },
            ),
            # 4. Retain multiple facts from a context dump.
            Task(
                task_id="ctx_multiple_facts",
                description="Retain several facts from a briefing",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Here are the project details:\n"
                            "- Project name: Aurora\n"
                            "- Language: Rust\n"
                            "- Team lead: Priya Sharma\n"
                            "- Deadline: June 15, 2026\n"
                            "- Priority: Critical\n"
                            "Remember all of this."
                        ),
                    },
                    {
                        "role": "assistant",
                        "content": (
                            "I've noted the project details: Aurora, written in Rust, "
                            "led by Priya Sharma, due June 15 2026, critical priority."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Write a brief status email to stakeholders about our project. "
                            "Include the project name, language, team lead, and deadline."
                        ),
                    },
                ],
                expected={
                    "must_contain": ["aurora", "rust", "priya", "june"],
                    "must_not_contain": [],
                },
            ),
            # 5. Remember a correction / update.
            Task(
                task_id="ctx_correction",
                description="Remember a correction to earlier information",
                input_messages=[
                    {
                        "role": "user",
                        "content": "The meeting is on Wednesday at 2pm.",
                    },
                    {
                        "role": "assistant",
                        "content": "Got it — meeting on Wednesday at 2pm.",
                    },
                    {
                        "role": "user",
                        "content": "Actually, it's been moved to Thursday at 3pm.",
                    },
                    {
                        "role": "assistant",
                        "content": "Updated — the meeting is now Thursday at 3pm.",
                    },
                    {
                        "role": "user",
                        "content": "When is the meeting?",
                    },
                ],
                expected={
                    "must_contain": ["thursday", "3"],
                    "must_not_contain": ["wednesday", "2pm"],
                },
            ),
        ]

    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        """Check that the response references the correct earlier context."""
        response = await adapter.send_message(messages=task.input_messages)
        text = response.lower()

        must_contain: list[str] = task.expected["must_contain"]
        must_not_contain: list[str] = task.expected.get("must_not_contain", [])
        mode: str = task.expected.get("must_contain_mode", "all")

        # Positive checks.
        if mode == "any":
            positive_hits = 1 if any(kw.lower() in text for kw in must_contain) else 0
            positive_total = 1
        else:
            positive_hits = sum(1 for kw in must_contain if kw.lower() in text)
            positive_total = len(must_contain) if must_contain else 1

        positive_ratio = positive_hits / positive_total

        # Negative checks (penalty for forbidden content).
        violations = sum(1 for kw in must_not_contain if kw.lower() in text)
        penalty = violations * 0.2

        score = max(positive_ratio - penalty, 0.0)

        msg_parts = [f"Positive: {positive_hits}/{positive_total}"]
        if violations:
            msg_parts.append(f"Violations: {violations}")
        message = ", ".join(msg_parts)

        return TaskResult(
            task_id=task.task_id,
            score=round(score, 4),
            passed=score >= 0.5,
            message=message,
            raw_response=response,
        )
