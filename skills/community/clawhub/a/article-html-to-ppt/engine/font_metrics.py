"""Runtime font-metrics registry (P4).

Loads the pre-generated tables in engine/metrics/ (produced offline by
scripts/generate_font_metrics.py). Compile-time text measurement uses ONLY
these shipped tables — never live font queries — so the same engine
checkout produces identical geometry on every machine.

Lookup: exact family match (case/space-insensitive), else the DEFAULT
model — a slightly conservative width table so unmeasured fonts err
toward overflow-catching rather than overflow-shipping.
"""

from __future__ import annotations

import json
import unicodedata
from functools import lru_cache
from pathlib import Path

_METRICS_DIR = Path(__file__).resolve().parent / "metrics"

DEFAULT = {
    "family": "__default__",
    "ascii": None,        # falls through to the categorical model
    "cjk": 1.0,
    "fallback_wide": 1.0,
    "fallback_narrow": 0.38,
    "latin": 0.56,
}


def _norm(family: str) -> str:
    return "".join(family.lower().split())


@lru_cache(maxsize=1)
def _registry() -> dict[str, dict]:
    tables: dict[str, dict] = {}
    if _METRICS_DIR.is_dir():
        for path in sorted(_METRICS_DIR.glob("*.json")):
            try:
                table = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if table.get("family") and len(table.get("ascii") or []) == 95:
                tables[_norm(table["family"])] = table
    return tables


def table_for(family: str | None) -> dict:
    if family:
        table = _registry().get(_norm(family))
        if table:
            return table
    return DEFAULT


def char_width_em(char: str, family: str | None = None) -> float:
    table = table_for(family)
    cp = ord(char)
    if 0x20 <= cp <= 0x7E and table.get("ascii"):
        return table["ascii"][cp - 0x20]
    eaw = unicodedata.east_asian_width(char)
    if eaw in ("W", "F"):
        # Clamp to full width: fonts without real CJK glyphs report the
        # notdef/fallback advance, but the renderer substitutes a CJK face
        # that draws full-width. Under-estimating here would ship overflow.
        return max(table.get("cjk", 1.0), 1.0)
    if 0x20 <= cp <= 0x7E:  # default model: categorical latin
        if char.isspace() or unicodedata.category(char).startswith("P"):
            return table.get("fallback_narrow", 0.38)
        return table.get("latin", 0.56)
    if char.isspace() or unicodedata.category(char).startswith("P"):
        return table.get("fallback_narrow", 0.38)
    return table.get("fallback_wide", 1.0) * 0.62


def measured_families() -> list[str]:
    return sorted(t["family"] for t in _registry().values())
