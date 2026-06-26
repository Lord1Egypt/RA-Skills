#!/usr/bin/env python3
"""Scan text artifacts for obvious sensitive text patterns."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from redaction_common import find_line_findings, iter_candidate_files, read_text_if_supported


def require_existing_path(parser: argparse.ArgumentParser, raw_path: str, label: str) -> Path:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        parser.error(f"{label} does not exist: {path}")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Root file or directory to scan.")
    parser.add_argument("--out", required=True, help="Output JSON file.")
    args = parser.parse_args()

    root = require_existing_path(parser, args.root, "--root")
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    findings: list[dict[str, object]] = []
    scanned_files = 0
    skipped_files: list[str] = []

    for path in iter_candidate_files(root):
        text = read_text_if_supported(path)
        if text is None:
            skipped_files.append(str(path.relative_to(root)) if root.is_dir() else path.name)
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

    error_count = sum(1 for item in findings if item["severity"] == "error")
    warning_count = sum(1 for item in findings if item["severity"] == "warning")
    payload = {
        "root": str(root),
        "scanned_files": scanned_files,
        "skipped_files": skipped_files,
        "finding_count": len(findings),
        "error_count": error_count,
        "warning_count": warning_count,
        "findings": findings,
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
