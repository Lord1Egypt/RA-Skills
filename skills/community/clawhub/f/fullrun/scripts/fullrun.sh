#!/bin/bash

# Fullrun Script
# Automatically execute tasks from checklist.md with state management and scheduled checking

set -e

# Use current working directory as project root
WORKDIR="$(pwd)"
STATUS_FILE="$WORKDIR/.claude-status.txt"
CHECKLIST_FILE="$WORKDIR/checklist.md"
LOG_FILE="$WORKDIR/.fullrun.log"

# Status values:
# 0 = idle, ready to execute
# 1 = claude is running/executing tasks
# 2 = all tasks completed, monitoring should exit

# Logging function
log() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $*" >> "$LOG_FILE"
    echo "$*"
}

# Set status state
# Only allows values 0, 1, or 2
set_status() {
    local new_status="$1"

    # Validate status value - only allow 0, 1, or 2
    if [[ "$new_status" != "0" && "$new_status" != "1" && "$new_status" != "2" ]]; then
        log "ERROR: Invalid status value '$new_status'. Only 0, 1, or 2 are allowed."
        return 1
    fi

    echo "$new_status" > "$STATUS_FILE"
    log "Status set to: $new_status"
}

# Get current status
get_status() {
    if [ ! -f "$STATUS_FILE" ]; then
        echo "0"
    else
        cat "$STATUS_FILE"
    fi
}

# Check if there are pending tasks
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

# Get the first pending task
get_next_task() {
    if [ ! -f "$CHECKLIST_FILE" ]; then
        echo ""
        return
    fi
    grep '\[ \]' "$CHECKLIST_FILE" | head -1 | sed 's/.*\[ \] //'
}

# Mark task as done
# Uses awk to replace the first [ ] with [x]
mark_task_done() {
    local task_line="$1"

    # Use awk for cross-platform compatibility
    # This replaces only the first occurrence of [ ] with [x]
    awk '{if(!done && /\[ \]/){sub(/\[ \]/,"[x]");done=1} print}' "$CHECKLIST_FILE" > "$CHECKLIST_FILE.new" && mv "$CHECKLIST_FILE.new" "$CHECKLIST_FILE"

    log "Marked task as done"
}

# Execute task
# This function logs the task and delegates to Claude for execution.
# The actual command execution is handled by Claude Code based on the task description.
execute_task() {
    local task="$1"
    log "=========================================="
    log "STARTING TASK: $task"
    log "=========================================="

    # Output the task for Claude to execute
    # Claude Code will read this and execute the appropriate commands
    echo ""
    echo ">>> TASK: $task"
    echo ""

    # Note: Task execution is delegated to Claude Code.
    # The task description from checklist.md should describe what needs to be done.
    # Claude will interpret and execute the necessary commands.
}

# Main execution loop
run_tasks() {
    set_status "1"
    log "Starting task execution loop"

    while true; do
        pending=$(has_pending_tasks)
        if [ "$pending" = "false" ]; then
            log "All tasks completed"
            set_status "2"
            break
        fi

        task=$(get_next_task)
        if [ -z "$task" ]; then
            log "No task found, setting status to idle"
            set_status "0"
            break
        fi

        execute_task "$task"
        mark_task_done "$task"
    done

    log "Task execution loop finished"
}

# Command handling
case "${1:-}" in
    status)
        get_status
        ;;
    check)
        status=$(get_status)
        pending=$(has_pending_tasks)
        echo "Status: $status (0=idle, 1=running, 2=completed), Pending tasks: $pending"
        ;;
    run)
        run_tasks
        ;;
    start)
        status=$(get_status)
        pending=$(has_pending_tasks)
        if [ "$status" = "0" ] && [ "$pending" = "true" ]; then
            log "Starting task execution..."
            run_tasks
        elif [ "$status" = "1" ]; then
            echo "Already executing (status=1)"
        elif [ "$status" = "2" ]; then
            echo "All tasks completed (status=2)"
        else
            echo "No pending tasks or unknown status"
        fi
        ;;
    *)
        echo "Usage: $0 {status|check|run|start}"
        exit 1
        ;;
esac
