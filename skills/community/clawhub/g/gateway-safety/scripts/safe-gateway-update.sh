#!/bin/bash
# safe-gateway-update.sh - Safely update openclaw.json with auto-rollback
# Usage: ./safe-gateway-update.sh <new_config_json_path> [timeout_seconds]

CONFIG_PATH="$HOME/.openclaw/openclaw.json"
BACKUP_PATH="$HOME/.openclaw/openclaw.json.bak"
NEW_CONFIG="$1"
TIMEOUT="${2:-30}"
LOG_FILE="$HOME/.rook/logs/gateway-update.log"
COUNT_FILE="$HOME/.openclaw/config_failure_count"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

if [ -z "$NEW_CONFIG" ]; then
    log "Usage: $0 <new_config_json_path> [timeout_seconds]"
    exit 1
fi

if [ ! -f "$NEW_CONFIG" ]; then
    log "Error: New config file '$NEW_CONFIG' not found."
    exit 1
fi

# Validate JSON before applying
if ! jq empty "$NEW_CONFIG" >/dev/null 2>&1; then
    log "Error: New config is not valid JSON."
    exit 1
fi

log "--- Gateway Update Started ---"
log "Target: $CONFIG_PATH"
log "Source: $NEW_CONFIG"
log "Timeout: ${TIMEOUT}s"

log "Backing up current config to $BACKUP_PATH"
cp "$CONFIG_PATH" "$BACKUP_PATH"

log "Applying new config..."
cp "$NEW_CONFIG" "$CONFIG_PATH"

log "Restarting gateway..."
openclaw gateway restart

log "Waiting for gateway to stabilize..."
SUCCESS=0
for ((i=1; i<=$TIMEOUT; i++)); do
    STATUS=$(openclaw gateway status 2>/dev/null)
    if echo "$STATUS" | grep -q "RPC probe: ok"; then
        log "Gateway is back online and healthy (attempt $i)."
        SUCCESS=1
        break
    fi
    sleep 1
done

if [ $SUCCESS -eq 1 ]; then
    log "Update SUCCESSFUL."
    # Clear any failed attempts on success
    rm -f "$COUNT_FILE"
    # Keep as the new known-good
    cp "$CONFIG_PATH" "$HOME/.openclaw/openclaw.json.known-good"
    log "--- Gateway Update Finished (Success) ---"
    exit 0
else
    log "TIMEOUT REACHED. Gateway failed to respond. ROLLING BACK..."
    cp "$BACKUP_PATH" "$CONFIG_PATH"
    
    # Increment failure counter to prevent loops
    COUNT=$(cat "$COUNT_FILE" 2>/dev/null || echo 0)
    COUNT=$((COUNT + 1))
    echo "$COUNT" > "$COUNT_FILE"

    log "Restarting gateway with original config (Failure #$COUNT)..."
    openclaw gateway restart
    
    # If we've failed too many times, we should probably stop and wait for a human
    if [ "$COUNT" -ge 3 ]; then
        log "CRITICAL: Multiple consecutive config failures detected ($COUNT). STOPPING."
        echo "CRITICAL: GATEWAY UPDATE LOOP DETECTED ($COUNT failures). AGENTS: DO NOT RETRY WITHOUT MANUAL REVIEW FROM KEVIN." > "$HOME/.openclaw/GATEWAY_LOCKOUT"
    fi

    # Final check
    sleep 5
    if openclaw gateway status 2>/dev/null | grep -q "RPC probe: ok"; then
        log "Rollback successful. Gateway is online with previous config."
    else
        log "CRITICAL: Rollback failed to bring gateway online. Manual intervention required."
    fi
    log "--- Gateway Update Finished (Failed/Rolled Back) ---"
    exit 1
fi
