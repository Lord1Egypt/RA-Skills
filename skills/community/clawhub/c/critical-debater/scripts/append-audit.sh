#!/bin/bash
# append-audit.sh — Atomically append a JSONL line to audit trail
set -euo pipefail

AUDIT_FILE="${1:?Usage: $0 <audit_file> <json_line>}"
JSON_LINE="${2:?Usage: $0 <audit_file> <json_line>}"

if ! echo "$JSON_LINE" | jq empty 2>/dev/null; then
  echo "ERROR: Invalid JSON: $JSON_LINE" >&2
  exit 1
fi

touch "$AUDIT_FILE"

TEMP_FILE=$(mktemp "${AUDIT_FILE}.XXXXXX")
cp "$AUDIT_FILE" "$TEMP_FILE"
echo "$JSON_LINE" >> "$TEMP_FILE"
mv "$TEMP_FILE" "$AUDIT_FILE"
