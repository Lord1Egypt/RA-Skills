"""
Driftwatch — Workspace Hygiene Checks
Scans workspace root for common hygiene issues:
  - Duplicate memory files (MEMORY.md vs memory.md as independent files)
  - Empty bootstrap files (0 bytes)
  - Missing bootstrap files
  - Missing subagent files
  - Extra markdown files not in bootstrap order
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from references.constants import (
    BOOTSTRAP_FILE_ORDER,
    SUBAGENT_FILES,
)

KNOWN_SUBDIRS = {"skills", "memory", "projects", "specs", "subagents"}


def analyze_hygiene(workspace_path: str) -> dict:
    findings = []

    # --- Check 1: Duplicate memory files ---
    memory_upper = os.path.join(workspace_path, "MEMORY.md")
    memory_lower = os.path.join(workspace_path, "memory.md")

    upper_is_real = os.path.exists(memory_upper) and not os.path.islink(memory_upper)
    lower_is_real = os.path.exists(memory_lower) and not os.path.islink(memory_lower)

    if upper_is_real and lower_is_real:
        findings.append({
            "check": "duplicate_memory",
            "severity": "critical",
            "message": (
                "Both MEMORY.md and memory.md exist as independent files — "
                "both will be injected, silently doubling memory budget consumption"
            ),
            "files": ["MEMORY.md", "memory.md"],
        })

    # --- Check 2: Empty bootstrap files ---
    empty_files = []
    for filename in BOOTSTRAP_FILE_ORDER:
        path = os.path.join(workspace_path, filename)
        if os.path.exists(path) and not os.path.islink(path):
            if os.path.getsize(path) == 0:
                empty_files.append(filename)

    for filename in empty_files:
        findings.append({
            "check": "empty_bootstrap",
            "severity": "warning",
            "message": (
                f"{filename} exists but is empty (0 chars) — "
                "consuming a bootstrap slot without providing instructions"
            ),
            "files": [filename],
        })

    # --- Check 3: Missing bootstrap files ---
    for filename in BOOTSTRAP_FILE_ORDER:
        path = os.path.join(workspace_path, filename)
        if not os.path.exists(path):
            findings.append({
                "check": "missing_bootstrap",
                "severity": "info",
                "message": (
                    f"{filename} not found in workspace — "
                    "not contributing to bootstrap context"
                ),
                "files": [filename],
            })

    # --- Check 4: Missing subagent files ---
    for filename in SUBAGENT_FILES:
        path = os.path.join(workspace_path, filename)
        if not os.path.exists(path):
            findings.append({
                "check": "missing_subagent",
                "severity": "warning",
                "message": (
                    f"{filename} is missing — this file is injected into all subagent sessions "
                    "and is required for proper delegation"
                ),
                "files": [filename],
            })

    # --- Check 5: Extra markdown files in workspace root ---
    bootstrap_set = set(BOOTSTRAP_FILE_ORDER)
    extra_md = []

    try:
        entries = os.listdir(workspace_path)
    except OSError:
        entries = []

    for entry in sorted(entries):
        if not entry.lower().endswith(".md"):
            continue
        entry_path = os.path.join(workspace_path, entry)
        # Only look at files (real or symlink) directly in root — not subdirs
        if not os.path.isfile(entry_path):
            continue
        if entry in bootstrap_set:
            continue
        # Check if file is in a known subdir (it's in root, so this doesn't apply,
        # but guard against any oddly-named .md that matches a subdir name)
        if entry.lower() in KNOWN_SUBDIRS:
            continue
        extra_md.append(entry)

    # Filter out files already flagged by duplicate_memory
    duplicate_flagged = set()
    for f in findings:
        if f.get("check") == "duplicate_memory":
            duplicate_flagged.update(f.get("files", []))
    extra_md = [f for f in extra_md if f not in duplicate_flagged]

    if extra_md:
        findings.append({
            "check": "extra_files",
            "severity": "info",
            "message": (
                f"{len(extra_md)} markdown file(s) in workspace root are not in the "
                "bootstrap loading order and won't be injected into context: "
                + ", ".join(extra_md)
            ),
            "files": extra_md,
        })

    return {
        "checks_run": [
            "duplicate_memory",
            "empty_bootstrap",
            "missing_bootstrap",
            "missing_subagent",
            "extra_files",
        ],
        "findings": findings,
    }
