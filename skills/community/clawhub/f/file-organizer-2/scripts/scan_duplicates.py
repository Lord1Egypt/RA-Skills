#!/usr/bin/env python3
"""Read-only duplicate scanner.

Finds duplicate and near-duplicate files by content hash, name, and size.
This script NEVER deletes, moves, or renames anything — it only reports.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from hashlib import sha256
from pathlib import Path
from typing import Any


def digest_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    """Compute SHA-256 of a file without loading it fully into memory."""
    digest = sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scan(
    root: Path,
    *,
    recursive: bool,
    max_bytes: int,
    include_hidden: bool,
) -> dict[str, Any]:
    iterator = root.rglob("*") if recursive else root.iterdir()
    groups_by_hash: dict[str, list[str]] = defaultdict(list)
    groups_by_name: dict[str, list[str]] = defaultdict(list)
    groups_by_size: dict[int, list[str]] = defaultdict(list)
    total_files = 0
    skipped = 0

    for path in iterator:
        if not path.is_file() or path.is_symlink():
            continue
        if not include_hidden and path.name.startswith("."):
            continue
        try:
            size = path.stat().st_size
        except OSError:
            skipped += 1
            continue
        if size > max_bytes:
            skipped += 1
            continue
        total_files += 1
        rel = path.as_posix()
        groups_by_name[path.name].append(rel)
        groups_by_size[size].append(rel)
        try:
            groups_by_hash[digest_file(path)].append(rel)
        except OSError:
            skipped += 1

    exact_dupes = [
        sorted(paths) for paths in groups_by_hash.values() if len(paths) > 1
    ]
    name_dupes = [
        sorted(paths) for paths in groups_by_name.values() if len(paths) > 1
    ]
    size_dupes = [
        sorted(paths) for paths in groups_by_size.values() if len(paths) > 1
    ]

    return {
        "root": str(root),
        "recursive": recursive,
        "total_files": total_files,
        "skipped": skipped,
        "exact_duplicate_groups": exact_dupes,
        "same_name_groups": name_dupes,
        "similar_size_groups": size_dupes,
    }


def format_human(report: dict[str, Any]) -> str:
    lines = [
        f"Root: {report['root']}",
        f"Files scanned: {report['total_files']} (skipped {report['skipped']})",
        "",
    ]

    exact = report["exact_duplicate_groups"]
    lines.append(f"完全重复组 (SHA-256 相同): {len(exact)} 组")
    for group in exact:
        lines.append("  - " + "\n    - ".join(group))

    name_dupes = report["same_name_groups"]
    lines.append(f"\n同名文件组: {len(name_dupes)} 组")
    for group in name_dupes[:50]:
        lines.append("  - " + "\n    - ".join(group))

    size_dupes = report["similar_size_groups"]
    lines.append(f"\n相似大小文件组: {len(size_dupes)} 组")
    lines.append("（注意：相似大小不等于内容重复，仅作候选提示）")
    for group in size_dupes[:50]:
        lines.append("  - " + "\n    - ".join(group))

    lines.append("\n本脚本只报告，不删除/移动/重命名任何文件。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only duplicate scanner (never deletes or moves files)."
    )
    parser.add_argument("root", type=Path, help="Directory to scan")
    parser.add_argument(
        "--recursive", "-r", action="store_true", help="Recurse into subdirectories"
    )
    parser.add_argument(
        "--max-bytes",
        type=int,
        default=256 * 1024 * 1024,
        help="Skip files larger than this (default 256 MiB)",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden (dot) files",
    )
    parser.add_argument(
        "--json", type=Path, help="Write machine-readable JSON to this path"
    )
    args = parser.parse_args()

    if args.max_bytes <= 0:
        parser.error("--max-bytes must be positive")

    root = args.root.expanduser()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    report = scan(
        root,
        recursive=args.recursive,
        max_bytes=args.max_bytes,
        include_hidden=args.include_hidden,
    )

    if args.json is not None:
        args.json.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"JSON written to {args.json}")
    else:
        print(format_human(report))

    return 0


if __name__ == "__main__":
    sys.exit(main())
