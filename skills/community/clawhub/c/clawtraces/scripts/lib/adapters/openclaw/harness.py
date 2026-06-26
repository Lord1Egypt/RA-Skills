# FILE_META
# INPUT:  scope_id (OpenClaw agent_id) + PipelineOptions
# OUTPUT: HarnessBundle (zip bytes + PII scrub report) or None
# POS:    skill lib adapters/openclaw — harness packager
# MISSION: Pack OpenClaw agent workspace (SOUL.md / USER.md / memory/ ...) into
#          a zip, honoring existing PII scrub rules from workspace_bundle.py.

"""Harness packager for OpenClaw workspace bundles.

Scope model for OpenClaw (docs/adapter-design.md §6.2):

    scope_type = "agent"
    scope_id   = <agent_id>   e.g. "main"

Harness contents (§6.3):

    SOUL.md / USER.md / TOOLS.md / AGENTS.md / MEMORY.md
    memory/**/*.md
    cron/**/*
    sessions.json

Kept backward-compatible with the existing ``workspace_bundle.py`` script
during Phase 4: both call into the same packager + PII scrubber so
migration does not change what ends up on disk.

**Phase 4 scaffold — implementation follows in B2**.
"""

from __future__ import annotations

from typing import Any

from .. import ScopeInfo


def list_scopes(opts: Any = None) -> list[ScopeInfo]:
    """Enumerate available OpenClaw agents as harness scopes.

    Returns empty list until B2 wires this up to
    ``lib.parse.session_index.find_openclaw_sessions_dirs``.
    """
    raise NotImplementedError(
        "adapters.openclaw.list_scopes: Phase 4 scaffold — not yet wired up."
    )


def build_harness(scope_id: str, opts: Any = None):
    """Pack one OpenClaw agent's workspace into a HarnessBundle.

    Delegates to the existing ``workspace_bundle.create_workspace_bundle``
    once B2 completes.
    """
    raise NotImplementedError(
        "adapters.openclaw.build_harness: Phase 4 scaffold — not yet wired up. "
        "Use workspace_bundle.py until B2 migration completes."
    )
