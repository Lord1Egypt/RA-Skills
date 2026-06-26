#!/bin/bash
# set_agent_model.sh - Update agent model assignment

set -e

AGENT_ID="${1:?Usage: set_agent_model.sh <agent_id|all> <model>}"
NEW_MODEL="${2:?Usage: set_agent_model.sh <agent_id|all> <model>}"
CONFIG_FILE="/data/.openclaw/openclaw.json"
BACKUP_FILE="/tmp/openclaw-config-$(date +%s).bak"

# Validate model exists in config
MODEL_EXISTS=$(jq --arg m "$NEW_MODEL" '.models.providers.openrouter.models[] | select(.id == $m) | .id' "$CONFIG_FILE" | grep -q "$NEW_MODEL" && echo "yes" || echo "no")

if [ "$MODEL_EXISTS" = "no" ]; then
  echo "❌ Model not found in config: $NEW_MODEL"
  echo ""
  echo "Available models:"
  jq -r '.models.providers.openrouter.models[].id' "$CONFIG_FILE" | head -20
  exit 1
fi

# Backup config
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "💾 Backed up to: $BACKUP_FILE"

# Update agent(s)
if [ "$AGENT_ID" = "all" ]; then
  AGENTS=$(jq -r '.agents.list[].id' "$CONFIG_FILE")
else
  AGENTS="$AGENT_ID"
fi

for agent in $AGENTS; do
  # Check agent exists
  AGENT_EXISTS=$(jq --arg a "$agent" '.agents.list[] | select(.id == $a) | .id' "$CONFIG_FILE" | grep -q "$agent" && echo "yes" || echo "no")
  
  if [ "$AGENT_EXISTS" = "no" ]; then
    echo "⚠️  Agent not found: $agent"
    continue
  fi
  
  # Update model
  jq --arg agent "$agent" --arg model "$NEW_MODEL" \
    '.agents.list[] |= if .id == $agent then .model.primary = $model else . end' \
    "$CONFIG_FILE" > /tmp/openclaw.json.tmp
  
  mv /tmp/openclaw.json.tmp "$CONFIG_FILE"
  
  # Get agent name for display
  NAME=$(jq --arg a "$agent" -r '.agents.list[] | select(.id == $a) | .name' "$CONFIG_FILE")
  echo "✅ Updated $agent ($NAME) → $NEW_MODEL"
done

echo ""
echo "✨ Config updated. Restart gateway to apply:"
echo "   openclaw gateway restart"
