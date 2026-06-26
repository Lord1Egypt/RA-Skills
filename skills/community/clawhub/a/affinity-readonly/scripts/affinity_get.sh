#!/usr/bin/env bash
set -euo pipefail

# Read-only Affinity GET helper
# Usage:
#   affinity_get.sh "/companies" "page_size=25"

if [[ "${1:-}" == "" ]]; then
  echo "Usage: $0 <endpoint-path> [query]" >&2
  exit 2
fi

if [[ -z "${AFFINITY_API_KEY:-}" ]]; then
  echo "AFFINITY_API_KEY is not set" >&2
  exit 3
fi

endpoint="$1"
query="${2:-}"
base="${AFFINITY_API_BASE:-https://api.affinity.co}"

if [[ "$endpoint" != /* ]]; then
  echo "Endpoint must start with / (example: /companies)" >&2
  exit 2
fi

# Prevent accidental non-GET by only supporting this script + curl GET invocation.
url="${base}${endpoint}"
if [[ -n "$query" ]]; then
  url+="?${query}"
fi

# Use Bearer token auth for Affinity API.
# Do not echo command with key.
resp="$(curl -fsS --get \
  -H "Accept: application/json" \
  -H "Authorization: Bearer ${AFFINITY_API_KEY}" \
  "$url")"

if command -v jq >/dev/null 2>&1; then
  printf '%s' "$resp" | jq .
else
  printf '%s\n' "$resp"
fi
