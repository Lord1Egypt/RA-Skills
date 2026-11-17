"""FK-Bench v2 — Item JSON schema validator.

This is a lightweight structural validator (no pydantic dependency). For
schema-level rules it is the same logic as ``dsl.schema.validate_item_dict``
but kept in the validator package so consumers can run schema validation
without importing the generator code.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from dsl import (
    ACTION_KINDS,
    DIFFICULTIES,
    MODULES,
    SCENES,
)
from dsl.schema import validate_item_dict, validate_item_json

__all__ = ["validate_item_dict", "validate_item_json"]


def assert_distribution(items: List[Any]) -> List[str]:
    """Return a list of distribution violations (empty list == OK)."""
    from collections import Counter
    from dsl import MOD_DIST, SCENE_DIST

    errors: List[str] = []

    mod_counts: Counter[str] = Counter(it.meta.module for it in items)
    for m, want in MOD_DIST.items():
        expected = sum(want.values())
        if mod_counts.get(m, 0) != expected:
            errors.append(f"module {m}: expected {expected} items, got {mod_counts.get(m, 0)}")

    scene_counts: Counter[str] = Counter(it.meta.scene_type for it in items)
    for s, want in SCENE_DIST.items():
        expected = sum(want.values())
        if scene_counts.get(s, 0) != expected:
            errors.append(f"scene {s}: expected {expected} items, got {scene_counts.get(s, 0)}")

    diff_counts: Counter[str] = Counter(it.meta.difficulty for it in items)
    want_diff = {
        "basic": sum(d["basic"] for d in MOD_DIST.values()),
        "intermediate": sum(d["intermediate"] for d in MOD_DIST.values()),
        "edge_case": sum(d["edge_case"] for d in MOD_DIST.values()),
    }
    for d, want in want_diff.items():
        if diff_counts.get(d, 0) != want:
            errors.append(f"difficulty {d}: expected {want}, got {diff_counts.get(d, 0)}")

    if len(items) != 500:
        errors.append(f"total items: expected 500, got {len(items)}")
    return errors
