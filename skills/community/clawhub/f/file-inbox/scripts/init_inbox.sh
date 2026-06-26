#!/usr/bin/env bash
# init_inbox.sh — Initialize the file-inbox directory structure
# Idempotent: safe to run multiple times

set -euo pipefail

INBOX_DIR="${INBOX_DIR:-inbox}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
INBOX_PATH="$WORKSPACE_ROOT/$INBOX_DIR"

echo "Initializing file inbox at: $INBOX_PATH"

# Create directories
mkdir -p "$INBOX_PATH/inbound"
mkdir -p "$INBOX_PATH/outbound"

# Create .meta.json if not exists
META_FILE="$INBOX_PATH/.meta.json"
if [ ! -f "$META_FILE" ]; then
  cat > "$META_FILE" <<'EOF'
{
  "nextId": 1,
  "total": 0,
  "inbound": 0,
  "outbound": 0,
  "lastUpdated": ""
}
EOF
  echo "Created .meta.json"
else
  echo ".meta.json already exists — skipping"
fi

# Create INDEX.md if not exists
INDEX_FILE="$INBOX_PATH/INDEX.md"
if [ ! -f "$INDEX_FILE" ]; then
  TODAY=$(date +%Y-%m-%d)
  cat > "$INDEX_FILE" <<EOF
# File Inbox

> Total: 0 files | Inbound: 0 | Outbound: 0
> Last updated: $TODAY

## Recent Files

| ID | Direction | Filename | Type | Tags | Sender/Dest | Date | Notes |
|----|-----------|----------|------|------|-------------|------|-------|

EOF
  echo "Created INDEX.md"
else
  echo "INDEX.md already exists — skipping"
fi

echo "Done. File inbox ready at: $INBOX_PATH"
