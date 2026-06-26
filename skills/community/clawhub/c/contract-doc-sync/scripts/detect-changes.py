#!/usr/bin/env python3
"""
detect-changes.py — Parse git diff output to classify file changes and output a JSON report.

Usage:
    python3 detect-changes.py [--base <commit|branch>] [--staged]
"""

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Category classification rules (order matters — first match wins)
# ---------------------------------------------------------------------------
CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("controller", ["controller/", "Controller.java"]),
    ("facade", ["facade/", "Facade.java", "FacadeImpl.java"]),
    ("service", ["service/", "Service.java", "ServiceImpl.java"]),
    ("repository", ["repository/", "Mapper.java", "Repository.java"]),
    (
        "entity",
        [
            "entity/",
            "DO.java",
            "VO.java",
            "Request.java",
            "Result.java",
            "DTO.java",
        ],
    ),
    (
        "config",
        [
            "config/",
            "Configuration.java",
            "Properties.java",
            ".yaml",
            ".yml",
            ".properties",
        ],
    ),
    ("client", ["clients/", "Client.java"]),
    (
        "common",
        [
            "common/",
            "CommonErrorCode",
            "BaseException",
            "BizException",
        ],
    ),
    ("shared", ["shared/"]),
    ("docs", ["docs/"]),
    ("pom", ["pom.xml"]),
    ("scripts", ["scripts/"]),
]

# ---------------------------------------------------------------------------
# docTargets mapping per category
# ---------------------------------------------------------------------------
DOC_TARGETS: dict[str, list[str]] = {
    "controller": ["api-reference"],
    "facade": ["api-reference", "technical-design"],
    "service": ["technical-design"],
    "repository": ["technical-design"],
    "entity": ["technical-design", "class-diagram"],
    "config": ["configuration-reference"],
    "client": ["client-docs"],
    "common": ["error-handling"],
    "shared": ["technical-design"],
    "docs": ["self-referential"],
    "pom": ["system-overview", "version-table"],
    "scripts": [],
    "other": [],
}

# Human-readable impact descriptions for each doc target
_DOC_IMPACT_DESCRIPTIONS: dict[str, str] = {
    "api-reference": "controller changes require API doc review",
    "technical-design": "service/repository/facade changes require technical design update",
    "class-diagram": "entity changes require class diagram update",
    "configuration-reference": "config changes require configuration reference update",
    "client-docs": "client changes require client documentation update",
    "error-handling": "common exception changes require error-handling doc update",
    "self-referential": "documentation changes are self-referential",
    "system-overview": "pom changes may affect system overview",
    "version-table": "pom changes may affect version table",
}


def classify_file(path: str) -> str:
    """Return the category for *path* based on pattern matching."""
    for category, patterns in CATEGORY_RULES:
        for pat in patterns:
            if pat in path:
                return category
    return "other"


def get_doc_targets(category: str) -> list[str]:
    return list(DOC_TARGETS.get(category, []))


def extract_module(path: str) -> str:
    """Extract the Maven module name from a file path.

    Examples:
        app/src/main/java/... → app
        common/src/main/java/... → common
        clients/client-cache/src/... → clients/client-cache
    """
    parts = Path(path).parts
    # Module is everything up to (but not including) 'src'
    module_parts: list[str] = []
    for p in parts:
        if p == "src":
            break
        module_parts.append(p)
    return "/".join(module_parts) if module_parts else path


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------
def run_git(*args: str, cwd: str | None = None) -> str:
    """Run a git command and return stripped stdout."""
    try:
        result = subprocess.run(
            ["git"] + list(args),
            capture_output=True,
            text=True,
            cwd=cwd,
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except FileNotFoundError:
        print("Error: git not found in PATH", file=sys.stderr)
        sys.exit(1)


def get_base_commit(cwd: str | None) -> str | None:
    """Return the short hash of HEAD~1, or None if unavailable."""
    out = run_git("rev-parse", "--short", "HEAD~1", cwd=cwd)
    return out if out else None


def get_changed_files(base: str | None, staged: bool, cwd: str | None) -> list[dict]:
    """Return a list of changed file dicts with 'path' and 'status' keys."""
    if staged:
        out = run_git("diff", "--name-status", "--cached", cwd=cwd)
    elif base:
        out = run_git("diff", "--name-status", base, cwd=cwd)
    else:
        # Fallback: staged changes
        out = run_git("diff", "--name-status", "--cached", cwd=cwd)

    if not out:
        return []

    files: list[dict] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        # git diff --name-status lines look like:
        #   M       path/to/file
        #   A       path/to/file
        #   D       path/to/file
        #   R100    old/path  new/path   (rename, we take the new path)
        parts = line.split("\t")
        status = parts[0][0]  # first character: M, A, D, R, C
        if status == "R":
            # Rename: parts = ["R100", "old_path", "new_path"]
            path = parts[-1] if len(parts) > 2 else parts[1]
            status = "M"  # treat renames as modifications
        elif status == "C":
            # Copy: parts = ["C100", "old_path", "new_path"]
            path = parts[-1] if len(parts) > 2 else parts[1]
            status = "A"  # treat copies as additions
        else:
            path = parts[1] if len(parts) > 1 else parts[0]

        # Normalize status to A/M/D
        if status not in ("A", "M", "D"):
            status = "M"  # unknown statuses treated as modifications

        files.append({"path": path, "status": status})
    return files


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify git changes by category and produce a JSON report."
    )
    parser.add_argument(
        "--base",
        default=None,
        help="Base commit or branch to diff against (default: HEAD~1).",
    )
    parser.add_argument(
        "--staged",
        action="store_true",
        default=False,
        help="Check staged (cached) changes instead of diffing against a commit.",
    )
    args = parser.parse_args()

    cwd = os.getcwd()

    # Determine base commit
    base = args.base
    if not args.staged and base is None:
        base = get_base_commit(cwd)
        if base is None:
            print(
                "Warning: HEAD~1 not available (shallow history or no previous commit). "
                "Falling back to staged changes.",
                file=sys.stderr,
            )
            args.staged = True

    # Resolve full commit hash for the report
    base_commit = ""
    if not args.staged and base:
        base_commit = run_git("rev-parse", "--short", base, cwd=cwd) or base

    # Get changed files
    changed_files = get_changed_files(base, args.staged, cwd)

    # Classify each file
    by_category: Counter = Counter()
    by_module: Counter = Counter()
    by_status: Counter = Counter()
    doc_targets_per_target: defaultdict[str, list[str]] = defaultdict(list)

    for entry in changed_files:
        path = entry["path"]
        status = entry["status"]
        category = classify_file(path)
        module = extract_module(path)
        doc_targets = get_doc_targets(category)

        entry["category"] = category
        entry["module"] = module
        entry["docTargets"] = doc_targets

        by_category[category] += 1
        by_module[module] += 1
        by_status[status] += 1

        for target in doc_targets:
            doc_targets_per_target[target].append(
                _DOC_IMPACT_DESCRIPTIONS.get(
                    target, f"{category} changes affect {target}"
                )
            )

    # Deduplicate impact descriptions per target
    doc_impact: dict[str, list[str]] = {}
    for target, descriptions in doc_targets_per_target.items():
        seen: set[str] = set()
        unique: list[str] = []
        for desc in descriptions:
            if desc not in seen:
                seen.add(desc)
                unique.append(desc)
        doc_impact[target] = unique

    report = {
        "baseCommit": base_commit,
        "changedFiles": changed_files,
        "summary": {
            "total": len(changed_files),
            "byCategory": dict(by_category),
            "byModule": dict(by_module),
            "byStatus": dict(by_status),
        },
        "docImpact": doc_impact,
    }

    json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
    print()  # trailing newline


if __name__ == "__main__":
    main()
