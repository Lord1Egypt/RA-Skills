#!/bin/bash
# agent-deploy v2.1: Remove an OpenClaw agent
set -euo pipefail

AGENT_ID="${1:?Usage: remove.sh <agentId>}"
CONFIG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
BACKUP="$HOME/.openclaw/openclaw.json.pre-remove-$AGENT_ID"
OC="${OPENCLAW_BIN:-openclaw}"
HELPER="$(dirname "$0")/deploy_helper.py"

if [ "$AGENT_ID" = "main" ]; then
    echo "ERROR: Cannot remove the main agent!"
    exit 1
fi

echo "[agent-deploy] Remove: $AGENT_ID"

if [ ! -f "$CONFIG" ]; then
    echo "ERROR: Config not found: $CONFIG"
    exit 1
fi

cp "$CONFIG" "$BACKUP"
echo "  Backup: $BACKUP"

echo "  Removing from agents.list..."
NEW_LIST=$(python3 "$HELPER" gen-remove-agents "$AGENT_ID")
$OC config set agents.list "$NEW_LIST"

echo "  Removing from bindings..."
NEW_BINDINGS=$(python3 "$HELPER" gen-remove-bindings "$AGENT_ID")
$OC config set bindings "$NEW_BINDINGS"

echo "  Removing telegram account..."
$OC config unset "channels.telegram.accounts.$AGENT_ID" 2>/dev/null || true

echo "  Validating..."
if ! $OC doctor 2>/dev/null; then
    echo "VALIDATION FAILED. Rolling back..."
    cp "$BACKUP" "$CONFIG"
    exit 1
fi

echo ""
echo "SUCCESS: Agent '$AGENT_ID' removed"
echo "  Workspace NOT deleted: $HOME/.openclaw/workspace-$AGENT_ID"
echo "  Channels/bindings hot-reload automatically."
