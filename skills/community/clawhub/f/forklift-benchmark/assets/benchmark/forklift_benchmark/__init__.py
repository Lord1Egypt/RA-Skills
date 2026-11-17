"""Forklift Embodied Intelligence Benchmark v2.

Top-level package providing:
  * Dataset loading and inspection for the 500-item FK-Bench v2 release.
  * Thin convenience re-exports for the action DSL, validators, and scorer.
  * Versioning metadata used by tooling, packaging, and `CITATION.cff`.

This package is intentionally minimal — the heavy lifting lives in the
``dsl/``, ``generator/``, ``validator/``, and ``scorer/`` subpackages. Those
subpackages are produced by sibling tasks in the build pipeline; when they
are absent (e.g. in a fresh checkout) the convenience imports degrade
gracefully to ``None`` so that the package can still be imported.
"""

from __future__ import annotations

__version__ = "2.0.0"
__all__ = ["__version__", "BENCHMARK_NAME", "DATASET_VERSION"]


BENCHMARK_NAME = "FK-Bench v2"
DATASET_VERSION = "2.0.0"


def get_version() -> str:
    """Return the human-readable version string for this benchmark release."""
    return __version__


try:  # pragma: no cover — convenience re-export
    from dsl.actions import ActionKind  # type: ignore
except Exception:  # pragma: no cover
    ActionKind = None  # type: ignore[assignment]

try:  # pragma: no cover
    from dsl.schema import Item  # type: ignore
except Exception:  # pragma: no cover
    Item = None  # type: ignore[assignment]

try:  # pragma: no cover
    from scorer.aggregate import score_item  # type: ignore
except Exception:  # pragma: no cover
    score_item = None  # type: ignore[assignment]
