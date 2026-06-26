#!/bin/bash
# agent-deploy v2.1: Deploy a new isolated OpenClaw agent
# Uses openclaw config set + doctor validation + auto-rollback
set -euo pipefail

AGENT_ID="${1:?Usage: deploy.sh <agentId> <botToken> [workspace_path]}"
BOT_TOKEN="${2:?Usage: deploy.sh <agentId> <botToken> [workspace_path]}"
WORKSPACE="${3:-$HOME/.openclaw/workspace-$AGENT_ID}"
CONFIG="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
BACKUP="$HOME/.openclaw/openclaw.json.pre-$AGENT_ID"
OC="${OPENCLAW_BIN:-openclaw}"
HELPER="$(dirname "$0")/deploy_helper.py"

echo "[agent-deploy] v2.4"
echo "  Agent:     $AGENT_ID"
echo "  Token:     ${BOT_TOKEN:0:10}..."
echo "  Workspace: $WORKSPACE"
echo "  Config:    $CONFIG"
echo ""

# Validate token format
if ! echo "$BOT_TOKEN" | grep -qP '^[0-9]+:[A-Za-z0-9_-]+$'; then
    echo "ERROR: Invalid bot token format (expected digits:alphanumeric)"
    exit 1
fi

if [ ! -f "$CONFIG" ]; then
    echo "ERROR: Config not found: $CONFIG"
    exit 1
fi

# [1/8] Pre-flight checks
echo "[1/8] Pre-flight checks..."
PREFLIGHT=$(python3 "$HELPER" preflight "$AGENT_ID" "$BOT_TOKEN" 2>&1) || {
    echo "$PREFLIGHT"
    exit 1
}
echo "  $PREFLIGHT"

# [2/8] Backup
echo "[2/8] Backup..."
cp "$CONFIG" "$BACKUP"
echo "  $BACKUP"

# [3/8] Create workspace
echo "[3/8] Create workspace..."
mkdir -p "$WORKSPACE/memory" "$WORKSPACE/output" "$WORKSPACE/skills"
if [ ! -f "$WORKSPACE/SOUL.md" ]; then
    printf '# Agent\n\nYou are a helpful AI assistant.\n' > "$WORKSPACE/SOUL.md"
    echo "  Created default SOUL.md"
fi
echo "  $WORKSPACE"


# [4/8] Merge auth profiles (global + main agent)
echo "[4/8] Merge auth profiles..."
python3 "$HELPER" merge-auth "$AGENT_ID"
if [ $? -ne 0 ]; then
    echo "  WARNING: Auth merge failed. New agent may not have API keys."
    echo "  Run manually: openclaw agents add $AGENT_ID"
fi

# [5/8] Update agents.list
echo "[5/8] Update agents.list..."
NEW_LIST=$(python3 "$HELPER" gen-agents-list "$AGENT_ID" "$WORKSPACE")
$OC config set agents.list "$NEW_LIST" || {
    echo "ERROR: Failed to set agents.list. Rolling back..."
    cp "$BACKUP" "$CONFIG"
    exit 1
}
echo "  Added $AGENT_ID"

# [6/8] Update bindings
echo "[6/8] Update bindings..."
NEW_BINDINGS=$(python3 "$HELPER" gen-bindings "$AGENT_ID")
$OC config set bindings "$NEW_BINDINGS" || {
    echo "ERROR: Failed to set bindings. Rolling back..."
    cp "$BACKUP" "$CONFIG"
    exit 1
}
echo "  Added $AGENT_ID -> telegram:$AGENT_ID"

# [7/8] Update telegram accounts
echo "[7/8] Update telegram accounts..."
# Handle single-bot to multi-account migration
if echo "$PREFLIGHT" | grep -q "MIGRATE_SINGLE_BOT"; then
    echo "  Migrating from single-bot to multi-account mode..."
    OLD_ACCT=$(python3 "$HELPER" migrate-single-bot)
    $OC config set channels.telegram.accounts.default "$OLD_ACCT" || true
    $OC config unset channels.telegram.botToken 2>/dev/null || true
    $OC config unset channels.telegram.dmPolicy 2>/dev/null || true
fi
ACCT_JSON="{\"botToken\": \"$BOT_TOKEN\", \"dmPolicy\": \"pairing\"}"
$OC config set "channels.telegram.accounts.$AGENT_ID" "$ACCT_JSON" || {
    echo "ERROR: Failed to set telegram account. Rolling back..."
    cp "$BACKUP" "$CONFIG"
    exit 1
}
echo "  Added account $AGENT_ID"

# [8/8] Doctor validation
echo "[8/8] Validating..."
if ! $OC doctor 2>/dev/null; then
    echo ""
    echo "VALIDATION FAILED. Rolling back..."
    cp "$BACKUP" "$CONFIG"
    echo "Rolled back to: $BACKUP"
    exit 1
fi
echo "  Doctor check passed"

echo ""
echo "SUCCESS: Agent '$AGENT_ID' deployed"
echo "  Sandbox:  mode=non-main, scope=agent, workspaceAccess=none"
echo "  Tools:    deny=[gateway]"
echo "  Telegram: account=$AGENT_ID"
echo ""
echo "NOTE: channels/bindings hot-reload automatically."
echo "      If not responding, restart: systemctl --user restart openclaw-gateway"
