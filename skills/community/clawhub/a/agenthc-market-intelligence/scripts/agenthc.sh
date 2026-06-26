#!/usr/bin/env bash
# Stock Market Intelligence CLI helper
# Usage: agenthc.sh <endpoint> [--ticker TICKER] [--format FORMAT]
#
# Requires: AGENTHC_API_KEY environment variable
# Example: agenthc.sh overview
# Example: agenthc.sh equities --ticker AAPL --format agent

set -euo pipefail

BASE_URL="https://api.traderhc.com"

if [ -z "${AGENTHC_API_KEY:-}" ]; then
  echo "Error: AGENTHC_API_KEY not set" >&2
  echo "Register: curl -s -X POST '$BASE_URL/api/v1/register' -H 'Content-Type: application/json' -d '{\"name\": \"MyAgent\"}'" >&2
  exit 1
fi

ENDPOINT="${1:-}"
if [ -z "$ENDPOINT" ]; then
  echo "Usage: agenthc.sh <endpoint> [--ticker TICKER] [--format FORMAT]" >&2
  echo "See api.traderhc.com/docs for available endpoints." >&2
  exit 1
fi

# Sanitize inputs: only allow alphanumeric, underscore, hyphen
if [[ ! "$ENDPOINT" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Error: Invalid endpoint name" >&2
  exit 1
fi

shift

# Parse optional arguments
TICKER=""
FORMAT="compact"
while [ $# -gt 0 ]; do
  case "$1" in
    --ticker) TICKER="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Sanitize ticker and format
if [ -n "$TICKER" ] && [[ ! "$TICKER" =~ ^[a-zA-Z0-9._-]+$ ]]; then
  echo "Error: Invalid ticker" >&2
  exit 1
fi
if [[ ! "$FORMAT" =~ ^[a-zA-Z0-9_-]+$ ]]; then
  echo "Error: Invalid format" >&2
  exit 1
fi

# Build URL with sanitized inputs
URL="$BASE_URL/api/v1/data/$ENDPOINT?format=$FORMAT"
if [ -n "$TICKER" ]; then
  URL="$URL&ticker=$TICKER"
fi

curl -s "$URL" -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
