"""
CI lint preventing local-network-only violation.

Scans server/**/*.py and ui/**/*.py (if present) for any code that binds to
0.0.0.0 or an empty host, which would expose the service on all interfaces.
Per Design Constraint #6, all network binds must be restricted to 127.0.0.1.

These tests are meant to fail fast in CI if a developer accidentally introduces
a public bind, not to test runtime behaviour.
"""

import re
from pathlib import Path

# Patterns that indicate a public or empty-host bind
FORBIDDEN_PATTERNS = [
    re.compile(r"0\.0\.0\.0"),
    re.compile(r'host\s*=\s*["\'](\s*|0\.0\.0\.0)["\']'),
    re.compile(r'bind\(\s*\(\s*["\'](\s*|0\.0\.0\.0)["\']'),
]

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_GLOBS = ["server/**/*.py", "ui/**/*.py"]


def _collect_files() -> list[Path]:
    files = []
    for pattern in SCAN_GLOBS:
        files.extend(REPO_ROOT.glob(pattern))
    return files


def _check_file(path: Path) -> list[tuple[int, str]]:
    """Return list of (line_number, line) pairs that match a forbidden pattern."""
    offences = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.lstrip()
        if line.startswith("#"):
            continue  # pure comment — skip
        for pat in FORBIDDEN_PATTERNS:
            if pat.search(raw):
                offences.append((lineno, raw))
                break  # report line once even if multiple patterns match
    return offences


def test_no_public_bind_in_server_and_ui():
    """No non-test Python file in server/ or ui/ may bind to 0.0.0.0 or empty host."""
    files = _collect_files()
    all_offences: dict[str, list[tuple[int, str]]] = {}

    for fpath in files:
        # Skip test files themselves
        if fpath.name.startswith("test_"):
            continue
        offences = _check_file(fpath)
        if offences:
            all_offences[str(fpath.relative_to(REPO_ROOT))] = offences

    if all_offences:
        lines = ["Public bind detected — must use 127.0.0.1 (Design Constraint #6):"]
        for fname, hits in all_offences.items():
            for lineno, text in hits:
                lines.append(f"  {fname}:{lineno}: {text.rstrip()}")
        raise AssertionError("\n".join(lines))
