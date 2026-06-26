#!/usr/bin/env bash
set -euo pipefail

echo "[facebook-hybrid-operator] Environment check"

GRAPH_VERSION="${FACEBOOK_GRAPH_VERSION:-v22.0}"
TOKEN_STATUS="missing"
PAGE_STATUS="missing"

if [ -n "${FACEBOOK_PAGE_ACCESS_TOKEN:-}" ]; then
  TOKEN_STATUS="configured"
fi

if [ -n "${FACEBOOK_PAGE_ID:-}" ]; then
  PAGE_STATUS="configured"
fi

echo "GRAPH_VERSION=${GRAPH_VERSION}"
echo "FACEBOOK_PAGE_ACCESS_TOKEN=${TOKEN_STATUS}"
echo "FACEBOOK_PAGE_ID=${PAGE_STATUS}"

if [ "$TOKEN_STATUS" = "configured" ] && [ "$PAGE_STATUS" = "configured" ]; then
  echo "API path looks ready for basic Page posting."
else
  echo "API path is not fully configured yet. Browser automation can still be used."
fi
