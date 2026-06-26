#!/usr/bin/env bash
# Called by the SessionEnd hook when a Claude Code session terminates.
# Marks the registry entry dead and captures the local UUID.
#
# Usage: on_session_end.sh <session-label>
#
# Designed to be called from .claude/settings.json SessionEnd hook.

SESSION_LABEL="${1:?Missing session label}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Mark registry dead + capture UUID ────────────────────────────────────────
python3 "$SCRIPT_DIR/registry.py" mark-dead "$SESSION_LABEL"
