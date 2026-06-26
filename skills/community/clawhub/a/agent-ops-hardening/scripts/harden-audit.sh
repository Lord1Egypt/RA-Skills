#!/bin/bash
# harden-audit.sh — Quick audit of common hardening gaps in an OpenClaw workspace
# Usage: bash scripts/harden-audit.sh [workspace_dir]

WORKSPACE="${1:-$(pwd)}"
ISSUES=0

echo "🔍 Agent Ops Hardening Audit"
echo "Workspace: $WORKSPACE"
echo "---"

# 1. Check MEMORY.md line count
if [ -f "$WORKSPACE/MEMORY.md" ]; then
  LINES=$(wc -l < "$WORKSPACE/MEMORY.md")
  if [ "$LINES" -gt 200 ]; then
    echo "⚠️  MEMORY.md is $LINES lines (target: <200). Trim to reduce token burn."
    ISSUES=$((ISSUES+1))
  else
    echo "✅ MEMORY.md is $LINES lines (under 200)"
  fi
else
  echo "⚠️  No MEMORY.md found"
  ISSUES=$((ISSUES+1))
fi

# 2. Check for SOUL.md
if [ -f "$WORKSPACE/SOUL.md" ]; then
  echo "✅ SOUL.md exists"
else
  echo "⚠️  No SOUL.md — agent has no identity"
  ISSUES=$((ISSUES+1))
fi

# 3. Check for USER.md
if [ -f "$WORKSPACE/USER.md" ]; then
  echo "✅ USER.md exists"
else
  echo "⚠️  No USER.md — agent doesn't know who it's helping"
  ISSUES=$((ISSUES+1))
fi

# 4. Check for HEARTBEAT.md
if [ -f "$WORKSPACE/HEARTBEAT.md" ]; then
  echo "✅ HEARTBEAT.md exists"
  if grep -q "heartbeat-state" "$WORKSPACE/HEARTBEAT.md"; then
    echo "✅ Heartbeat state gating configured"
  else
    echo "⚠️  No heartbeat-state.json gating — heartbeats may re-check unnecessarily"
    ISSUES=$((ISSUES+1))
  fi
else
  echo "⚠️  No HEARTBEAT.md — agent has no proactive check routine"
  ISSUES=$((ISSUES+1))
fi

# 5. Check for trash CLI
if command -v trash &>/dev/null; then
  echo "✅ trash CLI available"
else
  echo "⚠️  trash CLI not installed — rm is the only delete path (dangerous)"
  ISSUES=$((ISSUES+1))
fi

# 6. Check for daily notes directory
if [ -d "$WORKSPACE/memory" ] || [ -d "$(dirname "$WORKSPACE")/rick-vault/memory" ]; then
  echo "✅ Daily notes directory exists"
else
  echo "⚠️  No memory/ directory — agent has no daily note system"
  ISSUES=$((ISSUES+1))
fi

# 7. Check TOOLS.md for session rotation
if [ -f "$WORKSPACE/TOOLS.md" ]; then
  if grep -qi "session rotation\|rotate.*session" "$WORKSPACE/TOOLS.md"; then
    echo "✅ Session rotation protocol documented"
  else
    echo "⚠️  No session rotation protocol in TOOLS.md"
    ISSUES=$((ISSUES+1))
  fi
fi

# 8. Check for heartbeat-state.json
STATE_FILE=""
for p in "$WORKSPACE/memory/heartbeat-state.json" "$WORKSPACE/../rick-vault/control/heartbeat-state.json" "$HOME/rick-vault/control/heartbeat-state.json"; do
  if [ -f "$p" ]; then STATE_FILE="$p"; break; fi
done
if [ -n "$STATE_FILE" ]; then
  echo "✅ heartbeat-state.json found at $STATE_FILE"
else
  echo "⚠️  No heartbeat-state.json — heartbeats have no interval gating"
  ISSUES=$((ISSUES+1))
fi

echo ""
echo "---"
if [ "$ISSUES" -eq 0 ]; then
  echo "✅ All checks passed. Workspace is hardened."
else
  echo "⚠️  $ISSUES issue(s) found. Review and fix above."
fi
