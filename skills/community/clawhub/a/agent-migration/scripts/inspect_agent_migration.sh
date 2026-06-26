#!/usr/bin/env bash
set -euo pipefail

OLD_ID="${1:-}"
NEW_ID="${2:-}"

if [[ -z "$OLD_ID" || -z "$NEW_ID" ]]; then
  echo "Usage: inspect_agent_migration.sh <old-agent-id> <new-agent-id>"
  exit 1
fi

echo "== Config matches =="
grep -nE "\"id\": \"$OLD_ID\"|\"id\": \"$NEW_ID\"|$OLD_ID|$NEW_ID" ~/.openclaw/openclaw.json || true

echo
echo "== Agent dirs =="
ls -ld ~/.openclaw/agents/$OLD_ID ~/.openclaw/agents/$NEW_ID 2>/dev/null || true

echo
echo "== Session files =="
find ~/.openclaw/agents/$OLD_ID ~/.openclaw/agents/$NEW_ID -maxdepth 3 \( -name '*.jsonl' -o -name '*.json' -o -name '*.lock' \) 2>/dev/null | sort || true

echo
echo "== Workspace dirs =="
find ~/claw-workspace -maxdepth 1 -type d | sort || true

echo
echo "Inspection complete."
