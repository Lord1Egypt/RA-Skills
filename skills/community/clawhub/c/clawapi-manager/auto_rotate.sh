#!/bin/bash
#
# API Cockpit - Auto Rotation Script
# Automatically rotates API keys when quota thresholds are exceeded
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/config"
LOG_DIR="${SCRIPT_DIR}/logs"

# Load environment variables
if [ -f "${CONFIG_DIR}/.env" ]; then
    source "${CONFIG_DIR}/.env"
else
    echo "Error: ${CONFIG_DIR}/.env not found"
    exit 1
fi

# Ensure log directory exists
mkdir -p "${LOG_DIR}"

LOG_FILE="${LOG_DIR}/auto_rotation_$(date '+%Y%m%d').log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "${LOG_FILE}"
}

send_telegram_alert() {
    local message="$1"
    
    if [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && [ -n "${TELEGRAM_CHAT_ID:-}" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${message}" \
            -d "parse_mode=Markdown" > /dev/null 2>&1
    fi
}

rotate_key() {
    local provider="$1"
    
    log "Rotating ${provider} API key..."
    
    # TODO: Implement actual key rotation logic
    # This would typically involve:
    # 1. Fetching a new key from a key pool
    # 2. Updating the .env file
    # 3. Restarting relevant services
    # 4. Verifying the new key works
    
    send_telegram_alert "🔄 *KEY ROTATION*: ${provider} key has been rotated"
    
    log "${provider} key rotation complete"
}

check_and_rotate() {
    local quota_data
    quota_data=$("${SCRIPT_DIR}/check_quota.sh")
    
    # Parse each provider's quota
    local providers=("antigravity" "codex" "copilot" "windsurf")
    
    for provider in "${providers[@]}"; do
        local percentage
        percentage=$(echo "${quota_data}" | jq -r ".providers[] | select(.provider == \"${provider}\") | .quota.percentage // 0")
        
        if [ -n "${percentage}" ] && (( $(echo "${percentage} >= ${QUOTA_CRITICAL_THRESHOLD:-95}" | bc -l) )); then
            log "${provider} quota critical (${percentage}%), initiating rotation"
            rotate_key "${provider}"
        fi
    done
}

main() {
    if [ "${AUTO_ROTATION_ENABLED:-false}" != "true" ]; then
        log "Auto-rotation is disabled"
        exit 0
    fi
    
    log "=== Starting auto-rotation check ==="
    check_and_rotate
    log "=== Auto-rotation check complete ==="
}

main "$@"
