"""Collect source facts and duplicate-block candidates without declaring semantic defects."""

from __future__ import annotations

import argparse
from collections import defaultdict
import math
from pathlib import Path
import re
import sys

from detect_lang import require_python

# Check the interpreter before importing modules that need Python 3.11+ (tomllib).
require_python()

from dependencies import READERS, load_manifest, read_dependencies  # noqa: E402
from detect_lang import (  # noqa: E402
    BUILD_NAMES,
    IGNORED_DIRS,
    MAX_UNITS,
    SOURCE_SUFFIXES,
    add_project_arguments,
    detect_languages,
    discover_units,
    markdown_report,
    positive_int,
    print_report,
    print_text,
    scan_files,
)

ENTRY_PATTERN = re.compile(
    r"\bfn\s+main\s*\(|\bint\s+w?main\s*\(|\bfunc\s+main\s*\(\s*\)|"
    r"\bstatic\s+void\s+main\s*\(|\bfun\s+main\s*\(|"
    r"if\s+__name__\s*==\s*['\"]__main__['\"]"
)
BLOCK_COMMENT_CONTINUATION = re.compile(r"^\*(?:\s|/|$)")
MANIFEST_ENTRY_KEYS = {
    "package.json": (("main",), ("module",), ("bin",), ("exports",), ("scripts",)),
    "pyproject.toml": (
        ("project", "scripts"),
        ("project", "gui-scripts"),
        ("project", "entry-points"),
        ("tool", "poetry", "scripts"),
    ),
    "Cargo.toml": (("bin",), ("lib",)),
}
LIST_LIMIT = 100


def source_paths(files: list[Path], languages: list[str]) -> list[Path]:
    """Select source suffixes for the given languages without inferring reachability from them."""
    known = [SOURCE_SUFFIXES[lang] for lang in languages if lang in SOURCE_SUFFIXES]
    suffixes = set().union(*(known or SOURCE_SUFFIXES.values()))
    return [path for path in files if path.suffix.lower() in suffixes]


def decode_source(data: bytes) -> tuple[str, str]:
    """Decode UTF-8 first, then GB18030 for legacy Chinese sources, and never drop a file."""
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace"), "utf-8-with-replacement"


def read_sources(
    paths: list[Path],
    root: Path,
    warnings: list[str],
    decoded: list[dict] | None = None,
) -> dict[str, list[str]]:
    """Read each source once; record read failures as gaps and non-UTF-8 decoding as coverage notes."""
    sources = {}
    for path in paths:
        relative = path.relative_to(root).as_posix()
        try:
            data = path.read_bytes()
        except OSError as error:
            warnings.append(f"{relative}: {type(error).__name__}")
            continue
        text, encoding = decode_source(data)
        if decoded is not None and encoding != "utf-8-sig":
            decoded.append({"file": relative, "encoding": encoding})
        sources[relative] = text.splitlines()
    return sources


def report_language(requested: str, languages: list[str]) -> str:
    """Name the selected language, or mixed/unknown when the scanned languages are ambiguous."""
    if requested != "auto":
        return requested
    if len(languages) == 1:
        return languages[0]
    return "mixed" if languages else "unknown"


def scan_languages(
    requested: str, root_languages: list[str], units: list[dict]
) -> list[str]:
    """Use the explicit language, or every language found at the root and in nested units."""
    if requested != "auto":
        return [requested]
    return sorted(set(root_languages).union(*(unit["languages"] for unit in units)))


def manifest_entries(root: Path, units: list[dict], warnings: list[str]) -> list[dict]:
    """List manifest-declared entry points of every review unit; they need inspection, not trust."""
    entries = []
    for unit in units:
        for name, key_paths in MANIFEST_ENTRY_KEYS.items():
            if name not in unit["manifests"]:
                continue
            relative = name if unit["path"] == "." else f"{unit['path']}/{name}"
            try:
                data = load_manifest(root / relative)
            except (OSError, ValueError) as error:
                warnings.append(
                    f"{relative} could not be parsed for entry candidates: {type(error).__name__}"
                )
                continue
            for keys in key_paths:
                value = data
                for key in keys:
                    value = value.get(key) if isinstance(value, dict) else None
                if value:
                    entries.append(
                        {
                            "file": relative,
                            "field": ".".join(keys),
                            "kind": "inspect_manifest_entry",
                        }
                    )
    return entries


def unit_inventories(
    root: Path, units: list[dict], selected: str | None
) -> tuple[list[dict], list[str]]:
    """Inventory declared dependencies per review unit and language that has a manifest reader.

    Returns the inventories and the unit languages that have no reader.
    """
    inventories, unsupported = [], set()
    for unit in units:
        for language in unit["languages"]:
            if selected and language != selected:
                continue
            if language not in READERS:
                unsupported.add(language)
                continue
            report = read_dependencies(root / unit["path"], language)
            prefix = "" if unit["path"] == "." else f"{unit['path']}/"
            inventories.append(
                {
                    "unit": unit["path"],
                    "language": language,
                    "count": report["count"],
                    "manifests": [prefix + name for name in report["manifests"]],
                    "warnings": report["warnings"],
                    "errors": report["errors"],
                }
            )
    return inventories, sorted(unsupported)


def coverage_section(
    ignored: frozenset[str], pruned: list[dict], decoded: list[dict]
) -> dict:
    """Describe what the scan policy excluded or decoded specially, using bounded lists."""
    return {
        "excluded_directories": sorted(ignored),
        "pruned_directories": pruned[:LIST_LIMIT],
        "pruned_directory_count": len(pruned),
        "follows_symlinks": False,
        "decoded_with_fallback": decoded[:LIST_LIMIT],
        "decoded_with_fallback_count": len(decoded),
    }


def collect_facts(
    root: Path,
    files: list[Path],
    warnings: list[str],
    requested: str,
    pruned: list[dict],
    ignored: frozenset[str],
) -> dict:
    """Collect bounded facts per review unit without claiming complete framework coverage."""
    units, truncated = discover_units(root, files)
    if truncated:
        warnings.append(f"more than {MAX_UNITS} review units; narrow --root")
    root_languages = detect_languages(root, files)
    languages = scan_languages(requested, root_languages, units)
    decoded: list[dict] = []
    sources = read_sources(source_paths(files, languages), root, warnings, decoded)
    entries = [
        {"file": file, "line": number, "kind": "source_entry_candidate"}
        for file, lines in sources.items()
        for number, line in enumerate(lines, 1)
        if ENTRY_PATTERN.search(line)
    ]
    entries.extend(manifest_entries(root, units, warnings))
    selected = None if requested == "auto" else requested
    inventories, unsupported = unit_inventories(root, units, selected)
    errors = [
        f"{item['unit']} ({item['language']}): {error}"
        for item in inventories
        for error in item["errors"]
    ]
    complete = not warnings and not errors
    coverage = coverage_section(ignored, pruned, decoded)
    coverage.update(
        entry_points="heuristic candidates; framework/config/export roots require inspection",
        dependency_languages_without_reader=unsupported,
    )
    return {
        "status": "completed" if complete else "incomplete",
        "complete": complete,
        "project": {
            "root": str(root),
            "language": report_language(requested, languages),
            "detected_languages": root_languages,
            "repository_languages": scan_languages("auto", root_languages, units),
        },
        "codebase": {
            "scanned_files": len(files),
            "source_files": len(sources),
            "source_lines": sum(len(lines) for lines in sources.values()),
        },
        "units": units,
        "build_files": [
            path.relative_to(root).as_posix() for path in files if path.name in BUILD_NAMES
        ],
        "entry_point_candidates": entries,
        "dependency_inventories": inventories,
        "warnings": warnings,
        "errors": errors,
        "coverage": coverage,
    }


def is_comment(text: str, suffix: str) -> bool:
    """Recognize whole-line comments without hiding code such as '*p = 0;' or '--count;'."""
    if suffix == ".py":
        return text.startswith("#")
    return text.startswith(("//", "/*")) or bool(BLOCK_COMMENT_CONTINUATION.match(text))


def meaningful_lines(lines: list[str], suffix: str) -> list[tuple[int, str]]:
    """Retain substantive lines and their locations, excluding punctuation-only and comment lines."""
    output = []
    for number, line in enumerate(lines, 1):
        text = line.strip()
        if not text or not re.search(r"\w", text) or is_comment(text, suffix):
            continue
        output.append((number, text))
    return output


def separated(locations: list[tuple[str, int]], threshold: int) -> tuple:
    """Keep sorted window locations, dropping same-file windows that overlap a kept one."""
    kept, last = [], {}
    for file, start in sorted(locations):
        if file in last and start - last[file] < threshold:
            continue
        kept.append((file, start))
        last[file] = start
    return tuple(kept)


def same_file_gap(locations: tuple) -> float:
    """Return the smallest distance between copies in one file, which bounds how far they grow."""
    gaps = [b[1] - a[1] for a, b in zip(locations, locations[1:]) if a[0] == b[0]]
    return min(gaps, default=math.inf)


def extend_match(
    locations: tuple, threshold: int, groups: dict, window_key: dict, consumed: set
) -> int:
    """Grow a repeated block while the next windows repeat at exactly the shifted locations."""
    length, limit = threshold, same_file_gap(locations)
    while length < limit:
        shift = length - threshold + 1
        shifted = tuple((file, start + shift) for file, start in locations)
        block = window_key.get(shifted[0])
        if block is None or groups[block] != shifted:
            break
        consumed.add(block)
        length += 1
    return length


def duplicate_candidates(
    sources: dict[str, list[str]], threshold: int, max_results: int
) -> tuple[list[dict], bool]:
    """Report maximal ordered blocks repeated across or within files.

    Windows of `threshold` substantive lines are indexed once. Consecutive windows that repeat
    at exactly the same set of locations are merged, so one long copy yields one candidate.
    """
    filtered = {
        file: meaningful_lines(lines, Path(file).suffix) for file, lines in sources.items()
    }
    blocks: dict[tuple[str, ...], list[tuple[str, int]]] = defaultdict(list)
    for file, rows in filtered.items():
        for start in range(len(rows) - threshold + 1):
            block = tuple(text for _, text in rows[start : start + threshold])
            if len(set(block)) >= 2:
                blocks[block].append((file, start))
    groups = {}
    for block, locations in blocks.items():
        kept = separated(locations, threshold)
        if len(kept) >= 2:
            groups[block] = kept
    window_key = {location: block for block, kept in groups.items() for location in kept}
    results, consumed = [], set()
    for block in sorted(groups, key=groups.get):
        if block in consumed:
            continue
        locations = groups[block]
        length = extend_match(locations, threshold, groups, window_key, consumed)
        if len(results) >= max_results:
            return results, True
        results.append(
            {
                "matched_nontrivial_lines": length,
                "locations": [
                    {
                        "file": file,
                        "start": filtered[file][start][0],
                        "end": filtered[file][start + length - 1][0],
                    }
                    for file, start in locations
                ],
            }
        )
    return results, False


def main() -> int:
    """Run read-only scans and report truncation or read failures as incomplete coverage."""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="mode", required=True)
    facts = subparsers.add_parser("facts")
    duplicates = subparsers.add_parser("duplicates")
    for command in (facts, duplicates):
        add_project_arguments(command)
        command.add_argument("--max-files", type=positive_int, default=10000)
        command.add_argument(
            "--include-dir",
            action="append",
            default=[],
            metavar="NAME",
            help="scan a directory name that is excluded by default (repeatable), e.g. build",
        )
    facts.add_argument("--output", choices=("json", "md"), default="json")
    duplicates.add_argument("--threshold", type=positive_int, default=6)
    duplicates.add_argument("--max-results", type=positive_int, default=200)
    duplicates.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be an existing directory")
    ignored = IGNORED_DIRS - set(args.include_dir)
    pruned: list[dict] = []
    files, warnings = scan_files(root, args.max_files, pruned, ignored)
    if args.mode == "facts":
        report = collect_facts(root, files, warnings, args.lang, pruned, ignored)
        if args.output == "md":
            print_text(markdown_report(report, "CodeSift facts"))
        else:
            print_report(report, True)
        return 0 if report["complete"] else 2
    units, _ = discover_units(root, files)
    languages = scan_languages(args.lang, detect_languages(root, files), units)
    decoded: list[dict] = []
    sources = read_sources(source_paths(files, languages), root, warnings, decoded)
    candidates, truncated = duplicate_candidates(
        sources, args.threshold, args.max_results
    )
    if truncated:
        warnings.append(
            "candidate output truncated; raise --max-results or narrow --root"
        )
    report = {
        "status": "completed" if not warnings else "incomplete",
        "complete": not warnings,
        "language": report_language(args.lang, languages),
        "source_files": len(sources),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "warnings": warnings,
        "evidence": "maximal ordered line-block matches within or across files; not semantic clones or a deletion recommendation",
        "coverage": coverage_section(ignored, pruned, decoded),
    }
    print_report(report, args.json)
    return 0 if report["complete"] else 2


if __name__ == "__main__":
    sys.exit(main())
