#!/usr/bin/env bash
echo "DEPRECATED: This skill is no longer maintained. Use x402janus skill instead." && exit 1

set -euo pipefail

API_BASE_DEFAULT="https://x402pulse.xyz"
API_BASE="${API_BASE:-$API_BASE_DEFAULT}"

curl -sS -f \
  --connect-timeout "${CONNECT_TIMEOUT:-10}" \
  --max-time "${MAX_TIME:-30}" \
  "$API_BASE/api/config"
