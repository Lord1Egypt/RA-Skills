"""Canonical skip-filter constants for ERPClaw manifest + integrity walks.

Single source of truth. Two consumers MUST use the constants from this module:

1. `release/regen_module_manifests.py` — when hashing source/<module>/ into the
   `files_sha256` manifest written to module_registry.json
2. `source/erpclaw/scripts/module_manager.py` — when walking an
   install-time delivered tree for integrity verification

If these two walks see different files, the integrity check fails as
"N extra files" or "N missing files" purely from filter divergence — a
class of bug that hit v4.2.1 (extracted into v4.2.3 as part of T1.3 in
PENDING_WORK_PLAN_2026-05-10.md).

ClawHub publish strips `tests/`, `.github/`, `bin/`, `.sig`, `.gitkeep`,
`.clawhubignore` at upload time. The manifest must match what ClawHub
actually ships, not what's in source/.
"""

# Directory names that should be skipped at any depth during the walk.
SKIP_DIRS = frozenset({
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "dist",
    "build",
    "tests",
    ".github",
    "bin",
})

# File-name suffixes that should be skipped.
SKIP_SUFFIXES = (".pyc", ".pyo", ".bak", ".tmp", ".DS_Store", ".sig")

# Exact file names that should be skipped (any directory).
SKIP_FILE_EXACT = frozenset({
    ".DS_Store",
    ".gitkeep",
    ".clawhubignore",
})


def should_skip(rel_path):
    """Convenience helper: True if a relative path matches the skip rules.

    rel_path: a "/"-separated relative path string. Returns True if any
    parent directory is in SKIP_DIRS, the filename is in SKIP_FILE_EXACT,
    or the filename ends with any SKIP_SUFFIXES entry.
    """
    parts = rel_path.split("/")
    if any(p in SKIP_DIRS for p in parts):
        return True
    fname = parts[-1]
    if fname in SKIP_FILE_EXACT:
        return True
    if fname.endswith(SKIP_SUFFIXES):
        return True
    return False
