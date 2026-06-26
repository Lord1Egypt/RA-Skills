#!/usr/bin/env python3
"""Verify the redacted output and surface any remaining manual-review items."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from redaction_common import find_line_findings, iter_candidate_files, read_text_if_supported


def require_existing_path(parser: argparse.ArgumentParser, raw_path: str, label: str) -> Path:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        parser.error(f"{label} does not exist: {path}")
    return path


def load_manual_review_items(path: Path) -> List[dict[str, str]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"Unable to read --redaction report: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"--redaction report is not valid UTF-8: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"--redaction report is not valid JSON: {path}") from exc

    items: List[dict[str, str]] = []
    for item in payload.get("skipped_files") or []:
        if isinstance(item, dict):
            file_name = str(item.get("file") or "").strip()
            reason = str(item.get("reason") or "manual-review-required").strip()
        else:
            file_name = str(item).strip()
            reason = "manual-review-required"
        if file_name:
            items.append({"file": file_name, "reason": reason})
    return items


def merge_manual_review_items(*groups: List[dict[str, str]]) -> List[dict[str, str]]:
    merged: list[dict[str, str]] = []
    seen_files: set[str] = set()
    for group in groups:
        for item in group:
            file_name = str(item.get("file") or "").strip()
            reason = str(item.get("reason") or "manual-review-required").strip()
            if not file_name or file_name in seen_files:
                continue
            merged.append({"file": file_name, "reason": reason})
            seen_files.add(file_name)
    return merged


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Redacted output directory or file.")
    parser.add_argument("--redaction", required=True, help="Redaction JSON report used to surface skipped files as manual-review items.")
    parser.add_argument("--out", required=True, help="Output JSON report path.")
    args = parser.parse_args()

    root = require_existing_path(parser, args.root, "--root")
    redaction_path = require_existing_path(parser, args.redaction, "--redaction")
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    findings: list[dict[str, object]] = []
    scanned_files = 0
    skipped_files: list[str] = []
    output_manual_review_files: list[dict[str, str]] = []

    for path in iter_candidate_files(root):
        text = read_text_if_supported(path)
        if text is None:
            rel_path = str(path.relative_to(root)) if root.is_dir() else path.name
            skipped_files.append(rel_path)
            output_manual_review_files.append({"file": rel_path, "reason": "binary-or-unsupported-output"})
            continue
        scanned_files += 1
        rel_path = str(path.relative_to(root)) if root.is_dir() else path.name
        for finding in find_line_findings(text):
            findings.append(
                {
                    "file": rel_path,
                    "line": finding["line"],
                    "code": finding["code"],
                    "severity": finding["severity"],
                    "snippet": finding["snippet"],
                }
            )

    try:
        manual_review_files = merge_manual_review_items(
            load_manual_review_items(redaction_path),
            output_manual_review_files,
        )
    except ValueError as exc:
        parser.error(str(exc))
    error_count = sum(1 for item in findings if item["severity"] == "error")
    warning_count = sum(1 for item in findings if item["severity"] == "warning")
    if findings:
        status = "fix-required"
    elif manual_review_files:
        status = "manual-review-required"
    else:
        status = "share-ready"
    payload = {
        "root": str(root),
        "scanned_files": scanned_files,
        "skipped_files": skipped_files,
        "manual_review_files": manual_review_files,
        "manual_review_count": len(manual_review_files),
        "finding_count": len(findings),
        "error_count": error_count,
        "warning_count": warning_count,
        "status": status,
        "findings": findings,
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
