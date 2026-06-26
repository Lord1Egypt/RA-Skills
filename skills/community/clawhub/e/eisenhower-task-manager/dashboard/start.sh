#!/bin/bash
# Eisenhower Task Dashboard Startup Script
# Automatically checks/installs dependencies and remembers the last used port

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT_FILE="$SCRIPT_DIR/port.conf"

# Check and install dependencies if needed
if [ ! -d "$SCRIPT_DIR/node_modules" ]; then
  echo "[Dashboard] First time setup - installing dependencies..."
  bash "$SCRIPT_DIR/check-and-install.sh"
  if [ $? -ne 0 ]; then
    exit 1
  fi
fi

# Read saved port
if [ -f "$PORT_FILE" ]; then
    SAVED_PORT=$(cat "$PORT_FILE" | tr -d '[:space:]')
fi

# If we are in the development repository (detected by being inside yayayahei-skills)
# use 8081 as default to avoid clashing with the global installation
if [[ "$SCRIPT_DIR" == *"yayayahei-skills"* ]]; then
    DEFAULT_PORT=8081
else
    DEFAULT_PORT=8080
fi

SAVED_PORT=${SAVED_PORT:-$DEFAULT_PORT}

# Parse arguments
USER_PORT=""
# Preserve existing EISENHOWER_TASKS_DIR from environment
DAEMON_MODE=false
ARGS=()

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --port)
            USER_PORT="$2"
            shift 2
            ;;
        --tasks-dir)
            if [ -n "$EISENHOWER_TASKS_DIR" ] && [ "$EISENHOWER_TASKS_DIR" != "$2" ]; then
                echo "[Dashboard] Note: System environment variable EISENHOWER_TASKS_DIR is set. Ignoring --tasks-dir argument."
            else
                EISENHOWER_TASKS_DIR="$2"
            fi
            shift 2
            ;;
        --daemon)
            DAEMON_MODE=true
            shift
            ;;
        *)
            ARGS+=("$1")
            shift
            ;;
    esac
done

# Determine which port to use
if [ -n "$USER_PORT" ]; then
    # User specified a port, save it for next time
    echo "$USER_PORT" > "$PORT_FILE"
    echo "[Dashboard] Port saved: $USER_PORT"
    ARGS+=("--port" "$USER_PORT")
else
    # No port specified, use saved port
    ARGS+=("--port" "$SAVED_PORT")
    echo "[Dashboard] Using saved port: $SAVED_PORT"
fi

# Export EISENHOWER_TASKS_DIR if specified
if [ -n "$EISENHOWER_TASKS_DIR" ]; then
    export EISENHOWER_TASKS_DIR="$EISENHOWER_TASKS_DIR"
    echo "[Dashboard] Using tasks directory: $EISENHOWER_TASKS_DIR"
    # Ensure it's passed to the background process in daemon mode
    ARGS+=("--tasks-dir" "$EISENHOWER_TASKS_DIR")
fi

cd "$SCRIPT_DIR"

if [ "$DAEMON_MODE" = true ]; then
    # Daemon mode: run in background with nohup
    LOG_FILE="$SCRIPT_DIR/dashboard.log"
    PID_FILE="$SCRIPT_DIR/dashboard.pid"
    
    # Check if already running
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE")
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "[Dashboard] Already running (PID: $OLD_PID)"
            echo "[Dashboard] Visit: http://localhost:${USER_PORT:-$SAVED_PORT}"
            exit 0
        fi
    fi
    
    echo "[Dashboard] Starting in daemon mode..."
    echo "[Dashboard] Log file: $LOG_FILE"
    if [ -n "$EISENHOWER_TASKS_DIR" ]; then
        nohup env EISENHOWER_TASKS_DIR="$EISENHOWER_TASKS_DIR" node server.js "${ARGS[@]}" > "$LOG_FILE" 2>&1 &
    else
        nohup node server.js "${ARGS[@]}" > "$LOG_FILE" 2>&1 &
    fi
    PID=$!
    echo $PID > "$PID_FILE"
    
    # Wait a moment to check if it started successfully
    sleep 2
    if kill -0 $PID 2>/dev/null; then
        echo "[Dashboard] Started successfully (PID: $PID)"
        echo "[Dashboard] Visit: http://localhost:${USER_PORT:-$SAVED_PORT}"
        echo "[Dashboard] Stop with: kill $PID"
    else
        echo "[Dashboard] Failed to start. Check log: $LOG_FILE"
        rm -f "$PID_FILE"
        exit 1
    fi
else
    # Interactive mode: run in foreground
    node server.js "${ARGS[@]}"
fi
