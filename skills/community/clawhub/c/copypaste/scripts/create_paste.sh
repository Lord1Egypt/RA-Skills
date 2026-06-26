#!/usr/bin/env bash
set -euo pipefail

API_BASE="https://api.copy-paste.cloud"
API_KEY="${COPYPASTE_API_KEY:?COPYPASTE_API_KEY is not set. Generate a key at https://copy-paste.cloud/developer}"

ALLOWED_LANGUAGES="bash c cpp csharp css dockerfile go html java javascript json kotlin markdown php python ruby rust sql swift typescript xml yaml"

# Defaults
CONTENT=""
TITLE=""
LANGUAGE=""
TAGS=""
PRIVATE=false
BURN=false
EXPIRES=""

usage() {
  echo "Usage: create_paste.sh --content <text> [options]" >&2
  echo "" >&2
  echo "Options:" >&2
  echo "  --content <text>           Paste content (required)" >&2
  echo "  --title <text>             Optional title" >&2
  echo "  --language <lang>          Language for syntax highlighting" >&2
  echo "  --tags <tag1,tag2,...>     Comma-separated tags (max 3)" >&2
  echo "  --private                  Make paste private (owner only)" >&2
  echo "  --burn-after-read          Delete after first view" >&2
  echo "  --expires-in-hours <n>     Expire after N hours" >&2
  echo "" >&2
  echo "Allowed languages: ${ALLOWED_LANGUAGES}" >&2
  exit 1
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --content)           CONTENT="$2";          shift 2 ;;
    --title)             TITLE="$2";            shift 2 ;;
    --language)          LANGUAGE="$2";         shift 2 ;;
    --tags)              TAGS="$2";             shift 2 ;;
    --private)           PRIVATE=true;          shift   ;;
    --burn-after-read)   BURN=true;             shift   ;;
    --expires-in-hours)  EXPIRES="$2";          shift 2 ;;
    --help|-h)           usage ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      ;;
  esac
done

# Validate required fields
if [[ -z "$CONTENT" ]]; then
  echo "Error: --content is required." >&2
  usage
fi

# Validate language if provided
if [[ -n "$LANGUAGE" ]]; then
  if ! echo " ${ALLOWED_LANGUAGES} " | grep -qw "$LANGUAGE"; then
    echo "Error: unsupported language '${LANGUAGE}'." >&2
    echo "Allowed: ${ALLOWED_LANGUAGES}" >&2
    exit 1
  fi
fi

# Build JSON payload using jq to handle escaping safely
payload=$(jq -n \
  --arg content   "$CONTENT" \
  --arg title     "$TITLE" \
  --arg language  "$LANGUAGE" \
  --arg tags      "$TAGS" \
  --argjson priv  "$PRIVATE" \
  --argjson burn  "$BURN" \
  --arg expires   "$EXPIRES" \
  '{
    content: $content,
    title:   (if $title    != "" then $title    else null end),
    language:(if $language != "" then $language else null end),
    tags:    (if $tags     != "" then ($tags | split(",") | map(ltrimstr(" ") | rtrimstr(" ")) | map(select(. != ""))) else [] end),
    isPrivate:      $priv,
    burnAfterRead:  $burn,
    expiresInHours: (if $expires != "" then ($expires | tonumber) else null end)
  }')

response=$(curl -sS --fail-with-body \
  -X POST "${API_BASE}/api/v1/pastes" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$payload")

paste_id=$(echo "$response" | jq -r '.id')
echo "Paste created successfully!"
echo "URL: https://copy-paste.cloud/${paste_id}"
echo "ID:  ${paste_id}"
