#!/bin/bash
# send_agent_msg.sh - Batch send messages to OpenClaw agents via Telegram

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="/data/.openclaw/openclaw.json"
TELEGRAM_API="https://api.telegram.org/bot"

# Parse arguments
MESSAGE=""
AGENTS=()
CHANNEL="telegram"
USER_ID="8341113912"
VARS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agents)
      shift
      while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
        AGENTS+=("$1")
        shift
      done
      ;;
    --all)
      AGENTS=("all")
      shift
      ;;
    --channel)
      CHANNEL="$2"
      shift 2
      ;;
    --vars)
      shift
      while [[ $# -gt 0 && ! "$1" =~ ^-- ]]; do
        VARS+=("$1")
        shift
      done
      ;;
    *)
      if [ -z "$MESSAGE" ]; then
        MESSAGE="$1"
      fi
      shift
      ;;
  esac
done

if [ -z "$MESSAGE" ]; then
  echo "Usage: $0 <message> [--agents <agent1> <agent2>...] [--all] [--channel <channel>]"
  exit 1
fi

# Extract agent list from openclaw.json
if [[ " ${AGENTS[@]} " =~ " all " ]]; then
  AGENTS=($(jq -r '.agents.list[].id' "$CONFIG_FILE"))
fi

# Extract bot tokens from config
declare -A BOT_TOKENS
declare -A AGENT_NAMES

# Map agent ID → bot token + name
for agent in "${AGENTS[@]}"; do
  ACCOUNT_ID=$(jq -r ".bindings[] | select(.agentId==\"$agent\") | .match.accountId" "$CONFIG_FILE")
  BOT_TOKEN=$(jq -r ".channels.telegram.accounts[\"$ACCOUNT_ID\"].botToken" "$CONFIG_FILE")
  AGENT_NAME=$(jq -r ".agents.list[] | select(.id==\"$agent\") | .name" "$CONFIG_FILE")
  
  if [ -n "$BOT_TOKEN" ] && [ "$BOT_TOKEN" != "null" ]; then
    BOT_TOKENS[$agent]=$BOT_TOKEN
    AGENT_NAMES[$agent]=$AGENT_NAME
  fi
done

# Apply template variables
FINAL_MESSAGE="$MESSAGE"
for var in "${VARS[@]}"; do
  KEY="${var%=*}"
  VAL="${var#*=}"
  FINAL_MESSAGE="${FINAL_MESSAGE//\{\{$KEY\}\}/$VAL}"
done

# Send messages
SENT=0
FAILED=0

for agent in "${AGENTS[@]}"; do
  if [ -z "${BOT_TOKENS[$agent]}" ]; then
    echo "❌ $agent: No bot token found"
    ((FAILED++))
    continue
  fi
  
  BOT_TOKEN="${BOT_TOKENS[$agent]}"
  AGENT_NAME="${AGENT_NAMES[$agent]}"
  EMOJI=$(jq -r ".agents.list[] | select(.id==\"$agent\") | .identity.emoji // \"\"" "$CONFIG_FILE")
  
  # Send via Telegram API
  RESPONSE=$(curl -s -X POST "${TELEGRAM_API}${BOT_TOKEN}/sendMessage" \
    -d "chat_id=$USER_ID" \
    -d "text=$EMOJI $AGENT_NAME: $FINAL_MESSAGE")
  
  SUCCESS=$(echo "$RESPONSE" | jq -r '.ok // false')
  
  if [ "$SUCCESS" = "true" ]; then
    echo "✅ $agent ($AGENT_NAME)"
    ((SENT++))
  else
    ERROR=$(echo "$RESPONSE" | jq -r '.description // "Unknown error"')
    echo "❌ $agent: $ERROR"
    ((FAILED++))
  fi
done

echo ""
echo "📊 Summary: $SENT sent, $FAILED failed"
[ $FAILED -eq 0 ] && exit 0 || exit 1
