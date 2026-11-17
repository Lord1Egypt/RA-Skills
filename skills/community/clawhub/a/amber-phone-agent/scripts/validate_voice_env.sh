#!/usr/bin/env bash
set -euo pipefail

# Lightweight preflight for Amber Voice Assistant deployments.
# Safe: prints missing values only (never prints secret contents).

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_dir="$(cd "$script_dir/.." && pwd)"
runtime_dir="$skill_dir/runtime"
crm_dir="$skill_dir/amber-skills/crm"

if [[ -f "$runtime_dir/.env" ]]; then
  while IFS='=' read -r key value; do
    [[ "$key" =~ ^[A-Z0-9_]+$ ]] || continue
    case "$key" in
      TWILIO_ACCOUNT_SID|TWILIO_AUTH_TOKEN|TWILIO_CALLER_ID|OPENAI_API_KEY|OPENAI_PROJECT_ID|OPENAI_WEBHOOK_SECRET|PUBLIC_BASE_URL|OPENCLAW_GATEWAY_URL|OPENCLAW_GATEWAY_TOKEN|AMBER_REALTIME_MODEL|AMBER_REALTIME_VAD_THRESHOLD|AMBER_REALTIME_VAD_PREFIX_PADDING_MS|AMBER_REALTIME_VAD_SILENCE_DURATION_MS|AMBER_CRM_ENABLED|AMBER_CRM_TRANSCRIPT_ENRICHMENT)
        value="${value%$'\r'}"
        value="${value%\"}"
        value="${value#\"}"
        export "$key=$value"
        ;;
    esac
  done < "$runtime_dir/.env"
fi

required=(
  TWILIO_ACCOUNT_SID
  TWILIO_AUTH_TOKEN
  TWILIO_CALLER_ID
  OPENAI_API_KEY
  OPENAI_PROJECT_ID
  OPENAI_WEBHOOK_SECRET
  PUBLIC_BASE_URL
)

optional=(
  OPENCLAW_GATEWAY_URL
  OPENCLAW_GATEWAY_TOKEN
  AMBER_REALTIME_MODEL
  AMBER_REALTIME_VAD_THRESHOLD
  AMBER_REALTIME_VAD_PREFIX_PADDING_MS
  AMBER_REALTIME_VAD_SILENCE_DURATION_MS
  AMBER_CRM_ENABLED
  AMBER_CRM_TRANSCRIPT_ENRICHMENT
)

missing=0

echo "[amber-voice-assistant] Checking required env vars..."
for key in "${required[@]}"; do
  if [[ -z "${!key:-}" ]]; then
    echo "  ✗ missing: $key"
    missing=1
  else
    echo "  ✓ $key"
  fi
done

echo "[amber-voice-assistant] Checking optional env vars..."
for key in "${optional[@]}"; do
  if [[ -z "${!key:-}" ]]; then
    echo "  - not set: $key"
  else
    echo "  ✓ $key"
  fi
done

echo "[amber-voice-assistant] Tool checks..."
if command -v node >/dev/null 2>&1; then
  echo "  ✓ node $(node -v)"
else
  echo "  ✗ node missing"
  missing=1
fi

if command -v openclaw >/dev/null 2>&1; then
  echo "  ✓ openclaw $(openclaw --version | head -n1)"
else
  echo "  - openclaw CLI not found in PATH"
fi

if [[ "${AMBER_CRM_ENABLED:-false}" == "true" ]]; then
  echo "[amber-voice-assistant] CRM dependency check..."
  if (cd "$crm_dir" && node -e "require('better-sqlite3')" >/dev/null 2>&1); then
    echo "  ✓ CRM SQLite dependency loads"
  else
    echo "  ✗ CRM SQLite dependency failed to load"
    echo "    Run: cd amber-skills/crm && npm install"
    echo "    If Node was upgraded, run: cd amber-skills/crm && npm rebuild better-sqlite3"
    missing=1
  fi
fi

if [[ "$missing" -eq 1 ]]; then
  echo "[amber-voice-assistant] Preflight failed. Set missing required env vars."
  exit 1
fi

echo "[amber-voice-assistant] Preflight passed."
