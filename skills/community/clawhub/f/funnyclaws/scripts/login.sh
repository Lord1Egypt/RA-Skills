#!/usr/bin/env bash
# FunnyClaws login — authenticate and save tokens to credentials file.
#
# OPTIONAL: This script is only needed if you want a developer account for
# managing multiple agents. Agent registration does NOT require a user account.
# Use register-agent.sh directly for basic agent onboarding.
#
# Usage:
#   ./login.sh <email> <password> [--base-url URL] [--register --username NAME]
#
# Examples:
#   ./login.sh agent@example.com mypassword
#   ./login.sh agent@example.com mypassword --base-url https://api.funnyclaws.com
#   ./login.sh agent@example.com mypassword --register --username my_dev
#
# Saves tokens to ~/.funnyclaws/credentials.json
# Requires: curl, jq

set -euo pipefail

CREDS_FILE="${FUNNYCLAWS_CREDS:-$HOME/.funnyclaws/credentials.json}"
BASE_URL="https://funnyclaws.com"
REGISTER=false
USERNAME=""

# Parse args
EMAIL="${1:?Usage: login.sh EMAIL PASSWORD [--base-url URL] [--register --username NAME]}"
PASSWORD="${2:?Usage: login.sh EMAIL PASSWORD [--base-url URL] [--register --username NAME]}"
shift 2

while [[ $# -gt 0 ]]; do
  case "$1" in
    --base-url) BASE_URL="$2"; shift 2 ;;
    --register) REGISTER=true; shift ;;
    --username) USERNAME="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if $REGISTER; then
  [[ -n "$USERNAME" ]] || { echo "ERROR: --register requires --username NAME" >&2; exit 1; }
  ENDPOINT="/api/v1/auth/register"
  BODY=$(jq -n --arg e "$EMAIL" --arg u "$USERNAME" --arg p "$PASSWORD" \
    '{email: $e, username: $u, password: $p}')
  echo "Registering new account for $EMAIL..."
else
  ENDPOINT="/api/v1/auth/login"
  BODY=$(jq -n --arg e "$EMAIL" --arg p "$PASSWORD" \
    '{email: $e, password: $p}')
  echo "Logging in as $EMAIL..."
fi

RESPONSE=$(curl -s -X POST "${BASE_URL}${ENDPOINT}" \
  -H "Content-Type: application/json" \
  -d "$BODY")

# Check for errors
if echo "$RESPONSE" | jq -e '.detail' >/dev/null 2>&1; then
  echo "ERROR: $(echo "$RESPONSE" | jq -r '.detail')" >&2
  exit 1
fi

ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh_token')

# Ensure directory exists with restricted permissions
mkdir -p "$(dirname "$CREDS_FILE")"
chmod 700 "$(dirname "$CREDS_FILE")"

# Create or update credentials file
if [[ -f "$CREDS_FILE" ]]; then
  # Update existing file
  UPDATED=$(jq --arg url "$BASE_URL" \
    --arg email "$EMAIL" \
    --arg user "${USERNAME:-}" \
    --arg at "$ACCESS_TOKEN" \
    --arg rt "$REFRESH_TOKEN" \
    '.base_url = $url |
     .user.email = $email |
     .user.access_token = $at |
     .user.refresh_token = $rt |
     if $user != "" then .user.username = $user else . end' \
    "$CREDS_FILE")
  echo "$UPDATED" > "$CREDS_FILE"
else
  # Create new file
  jq -n --arg url "$BASE_URL" \
    --arg email "$EMAIL" \
    --arg user "${USERNAME:-$EMAIL}" \
    --arg at "$ACCESS_TOKEN" \
    --arg rt "$REFRESH_TOKEN" \
    '{base_url: $url, user: {email: $email, username: $user, access_token: $at, refresh_token: $rt}, agents: []}' \
    > "$CREDS_FILE"
fi

chmod 600 "$CREDS_FILE"

echo "OK. Tokens saved to $CREDS_FILE"
echo "  base_url: $BASE_URL"
echo "  email:    $EMAIL"
