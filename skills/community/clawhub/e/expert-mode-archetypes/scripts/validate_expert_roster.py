#!/usr/bin/env python3
"""Validate an Expert Mode project-local roster and dossiers.

Usage:
  python3 scripts/validate_expert_roster.py --project /path/to/project
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REQUIRED_DOSSIER_SECTIONS = [
    "## Scope",
    "## Archetype buckets",
    "## Load when",
    "## Do not load when",
    "## Client relationship stance",
    "## Expert operating loop",
    "## Judgement standards",
    "## Definitive information sources",
    "## Heuristic information sources",
]

RISKY_FAKE_AUTHORITY_PATTERNS = [
    r"\bDr\.\s+[A-Z][A-Za-z]+",
    r"\bProfessor\s+[A-Z][A-Za-z]+",
    r"\bcertified\s+[A-Z][A-Za-z]+",
    r"\bformer\s+[A-Z][A-Za-z]+\b",
    r"\bworked at\s+[A-Z][A-Za-z]+",
]


def extract_dossier_paths(roster_text: str) -> list[str]:
    paths: list[str] = []
    for match in re.finditer(r"dossiers/[a-z0-9][a-z0-9-]*\.md", roster_text):
        path = match.group(0)
        if path not in paths:
            paths.append(path)
    return paths


def validate(project: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    roster = project / "experts" / "roster.md"
    if not roster.exists():
        return [f"Missing roster: {roster}"], []

    roster_text = roster.read_text(encoding="utf-8")
    dossier_paths = extract_dossier_paths(roster_text)
    if not dossier_paths:
        errors.append("Roster contains no dossier paths like dossiers/<slug>.md")

    for rel in dossier_paths:
        dossier = project / "experts" / rel
        if not dossier.exists():
            errors.append(f"Missing dossier referenced by roster: {dossier}")
            continue
        text = dossier.read_text(encoding="utf-8")
        for section in REQUIRED_DOSSIER_SECTIONS:
            if section not in text:
                errors.append(f"{dossier}: missing section {section}")
        for pattern in RISKY_FAKE_AUTHORITY_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                warnings.append(
                    f"{dossier}: review possible fake-authority phrase matching {pattern!r}"
                )

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, help="Project directory containing experts/roster.md")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    errors, warnings = validate(project)
    if errors:
        print("Expert roster validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if warnings:
        print("Expert roster validation passed with warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("Expert roster validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
