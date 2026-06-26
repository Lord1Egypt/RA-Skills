#!/bin/bash
# pre-stop.sh — ExecStopPost hook for openclaw-gateway.service
# Triggered by systemd on gateway stop. Installed via SKILL.md — do not run manually.
# systemd injects: SERVICE_RESULT, EXIT_CODE

LOG="/tmp/config-watcher.log"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config-lib.sh"

# SERVICE_RESULT values:
#   success / signal → clean stop (systemctl stop / restart)
#   exit-code / core-dump / watchdog / ... → crash
# Crash cases are handled by recovery.sh (OnFailure) — skip here to avoid duplicate notifications.
case "${SERVICE_RESULT:-}" in
    success|signal)
        if [ "$(cat "$MANAGED_RESTART_FLAG" 2>/dev/null)" = "recovery" ]; then
            log "[pre-stop] Managed restart by recovery.sh detected — skipping notification"
        else
            log "[pre-stop] Gateway stopped cleanly — sending restart notification"
            echo "managed" > "$MANAGED_RESTART_FLAG"
            notify_status "$_MSG_RESTART_STARTING"
        fi
        ;;
    *)
        log "[pre-stop] Gateway exited abnormally (SERVICE_RESULT=${SERVICE_RESULT}) — skipping (recovery.sh will handle)"
        ;;
esac
