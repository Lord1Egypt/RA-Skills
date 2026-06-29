#!/usr/bin/env bash
# run-model-discovery.sh — Wrapper for auto-populate-models.py
# Called by cron. Silently discovers models from OpenClaw config
# and merges into orchestrator-data/models.json.
#
# No stdout during normal operation — only errors surface via cron alert.
# Logs to orchestrator-data/.last_discovery.json on success.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$SKILL_DIR/scripts/auto-populate-models.py"

if [ ! -f "$SCRIPT" ]; then
  echo "[model-discovery] ERROR: $SCRIPT not found" >&2
  exit 1
fi

# Run in silent mode — only errors shown
python3 "$SCRIPT" 2>&1 | grep -E "❌|ERR|failed" || true

echo "[model-discovery] completed at $(date -Iseconds)"
