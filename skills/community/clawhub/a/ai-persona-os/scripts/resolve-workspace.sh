#!/usr/bin/env bash
# resolve-workspace.sh — Print the agent's effective workspace path.
#
# Order of precedence:
#   1. $OPENCLAW_WORKSPACE env var (if the runtime sets one)
#   2. agents.defaults.workspace from ~/.openclaw/openclaw.json
#   3. Default: $HOME/.openclaw/workspace
#
# This is a convenience helper for the AI Persona OS skill. The skill body
# also describes the JSON-parsing logic so the agent can do it natively
# without invoking this script — but having it here means non-AI tooling
# (cron jobs, post-install scripts, manual debugging) can also resolve
# the path the same way.
#
# Usage:
#   bash scripts/resolve-workspace.sh        # prints the path
#   WS=$(bash scripts/resolve-workspace.sh)  # captures it
#
# Safe: no network calls, no writes, read-only.

set -u

DEFAULT="$HOME/.openclaw/workspace"
CONFIG="$HOME/.openclaw/openclaw.json"

# 1) Env var override (highest priority — useful for testing/CI)
if [ -n "${OPENCLAW_WORKSPACE:-}" ]; then
  echo "$OPENCLAW_WORKSPACE"
  exit 0
fi

# 2) Try to parse openclaw.json
if [ -r "$CONFIG" ]; then
  WS=""

  # Prefer jq if available
  if command -v jq >/dev/null 2>&1; then
    WS=$(jq -r '.agents.defaults.workspace // empty' "$CONFIG" 2>/dev/null)
  fi

  # Fall back to python3
  if [ -z "$WS" ] && command -v python3 >/dev/null 2>&1; then
    WS=$(python3 -c "
import json, sys
try:
    with open(sys.argv[1]) as f:
        cfg = json.load(f)
    print(cfg.get('agents', {}).get('defaults', {}).get('workspace', ''))
except Exception:
    pass
" "$CONFIG" 2>/dev/null)
  fi

  # Last resort: grep + sed
  if [ -z "$WS" ]; then
    WS=$(grep -E '"workspace"[[:space:]]*:' "$CONFIG" 2>/dev/null | head -1 \
         | sed -n 's/.*"workspace"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  fi

  if [ -n "$WS" ]; then
    # Expand ~ and $HOME / ${HOME}
    WS="${WS/#\~/$HOME}"
    WS="${WS//\$HOME/$HOME}"
    WS="${WS//\$\{HOME\}/$HOME}"
    echo "$WS"
    exit 0
  fi
fi

# 3) Default
echo "$DEFAULT"
