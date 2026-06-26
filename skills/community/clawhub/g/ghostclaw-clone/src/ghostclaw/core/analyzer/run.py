"""
Fingerprinting and fast comparison of analysis runs.

Enables O(1) delta detection by comparing content-addressed hashes of
issues, ghosts, flags, and metrics between two runs.
"""

import hashlib
from typing import Any, Dict, List


def _stable_hash(items: Any) -> str:
    """Compute a stable SHA-256 hash for a collection of items."""
    if not items:
        return hashlib.sha256(b"").hexdigest()
    try:
        # For lists of dicts, sorting ensures stable representation
        if isinstance(items, list):
            # Convert to a deterministic string representation
            normalized = repr(sorted(items)).encode("utf-8")
        else:
            normalized = repr(items).encode("utf-8")
    except Exception:
        normalized = repr(items).encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()


class FingerprintedRun:
    """
    Immutable fingerprint of a single analysis run.

    Attributes:
        issue_hash: SHA-256 of the issues list
        ghost_hash: SHA-256 of the architectural_ghosts list
        flag_hash: SHA-256 of the red_flags list
        metrics_hash: SHA-256 of the metrics dict
    """

    __slots__ = ("issue_hash", "ghost_hash", "flag_hash", "metrics_hash")

    def __init__(
        self,
        issue_hash: str,
        ghost_hash: str,
        flag_hash: str,
        metrics_hash: str,
    ):
        self.issue_hash = issue_hash
        self.ghost_hash = ghost_hash
        self.flag_hash = flag_hash
        self.metrics_hash = metrics_hash

    @classmethod
    def from_report(cls, report_data: Dict[str, Any]) -> "FingerprintedRun":
        """
        Create a FingerprintedRun from an analysis report dict.

        The report is expected to have top-level keys:
        'issues', 'architectural_ghosts', 'red_flags', 'metrics'.
        """
        issues = report_data.get("issues", [])
        ghosts = report_data.get("architectural_ghosts", [])
        flags = report_data.get("red_flags", [])
        metrics = report_data.get("metrics", {})

        if not isinstance(metrics, dict):
            metrics = {}

        # Compute metrics hash in a stable way: sorted items
        metrics_normalized = sorted(metrics.items())
        metrics_hash = _stable_hash(metrics_normalized)

        return cls(
            issue_hash=_stable_hash(issues),
            ghost_hash=_stable_hash(ghosts),
            flag_hash=_stable_hash(flags),
            metrics_hash=metrics_hash,
        )

    def as_dict(self) -> Dict[str, str]:
        return {
            "issue_hash": self.issue_hash,
            "ghost_hash": self.ghost_hash,
            "flag_hash": self.flag_hash,
            "metrics_hash": self.metrics_hash,
        }
