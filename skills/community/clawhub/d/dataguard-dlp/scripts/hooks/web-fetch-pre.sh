#!/bin/bash
# DataGuard DLP — web_fetch Tool Hook
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Intercepts web_fetch calls and scans for sensitive data
# Called by OpenClaw before web_fetch executes
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
DLP_SCAN="$SKILL_DIR/scripts/dlp-scan.sh"
DOMAIN_CHECK="$SKILL_DIR/scripts/domain-allowlist.sh"
CONTEXT_TRACK="$SKILL_DIR/scripts/context-track.sh"
AUDIT_LOG="$SKILL_DIR/scripts/audit-log.sh"

# Read stdin for tool call parameters
INPUT=$(cat)

# Extract URL from parameters (using sed instead of grep -oP)
URL=$(echo "$INPUT" | sed -n 's/.*"url"\s*:\s*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$URL" ]; then
  # No URL to check, allow
  echo "$INPUT"
  exit 0
fi

# Extract domain from URL
DOMAIN=$(echo "$URL" | sed -E 's|https?://([^/]+).*|\1|' | sed 's/:.*//')

# Check domain allowlist
DOMAIN_RESULT=$("$DOMAIN_CHECK" --check "$DOMAIN" 2>&1) || true

if echo "$DOMAIN_RESULT" | grep -q "BLOCKED"; then
  echo "🚫 DataGuard: Blocked request to high-risk domain" >&2
  echo "Domain: $DOMAIN" >&2
  echo "Reason: Domain is in blocklist (pastebin, webhook, etc.)" >&2
  "$AUDIT_LOG" --log-block "web_fetch" "$DOMAIN" "BLOCKED_DOMAIN" "10" "$URL" >&2
  exit 10
fi

# Check for POST/PUT data (body parameter) — using sed instead of grep -oP
BODY=$(echo "$INPUT" | sed -n 's/.*"\(body\|data\|payload\)"\s*:\s*"\([^"]*\)".*/\2/p' | head -1)

if [ -n "$BODY" ]; then
  # Scan body for sensitive patterns
  RISK_OUTPUT=$(echo "$BODY" | "$DLP_SCAN" 2>&1) || RISK_SCORE=$?
  RISK_SCORE=${RISK_SCORE:-0}
  
  if [ "$RISK_SCORE" -ge 6 ]; then
    echo "🚫 DataGuard: Blocked sensitive data transfer" >&2
    echo "URL: $URL" >&2
    echo "" >&2
    echo "$RISK_OUTPUT" >&2
    # Redact body preview in log — never log raw body content
    "$AUDIT_LOG" --log-block "web_fetch" "$DOMAIN" "SENSITIVE_DATA" "$RISK_SCORE" "[REDACTED]" >&2
    exit "$RISK_SCORE"
  fi
  
  if [ "$RISK_SCORE" -ge 3 ]; then
    echo "⚠️  DataGuard: Warning - suspicious patterns detected" >&2
    echo "URL: $URL" >&2
    echo "Risk Score: $RISK_SCORE" >&2
    echo "" >&2
    echo "$RISK_OUTPUT" >&2
    # Log warning — no raw body in logs
    "$AUDIT_LOG" --log-block "web_fetch" "$DOMAIN" "WARN" "$RISK_SCORE" "[REDACTED]" >&2 || true
  fi
fi

# Check context score (recent sensitive file reads)
CONTEXT_SCORE=$("$CONTEXT_TRACK" --score 2>/dev/null || echo "0")

if [ "$CONTEXT_SCORE" -ge 5 ]; then
  echo "⚠️  DataGuard: Elevated context risk detected" >&2
  echo "Recent sensitive file reads detected (score: $CONTEXT_SCORE)" >&2
  echo "This may indicate data exfiltration attempt." >&2
  echo "" >&2
  echo "If this is legitimate, approve the request." >&2
  echo "" >&2
fi

# Allow the request
echo "$INPUT"
exit 0