#!/usr/bin/env bash
# antenna-relay-exec.sh — Heredoc-free wrapper for antenna-relay.sh
#
# OpenClaw's exec approval system rejects commands containing shell
# metasyntax (pipes, heredocs, command substitution, etc.) even inside
# quotes. To guarantee the exec command string is always clean, the
# caller base64-encodes the raw message and passes it as a single safe
# argument. This wrapper decodes it and pipes to antenna-relay.sh.
#
# Usage (from the Antenna relay agent):
#   bash ../scripts/antenna-relay-exec.sh "<base64-encoded-message>"
#
# The relay agent MUST base64-encode the full raw inbound message before
# calling this script. Output is the same JSON as antenna-relay.sh.
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [[ $# -lt 1 ]]; then
  echo '{"action":"reject","status":"error","reason":"No message argument provided"}'
  exit 0
fi

B64_MESSAGE="$1"
# REF-403: temp file holds plaintext envelope including auth header.
# Create with strict 0600 perms and best-effort wipe on exit.
umask 077
TMPFILE=$(mktemp /tmp/antenna-relay-msg.XXXXXX)
chmod 0600 "$TMPFILE" 2>/dev/null || true

cleanup_tmpfile() {
  if [[ -f "$TMPFILE" ]]; then
    # Best-effort overwrite before unlink (no-op on tmpfs, helps on disk-backed /tmp)
    command -v shred >/dev/null 2>&1 && shred -u "$TMPFILE" 2>/dev/null && return
    : > "$TMPFILE" 2>/dev/null || true
    rm -f "$TMPFILE" 2>/dev/null || true
  fi
}
trap cleanup_tmpfile EXIT

# Decode the base64 argument back to the original raw message
printf '%s' "$B64_MESSAGE" | base64 -d > "$TMPFILE" 2>/dev/null
if [[ $? -ne 0 ]] || [[ ! -s "$TMPFILE" ]]; then
  echo '{"action":"reject","status":"error","reason":"Failed to decode base64 message argument"}'
  exit 0
fi

bash "$SCRIPT_DIR/antenna-relay.sh" --stdin < "$TMPFILE"
