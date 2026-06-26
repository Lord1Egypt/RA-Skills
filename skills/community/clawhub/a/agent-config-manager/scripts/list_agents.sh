#!/bin/bash
# list_agents.sh - List all OpenClaw agents and their models

CONFIG_FILE="/data/.openclaw/openclaw.json"

echo "🤖 OpenClaw Agents"
echo ""

jq -r '
  .agents.list[] |
  "\(.identity.emoji // \"🔲\") \(.id)\t\(.name)\t\(.model.primary // \"N/A\")"
' "$CONFIG_FILE" | column -t -s $'\t'

echo ""
echo "📊 Total agents: $(jq '.agents.list | length' "$CONFIG_FILE")"
echo ""
echo "📡 Channel Bindings:"
jq -r '
  .bindings[] |
  "  \(.agentId) → telegram/@\(.match.accountId)"
' "$CONFIG_FILE"
