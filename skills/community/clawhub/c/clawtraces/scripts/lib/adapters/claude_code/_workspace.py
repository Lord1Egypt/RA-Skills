# FILE_META
# INPUT:  real cwd string + PipelineOptions (CLAUDE_HOME override)
# OUTPUT: workspace_snapshot Attachment list + mcp/skills summaries
# POS:    skill lib adapters/claude_code — private workspace snapshot helper
# MISSION: Collect the per-session context slices the server needs to rebuild the system prompt.

"""Per-session workspace_snapshot collector.

Per docs/adapter-design.md §5.3 + §8.3, a Claude Code session_bundle
carries three core-zone artifacts alongside ``raw_session.jsonl``:

  workspace_snapshot/project_claude_md   ← <cwd>/CLAUDE.md
  workspace_snapshot/user_claude_md      ← ~/.claude/CLAUDE.md
  workspace_snapshot/mcp_snapshot.json   ← merged mcpServers view

We also derive two summaries that feed back into ``prompt_hint.extras``:

  mcp_servers    — sorted list of effective MCP server names in play
  skills_enabled — sorted list of plugins toggled on (enabledPlugins
                   values truthy), drawn from user + project settings.

Settings provenance we consider:
  - ~/.claude/settings.json                                  (user scope)
  - <cwd>/.claude/settings.json                              (project scope)
  - <cwd>/.mcp.json                                          (project MCP)

Intentionally **excluded**:
  - ~/.claude/settings.local.json  (host-specific, may leak host state)
  - <cwd>/.claude/settings.local.json  (often user-private overrides)
  PII scrub still runs on the text we do ship; local.json stays out
  entirely to keep the threat surface small.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .. import Attachment
from ._paths import claude_home


def collect(cwd: str | None, opts: Any = None) -> dict:
    """Gather workspace_snapshot artifacts + summaries for one session.

    Returns a dict with keys:
      attachments     list[Attachment] — core-zone files to zip
      mcp_servers     list[str] | None — sorted effective MCP names
      skills_enabled  list[str] | None — sorted enabled plugin names

    ``None`` values mean "no signal at all" (no settings files read).
    Empty lists mean "read settings but found nothing configured" — the
    distinction matters for delivery auditing.
    """
    attachments: list[Attachment] = []
    project_root = Path(cwd) if cwd else None
    user_root = claude_home(opts)

    # ─── CLAUDE.md snapshots ───────────────────────────────────────────
    if project_root is not None:
        project_md = _read_file(project_root / "CLAUDE.md")
        if project_md is not None:
            attachments.append(
                Attachment(
                    zip_path="workspace_snapshot/project_claude_md",
                    content=project_md,
                    is_core=True,
                )
            )

    user_md = _read_file(user_root / "CLAUDE.md")
    if user_md is not None:
        attachments.append(
            Attachment(
                zip_path="workspace_snapshot/user_claude_md",
                content=user_md,
                is_core=True,
            )
        )

    # ─── settings/MCP ingest ───────────────────────────────────────────
    user_settings = _read_json(user_root / "settings.json")
    project_settings = (
        _read_json(project_root / ".claude" / "settings.json") if project_root else None
    )
    project_mcp = (
        _read_json(project_root / ".mcp.json") if project_root else None
    )

    any_settings_seen = any(
        x is not None for x in (user_settings, project_settings, project_mcp)
    )

    user_mcp = _extract_mcp_servers(user_settings)
    project_settings_mcp = _extract_mcp_servers(project_settings)
    project_mcp_file = _extract_mcp_servers(project_mcp)
    effective = {**user_mcp, **project_settings_mcp, **project_mcp_file}

    if any_settings_seen:
        mcp_snapshot = {
            "user": user_mcp,
            "project_settings": project_settings_mcp,
            "project_mcp": project_mcp_file,
            "effective": effective,
        }
        attachments.append(
            Attachment(
                zip_path="workspace_snapshot/mcp_snapshot.json",
                content=json.dumps(mcp_snapshot, ensure_ascii=False, indent=2).encode(
                    "utf-8"
                ),
                is_core=True,
            )
        )
        mcp_servers = sorted(effective.keys())
    else:
        mcp_servers = None

    # ─── skills_enabled (plugins) ──────────────────────────────────────
    enabled = _merge_enabled_plugins(user_settings, project_settings)
    if any_settings_seen and enabled is not None:
        skills_enabled = sorted(k for k, v in enabled.items() if v)
    else:
        skills_enabled = None

    return {
        "attachments": attachments,
        "mcp_servers": mcp_servers,
        "skills_enabled": skills_enabled,
    }


# ─── Low-level readers ─────────────────────────────────────────────────

def _read_file(path: Path) -> bytes | None:
    try:
        if not path.is_file():
            return None
        return path.read_bytes()
    except OSError:
        return None


def _read_json(path: Path) -> dict | None:
    try:
        if not path.is_file():
            return None
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _extract_mcp_servers(obj: dict | None) -> dict:
    """Pull ``mcpServers`` out of a settings/.mcp.json dict, guarding types."""
    if not isinstance(obj, dict):
        return {}
    raw = obj.get("mcpServers")
    if not isinstance(raw, dict):
        return {}
    # Defensive copy; we do not mutate caller objects.
    return {k: v for k, v in raw.items() if isinstance(k, str)}


def _merge_enabled_plugins(user: dict | None, project: dict | None) -> dict | None:
    u = user.get("enabledPlugins") if isinstance(user, dict) else None
    p = project.get("enabledPlugins") if isinstance(project, dict) else None
    if not isinstance(u, dict):
        u = {}
    if not isinstance(p, dict):
        p = {}
    if not u and not p:
        # Neither file had the key at all. Signal "no data" vs "empty".
        if user is None and project is None:
            return None
        return {}
    # Project overrides user for the same plugin key.
    return {**u, **p}


__all__ = ["collect"]
