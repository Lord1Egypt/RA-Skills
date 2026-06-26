"""
scripts/check_test_isolation.py — CI safety check for test isolation.

Fails (exit 1) if any test file references a hard-coded production path
such as ~/.friday-bp/ or .friday-bp/data.db.

Intentionally excluded from pattern matching:
  - Comment lines   (# ...)
  - Module, class, and function docstrings

String values in code ARE checked, because a literal like
``"~/.friday-bp/data.db"`` used as a value would bypass isolation.

Usage
-----
    python3 scripts/check_test_isolation.py

Exit codes
----------
    0 — No violations found
    1 — One or more violations found (printed to stdout)
"""

import ast
import io
import pathlib
import re
import sys
import tokenize

# Production-path patterns that should never appear in test code.
PATTERN = re.compile(r"~/\.friday-bp/|\.friday-bp/data\.db")

# Inline suppression comment — add ``# isolation-check: allow`` to a line
# to opt it out of this check (e.g. in meta-tests that reference the path
# intentionally).
SUPPRESS = re.compile(r"#\s*isolation-check:\s*allow")

violations: list[str] = []


def _docstring_lines(source: str) -> set[int]:
    """Return the set of 1-based line numbers that belong to a docstring node.

    Only module/class/function docstrings are excluded; regular string
    expressions elsewhere are *not* excluded.
    """
    docstring_lines: set[int] = set()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return docstring_lines

    for node in ast.walk(tree):
        if not isinstance(
            node,
            (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
        ):
            continue
        if not node.body:
            continue
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant):
            for lineno in range(first.lineno, (first.end_lineno or first.lineno) + 1):
                docstring_lines.add(lineno)

    return docstring_lines


def _comment_lines(source: str) -> set[int]:
    """Return 1-based line numbers for comment tokens."""
    comment_lines: set[int] = set()
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for tok_type, _tok_string, tok_start, _tok_end, _ in tokens:
            if tok_type == tokenize.COMMENT:
                comment_lines.add(tok_start[0])
    except tokenize.TokenError:
        pass
    return comment_lines


def _violations_in_file(filepath: pathlib.Path) -> list[tuple[int, str]]:
    source = filepath.read_text(encoding="utf-8")
    lines = source.splitlines()
    skip = _docstring_lines(source) | _comment_lines(source)

    hits: list[tuple[int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        if lineno not in skip and PATTERN.search(line) and not SUPPRESS.search(line):
            hits.append((lineno, line))
    return hits


for test_file in pathlib.Path("tests").rglob("*.py"):
    for lineno, line in _violations_in_file(test_file):
        violations.append(f"{test_file}:{lineno}: {line.strip()}")

if violations:
    print("Test isolation violations detected:")
    for v in violations:
        print(f"  {v}")
    sys.exit(1)

print("OK — no production paths in tests")
