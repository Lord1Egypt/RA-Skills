#!/usr/bin/env python3
"""Fail-closed validator for canonical book JSON and its derivative bundle."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from build_derivatives import collect_tree_paths, load_tree, prefix_for, render_derivatives
from compare_tree_export import canonical_nodes, fingerprint


REQUIRED_NODE_FIELDS = (
    "key",
    "title",
    "level",
    "parent_key",
    "sort",
    "logical_page",
    "source_page",
    "heading_start",
    "content_start",
    "content_end",
    "heading_score",
    "structural_only",
    "content",
    "content_chars",
    "source_file",
)
VALID_REVIEW_DECISIONS = {"corrected", "accepted", "false_positive"}
MOJIBAKE = re.compile(r"Ã|Â|â|ï¿½")
PAGE_MARKER = re.compile(r"={3,}\s*第\s*\d+\s*页\s*={3,}")
PRIVATE_USE = re.compile(r"[\ue000-\uf8ff\U000f0000-\U000ffffd\U00100000-\U0010fffd]")
LIKELY_OCR_PATTERNS = (
    ("cjk_double_space", re.compile(r"[\u3400-\u9fff][ \u3000]{2,}[\u3400-\u9fff]")),
    ("ascii_punctuation_between_cjk", re.compile(r"[\u3400-\u9fff][,;:!?][\u3400-\u9fff]")),
    ("mixed_letter_digit_run", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]+\d+[A-Za-z0-9]*|\d+[A-Za-z]+[A-Za-z0-9]*(?![A-Za-z0-9])")),
    ("duplicated_punctuation", re.compile(r"([，。！？；：、,.!?;:])\1+")),
)


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[tuple[str | None, str]] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str, candidate_id: str | None = None) -> None:
        self.warnings.append((candidate_id, message))


def is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_tree(
    path: Path,
    tree: dict[str, Any],
    audit: Audit,
    min_heading_score: float,
) -> tuple[dict[str, dict[str, Any]], str]:
    label = str(tree.get("book_id") or path.name)
    if not isinstance(tree.get("book_id"), str) or not tree["book_id"].strip():
        audit.error(f"{path}: book_id must be a nonempty string")
    if not isinstance(tree.get("title"), str) or not tree["title"].strip():
        audit.error(f"{path}: title must be a nonempty string")
    if tree.get("authority") != "printed_toc":
        audit.error(f"{label}: authority must equal printed_toc")
    if "review_status" in tree and tree.get("review_status") != "approved":
        audit.error(f"{label}: review_status must equal approved for final delivery")
    nodes = tree.get("nodes", [])
    if not is_int(tree.get("node_count")) or tree.get("node_count") != len(nodes):
        audit.error(f"{label}: node_count does not equal len(nodes)")

    by_key: dict[str, dict[str, Any]] = {}
    for index, node in enumerate(nodes, start=1):
        where = f"{label}: node {index}"
        if not isinstance(node, dict):
            audit.error(f"{where}: must be an object")
            continue
        missing = [field for field in REQUIRED_NODE_FIELDS if field not in node]
        if missing:
            audit.error(f"{where}: missing fields {', '.join(missing)}")
        key = node.get("key")
        if not isinstance(key, str) or not key:
            audit.error(f"{where}: key must be a nonempty string")
        elif key in by_key:
            audit.error(f"{label}: duplicate key {key}")
        else:
            by_key[key] = node
        if not isinstance(node.get("title"), str) or not node.get("title", "").strip():
            audit.error(f"{where}: title must be a nonempty string")
        for field in ("level", "sort", "heading_start", "content_start", "content_end"):
            if not is_int(node.get(field)):
                audit.error(f"{where}: {field} must be an integer")
        if node.get("logical_page") is not None and not is_int(node.get("logical_page")):
            audit.error(f"{where}: logical_page must be an integer or null")
        if node.get("source_page") is not None and not is_int(node.get("source_page")):
            audit.error(f"{where}: source_page must be an integer or null")
        if not isinstance(node.get("heading_score"), (int, float)) or isinstance(node.get("heading_score"), bool):
            audit.error(f"{where}: heading_score must be numeric")
        elif not 0 <= float(node["heading_score"]) <= 1:
            audit.error(f"{where}: heading_score must be within 0..1")
        elif float(node["heading_score"]) < min_heading_score:
            audit.error(
                f"{where}: heading_score {node['heading_score']} is below the declared threshold {min_heading_score}"
            )
        if not isinstance(node.get("structural_only"), bool):
            audit.error(f"{where}: structural_only must be boolean")
        content = node.get("content")
        if not isinstance(content, str):
            audit.error(f"{where}: content must be a string")
            content = ""
        if node.get("structural_only") is False and not content.strip():
            audit.error(f"{where}: content-bearing node is empty")
        if not is_int(node.get("content_chars")) or node.get("content_chars") != len(content):
            audit.error(f"{where}: content_chars mismatch")
        if not isinstance(node.get("source_file"), str) or not node.get("source_file", "").strip():
            audit.error(f"{where}: source_file must be a nonempty string")
        if all(is_int(node.get(field)) for field in ("heading_start", "content_start", "content_end")):
            if not node["heading_start"] <= node["content_start"] <= node["content_end"]:
                audit.error(f"{where}: invalid heading/content offsets")

        if "\ufffd" in content:
            audit.error(f"{where}: contains U+FFFD")
        if MOJIBAKE.search(content):
            audit.error(f"{where}: contains likely mojibake")
        if PAGE_MARKER.search(content):
            audit.error(f"{where}: contains an intermediate page marker")
        if PRIVATE_USE.search(content):
            audit.error(f"{where}: contains a Unicode private-use character")
        if any(ord(char) < 32 and char not in "\t\n\r" for char in content):
            audit.error(f"{where}: contains an invalid control character")
        for name, pattern in LIKELY_OCR_PATTERNS:
            for occurrence, _ in enumerate(pattern.finditer(content), start=1):
                audit.warn(
                    f"{where}: review candidate {name}",
                    candidate_id=f"{label}:{key}:{name}:{occurrence}",
                )

    expected_sorts = list(range(1, len(nodes) + 1))
    actual_sorts = [node.get("sort") for node in nodes if isinstance(node, dict)]
    if sorted(value for value in actual_sorts if is_int(value)) != expected_sorts:
        audit.error(f"{label}: sort values must be exactly 1..node_count")

    last_heading: int | None = None
    for node in sorted((n for n in nodes if isinstance(n, dict)), key=lambda n: n.get("sort", 0)):
        key = node.get("key")
        parent = node.get("parent_key")
        if parent is not None:
            if parent not in by_key:
                audit.error(f"{label}: {key} references missing parent {parent}")
            elif is_int(node.get("level")) and is_int(by_key[parent].get("level")):
                if node["level"] != by_key[parent]["level"] + 1:
                    audit.error(f"{label}: {key} level is inconsistent with parent {parent}")
        elif node.get("level") != 1:
            audit.error(f"{label}: root {key} must have level 1")
        heading = node.get("heading_start")
        if is_int(heading):
            if last_heading is not None and heading < last_heading:
                audit.error(f"{label}: heading offsets are not monotonic at {key}")
            last_heading = heading

    for key in by_key:
        seen: set[str] = set()
        cursor: str | None = key
        while cursor is not None:
            if cursor in seen:
                audit.error(f"{label}: parent cycle involving {cursor}")
                break
            seen.add(cursor)
            parent_node = by_key.get(cursor)
            cursor = parent_node.get("parent_key") if parent_node else None

    try:
        canonical = canonical_nodes(nodes, remote=False)
        digest = fingerprint(canonical)
    except (ValueError, TypeError) as exc:
        audit.error(f"{label}: fingerprint failed: {exc}")
        digest = "-"
    return by_key, digest


def validate_artifacts(path: Path, tree: dict[str, Any], artifact_dir: Path, audit: Audit) -> None:
    prefix = prefix_for(path)
    label = str(tree.get("book_id") or path.name)
    expected = render_derivatives(tree, prefix)
    for relative, expected_text in expected.items():
        target = artifact_dir / relative
        if not target.is_file():
            audit.error(f"{label}: missing derivative {target}")
            continue
        actual = target.read_text(encoding="utf-8-sig")
        if actual.replace("\r\n", "\n") != expected_text:
            audit.error(f"{label}: stale or non-deterministic derivative {target}")

    chapter_dir = artifact_dir / f"{prefix}_chapters"
    expected_chapters = {str(relative) for relative in expected if relative.parent.name == chapter_dir.name}
    actual_chapters = {
        str(Path(chapter_dir.name) / item.name) for item in chapter_dir.glob("*.txt")
    } if chapter_dir.is_dir() else set()
    extras = sorted(actual_chapters - expected_chapters)
    if extras:
        audit.error(f"{label}: unexpected stale chapter files: {', '.join(extras)}")


def load_review_rows(path: Path, audit: Audit) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            required = {"candidate_id", "book_id", "node_key", "original", "suggestion", "context", "decision", "reviewer"}
            if reader.fieldnames is None or not required.issubset(reader.fieldnames):
                audit.error(f"{path}: OCR review TSV must contain {', '.join(sorted(required))}")
                return []
            return [dict(row) for row in reader]
    except OSError as exc:
        audit.error(f"{path}: cannot read OCR review ledger: {exc}")
        return []


def validate_review_ledger(
    path: Path,
    books: dict[str, dict[str, dict[str, Any]]],
    audit: Audit,
) -> set[str]:
    rows = load_review_rows(path, audit)
    candidate_ids: set[str] = set()
    for number, row in enumerate(rows, start=2):
        where = f"{path}: row {number}"
        candidate_id = (row.get("candidate_id") or "").strip()
        if not candidate_id:
            audit.error(f"{where}: candidate_id is empty")
        elif candidate_id in candidate_ids:
            audit.error(f"{where}: duplicate candidate_id {candidate_id}")
        candidate_ids.add(candidate_id)
        decision = (row.get("decision") or "").strip()
        reviewer = (row.get("reviewer") or "").strip()
        if decision not in VALID_REVIEW_DECISIONS:
            audit.error(f"{where}: unresolved or invalid decision {decision!r}")
        if not reviewer:
            audit.error(f"{where}: reviewer is empty")
        book_id = (row.get("book_id") or "").strip()
        node_key = (row.get("node_key") or "").strip()
        node = books.get(book_id, {}).get(node_key)
        if node is None:
            audit.error(f"{where}: unknown book/node {book_id}/{node_key}")
            continue
        if decision == "corrected":
            original = row.get("original") or ""
            suggestion = row.get("suggestion") or ""
            if not original or not suggestion:
                audit.error(f"{where}: corrected rows require original and suggestion")
            elif original in str(node.get("content", "")):
                audit.error(f"{where}: corrected original text still exists in the target node")
    return candidate_ids


def compare_remote(local_dir: Path, remote_export: Path, audit: Audit) -> None:
    comparator = Path(__file__).with_name("compare_tree_export.py")
    result = subprocess.run(
        [sys.executable, str(comparator), "--local-dir", str(local_dir), "--remote-export", str(remote_export)],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        audit.error(f"remote read-back comparison failed with exit code {result.returncode}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trees", nargs="+", type=Path, help="canonical *_tree.json files or directories")
    parser.add_argument("--artifact-dir", type=Path, help="require deterministic derivatives in this directory")
    parser.add_argument("--ocr-review", type=Path, help="reviewed OCR candidate TSV")
    parser.add_argument("--require-ocr-review", action="store_true")
    parser.add_argument("--remote-export", type=Path, help="full remote read-back export")
    parser.add_argument("--fail-on-warnings", action="store_true")
    parser.add_argument("--min-heading-score", type=float, default=0.8)
    args = parser.parse_args()

    audit = Audit()
    try:
        paths = collect_tree_paths(args.trees)
    except (OSError, ValueError) as exc:
        print(f"ERROR\t{exc}", file=sys.stderr)
        return 2

    books: dict[str, dict[str, dict[str, Any]]] = {}
    total_nodes = 0
    for path in paths:
        try:
            tree = load_tree(path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            audit.error(f"{path}: {exc}")
            continue
        book_id = str(tree.get("book_id") or path.name)
        if book_id in books:
            audit.error(f"duplicate book_id across files: {book_id}")
        by_key, digest = validate_tree(path, tree, audit, args.min_heading_score)
        books[book_id] = by_key
        total_nodes += len(tree.get("nodes", []))
        print(f"FINGERPRINT\t{book_id}\t{len(tree.get('nodes', []))}\t{digest}")
        if args.artifact_dir:
            try:
                validate_artifacts(path, tree, args.artifact_dir, audit)
            except (OSError, ValueError, TypeError) as exc:
                audit.error(f"{book_id}: derivative validation failed: {exc}")

    if args.require_ocr_review and args.ocr_review is None:
        audit.error("final validation requires --ocr-review")
    resolved_warning_ids: set[str] = set()
    if args.ocr_review is not None:
        resolved_warning_ids = validate_review_ledger(args.ocr_review, books, audit)
        audit.warnings = [
            (candidate_id, message)
            for candidate_id, message in audit.warnings
            if candidate_id is None or candidate_id not in resolved_warning_ids
        ]

    if args.remote_export is not None:
        parents = {path.resolve().parent for path in paths}
        if len(parents) != 1:
            audit.error("remote comparison requires all local trees to share one directory")
        else:
            compare_remote(next(iter(parents)), args.remote_export, audit)

    for candidate_id, warning in audit.warnings:
        suffix = f"\tcandidate_id={candidate_id}" if candidate_id else ""
        print(f"WARNING\t{warning}{suffix}")
    for error in audit.errors:
        print(f"ERROR\t{error}", file=sys.stderr)

    warning_failure = args.fail_on_warnings and bool(audit.warnings)
    result = "FAIL" if audit.errors or warning_failure else "PASS"
    print(
        f"{result}\t{len(paths)} books\t{total_nodes} nodes\t"
        f"{len(audit.errors)} errors\t{len(audit.warnings)} warnings"
    )
    return 1 if audit.errors or warning_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
