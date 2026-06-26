#!/usr/bin/env python3
"""
check_skill_md_sync.py
~~~~~~~~~~~~~~~~~~~~~~
Verify that every @mcp.tool in server/main.py is documented in SKILL.md and
vice-versa.  Exits 0 when in sync; exits 1 with a diff when not.

Usage:
    python3 scripts/check_skill_md_sync.py        # from repo root
"""

import ast
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths (relative to repo root)
# ---------------------------------------------------------------------------
MAIN_PY = Path("server/main.py")
SKILL_MD = Path("SKILL.md")

# ---------------------------------------------------------------------------
# Names that appear in SKILL.md for reasons other than being MCP tools
# (e.g. code-block examples, prose references).  Add here if the regex
# produces false positives.
# ---------------------------------------------------------------------------
# Parameter/value names that appear as bullet items in SKILL.md docs
# but are not MCP tool names.
SKILL_MD_IGNORE: set[str] = {
    "home_currency",  # parameter value of set_setting/get_setting
    "timezone",  # parameter value of set_setting/get_setting
}


def get_mcp_tools_in_code() -> set[str]:
    """Return the set of function names decorated with @mcp.tool in main.py."""
    src = MAIN_PY.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(MAIN_PY))
    tools: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for dec in node.decorator_list:
                d_str = ast.unparse(dec) if hasattr(ast, "unparse") else ""
                if "mcp.tool" in d_str:
                    tools.append(node.name)
                    break
    return set(tools)


def get_mcp_tools_in_skill_md() -> set[str]:
    """
    Extract tool names referenced in the MCP-tools section of SKILL.md.

    Recognises two list-item patterns used throughout the file:
      - `tool_name`        (no-arg tools, e.g. ``- `sync` — …``)
      - `tool_name(…`      (tools with parameters,  e.g. ``- `list(filters?)` — …``)

    Only lines that start with "- `" are considered to avoid picking up inline
    mentions in prose or code examples.
    """
    text = SKILL_MD.read_text(encoding="utf-8")
    found: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        # Must be a bullet-list item starting with a backtick-quoted identifier
        m = re.match(r"^- `([a-z_][a-z0-9_]*)(?:\(|`)", stripped)
        if m:
            found.add(m.group(1))
    return found - SKILL_MD_IGNORE


def main() -> None:
    if not MAIN_PY.exists():
        print(f"ERROR: {MAIN_PY} not found — run from repo root.", file=sys.stderr)
        sys.exit(2)
    if not SKILL_MD.exists():
        print(f"ERROR: {SKILL_MD} not found — run from repo root.", file=sys.stderr)
        sys.exit(2)

    in_code = get_mcp_tools_in_code()
    in_doc = get_mcp_tools_in_skill_md()

    missing_doc = in_code - in_doc  # in code but not documented
    missing_code = in_doc - in_code  # documented but not in code

    if missing_doc:
        print("❌  Tools in server/main.py but MISSING from SKILL.md:")
        for t in sorted(missing_doc):
            print(f"     - {t}")

    if missing_code:
        print("❌  Tools in SKILL.md but NOT FOUND in server/main.py")
        print("    (renamed or deleted without updating the docs?):")
        for t in sorted(missing_code):
            print(f"     - {t}")

    if missing_doc or missing_code:
        sys.exit(1)

    print(f"✅  OK — {len(in_code)} MCP tools, all documented in SKILL.md")


if __name__ == "__main__":
    main()
