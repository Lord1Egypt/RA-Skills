#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any


def _normalized(text: str) -> str:
    return " ".join(text.lower().split())


def _keyword_hits(answer: str, keywords: list[str]) -> list[str]:
    normalized_answer = _normalized(answer)
    cleaned = [kw.strip() for kw in keywords if kw and kw.strip()]
    return [kw for kw in cleaned if _normalized(kw) in normalized_answer]


def _checkpoint_score(answer: str, checkpoints: list[dict[str, Any]]) -> dict[str, Any]:
    if not checkpoints:
        return {
            "enabled": False,
            "score": 0.0,
            "earned_weight": 0.0,
            "total_weight": 0.0,
            "passed_count": 0,
            "total_count": 0,
            "details": [],
        }

    total_weight = 0.0
    earned_weight = 0.0
    passed_count = 0
    details: list[dict[str, Any]] = []

    for idx, raw in enumerate(checkpoints, start=1):
        if not isinstance(raw, dict):
            continue
        name = str(raw.get("name", f"checkpoint_{idx}")).strip() or f"checkpoint_{idx}"
        keywords = raw.get("keywords", [])
        if not isinstance(keywords, list):
            keywords = [str(keywords)]
        keywords = [str(k).strip() for k in keywords if str(k).strip()]
        if not keywords:
            continue

        mode = str(raw.get("mode", "all")).strip().lower()
        if mode not in {"all", "any"}:
            mode = "all"
        try:
            weight = float(raw.get("weight", 1.0))
        except (TypeError, ValueError):
            weight = 1.0
        weight = max(0.0, weight)

        hits = _keyword_hits(answer, keywords)
        passed = len(hits) > 0 if mode == "any" else len(hits) == len(keywords)

        total_weight += weight
        if passed:
            earned_weight += weight
            passed_count += 1

        details.append(
            {
                "name": name,
                "mode": mode,
                "weight": weight,
                "passed": passed,
                "hits": hits,
                "keywords": keywords,
            }
        )

    score = earned_weight / total_weight if total_weight > 0 else 0.0
    return {
        "enabled": bool(details),
        "score": score,
        "earned_weight": earned_weight,
        "total_weight": total_weight,
        "passed_count": passed_count,
        "total_count": len(details),
        "details": details,
    }


def _structure_score(answer: str) -> dict[str, Any]:
    text = answer.strip()
    if not text:
        return {
            "score": 0.0,
            "list_signal": 0.0,
            "step_signal": 0.0,
            "risk_signal": 0.0,
        }

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    bullet_re = re.compile(r"^[-*•]\s+")
    number_re = re.compile(r"^\d{1,2}[).、.]\s*")
    bullet_count = sum(1 for line in lines if bullet_re.match(line) or number_re.match(line))
    list_signal = 1.0 if bullet_count >= 2 else 0.0

    normalized = _normalized(text)
    step_markers = (
        "week",
        "day",
        "step",
        "phase",
        "第1",
        "第一",
        "步骤",
        "第1周",
        "第2周",
        "本周",
        "下周",
    )
    risk_markers = (
        "risk",
        "caution",
        "avoid",
        "warning",
        "注意",
        "风险",
        "禁忌",
        "避免",
    )
    step_signal = 1.0 if any(marker in normalized for marker in step_markers) else 0.0
    risk_signal = 1.0 if any(marker in normalized for marker in risk_markers) else 0.0

    score = (list_signal + step_signal + risk_signal) / 3
    return {
        "score": score,
        "list_signal": list_signal,
        "step_signal": step_signal,
        "risk_signal": risk_signal,
    }


def _safe_ratio(hit_count: int, total_count: int, default: float) -> float:
    if total_count <= 0:
        return default
    return hit_count / total_count


def _resolve_weights(case: dict[str, Any]) -> tuple[float, float, float]:
    raw = case.get("weights", {})
    if not isinstance(raw, dict):
        raw = {}

    def _read(name: str, fallback: float) -> float:
        try:
            value = float(raw.get(name, fallback))
        except (TypeError, ValueError):
            value = fallback
        return max(0.0, value)

    content = _read("content", 0.65)
    safety = _read("safety", 0.25)
    structure = _read("structure", 0.10)
    total = content + safety + structure
    if total <= 0:
        return 0.65, 0.25, 0.10
    return content / total, safety / total, structure / total


def _score_answer(case: dict[str, Any], answer: str) -> dict[str, Any]:
    expected_keywords = case.get("expected_keywords", [])
    forbidden_keywords = case.get("forbidden_keywords", [])
    checkpoints = case.get("checkpoints", [])
    if not isinstance(expected_keywords, list):
        expected_keywords = [str(expected_keywords)]
    if not isinstance(forbidden_keywords, list):
        forbidden_keywords = [str(forbidden_keywords)]
    if not isinstance(checkpoints, list):
        checkpoints = []

    expected_hits = _keyword_hits(answer, [str(k) for k in expected_keywords])
    forbidden_hits = _keyword_hits(answer, [str(k) for k in forbidden_keywords])
    expected_coverage = _safe_ratio(len(expected_hits), len(expected_keywords), 1.0)
    forbidden_ratio = _safe_ratio(len(forbidden_hits), len(forbidden_keywords), 0.0)
    safety_score = max(0.0, 1.0 - forbidden_ratio)

    checkpoint = _checkpoint_score(answer, checkpoints)
    content_score = checkpoint["score"] if checkpoint["enabled"] else expected_coverage

    structure = _structure_score(answer)
    w_content, w_safety, w_structure = _resolve_weights(case)
    overall = (
        content_score * w_content
        + safety_score * w_safety
        + structure["score"] * w_structure
    )

    return {
        "overall": overall,
        "content_score": content_score,
        "safety_score": safety_score,
        "structure_score": structure["score"],
        "expected_coverage": expected_coverage,
        "expected_hits": expected_hits,
        "forbidden_hits": forbidden_hits,
        "checkpoint_enabled": checkpoint["enabled"],
        "checkpoint_passed_count": checkpoint["passed_count"],
        "checkpoint_total_count": checkpoint["total_count"],
        "checkpoint_earned_weight": checkpoint["earned_weight"],
        "checkpoint_total_weight": checkpoint["total_weight"],
        "checkpoint_details": checkpoint["details"],
    }


def _evaluate_cases(cases: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        baseline = _score_answer(case, str(case.get("baseline_answer", "")))
        engram = _score_answer(case, str(case.get("engram_answer", "")))
        rows.append(
            {
                "id": str(case.get("id", "")),
                "domain": str(case.get("domain", "")),
                "baseline_overall": baseline["overall"],
                "engram_overall": engram["overall"],
                "delta": engram["overall"] - baseline["overall"],
                "baseline_content_score": baseline["content_score"],
                "engram_content_score": engram["content_score"],
                "baseline_safety_score": baseline["safety_score"],
                "engram_safety_score": engram["safety_score"],
                "baseline_structure_score": baseline["structure_score"],
                "engram_structure_score": engram["structure_score"],
                "baseline_expected_hits": ", ".join(baseline["expected_hits"]),
                "engram_expected_hits": ", ".join(engram["expected_hits"]),
                "baseline_forbidden_hits": ", ".join(baseline["forbidden_hits"]),
                "engram_forbidden_hits": ", ".join(engram["forbidden_hits"]),
                "baseline_checkpoints": (
                    f"{baseline['checkpoint_passed_count']}/{baseline['checkpoint_total_count']}"
                    if baseline["checkpoint_enabled"] else "-"
                ),
                "engram_checkpoints": (
                    f"{engram['checkpoint_passed_count']}/{engram['checkpoint_total_count']}"
                    if engram["checkpoint_enabled"] else "-"
                ),
            }
        )

    baseline_avg = (
        sum(row["baseline_overall"] for row in rows) / len(rows) if rows else 0.0
    )
    engram_avg = (
        sum(row["engram_overall"] for row in rows) / len(rows) if rows else 0.0
    )
    return {
        "rows": rows,
        "baseline_avg": baseline_avg,
        "engram_avg": engram_avg,
        "avg_delta": engram_avg - baseline_avg,
    }


def _render_report(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("Case Study Report")
    lines.append("=" * 68)
    lines.append(
        "Average overall | baseline={:.3f} engram={:.3f} delta={:+.3f}".format(
            report["baseline_avg"],
            report["engram_avg"],
            report["avg_delta"],
        )
    )
    lines.append(
        "Dimensions: content (checkpoints or expected keywords) + safety + structure"
    )
    lines.append("")
    for row in report["rows"]:
        lines.append(
            "[{id}] {domain} | overall baseline={baseline_overall:.3f} engram={engram_overall:.3f} delta={delta:+.3f}".format(
                **row
            )
        )
        lines.append(
            "  content  | baseline={baseline_content_score:.3f} engram={engram_content_score:.3f}".format(
                **row
            )
        )
        lines.append(
            "  safety   | baseline={baseline_safety_score:.3f} engram={engram_safety_score:.3f}".format(
                **row
            )
        )
        lines.append(
            "  structure| baseline={baseline_structure_score:.3f} engram={engram_structure_score:.3f}".format(
                **row
            )
        )
        lines.append(
            "  checkpoints | baseline: {baseline_checkpoints} | engram: {engram_checkpoints}".format(
                **row
            )
        )
        lines.append(
            "  expected hits | baseline: {baseline_expected_hits} | engram: {engram_expected_hits}".format(
                **row
            )
        )
        lines.append(
            "  forbidden hits| baseline: {baseline_forbidden_hits} | engram: {engram_forbidden_hits}".format(
                **row
            )
        )
    return "\n".join(lines)


def _write_csv(report: dict[str, Any], path: Path) -> None:
    fields = [
        "id",
        "domain",
        "baseline_overall",
        "engram_overall",
        "delta",
        "baseline_content_score",
        "engram_content_score",
        "baseline_safety_score",
        "engram_safety_score",
        "baseline_structure_score",
        "engram_structure_score",
        "baseline_checkpoints",
        "engram_checkpoints",
        "baseline_expected_hits",
        "engram_expected_hits",
        "baseline_forbidden_hits",
        "engram_forbidden_hits",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(report["rows"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Score baseline vs Engram case study answers")
    parser.add_argument("--input", required=True, help="Path to case study JSON file")
    parser.add_argument("--csv", help="Optional CSV output path")
    args = parser.parse_args()

    input_path = Path(args.input)
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise SystemExit("Input JSON must be a list of case objects.")

    cases = [item for item in raw if isinstance(item, dict)]
    report = _evaluate_cases(cases)
    print(_render_report(report))

    if args.csv:
        csv_path = Path(args.csv)
        _write_csv(report, csv_path)
        print(f"\nCSV written to: {csv_path}")


if __name__ == "__main__":
    main()
