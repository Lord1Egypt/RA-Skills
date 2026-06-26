#!/bin/bash
# DataGuard DLP — sessions_send Tool Hook
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Intercepts sessions_send calls and scans for sensitive data
# Called by OpenClaw before sessions_send executes
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
DLP_SCAN="$SKILL_DIR/scripts/dlp-scan.sh"
CONTEXT_TRACK="$SKILL_DIR/scripts/context-track.sh"
AUDIT_LOG="$SKILL_DIR/scripts/audit-log.sh"

# Read stdin for tool call parameters
INPUT=$(cat)

# Extract message content — using sed instead of grep -oP
MESSAGE=$(echo "$INPUT" | sed -n 's/.*"message"\s*:\s*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$MESSAGE" ]; then
  # No message content to check
  echo "$INPUT"
  exit 0
fi

# Extract session key or label — using sed instead of grep -oP
SESSION=$(echo "$INPUT" | sed -n 's/.*"\(sessionKey\|label\)"\s*:\s*"\([^"]*\)".*/\2/p' | head -1)
[ -z "$SESSION" ] && SESSION="unknown"

# Check context score first (important for sessions_send)
CONTEXT_SCORE=$("$CONTEXT_TRACK" --score 2>/dev/null || echo "0")

# Scan message for sensitive patterns
RISK_OUTPUT=$(echo "$MESSAGE" | "$DLP_SCAN" 2>&1) || RISK_SCORE=$?
RISK_SCORE=${RISK_SCORE:-0}

# Add context risk
TOTAL_SCORE=$((RISK_SCORE + CONTEXT_SCORE / 2))

if [ "$TOTAL_SCORE" -ge 6 ]; then
  echo "🚫 DataGuard: BLOCKED message to session" >&2
  echo "Session: $SESSION" >&2
  echo "" >&2
  echo "$RISK_OUTPUT" >&2
  if [ "$CONTEXT_SCORE" -gt 0 ]; then
    echo "" >&2
    echo "Context Risk: +$((CONTEXT_SCORE / 2)) (recent sensitive file reads)" >&2
  fi
  echo "" >&2
  echo "Total Risk Score: $TOTAL_SCORE" >&2
  echo "" >&2
  echo "REASON: Message contains sensitive data (credentials, PII, or internal references)" >&2
  echo "" >&2
  echo "To allow this message, explicitly approve it." >&2
  
  # Never log raw message — always redact
  "$AUDIT_LOG" --log-block "sessions_send" "$SESSION" "SENSITIVE_MESSAGE" "$TOTAL_SCORE" "[REDACTED]" >&2
  exit "$TOTAL_SCORE"
fi

if [ "$TOTAL_SCORE" -ge 3 ]; then
  echo "⚠️  DataGuard: WARNING - suspicious message content" >&2
  echo "Session: $SESSION" >&2
  echo "Risk Score: $TOTAL_SCORE" >&2
  echo "" >&2
  echo "$RISK_OUTPUT" >&2
fi

# Check for code blocks containing credentials
if echo "$MESSAGE" | grep -qiE '```(json|yaml|env|bash|shell).*?(password|api[_-]?key|secret|token|credential)'; then
  echo "🚫 DataGuard: BLOCKED - credentials detected in code block" >&2
  echo "Session: $SESSION" >&2
  echo "REASON: Message contains code block with credential patterns" >&2
  "$AUDIT_LOG" --log-block "sessions_send" "$SESSION" "CREDENTIALS_IN_CODE" "8" "[REDACTED]" >&2
  exit 8
fi

# Allow the message
echo "$INPUT"
exit 0