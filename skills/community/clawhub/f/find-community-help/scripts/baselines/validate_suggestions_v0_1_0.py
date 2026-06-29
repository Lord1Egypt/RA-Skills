#!/usr/bin/env python3
"""Validate the canonical agent-travel suggestion block (v0.1.0 baseline)."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


START = "<!-- agent-travel:suggestions:start -->"
END = "<!-- agent-travel:suggestions:end -->"
TOP_LEVEL_REQUIRED = {
    "generated_at",
    "expires_at",
    "budget",
    "search_mode",
    "tool_preference",
    "source_scope",
    "thread_scope",
    "problem_fingerprint",
    "advisory_only",
}
ITEM_REQUIRED = {
    "title",
    "applies_when",
    "hint",
    "confidence",
    "manual_check",
    "solves_point",
    "new_idea",
    "fit_reason",
    "match_reasoning",
    "version_scope",
    "do_not_apply_when",
}
ALLOWED_TOOL_PREFERENCES = {"public-only", "all-available", "custom"}
MATCH_AXES = {
    "host",
    "version",
    "symptom",
    "constraint",
    "constraint_pattern",
    "desired_next_outcome",
    "desired-next-outcome",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="Path to suggestions.md")
    return parser.parse_args()


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1


def parse_iso(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    if not path.exists():
        return fail([f"file not found: {path}"])

    text = path.read_text(encoding="utf-8")
    start = text.rfind(START)
    end = text.rfind(END)
    if start == -1 or end == -1 or end <= start:
        return fail(["missing or invalid agent-travel markers"])

    block = text[start + len(START) : end].strip()
    lines = [line.rstrip() for line in block.splitlines()]

    errors: list[str] = []
    top_level: dict[str, str] = {}
    suggestions: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_evidence: list[str] | None = None
    current_match_reasoning: list[str] | None = None

    key_pattern = re.compile(r"^([a-z_]+):\s*(.+)$")
    heading_pattern = re.compile(r"^##\s+suggestion-\d+\s*$")

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("# agent-travel suggestions"):
            continue
        if heading_pattern.match(line):
            current = {"evidence": [], "match_reasoning": []}
            suggestions.append(current)
            current_evidence = None
            current_match_reasoning = None
            continue
        if line == "evidence:":
            if current is None:
                errors.append("found evidence block before any suggestion heading")
                continue
            current_evidence = current["evidence"]  # type: ignore[assignment]
            current_match_reasoning = None
            continue
        if line == "match_reasoning:":
            if current is None:
                errors.append("found match_reasoning block before any suggestion heading")
                continue
            current_match_reasoning = current["match_reasoning"]  # type: ignore[assignment]
            current_evidence = None
            continue
        if line.startswith("- "):
            if current_evidence is None:
                if current_match_reasoning is None:
                    errors.append(f"unexpected list item outside block: {line}")
                    continue
                current_match_reasoning.append(line[2:].strip())
                continue
            current_evidence.append(line[2:].strip())
            continue

        match = key_pattern.match(line)
        if not match:
            errors.append(f"unrecognized line: {line}")
            current_evidence = None
            current_match_reasoning = None
            continue

        key, value = match.groups()
        current_evidence = None
        current_match_reasoning = None
        if current is None:
            top_level[key] = value
        else:
            current[key] = value

    missing_top = sorted(TOP_LEVEL_REQUIRED - set(top_level))
    if missing_top:
        errors.append(f"missing top-level fields: {', '.join(missing_top)}")
    if top_level.get("advisory_only", "").lower() != "true":
        errors.append("advisory_only must be true")
    if top_level.get("thread_scope", "") != "active_conversation_only":
        errors.append("thread_scope must be active_conversation_only")
    tool_preference = top_level.get("tool_preference", "")
    if tool_preference not in ALLOWED_TOOL_PREFERENCES:
        errors.append(f"tool_preference must be one of: {', '.join(sorted(ALLOWED_TOOL_PREFERENCES))}")
    if "primary" not in top_level.get("source_scope", ""):
        errors.append("source_scope must include primary")

    if {"generated_at", "expires_at"} <= set(top_level):
        try:
            generated = parse_iso(top_level["generated_at"])
            expires = parse_iso(top_level["expires_at"])
            if expires <= generated:
                errors.append("expires_at must be later than generated_at")
        except ValueError as exc:
            errors.append(f"invalid ISO date: {exc}")

    if not suggestions:
        errors.append("no suggestions found")

    for index, suggestion in enumerate(suggestions, start=1):
        missing = sorted(ITEM_REQUIRED - set(suggestion))
        if missing:
            errors.append(f"suggestion-{index} is missing fields: {', '.join(missing)}")
        evidence = suggestion.get("evidence", [])
        if not isinstance(evidence, list) or len(evidence) < 2:
            errors.append(f"suggestion-{index} needs at least 2 evidence items")
        elif not any(item.startswith("primary_") or item.startswith("primary:") for item in evidence):
            errors.append(f"suggestion-{index} needs at least 1 primary evidence item")
        match_reasoning = suggestion.get("match_reasoning", [])
        if not isinstance(match_reasoning, list) or len(match_reasoning) < 4:
            errors.append(f"suggestion-{index} needs at least 4 match_reasoning items")
        elif any(":" not in item for item in match_reasoning):
            errors.append(f"suggestion-{index} match_reasoning items must use axis: explanation format")
        else:
            matched_axes = {
                item.split(":", 1)[0].strip().replace(" ", "_").lower() for item in match_reasoning
            }
            if len(matched_axes & MATCH_AXES) < 4:
                errors.append(f"suggestion-{index} needs at least 4 distinct match_reasoning axes")

    if errors:
        return fail(errors)

    print(f"OK: validated {len(suggestions)} suggestion(s) in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
