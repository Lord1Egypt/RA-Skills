#!/bin/bash
# Gateway Restore — roll back a gateway to its last known-good config
# Usage: gateway-restore.sh [slack|discord] [--tag-current]
#   slack|discord  — which gateway to restore (default: slack)
#   --tag-current  — instead of restoring, tag the current config as known-good
#
# Exit codes: 0=success, 1=no known-good found, 2=restore+restart failed

set -euo pipefail
export PATH="/home/swabby/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

GATEWAY="${1:-slack}"
ACTION="${2:-restore}"

log() { echo "[$(date '+%H:%M:%S')] $*"; }
err() { echo "[$(date '+%H:%M:%S')] ERROR: $*" >&2; }

case "$GATEWAY" in
  slack)
    CONFIG="$HOME/.openclaw-slack/openclaw.json"
    BACKUP_DIR="$HOME/.openclaw-slack/config-backups"
    RESTART_SCRIPT="$HOME/bin/safe-slack-restart.sh"
    ;;
  discord)
    CONFIG="$HOME/.openclaw/openclaw.json"
    BACKUP_DIR="$HOME/.openclaw/config-backups"
    RESTART_SCRIPT="$HOME/bin/safe-gateway-restart.sh"
    ;;
  *)
    err "Unknown gateway: $GATEWAY (use slack or discord)"
    exit 1
    ;;
esac

KNOWN_GOOD="$BACKUP_DIR/known-good.json"
mkdir -p "$BACKUP_DIR"

# --- Tag current config as known-good ---
if [ "$ACTION" = "--tag-current" ]; then
    cp "$CONFIG" "$KNOWN_GOOD"
    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    cp "$CONFIG" "$BACKUP_DIR/known-good-${TIMESTAMP}.json"
    log "✅ Current $GATEWAY config tagged as known-good: $KNOWN_GOOD"
    exit 0
fi

# --- Restore ---
if [ ! -f "$KNOWN_GOOD" ]; then
    # Fall back to the oldest *-known-good.json if the standard file doesn't exist
    FALLBACK=$(ls "$BACKUP_DIR"/*known-good*.json 2>/dev/null | sort | head -1 || true)
    if [ -z "$FALLBACK" ]; then
        err "No known-good config found at $KNOWN_GOOD — tag one first with --tag-current"
        exit 1
    fi
    log "Using fallback known-good: $FALLBACK"
    KNOWN_GOOD="$FALLBACK"
fi

log "Restoring $GATEWAY gateway from known-good config..."
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
CURRENT_BACKUP="$BACKUP_DIR/pre-restore-${TIMESTAMP}.json"
cp "$CONFIG" "$CURRENT_BACKUP"
log "Current config backed up to $CURRENT_BACKUP"

cp "$KNOWN_GOOD" "$CONFIG"
log "Known-good config restored. Restarting gateway..."

bash "$RESTART_SCRIPT" "restore to known-good config"
EXIT=$?

if [ $EXIT -eq 0 ]; then
    log "✅ $GATEWAY gateway restored and healthy"
elif [ $EXIT -eq 1 ]; then
    log "⚠️  Restart failed — rolled back to previous config"
    cp "$CURRENT_BACKUP" "$CONFIG"
else
    err "CRITICAL: Restart + rollback failed — check $GATEWAY gateway manually"
fi

exit $EXIT
