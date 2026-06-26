#!/usr/bin/env python3
"""Council v2 mechanical synthesis."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

VERDICT_POINTS = {
    "approve": 1.0,
    "approve_with_conditions": 0.5,
    "reject": 0.0,
}


def load_reviews(paths: list[str], use_stdin: bool) -> list[dict]:
    if use_stdin:
        data = json.load(sys.stdin)
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        raise ValueError("stdin must be a JSON object or array")

    reviews = []
    for raw_path in paths:
        path = Path(raw_path)
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, list):
            reviews.extend(data)
        else:
            reviews.append(data)
    return reviews


def validate(review: dict) -> dict:
    required = ["reviewer", "model", "verdict", "confidence", "findings", "summary"]
    for field in required:
        if field not in review:
            raise ValueError(f"missing field: {field}")
    if review["verdict"] not in VERDICT_POINTS:
        raise ValueError(f"invalid verdict: {review['verdict']}")
    if not isinstance(review["findings"], list):
        raise ValueError("findings must be a list")
    return review


def strongest_finding(review: dict) -> dict | None:
    priority = {"critical": 3, "warning": 2, "note": 1}
    findings = review.get("findings", [])
    if not findings:
        return None
    return sorted(findings, key=lambda f: priority.get(f.get("severity"), 0), reverse=True)[0]


def derive_conditions(reviews: list[dict]) -> list[str]:
    seen = []
    for review in reviews:
        for finding in review.get("findings", []):
            sev = finding.get("severity")
            rec = finding.get("recommendation", "").strip()
            if sev in {"critical", "warning"} and rec and rec not in seen:
                seen.append(rec)
    return seen


def critical_blocks(reviews: list[dict]) -> list[dict]:
    blocks = []
    for review in reviews:
        for finding in review.get("findings", []):
            if finding.get("severity") == "critical":
                blocks.append({
                    "reviewer": review["reviewer"],
                    "title": finding.get("title", "Untitled critical finding"),
                    "detail": finding.get("detail", ""),
                })
    return blocks


def minority_report(reviews: list[dict], result: str) -> dict | None:
    dissenters = [r for r in reviews if r["verdict"] != result]
    if not dissenters:
        return None
    ranked = sorted(
        dissenters,
        key=lambda r: (VERDICT_POINTS[r["verdict"]], -float(r.get("confidence", 0.0))),
    )
    top = ranked[0]
    return {
        "reviewer": top["reviewer"],
        "verdict": top["verdict"],
        "summary": top["summary"],
    }


def anti_consensus(reviews: list[dict]) -> dict:
    unanimous = len({r["verdict"] for r in reviews}) == 1
    if not unanimous:
        return {
            "triggered": False,
            "note": "Not unanimous.",
            "strongest_counterargument": "",
        }

    counters = []
    for review in reviews:
        finding = strongest_finding(review)
        if finding:
            counters.append(finding.get("detail", ""))
    counter = max(counters, key=len) if counters else "No serious counterargument was surfaced by reviewers. Human operator should still probe correlated bias."
    return {
        "triggered": True,
        "note": "Unanimous decision. Treat agreement as signal, not proof.",
        "strongest_counterargument": counter,
    }


def mechanical_result(reviews: list[dict]) -> tuple[str, dict]:
    blocks = critical_blocks(reviews)
    if blocks:
        total = sum(VERDICT_POINTS[r["verdict"]] for r in reviews)
        return "blocked", {
            "approve_points": total,
            "reviewer_count": len(reviews),
            "thresholds": {"approve": "> 50% with no criticals", "approve_with_conditions": "mixed or conditional majority", "reject": "conservative default on unresolved split", "blocked": "any critical finding"},
        }

    total = sum(VERDICT_POINTS[r["verdict"]] for r in reviews)
    count = len(reviews)
    ratio = total / count if count else 0.0
    verdict_counts = Counter(r["verdict"] for r in reviews)

    if ratio > 0.75 and verdict_counts["reject"] == 0:
        result = "approve"
    elif ratio >= 0.5:
        result = "approve_with_conditions"
    else:
        result = "reject"

    if verdict_counts["approve"] == verdict_counts["reject"] and verdict_counts["approve"] > 0:
        result = "approve_with_conditions" if verdict_counts["approve_with_conditions"] else "reject"

    return result, {
        "approve_points": total,
        "reviewer_count": count,
        "thresholds": {"approve": "> 0.75 average with no rejects", "approve_with_conditions": ">= 0.5 average or conservative tie resolution", "reject": "< 0.5 average or unresolved conservative split", "blocked": "any critical finding"},
    }


def build_output(reviews: list[dict]) -> dict:
    reviews = [validate(r) for r in reviews]
    result, votes = mechanical_result(reviews)
    blocks = critical_blocks(reviews)
    return {
        "verdicts": [
            {
                "reviewer": r["reviewer"],
                "model": r["model"],
                "verdict": r["verdict"],
                "confidence": r["confidence"],
                "summary": r["summary"],
            }
            for r in reviews
        ],
        "mechanical_result": result,
        "vote_count": votes,
        "critical_blocks": blocks,
        "minority_report": minority_report(reviews, result),
        "anti_consensus_check": anti_consensus(reviews),
        "conditions": derive_conditions(reviews),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Council v2 synthesis")
    parser.add_argument("files", nargs="*")
    parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()

    try:
        reviews = load_reviews(args.files, args.stdin)
        output = build_output(reviews)
    except Exception as exc:
        print(json.dumps({"error": str(exc), "generated_at": datetime.now(timezone.utc).isoformat()}))
        return 3

    print(json.dumps(output, indent=2))
    result = output["mechanical_result"]
    if result in {"reject", "blocked"}:
        return 1
    if result == "approve_with_conditions":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
