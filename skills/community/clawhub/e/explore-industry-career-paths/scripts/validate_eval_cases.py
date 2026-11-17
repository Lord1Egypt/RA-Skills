#!/usr/bin/env python3
"""Validate the release regression-case inventory."""

from __future__ import annotations

import csv
from pathlib import Path


REQUIRED_COLUMNS = {
    "case_id",
    "category",
    "prompt",
    "expected_mode",
    "required_modules",
    "critical_check",
    "risk_level",
}
ALLOWED_MODES = {"快速判断", "系统入门", "转行求职", "创业验证", "继续复盘"}
ALLOWED_RISKS = {"low", "medium", "high", "critical"}
EXPECTED_CASES = 50


def main() -> None:
    path = Path(__file__).resolve().parents[1] / "evals" / "cases.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        if columns != REQUIRED_COLUMNS:
            raise SystemExit(
                f"Invalid columns: expected {sorted(REQUIRED_COLUMNS)}, got {sorted(columns)}"
            )
        rows = list(reader)

    errors: list[str] = []
    if len(rows) != EXPECTED_CASES:
        errors.append(f"expected {EXPECTED_CASES} cases, got {len(rows)}")

    seen: set[str] = set()
    for line_number, row in enumerate(rows, start=2):
        case_id = row["case_id"].strip()
        if not all(value.strip() for value in row.values()):
            errors.append(f"line {line_number}: blank field")
        if case_id in seen:
            errors.append(f"line {line_number}: duplicate case_id {case_id}")
        seen.add(case_id)
        if row["expected_mode"] not in ALLOWED_MODES:
            errors.append(f"line {line_number}: invalid mode {row['expected_mode']}")
        if row["risk_level"] not in ALLOWED_RISKS:
            errors.append(f"line {line_number}: invalid risk {row['risk_level']}")

    if errors:
        raise SystemExit("Evaluation case validation failed:\n- " + "\n- ".join(errors))

    categories: dict[str, int] = {}
    for row in rows:
        categories[row["category"]] = categories.get(row["category"], 0) + 1
    print(f"Validated {len(rows)} unique cases: {categories}")


if __name__ == "__main__":
    main()
