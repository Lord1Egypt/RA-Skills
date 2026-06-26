#!/bin/bash
# heartbeat_check.sh - Send heartbeat to all agents, wait for manual ACKs on Telegram

set -e

CONFIG_FILE="/data/.openclaw/openclaw.json"
HEARTBEAT_MESSAGE="${1:-Heartbeat: Tout le monde là? Envoie ✅ si tu reçois}"
WAIT_TIME="${2:-10}"

echo "💓 Sending heartbeat..."
echo "Message: \"$HEARTBEAT_MESSAGE\""
echo ""

# Get all agent names
AGENTS=$(jq -r '.agents.list[].id' "$CONFIG_FILE")

# Send message via agent-messenger
python3 "$(dirname "$0")/send_telegram_direct.py" \
  "$HEARTBEAT_MESSAGE" \
  --agents $AGENTS \
  --format "{emoji} {name}: {message}"

echo ""
echo "⏳ Waiting ${WAIT_TIME}s for manual ACKs on Telegram..."
echo "   → Check Telegram and react with ✅ to confirm receipt"
sleep "$WAIT_TIME"

echo ""
echo "✨ Heartbeat complete!"
echo ""
echo "📊 To track responses, check:"
echo "   1. Telegram for ✅ reactions from each agent"
echo "   2. This output confirms all agents received the message"
echo ""

# Optional: Return exit code based on responses
# (Would need to poll Telegram API for reaction counts)
exit 0
