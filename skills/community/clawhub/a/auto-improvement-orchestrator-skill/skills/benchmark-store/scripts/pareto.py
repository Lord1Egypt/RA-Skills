"""Pareto front tracking for multi-dimensional skill improvement."""

from __future__ import annotations
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import read_json, write_json, utc_now_iso


@dataclass
class ParetoEntry:
    """A point in the Pareto front."""
    run_id: str
    candidate_id: str
    scores: dict[str, float]  # dimension -> score
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = utc_now_iso()

    def dominates(self, other: "ParetoEntry") -> bool:
        """Returns True if self dominates other (better or equal in all, strictly better in at least one)."""
        all_dims = set(self.scores) | set(other.scores)
        dominated_dimensions = all(
            self.scores.get(d, 0) >= other.scores.get(d, 0)
            for d in all_dims
        )
        strictly_better = any(
            self.scores.get(d, 0) > other.scores.get(d, 0)
            for d in all_dims
        )
        return dominated_dimensions and strictly_better


class ParetoFront:
    """Maintains a Pareto front of non-dominated solutions."""

    def __init__(self, storage_path: Path | None = None):
        self.entries: list[ParetoEntry] = []
        self.storage_path = storage_path
        if storage_path and storage_path.exists():
            self._load()

    def add(self, entry: ParetoEntry) -> dict:
        """Try to add an entry. Returns {accepted, reason, dominated_count}."""
        # Check if new entry is dominated by any existing entry
        for existing in self.entries:
            if existing.dominates(entry):
                return {"accepted": False, "reason": "dominated_by_existing",
                        "dominator": existing.run_id}

        # Remove entries dominated by the new one
        dominated = [e for e in self.entries if entry.dominates(e)]
        self.entries = [e for e in self.entries if not entry.dominates(e)]
        self.entries.append(entry)

        if self.storage_path:
            self._save()

        return {"accepted": True, "reason": "added_to_front",
                "dominated_count": len(dominated),
                "front_size": len(self.entries)}

    # Per-dimension tolerance defaults: security is strict (2%), efficiency
    # is loose (10%), everything else gets 5%.
    DEFAULT_TOLERANCES: dict[str, float] = {
        "security": 0.02,
        "efficiency": 0.10,
    }
    DEFAULT_TOLERANCE = 0.05

    def check_regression(self, scores: dict[str, float],
                         tolerances: dict[str, float] | None = None) -> dict:
        """Check if new scores would cause a regression on any Pareto dimension.

        Args:
            scores: new candidate scores per dimension.
            tolerances: per-dimension tolerance overrides.  Falls back to
                DEFAULT_TOLERANCES, then DEFAULT_TOLERANCE (5%).
        """
        if not self.entries:
            return {"regressed": False, "details": "Empty front"}

        tols = {**self.DEFAULT_TOLERANCES, **(tolerances or {})}

        # Find the best score for each dimension across the front
        best_per_dim: dict[str, float] = {}
        for entry in self.entries:
            for dim, score in entry.scores.items():
                if dim not in best_per_dim or score > best_per_dim[dim]:
                    best_per_dim[dim] = score

        regressions = []
        for dim, best in best_per_dim.items():
            tol = tols.get(dim, self.DEFAULT_TOLERANCE)
            new_score = scores.get(dim, 0)
            if new_score < best * (1 - tol):
                regressions.append({"dimension": dim, "best": best, "new": new_score,
                                    "delta": new_score - best, "tolerance": tol})

        return {"regressed": len(regressions) > 0, "regressions": regressions,
                "dimensions_checked": len(best_per_dim)}

    def _save(self):
        write_json(self.storage_path, {"entries": [asdict(e) for e in self.entries],
                                        "updated_at": utc_now_iso()})

    def _load(self):
        data = read_json(self.storage_path)
        self.entries = [ParetoEntry(**e) for e in data.get("entries", [])]
