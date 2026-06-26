# FILE_META
# INPUT:  scope_id (sha256(cwd)[:16]) + PipelineOptions
# OUTPUT: HarnessBundle (zip bytes + scrub report) or ScopeInfo list
# POS:    skill lib adapters/claude_code — harness packaging stage
# MISSION: Bundle per-project .claude/ + global settings into a scope='project' harness zip.

"""Claude Code harness packaging.

Scope model (docs/adapter-design.md §6.2): one scope per project cwd.
``scope_id = sha256(cwd)[:16]`` — matching the cwd_hash convention
prompt_hint uses, so one project's sessions and its harness live under
the same key server-side.

Zip layout::

    project/
      CLAUDE.md
      .claude/settings.json
      .claude/agents/<name>.md
      .mcp.json
    user/
      CLAUDE.md
      settings.json
      agents/<name>.md

Excluded on purpose (same rationale as _workspace.py):
  - settings.local.json (both scopes) — host-specific and user-private.
  - state files like session jsonls themselves (those ship via
    session_bundle.zip).

list_scopes() enumerates every ~/.claude/projects/<slug>/ we can resolve
to a real cwd. The real cwd is read from the first content-bearing event
of any jsonl in that directory (slug → cwd decoding is lossy). Projects
with no readable jsonl at all are skipped.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .. import ScopeInfo
from ._paths import claude_home, projects_dir

try:
    from lib.harness import HarnessBundle, HarnessFile, build_bundle
    from lib.harness.packager import walk_directory
except ImportError:
    from ...harness import HarnessBundle, HarnessFile, build_bundle  # type: ignore
    from ...harness.packager import walk_directory  # type: ignore


# Event types that carry the real cwd string on every line.
_CWD_BEARING_TYPES = {"user", "assistant", "system", "attachment"}
# How many lines to scan per jsonl when probing for a cwd.
_CWD_PROBE_LINE_CAP = 50


def list_scopes(opts: Any = None) -> list[ScopeInfo]:
    """Enumerate every project scope with at least one recorded session."""
    return [
        ScopeInfo(
            scope_type="project",
            scope_id=_scope_id(cwd),
            display_name=cwd,
        )
        for cwd in _enumerate_project_cwds(opts)
    ]


def build_harness(scope_id: str, opts: Any = None) -> HarnessBundle:
    """Pack a single project's Claude Code context + user-global context."""
    cwd = _resolve_cwd(scope_id, opts)
    if cwd is None:
        raise ValueError(
            f"unknown claude-code scope_id: {scope_id!r} (no project matches)"
        )

    project_root = Path(cwd)
    user_root = claude_home(opts)

    manifest: list[HarnessFile] = []

    # ─── Project scope ─────────────────────────────────────────────────
    manifest.extend(_project_files(project_root))

    # ─── User scope ────────────────────────────────────────────────────
    manifest.extend(_user_files(user_root))

    return build_bundle(manifest)


# ─── Manifest builders ─────────────────────────────────────────────────

def _project_files(project_root: Path) -> list[HarnessFile]:
    out: list[HarnessFile] = []

    # Standalone files at project root.
    for name, arc in (
        ("CLAUDE.md", "project/CLAUDE.md"),
        (".mcp.json", "project/.mcp.json"),
    ):
        out.append(HarnessFile(src=project_root / name, arc=arc, scrub=True))

    # .claude/settings.json only (exclude settings.local.json).
    out.append(
        HarnessFile(
            src=project_root / ".claude" / "settings.json",
            arc="project/.claude/settings.json",
            scrub=True,
        )
    )

    # .claude/agents/ — pack the whole directory.
    out.extend(
        walk_directory(
            project_root / ".claude" / "agents",
            arc_prefix="project/.claude/agents",
            scrub=True,
        )
    )
    return out


def _user_files(user_root: Path) -> list[HarnessFile]:
    out: list[HarnessFile] = []
    for name, arc in (
        ("CLAUDE.md", "user/CLAUDE.md"),
        ("settings.json", "user/settings.json"),
    ):
        out.append(HarnessFile(src=user_root / name, arc=arc, scrub=True))

    out.extend(
        walk_directory(
            user_root / "agents",
            arc_prefix="user/agents",
            scrub=True,
        )
    )
    return out


# ─── Scope enumeration ─────────────────────────────────────────────────

def _enumerate_project_cwds(opts: Any = None) -> list[str]:
    """Return the unique, sorted list of real cwds we have sessions for."""
    root = projects_dir(opts)
    if not root.is_dir():
        return []
    seen: set[str] = set()
    for project_dir in sorted(root.iterdir()):
        if not project_dir.is_dir():
            continue
        cwd = _probe_cwd(project_dir)
        if cwd:
            seen.add(cwd)
    return sorted(seen)


def _probe_cwd(project_dir: Path) -> str | None:
    """Read the first cwd-bearing event from any jsonl in this project dir."""
    for jsonl_path in sorted(project_dir.glob("*.jsonl")):
        try:
            with jsonl_path.open("r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i >= _CWD_PROBE_LINE_CAP:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("type") in _CWD_BEARING_TYPES and obj.get("cwd"):
                        return obj["cwd"]
        except OSError:
            continue
    return None


def _resolve_cwd(scope_id: str, opts: Any = None) -> str | None:
    """Reverse scope_id → cwd by scanning the project directory."""
    for cwd in _enumerate_project_cwds(opts):
        if _scope_id(cwd) == scope_id:
            return cwd
    return None


def _scope_id(cwd: str) -> str:
    return hashlib.sha256(cwd.encode("utf-8")).hexdigest()[:16]


__all__ = ["list_scopes", "build_harness", "_scope_id"]
