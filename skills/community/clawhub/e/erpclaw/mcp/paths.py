"""ERPCLAW_HOME resolution for the MCP server (ADR-0017 backward-compat contract).

The MCP server is spawned on demand from the source tree, *before* the installed
``erpclaw_lib`` is guaranteed to be on ``sys.path``. The canonical resolver is
``erpclaw_lib.paths`` (ADR-0017); this module reproduces its logic inline so the
server can resolve the install root with zero pre-bootstrap import dependency —
exactly the pattern ``source/erpclaw/scripts/db_query.py`` uses for the same
reason. When the installed lib *is* importable the two agree byte-for-byte; the
L0 selftest pins that equivalence.

``ERPCLAW_HOME`` is a *defaulting* variable: unset ⇒ ``~/.openclaw/erpclaw``
expanded, byte-identical to today's OpenClaw installs. There is exactly one var,
resolved once here, consumed by every tool.
"""
import os

# Mirrors erpclaw_lib.paths._DEFAULT_HOME and the db_query.py router literal.
_DEFAULT_HOME = "~/.openclaw/erpclaw"


def erpclaw_home() -> str:
    """Resolve the ERPClaw install root.

    Returns ``$ERPCLAW_HOME`` (expanduser-normalized) when set, else
    ``~/.openclaw/erpclaw`` expanded. With ERPCLAW_HOME unset this equals
    ``os.path.expanduser("~/.openclaw/erpclaw")`` byte-for-byte.
    """
    return os.path.expanduser(os.environ.get("ERPCLAW_HOME", _DEFAULT_HOME))


def lib_dir() -> str:
    """Path to the installed shared-lib dir (the ``sys.path.insert`` target)."""
    return os.path.join(erpclaw_home(), "lib")


def db_path() -> str:
    """Default SQLite DB path under the install root."""
    return os.path.join(erpclaw_home(), "data.sqlite")


def skill_md_path() -> str:
    """Path to the installed foundation SKILL.md (discovery source, ADR-0024 §5).

    Installs lay the foundation SKILL.md at the install root. The source-tree
    copy (``source/erpclaw/SKILL.md``) is the fallback when running uninstalled
    from the tree (e.g. the L0 unit tests + the Mac dev loop).
    """
    return os.path.join(erpclaw_home(), "SKILL.md")
