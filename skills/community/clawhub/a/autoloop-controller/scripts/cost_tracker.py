"""Immutable cost tracking for autoloop iterations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CostRecord:
    """Single cost entry from one pipeline run."""
    iteration: int
    cost_usd: float
    duration_seconds: float
    decision: str  # keep / reject / pending

    def to_dict(self) -> dict:
        return {"iteration": self.iteration, "cost_usd": self.cost_usd,
                "duration_seconds": self.duration_seconds, "decision": self.decision}


@dataclass(frozen=True, slots=True)
class CostTracker:
    """Immutable cost tracker — add() returns a new instance."""
    budget_limit: float = 50.0
    records: tuple[CostRecord, ...] = ()

    def add(self, record: CostRecord) -> "CostTracker":
        return CostTracker(
            budget_limit=self.budget_limit,
            records=(*self.records, record),
        )

    @property
    def total_cost(self) -> float:
        return sum(r.cost_usd for r in self.records)

    @property
    def total_duration(self) -> float:
        return sum(r.duration_seconds for r in self.records)

    @property
    def over_budget(self) -> bool:
        return self.total_cost >= self.budget_limit

    @property
    def iteration_count(self) -> int:
        return len(self.records)

    def summary(self) -> dict:
        return {
            "total_cost_usd": round(self.total_cost, 4),
            "total_duration_seconds": round(self.total_duration, 1),
            "budget_limit_usd": self.budget_limit,
            "over_budget": self.over_budget,
            "iterations": self.iteration_count,
            "records": [r.to_dict() for r in self.records],
        }
