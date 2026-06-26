"""Provider health tracking: record outcomes, compute scores, smart ordering."""

from __future__ import annotations

import json
import logging
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .storage import _memory_root

logger = logging.getLogger(__name__)

# Health score weights
_W_SUCCESS = 0.50
_W_LATENCY = 0.30
_W_FRESHNESS = 0.20

# Latency thresholds (ms) for scoring: <= fast → 1.0, >= slow → 0.0
_LATENCY_FAST_MS = 500
_LATENCY_SLOW_MS = 5000

# Default analysis window
_DEFAULT_WINDOW_HOURS = 72

# Minimum records needed before health-based reordering kicks in
_MIN_RECORDS_FOR_REORDER = 5


def _health_storage_path() -> Path:
    return _memory_root() / "provider-health" / "health.jsonl"


class HealthTracker:
    """Tracks provider performance and computes health scores."""

    def __init__(self, storage_path: Path | None = None) -> None:
        self.path = storage_path or _health_storage_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        provider: str,
        *,
        success: bool,
        latency_ms: int,
        error_type: str | None = None,
    ) -> None:
        """Append a health record for a provider attempt."""
        entry = {
            "ts": datetime.now(UTC).isoformat(),
            "provider": provider,
            "success": success,
            "latency_ms": latency_ms,
            "error_type": error_type,
        }
        try:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            logger.warning("Failed to write health record for %s", provider, exc_info=True)

    def _load_records(self, window_hours: int = _DEFAULT_WINDOW_HOURS) -> list[dict[str, Any]]:
        """Load records within the time window."""
        if not self.path.exists():
            return []

        cutoff = datetime.now(UTC) - timedelta(hours=window_hours)
        records: list[dict[str, Any]] = []

        try:
            with self.path.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                        ts = datetime.fromisoformat(rec["ts"])
                        if ts >= cutoff:
                            records.append(rec)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        except OSError:
            logger.warning("Failed to read health records", exc_info=True)

        return records

    def get_scores(self, window_hours: int = _DEFAULT_WINDOW_HOURS) -> dict[str, float]:
        """Compute health scores (0.0–1.0) per provider within time window."""
        records = self._load_records(window_hours)
        if not records:
            return {}

        # Group by provider
        by_provider: dict[str, list[dict[str, Any]]] = {}
        for rec in records:
            name = rec.get("provider", "")
            if name:
                by_provider.setdefault(name, []).append(rec)

        now = datetime.now(UTC)
        scores: dict[str, float] = {}

        for name, recs in by_provider.items():
            # Success rate
            total = len(recs)
            successes = sum(1 for r in recs if r.get("success"))
            success_rate = successes / total if total > 0 else 0.0

            # Average latency score
            latencies = [r.get("latency_ms", _LATENCY_SLOW_MS) for r in recs]
            avg_latency = sum(latencies) / len(latencies) if latencies else _LATENCY_SLOW_MS
            # Map latency to 0.0–1.0 (lower is better)
            if avg_latency <= _LATENCY_FAST_MS:
                latency_score = 1.0
            elif avg_latency >= _LATENCY_SLOW_MS:
                latency_score = 0.0
            else:
                latency_score = 1.0 - (avg_latency - _LATENCY_FAST_MS) / (_LATENCY_SLOW_MS - _LATENCY_FAST_MS)

            # Freshness: how recent is the latest record
            latest_ts = max(
                (datetime.fromisoformat(r["ts"]) for r in recs),
                default=now - timedelta(hours=window_hours),
            )
            age_hours = (now - latest_ts).total_seconds() / 3600.0
            freshness = max(0.0, 1.0 - age_hours / window_hours)

            score = (
                _W_SUCCESS * success_rate
                + _W_LATENCY * latency_score
                + _W_FRESHNESS * freshness
            )
            scores[name] = round(min(1.0, max(0.0, score)), 4)

        return scores

    def get_summary(self, window_hours: int = _DEFAULT_WINDOW_HOURS) -> dict[str, Any]:
        """Return a dashboard-friendly summary of provider health."""
        records = self._load_records(window_hours)
        scores = self.get_scores(window_hours)

        # Group stats
        by_provider: dict[str, dict[str, Any]] = {}
        for rec in records:
            name = rec.get("provider", "")
            if not name:
                continue
            stats = by_provider.setdefault(name, {
                "total": 0, "successes": 0, "failures": 0,
                "latencies": [], "error_types": {},
            })
            stats["total"] += 1
            if rec.get("success"):
                stats["successes"] += 1
            else:
                stats["failures"] += 1
                et = rec.get("error_type", "unknown")
                stats["error_types"][et] = stats["error_types"].get(et, 0) + 1
            stats["latencies"].append(rec.get("latency_ms", 0))

        providers: list[dict[str, Any]] = []
        for name in sorted(by_provider.keys()):
            s = by_provider[name]
            lats = s["latencies"]
            providers.append({
                "provider": name,
                "health_score": scores.get(name, 0.0),
                "total_requests": s["total"],
                "success_rate": round(s["successes"] / s["total"], 4) if s["total"] > 0 else 0.0,
                "avg_latency_ms": round(sum(lats) / len(lats)) if lats else 0,
                "min_latency_ms": min(lats) if lats else 0,
                "max_latency_ms": max(lats) if lats else 0,
                "error_breakdown": s["error_types"],
            })

        providers.sort(key=lambda x: -x["health_score"])

        return {
            "window_hours": window_hours,
            "total_records": len(records),
            "providers": providers,
            "timestamp_utc": datetime.now(UTC).isoformat(),
        }

    def smart_order(self, base_order: list[str]) -> list[str]:
        """Reorder providers by health score, falling back to base_order for unknowns.

        Only reorders if enough data is available (_MIN_RECORDS_FOR_REORDER).
        Providers not in health data keep their base_order position.
        """
        scores = self.get_scores()

        # Check if we have enough data to reorder
        total_records = sum(
            1 for _ in self._load_records() if True
        )
        if total_records < _MIN_RECORDS_FOR_REORDER:
            return list(base_order)

        # Split into scored and unscored
        scored = [(name, scores[name]) for name in base_order if name in scores]
        unscored = [name for name in base_order if name not in scores]

        # Sort scored by health score descending
        scored.sort(key=lambda x: -x[1])

        # Interleave: scored first, then unscored in original order
        return [name for name, _ in scored] + unscored

    def compact(self, keep_hours: int = _DEFAULT_WINDOW_HOURS) -> int:
        """Remove records older than keep_hours. Returns number removed."""
        records = self._load_records(keep_hours)
        if not self.path.exists():
            return 0

        try:
            all_lines = self.path.read_text(encoding="utf-8").strip().split("\n")
            old_count = len([l for l in all_lines if l.strip()])
        except OSError:
            return 0

        new_count = len(records)
        removed = old_count - new_count

        if removed > 0:
            try:
                with self.path.open("w", encoding="utf-8") as f:
                    for rec in records:
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            except OSError:
                logger.warning("Failed to compact health records", exc_info=True)
                return 0

        return removed
