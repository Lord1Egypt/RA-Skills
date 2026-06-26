#!/bin/bash
# bitwarden-credential.sh — Store a credential in Bitwarden via CLI
# Usage: ./bitwarden-credential.sh <name> <username> <password> [notes]
# Requires: BW_SESSION env var (run `bw unlock` first to get it)

set -e

if ! command -v bw &>/dev/null; then
  echo "ERROR: Bitwarden CLI (bw) not found. Install from: https://bitwarden.com/download"
  exit 1
fi

if [ -z "$BW_SESSION" ]; then
  echo "ERROR: BW_SESSION not set."
  echo ""
  echo "1. In your terminal, run: bw unlock"
  echo "2. Copy the session key from the output"
  echo "3. Provide it to me, then I can store the credential"
  exit 1
fi

NAME="${1:-}"
USERNAME="${2:-}"
PASSWORD="${3:-}"
NOTES="${4:-}"

if [ -z "$NAME" ] || [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
  echo "Usage: bitwarden-credential.sh <name> <username> <password> [notes]"
  exit 1
fi

# Build JSON and base64-encode it (bw create item requires base64 input)
# Use jq to safely escape all fields; notes on single line (comma-separated)
if [ -n "$NOTES" ]; then
  ITEM_B64=$(jq -n \
    --arg name "$NAME" \
    --arg username "$USERNAME" \
    --arg password "$PASSWORD" \
    --arg notes "$NOTES" \
    '{
      name: $name,
      type: 1,
      login: { uris: [], username: $username, password: $password },
      notes: $notes,
      favorite: false
    }' | base64 | tr -d '\n')
else
  ITEM_B64=$(jq -n \
    --arg name "$NAME" \
    --arg username "$USERNAME" \
    --arg password "$PASSWORD" \
    '{
      name: $name,
      type: 1,
      login: { uris: [], username: $username, password: $password },
      favorite: false
    }' | base64 | tr -d '\n')
fi

echo "Storing: $NAME"
echo "$ITEM_B64" | bw create item --session "$BW_SESSION"
echo "Done."
