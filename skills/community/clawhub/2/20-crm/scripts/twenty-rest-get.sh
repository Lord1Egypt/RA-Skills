#!/bin/bash
set -euo pipefail

# Usage: twenty-rest-get.sh "/companies" [key=value ...]
# Example: twenty-rest-get.sh "/companies" "limit=10" "offset=0"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/twenty-config.sh"

PATH_PART="${1:-}"

if [ -z "$PATH_PART" ]; then
  echo "Usage: twenty-rest-get.sh \"/path\" [key=value ...]" >&2
  exit 1
fi
validate_rest_path "$PATH_PART"

URL="$TWENTY_BASE_URL/rest${PATH_PART}"
CURL_ARGS=()
if [ "$#" -gt 1 ]; then
  for param in "${@:2}"; do
    if [[ "$param" != *=* ]]; then
      echo "Invalid query parameter '$param'. Expected key=value." >&2
      exit 1
    fi
    key="${param%%=*}"
    value="${param#*=}"
    if [[ -z "$key" || ! "$key" =~ ^[A-Za-z0-9._~-]+$ ]]; then
      echo "Invalid query parameter name '$key'." >&2
      exit 1
    fi
    CURL_ARGS+=(--data-urlencode "$key=$value")
  done
fi

curl -sS -G "$URL" "${CURL_ARGS[@]}" \
  -H "Authorization: Bearer $TWENTY_API_KEY" \
  -H "Accept: application/json"
