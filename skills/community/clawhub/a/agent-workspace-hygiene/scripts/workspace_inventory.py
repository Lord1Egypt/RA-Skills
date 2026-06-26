#!/usr/bin/env python3
"""Read-only workspace inventory for the workspace-hygiene skill."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SAFE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".parcel-cache",
    ".turbo",
    ".nyc_output",
    "build",
    "coverage",
    "dist",
    "htmlcov",
    "test-results",
    "playwright-report",
}

REVIEW_DIR_NAMES = {
    "node_modules",
    ".venv",
    "venv",
    ".tox",
    ".nox",
    "data",
    "datasets",
}

SAFE_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".tmp",
    ".temp",
    ".bak",
    ".orig",
    ".rej",
    ".log",
}

REVIEW_SUFFIXES = {
    ".db",
    ".sqlite",
    ".sqlite3",
    ".duckdb",
    ".csv",
    ".tsv",
    ".xlsx",
    ".xls",
    ".docx",
    ".doc",
    ".pdf",
    ".pptx",
    ".ipynb",
    ".zip",
    ".7z",
    ".rar",
    ".tar",
    ".gz",
    ".parquet",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
}

PROTECTED_NAMES = {
    ".git",
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "id_rsa",
    "id_ed25519",
}

PROTECTED_PREFIXES = (
    ".git/",
    ".codex/skills/",
)

ACTION_ORDER = {
    "safe_to_remove_or_archive": 0,
    "review_before_archive": 1,
    "skip_protected": 2,
}

ACTION_SEQUENCE = tuple(ACTION_ORDER)


@dataclass
class Candidate:
    path: str
    kind: str
    action: str
    reason: str
    size_bytes: int
    size_status: str
    modified_utc: str | None
    git_status: str


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def run_git(root: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout


def git_status_map(root: Path) -> tuple[bool, dict[str, str]]:
    output = run_git(root, ["status", "--ignored", "--porcelain=v1"])
    if output is None:
        return False, {}
    statuses: dict[str, str] = {}
    for line in output.splitlines():
        if len(line) < 4:
            continue
        code = line[:2]
        path = line[3:]
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[-1]
        statuses[path.replace("\\", "/")] = code
    return True, statuses


def tracked_files(root: Path) -> set[str]:
    output = run_git(root, ["ls-files", "-z"])
    if output is None:
        return set()
    return {item for item in output.split("\0") if item}


def has_tracked_under(prefix: str, tracked: set[str]) -> bool:
    prefix = prefix.rstrip("/") + "/"
    return any(path == prefix[:-1] or path.startswith(prefix) for path in tracked)


def is_protected(rel: str, name: str) -> bool:
    lower_name = name.lower()
    lower_rel = rel.lower()
    if lower_name in PROTECTED_NAMES:
        return True
    if lower_rel == ".codex/skills":
        return True
    if any(lower_rel.startswith(prefix) for prefix in PROTECTED_PREFIXES):
        return True
    if any(word in lower_name for word in ("secret", "credential", "private_key")):
        return True
    return (
        lower_name == "token"
        or lower_name.startswith("token.")
        or lower_name.endswith(".token")
        or "_token" in lower_name
        or "-token" in lower_name
    )


def file_size(path: Path) -> tuple[int, str]:
    try:
        return path.stat().st_size, "exact"
    except OSError:
        return 0, "unknown"


def dir_size(path: Path, max_files: int = 2000) -> tuple[int, str]:
    total = 0
    seen = 0
    for current, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git"}]
        for filename in files:
            seen += 1
            if seen > max_files:
                return total, "partial"
            size, _ = file_size(Path(current) / filename)
            total += size
    return total, "exact"


def modified_utc(path: Path) -> str | None:
    try:
        stamp = path.stat().st_mtime
    except OSError:
        return None
    return datetime.fromtimestamp(stamp, tz=timezone.utc).isoformat()


def is_recent(path: Path, recent_hours: int) -> bool:
    if recent_hours <= 0:
        return False
    try:
        stamp = path.stat().st_mtime
    except OSError:
        return False
    cutoff = datetime.now(timezone.utc).timestamp() - (recent_hours * 3600)
    return stamp >= cutoff


def make_candidate(path: Path, root: Path, kind: str, action: str, reason: str, status: str, measure: bool = True) -> Candidate:
    if not measure:
        size_bytes, size_status = 0, "skipped"
    elif kind == "directory":
        size_bytes, size_status = dir_size(path)
    else:
        size_bytes, size_status = file_size(path)
    return Candidate(
        relpath(path, root),
        kind,
        action,
        reason,
        size_bytes,
        size_status,
        modified_utc(path),
        status,
    )


def status_for(rel: str, statuses: dict[str, str]) -> str:
    if rel in statuses:
        return statuses[rel]
    prefix = rel.rstrip("/") + "/"
    child_codes = {code for path, code in statuses.items() if path.startswith(prefix)}
    if not child_codes:
        return ""
    if child_codes == {"!!"}:
        return "!!"
    if child_codes == {"??"}:
        return "??"
    return "mixed"


def classify_dir(path: Path, root: Path, status: str, tracked: set[str], in_git: bool) -> Candidate | None:
    rel = relpath(path, root)
    name = path.name
    if is_protected(rel, name):
        return make_candidate(path, root, "directory", "skip_protected", "protected path", status, measure=False)
    if name in SAFE_DIR_NAMES or rel.endswith("/.next/cache") or rel.endswith("/node_modules/.cache"):
        if in_git and has_tracked_under(rel, tracked):
            return make_candidate(path, root, "directory", "review_before_archive", "generated-looking directory contains tracked files", status)
        return make_candidate(path, root, "directory", "safe_to_remove_or_archive", "generated cache or build/test output", status)
    if name in REVIEW_DIR_NAMES:
        return make_candidate(path, root, "directory", "review_before_archive", "dependency, data, or environment directory", status)
    return None


def classify_file(path: Path, root: Path, status: str, in_git: bool, recent_hours: int) -> Candidate | None:
    rel = relpath(path, root)
    name = path.name
    suffix = path.suffix.lower()
    if is_protected(rel, name):
        return make_candidate(path, root, "file", "skip_protected", "secret-looking or protected file", status)
    if in_git and status not in {"??", "!!"}:
        return None
    if name == ".coverage" or suffix in SAFE_FILE_SUFFIXES:
        if not in_git:
            return make_candidate(path, root, "file", "review_before_archive", "temporary-looking file; git status unavailable", status)
        if is_recent(path, recent_hours):
            return make_candidate(path, root, "file", "review_before_archive", "temporary-looking file modified recently", status)
        return make_candidate(path, root, "file", "safe_to_remove_or_archive", "temporary, log, cache, or rejected patch file", status)
    if suffix in REVIEW_SUFFIXES or rel.startswith("data/"):
        return make_candidate(path, root, "file", "review_before_archive", "data, document, report, image, archive, or local database", status)
    if status == "??":
        return make_candidate(path, root, "file", "review_before_archive", "untracked file with unclear provenance", status)
    if status == "!!":
        if is_recent(path, recent_hours):
            return make_candidate(path, root, "file", "review_before_archive", "ignored file modified recently", status)
        return make_candidate(path, root, "file", "safe_to_remove_or_archive", "ignored generated file", status)
    return None


def sort_candidates(items: list[Candidate]) -> list[Candidate]:
    return sorted(items, key=lambda item: (ACTION_ORDER.get(item.action, 99), -item.size_bytes, item.path))


def limit_by_bucket(groups: dict[str, list[Candidate]], max_entries: int) -> list[Candidate]:
    if max_entries <= 0:
        return []
    non_empty_actions = [action for action in ACTION_SEQUENCE if groups.get(action)]
    if not non_empty_actions:
        return []
    per_bucket = max(1, max_entries // len(non_empty_actions))
    selected: list[Candidate] = []
    leftovers: list[Candidate] = []
    for action in ACTION_SEQUENCE:
        items = groups.get(action, [])
        selected.extend(items[:per_bucket])
        leftovers.extend(items[per_bucket:])
    remaining = max_entries - len(selected)
    if remaining > 0:
        selected.extend(sort_candidates(leftovers)[:remaining])
    return selected[:max_entries]


def inventory(root: Path, max_entries: int, max_files: int, recent_hours: int) -> dict:
    root = root.resolve()
    in_git, statuses = git_status_map(root)
    tracked = tracked_files(root) if in_git else set()
    candidates: list[Candidate] = []
    scanned_files = 0
    truncated = False

    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        rel_current = "" if current_path == root else relpath(current_path, root)
        if rel_current.startswith(".git"):
            dirs[:] = []
            continue

        kept_dirs = []
        for dirname in dirs:
            dir_path = current_path / dirname
            rel = relpath(dir_path, root)
            status = status_for(rel, statuses)
            candidate = classify_dir(dir_path, root, status, tracked, in_git)
            if candidate:
                candidates.append(candidate)
                if candidate.action in {"safe_to_remove_or_archive", "review_before_archive", "skip_protected"}:
                    continue
            kept_dirs.append(dirname)
        dirs[:] = kept_dirs

        for filename in files:
            scanned_files += 1
            if scanned_files > max_files:
                truncated = True
                break
            file_path = current_path / filename
            rel = relpath(file_path, root)
            candidate = classify_file(file_path, root, status_for(rel, statuses), in_git, recent_hours)
            if candidate:
                candidates.append(candidate)
        if truncated:
            break

    safe = sorted([item for item in candidates if item.action == "safe_to_remove_or_archive"], key=lambda item: (-item.size_bytes, item.path))
    review = sorted([item for item in candidates if item.action == "review_before_archive"], key=lambda item: (-item.size_bytes, item.path))
    protected = sorted([item for item in candidates if item.action == "skip_protected"], key=lambda item: (-item.size_bytes, item.path))
    groups = {
        "safe_to_remove_or_archive": safe,
        "review_before_archive": review,
        "skip_protected": protected,
    }

    def total(items: Iterable[Candidate]) -> int:
        return sum(item.size_bytes for item in items)

    intervention = "no_intervention_needed"
    if safe or review:
        intervention = "prompt_cleanup_recommended"

    return {
        "root": str(root),
        "git_detected": in_git,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "truncated": truncated,
        "scanned_files": scanned_files,
        "quality": {
            "intervention": intervention,
            "reason": "cleanup candidates found" if intervention != "no_intervention_needed" else "no cleanup candidates found",
        },
        "summary": {
            "safe_count": len(safe),
            "safe_size_bytes": total(safe),
            "review_count": len(review),
            "review_size_bytes": total(review),
            "protected_count": len(protected),
            "partial_size_count": len([item for item in candidates if item.size_status == "partial"]),
        },
        "top_candidates": {
            action: [asdict(item) for item in groups[action][:3]]
            for action in ACTION_SEQUENCE
        },
        "candidates": [asdict(item) for item in limit_by_bucket(groups, max_entries)],
    }


def human_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{size} B"


def print_report(data: dict) -> None:
    summary = data["summary"]
    print("Workspace cleanup plan")
    print(f"Root: {data['root']}")
    print(f"Safe candidates: {summary['safe_count']}, {human_size(summary['safe_size_bytes'])}")
    print(f"Needs review: {summary['review_count']}, {human_size(summary['review_size_bytes'])}")
    print(f"Skipped/protected: {summary['protected_count']}")
    if summary.get("partial_size_count"):
        print(f"Note: {summary['partial_size_count']} directory size value(s) are partial.")
    if data["truncated"]:
        print("Note: scan was truncated; rerun with a higher --max-files for a full inventory.")
    for action, title in (
        ("safe_to_remove_or_archive", "Safe to remove or archive"),
        ("review_before_archive", "Needs user review"),
        ("skip_protected", "Protected or skipped"),
    ):
        items = [item for item in data["candidates"] if item["action"] == action]
        if not items:
            continue
        print("")
        print(title + ":")
        for item in items[:20]:
            size_note = "" if item.get("size_status") == "exact" else f", {item.get('size_status')}"
            print(f"- {item['path']} ({human_size(item['size_bytes'])}{size_note}): {item['reason']}")


def summary_payload(data: dict) -> dict:
    return {
        "root": data["root"],
        "git_detected": data["git_detected"],
        "generated_at_utc": data["generated_at_utc"],
        "truncated": data["truncated"],
        "scanned_files": data["scanned_files"],
        "quality": data["quality"],
        "summary": data["summary"],
        "top_candidates": data["top_candidates"],
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Read-only workspace cleanup inventory.")
    parser.add_argument("--root", default=".", help="Workspace root to inspect.")
    parser.add_argument("--summary-json", action="store_true", help="Print compact JSON output.")
    parser.add_argument("--details-json", action="store_true", help="Print detailed JSON output.")
    parser.add_argument("--report", action="store_true", help="Print a human-readable report.")
    parser.add_argument("--max-entries", type=int, default=80, help="Maximum candidate entries to include.")
    parser.add_argument("--max-files", type=int, default=50000, help="Maximum files to scan before truncating.")
    parser.add_argument("--recent-hours", type=int, default=24, help="Downgrade recently modified generated-looking files to review.")
    args = parser.parse_args(argv)

    data = inventory(Path(args.root), args.max_entries, args.max_files, args.recent_hours)
    if args.report:
        print_report(data)
    elif args.summary_json:
        print(json.dumps(summary_payload(data), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False if args.summary_json else True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
