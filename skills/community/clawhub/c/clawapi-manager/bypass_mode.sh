#!/bin/bash
#
# API Cockpit - Bypass Mode Controller
# Ensures OpenClaw can work directly even if cockpit fails
# Implements: 旁路模式，cockpit 挂不影响 OpenClaw 直连
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/data"
BYPASS_STATE_FILE="${DATA_DIR}/bypass_state.json"

mkdir -p "${DATA_DIR}"

# Get current bypass state
get_bypass_state() {
    if [ -f "${BYPASS_STATE_FILE}" ]; then
        cat "${BYPASS_STATE_FILE}"
    else
        echo '{"enabled": false, "reason": "", "timestamp": ""}'
    fi
}

# Enable bypass mode
enable_bypass() {
    local reason="${1:-manual}"
    local timestamp
    timestamp=$(date -Iseconds)
    
    # Read current state
    local state
    state=$(get_bypass_state)
    
    # Update state
    local new_state
    new_state=$(echo "${state}" | jq \
        --arg reason "${reason}" \
        --arg timestamp "${timestamp}" \
        '.enabled = true | .reason = $reason | .timestamp = $timestamp')
    
    # Atomic write
    local tmp="${BYPASS_STATE_FILE}.$$"
    echo "${new_state}" > "${tmp}"
    mv "${tmp}" "${BYPASS_STATE_FILE}"
    
    echo "Bypass mode ENABLED: ${reason}"
}

# Disable bypass mode
disable_bypass() {
    local timestamp
    timestamp=$(date -Iseconds)
    
    local state
    state=$(get_bypass_state)
    
    local new_state
    new_state=$(echo "${state}" | jq \
        --arg timestamp "${timestamp}" \
        '.enabled = false | .timestamp = $timestamp')
    
    local tmp="${BYPASS_STATE_FILE}.$$"
    echo "${new_state}" > "${tmp}"
    mv "${tmp}" "${BYPASS_STATE_FILE}"
    
    echo "Bypass mode DISABLED"
}

# Check if bypass is enabled
is_bypass_enabled() {
    local state
    state=$(get_bypass_state)
    echo "${state}" | jq -r '.enabled'
}

# Get bypass status
get_status() {
    get_bypass_state | jq .
}

# Auto-enable bypass on cockpit failure
# This should be called by health check when cockpit is down
auto_bypass_on_failure() {
    local failure_reason="${1:-health_check_failed}"
    
    # Only enable bypass if not already enabled
    if [ "$(is_bypass_enabled)" == "false" ]; then
        enable_bypass "auto:${failure_reason}"
        echo "Auto-enabled bypass due to: ${failure_reason}"
    else
        echo "Bypass already enabled"
    fi
}

# Main
case "${1:-status}" in
    enable)
        enable_bypass "${2:-manual}"
        ;;
    disable)
        disable_bypass
        ;;
    status)
        get_status
        ;;
    is-enabled)
        is_bypass_enabled
        ;;
    auto-bypass)
        auto_bypass_on_failure "${2:-unknown}"
        ;;
    *)
        get_status
        ;;
esac
