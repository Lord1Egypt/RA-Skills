#!/bin/bash
#
# API Cockpit - Unified Quota Check Script
# Queries all configured API providers and reports quota status
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="${SCRIPT_DIR}/lib"
CONFIG_DIR="${SCRIPT_DIR}/config"
LOG_DIR="${SCRIPT_DIR}/logs"

# Load environment variables
if [ -f "${CONFIG_DIR}/.env" ]; then
    source "${CONFIG_DIR}/.env"
else
    echo "Error: ${CONFIG_DIR}/.env not found. Copy .env.example and configure it."
    exit 1
fi

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

# Timestamp for logging
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="${LOG_DIR}/quota_check_$(date '+%Y%m%d').log"

# Function to log messages
log() {
    echo "[${TIMESTAMP}] $*" | tee -a "${LOG_FILE}"
}

# Function to send Telegram alert
send_telegram_alert() {
    local message="$1"
    
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${message}" \
            -d "parse_mode=Markdown" > /dev/null 2>&1
    fi
}

# Function to check quota for a provider
check_provider() {
    local provider="$1"
    local script="${LIB_DIR}/${provider}.py"
    
    if [ ! -f "${script}" ]; then
        log "Warning: ${provider} adapter not found"
        return 1
    fi
    
    log "Checking ${provider}..."
    
    local result
    result=$(python3 "${script}" quota 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "${result}"
        
        # Parse quota percentage
        local percentage
        percentage=$(echo "${result}" | jq -r '.quota.percentage // 0')
        
        # Check thresholds
        if (( $(echo "${percentage} >= ${QUOTA_CRITICAL_THRESHOLD:-95}" | bc -l) )); then
            local alert="🚨 *CRITICAL*: ${provider} quota at ${percentage}%"
            log "${alert}"
            send_telegram_alert "${alert}"
        elif (( $(echo "${percentage} >= ${QUOTA_WARNING_THRESHOLD:-80}" | bc -l) )); then
            local alert="⚠️ *WARNING*: ${provider} quota at ${percentage}%"
            log "${alert}"
            send_telegram_alert "${alert}"
        else
            log "${provider} quota OK: ${percentage}%"
        fi
    else
        log "Error checking ${provider}: ${result}"
        send_telegram_alert "❌ *ERROR*: Failed to check ${provider} quota"
    fi
}

# Main execution
main() {
    log "=== Starting quota check ==="
    
    local providers=("antigravity" "codex" "copilot" "windsurf")
    local results=()
    
    for provider in "${providers[@]}"; do
        result=$(check_provider "${provider}")
        if [ -n "${result}" ]; then
            results+=("${result}")
        fi
    done
    
    # Generate summary
    log "=== Quota check complete ==="
    
    # Output JSON summary
    if [ ${#results[@]} -gt 0 ]; then
        echo "{"
        echo "  \"timestamp\": \"$(date -Iseconds)\","
        echo "  \"providers\": ["
        for i in "${!results[@]}"; do
            echo "${results[$i]}"
            if [ $i -lt $((${#results[@]} - 1)) ]; then
                echo ","
            fi
        done
        echo "  ]"
        echo "}"
    fi
}

# Run main function
main "$@"
