#!/bin/bash
# Shared config for Cin7 Core API scripts
# Sources .env from the project root

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$SKILL_DIR/.env"

if [ -f "$ENV_FILE" ]; then
  # Read .env safely, stripping any Windows \r characters
  while IFS='=' read -r key value; do
    key=$(echo "$key" | tr -d '\r')
    value=$(echo "$value" | tr -d '\r')
    [ -n "$key" ] && [[ ! "$key" =~ ^# ]] && export "$key=$value"
  done < "$ENV_FILE"
fi

CIN7_API_URL="${CIN7_API_URL:-https://inventory.dearsystems.com/ExternalApi/v2}"
CIN7_ACCOUNT_ID="${CIN7_ACCOUNT_ID:?CIN7_ACCOUNT_ID is required}"
CIN7_APP_KEY="${CIN7_APP_KEY:-$CIN7_API_KEY}"
CIN7_APP_KEY="${CIN7_APP_KEY:?CIN7_APP_KEY or CIN7_API_KEY is required}"

cin7_get() {
  local endpoint="$1"
  shift
  curl -s -f \
    -H "api-auth-accountid: $CIN7_ACCOUNT_ID" \
    -H "api-auth-applicationkey: $CIN7_APP_KEY" \
    -H "Content-Type: application/json" \
    "${CIN7_API_URL}/${endpoint}$@"
}

cin7_post() {
  local endpoint="$1"
  local data="$2"
  curl -s -f \
    -X POST \
    -H "api-auth-accountid: $CIN7_ACCOUNT_ID" \
    -H "api-auth-applicationkey: $CIN7_APP_KEY" \
    -H "Content-Type: application/json" \
    -d "$data" \
    "${CIN7_API_URL}/${endpoint}"
}

cin7_put() {
  local endpoint="$1"
  local data="$2"
  curl -s -f \
    -X PUT \
    -H "api-auth-accountid: $CIN7_ACCOUNT_ID" \
    -H "api-auth-applicationkey: $CIN7_APP_KEY" \
    -H "Content-Type: application/json" \
    -d "$data" \
    "${CIN7_API_URL}/${endpoint}"
}
