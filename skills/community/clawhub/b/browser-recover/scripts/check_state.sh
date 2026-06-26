#!/bin/bash
# Browser State Diagnostic Script for OpenClaw
# Checks browser processes, port usage, and lock files

set -e

# Colors for output
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default configuration
DEFAULT_PORTS=(9222 18800)
DEFAULT_PROFILE_PATH="$HOME/.openclaw/browser"

# Try to read OpenClaw config
OPENCLAW_CONFIG="$HOME/.openclaw/config/openclaw.json"
if [[ -f "$OPENCLAW_CONFIG" ]]; then
    DEBUG_PORT=$(jq -r '.browser.debugPort // empty' "$OPENCLAW_CONFIG" 2>/dev/null || true)
    if [[ -n "$DEBUG_PORT" ]]; then
        DEFAULT_PORTS+=("$DEBUG_PORT")
    fi
fi

echo -e "${CYAN}=== Browser Environment Diagnostic ===${NC}"
echo ""

# Check 1: Browser processes
echo -e "${YELLOW}[1/3] Browser Processes:${NC}"
PROCESS_COUNT=$(ps -ef | grep -E 'chromium|chrome' | grep -v grep | wc -l)
if [[ $PROCESS_COUNT -gt 0 ]]; then
    echo "  Found $PROCESS_COUNT browser process(es):"
    ps -ef | grep -E 'chromium|chrome' | grep -v grep | awk '{print "    PID " $2 ": " $8}'
else
    echo "  No browser processes running"
fi
echo ""

# Check 2: Port status
echo -e "${YELLOW}[2/3] Port Status:${NC}"
PORT_CONFLICTS=0
for port in "${DEFAULT_PORTS[@]}"; do
    if command -v lsof &> /dev/null; then
        PORT_INFO=$(lsof -iTCP:"$port" -sTCP:LISTEN -P 2>/dev/null || true)
        if [[ -n "$PORT_INFO" ]]; then
            echo "  Port $port: IN USE"
            echo "$PORT_INFO" | tail -n +2 | awk '{print "    PID " $2 ": " $1}'
            PORT_CONFLICTS=$((PORT_CONFLICTS + 1))
        else
            echo "  Port $port: Available"
        fi
    elif command -v netstat &> /dev/null; then
        if netstat -tuln | grep -q ":$port "; then
            echo "  Port $port: IN USE"
            PORT_CONFLICTS=$((PORT_CONFLICTS + 1))
        else
            echo "  Port $port: Available"
        fi
    fi
done

if [[ $PORT_CONFLICTS -eq 0 ]]; then
    echo "  All ports are available"
fi
echo ""

# Check 3: Lock files
echo -e "${YELLOW}[3/3] Lock Files:${NC}"
if [[ -d "$DEFAULT_PROFILE_PATH" ]]; then
    LOCK_COUNT=$(find "$DEFAULT_PROFILE_PATH" -name "Singleton*" 2>/dev/null | wc -l)
    if [[ $LOCK_COUNT -gt 0 ]]; then
        echo "  Found $LOCK_COUNT lock file(s):"
        find "$DEFAULT_PROFILE_PATH" -name "Singleton*" 2>/dev/null | while read -r lock_file; do
            echo "    $lock_file"
        done
    else
        echo "  No lock files found"
    fi
else
    echo "  Profile path not found: $DEFAULT_PROFILE_PATH"
fi
echo ""

# Summary
echo -e "${CYAN}=== Summary ===${NC}"
if [[ $PROCESS_COUNT -gt 0 || $PORT_CONFLICTS -gt 0 || $LOCK_COUNT -gt 0 ]]; then
    echo "  Status: Issues detected"
    echo "  Recommendation: Run recover.sh to clean up"
else
    echo "  Status: Environment is clean"
fi

exit 0
