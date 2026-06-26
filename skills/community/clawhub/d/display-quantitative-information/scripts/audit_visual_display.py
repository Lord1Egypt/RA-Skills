#!/usr/bin/env python3
"""Audit a structured chart specification for quantitative display risks."""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


TEMPLATE: Dict[str, Any] = {
    "title": "Monthly defect rate by production line",
    "purpose": "Compare defect-rate trends across production lines and identify changes after a process change.",
    "chart_type": "line",
    "data_points": 120,
    "variables": ["month", "line", "defect_rate_per_1000_units"],
    "data_grain": "one row per production line per month",
    "encodings": {"x": "month", "y": "defect_rate_per_1000_units", "color": "line", "size": None, "shape": None, "facet": None, "label": None},
    "axes": {"x_labeled": True, "y_labeled": True, "units_shown": True, "y_zero_baseline": None, "y_scale": "linear", "same_scale_across_panels": True, "axis_break": False, "dual_axis": False},
    "labels": {"direct_labels": True, "legend": False, "source_shown": True, "definitions_shown": True, "annotations": ["process change, 2025-09"]},
    "context": {"denominator_shown": True, "uncertainty_shown": None, "sample_size_shown": None, "comparison_baseline_shown": True, "time_range_justified": True},
    "design": {"grid": "light", "decorations": [], "three_d": False, "background_image": False, "uses_area_for_quantity": False, "uses_volume_for_quantity": False, "color_count": 4, "color_is_only_identifier": False},
    "integrity_measurements": {"data_effect_percent": None, "visual_effect_percent": None},
    "medium": {"destination": "report", "color_required": False, "minimum_text_size_pt": 9},
}


@dataclass
class Finding:
    severity: str
    category: str
    message: str
    recommendation: str


SEVERITY_PENALTY = {"severe": 25, "warning": 10, "info": 3}
SEVERITY_RANK = {"severe": 0, "warning": 1, "info": 2}


def is_true(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() in {"true", "yes", "y", "1"})


def is_false(value: Any) -> bool:
    return value is False or (isinstance(value, str) and value.strip().lower() in {"false", "no", "n", "0"})


def is_unknown(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in {"", "unknown", "n/a", "na", "none"})


def get(spec: Dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = spec
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def add(findings: List[Finding], severity: str, category: str, message: str, recommendation: str) -> None:
    findings.append(Finding(severity, category, message, recommendation))


def norm_chart(spec: Dict[str, Any]) -> str:
    return str(spec.get("chart_type", "")).strip().lower().replace(" ", "_").replace("-", "_")


def load_spec(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        raise SystemExit(f"Error: spec file not found: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Error: invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("Error: chart spec must be a JSON object.")
    return data


def audit(spec: Dict[str, Any]) -> Dict[str, Any]:
    findings: List[Finding] = []
    passed: List[str] = []
    chart = norm_chart(spec)
    axes = spec.get("axes") if isinstance(spec.get("axes"), dict) else {}
    labels = spec.get("labels") if isinstance(spec.get("labels"), dict) else {}
    context = spec.get("context") if isinstance(spec.get("context"), dict) else {}
    design = spec.get("design") if isinstance(spec.get("design"), dict) else {}
    medium = spec.get("medium") if isinstance(spec.get("medium"), dict) else {}

    if not str(spec.get("purpose", "")).strip():
        add(findings, "warning", "purpose", "No analytical purpose is stated.", "State the viewer's comparison or decision before choosing a display form.")
    else:
        passed.append("analytical purpose stated")

    if chart in {"bar", "bar_chart", "column", "column_chart", "stacked_bar", "grouped_bar"}:
        baseline = axes.get("y_zero_baseline")
        if is_false(baseline) and not is_true(axes.get("axis_break")):
            add(findings, "severe", "graphical integrity", "Bars encode magnitude by length but the quantitative axis is not marked as starting at zero.", "Start the quantitative axis at zero, or use a dot/difference plot if deviations are the point.")
        elif is_true(baseline):
            passed.append("bar/column baseline starts at zero")

    if chart in {"pie", "donut", "doughnut"}:
        slices = spec.get("slices") or spec.get("categories") or spec.get("data_points")
        try:
            if slices is not None and int(slices) > 5:
                add(findings, "warning", "comparison", "The part-to-whole chart appears to have many slices.", "Use a sorted bar, table, or grouped categories when ranking or exact comparison matters.")
        except (TypeError, ValueError):
            pass

    if chart in {"choropleth", "map", "symbol_map"} and is_false(context.get("denominator_shown")):
        add(findings, "warning", "denominator", "The map lacks a visible denominator or exposure basis.", "Use rates or normalized values when raw counts mostly reflect population, area, tests, stores, or exposure.")

    if is_true(axes.get("axis_break")):
        add(findings, "warning", "scale", "The spec uses an axis break.", "Use an unbroken scale when possible; otherwise label the break prominently and explain why it is needed.")
    if is_true(axes.get("dual_axis")):
        add(findings, "warning", "scale", "The spec uses dual axes.", "Check whether the apparent relationship depends on arbitrary scaling; consider indexed series, small multiples, or a scatterplot.")
    if is_false(axes.get("same_scale_across_panels")):
        add(findings, "warning", "comparison", "Comparable panels are not marked as using the same scale.", "Use common scales when cross-panel magnitude matters, or label independent scaling clearly.")

    if is_false(axes.get("x_labeled")):
        add(findings, "warning", "labeling", "The x-axis is not labeled.", "Add an x-axis label or direct labels that make the horizontal variable unambiguous.")
    if is_false(axes.get("y_labeled")):
        add(findings, "warning", "labeling", "The y-axis is not labeled.", "Add a y-axis label with units.")
    if is_false(axes.get("units_shown")):
        add(findings, "warning", "labeling", "Units are not visible.", "Show units in axis labels, legends, annotations, or caption.")
    elif is_true(axes.get("units_shown")):
        passed.append("units shown")

    if is_false(labels.get("source_shown")):
        add(findings, "warning", "context", "The data source is not shown.", "Add a concise source note for decision, publication, or external-facing use.")
    if is_false(labels.get("definitions_shown")):
        add(findings, "info", "context", "Definitions are not shown.", "Define abbreviations, derived rates, filters, or inclusion rules when readers may not know them.")

    uncertainty = context.get("uncertainty_shown")
    if is_false(uncertainty):
        add(findings, "warning", "uncertainty", "Uncertainty is hidden or marked absent.", "If these are estimates, forecasts, samples, simulations, or measurements, show intervals, bands, sample sizes, or caveats.")
    elif is_unknown(uncertainty):
        add(findings, "info", "uncertainty", "Uncertainty treatment is unspecified.", "If values are estimates, forecasts, samples, simulations, or measurements, state or show uncertainty.")
    else:
        passed.append("uncertainty treatment specified")

    if is_false(context.get("sample_size_shown")):
        add(findings, "info", "sample size", "Sample size is not shown.", "Show sample size when it affects reliability or comparison.")
    if is_false(context.get("time_range_justified")):
        add(findings, "warning", "context", "The time range is not justified.", "Include enough history or context for the claim, or state why the selected window is appropriate.")

    if is_true(design.get("three_d")):
        add(findings, "severe", "chartjunk", "The design uses 3D or perspective effects.", "Remove 3D unless the data are truly spatial and perspective is necessary.")
    if is_true(design.get("background_image")):
        add(findings, "warning", "chartjunk", "The chart uses a background image.", "Remove background imagery unless it is part of the data context, such as a map or instrument image.")
    decorations = design.get("decorations") or []
    if isinstance(decorations, str):
        decorations = [decorations]
    if decorations:
        add(findings, "warning", "data-ink", "Decorative elements are listed: " + ", ".join(map(str, decorations)) + ".", "Remove decorations unless each one directly supports interpretation.")
    if is_true(design.get("uses_area_for_quantity")):
        add(findings, "warning", "encoding", "Area encodes quantity.", "Confirm displayed area is proportional to value; prefer position or length for precise comparison.")
    if is_true(design.get("uses_volume_for_quantity")):
        add(findings, "severe", "encoding", "Volume encodes quantity.", "Avoid volume encodings for non-spatial quantities.")
    if is_true(design.get("color_is_only_identifier")):
        add(findings, "warning", "accessibility", "Color is the only identifier for at least one grouping.", "Add direct labels, symbols, line styles, or panel labels.")
    try:
        if int(design.get("color_count", 0)) > 8:
            add(findings, "info", "color", "The spec uses many colors.", "Check whether facets, grouping, or highlighting would reduce color lookup.")
    except (TypeError, ValueError):
        pass
    try:
        min_pt = float(medium.get("minimum_text_size_pt"))
        if min_pt < 8:
            add(findings, "warning", "accessibility", "Minimum text size is below 8 pt.", "Increase text size or simplify labels for the intended medium.")
    except (TypeError, ValueError):
        pass

    lie_factor: Optional[float] = None
    data_effect = get(spec, "integrity_measurements.data_effect_percent")
    visual_effect = get(spec, "integrity_measurements.visual_effect_percent")
    if data_effect is not None or visual_effect is not None:
        try:
            data_value = float(data_effect)
            visual_value = float(visual_effect)
            if math.isclose(data_value, 0.0):
                add(findings, "warning", "lie factor", "Cannot compute lie factor because the data effect is zero.", "Use absolute differences or another proportionality check.")
            else:
                lie_factor = visual_value / data_value
                if lie_factor < 0:
                    add(findings, "severe", "lie factor", f"Lie factor is {lie_factor:.3g}, implying opposite visual and numerical direction.", "Check the encoding; the visual direction should not reverse the numerical direction.")
                elif not (0.95 <= lie_factor <= 1.05):
                    severity = "severe" if lie_factor < 0.67 or lie_factor > 1.5 else "warning"
                    add(findings, severity, "lie factor", f"Lie factor is {lie_factor:.3g}; visual change is not proportional to data change.", "Make visual dimensions proportional to numerical quantities or use a safer encoding.")
                else:
                    passed.append("lie factor is near 1")
        except (TypeError, ValueError):
            add(findings, "info", "lie factor", "Lie factor inputs are incomplete or not numeric.", "Provide numeric data_effect_percent and visual_effect_percent if visual distortion can be measured.")

    findings.sort(key=lambda f: (SEVERITY_RANK.get(f.severity, 9), f.category, f.message))
    penalty = sum(SEVERITY_PENALTY.get(f.severity, 0) for f in findings)
    score = max(0, 100 - penalty)
    top_priorities = [asdict(f) for f in findings if f.severity in {"severe", "warning"}][:3]
    return {
        "title": spec.get("title"),
        "chart_type": chart or None,
        "score_0_100": score,
        "lie_factor": lie_factor,
        "findings": [asdict(f) for f in findings],
        "top_priorities": top_priorities,
        "passed_checks": passed,
    }


def print_markdown(result: Dict[str, Any]) -> None:
    print(f"Audit score: {result['score_0_100']}/100")
    if result.get("lie_factor") is not None:
        print(f"Lie factor: {result['lie_factor']:.3g}")
    if result.get("top_priorities"):
        print("\nTop priorities:")
        for item in result["top_priorities"]:
            print(f"- {item['severity'].upper()} — {item['category']}: {item['message']} Recommendation: {item['recommendation']}")
    if result.get("findings"):
        print("\nAll findings:")
        for item in result["findings"]:
            print(f"- {item['severity'].upper()} — {item['category']}: {item['message']} Recommendation: {item['recommendation']}")
    else:
        print("\nNo findings from the automated checklist. Human review is still required.")
    if result.get("passed_checks"):
        print("\nPassed checks:")
        for item in result["passed_checks"]:
            print(f"- {item}")


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a JSON chart spec for quantitative-display integrity and clarity.")
    parser.add_argument("--spec", type=Path, help="Path to JSON chart spec.")
    parser.add_argument("--template", action="store_true", help="Print a JSON chart-spec template to stdout.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    if args.template:
        print(json.dumps(TEMPLATE, indent=2))
        return 0
    if not args.spec:
        parser.error("provide --spec chart.json or --template")
    result = audit(load_spec(args.spec))
    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print_markdown(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
