#!/usr/bin/env bash
# health-check.sh — Agent Bus pipeline health check
set -euo pipefail

MY_AGENT_ID="${AGENT_BUS_AGENT_ID:-your-agent-id}"
REPO="${AGENT_BUS_REPO:-~/agent-bus-repo}"

echo "=== Agent Bus Health Check ==="
echo ""

# 1. Git connectivity
echo "[1/4] Git connectivity..."
if git -C "$REPO" ls-remote origin HEAD &>/dev/null; then
  echo "  ✅ Git remote reachable"
else
  echo "  ❌ Git remote unreachable — check network or repo URL"
fi

# 2. Pair status
echo "[2/4] Pair relationships..."
PAIRS=$(bash "$REPO/agent-bus.sh" check-acl 2>/dev/null || echo "")
if [[ -n "$PAIRS" ]]; then
  echo "  ✅ ACL loaded"
  echo "$PAIRS" | sed 's/^/    /'
else
  echo "  ⚠️  No pairs found — run pair-request to establish a connection"
fi

# 3. Inbox unread count
echo "[3/4] Inbox unread count..."
UNREAD=$(find "$REPO/inbox/$MY_AGENT_ID/" -name "*.md" -exec grep -l "^status: unread" {} \; 2>/dev/null | wc -l)
if [[ "$UNREAD" -gt 0 ]]; then
  echo "  📬 $UNREAD unread message(s)"
else
  echo "  ✅ Inbox clean"
fi

# 4. Watch cron status
echo "[4/4] Watch cron status..."
WATCH_CRON=$(openclaw cron list 2>/dev/null | grep "agent-bus-watch" || echo "")
if [[ -n "$WATCH_CRON" ]]; then
  echo "  ✅ Watch cron registered"
else
  echo "  ⚠️  Watch cron not found — run scripts/setup-watch-cron.sh to register"
fi

echo ""
echo "=== Done ==="
