#!/usr/bin/env python3
"""Suggest display families from a CSV's structure and a stated goal."""

from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DATE_RE = re.compile(r"^(\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{1,2})$")
RATE_RE = re.compile(r"(rate|percent|percentage|pct|share|ratio|per_|per100|per_100|index|score|yield|density)", re.I)
COUNT_RE = re.compile(r"(count|n$|num|number|total|units|cases|incidents|defects|claims|clicks|population)", re.I)
GEO_RE = re.compile(r"(country|state|county|city|region|latitude|longitude|lat|lon|lng|postcode|zip)", re.I)
TIME_NAME_RE = re.compile(r"(date|time|year|month|week|day|quarter)", re.I)


def to_float(v: str) -> Optional[float]:
    try:
        return float(v.replace(",", ""))
    except (AttributeError, ValueError):
        return None


def infer_value(name: str, values: List[str]) -> str:
    sample = [str(v).strip() for v in values if v is not None and str(v).strip() != ""]
    if not sample:
        return "empty"
    if TIME_NAME_RE.search(name):
        date_hits = sum(1 for v in sample if DATE_RE.match(v))
        if date_hits / len(sample) >= 0.4:
            return "date_or_time"
    numeric = sum(1 for v in sample if to_float(v) is not None)
    dates = sum(1 for v in sample if DATE_RE.match(v))
    if dates / len(sample) >= 0.6:
        return "date_or_time"
    if numeric / len(sample) >= 0.85:
        return "quantitative"
    unique_ratio = len(set(sample)) / max(1, len(sample))
    if unique_ratio < 0.5 or len(set(sample)) <= 30:
        return "categorical"
    return "text_or_id"


def numeric_stats(values: List[str]) -> Dict[str, Optional[float]]:
    nums = [x for x in (to_float(str(v).strip()) for v in values) if x is not None]
    if not nums:
        return {"min": None, "max": None, "mean": None}
    return {"min": min(nums), "max": max(nums), "mean": statistics.fmean(nums)}


def inspect_csv(path: Path, max_rows: int) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                raise SystemExit("Error: CSV has no header row.")
            rows = []
            for idx, row in enumerate(reader):
                if idx >= max_rows:
                    break
                rows.append(row)
    except FileNotFoundError:
        raise SystemExit(f"Error: CSV file not found: {path}")
    except csv.Error as exc:
        raise SystemExit(f"Error: could not parse CSV: {exc}")

    columns = []
    for name in reader.fieldnames or []:
        vals = [row.get(name, "") for row in rows]
        kind = infer_value(name, vals)
        missing = sum(1 for v in vals if v is None or str(v).strip() == "")
        nonmissing = [str(v).strip() for v in vals if v is not None and str(v).strip() != ""]
        unique = len(set(nonmissing))
        role = ""
        if kind == "quantitative":
            if RATE_RE.search(name):
                role = "rate_or_normalized_measure"
            elif COUNT_RE.search(name):
                role = "count_or_exposure"
            else:
                role = "measure"
        elif kind == "categorical" and GEO_RE.search(name):
            role = "geographic_category"
        elif kind == "date_or_time":
            role = "time"
        columns.append({"name": name, "type": kind, "role": role, "missing_in_sample": missing, "unique_in_sample": unique, "stats": numeric_stats(vals) if kind == "quantitative" else None})
    return {"path": str(path), "sample_rows": len(rows), "columns": columns}


def choose_primary_quant(cols: List[Dict[str, Any]]) -> Optional[str]:
    q = [c for c in cols if c["type"] == "quantitative"]
    if not q:
        return None
    for c in q:
        if c.get("role") == "rate_or_normalized_measure":
            return c["name"]
    non_exposure = [c for c in q if c.get("role") != "count_or_exposure"]
    if non_exposure:
        return non_exposure[0]["name"]
    return q[0]["name"]


def recommendations(profile: Dict[str, Any], goal: str, question: str = "") -> List[Dict[str, Any]]:
    cols = profile["columns"]
    q = [c["name"] for c in cols if c["type"] == "quantitative"]
    cat = [c["name"] for c in cols if c["type"] == "categorical"]
    geo = [c["name"] for c in cols if c.get("role") == "geographic_category"]
    time = [c["name"] for c in cols if c["type"] == "date_or_time"]
    primary = choose_primary_quant(cols)
    recs: List[Dict[str, Any]] = []

    def add(display: str, why: str, caution: str = "", checks: Optional[List[str]] = None, priority: str = "candidate") -> None:
        recs.append({"display": display, "priority": priority, "why": why, "caution": caution, "integrity_checks": checks or []})

    normalized_available = any(c.get("role") == "rate_or_normalized_measure" for c in cols)
    count_available = any(c.get("role") == "count_or_exposure" for c in cols)

    if goal == "auto":
        if time and primary:
            display = "time-series line chart"
            if cat:
                display += " with direct labels or small multiples"
            add(display, f"{time[0]} supplies order and {primary} is the likely outcome measure.", "Use a common scale across panels if cross-group magnitude matters.", ["label time window", "show units", "annotate relevant events"], "strong")
        if cat and primary:
            add("sorted dot plot or zero-baseline bar chart", f"{cat[0]} can group {primary} for comparison.", "Use bars only when absolute magnitude from zero is the task; dots work well for compact ranked comparisons or intervals.", ["sort deliberately", "show units", "check zero baseline if bars"], "strong" if not time else "candidate")
        if len(q) >= 2:
            x, y = q[0], primary if primary and primary != q[0] else q[1]
            add("scatterplot", f"{x} and {y} support relationship, outlier, and leverage checks.", "Use transparency or density if there are many rows; label transformations.", ["check overplotting", "show fit only if model is meaningful"], "candidate")
        if primary:
            add("distribution display", f"{primary} can be inspected for spread, skew, and outliers.", "Avoid summarizing by mean alone if distribution affects the decision.", ["show sample size", "consider raw points"], "candidate")
        if geo and primary:
            add("map plus companion ranking", f"{geo[0]} suggests geography may matter for {primary}.", "Normalize by exposure when raw counts mostly reflect population or opportunity.", ["check denominator", "use a companion table/dot plot"], "candidate")
        if count_available and not normalized_available:
            add("rate or normalized measure before plotting", "The CSV appears to include raw counts or exposure fields but no obvious rate/share column.", "Create an appropriate denominator before making population- or opportunity-sensitive comparisons.", ["identify denominator", "label rate definition"], "caution")
        if not recs:
            add("table", "The sampled columns do not clearly support a quantitative chart.", "Clarify the analytical question or provide typed columns.", ["verify headers", "identify units"], "fallback")
    elif goal == "lookup":
        add("table or text-table", "Exact values are the main task.", "Sort and round deliberately; add inline bars only if pattern comparison matters.", ["align numbers", "show units"], "strong")
    elif goal == "trend":
        add("time-series line chart", "Ordered time is needed for trend, seasonality, or event effects.", "If no time column exists, identify or create one before plotting.", ["label time window", "annotate events", "use common scales for groups"], "strong")
    elif goal == "comparison":
        add("sorted bar or dot plot", "Magnitude comparison across categories is central.", "Bars need zero baselines; dots work well for many categories or intervals.", ["sort categories", "show units", "check baseline"], "strong")
    elif goal == "relationship":
        add("scatterplot", "Relationships need at least two quantitative variables.", "Label transformations and use density methods for overplotting.", ["check outliers", "avoid unjustified causal language"], "strong")
    elif goal == "distribution":
        add("histogram, dot plot, box plot, or violin", "Distribution tasks need spread, tails, and outliers.", "Choose a form the audience can read; show raw points when sample size is modest.", ["show sample size", "choose binning deliberately"], "strong")
    elif goal == "geography":
        add("map plus companion ranking", "Spatial position matters for geographic questions.", "Normalize by exposure when raw counts mostly reflect population or opportunity.", ["check denominator", "state projection/boundaries if relevant"], "strong")
    elif goal == "uncertainty":
        add("interval, band, fan, or distribution display", "Estimates and forecasts need uncertainty visible.", "Label what the interval means.", ["show interval definition", "avoid false precision"], "strong")
    return recs


def print_markdown(profile: Dict[str, Any], recs: List[Dict[str, Any]]) -> None:
    print(f"Rows sampled: {profile['sample_rows']}")
    print("Columns:")
    for col in profile["columns"]:
        extra = f", role={col['role']}" if col.get("role") else ""
        print(f"- {col['name']}: {col['type']}{extra} ({col['unique_in_sample']} unique, {col['missing_in_sample']} missing in sample)")
    print("\nRecommendations:")
    for rec in recs:
        line = f"- [{rec['priority']}] {rec['display']}: {rec['why']}"
        if rec.get("caution"):
            line += f" Caution: {rec['caution']}"
        print(line)
        if rec.get("integrity_checks"):
            print("  Checks: " + "; ".join(rec["integrity_checks"]))


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect a CSV and suggest quantitative display families.")
    parser.add_argument("--csv", type=Path, required=True, help="Input CSV with a header row.")
    parser.add_argument("--goal", choices=("auto", "lookup", "trend", "comparison", "relationship", "distribution", "geography", "uncertainty"), default="auto")
    parser.add_argument("--question", default="", help="Optional user question to include in output metadata.")
    parser.add_argument("--max-rows", type=int, default=500, help="Rows to sample for type inference. Default: 500.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    if args.max_rows <= 0:
        print("Error: --max-rows must be positive.", file=sys.stderr)
        return 2
    profile = inspect_csv(args.csv, args.max_rows)
    result = {"profile": profile, "goal": args.goal, "question": args.question, "recommendations": recommendations(profile, args.goal, args.question)}
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print_markdown(profile, result["recommendations"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
