#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
AUDIT_DIR="$ROOT/logs/audit"
mkdir -p "$AUDIT_DIR"

TODAY="$(date +%F)"
JSONL="$AUDIT_DIR/$TODAY.jsonl"
INDEX="$AUDIT_DIR/index.json"
TARGETS="$AUDIT_DIR/by-target.json"
RISK="$AUDIT_DIR/by-risk.json"
LATEST="$AUDIT_DIR/latest.md"
OPEN_ITEMS="$AUDIT_DIR/open-items.json"
OPEN_ITEMS_HISTORY="$AUDIT_DIR/open-items-history.json"

: > "$JSONL"
[ -f "$INDEX" ] || printf '{\n  "version": 2,\n  "days": []\n}\n' > "$INDEX"
[ -f "$TARGETS" ] || printf '{\n  "version": 3,\n  "targets": {}\n}\n' > "$TARGETS"
[ -f "$RISK" ] || printf '{\n  "version": 4,\n  "riskBuckets": {}\n}\n' > "$RISK"
[ -f "$LATEST" ] || printf '# Latest audit summary\n\n' > "$LATEST"
[ -f "$OPEN_ITEMS" ] || printf '{\n  "version": 7,\n  "items": []\n}\n' > "$OPEN_ITEMS"
[ -f "$OPEN_ITEMS_HISTORY" ] || printf '{\n  "version": 8,\n  "items": {}\n}\n' > "$OPEN_ITEMS_HISTORY"

echo "Initialized audit structure in: $AUDIT_DIR"
