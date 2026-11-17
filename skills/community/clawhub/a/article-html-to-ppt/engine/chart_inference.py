"""P10: chart auto-inference — when the model doesn't write chart/diagram_ir,
the engine infers one from the slide's blocks and relations.

Rules (deterministic, no LLM):
  - metric blocks ≥ 2 with numeric values → auto chart
  - relation=comparison → combo (column + line overlay)
  - relation=sequence → line
  - default → column
  - table block with source data → additional series from table rows

The inferred chart payload is injected into the slide dict before
decide_deck, so the existing chart_* archetype dispatch path picks it up
without any change to policy.py or layout.py.
"""

from __future__ import annotations

import re
from typing import Any

from .source_doc import parse_anchor, extract_numbers

# Regex for parsing metric values: keep only sign, digits, and decimal point.
# Strips currency symbols, %, Chinese unit suffixes (亿/万/千/元/角/分), commas.
_VALUE_CLEAN = re.compile(r"[^0-9.+\-]")


def _parse_metric_value(value_str: str) -> float | None:
    """Parse a metric value string into a float for chart data.

    Handles: "+36%", "36%", "$49", "1.2亿", "720万元", "2000", "1,200", "-5%", etc.
    Returns None if the value is not parseable as a number.
    """
    if value_str is None:
        return None
    if isinstance(value_str, (int, float)):
        return float(value_str)
    if not isinstance(value_str, str) or not value_str.strip():
        return None
    # strip everything except sign, digits, and decimal point
    s = _VALUE_CLEAN.sub("", value_str.strip())
    if not s or s in ("+", "-", "."):
        return None
    # handle leading sign
    sign = 1.0
    if s.startswith("+"):
        s = s[1:]
    elif s.startswith("-"):
        sign = -1.0
        s = s[1:]
    try:
        return sign * float(s)
    except ValueError:
        return None


def _infer_chart_type(slide: dict) -> str:
    """Determine chart type from slide relations."""
    relations = slide.get("relations", []) or []
    rel_types = {r.get("relation") for r in relations if isinstance(r, dict)}
    if "comparison" in rel_types:
        return "combo"
    if "sequence" in rel_types or "causal" in rel_types:
        return "line"
    return "column"


def _infer_chart_data(metrics: list[dict]) -> dict | None:
    """Build chart data from metric blocks."""
    labels = []
    values = []
    for m in metrics:
        label = m.get("label", "")
        value_str = m.get("value", "")
        parsed = _parse_metric_value(value_str)
        if parsed is None:
            # If a single metric can't be parsed, skip the whole chart —
            # mixed parseable/unparseable values produce misleading charts.
            return None
        labels.append(label)
        values.append(parsed)
    if len(labels) < 2:
        return None
    return {
        "categories": labels,
        "series": [{"name": labels[0] if len(labels) == 1 else "", "values": values}],
    }


def _extract_table_series(slide: dict, docs: dict) -> list[dict] | None:
    """Extract numeric series from a table block's source data.

    The table block carries a source_ref pointing to a parsed table element
    in the source doc. If the table has numeric columns, they become chart
    series (each column = one series, first column = categories).
    """
    table_blocks = [b for b in slide.get("blocks", []) if b.get("role") == "table"]
    if not table_blocks:
        return None
    ref = table_blocks[0].get("source_ref", {})
    source_id = ref.get("source_id", "")
    loc = ref.get("loc", "")
    doc = docs.get(source_id)
    if not doc or not loc:
        return None
    parsed = parse_anchor(loc)
    if not parsed:
        return None
    element = doc.get(f"{parsed[0]}_{parsed[1]}")
    if not element or not element.rows:
        return None
    rows = element.rows  # list of list[str]
    if len(rows) < 2:
        return None
    # Assume first row is header, columns 1+ are numeric series
    headers = rows[0]
    series_dict: dict[str, list[float]] = {}
    for col_idx in range(1, len(headers)):
        col_name = headers[col_idx]
        values = []
        for row in rows[1:]:
            if col_idx < len(row):
                nums = extract_numbers(row[col_idx])
                if nums:
                    # take the first number found in the cell
                    v = next(iter(nums)).rstrip("%")
                    try:
                        values.append(float(v))
                    except ValueError:
                        values.append(0.0)
                else:
                    values.append(0.0)
        if any(v != 0.0 for v in values):
            series_dict[col_name] = values
    if not series_dict:
        return None
    return [{"name": name, "values": vals} for name, vals in series_dict.items()]


def infer_charts(ir: dict, docs: dict) -> dict:
    """Inject auto-generated chart payloads into slides that need them.

    Only fires when the slide does NOT already have an explicit chart or
    diagram_ir payload (model-written payloads take priority). The engine
    never overwrites what the model deliberately provided.

    Returns the ir dict (mutated in-place for convenience).
    """
    for slide in ir.get("slides", []):
        if slide.get("chart") or slide.get("diagram_ir"):
            continue  # model already provided one; never override
        if slide.get("refine"):
            # P12-refine: explicit page-level composition intent wins over
            # chart inference — the user asked for this composition, not a
            # chart. (An explicit chart inside a refine slot still works.)
            continue

        metrics = [b for b in slide.get("blocks", []) if b.get("role") == "metric"]
        table_series = _extract_table_series(slide, docs)

        if len(metrics) >= 2:
            chart_data = _infer_chart_data(metrics)
            if chart_data is None:
                continue
            chart_type = _infer_chart_type(slide)
            # If a table is also present, use its numeric series instead of
            # the single metric-derived series for a richer chart.
            if table_series and len(table_series) >= 1:
                chart_data["series"] = table_series
                # Keep categories from metrics (they are the human-readable labels)
            slide["chart"] = {
                "type": chart_type,
                "data": chart_data,
                # provenance: chart was inferred, not model-written
                "inferred": True,
            }
        elif table_series and len(table_series) >= 1:
            # Table-only: use the table's first column as categories, remaining
            # columns as series.
            ref = (slide.get("blocks", [])[0].get("source_ref", {})
                   if slide.get("blocks") else {})
            loc = ref.get("loc", "")
            parsed = parse_anchor(loc) if loc else None
            categories = []
            if parsed:
                element = docs.get(ref.get("source_id", ""))
                if element:
                    el = element.get(f"{parsed[0]}_{parsed[1]}")
                    if el and el.rows:
                        categories = [row[0] for row in el.rows[1:]]
            slide["chart"] = {
                "type": "column",
                "data": {
                    "categories": categories or [f"Row {i+1}" for i in range(len(table_series[0]["values"]))],
                    "series": table_series,
                },
                "inferred": True,
            }
    return ir