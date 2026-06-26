#!/usr/bin/env bash
set -euo pipefail

OLD_ID="${1:-}"
NEW_ID="${2:-}"
if [[ -z "$OLD_ID" || -z "$NEW_ID" ]]; then
  echo "Usage: verify_agent_migration.sh <old-agent-id> <new-agent-id>"
  exit 1
fi

CFG="$HOME/.openclaw/openclaw.json"

echo "== Config =="
grep -nE "\"id\": \"$OLD_ID\"|\"id\": \"$NEW_ID\"|/claw-workspace/$OLD_ID|/claw-workspace/$NEW_ID" "$CFG" || true

echo
echo "== Agent dirs =="
ls -ld "$HOME/.openclaw/agents/$OLD_ID" "$HOME/.openclaw/agents/$NEW_ID" 2>/dev/null || true

echo
echo "== Workspace dirs =="
ls -ld "$HOME/claw-workspace/$OLD_ID" "$HOME/claw-workspace/$NEW_ID" 2>/dev/null || true

echo
echo "== Session files =="
find "$HOME/.openclaw/agents/$NEW_ID" -maxdepth 3 -type f \( -name '*.jsonl' -o -name '*.json' -o -name '*.lock' -o -name '*.txt' \) 2>/dev/null | sort || true

echo
echo "== Doctor =="
openclaw doctor --non-interactive || true

echo
echo "Verification complete."
