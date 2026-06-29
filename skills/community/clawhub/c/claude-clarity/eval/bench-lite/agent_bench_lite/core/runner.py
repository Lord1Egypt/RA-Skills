"""
Benchmark runner that orchestrates evaluation across all dimensions.

The runner coordinates adapter calls, task distribution, and result collection.
It supports both sequential and parallel (async) execution of dimension evaluations.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from agent_bench_lite.core.evaluator import DimensionScore, Evaluator
from agent_bench_lite.core.reporter import BenchmarkReport
from agent_bench_lite.dimensions.context_retention import ContextRetentionDimension
from agent_bench_lite.dimensions.error_recovery import ErrorRecoveryDimension
from agent_bench_lite.dimensions.instruction_following import InstructionFollowingDimension
from agent_bench_lite.dimensions.multi_step_reasoning import MultiStepReasoningDimension
from agent_bench_lite.dimensions.planning import PlanningDimension
from agent_bench_lite.dimensions.tool_calling import ToolCallingDimension

if TYPE_CHECKING:
    from agent_bench_lite.adapters.base import BaseAdapter
    from agent_bench_lite.dimensions.base import BaseDimension, TaskResult


# All built-in dimensions, instantiated by default.
DEFAULT_DIMENSIONS: list[type[BaseDimension]] = [
    ToolCallingDimension,
    PlanningDimension,
    ContextRetentionDimension,
    ErrorRecoveryDimension,
    InstructionFollowingDimension,
    MultiStepReasoningDimension,
]


@dataclass
class RunConfig:
    """Configuration for a benchmark run."""

    parallel: bool = True
    """Run dimension evaluations in parallel via asyncio."""

    max_concurrency: int = 4
    """Maximum number of concurrent dimension evaluations."""

    timeout_per_task: float = 60.0
    """Timeout in seconds for each individual task."""

    dimensions: list[str] | None = None
    """If set, only run these dimension names (filters from available)."""

    metadata: dict[str, str] = field(default_factory=dict)
    """Arbitrary metadata to include in the report (e.g. model name)."""


class BenchmarkRunner:
    """Orchestrates a full benchmark evaluation.

    Args:
        adapter: The LLM adapter to evaluate.
        dimensions: List of dimension instances. If ``None``, all built-in
            dimensions are used.
        config: Optional :class:`RunConfig` controlling execution behavior.

    Example::

        runner = BenchmarkRunner(adapter=my_adapter)
        report = await runner.run()
        report.print_summary()
    """

    def __init__(
        self,
        adapter: BaseAdapter,
        dimensions: list[BaseDimension] | None = None,
        config: RunConfig | None = None,
    ) -> None:
        self.adapter = adapter
        self.config = config or RunConfig()

        if dimensions is not None:
            self._dimensions = dimensions
        else:
            self._dimensions = [cls() for cls in DEFAULT_DIMENSIONS]

        # Apply dimension name filter if configured.
        if self.config.dimensions:
            allowed = set(self.config.dimensions)
            self._dimensions = [d for d in self._dimensions if d.name in allowed]

        self.evaluator = Evaluator()

    @property
    def dimensions(self) -> list[BaseDimension]:
        """Active dimensions for this run."""
        return list(self._dimensions)

    async def run(self) -> BenchmarkReport:
        """Execute the full benchmark and return a :class:`BenchmarkReport`.

        Each dimension is evaluated independently.  Tasks within a dimension
        are always executed sequentially (order may matter for multi-turn
        evaluations), but different dimensions can run in parallel.
        """
        start = time.perf_counter()

        if self.config.parallel and len(self._dimensions) > 1:
            dimension_results = await self._run_parallel()
        else:
            dimension_results = await self._run_sequential()

        elapsed = time.perf_counter() - start

        # Score each dimension.
        scores: list[DimensionScore] = []
        for dim, results in dimension_results:
            score = self.evaluator.score_dimension(dim, results)
            scores.append(score)

        overall = self.evaluator.aggregate(scores)

        return BenchmarkReport(
            scores=scores,
            overall_score=overall,
            elapsed_seconds=round(elapsed, 3),
            adapter_name=type(self.adapter).__name__,
            metadata=self.config.metadata,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _run_sequential(
        self,
    ) -> list[tuple[BaseDimension, list[TaskResult]]]:
        """Evaluate each dimension one after another."""
        results: list[tuple[BaseDimension, list[TaskResult]]] = []
        for dim in self._dimensions:
            task_results = await self._evaluate_dimension(dim)
            results.append((dim, task_results))
        return results

    async def _run_parallel(
        self,
    ) -> list[tuple[BaseDimension, list[TaskResult]]]:
        """Evaluate dimensions concurrently up to *max_concurrency*."""
        sem = asyncio.Semaphore(self.config.max_concurrency)

        async def _guarded(dim: BaseDimension) -> tuple[BaseDimension, list[TaskResult]]:
            async with sem:
                return (dim, await self._evaluate_dimension(dim))

        tasks = [_guarded(dim) for dim in self._dimensions]
        return list(await asyncio.gather(*tasks))

    async def _evaluate_dimension(
        self, dim: BaseDimension
    ) -> list[TaskResult]:
        """Run every task in *dim* against the adapter and collect results."""
        task_results: list[TaskResult] = []
        for task in dim.get_tasks():
            try:
                result = await asyncio.wait_for(
                    dim.evaluate_task(task, self.adapter),
                    timeout=self.config.timeout_per_task,
                )
            except asyncio.TimeoutError:
                from agent_bench_lite.dimensions.base import TaskResult

                result = TaskResult(
                    task_id=task.task_id,
                    score=0.0,
                    passed=False,
                    message=f"Task timed out after {self.config.timeout_per_task}s",
                )
            except Exception as exc:
                from agent_bench_lite.dimensions.base import TaskResult

                result = TaskResult(
                    task_id=task.task_id,
                    score=0.0,
                    passed=False,
                    message=f"Unexpected error: {exc!r}",
                )
            task_results.append(result)
        return task_results
