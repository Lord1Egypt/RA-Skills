#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/require_obs_mcp.sh"

TRANSITION="${1:-Fade}"
DURATION_MS="${2:-300}"

mcporter call "obs.set_current_transition(transition_name: \"$TRANSITION\")" >/dev/null
mcporter call "obs.set_transition_duration(transition_duration: $DURATION_MS)" >/dev/null

echo "Applied transition preset: $TRANSITION (${DURATION_MS}ms)"
