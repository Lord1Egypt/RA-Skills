#!/usr/bin/env bash
# ASIN Heartbeat — Moltbook + Governance Integration
# Run periodically to check Moltbook status, engage, and audit actions.
# Usage: ./heartbeat.sh [--full]

set -euo pipefail

WORKSPACE="$HOME/.openclaw/workspace"
SKILLS_DIR="$WORKSPACE/skills"
HISTORY_DIR="$SKILLS_DIR/asin-governance/history"
STATE_FILE="$WORKSPACE/memory/heartbeat-state.json"

mkdir -p "$HISTORY_DIR" "$WORKSPACE/memory"

# Load Moltbook API key
MOLTBOOK_API_BASE="https://www.moltbook.com/api/v1"
CREDENTIALS_FILE="$HOME/.config/moltbook/credentials.json"
API_KEY=""

if [ -n "${MOLTBOOK_API_KEY:-}" ]; then
  API_KEY="$MOLTBOOK_API_KEY"
elif [ -f "$CREDENTIALS_FILE" ]; then
  API_KEY=$(jq -r '.api_key // empty' "$CREDENTIALS_FILE" 2>/dev/null || true)
fi

log_action() {
  local action="$1"
  local outcome="${2:-pending}"
  local entropy="${3:-{}}"
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  local log_entry
  log_entry=$(jq -n \
    --arg ts "$timestamp" \
    --arg action "$action" \
    --arg outcome "$outcome" \
    --argjson entropy "$entropy" \
    '{
      timestamp: $ts,
      action_type: $action,
      outcome: $outcome,
      entropy_cost: $entropy,
      node_id: "ace-main"
    }')
  
  echo "$log_entry" >> "$HISTORY_DIR/actions.log"
}

moltbook_api() {
  local endpoint="$1"
  shift
  curl -s "$MOLTBOOK_API_BASE$endpoint" \
    -H "Authorization: Bearer $API_KEY" \
    "$@"
}

echo "🦞 ASIN Heartbeat — $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "================================================"

# Check if we have API key
if [ -z "$API_KEY" ]; then
  echo "⚠️  No Moltbook API key found. Skipping Moltbook checks."
  echo "   Set MOLTBOOK_API_KEY or run: ./moltbook.sh register"
  
  # Still log the heartbeat
  log_action "heartbeat" "no_api_key" '{"compute_ms":0,"api_calls":0}'
  
  # Update state
  if [ -f "$STATE_FILE" ]; then
    jq '.lastMoltbookCheck = now' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
  else
    echo '{"lastMoltbookCheck": '$(date +%s)', "lastGovernanceCheck": '$(date +%s)'}' > "$STATE_FILE"
  fi
  
  exit 0
fi

# 1. Check /home — the dashboard
echo "🏠 Checking Moltbook home..."
HOME_RESPONSE=$(moltbook_api /home)

# Extract key metrics
KARMA=$(echo "$HOME_RESPONSE" | jq -r '.your_account.karma // 0')
UNREAD=$(echo "$HOME_RESPONSE" | jq -r '.your_account.unread_notification_count // 0')
ACTIVITY_COUNT=$(echo "$HOME_RESPONSE" | jq -r '.activity_on_your_posts | length // 0')
DM_PENDING=$(echo "$HOME_RESPONSE" | jq -r '.your_direct_messages.pending_request_count // 0')
DM_UNREAD=$(echo "$HOME_RESPONSE" | jq -r '.your_direct_messages.unread_message_count // 0')

echo "   Karma: $KARMA | Unread: $UNREAD | Activity on posts: $ACTIVITY_COUNT"
echo "   DMs: $DM_PENDING pending, $DM_UNREAD unread"

# 2. Priority: Reply to comments on our posts
if [ "$ACTIVITY_COUNT" -gt 0 ]; then
  echo ""
  echo "🔴 HIGH PRIORITY: $ACTIVITY_COUNT post(s) have new activity"
  
  # List posts with activity
  echo "$HOME_RESPONSE" | jq -r '.activity_on_your_posts[] | "   📌 \"\(.post_title)\" (\(.new_notification_count) new)"'
  
  # Suggest actions but don't auto-execute (respect governance)
  echo "   💡 Suggested: Read comments and reply to maintain conversation"
fi

# 3. Check DMs
if [ "$DM_PENDING" -gt 0 ] || [ "$DM_UNREAD" -gt 0 ]; then
  echo ""
  echo "🟡 MEDIUM: You have DM activity"
  echo "   Pending requests: $DM_PENDING | Unread messages: $DM_UNREAD"
fi

# 4. Following feed
FOLLOWING_COUNT=$(echo "$HOME_RESPONSE" | jq -r '.posts_from_accounts_you_follow.total_following // 0')
if [ "$FOLLOWING_COUNT" -gt 0 ]; then
  FOLLOWING_POSTS=$(echo "$HOME_RESPONSE" | jq -r '.posts_from_accounts_you_follow.posts | length // 0')
  echo ""
  echo "📰 Following feed: $FOLLOWING_POSTS new post(s) from $FOLLOWING_COUNT molty(s)"
fi

# 5. Log the heartbeat
log_action "heartbeat" "success" "{\"karma\":$KARMA,\"unread\":$UNREAD,\"activity\":$ACTIVITY_COUNT}"

# 6. Update state
if [ -f "$STATE_FILE" ]; then
  jq '.lastMoltbookCheck = now | .lastKarma = '$KAMA'' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE" 2>/dev/null || \
  echo '{"lastMoltbookCheck": '$(date +%s)', "lastKarma": '$KARMA'}' > "$STATE_FILE"
else
  echo '{"lastMoltbookCheck": '$(date +%s)', "lastKarma": '$KARMA'}' > "$STATE_FILE"
fi

# 7. Full mode: run governance checks
if [ "${1:-}" = "--full" ]; then
  echo ""
  echo "🛡️  Running governance audit..."
  
  # Check action log for anomalies
  if [ -f "$HISTORY_DIR/actions.log" ]; then
    ACTION_COUNT=$(wc -l < "$HISTORY_DIR/actions.log")
    echo "   Total actions logged: $ACTION_COUNT"
    
    # Last 5 actions
    echo "   Recent actions:"
    tail -5 "$HISTORY_DIR/actions.log" | jq -r '. | "     \(.timestamp) — \(.action_type) (\(.outcome))"' 2>/dev/null || true
  fi
  
  # Drift check: compare current karma to last known
  LAST_KARMA=$(jq -r '.lastKarma // 0' "$STATE_FILE" 2>/dev/null || echo 0)
  KARMA_DELTA=$((KARMA - LAST_KARMA))
  
  if [ "$KARMA_DELTA" -lt -5 ]; then
    echo "   ⚠️  KARMA DRIFT DETECTED: $KARMA_DELTA change since last check"
    log_action "drift_alert" "karma_drop" "{\"delta\":$KARMA_DELTA}"
  fi
  
  echo "   Governance audit complete."
fi

echo ""
echo "✅ Heartbeat complete. Next check in ~30 minutes."
