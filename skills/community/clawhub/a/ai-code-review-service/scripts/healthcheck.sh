#!/bin/bash
# Service Health Check Script for Code Review Platform
# Monitors all core services and sends alerts to Discord

set -e

# Configuration
SERVICES=("nginx" "docker" "code-review-service" "whisper-api-gateway")
DISCORD_WEBHOOK_URL="${DISCORD_WEBHOOK_URL:-}"
LOG_FILE="/var/log/code_review_healthcheck.log"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

send_alert() {
    local message="$1"
    if [ -z "$DISCORD_WEBHOOK_URL" ]; then
        return
    fi
    
    curl -s -H "Content-Type: application/json" \
         -X POST \
         -d "{\"content\": \"🚨 **HEALTH ALERT**: $message\"}" \
         "$DISCORD_WEBHOOK_URL" > /dev/null 2>&1
}

echo "====================================="
echo " Code Review Platform Health Check   "
echo "====================================="

all_healthy=true

for service in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "$service"; then
        echo -e "${GREEN}✅ $service is running${NC}"
        log "$service is running"
    else
        all_healthy=false
        echo -e "${RED}❌ $service is NOT running${NC}"
        log "$service is NOT running"
        
        # Try to restart the service
        echo -e "${YELLOW}Attempting to restart $service...${NC}"
        if systemctl restart "$service" > /dev/null 2>&1; then
            if systemctl is-active --quiet "$service"; then
                echo -e "${GREEN}✅ $service restarted successfully${NC}"
                log "$service restarted successfully"
                send_alert "Service $service was down and successfully restarted"
            else
                echo -e "${RED}❌ Failed to restart $service${NC}"
                log "Failed to restart $service"
                send_alert "CRITICAL: Service $service is down and failed to restart - manual intervention required"
            fi
        else
            echo -e "${RED}❌ Failed to restart $service${NC}"
            log "Failed to restart $service"
            send_alert "CRITICAL: Service $service is down and failed to restart - manual intervention required"
        fi
    fi
    echo "-------------------------------------"
done

# Check disk usage
echo "Disk Usage Check:"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
echo "Root partition usage: $DISK_USAGE%"
log "Root partition usage: $DISK_USAGE%"

if [ "$DISK_USAGE" -ge 90 ]; then
    all_healthy=false
    echo -e "${RED}❌ Disk usage critical: $DISK_USAGE%${NC}"
    send_alert "CRITICAL: Disk usage is at $DISK_USAGE% - please free up space immediately"
elif [ "$DISK_USAGE" -ge 80 ]; then
    echo -e "${YELLOW}⚠️  Disk usage warning: $DISK_USAGE%${NC}"
    send_alert "Warning: Disk usage is at $DISK_USAGE%"
fi
echo "-------------------------------------"

# Summary
if [ "$all_healthy" = true ]; then
    echo -e "${GREEN}✅ All services are healthy!${NC}"
    log "Health check completed: All services healthy"
    exit 0
else
    echo -e "${RED}❌ Some services require attention!${NC}"
    log "Health check completed: Some services unhealthy"
    exit 1
fi