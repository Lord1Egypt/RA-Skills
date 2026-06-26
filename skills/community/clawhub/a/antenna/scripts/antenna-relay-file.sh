#!/usr/bin/env bash
# antenna-relay-file.sh — Read raw message from a file and pass it to
# antenna-relay.sh via stdin.
#
# Usage: bash antenna-relay-file.sh /path/to/message-file
#
# Designed so the calling agent never needs to base64-encode or use
# shell metacharacters. The agent writes raw message text to a temp file
# (via the write tool), then execs this script with the file path.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INPUT_FILE="${1:-}"

if [[ -z "$INPUT_FILE" ]]; then
    echo '{"action":"reject","status":"error","reason":"No input file path provided"}'
    exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "{\"action\":\"reject\",\"status\":\"error\",\"reason\":\"Input file not found: $INPUT_FILE\"}"
    exit 1
fi

# REF-403: tighten file & parent-dir perms since the envelope contains the
# plaintext auth header. Best-effort — caller may not own the parent dir.
chmod 0600 "$INPUT_FILE" 2>/dev/null || true
INPUT_DIR="$(dirname "$INPUT_FILE")"
case "$INPUT_DIR" in
    /tmp/antenna-relay)
        chmod 0700 "$INPUT_DIR" 2>/dev/null || true
        ;;
esac

cleanup_input_file() {
    # REF-403: input file holds plaintext envelope with auth header.
    # Best-effort wipe before unlink (no-op on tmpfs, helps on disk-backed /tmp).
    case "$INPUT_FILE" in
        /tmp/antenna-relay/*|/tmp/antenna-relay-msg.*)
            if [[ -f "$INPUT_FILE" ]]; then
                command -v shred >/dev/null 2>&1 && shred -u "$INPUT_FILE" 2>/dev/null && return
                : > "$INPUT_FILE" 2>/dev/null || true
                rm -f "$INPUT_FILE" 2>/dev/null || true
            fi
            ;;
    esac
}

trap cleanup_input_file EXIT

# Feed the raw message to the relay script via stdin
bash "$SCRIPT_DIR/antenna-relay.sh" --stdin < "$INPUT_FILE"
