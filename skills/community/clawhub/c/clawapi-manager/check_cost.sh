#!/bin/bash
#
# API Cockpit - Cost Check Script
# Queries and reports API usage costs
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_DIR="${SCRIPT_DIR}/lib"
CONFIG_DIR="${SCRIPT_DIR}/config"
LOG_DIR="${SCRIPT_DIR}/logs"
DATA_DIR="${SCRIPT_DIR}/data"
LOCK_DIR="${SCRIPT_DIR}/locks"

# Ensure directories exist
mkdir -p "${LOG_DIR}"
mkdir -p "${DATA_DIR}"
mkdir -p "${LOCK_DIR}"

# File lock to prevent concurrent execution
LOCK_FILE="${LOCK_DIR}/check_cost.lock"
exec 9>"${LOCK_FILE}"
if ! flock -n 9; then
    echo "Script already running, exiting"
    exit 1
fi

# Load environment variables
if [ -f "${CONFIG_DIR}/.env" ]; then
    source "${CONFIG_DIR}/.env"
else
    echo "Error: ${CONFIG_DIR}/.env not found"
    exit 1
fi

# Ensure directories exist
mkdir -p "${LOG_DIR}"
mkdir -p "${DATA_DIR}"

# Timestamp for logging
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="${LOG_DIR}/cost_check_$(date '+%Y%m%d').log"

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

# Check budget threshold
check_budget_threshold() {
    local monthly_report
    monthly_report=$(python3 "${LIB_DIR}/cost_monitor.py" monthly)
    
    local monthly_total
    monthly_total=$(echo "${monthly_report}" | jq -r '.total // 0')
    
    local budget_threshold=${COST_BUDGET_THRESHOLD:-100}
    
    if (( $(echo "${monthly_total} >= ${budget_threshold}" | bc -l) )); then
        local alert="💰 *BUDGET ALERT*: Monthly cost at \$${monthly_total} (threshold: \$${budget_threshold})"
        log "${alert}"
        send_telegram_alert "${alert}"
    fi
}

# Main execution
main() {
    local command="${1:-report}"
    
    case "$command" in
        report)
            python3 "${LIB_DIR}/cost_monitor.py" report
            ;;
        daily)
            python3 "${LIB_DIR}/cost_monitor.py" daily
            ;;
        monthly)
            python3 "${LIB_DIR}/cost_monitor.py" monthly
            ;;
        chart)
            python3 "${LIB_DIR}/cost_monitor.py" chart
            ;;
        record)
            if [ $# -lt 3 ]; then
                echo "Usage: $0 record <provider> <cost>"
                exit 1
            fi
            python3 "${LIB_DIR}/cost_monitor.py" record "$2" "$3"
            ;;
        check)
            log "=== Starting cost check ==="
            check_budget_threshold
            log "=== Cost check complete ==="
            ;;
        *)
            echo "Usage: $0 [report|daily|monthly|chart|record|check]"
            echo ""
            echo "Commands:"
            echo "  report  - Show cost report"
            echo "  daily   - Show daily costs (JSON)"
            echo "  monthly - Show monthly costs (JSON)"
            echo "  chart   - Show chart data (JSON)"
            echo "  record <provider> <cost> - Record a cost entry"
            echo "  check   - Check budget thresholds"
            exit 1
            ;;
    esac
}

main "$@"
