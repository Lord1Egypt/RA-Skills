#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

command -v openclaw >/dev/null 2>&1 ||
  fail "OpenClaw is not available on PATH."

if ! openclaw mcp show receipt --json >/dev/null 2>&1; then
  openclaw mcp set receipt \
    '{"url":"https://receiptprotocol.com/mcp","transport":"streamable-http","auth":"oauth","supportsParallelToolCalls":false}'
fi
openclaw mcp tools receipt --include 'receipt_*'

login_output=""
if ! login_output="$(openclaw mcp login receipt 2>&1)"; then
  fail "OpenClaw could not start the Receipt OAuth authorization attempt."
fi

authorization_url=""
while IFS= read -r line; do
  if [[ "$line" =~ (https://receiptprotocol\.com/api/public/oauth/authorize\?[^[:space:]]+) ]]; then
    authorization_url="${BASH_REMATCH[1]}"
    break
  fi
done <<<"$login_output"

[[ -n "$authorization_url" ]] ||
  fail "OpenClaw started Receipt login but produced no authorization URL. Do not continue to callback completion."

printf '%s\n' \
  "RECEIPT_AUTHORIZATION_URL_BEGIN" \
  "$authorization_url" \
  "RECEIPT_AUTHORIZATION_URL_END" \
  "" \
  "Open that complete URL and approve Receipt." \
  "After approval, copy the entire localhost callback URL from the browser address bar." \
  "Then run:" \
  "bash ~/.openclaw/workspace/skills/get-with-receipt/scripts/complete-oauth-from-clipboard.sh"
