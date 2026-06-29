#!/usr/bin/env python3
"""Validate outputs from run_literature_workflow.py."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_SYNTHESES = {
    "direction_a_synthesis.md",
    "direction_b_synthesis.md",
    "cross_direction_analysis.md",
    "research_gaps.md",
    "improvement_ideas_ranked.md",
}
REQUIRED_SYNTHESIS_REVIEWS = {name.replace(".md", ".json") for name in REQUIRED_SYNTHESES}

SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_.=/+-]{20,}"),
    re.compile(r"api[_-]?key\s*[:=]\s*[A-Za-z0-9_.=/+-]{16,}", re.I),
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8-sig", errors="ignore").splitlines():
        if not line.strip():
            continue
        rows.append(json.loads(line))
    return rows


def latest_reviews(review_dir: Path) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    if not review_dir.exists():
        return latest
    for path in sorted(review_dir.glob("*.jsonl")):
        for row in read_jsonl(path):
            paper_id = str(row.get("paper_id", ""))
            if paper_id:
                latest[paper_id] = row.get("review", {})
    return latest


def review_passed(review: dict[str, Any]) -> bool:
    if review.get("pass") is True:
        return True
    final = review.get("final")
    return isinstance(final, dict) and final.get("pass") is True


def note_structure_errors(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    errors: list[str] = []
    for index in range(1, 10):
        if not re.search(rf"^##\s+{index}\.", text, flags=re.M):
            errors.append(f"missing section {index}")
    section_9 = re.search(r"^##\s+9\.", text, flags=re.M)
    if section_9:
        tail = text[section_9.end() :].strip()
        if len(tail) < 250:
            errors.append("section 9 too short or likely truncated")
    return errors


def scan_secret_leaks(out_dir: Path) -> list[str]:
    leaks = []
    for path in out_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".jsonl", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                leaks.append(str(path.relative_to(out_dir)))
                break
    return leaks


def validate(out_dir: Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if not out_dir.exists():
        return False, [f"Output directory not found: {out_dir}"]

    manifest_path = out_dir / "workflow_manifest.json"
    if not manifest_path.exists():
        errors.append("workflow_manifest.json missing")
        manifest = {}
    else:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))

    notes_a = list((out_dir / "notes" / "direction_a").glob("*.md"))
    notes_b = list((out_dir / "notes" / "direction_b").glob("*.md"))
    expected_a = int(manifest.get("count_a", len(notes_a)))
    expected_b = int(manifest.get("count_b", len(notes_b)))
    if len(notes_a) != expected_a:
        errors.append(f"direction_a note count mismatch: {len(notes_a)} != {expected_a}")
    if len(notes_b) != expected_b:
        errors.append(f"direction_b note count mismatch: {len(notes_b)} != {expected_b}")
    for note_path in notes_a + notes_b:
        structure_errors = note_structure_errors(note_path)
        if structure_errors:
            errors.append(f"note structure invalid: {note_path.relative_to(out_dir)}: {structure_errors}")

    synth_dir = out_dir / "syntheses"
    existing_synth = {path.name for path in synth_dir.glob("*.md")} if synth_dir.exists() else set()
    missing_synth = sorted(REQUIRED_SYNTHESES - existing_synth)
    if missing_synth:
        errors.append(f"missing synthesis files: {missing_synth}")
    for name in REQUIRED_SYNTHESES & existing_synth:
        text = (synth_dir / name).read_text(encoding="utf-8", errors="ignore")
        if len(text) < 1200:
            errors.append(f"synthesis file too short: {name}")

    synth_review_dir = out_dir / "synthesis_reviews"
    existing_synth_reviews = {path.name for path in synth_review_dir.glob("*.json")} if synth_review_dir.exists() else set()
    missing_synth_reviews = sorted(REQUIRED_SYNTHESIS_REVIEWS - existing_synth_reviews)
    if missing_synth_reviews:
        errors.append(f"missing synthesis review files: {missing_synth_reviews}")
    for name in REQUIRED_SYNTHESIS_REVIEWS & existing_synth_reviews:
        review = json.loads((synth_review_dir / name).read_text(encoding="utf-8-sig"))
        if not review_passed(review):
            errors.append(f"synthesis review failed: {name}")

    reviews = latest_reviews(out_dir / "reviews")
    expected_ids = {path.stem for path in notes_a + notes_b}
    missing_reviews = sorted(expected_ids - set(reviews))
    failed_reviews = sorted(pid for pid in expected_ids if not review_passed(reviews.get(pid, {})))
    if missing_reviews:
        errors.append(f"missing final reviews: {missing_reviews[:10]}")
    if failed_reviews:
        errors.append(f"failed final reviews: {failed_reviews[:10]}")

    if (out_dir / "quality_failure_report.md").exists():
        errors.append("quality_failure_report.md exists")
    if not (out_dir / "audit_report.md").exists():
        errors.append("audit_report.md missing")

    leaks = scan_secret_leaks(out_dir)
    if leaks:
        errors.append(f"possible API key leaks: {leaks[:10]}")

    return not errors, errors


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python validate_outputs.py <out-dir>")
        raise SystemExit(2)
    ok, errors = validate(Path(sys.argv[1]))
    if ok:
        print("Workflow outputs are valid.")
        raise SystemExit(0)
    print("Workflow output validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
