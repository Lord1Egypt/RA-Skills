#!/bin/bash

# EkyBot Workspace Health Check Script
# Checks workspace health and reports status to EkyBot

set -e

CONFIG_DIR="$HOME/.openclaw/ekybot-connector"
CONFIG_FILE="$CONFIG_DIR/config.json"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_detail() {
    echo -e "${BLUE}[DETAIL]${NC} $1"
}

# Check if configured
if [[ ! -f "$CONFIG_FILE" ]]; then
    print_error "EkyBot connector not configured. Run scripts/register_workspace.sh first."
    exit 1
fi

# Load configuration
WORKSPACE_ID=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['workspace_id'])")
API_KEY=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['api_key'])")
HEALTH_ENDPOINT=$(cat "$CONFIG_FILE" | python3 -c "import sys, json; print(json.load(sys.stdin)['endpoints']['health'])")

if [[ -z "$WORKSPACE_ID" ]] || [[ -z "$API_KEY" ]]; then
    print_error "Invalid configuration. Re-run registration."
    exit 1
fi

print_status "🏥 EkyBot Workspace Health Check"
echo "Workspace ID: $WORKSPACE_ID"
echo

# 1. Check OpenClaw Gateway Status
print_status "Checking OpenClaw Gateway..."
if command -v openclaw &> /dev/null; then
    GATEWAY_STATUS=$(openclaw status --json 2>/dev/null || echo '{"error":"failed"}')
    GATEWAY_RUNNING=$(echo "$GATEWAY_STATUS" | python3 -c "import sys, json; data = json.load(sys.stdin); print('true' if 'error' not in data and data.get('gateway', {}).get('running', False) else 'false')" 2>/dev/null)
    
    if [[ "$GATEWAY_RUNNING" == "true" ]]; then
        print_status "✅ Gateway running"
        GATEWAY_PORT=$(echo "$GATEWAY_STATUS" | python3 -c "import sys, json; print(json.load(sys.stdin).get('gateway', {}).get('port', 'unknown'))" 2>/dev/null)
        print_detail "Port: $GATEWAY_PORT"
    else
        print_warning "❌ Gateway not running"
    fi
else
    print_error "❌ OpenClaw CLI not found"
    GATEWAY_RUNNING="false"
fi

# 2. Check Agent Sessions
print_status "Checking agent sessions..."
if [[ "$GATEWAY_RUNNING" == "true" ]]; then
    SESSIONS_OUTPUT=$(openclaw sessions --json 2>/dev/null || echo '[]')
    ACTIVE_SESSIONS=$(echo "$SESSIONS_OUTPUT" | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null)
    print_status "✅ Active sessions: $ACTIVE_SESSIONS"
else
    ACTIVE_SESSIONS=0
    print_warning "Cannot check sessions (gateway not running)"
fi

# 3. System Resources
print_status "Checking system resources..."
if command -v top &> /dev/null; then
    # Get CPU and memory usage (macOS compatible)
    CPU_USAGE=$(top -l 1 -n 0 | grep "CPU usage" | awk '{print $3}' | sed 's/%//' || echo "unknown")
    MEMORY_PRESSURE=$(vm_stat | grep "Pages free" | awk '{print $3}' | sed 's/.$//' || echo "unknown")
    print_detail "CPU usage: ${CPU_USAGE}%"
    print_detail "Memory info available"
else
    print_warning "System monitoring tools not available"
    CPU_USAGE="unknown"
fi

# 4. Disk Space
print_status "Checking disk space..."
DISK_USAGE=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//' || echo "unknown")
print_detail "Disk usage: ${DISK_USAGE}%"

# 5. Last Activity
print_status "Checking last activity..."
if [[ -d "$HOME/.openclaw/agents" ]]; then
    LAST_ACTIVITY=$(find "$HOME/.openclaw/agents" -name "*.jsonl" -type f -exec stat -f "%m" {} \; 2>/dev/null | sort -nr | head -1 | xargs -I{} date -r {} "+%Y-%m-%d %H:%M:%S" 2>/dev/null || echo "unknown")
    print_detail "Last session activity: $LAST_ACTIVITY"
else
    LAST_ACTIVITY="unknown"
    print_warning "Agent directory not found"
fi

# Prepare health data payload
HEALTH_DATA=$(cat <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%S.%3NZ)",
  "status": "$(if [[ "$GATEWAY_RUNNING" == "true" ]]; then echo "healthy"; else echo "degraded"; fi)",
  "gateway": {
    "running": $GATEWAY_RUNNING,
    "port": $(if [[ "$GATEWAY_RUNNING" == "true" ]]; then echo "$GATEWAY_PORT"; else echo "null"; fi)
  },
  "sessions": {
    "active_count": $ACTIVE_SESSIONS
  },
  "system": {
    "cpu_usage": "$(if [[ "$CPU_USAGE" != "unknown" ]]; then echo "${CPU_USAGE}%"; else echo null; fi)",
    "disk_usage": "$(if [[ "$DISK_USAGE" != "unknown" ]]; then echo "${DISK_USAGE}%"; else echo null; fi)"
  },
  "last_activity": "$(if [[ "$LAST_ACTIVITY" != "unknown" ]]; then echo "$LAST_ACTIVITY"; else echo null; fi)"
}
EOF
)

# Send health data to EkyBot
print_status "Sending health report to EkyBot..."

RESPONSE=$(curl -s -X GET "$HEALTH_ENDPOINT" \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json")

if [[ $? -eq 0 ]]; then
    SUCCESS=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', 'false'))" 2>/dev/null || echo "false")
    if [[ "$SUCCESS" == "true" ]]; then
        print_status "✅ Health report sent successfully"
    else
        print_warning "Health report sent but server returned error:"
        echo "$RESPONSE"
    fi
else
    print_error "Failed to send health report to EkyBot"
fi

echo
print_status "Health check complete!"
echo "Full health data:"
echo "$HEALTH_DATA" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_DATA"