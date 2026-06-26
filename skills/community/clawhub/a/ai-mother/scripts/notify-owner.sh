#!/bin/bash
# Send a Feishu DM notification to the owner
# Only sends to direct message (open_id starting with ou_), never to groups
#
# Usage:
#   ./notify-owner.sh "<message>"
#   ./notify-owner.sh "<message>" "<open_id>"   # override recipient

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
CONFIG_FILE="$SKILL_DIR/config.json"
MSG=$1
OVERRIDE_ID=$2

if [ -z "$MSG" ]; then
    echo "Usage: $0 <message> [open_id]"
    exit 1
fi

# Load owner open_id from config
if [ -f "$CONFIG_FILE" ]; then
    OWNER_OPEN_ID=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('owner_feishu_open_id',''))" 2>/dev/null)
fi

# Use override if provided
[ -n "$OVERRIDE_ID" ] && OWNER_OPEN_ID="$OVERRIDE_ID"

if [ -z "$OWNER_OPEN_ID" ]; then
    echo "❌ No owner open_id configured."
    echo "Run: openclaw config to find your Feishu open_id, then:"
    echo "  echo '{\"owner_feishu_open_id\": \"ou_xxx\"}' > $CONFIG_FILE"
    exit 1
fi

# Safety check: only allow open_id (ou_) for DM, reject chat_id (oc_)
if [[ "$OWNER_OPEN_ID" == oc_* ]]; then
    echo "❌ Rejected: '$OWNER_OPEN_ID' is a group chat_id, not a user open_id."
    echo "AI Mother only sends DMs. Use an open_id starting with 'ou_'."
    exit 1
fi

if [[ "$OWNER_OPEN_ID" != ou_* ]]; then
    echo "❌ Rejected: '$OWNER_OPEN_ID' does not look like a valid open_id (must start with 'ou_')."
    exit 1
fi

echo "Sending DM to $OWNER_OPEN_ID..."

# Use openclaw message send (DM only, target = user:open_id)
openclaw message send \
    --channel feishu \
    --target "user:$OWNER_OPEN_ID" \
    --message "$MSG" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Feishu DM sent to $OWNER_OPEN_ID"
else
    echo "❌ Failed to send Feishu DM"
    exit 1
fi
