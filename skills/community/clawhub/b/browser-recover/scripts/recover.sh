#!/bin/bash
# Browser Recovery Script for OpenClaw
# Cleans up stale browser processes, ports, and lock files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default configuration
DEFAULT_PORTS=(9222 18800)
DEFAULT_PROFILE_PATH="$HOME/.openclaw/browser"

# Try to read OpenClaw config
OPENCLAW_CONFIG="$HOME/.openclaw/config/openclaw.json"
if [[ -f "$OPENCLAW_CONFIG" ]]; then
    echo "Reading OpenClaw configuration..." >&2
    # Extract browser debug port if configured
    DEBUG_PORT=$(jq -r '.browser.debugPort // empty' "$OPENCLAW_CONFIG" 2>/dev/null || true)
    if [[ -n "$DEBUG_PORT" ]]; then
        DEFAULT_PORTS+=("$DEBUG_PORT")
    fi
fi

# Parse arguments
KILL_PROCESSES=false
CLEAR_PORTS=false
CLEAR_LOCKS=false
FULL_RECOVERY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --kill-processes) KILL_PROCESSES=true; shift ;;
        --clear-ports) CLEAR_PORTS=true; shift ;;
        --clear-locks) CLEAR_LOCKS=true; shift ;;
        --full) FULL_RECOVERY=true; shift ;;
        *) echo -e "${RED}Unknown option: $1${NC}" >&2; exit 1 ;;
    esac
done

# If --full is specified, enable all recovery actions
if [[ "$FULL_RECOVERY" == true ]]; then
    KILL_PROCESSES=true
    CLEAR_PORTS=true
    CLEAR_LOCKS=true
fi

# If no specific action is specified, default to full recovery
if [[ "$KILL_PROCESSES" == false && "$CLEAR_PORTS" == false && "$CLEAR_LOCKS" == false ]]; then
    FULL_RECOVERY=true
    KILL_PROCESSES=true
    CLEAR_PORTS=true
    CLEAR_LOCKS=true
fi

echo -e "${GREEN}=== Browser Recovery Started ===${NC}" >&2

# Step 1: Kill stale browser processes
if [[ "$KILL_PROCESSES" == true ]]; then
    echo -e "${YELLOW}[1/3] Killing stale browser processes...${NC}" >&2
    
    PROCESS_NAMES=("chromium" "chromium-browser" "chromium_browse" "chrome" "google-chrome")
    KILLED_COUNT=0
    
    for proc in "${PROCESS_NAMES[@]}"; do
        if pkill -f "$proc" 2>/dev/null; then
            KILLED_COUNT=$((KILLED_COUNT + 1))
            echo "  Killed processes matching: $proc" >&2
        fi
    done
    
    if [[ $KILLED_COUNT -eq 0 ]]; then
        echo "  No stale processes found" >&2
    else
        echo "  Killed $KILLED_COUNT process group(s)" >&2
    fi
fi

# Step 2: Clear port conflicts
if [[ "$CLEAR_PORTS" == true ]]; then
    echo -e "${YELLOW}[2/3] Clearing port conflicts...${NC}" >&2
    
    CLEARED_COUNT=0
    for port in "${DEFAULT_PORTS[@]}"; do
        if command -v fuser &> /dev/null; then
            if fuser -k "${port}/tcp" 2>/dev/null; then
                CLEARED_COUNT=$((CLEARED_COUNT + 1))
                echo "  Cleared port: $port" >&2
            fi
        elif command -v lsof &> /dev/null; then
            PID=$(lsof -ti:"$port" 2>/dev/null || true)
            if [[ -n "$PID" ]]; then
                kill -9 "$PID" 2>/dev/null || true
                CLEARED_COUNT=$((CLEARED_COUNT + 1))
                echo "  Cleared port: $port (PID: $PID)" >&2
            fi
        fi
    done
    
    if [[ $CLEARED_COUNT -eq 0 ]]; then
        echo "  No port conflicts found" >&2
    else
        echo "  Cleared $CLEARED_COUNT port(s)" >&2
    fi
fi

# Step 3: Clear lock files
if [[ "$CLEAR_LOCKS" == true ]]; then
    echo -e "${YELLOW}[3/3] Clearing lock files...${NC}" >&2
    
    if [[ -d "$DEFAULT_PROFILE_PATH" ]]; then
        LOCK_FILES=$(find "$DEFAULT_PROFILE_PATH" -name "Singleton*" 2>/dev/null || true)
        
        if [[ -n "$LOCK_FILES" ]]; then
            echo "$LOCK_FILES" | while read -r lock_file; do
                rm -f "$lock_file"
                echo "  Removed: $lock_file" >&2
            done
        else
            echo "  No lock files found" >&2
        fi
        
        # Clear cache directories (optional, only if they're causing issues)
        CACHE_DIRS=("Cache" "Code Cache" "GPUCache")
        for cache_dir in "${CACHE_DIRS[@]}"; do
            if [[ -d "$DEFAULT_PROFILE_PATH/$cache_dir" ]]; then
                rm -rf "${DEFAULT_PROFILE_PATH:?}/$cache_dir" 2>/dev/null || true
                echo "  Cleared: $cache_dir" >&2
            fi
        done
    else
        echo "  Profile path not found: $DEFAULT_PROFILE_PATH" >&2
    fi
fi

# Wait for resources to release
echo "Waiting for resources to release..." >&2
sleep 2

echo -e "${GREEN}=== Browser Recovery Completed ===${NC}" >&2
exit 0
