#!/usr/bin/env bash
set -euo pipefail

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

command -v pbpaste >/dev/null 2>&1 ||
  fail "Receipt OAuth completion requires pbpaste on macOS."
command -v openclaw >/dev/null 2>&1 ||
  fail "OpenClaw is not available on PATH."

callback_url="$(pbpaste)" ||
  fail "Could not read the clipboard."

case "$callback_url" in
  http://127.0.0.1:8989/oauth/callback\?* | http://localhost:8989/oauth/callback\?*) ;;
  *) fail "Clipboard does not contain a valid OpenClaw Receipt callback URL." ;;
esac

query="${callback_url#*\?}"
query="${query%%\#*}"
code=""

IFS='&' read -r -a parameters <<<"$query"
for parameter in "${parameters[@]}"; do
  if [[ "$parameter" == code=* ]]; then
    code="${parameter#code=}"
    break
  fi
done

[[ -n "$code" ]] ||
  fail "Clipboard callback URL has no authorization code."

case "$code" in
  *[!A-Za-z0-9._~-]*) fail "Clipboard callback contains a malformed authorization code." ;;
esac

exec openclaw mcp login receipt --code "$code"
