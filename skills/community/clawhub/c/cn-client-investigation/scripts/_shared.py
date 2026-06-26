"""Shared helpers for cn-client-investigation scanners.

Keep this module small and import-light. Scripts in this folder (e.g.
provenance_verify.py, style_scan.py) import from here to avoid
duplicating commonly-used scanning primitives.
"""
from __future__ import annotations

import collections
import re


_METRIC_CONTEXT_CHARS = 8


def _metric_key(line: str, start: int) -> str:
    """Extract a short CJK-only pre-context window used to disambiguate
    values with the same rounded int + unit but belonging to different
    metrics (e.g. ``毛利率 19.4%`` vs ``净利润同比 -18.97%``).

    Keep only Chinese chars from the preceding ``_METRIC_CONTEXT_CHARS``
    characters; whitespace / punctuation / non-CJK chars usually carry no
    metric-identifier signal and would make the key over-strict.
    """
    window = line[max(0, start - _METRIC_CONTEXT_CHARS):start]
    return "".join(ch for ch in window if "\u4e00" <= ch <= "\u9fff")


def _decimal_places(num_str: str) -> int:
    """Return count of digits after decimal point in ``num_str``.

    Used to compute the "coarser precision" of a value pair — values
    whose diff is within half the coarser precision's least-significant
    digit are treated as precision variants of each other.
    """
    if "." not in num_str:
        return 0
    return len(num_str.rsplit(".", 1)[1])


def _is_precision_variant(a_str: str, b_str: str, a: float, b: float) -> bool:
    """Do ``a`` and ``b`` look like precision variants of each other?

    A value pair qualifies as a precision variant when the absolute
    difference is ≤ half of the coarser-precision least-significant
    digit. E.g.:
    - ``1.34`` (da=2) vs ``1.3`` (db=1) → min_prec=1 → tolerance=0.05,
      diff=0.04 ≤ 0.05 → variant. Correct for EPS drift.
    - ``14.10`` vs ``14.29`` → min_prec=2 → tolerance=0.005,
      diff=0.19 > 0.005 → NOT variant. Correct for cross-year same-int
      series that shouldn't be flagged.
    """
    min_prec = min(_decimal_places(a_str), _decimal_places(b_str))
    tolerance = 0.5 * (10 ** -min_prec)
    return abs(a - b) <= tolerance


def find_precision_drift(
    text: str, hard_number_re: re.Pattern[str]
) -> list[str]:
    """Detect same-metric multi-precision writes across the doc.

    Group hard numbers by ``(pre-context CJK key, round(value), unit)``
    — that's two layers of disambiguation:

    1. **Pre-context CJK key** prevents cross-metric collisions where
       different metrics happen to round to the same integer + unit
       (e.g. ``毛利率 19.4%`` vs ``净利润同比 -18.97%``).
    2. **Precision-tolerance post-filter**: within each group, emit a
       drift warning only if at least one value pair is within the
       precision tolerance of each other. Prevents cross-year same-int
       series (e.g. ``营收同比 2023: 8.66%`` vs ``营收同比 2024: 9.47%``)
       from being flagged — they round to the same int and share the
       metric key but are factually different period readings, not
       precision variants.

    Real drift pattern that still fires: ``EPS 1.34 / 1.340 / 1.3 元/股``
    across the same doc — same metric, values within precision tolerance.
    """
    groups: dict[tuple[str, int, str], list[tuple[str, float]]] = (
        collections.defaultdict(list)
    )
    for line in text.splitlines():
        for m in hard_number_re.finditer(line):
            num_str, unit = m.group(1), m.group(2)
            try:
                n = float(num_str.replace(",", ""))
            except ValueError:
                continue
            key = (_metric_key(line, m.start()), int(round(n)), unit)
            groups[key].append((f"{num_str}{unit}", n))

    warnings: list[str] = []
    for (metric, int_part, unit), entries in groups.items():
        distinct_forms = {form for form, _ in entries}
        if len(distinct_forms) < 2:
            continue
        # Only warn when at least one pair is within precision tolerance.
        has_drift = False
        for i, (form_a, val_a) in enumerate(entries):
            for form_b, val_b in entries[i + 1:]:
                if form_a == form_b:
                    continue
                # Extract raw numeric strings (strip unit suffix) for
                # decimal-place accounting.
                a_num = form_a.removesuffix(unit).strip().replace(",", "")
                b_num = form_b.removesuffix(unit).strip().replace(",", "")
                if _is_precision_variant(a_num, b_num, val_a, val_b):
                    has_drift = True
                    break
            if has_drift:
                break
        if not has_drift:
            continue
        label = f"{metric} {int_part}{unit}" if metric else f"{int_part}{unit}"
        warnings.append(
            f"precision drift near {label}: {', '.join(sorted(distinct_forms))}"
        )
    return warnings
