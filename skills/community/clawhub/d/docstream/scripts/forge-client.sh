#!/bin/bash
set -euo pipefail
API_BASE="${DOCSTREAM_API_URL:-https://anton.vosscg.com}"
API_KEY="${DOCSTREAM_API_KEY:-}"
EMAIL="${DOCSTREAM_EMAIL:-}"
if [ -z "$API_KEY" ] && [ -n "$EMAIL" ]; then
  RESP=$(curl -sf -X POST "$API_BASE/v1/keys" -H "Content-Type: application/json" -d "{\"email\": \"$EMAIL\"}")
  API_KEY=$(echo "$RESP" | grep -o '"api_key":"[^"]*"' | cut -d'"' -f4)
  [ -n "$API_KEY" ] && echo "✅ Free key: $API_KEY" >&2 || { echo "❌ Signup failed" >&2; exit 1; }
fi
[ -z "$API_KEY" ] && { echo "❌ Set DOCSTREAM_API_KEY or DOCSTREAM_EMAIL" >&2; exit 1; }
ACTION="${1:-help}"; shift || true
case "$ACTION" in
  process) curl -sf -X POST "$API_BASE/v1/documents/process" -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" -d "$1" ;;
  health) curl -sf "$API_BASE/v1/health" ;;
  *) echo "DocStream: process '<json>' | health" ;;
esac
