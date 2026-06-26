#!/usr/bin/env bash
# ClawTK Uninstall — Clean removal with config restore

set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
STATE_FILE="$OPENCLAW_DIR/clawtk-state.json"
SPEND_LOG="$OPENCLAW_DIR/clawtk-spend.jsonl"
CACHE_DB="$OPENCLAW_DIR/clawtk-cache.db"
CONFIG_FILE="$OPENCLAW_DIR/openclaw.json"
SKILL_DIR="$OPENCLAW_DIR/skills/clawtk"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[clawtk]${NC} $1"; }
warn() { echo -e "${YELLOW}[clawtk]${NC} $1"; }
err()  { echo -e "${RED}[clawtk]${NC} $1" >&2; }

echo ""
log "Uninstalling ClawTK..."
echo ""

# Step 1: Restore config from backup
if [ -f "$STATE_FILE" ]; then
    backup_path=$(jq -r '.configBackup // empty' "$STATE_FILE")

    if [ -n "$backup_path" ] && [ -f "$backup_path" ]; then
        cp "$backup_path" "$CONFIG_FILE"
        log "Config restored from: $backup_path"
    else
        warn "No config backup found. Your current config is unchanged."
        warn "You may want to manually review: $CONFIG_FILE"
    fi
fi

# Step 2: Unregister hooks
if command -v openclaw &>/dev/null; then
    openclaw plugins uninstall clawtk 2>/dev/null || true
    log "Hooks unregistered."
fi

# Step 3: Remove ClawTK files
rm -f "$STATE_FILE"
log "Removed state file."

rm -f "$SPEND_LOG"
log "Removed spend log."

rm -f "$CACHE_DB"
log "Removed cache database."

# Remove backup files
rm -f "$CONFIG_FILE".clawtk-backup.* 2>/dev/null || true
log "Removed config backups."

# Step 4: Remove skill directory
if [ -d "$SKILL_DIR" ]; then
    rm -rf "$SKILL_DIR"
    log "Removed skill directory."
fi

echo ""
log "ClawTK has been completely removed."
log "Restart your OpenClaw gateway for changes to take effect."
echo ""
