"""
Base classes for evaluation dimensions and task definitions.

Every evaluation dimension inherits from :class:`BaseDimension` and must
implement :meth:`get_tasks` and :meth:`evaluate_task`.
"""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from agent_bench_lite.adapters.base import BaseAdapter


@dataclass(frozen=True)
class Task:
    """A single evaluation task within a dimension.

    Attributes:
        task_id: Unique identifier for the task.
        description: Human-readable description shown to the agent.
        input_messages: Conversation messages to send to the adapter.
        expected: Ground-truth or expected behaviour metadata.
        tools: Optional tool definitions the agent may use.
        metadata: Arbitrary extra data for the evaluator.
    """

    task_id: str
    description: str
    input_messages: list[dict[str, str]]
    expected: dict[str, Any] = field(default_factory=dict)
    tools: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskResult:
    """Result of evaluating a single task.

    Attributes:
        task_id: Matches the originating :class:`Task`.
        score: A value in ``[0.0, 1.0]`` (1.0 = perfect).
        passed: Whether the task is considered passed (typically ``score >= 0.5``).
        message: Explanation of the score for debugging / reporting.
        raw_response: The full adapter response (kept for audit).
    """

    task_id: str
    score: float
    passed: bool
    message: str = ""
    raw_response: Any = None

    def __post_init__(self) -> None:
        # Clamp score to [0, 1].
        self.score = min(max(self.score, 0.0), 1.0)


class BaseDimension(abc.ABC):
    """Abstract base for an evaluation dimension.

    Subclasses define *what* to test (via :meth:`get_tasks`) and *how* to
    score it (via :meth:`evaluate_task`).

    Class attributes:
        name: Machine-readable slug (e.g. ``"tool_calling"``).
        display_name: Pretty name for reports (e.g. ``"Tool Calling Accuracy"``).
        description: Longer explanation of the dimension.
    """

    name: str = ""
    display_name: str = ""
    description: str = ""

    @abc.abstractmethod
    def get_tasks(self) -> list[Task]:
        """Return the ordered list of tasks for this dimension."""
        ...

    @abc.abstractmethod
    async def evaluate_task(self, task: Task, adapter: BaseAdapter) -> TaskResult:
        """Execute *task* against *adapter* and return a scored result.

        Implementations should:
        1. Send the task's ``input_messages`` (and optionally ``tools``)
           through the adapter.
        2. Compare the response to ``task.expected``.
        3. Return a :class:`TaskResult` with a score in ``[0, 1]``.
        """
        ...

    def __repr__(self) -> str:
        return f"<{type(self).__name__} name={self.name!r}>"
