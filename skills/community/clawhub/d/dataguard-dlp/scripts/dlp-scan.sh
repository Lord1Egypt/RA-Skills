#!/bin/bash
# DataGuard DLP — Pattern Scanner v2.1
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Focused detection for secrets, financial data, and infrastructure
# Usage: echo "$DATA" | bash dlp-scan.sh
# Returns: exit code = risk score (0-10+), stdout = detected patterns
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONTEXT_FILE="$SKILL_DIR/context/sensitive-reads.json"

# Read input from stdin or argument
DATA="${1:-$(cat)}"

# Initialize scoring
RISK_SCORE=0
PATTERNS_FOUND=()

# ══════════════════════════════════════════════════════════════════════
# CRITICAL (Score: 10) — BLOCK IMMEDIATELY
# ══════════════════════════════════════════════════════════════════════

# API Keys (Anthropic, OpenAI, generic)
if echo "$DATA" | grep -qiE 'sk-(ant|proj)?-?[a-zA-Z0-9_-]{20,}'; then
  PATTERNS_FOUND+=("CRITICAL:API_Key")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

if echo "$DATA" | grep -qiE 'ghp_[a-zA-Z0-9]{20,}|gho_[a-zA-Z0-9]{20,}|ghu_[a-zA-Z0-9]{20,}'; then
  PATTERNS_FOUND+=("CRITICAL:GitHub_Token")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

if echo "$DATA" | grep -qiE '(AKIA[A-Z0-9]{16})'; then
  PATTERNS_FOUND+=("CRITICAL:AWS_Access_Key")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

if echo "$DATA" | grep -qiE 'xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9-]+'; then
  PATTERNS_FOUND+=("CRITICAL:Slack_Token")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

if echo "$DATA" | grep -qiE 'xkeysib-[a-zA-Z0-9]+'; then
  PATTERNS_FOUND+=("CRITICAL:Brevo_Token")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

# Bearer/JWT tokens
if echo "$DATA" | grep -qiE 'Bearer [A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+'; then
  PATTERNS_FOUND+=("CRITICAL:Bearer_JWT")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

# Private keys
if echo "$DATA" | grep -q -- '-----BEGIN.*PRIVATE KEY-----'; then
  PATTERNS_FOUND+=("CRITICAL:Private_Key")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

# Database URLs with credentials
if echo "$DATA" | grep -qiE '(mysql://[^:]+:[^@]+@|postgres://[^:]+:[^@]+@|mongodb://[^:]+:[^@]+@|redis://[^:]+:[^@]+@)'; then
  PATTERNS_FOUND+=("CRITICAL:Database_URL")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

# Cloud credentials
if echo "$DATA" | grep -qiE '(aws_secret_access_key|aws_session_token)'; then
  PATTERNS_FOUND+=("CRITICAL:AWS_Secret")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

if echo "$DATA" | grep -qiE '(type.*service_account.*project_id.*private_key)'; then
  PATTERNS_FOUND+=("CRITICAL:GCP_Service_Account")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

# Passwords in configs
if echo "$DATA" | grep -qiE '(password["\s]*[:=]["\s]*[^\s"]{4,}|passwd["\s]*[:=]["\s]*[^\s"]{4,})'; then
  PATTERNS_FOUND+=("CRITICAL:Password")
  RISK_SCORE=$((RISK_SCORE + 10))
fi

# ══════════════════════════════════════════════════════════════════════
# HIGH (Score: 8) — STRONG INDICATORS
# ══════════════════════════════════════════════════════════════════════

# SSN
if echo "$DATA" | grep -qE '\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b'; then
  PATTERNS_FOUND+=("HIGH:SSN")
  RISK_SCORE=$((RISK_SCORE + 8))
fi

# Credit cards
if echo "$DATA" | grep -qE '\b[45][0-9]{12}[0-9]{0,3}\b|\b3[47][0-9]{13}\b|\b6(011|5[0-9]{2})[0-9]{12}\b'; then
  PATTERNS_FOUND+=("HIGH:Credit_Card")
  RISK_SCORE=$((RISK_SCORE + 8))
fi

# CVV
if echo "$DATA" | grep -qiE 'cvv *[=:] *[0-9]|[0-9] *cvv|cvc *[=:] *[0-9]|security.code *[=:] *[0-9]'; then
  PATTERNS_FOUND+=("HIGH:CVV")
  RISK_SCORE=$((RISK_SCORE + 8))
fi

# Internal IPs
if echo "$DATA" | grep -qE '\b(10\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[0-1])|192\.168)\.[0-9]{1,3}\.[0-9]{1,3}\b'; then
  PATTERNS_FOUND+=("HIGH:Internal_IP")
  RISK_SCORE=$((RISK_SCORE + 8))
fi

# Internal hostnames
if echo "$DATA" | grep -qiE '\.(local|internal|corp|lan|home)\b'; then
  PATTERNS_FOUND+=("HIGH:Internal_Hostname")
  RISK_SCORE=$((RISK_SCORE + 8))
fi

# Sensitive paths
if echo "$DATA" | grep -qE '(\.ssh/|/etc/(passwd|shadow)|\.env|\.credentials|\.htpasswd|id_rsa)'; then
  PATTERNS_FOUND+=("HIGH:Sensitive_Path")
  RISK_SCORE=$((RISK_SCORE + 8))
fi

# ══════════════════════════════════════════════════════════════════════
# MEDIUM (Score: 5) — CONTEXT-DEPENDENT
# ══════════════════════════════════════════════════════════════════════

# Phone numbers (US/international)
if echo "$DATA" | grep -qE '(\+?[0-9]{1,3}[-.\ ]?[0-9]{3}[-.\ ]?[0-9]{3}[-.\ ]?[0-9]{4}|\b[0-9]{3}[-.\ ][0-9]{3}[-.\ ][0-9]{4}\b)'; then
  PATTERNS_FOUND+=("MEDIUM:Phone")
  RISK_SCORE=$((RISK_SCORE + 5))
fi

# Email + name combos (PII)
if echo "$DATA" | grep -qiE '([A-Z][a-z]+\s+[A-Z][a-z]+.*[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'; then
  PATTERNS_FOUND+=("MEDIUM:PII_Email_Name")
  RISK_SCORE=$((RISK_SCORE + 5))
fi

# Secrets files
if echo "$DATA" | grep -qiE '(secrets?\.json|credentials\.json|\.pem|\.key|auth\.json)'; then
  PATTERNS_FOUND+=("MEDIUM:Secrets_File")
  RISK_SCORE=$((RISK_SCORE + 5))
fi

# ══════════════════════════════════════════════════════════════════════
# CONTEXT SCORING
# ══════════════════════════════════════════════════════════════════════

CONTEXT_SCORE=0
if [ -f "$SKILL_DIR/scripts/context-track.sh" ]; then
  CONTEXT_SCORE=$(bash "$SKILL_DIR/scripts/context-track.sh" --score 2>/dev/null || echo 0)
  RISK_SCORE=$((RISK_SCORE + CONTEXT_SCORE))
fi

# ══════════════════════════════════════════════════════════════════════
# OUTPUT
# ══════════════════════════════════════════════════════════════════════

if [ ${#PATTERNS_FOUND[@]} -gt 0 ]; then
  echo "⚠️  DataGuard Pattern Detection"
  echo "================================"
  echo "Risk Score: $RISK_SCORE"
  echo ""
  echo "Patterns:"
  for p in "${PATTERNS_FOUND[@]}"; do
    echo "  - $p"
  done
  
  [ -n "$CONTEXT_SCORE" ] && [ "$CONTEXT_SCORE" -gt 0 ] && echo "" && echo "Context: +$CONTEXT_SCORE (recent sensitive reads)"
  
  echo ""
  
  if [ "$RISK_SCORE" -ge 10 ]; then
    echo "🚫 BLOCK: CRITICAL"
    exit "$RISK_SCORE"
  elif [ "$RISK_SCORE" -ge 6 ]; then
    echo "🚫 BLOCK: Requires approval"
    exit "$RISK_SCORE"
  elif [ "$RISK_SCORE" -ge 3 ]; then
    echo "⚠️  WARN: Logging for audit"
    exit "$RISK_SCORE"
  else
    echo "✅ PASS: Low risk"
    exit 0
  fi
else
  echo "✅ DataGuard: No sensitive patterns detected"
  exit 0
fi