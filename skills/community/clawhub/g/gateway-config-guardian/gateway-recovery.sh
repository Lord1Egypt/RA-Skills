#!/bin/bash
# gateway-recovery.sh — Gateway crash recovery
# Triggered by systemd OnFailure. Installed via SKILL.md — do not run manually.

LOG="/tmp/gateway-recovery.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config-lib.sh"

GATEWAY_TIMEOUT=30

log "========================================="
log "Gateway failed repeatedly — starting recovery"

(
    flock -w 60 9 || { log "❌ Lock timeout, aborting recovery"; exit 1; }

    # [1/3] Validate config; rollback if needed
    log "--- [1/3] Check config ---"
    ROLLED_BACK=0
    result=$(validate_file "$CONFIG" 2>&1)
    if [ $? -ne 0 ]; then
        log "❌ Config invalid: $result"
        if rollback; then
            log "✅ Config rolled back"
            ROLLED_BACK=1
        else
            log "🚨 Config corrupted and no valid backup available"
            write_to_memory "- $_MSG_EVENT: $_MSG_MEM_CRASH_NO_BACKUP
- $_MSG_RESULT: ❌ $_MSG_MEM_CANNOT_RECOVER
- $_MSG_LOG: $LOG"
            notify_urgent "$_MSG_URGENT_TITLE" \
"⏰ $_MSG_TIME: $(date '+%Y-%m-%d %H:%M')
📋 $_MSG_EVENT: $_MSG_MEM_CRASH_NO_BACKUP
❌ $_MSG_REASON: $_MSG_URGENT_NOOP_REASON
📝 $_MSG_LOG:
$(tail_log "$LOG")"
            exit 1
        fi
    else
        log "✅ Config OK"
    fi

    # [2/3] Restart gateway (flagged as managed — notifications sent by this script)
    log "--- [2/3] Restart gateway ---"
    echo "recovery" > "$MANAGED_RESTART_FLAG"
    systemctl --user reset-failed openclaw-gateway.service 2>/dev/null
    systemctl --user restart openclaw-gateway.service

    # [3/3] Wait for gateway to come up (up to GATEWAY_TIMEOUT seconds)
    log "--- [3/3] Waiting for gateway (max ${GATEWAY_TIMEOUT}s) ---"
    elapsed=0
    while [ $elapsed -lt $GATEWAY_TIMEOUT ]; do
        nc -z 127.0.0.1 $GATEWAY_PORT 2>/dev/null && {
            log "✅ Gateway recovered"
            # Leave flag for monitor to remove (avoids race condition)

            if [ "$ROLLED_BACK" = "1" ]; then
                notify_success "$_MSG_RECOVERY_SUCCESS_TITLE" \
"⏰ $_MSG_TIME: $(date '+%Y-%m-%d %H:%M')
📋 $_MSG_EVENT: $_MSG_RECOVERY_WITH_ROLLBACK
🔧 $_MSG_ROLLED_BACK_TO: ${ROLLBACK_USED_BACKUP:-$_MSG_LATEST_BACKUP}
✅ $_MSG_RESULT: $_MSG_GATEWAY_BACK"
            else
                notify_success "$_MSG_RECOVERY_SUCCESS_TITLE" \
"⏰ $_MSG_TIME: $(date '+%Y-%m-%d %H:%M')
📋 $_MSG_EVENT: $_MSG_RECOVERY_NO_ROLLBACK
🔧 $_MSG_ACTION: $_MSG_RECOVERY_RESET_ACTION
✅ $_MSG_RESULT: $_MSG_GATEWAY_BACK"
            fi
            exit 0
        }
        sleep 5; elapsed=$((elapsed + 5))
        log "⏳ Waiting... ${elapsed}s/${GATEWAY_TIMEOUT}s"
    done

    rm -f "$MANAGED_RESTART_FLAG"
    log "❌ Gateway still unresponsive after ${GATEWAY_TIMEOUT}s"
    log "$(systemctl --user status openclaw-gateway.service 2>&1 | tail -5)"
    write_to_memory "- $_MSG_EVENT: $_MSG_MEM_RECOVERY_FAIL
- $_MSG_RESULT: ❌ $_MSG_MEM_TIMEOUT
- $_MSG_LOG: $LOG"
    notify_urgent "$_MSG_RECOVERY_FAIL_TITLE" \
"⏰ $_MSG_TIME: $(date '+%Y-%m-%d %H:%M')
📋 $_MSG_EVENT: $_MSG_RECOVERY_FAIL_EVENT
❌ $_MSG_REASON: $_MSG_RECOVERY_FAIL_REASON
📝 $_MSG_LOG:
$(tail_log "$LOG")
🔍 $_MSG_GATEWAY_LOG:
$(gateway_journal_errors)"
    exit 1

) 9>"$LOCK_FILE"

exit $?
