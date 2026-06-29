"""
Planning & Decomposition dimension.

Evaluates whether the agent can break down a complex task into a clear,
ordered set of sub-steps.  The agent is asked to produce a plan; the
evaluator checks that key required steps are present and reasonably ordered.
"""

from __future__ import annotations

import re

from agent_bench_lite.adapters.base import BaseAdapter
from agent_bench_lite.dimensions.base import BaseDimension, Task, TaskResult


class PlanningDimension(BaseDimension):
    """Can the agent break complex tasks into logical steps?"""

    name = "planning"
    display_name = "Planning & Decomposition"
    description = (
        "Measures the agent's ability to decompose a complex goal into a "
        "clear, ordered sequence of actionable sub-steps."
    )

    def get_tasks(self) -> list[Task]:
        return [
            # 1. Plan a website deployment.
            Task(
                task_id="plan_deploy_website",
                description="Plan the deployment of a web application",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "I need to deploy a new Python web application to production. "
                            "Create a step-by-step deployment plan. The app uses a PostgreSQL "
                            "database and needs HTTPS. List the steps clearly as a numbered list."
                        ),
                    },
                ],
                expected={
                    "required_concepts": [
                        "test",
                        "database",
                        "server",
                        "deploy",
                        "ssl",
                    ],
                    "min_steps": 4,
                },
            ),
            # 2. Plan a data migration.
            Task(
                task_id="plan_data_migration",
                description="Plan migration from SQL to NoSQL",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "We need to migrate our user data from a MySQL database to MongoDB. "
                            "There are 2 million records and we cannot have more than 5 minutes "
                            "of downtime. Give me a numbered step-by-step plan."
                        ),
                    },
                ],
                expected={
                    "required_concepts": [
                        "backup",
                        "schema",
                        "migrat",
                        "valid",
                        "downtime",
                    ],
                    "min_steps": 4,
                },
            ),
            # 3. Plan an incident response.
            Task(
                task_id="plan_incident_response",
                description="Plan response to a production outage",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Our main API is returning 500 errors for 20% of requests. "
                            "Create a numbered plan to diagnose and fix this production incident."
                        ),
                    },
                ],
                expected={
                    "required_concepts": [
                        "log",
                        "monitor",
                        "identif",
                        "fix",
                        "communicat",
                    ],
                    "min_steps": 4,
                },
            ),
            # 4. Plan a feature implementation.
            Task(
                task_id="plan_feature_auth",
                description="Plan implementation of authentication system",
                input_messages=[
                    {
                        "role": "user",
                        "content": (
                            "Plan the implementation of a user authentication system with "
                            "email/password login, OAuth2 social login, and two-factor "
                            "authentication. Provide numbered steps."
                        ),
                    },
                ],
                expected={
                    "required_concepts": [
                        "database",
                        "password",
                        "oauth",
                        "two-factor",
                        "test",
                    ],
                    "min_steps": 4,
                },
            ),
        ]

    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        """Check the agent's plan for required concepts and structure."""
        response = await adapter.send_message(messages=task.input_messages)
        text = response.lower()

        required: list[str] = task.expected["required_concepts"]
        min_steps: int = task.expected["min_steps"]

        # Check for numbered list structure.
        numbered_pattern = re.compile(r"(?:^|\n)\s*\d+[\.\)]\s+\S")
        steps_found = len(numbered_pattern.findall(text))

        # Check concept coverage.
        concepts_found = sum(1 for concept in required if concept in text)
        concept_ratio = concepts_found / len(required) if required else 1.0

        # Structure score: did they produce enough numbered steps?
        structure_score = min(steps_found / max(min_steps, 1), 1.0)

        # Weighted final score.
        score = 0.6 * concept_ratio + 0.4 * structure_score

        details = (
            f"Concepts: {concepts_found}/{len(required)}, "
            f"Steps found: {steps_found} (need >= {min_steps})"
        )

        return TaskResult(
            task_id=task.task_id,
            score=round(score, 4),
            passed=score >= 0.5,
            message=details,
            raw_response=response,
        )
