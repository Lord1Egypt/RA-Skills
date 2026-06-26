#!/bin/bash
# DataGuard DLP — exec Tool Hook
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Intercepts exec calls for outbound commands (curl, wget, nc, etc.)
# Called by OpenClaw before exec executes
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
DLP_SCAN="$SKILL_DIR/scripts/dlp-scan.sh"
DOMAIN_CHECK="$SKILL_DIR/scripts/domain-allowlist.sh"
CONTEXT_TRACK="$SKILL_DIR/scripts/context-track.sh"
AUDIT_LOG="$SKILL_DIR/scripts/audit-log.sh"

# Read stdin for tool call parameters
INPUT=$(cat)

# Extract command — using sed instead of grep -oP
COMMAND=$(echo "$INPUT" | sed -n 's/.*"command"\s*:\s*"\([^"]*\)".*/\1/p' | head -1)

if [ -z "$COMMAND" ]; then
  echo "$INPUT"
  exit 0
fi

# High-risk outbound commands
OUTBOUND_COMMANDS=("curl" "wget" "nc" "netcat" "rsync" "scp" "sftp" "ftp" "ssh" "telnet")

IS_OUTBOUND=0
CMD_BASE=$(echo "$COMMAND" | awk '{print $1}' | sed 's|.*/||')

for cmd in "${OUTBOUND_COMMANDS[@]}"; do
  if [ "$CMD_BASE" = "$cmd" ]; then
    IS_OUTBOUND=1
    break
  fi
done

# Check for pipe chains that include outbound
if echo "$COMMAND" | grep -qE '\|.*\b(curl|wget|nc|netcat)\b'; then
  IS_OUTBOUND=1
fi

if [ "$IS_OUTBOUND" -eq 0 ]; then
  # Not an outbound command, allow
  echo "$INPUT"
  exit 0
fi

# ── OUTBOUND COMMAND DETECTED ────────────────────────────────────────

echo "🔍 DataGuard: Detected outbound command: $CMD_BASE" >&2

# Extract URLs/domains from command
URLS=$(echo "$COMMAND" | grep -oE 'https?://[^ ]+' || echo "")
DOMAINS=$(echo "$COMMAND" | grep -oE '[-a-zA-Z0-9.]+\.[a-zA-Z]{2,}' | grep -vE '^(localhost|127\.0\.0\.1|0\.0\.0\.0)$' || echo "")

# Check domains against allowlist
if [ -n "$DOMAINS" ]; then
  while read -r domain; do
    DOMAIN_RESULT=$("$DOMAIN_CHECK" --check "$domain" 2>&1) || true
    
    if echo "$DOMAIN_RESULT" | grep -q "BLOCKED"; then
      echo "🚫 DataGuard: BLOCKED outbound request to high-risk domain" >&2
      echo "Domain: $domain" >&2
      echo "Reason: Domain is in blocklist" >&2
      "$AUDIT_LOG" --log-block "exec" "$domain" "BLOCKED_DOMAIN" "10" "[REDACTED]" >&2
      exit 10
    fi
    
    if echo "$DOMAIN_RESULT" | grep -q "UNKNOWN"; then
      echo "⚠️  DataGuard: WARNING - unknown domain in outbound command" >&2
      echo "Domain: $domain" >&2
      echo "This domain is not in the allowlist." >&2
    fi
  done <<< "$DOMAINS"
fi

# Check for data being sent (POST, body, etc.)
if echo "$COMMAND" | grep -qiE '(-d|--data|-X\s*POST|-X\s*PUT|--body)'; then
  # Extract data portion — using sed instead of grep -oP
  DATA=$(echo "$COMMAND" | sed -n 's/.*\(-d\|--data\)\s*["'"'"']*\([^"'"'"']*\).*/\2/p' | head -1)
  
  if [ -n "$DATA" ]; then
    RISK_OUTPUT=$(echo "$DATA" | "$DLP_SCAN" 2>&1) || RISK_SCORE=$?
    RISK_SCORE=${RISK_SCORE:-0}
    
    if [ "$RISK_SCORE" -ge 6 ]; then
      echo "🚫 DataGuard: BLOCKED sensitive data in outbound command" >&2
      echo "" >&2
      echo "$RISK_OUTPUT" >&2
      "$AUDIT_LOG" --log-block "exec" "$CMD_BASE" "SENSITIVE_DATA" "$RISK_SCORE" "[REDACTED]" >&2
      exit "$RISK_SCORE"
    fi
  fi
fi

# Check context (file reads before outbound)
CONTEXT_SCORE=$("$CONTEXT_TRACK" --score 2>/dev/null || echo "0")

if [ "$CONTEXT_SCORE" -ge 5 ]; then
  echo "⚠️  DataGuard: ELEVATED RISK - sensitive file read before outbound command" >&2
  echo "Context Score: $CONTEXT_SCORE" >&2
  echo "" >&2
fi

# Check for file upload patterns — log metadata only, do NOT cat the file
if echo "$COMMAND" | grep -qiE '(--upload-file|-T|--post-file)'; then
  # Extract file path — using sed instead of grep -oP
  FILE_PATH=$(echo "$COMMAND" | sed -n 's/.*\(--upload-file\|-T\|--post-file\)\s*\([^ ]*\).*/\2/p' | head -1)
  
  if [ -n "$FILE_PATH" ]; then
    echo "📁 DataGuard: File upload detected" >&2
    echo "File: $FILE_PATH" >&2
    
    # SECURITY: Do NOT cat the file contents into the scan pipeline.
    # Instead, scan the filename only — the agent already has access
    # and chose to upload; scanning the file would read arbitrary data
    # into a pipeline that could leak it.
    RISK_OUTPUT=$(echo "$FILE_PATH" | "$DLP_SCAN" 2>&1) || RISK_SCORE=$?
    RISK_SCORE=${RISK_SCORE:-0}
    
    if [ "$RISK_SCORE" -ge 3 ]; then
      echo "⚠️  DataGuard: WARNING - filename suggests sensitive content" >&2
      echo "File: $FILE_PATH" >&2
      echo "Risk Score: $RISK_SCORE" >&2
    fi
  fi
fi

# Allow the command with warning
echo "✓ DataGuard: Outbound command allowed (risk assessed)" >&2
echo "$INPUT"
exit 0