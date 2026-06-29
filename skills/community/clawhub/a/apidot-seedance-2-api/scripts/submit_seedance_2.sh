#!/bin/sh
set -eu

api_url="https://api.apidot.ai/api/generate/submit"
payload_file="${1:-}"
body_file=""
tmp_body_file=""

cleanup() {
  if [ -n "$tmp_body_file" ] && [ -f "$tmp_body_file" ]; then
    rm -f "$tmp_body_file"
  fi
}
trap cleanup EXIT INT TERM

if [ -z "${APIDOT_API_KEY:-}" ]; then
  echo "APIDOT_API_KEY is required. Set it in a server-side environment before running this script." >&2
  exit 1
fi

api_key_single_line=$(printf '%s' "$APIDOT_API_KEY" | tr -d '\r\n')
if [ "$api_key_single_line" != "$APIDOT_API_KEY" ]; then
  echo "APIDOT_API_KEY must not contain newline characters." >&2
  exit 1
fi
unset api_key_single_line

if [ -n "$payload_file" ]; then
  if [ ! -f "$payload_file" ]; then
    echo "Payload file not found: $payload_file" >&2
    exit 1
  fi
  body_file="$payload_file"
else
  if [ -t 0 ]; then
    echo "Usage: set APIDOT_API_KEY in the environment, then run scripts/submit_seedance_2.sh [payload.json]" >&2
    echo "Or pipe a reviewed JSON payload through standard input." >&2
    exit 1
  fi
  tmp_body_file=$(mktemp "${TMPDIR:-/tmp}/apidot-seedance-2-payload.XXXXXX")
  body_file="$tmp_body_file"
  chmod 600 "$body_file"
  cat > "$body_file"
fi

{
  printf 'header = "Content-Type: application/json"\n'
  printf 'header = "Authorization: Bearer %s"\n' "$APIDOT_API_KEY"
} | curl -sS "$api_url" --config - --data-binary "@$body_file"
