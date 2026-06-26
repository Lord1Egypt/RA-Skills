#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


MATCH_FIELDS = {"name", "location", "mode", "day", "slot", "weeks", "date", "dates"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check that prepared source entries are covered by the normalized schedule manifest."
    )
    parser.add_argument("manifest", help="Path to schedule manifest JSON")
    parser.add_argument("coverage", help="Path to coverage checklist JSON")
    return parser.parse_args()


def load_json(path: str) -> dict:
    return json.loads(Path(path).expanduser().resolve().read_text(encoding="utf-8"))


def normalize_course(course: dict) -> dict:
    normalized = dict(course)
    mode = normalized.get("mode")
    if mode is None:
        if "date" in normalized or "dates" in normalized:
            mode = "dated"
        elif "day" in normalized and "weeks" in normalized:
            mode = "recurring"
    if mode is not None:
        normalized["mode"] = mode
    if "weeks" in normalized:
        normalized["weeks"] = sorted(normalized["weeks"])
    if "dates" in normalized:
        normalized["dates"] = sorted(normalized["dates"])
    return normalized


def match_course(course: dict, matcher: dict) -> bool:
    for key, value in matcher.items():
        if key not in MATCH_FIELDS:
            raise ValueError(f"Unsupported match field '{key}'")
        candidate = course.get(key)
        if key in {"weeks", "dates"} and candidate is not None:
            candidate = sorted(candidate)
            value = sorted(value)
        if candidate != value:
            return False
    return True


def course_label(course: dict, index: int) -> str:
    parts = [
        course.get("name", f"<course-{index}>"),
        course.get("mode", "<unknown-mode>"),
        course.get("slot", "<unknown-slot>"),
    ]
    if course.get("mode") == "recurring":
        parts.insert(2, course.get("day", "<unknown-day>"))
    return " | ".join(parts)


def print_failures(label: str, lines: list[str]) -> None:
    for line in lines:
        print(f"FAIL [{label}] {line}")


def main() -> None:
    args = parse_args()
    manifest = load_json(args.manifest)
    coverage = load_json(args.coverage)

    courses = [normalize_course(course) for course in manifest.get("courses", [])]
    source_ids = {source["id"] for source in manifest.get("sources", []) if "id" in source}
    entries = coverage.get("source_entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("coverage file must contain a non-empty 'source_entries' list")

    entry_failures: list[str] = []
    provenance_failures: list[str] = []
    source_failures: list[str] = []
    uncovered_courses: list[str] = []
    covered_course_indexes: set[int] = set()

    for idx, entry in enumerate(entries, start=1):
        entry_id = entry.get("id", f"entry-{idx}")
        source_id = entry.get("source_id")
        description = entry.get("description", "")
        matchers = entry.get("matches")
        if not isinstance(matchers, list) or not matchers:
            entry_failures.append(f"{entry_id}: missing non-empty matches list")
            continue
        if source_id is not None and source_id not in source_ids:
            entry_failures.append(f"{entry_id}: unknown source_id '{source_id}'")
            continue
        for matcher_index, matcher in enumerate(matchers, start=1):
            if not isinstance(matcher, dict) or not matcher:
                entry_failures.append(f"{entry_id}: matcher {matcher_index} is empty or invalid")
                continue
            field_matched_indexes = []
            matched_indexes = []
            for course_index, course in enumerate(courses, start=1):
                if not match_course(course, matcher):
                    continue
                field_matched_indexes.append(course_index)
                if source_id is not None and source_id not in course.get("sources", []):
                    continue
                matched_indexes.append(course_index)
            if not matched_indexes:
                source_hint = f", source_id={source_id!r}" if source_id is not None else ""
                matcher_json = json.dumps(matcher, ensure_ascii=False, sort_keys=True)
                if source_id is not None and field_matched_indexes:
                    labels = ", ".join(
                        course_label(courses[course_index - 1], course_index)
                        for course_index in field_matched_indexes
                    )
                    provenance_failures.append(
                        f"{entry_id}: matcher {matcher_index} matched fields but failed source provenance | description={description!r}, source_id={source_id!r} | matcher={matcher_json} | field_matches={labels}"
                    )
                else:
                    entry_failures.append(
                        f"{entry_id}: matcher {matcher_index} not covered | description={description!r}{source_hint} | matcher={matcher_json}"
                    )
                continue
            covered_course_indexes.update(matched_indexes)

    for course in courses:
        course_sources = course.get("sources")
        if course_sources is None:
            source_failures.append(f"course without sources: {course.get('name', '<unknown>')}")
        elif not isinstance(course_sources, list) or not course_sources:
            source_failures.append(f"course with empty sources: {course.get('name', '<unknown>')}")
        else:
            for source_id in course_sources:
                if source_id not in source_ids:
                    source_failures.append(
                        f"course {course.get('name', '<unknown>')} references unknown source_id '{source_id}'"
                    )

    for course_index, course in enumerate(courses, start=1):
        if course_index not in covered_course_indexes:
            uncovered_courses.append(
                f"manifest course not covered by any source entry: {course_label(course, course_index)}"
            )

    if entry_failures or provenance_failures or source_failures or uncovered_courses:
        print_failures("entry", entry_failures)
        print_failures("provenance", provenance_failures)
        print_failures("sources", source_failures)
        print_failures("uncovered", uncovered_courses)
        print(
            "SUMMARY "
            f"entry_failures={len(entry_failures)} "
            f"provenance_failures={len(provenance_failures)} "
            f"source_failures={len(source_failures)} "
            f"uncovered_courses={len(uncovered_courses)}"
        )
        raise SystemExit(1)

    print(f"OK source_entries={len(entries)} courses={len(courses)}")


if __name__ == "__main__":
    main()
