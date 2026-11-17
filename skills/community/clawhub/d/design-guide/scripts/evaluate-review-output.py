#!/usr/bin/env python3
"""Evaluate a captured design-guide review response against an explicit scope contract."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

try:
    from i18n import add_locale_argument, resolve_locale, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, resolve_locale, t


SCOPE_PATTERN = re.compile(r"^(?:\*\*)?Review scope(?:\*\*)?:\s*(.+)$", re.IGNORECASE)
EXCLUDED_PATTERN = re.compile(r"^(?:\*\*)?Not included by default(?:\*\*)?:\s*(.+)$", re.IGNORECASE)


def load_json(path: pathlib.Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return data


def section_value(lines: list[str], pattern: re.Pattern[str]) -> tuple[str | None, int | None]:
    for index, line in enumerate(lines[:12]):
        match = pattern.match(line.strip())
        if match:
            return match.group(1).strip(), index
    return None, None


def evaluate(case: dict, response: str) -> list[str]:
    errors: list[str] = []
    lines = response.splitlines()
    scope, scope_index = section_value(lines, SCOPE_PATTERN)
    excluded, excluded_index = section_value(lines, EXCLUDED_PATTERN)
    if not scope:
        errors.append("missing Review scope line near the start")
    if not excluded:
        errors.append("missing Not included by default line near the start")

    for term in case.get("scopeMustMention", []):
        if not scope or term.casefold() not in scope.casefold():
            errors.append(f"scope does not mention required term: {term}")
    for term in case.get("excludedMustMention", []):
        if not excluded or term.casefold() not in excluded.casefold():
            errors.append(f"excluded scope does not mention: {term}")

    omitted = {index for index in (scope_index, excluded_index) if index is not None}
    body = "\n".join(line for index, line in enumerate(lines) if index not in omitted)
    for term in case.get("bodyMustNotMention", []):
        if term.casefold() in body.casefold():
            errors.append(f"response body inherits or expands out-of-scope term: {term}")
    for term in case.get("bodyMustMention", []):
        if term.casefold() not in body.casefold():
            errors.append(f"response body misses required evidence/output term: {term}")
    max_words = case.get("maxWords")
    if isinstance(max_words, int) and len(response.split()) > max_words:
        errors.append(f"response exceeds maxWords: {max_words}")
    return errors


def main() -> int:
    locale = resolve_locale()
    parser = argparse.ArgumentParser(description=t("Check a captured design-review response against its scope contract.", locale))
    add_locale_argument(parser)
    parser.add_argument("case", help=t("JSON scope contract", locale))
    parser.add_argument("response", help=t("Captured Markdown/text response", locale))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        case = load_json(pathlib.Path(args.case))
        response = pathlib.Path(args.response).read_text(encoding="utf-8")
        errors = evaluate(case, response)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(t("Evaluation error: {error}", args.locale, error=exc), file=sys.stderr)
        return 2
    result = {"case": case.get("id"), "passed": not errors, "errors": errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif errors:
        print(t("Review behavior: FAIL ({id})", args.locale, id=case.get("id", "unknown")))
        for error in errors:
            print(f"- {error}")
    else:
        print(t("Review behavior: PASS ({id})", args.locale, id=case.get("id", "unknown")))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
