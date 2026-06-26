#!/usr/bin/env python3
"""Write a redacted copy of supported text artifacts into a clean output directory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from redaction_common import iter_candidate_files, read_text_if_supported, redact_text


def merge_counts(total: dict[str, int], current: dict[str, int]) -> None:
    for key, value in current.items():
        total[key] = total.get(key, 0) + int(value)


def require_existing_path(parser: argparse.ArgumentParser, raw_path: str, label: str) -> Path:
    path = Path(raw_path).expanduser().resolve()
    if not path.exists():
        parser.error(f"{label} does not exist: {path}")
    return path


def path_is_within(candidate: Path, ancestor: Path) -> bool:
    try:
        candidate.relative_to(ancestor)
    except ValueError:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Source file or directory.")
    parser.add_argument("--out-dir", required=True, help="Output directory for the redacted copy.")
    parser.add_argument("--out", required=True, help="Output JSON report path.")
    args = parser.parse_args()

    root = require_existing_path(parser, args.root, "--root")
    out_dir = Path(args.out_dir).expanduser().resolve()
    report_path = Path(args.out).expanduser().resolve()
    if root.is_dir() and (
        out_dir == root or path_is_within(out_dir, root) or path_is_within(root, out_dir)
    ):
        parser.error("--out-dir must not overlap with --root when --root is a directory")
    if out_dir.exists() and any(out_dir.iterdir()):
        parser.error("--out-dir must be empty before redaction starts")
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    files: list[dict[str, object]] = []
    skipped_files: list[dict[str, str]] = []
    totals = {
        "private_url": 0,
        "public_url_query": 0,
        "private_path": 0,
        "secret_like": 0,
        "email": 0,
        "phone": 0,
    }

    for path in iter_candidate_files(root):
        if out_dir.exists() and path_is_within(path, out_dir):
            continue
        rel_path = Path(path.name) if root.is_file() else path.relative_to(root)
        text = read_text_if_supported(path)
        if text is None:
            skipped_files.append({"file": str(rel_path), "reason": "binary-or-unsupported"})
            continue

        redacted, counts = redact_text(text)
        merge_counts(totals, counts)
        target_path = out_dir / rel_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(redacted, encoding="utf-8")
        files.append(
            {
                "file": str(rel_path),
                "changed": redacted != text,
                "redaction_counts": counts,
            }
        )

    payload = {
        "root": str(root),
        "output_dir": str(out_dir),
        "processed_files": len(files),
        "skipped_files": skipped_files,
        "redaction_counts": totals,
        "files": files,
    }
    report_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
