#!/usr/bin/env bash
set -euo pipefail

INPUT="$(cat)"
STATE="docs/cccc/state.json"
mkdir -p docs/cccc/logs
STAMP="$(date -u +"%Y%m%dT%H%M%SZ")"
echo "$INPUT" > "docs/cccc/logs/stop-failure-$STAMP.json"

if [[ -f "$STATE" ]]; then
  python3 .claude/skills/cc-codex-collaborate/scripts/cccc-update-state.py \
    --set 'status="PAUSED_FOR_SYSTEM"' \
    --set 'pause_reason="StopFailure hook recorded an API or runtime failure. Manual review is required before resuming."' >/dev/null 2>&1 || true
fi

exit 0
