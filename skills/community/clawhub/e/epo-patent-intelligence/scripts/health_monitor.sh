#!/bin/bash
# Patent Bot Health Monitoring Script
# Checks system health and sends alerts if issues detected

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
LOG_DIR="$SKILL_DIR/logs"
HEALTH_LOG="$LOG_DIR/health_monitor.log"
ALERT_THRESHOLD=3  # Number of consecutive failures before alert

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$HEALTH_LOG"
}

# Alert function (placeholder - implement actual alerting)
alert() {
    local message="$1"
    local severity="$2"
    
    log "ALERT [$severity]: $message"
    
    # TODO: Implement actual alerting mechanisms:
    # - Email notifications
    # - Slack/Teams webhooks
    # - SMS alerts
    # - PagerDuty integration
    
    # For now, just log to file
    echo "ALERT [$severity] at $(date): $message" >> "$LOG_DIR/alerts.log"
}

# Check HTTP server
check_http_server() {
    local pid=$(ps aux | grep "python3.*8080" | grep -v grep | awk '{print $2}')
    
    if [ -z "$pid" ]; then
        log "❌ HTTP server not running"
        return 1
    else
        # Check if server is responding
        local response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>/dev/null || echo "FAILED")
        
        if [ "$response" = "200" ]; then
            local uptime=$(ps -p "$pid" -o etime= | xargs)
            log "✅ HTTP server: PID $pid, uptime $uptime, response $response"
            return 0
        else
            log "❌ HTTP server running (PID $pid) but not responding (code: $response)"
            return 1
        fi
    fi
}

# Check Cloudflare tunnel
check_tunnel() {
    local pid=$(ps aux | grep cloudflared | grep -v grep | awk '{print $2}')
    
    if [ -z "$pid" ]; then
        log "❌ Cloudflare tunnel not running"
        return 1
    else
        local uptime=$(ps -p "$pid" -o etime= | xargs)
        log "✅ Cloudflare tunnel: PID $pid, uptime $uptime"
        return 0
    fi
}

# Check database
check_database() {
    local db_path="$SKILL_DIR/data/patents.db"
    
    if [ ! -f "$db_path" ]; then
        log "❌ Database file not found: $db_path"
        return 1
    fi
    
    # Check database integrity
    local result=$(python3 -c "
import sqlite3
import sys

try:
    conn = sqlite3.connect('$db_path')
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='patents';\")
    if not cursor.fetchone():
        print('TABLE_MISSING')
        sys.exit(1)
    
    # Check patent count
    cursor.execute('SELECT COUNT(*) FROM patents')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print('EMPTY_DATABASE')
        sys.exit(1)
    
    # Check for corruption
    cursor.execute('PRAGMA integrity_check')
    integrity = cursor.fetchone()[0]
    
    if integrity != 'ok':
        print('CORRUPTED')
        sys.exit(1)
    
    conn.close()
    print(f'OK:{count}')
    sys.exit(0)
    
except Exception as e:
    print(f'ERROR:{str(e)}')
    sys.exit(1)
" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        local count=$(echo "$result" | cut -d':' -f2)
        log "✅ Database: $count patents, integrity OK"
        return 0
    else
        log "❌ Database issue: $result"
        return 1
    fi
}

# Check disk space
check_disk_space() {
    local threshold=10  # Alert when less than 10% free
    local free_percent=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    local free_gb=$(df -h / | awk 'NR==2 {print $4}')
    
    if [ "$free_percent" -lt "$threshold" ]; then
        log "⚠️  Low disk space: $free_gb free ($free_percent% used)"
        return 1
    else
        log "✅ Disk space: $free_gb free ($free_percent% used)"
        return 0
    fi
}

# Check memory usage
check_memory() {
    local threshold=90  # Alert when more than 90% used
    local used_percent=$(free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}')
    
    if [ "$used_percent" -gt "$threshold" ]; then
        log "⚠️  High memory usage: $used_percent% used"
        return 1
    else
        log "✅ Memory usage: $used_percent% used"
        return 0
    fi
}

# Check cron job
check_cron() {
    if crontab -l 2>/dev/null | grep -q "weekly_automation_enhanced.sh"; then
        log "✅ Cron job configured"
        return 0
    else
        log "❌ Cron job not found"
        return 1
    fi
}

# Check recent logs for errors
check_logs() {
    local error_count=0
    local log_files=("$LOG_DIR/weekly_report.log" "$LOG_DIR/cron.log" "$LOG_DIR/collection.log")
    
    for log_file in "${log_files[@]}"; do
        if [ -f "$log_file" ]; then
            # Count errors in last 24 hours (exclude benign warnings)
            local errors=$(grep -i "error\|failed\|❌" "$log_file" | grep -v "⚠️ Report not yet generated" | grep -c "$(date -d '24 hours ago' '+%Y-%m-%d')")
            local warnings=$(grep -i "⚠️" "$log_file" | grep -c "$(date -d '24 hours ago' '+%Y-%m-%d')")
            
            if [ "$errors" -gt 0 ]; then
                log "⚠️  Found $errors errors in $(basename "$log_file")"
                error_count=$((error_count + errors))
            fi
            
            if [ "$warnings" -gt 0 ] && [ "$errors" -eq 0 ]; then
                log "ℹ️  Found $warnings warnings in $(basename "$log_file") (non-critical)"
            fi
        fi
    done
    
    if [ "$error_count" -eq 0 ]; then
        log "✅ No recent errors in logs"
        return 0
    else
        log "❌ Total recent errors: $error_count"
        return 1
    fi
}

# Main health check
main() {
    log "=== Patent Bot Health Check ==="
    log "Starting at $(date)"
    
    local failures=0
    local checks=()
    
    # Run all checks
    checks+=("HTTP Server" check_http_server)
    checks+=("Cloudflare Tunnel" check_tunnel)
    checks+=("Database" check_database)
    checks+=("Disk Space" check_disk_space)
    checks+=("Memory Usage" check_memory)
    checks+=("Cron Job" check_cron)
    checks+=("Logs" check_logs)
    
    # Execute checks
    for ((i=0; i<${#checks[@]}; i+=2)); do
        local check_name="${checks[i]}"
        local check_func="${checks[i+1]}"
        
        log "Checking $check_name..."
        if $check_func; then
            log "  $check_name: ✅ PASS"
        else
            log "  $check_name: ❌ FAIL"
            failures=$((failures + 1))
        fi
    done
    
    # Summary
    log ""
    log "=== Health Check Summary ==="
    log "Total checks: $(( ${#checks[@]} / 2 ))"
    log "Passed: $(( (${#checks[@]} / 2) - failures ))"
    log "Failed: $failures"
    
    if [ "$failures" -eq 0 ]; then
        log "Overall status: ✅ HEALTHY"
        
        # Check for consecutive failures in alert tracking
        if [ -f "$LOG_DIR/failure_count.txt" ]; then
            rm "$LOG_DIR/failure_count.txt"
        fi
    else
        log "Overall status: ❌ UNHEALTHY ($failures issues)"
        
        # Track consecutive failures
        if [ -f "$LOG_DIR/failure_count.txt" ]; then
            local current_count=$(cat "$LOG_DIR/failure_count.txt")
            current_count=$((current_count + 1))
        else
            local current_count=1
        fi
        
        echo "$current_count" > "$LOG_DIR/failure_count.txt"
        
        # Send alert if threshold reached
        if [ "$current_count" -ge "$ALERT_THRESHOLD" ]; then
            alert "Patent Bot system has been unhealthy for $current_count consecutive checks. $failures issues detected." "CRITICAL"
        elif [ "$current_count" -eq 1 ]; then
            alert "Patent Bot system is unhealthy. $failures issues detected." "WARNING"
        fi
    fi
    
    log "Health check completed at $(date)"
    log ""
}

# Run main function
main "$@"