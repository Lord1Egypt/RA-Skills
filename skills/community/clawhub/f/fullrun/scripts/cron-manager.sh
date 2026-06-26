#!/bin/bash

# Cron Job Manager for Fullrun
# Manages scheduled task checking

# Use current working directory as project root
WORKDIR="$(pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

STATUS_FILE="$WORKDIR/.claude-status.txt"
CHECKLIST_FILE="$WORKDIR/checklist.md"
LOG_FILE="$WORKDIR/.fullrun.log"
PID_FILE="$WORKDIR/.monitor.pid"

# Status values:
# 0 = idle, ready to execute
# 1 = claude is running/executing tasks
# 2 = all tasks completed, monitoring should exit

has_pending_tasks() {
    if [ ! -f "$CHECKLIST_FILE" ]; then
        echo "false"
        return
    fi
    if grep -q '\[ \]' "$CHECKLIST_FILE"; then
        echo "true"
    else
        echo "false"
    fi
}

get_status() {
    if [ ! -f "$STATUS_FILE" ]; then
        echo "0"
    else
        cat "$STATUS_FILE"
    fi
}

start_monitor() {
    echo "Starting scheduled monitoring..."
    (
        while true; do
            sleep 60

            status=$(get_status)
            pending=$(has_pending_tasks)

            echo "[$(date)] Check: status=$status, pending=$pending" >> "$LOG_FILE"

            # Status 2 = all tasks completed, exit monitoring
            if [ "$status" = "2" ]; then
                echo "[$(date)] All tasks completed (status=2), stopping monitoring" >> "$LOG_FILE"
                break
            fi

            # No pending tasks, mark as completed and exit
            if [ "$pending" = "false" ]; then
                echo "2" > "$STATUS_FILE"
                echo "[$(date)] No pending tasks, marking status=2 and stopping" >> "$LOG_FILE"
                break
            fi

            # Status 0 = idle and has pending tasks, start execution
            if [ "$status" = "0" ] && [ "$pending" = "true" ]; then
                echo "[$(date)] Idle state detected (status=0), starting task execution..." >> "$LOG_FILE"
                echo "1" > "$STATUS_FILE"
                "$SCRIPT_DIR/fullrun.sh" run >> "$LOG_FILE" 2>&1
                current_status=$(get_status)
                if [ "$current_status" = "1" ]; then
                    echo "0" > "$STATUS_FILE"
                fi
            fi

        done

        echo "[$(date)] Monitor exited" >> "$LOG_FILE"
    ) &

    echo $! > "$PID_FILE"
    echo "Monitoring started, PID: $(cat $PID_FILE)"
}

stop_monitor() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid
            echo "Monitoring stopped (PID: $pid)"
        else
            echo "Monitor process does not exist"
        fi
        rm "$PID_FILE"
    else
        echo "No running monitor found"
    fi
}

monitor_status() {
    if [ -f "$PID_FILE" ]; then
        pid=$(cat "$PID_FILE")
        if ps -p $pid > /dev/null 2>&1; then
            status=$(get_status)
            pending=$(has_pending_tasks)
            echo "Monitoring running (PID: $pid)"
            echo "Status: $status (0=idle, 1=running, 2=completed)"
            echo "Pending tasks: $pending"
            return
        fi
    fi
    echo "Monitoring not running"
}

case "${1:-status}" in
    start)
        start_monitor
        ;;
    stop)
        stop_monitor
        ;;
    status)
        monitor_status
        ;;
    restart)
        stop_monitor
        sleep 1
        start_monitor
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac
