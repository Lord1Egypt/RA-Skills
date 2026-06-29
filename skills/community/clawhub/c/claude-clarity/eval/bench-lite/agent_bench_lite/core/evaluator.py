"""
Evaluator: scoring logic that converts raw task results into dimension scores.

Each dimension receives a 0-100 score.  The overall score is a weighted
average of all dimension scores (equal weight by default).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_bench_lite.dimensions.base import BaseDimension, TaskResult


@dataclass(frozen=True)
class DimensionScore:
    """Score for a single evaluation dimension."""

    dimension_name: str
    """Machine-readable name of the dimension."""

    display_name: str
    """Human-readable name for reporting."""

    score: float
    """Aggregate score in [0, 100]."""

    passed: int
    """Number of tasks that passed."""

    failed: int
    """Number of tasks that failed."""

    total: int
    """Total number of tasks."""

    weight: float = 1.0
    """Weight used in overall aggregation."""

    task_details: list[dict[str, object]] = field(default_factory=list)
    """Per-task breakdown for detailed reports."""


class Evaluator:
    """Converts raw :class:`TaskResult` lists into :class:`DimensionScore` objects.

    Scoring strategy
    ----------------
    Each task contributes a score in ``[0.0, 1.0]``.  The dimension score is
    the mean task score scaled to ``[0, 100]``.

    Weighting
    ---------
    ``dimension_weights`` lets you override the default equal weighting.
    Keys are dimension *names*; values are positive floats.  Missing
    dimensions receive weight ``1.0``.
    """

    def __init__(self, dimension_weights: dict[str, float] | None = None) -> None:
        self.dimension_weights: dict[str, float] = dimension_weights or {}

    def score_dimension(
        self,
        dimension: BaseDimension,
        results: list[TaskResult],
    ) -> DimensionScore:
        """Compute the aggregate score for *dimension* from its task results."""
        if not results:
            return DimensionScore(
                dimension_name=dimension.name,
                display_name=dimension.display_name,
                score=0.0,
                passed=0,
                failed=0,
                total=0,
                weight=self.dimension_weights.get(dimension.name, 1.0),
            )

        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = total - passed

        # Mean score scaled to 0-100.
        raw = sum(r.score for r in results) / total
        score = round(min(max(raw * 100.0, 0.0), 100.0), 2)

        task_details = [
            {
                "task_id": r.task_id,
                "score": r.score,
                "passed": r.passed,
                "message": r.message,
            }
            for r in results
        ]

        return DimensionScore(
            dimension_name=dimension.name,
            display_name=dimension.display_name,
            score=score,
            passed=passed,
            failed=failed,
            total=total,
            weight=self.dimension_weights.get(dimension.name, 1.0),
            task_details=task_details,
        )

    def aggregate(self, scores: list[DimensionScore]) -> float:
        """Compute the weighted overall score from dimension scores.

        Returns a value in ``[0, 100]``, rounded to two decimal places.
        """
        if not scores:
            return 0.0

        weighted_sum = sum(s.score * s.weight for s in scores)
        total_weight = sum(s.weight for s in scores)
        if total_weight == 0:
            return 0.0
        return round(weighted_sum / total_weight, 2)
