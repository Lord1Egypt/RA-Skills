"""Discovery: enumerate foundation actions + their metadata for the meta-tools.

ADR-0024 §5 makes SKILL.md / the action ACTIONS dicts the discovery source,
tied to the L0 ``test_skillmd_action_completeness`` invariant. To avoid a second
parser that can drift from that gate (SIM-0c), this module extracts action names
the *same* way the L0 gate does — AST over the ``ACTIONS = {...}`` /
``<DOMAIN>_ACTIONS = {...}`` dict literals in the foundation scripts. Descriptions
come from the SKILL.md catalog tables; the destructive flag comes from the
router's own ``DANGEROUS_ACTIONS`` frozenset (the single source of truth the
router gate uses), so the MCP layer can never disagree with the router about
what is gated.

v1 scope is foundation-only (Nik D3). The public surface accepts a ``module``
argument and ignores anything but foundation for now; all-module aggregation
across ``module_registry.json`` is later config, not a redesign.
"""
import ast
import os
import re
from functools import lru_cache

# The foundation source root: this file lives at source/erpclaw/mcp/, so the
# foundation module dir is its parent.
_FOUNDATION_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS_DIR = os.path.join(_FOUNDATION_DIR, "scripts")
_ROUTER_PATH = os.path.join(_SCRIPTS_DIR, "db_query.py")
_SOURCE_SKILL_MD = os.path.join(_FOUNDATION_DIR, "SKILL.md")


def _is_router_target(t):
    return isinstance(t, ast.Name) and (t.id == "ACTIONS" or t.id.endswith("_ACTIONS"))


@lru_cache(maxsize=1)
def _foundation_action_names() -> frozenset:
    """AST-extract every action key from the foundation's own ACTIONS dicts.

    Mirrors testing/unit/constitution/test_skillmd_completeness._extract_python_actions
    so discovery == the L0 completeness set. Sub-module dirs that have their own
    SKILL.md own their own actions and are excluded (foundation scope, Nik D3).
    """
    # Sub-modules under source/ with their own SKILL.md own their own actions.
    submodule_dirs = set()
    for root, dirs, files in os.walk(_SCRIPTS_DIR):
        dirs[:] = [d for d in dirs if d != "__pycache__" and d != "tests"]
        # A scripts subtree that is itself a module (has SKILL.md alongside a
        # scripts/ dir) is excluded — but foundation domain dirs do NOT have
        # their own SKILL.md, so this is a no-op for the foundation tree and a
        # safety net if that ever changes.
        if "SKILL.md" in files and root != _FOUNDATION_DIR:
            submodule_dirs.add(os.path.abspath(root))

    actions = set()
    for root, dirs, files in os.walk(_SCRIPTS_DIR):
        dirs[:] = [
            d for d in dirs
            if d != "__pycache__" and d != "tests"
            and os.path.abspath(os.path.join(root, d)) not in submodule_dirs
        ]
        for f in files:
            if not f.endswith(".py"):
                continue
            try:
                tree = ast.parse(open(os.path.join(root, f)).read())
            except Exception:
                continue
            for node in ast.walk(tree):
                if (isinstance(node, ast.Assign)
                        and any(_is_router_target(t) for t in node.targets)
                        and isinstance(node.value, ast.Dict)):
                    for k in node.value.keys:
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            actions.add(k.value)
    return frozenset(actions)


@lru_cache(maxsize=1)
def dangerous_actions() -> frozenset:
    """The router's DANGEROUS_ACTIONS frozenset, AST-parsed (single source of truth).

    The MCP confirm mapping reads THIS, never a copy, so the protocol layer and
    the router gate can never disagree (ADR-0024 sub-decision 2).
    """
    try:
        tree = ast.parse(open(_ROUTER_PATH).read())
    except Exception:
        return frozenset()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "DANGEROUS_ACTIONS"
                        for t in node.targets)):
            names = set()
            for e in ast.walk(node.value):
                if isinstance(e, ast.Constant) and isinstance(e.value, str):
                    names.add(e.value)
            return frozenset(names)
    return frozenset()


@lru_cache(maxsize=1)
def _skillmd_descriptions() -> dict:
    """Map action name → its SKILL.md catalog-row description (best effort).

    The catalog rows are markdown tables ``| `a` / `b` / `c` | description |``.
    Every backtick action token on a row shares that row's description. Used for
    human-readable tool descriptions; absence is non-fatal (name still listed).
    """
    text = _read_source_skill_md()
    descriptions = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        action_cell, desc_cell = cells[0], cells[1]
        tokens = re.findall(r"`([a-z][\w-]*)`", action_cell)
        if not tokens:
            continue
        for tok in tokens:
            descriptions[tok] = desc_cell
    return descriptions


def _read_source_skill_md() -> str:
    if os.path.isfile(_SOURCE_SKILL_MD):
        return open(_SOURCE_SKILL_MD).read()
    return ""


def list_actions(module: str = "foundation") -> list:
    """Return the discoverable action catalog (foundation scope, Nik D3).

    ``module`` is accepted for forward-compat module-agnosticism; v1 serves the
    foundation catalog for any value. Each entry: ``name``, ``destructive``,
    ``description`` (may be empty). Credential carve-out actions are excluded
    here so they are not even discoverable over MCP in v1 (ADR-0024 §4).
    """
    from .confirm import CREDENTIAL_CARVE_OUT  # local import avoids a cycle

    names = _foundation_action_names()
    dangerous = dangerous_actions()
    descs = _skillmd_descriptions()
    out = []
    for name in sorted(names):
        if name in CREDENTIAL_CARVE_OUT:
            continue
        out.append({
            "name": name,
            "destructive": name in dangerous,
            "description": descs.get(name, ""),
        })
    return out


def describe_action(action_name: str) -> dict:
    """Return the metadata payload for one action, or an error dict if unknown.

    Includes the destructive flag and the SKILL.md description. Destructive
    actions carry an explicit note that a genuine second confirmation
    (``user_confirmed: true``) is required (ADR-0024 sub-decision 2).
    """
    from .confirm import CREDENTIAL_CARVE_OUT

    names = _foundation_action_names()
    if action_name in CREDENTIAL_CARVE_OUT:
        return {
            "status": "error",
            "error": f"Action '{action_name}' is not exposed over MCP in v1 "
                     f"(credential carve-out, ADR-0017 S0c).",
        }
    if action_name not in names:
        return {
            "status": "error",
            "error": f"Unknown foundation action: {action_name!r}. "
                     f"Call erpclaw_list_actions to see the catalog.",
        }
    destructive = action_name in dangerous_actions()
    payload = {
        "status": "ok",
        "name": action_name,
        "destructive": destructive,
        "description": _skillmd_descriptions().get(action_name, ""),
        "args_hint": "Pass action arguments as a JSON object on erpclaw_action; "
                     "keys map to the router's --kebab-case flags "
                     "(e.g. {\"name\": \"Acme\", \"company_id\": \"...\"} "
                     "→ --name Acme --company-id ...).",
    }
    if destructive:
        payload["requires_confirmation"] = True
        payload["confirmation_note"] = (
            "This action is destructive/high-impact. erpclaw_action will NOT "
            "execute it unless called with user_confirmed=true reflecting a "
            "genuine user confirmation (ADR-0018 / ADR-0024)."
        )
    return payload
