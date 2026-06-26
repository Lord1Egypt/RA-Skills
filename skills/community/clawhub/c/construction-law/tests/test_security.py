"""
Security guardrail test for all runtime scripts.

Uses ast.parse to walk the syntax tree of every .py file in scripts/,
catching forbidden imports and calls regardless of whitespace, aliasing,
or formatting — without false-positiving on comments, docstrings, or
strings.

Enforces the "no network / no external process / no dynamic code loading"
claim in SKILL.md.

Run:
    python3 -m unittest tests.test_security
    python3 -m pytest tests/test_security.py
"""

import ast
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

# Top-level modules that must never be imported
FORBIDDEN_MODULES = {
    "subprocess", "socket", "requests", "httpx", "aiohttp",
    "importlib", "pickle", "marshal",
}

# Dotted imports: "from urllib.request import ..." etc.
FORBIDDEN_DOTTED = {
    "urllib.request", "urllib.error",
    "http.client", "http.server",
}

# Bare dangerous built-in calls
FORBIDDEN_CALLS = {"exec", "eval", "compile"}

# Attribute calls: os.system(), pickle.loads(), etc.
FORBIDDEN_ATTR_CALLS = {
    ("os", "system"),
    ("pickle", "loads"),
    ("marshal", "loads"),
    ("importlib", "import_module"),
}


def _scan_file(py_file):
    """Parse a single .py file and return a list of violation strings."""
    with open(py_file, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=str(py_file))
    violations = []
    name = py_file.name

    for node in ast.walk(tree):
        # import X / import X as Y
        if isinstance(node, ast.Import):
            for alias in node.names:
                top = alias.name.split(".")[0]
                if top in FORBIDDEN_MODULES or alias.name in FORBIDDEN_DOTTED:
                    violations.append(
                        f"  {name}:L{node.lineno}: import {alias.name}"
                    )
        # from X import Y
        elif isinstance(node, ast.ImportFrom) and node.module:
            top = node.module.split(".")[0]
            if top in FORBIDDEN_MODULES or node.module in FORBIDDEN_DOTTED:
                violations.append(
                    f"  {name}:L{node.lineno}: from {node.module} import ..."
                )
        # function calls
        elif isinstance(node, ast.Call):
            func = node.func
            # bare dangerous call
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                violations.append(
                    f"  {name}:L{node.lineno}: {func.id}() call"
                )
            # attribute call: os.system(...), pickle.loads(...), etc.
            elif (isinstance(func, ast.Attribute)
                  and isinstance(func.value, ast.Name)):
                pair = (func.value.id, func.attr)
                if pair in FORBIDDEN_ATTR_CALLS:
                    violations.append(
                        f"  {name}:L{node.lineno}: "
                        f"{func.value.id}.{func.attr}() call"
                    )

    return violations


class TestNoForbiddenImports(unittest.TestCase):
    """Enforce the 'stdlib-only, no network, no subprocess' security claim."""

    def test_all_scripts_clean(self):
        violations = []
        for py_file in sorted(SCRIPTS_DIR.glob("*.py")):
            violations.extend(_scan_file(py_file))

        self.assertEqual(
            violations, [],
            "Forbidden import/call found in scripts/:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
