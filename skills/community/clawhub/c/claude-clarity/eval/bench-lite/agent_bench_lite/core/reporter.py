"""
Reporter: formats benchmark results for CLI display and JSON export.

Provides a :class:`BenchmarkReport` dataclass that holds scores and metadata,
with methods for pretty-printing and serialization.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import TextIO

from agent_bench_lite.core.evaluator import DimensionScore

# ── ANSI colour helpers (no external dependency) ─────────────────────

class _Color:
    """Minimal ANSI colour codes for terminal output."""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_GREEN = "\033[42m"
    BG_RED = "\033[41m"
    BG_YELLOW = "\033[43m"

    @staticmethod
    def score_color(score: float) -> str:
        """Return an ANSI colour appropriate for *score* (0-100)."""
        if score >= 80:
            return _Color.GREEN
        if score >= 50:
            return _Color.YELLOW
        return _Color.RED

    @staticmethod
    def score_badge(score: float) -> str:
        """Return a coloured background badge for *score*."""
        if score >= 80:
            bg = _Color.BG_GREEN
        elif score >= 50:
            bg = _Color.BG_YELLOW
        else:
            bg = _Color.BG_RED
        return f"{bg}{_Color.WHITE}{_Color.BOLD} {score:6.2f} {_Color.RESET}"


# ── Bar chart helper ─────────────────────────────────────────────────

def _bar(score: float, width: int = 30) -> str:
    """Render a horizontal bar of *width* characters filled proportionally."""
    filled = round(score / 100.0 * width)
    empty = width - filled
    color = _Color.score_color(score)
    return f"{color}{'█' * filled}{_Color.DIM}{'░' * empty}{_Color.RESET}"


# ── Report dataclass ─────────────────────────────────────────────────

@dataclass
class BenchmarkReport:
    """Immutable report produced by :class:`BenchmarkRunner`.

    Attributes:
        scores: Per-dimension score breakdowns.
        overall_score: Weighted aggregate (0-100).
        elapsed_seconds: Wall-clock time for the full run.
        adapter_name: Name of the adapter class used.
        metadata: Extra metadata (model name, version, etc.).
        timestamp: ISO-8601 creation timestamp (auto-populated).
    """

    scores: list[DimensionScore]
    overall_score: float
    elapsed_seconds: float
    adapter_name: str
    metadata: dict[str, str] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    # ── Pretty CLI output ────────────────────────────────────────────

    def print_summary(self, file: TextIO | None = None) -> None:
        """Print a colourful summary table to *file* (defaults to stdout)."""
        import sys

        out = file or sys.stdout
        w = out.write

        line = f"{_Color.DIM}{'─' * 72}{_Color.RESET}\n"

        w("\n")
        box_top = "╔══════════════════════════════════════════════════════════╗"
        box_mid = "║         agent-bench-lite  Evaluation Report             ║"
        box_bot = "╚══════════════════════════════════════════════════════════╝"
        bc = f"{_Color.BOLD}{_Color.CYAN}"
        w(f"{bc}  {box_top}{_Color.RESET}\n")
        w(f"{bc}  {box_mid}{_Color.RESET}\n")
        w(f"{bc}  {box_bot}{_Color.RESET}\n")
        w("\n")

        w(f"  {_Color.DIM}Adapter:{_Color.RESET}  {_Color.BOLD}{self.adapter_name}{_Color.RESET}\n")
        w(f"  {_Color.DIM}Time:{_Color.RESET}     {self.elapsed_seconds:.3f}s\n")
        w(f"  {_Color.DIM}Date:{_Color.RESET}     {self.timestamp}\n")
        if self.metadata:
            for k, v in self.metadata.items():
                w(f"  {_Color.DIM}{k}:{_Color.RESET}  {v}\n")
        w("\n")
        w(line)
        w(f"  {_Color.BOLD}{'Dimension':<32} {'Score':>7}  {'Pass':>5}  Bar{_Color.RESET}\n")
        w(line)

        for ds in sorted(self.scores, key=lambda s: s.score, reverse=True):
            color = _Color.score_color(ds.score)
            bar = _bar(ds.score)
            pass_str = f"{ds.passed}/{ds.total}"
            w(
                f"  {ds.display_name:<32} "
                f"{color}{ds.score:>6.2f}{_Color.RESET}  "
                f"{pass_str:>5}  {bar}\n"
            )

        w(line)

        badge = _Color.score_badge(self.overall_score)
        w(f"\n  {_Color.BOLD}Overall Score:{_Color.RESET}  {badge}\n\n")

    # ── Detailed per-task output ─────────────────────────────────────

    def print_details(self, file: TextIO | None = None) -> None:
        """Print per-task details for every dimension."""
        import sys

        out = file or sys.stdout
        w = out.write

        for ds in self.scores:
            color = _Color.score_color(ds.score)
            w(f"\n{_Color.BOLD}{color}▸ {ds.display_name}{_Color.RESET}  ({ds.score:.2f}/100)\n")
            for td in ds.task_details:
                icon = (
                    f"{_Color.GREEN}✓{_Color.RESET}"
                    if td["passed"]
                    else f"{_Color.RED}✗{_Color.RESET}"
                )
                msg = td["message"]
                tid = td["task_id"]
                sc = td["score"]
                w(f"    {icon}  {tid:<36}  score={sc:.2f}"
                  f"  {_Color.DIM}{msg}{_Color.RESET}\n")

    # ── JSON serialization ───────────────────────────────────────────

    def to_dict(self) -> dict:
        """Return the report as a plain dictionary (JSON-serializable)."""
        return {
            "overall_score": self.overall_score,
            "elapsed_seconds": self.elapsed_seconds,
            "adapter": self.adapter_name,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "dimensions": [asdict(s) for s in self.scores],
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize the report to a JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def save_json(self, path: str | Path) -> Path:
        """Write the JSON report to *path* and return the resolved path."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(), encoding="utf-8")
        return p.resolve()
