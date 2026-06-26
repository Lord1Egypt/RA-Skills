#!/usr/bin/env bash
# ClawTK Cloud Sync — push local spend data to api.clawtk.co
# Usage:
#   sync.sh               Sync new entries since last sync
#   sync.sh --compact     Sync + rewrite JSONL to remove synced entries

set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
STATE_FILE="$OPENCLAW_DIR/clawtk-state.json"
SPEND_LOG="$OPENCLAW_DIR/clawtk-spend.jsonl"
SYNC_OFFSET="$OPENCLAW_DIR/.clawtk-sync-offset"
API_BASE="https://api.clawtk.co/v1"
BATCH_SIZE=500

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[clawtk]${NC} $1"; }
warn() { echo -e "${YELLOW}[clawtk]${NC} $1"; }
err()  { echo -e "${RED}[clawtk]${NC} $1" >&2; }

# ── Preflight ────────────────────────────────────────────────────────────────

if [ ! -f "$STATE_FILE" ]; then
    err "ClawTK is not set up. Run /clawtk setup first."
    exit 1
fi

tier=$(jq -r '.tier' "$STATE_FILE")
license_key=$(jq -r '.licenseKey // empty' "$STATE_FILE")

if [ "$tier" = "free" ]; then
    err "Cloud sync requires Pro or Cloud tier."
    err "Upgrade at https://clawtk.co/pro"
    exit 1
fi

if [ -z "$license_key" ]; then
    err "No license key found. Run /clawtk activate YOUR-KEY first."
    exit 1
fi

if [ ! -f "$SPEND_LOG" ]; then
    log "No spend data to sync."
    exit 0
fi

# ── Read Offset ──────────────────────────────────────────────────────────────

offset=0
if [ -f "$SYNC_OFFSET" ]; then
    offset=$(cat "$SYNC_OFFSET")
fi

total_lines=$(wc -l < "$SPEND_LOG" | tr -d ' ')

if [ "$offset" -ge "$total_lines" ]; then
    log "Already up to date. No new entries to sync."
    exit 0
fi

new_lines=$((total_lines - offset))
log "Found $new_lines new entries to sync."
log "Data sent: timestamp, token count, estimated cost, tool name, hash."
log "No message content, file contents, or conversation data is included."

# ── Batch and Send ───────────────────────────────────────────────────────────

synced=0
current_offset=$((offset + 1))

while [ "$current_offset" -le "$total_lines" ]; do
    # Extract batch using sed (line range)
    end_line=$((current_offset + BATCH_SIZE - 1))
    if [ "$end_line" -gt "$total_lines" ]; then
        end_line=$total_lines
    fi

    # Build JSON array from JSONL lines
    batch=$(sed -n "${current_offset},${end_line}p" "$SPEND_LOG" | jq -s '.')

    batch_size=$(echo "$batch" | jq 'length')

    if [ "$batch_size" -eq 0 ]; then
        break
    fi

    # POST to API
    response=$(curl -sS --max-time 30 \
        -H "Content-Type: application/json" \
        -H "X-License-Key: $license_key" \
        -d "{\"entries\": $batch}" \
        "$API_BASE/spend" 2>&1)

    # Check response
    ingested=$(echo "$response" | jq -r '.ingested // 0' 2>/dev/null)

    if [ "$ingested" = "0" ] && echo "$response" | jq -e '.error' &>/dev/null; then
        error_msg=$(echo "$response" | jq -r '.error')
        err "API error: $error_msg"
        err "Synced $synced entries before failure."
        # Save partial progress
        echo "$((current_offset - 1))" > "$SYNC_OFFSET"
        exit 1
    fi

    synced=$((synced + batch_size))
    current_offset=$((end_line + 1))

    log "Synced batch: $synced / $new_lines entries"
done

# ── Update Offset ────────────────────────────────────────────────────────────

echo "$total_lines" > "$SYNC_OFFSET"
log "Sync complete. $synced entries pushed to clawtk.co"

# Check for alerts that fired
alerts=$(echo "$response" | jq -r '.alerts // [] | join(", ")' 2>/dev/null)
if [ -n "$alerts" ] && [ "$alerts" != "" ]; then
    warn "Alerts triggered: $alerts"
fi

# ── Optional Compact ─────────────────────────────────────────────────────────

if [ "${1:-}" = "--compact" ] && [ "$total_lines" -gt 100000 ]; then
    log "Compacting spend log (removing $total_lines synced entries)..."

    # Keep only unsynced lines (there shouldn't be any after a full sync,
    # but new entries may have been appended during sync)
    current_total=$(wc -l < "$SPEND_LOG" | tr -d ' ')
    if [ "$current_total" -gt "$total_lines" ]; then
        tail -n $((current_total - total_lines)) "$SPEND_LOG" > "$SPEND_LOG.tmp"
        mv "$SPEND_LOG.tmp" "$SPEND_LOG"
        echo "0" > "$SYNC_OFFSET"
        log "Compacted: kept $((current_total - total_lines)) unsynced entries."
    else
        : > "$SPEND_LOG"
        echo "0" > "$SYNC_OFFSET"
        log "Compacted: spend log cleared."
    fi
fi
