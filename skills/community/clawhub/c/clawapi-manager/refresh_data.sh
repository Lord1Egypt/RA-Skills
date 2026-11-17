#!/bin/bash
#
# API Cockpit - Data Refresh Script
# Generates data.json for Dashboard polling
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_FILE="${SCRIPT_DIR}/data/data.json"
DATA_FILE_TMP="${DATA_FILE}.tmp"
LOCK_FILE="${SCRIPT_DIR}/locks/refresh_data.lock"

# Ensure lock directory exists
mkdir -p "${SCRIPT_DIR}/locks"

# File lock
exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
    echo "Another refresh in progress"
    exit 1
fi

# Get timestamp
TIMESTAMP=$(date -Iseconds)

# Helper: atomic write
atomic_write() {
    local content="$1"
    local target="$2"
    local tmp="${target}.tmp.$$"
    echo "${content}" > "${tmp}"
    mv "${tmp}" "${target}"
}

# Get health data from nodes
get_health_data() {
    local health='{"nodes":{},"gateway":{},"status":"ok"}'
    echo "${health}"
}

# Get cost data
get_cost_data() {
    if [ -f "${SCRIPT_DIR}/data/costs.json" ]; then
        python3 -c "
import json
import sys
from datetime import datetime

with open('${SCRIPT_DIR}/data/costs.json') as f:
    costs = json.load(f)

today = datetime.now().strftime('%Y-%m-%d')
month = datetime.now().strftime('%Y-%m')

today_cost = sum(costs['daily'].get(today, {}).values())
month_cost = sum(costs['monthly'].get(month, {}).values())

print(json.dumps({'today': today_cost, 'month': month_cost, 'by_model': costs['monthly'].get(month, {})}))
"
    else
        echo '{"today":0,"month":0,"by_model":{}}'
    fi
}

# Get quota data
get_quota_data() {
    echo '{"providers":{}}'
}

# Generate data.json
generate_data() {
    local health_data
    local cost_data
    local quota_data
    
    health_data=$(get_health_data)
    cost_data=$(get_cost_data)
    quota_data=$(get_quota_data)
    
    # Build JSON
    local json
    json=$(cat <<EOF
{
  "version": "1.0",
  "timestamp": "${TIMESTAMP}",
  "health": ${health_data},
  "cost": ${cost_data},
  "quota": ${quota_data},
  "alerts": []
}
EOF
)
    
    atomic_write "${json}" "${DATA_FILE}"
    echo "Data refreshed at ${TIMESTAMP}"
}

# Main
case "${1:-}" in
    refresh)
        generate_data
        ;;
    *)
        generate_data
        ;;
esac
