#!/usr/bin/env python3
"""
Agent Scorecard — Historical Tracking & Trend Analysis
========================================================
Load evaluation history, compute trends, compare periods, detect regressions.

Usage:
    from scorecard_track import Tracker
    tracker = Tracker("scorecard_history.jsonl")
    trend = tracker.trend("accuracy", last_n=20)
    comparison = tracker.compare(before_n=10, after_n=10)

CLI:
    python3 scorecard_track.py --history scorecard_history.jsonl --trend accuracy
    python3 scorecard_track.py --history scorecard_history.jsonl --compare 10
    python3 scorecard_track.py --history scorecard_history.jsonl --summary
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TrendResult:
    dimension: str
    scores: List[float]
    mean: float
    std_dev: float
    direction: str  # "improving", "degrading", "stable"
    slope: float
    min_score: float
    max_score: float
    count: int

    def sparkline(self) -> str:
        """ASCII sparkline of scores."""
        if not self.scores:
            return ""
        blocks = " ▁▂▃▄▅▆▇█"
        mn, mx = min(self.scores), max(self.scores)
        rng = mx - mn if mx != mn else 1
        return "".join(
            blocks[min(len(blocks) - 1, int((s - mn) / rng * (len(blocks) - 1)))]
            for s in self.scores
        )


@dataclass
class ComparisonResult:
    dimension: str
    before_mean: float
    after_mean: float
    delta: float
    direction: str  # "improved", "degraded", "unchanged"
    before_count: int
    after_count: int


class Tracker:
    """Load and analyse evaluation history."""

    def __init__(self, history_path: str):
        self.path = history_path
        self._records: List[dict] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self._records.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except FileNotFoundError:
            self._records = []

    @property
    def records(self) -> List[dict]:
        return list(self._records)

    def filter(
        self,
        agent: Optional[str] = None,
        task_type: Optional[str] = None,
        last_n: Optional[int] = None,
    ) -> List[dict]:
        recs = self._records
        if agent:
            recs = [r for r in recs if r.get("agent") == agent]
        if task_type:
            recs = [r for r in recs if r.get("task_type") == task_type]
        if last_n and last_n > 0:
            recs = recs[-last_n:]
        return recs

    def _extract_dim_scores(
        self, records: List[dict], dimension: str
    ) -> List[float]:
        scores: List[float] = []
        for rec in records:
            for dim in rec.get("dimensions", []):
                if dim.get("name") == dimension:
                    scores.append(dim["score"])
                    break
        return scores

    def _extract_overall(self, records: List[dict]) -> List[float]:
        return [r["overall_score"] for r in records if "overall_score" in r]

    @staticmethod
    def _linear_slope(values: List[float]) -> float:
        n = len(values)
        if n < 2:
            return 0.0
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        num = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        den = sum((i - x_mean) ** 2 for i in range(n))
        return num / den if den else 0.0

    @staticmethod
    def _stats(values: List[float]) -> tuple:
        if not values:
            return 0.0, 0.0, 0.0, 0.0
        mean = sum(values) / len(values)
        var = sum((v - mean) ** 2 for v in values) / len(values)
        return mean, math.sqrt(var), min(values), max(values)

    def trend(
        self,
        dimension: str = "overall",
        agent: Optional[str] = None,
        task_type: Optional[str] = None,
        last_n: Optional[int] = None,
    ) -> TrendResult:
        recs = self.filter(agent=agent, task_type=task_type, last_n=last_n)
        if dimension == "overall":
            scores = self._extract_overall(recs)
        else:
            scores = self._extract_dim_scores(recs, dimension)

        mean, std, mn, mx = self._stats(scores)
        slope = self._linear_slope(scores)

        if abs(slope) < 0.05:
            direction = "stable"
        elif slope > 0:
            direction = "improving"
        else:
            direction = "degrading"

        return TrendResult(
            dimension=dimension,
            scores=scores,
            mean=round(mean, 3),
            std_dev=round(std, 3),
            direction=direction,
            slope=round(slope, 4),
            min_score=round(mn, 3) if scores else 0.0,
            max_score=round(mx, 3) if scores else 0.0,
            count=len(scores),
        )

    def compare(
        self,
        before_n: int = 10,
        after_n: int = 10,
        agent: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> List[ComparisonResult]:
        """Compare the last after_n evals to the before_n evals preceding them."""
        recs = self.filter(agent=agent, task_type=task_type)
        if len(recs) < before_n + after_n:
            before_recs = recs[: len(recs) // 2]
            after_recs = recs[len(recs) // 2 :]
        else:
            after_recs = recs[-after_n:]
            before_recs = recs[-(before_n + after_n) : -after_n]

        # Collect all dimension names
        dim_names: list[str] = ["overall"]
        for rec in recs:
            for d in rec.get("dimensions", []):
                if d["name"] not in dim_names:
                    dim_names.append(d["name"])

        results: list[ComparisonResult] = []
        for dim in dim_names:
            if dim == "overall":
                before_scores = self._extract_overall(before_recs)
                after_scores = self._extract_overall(after_recs)
            else:
                before_scores = self._extract_dim_scores(before_recs, dim)
                after_scores = self._extract_dim_scores(after_recs, dim)

            b_mean = sum(before_scores) / len(before_scores) if before_scores else 0
            a_mean = sum(after_scores) / len(after_scores) if after_scores else 0
            delta = a_mean - b_mean

            if abs(delta) < 0.1:
                direction = "unchanged"
            elif delta > 0:
                direction = "improved"
            else:
                direction = "degraded"

            results.append(ComparisonResult(
                dimension=dim,
                before_mean=round(b_mean, 3),
                after_mean=round(a_mean, 3),
                delta=round(delta, 3),
                direction=direction,
                before_count=len(before_scores),
                after_count=len(after_scores),
            ))

        return results

    def summary(
        self,
        agent: Optional[str] = None,
        task_type: Optional[str] = None,
    ) -> str:
        recs = self.filter(agent=agent, task_type=task_type)
        if not recs:
            return "No evaluation history found."

        lines = [
            f"History: {len(recs)} evaluations",
        ]
        # Overall trend
        ot = self.trend("overall", agent=agent, task_type=task_type)
        lines.append(
            f"Overall: mean={ot.mean}, trend={ot.direction} "
            f"(slope={ot.slope}) {ot.sparkline()}"
        )

        # Per-dimension
        dim_names: list[str] = []
        for rec in recs:
            for d in rec.get("dimensions", []):
                if d["name"] not in dim_names:
                    dim_names.append(d["name"])

        for dim in dim_names:
            t = self.trend(dim, agent=agent, task_type=task_type)
            lines.append(
                f"  {dim}: mean={t.mean}, {t.direction} "
                f"(slope={t.slope}) {t.sparkline()}"
            )

        # Pass rate
        passed = sum(1 for r in recs if r.get("overall_passed"))
        lines.append(f"Pass rate: {passed}/{len(recs)} ({100*passed/len(recs):.0f}%)")

        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Scorecard — trend analysis")
    parser.add_argument("--history", required=True, help="Path to JSONL history file")
    parser.add_argument("--trend", default=None, help="Show trend for dimension (or 'overall')")
    parser.add_argument("--compare", type=int, default=None, help="Compare last N vs previous N")
    parser.add_argument("--summary", action="store_true", help="Show full summary")
    parser.add_argument("--agent", default=None, help="Filter by agent")
    parser.add_argument("--task", default=None, help="Filter by task type")
    parser.add_argument("--last", type=int, default=None, help="Use only last N records")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    tracker = Tracker(args.history)

    if args.summary:
        if args.json:
            recs = tracker.filter(agent=args.agent, task_type=args.task)
            print(json.dumps({"count": len(recs), "records": recs}, indent=2))
        else:
            print(tracker.summary(agent=args.agent, task_type=args.task))
        return

    if args.trend:
        t = tracker.trend(
            args.trend, agent=args.agent, task_type=args.task, last_n=args.last
        )
        if args.json:
            print(json.dumps({
                "dimension": t.dimension, "mean": t.mean, "std_dev": t.std_dev,
                "direction": t.direction, "slope": t.slope, "count": t.count,
                "min": t.min_score, "max": t.max_score, "scores": t.scores,
            }, indent=2))
        else:
            print(f"{t.dimension}: mean={t.mean}, {t.direction} (slope={t.slope})")
            print(f"  range: {t.min_score}–{t.max_score}, std_dev={t.std_dev}, n={t.count}")
            print(f"  {t.sparkline()}")
        return

    if args.compare is not None:
        n = args.compare
        results = tracker.compare(before_n=n, after_n=n, agent=args.agent, task_type=args.task)
        if args.json:
            print(json.dumps([{
                "dimension": r.dimension, "before": r.before_mean,
                "after": r.after_mean, "delta": r.delta, "direction": r.direction,
            } for r in results], indent=2))
        else:
            for r in results:
                symbol = {"improved": "↑", "degraded": "↓", "unchanged": "→"}[r.direction]
                print(f"  {symbol} {r.dimension}: {r.before_mean} → {r.after_mean} ({r.delta:+.3f})")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
