#!/bin/bash
# Enhanced Patent Dashboard Monitoring
# Runs comprehensive checks and can auto-recover

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"
LOG_DIR="$SKILL_DIR/logs"
MONITOR_LOG="$LOG_DIR/enhanced_monitor.log"
FAILURE_COUNT_FILE="$LOG_DIR/failure_count.txt"
ALERT_THRESHOLD=3
AUTO_RECOVER=true

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$MONITOR_LOG"
}

# Alert function
alert() {
    local message="$1"
    local severity="$2"
    
    log "ALERT [$severity]: $message"
    echo "ALERT [$severity] at $(date): $message" >> "$LOG_DIR/alerts.log"
    
    # TODO: Add actual alerting (Telegram, email, etc.)
}

# Increment failure counter
increment_failure() {
    local count=1
    if [ -f "$FAILURE_COUNT_FILE" ]; then
        count=$(cat "$FAILURE_COUNT_FILE")
        count=$((count + 1))
    fi
    echo "$count" > "$FAILURE_COUNT_FILE"
    echo "$count"
}

# Reset failure counter
reset_failure() {
    echo "0" > "$FAILURE_COUNT_FILE"
}

# Check HTTP server
check_http_server() {
    log "🔍 Checking HTTP server..."
    
    # Check if process is running
    local pid=$(ps aux | grep "python3.*8080" | grep -v grep | awk '{print $2}')
    
    if [ -z "$pid" ]; then
        log "❌ HTTP server not running"
        return 1
    fi
    
    # Check if responding
    local response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ 2>/dev/null || echo "FAILED")
    
    if [ "$response" = "200" ]; then
        local uptime=$(ps -p "$pid" -o etime= | xargs)
        log "✅ HTTP server: PID $pid, uptime $uptime, response $response"
        return 0
    else
        log "❌ HTTP server not responding (PID: $pid, response: $response)"
        return 1
    fi
}

# Check Cloudflare tunnel
check_cloudflare_tunnel() {
    log "🔍 Checking Cloudflare tunnel..."
    
    # Check if process is running
    local pid=$(ps aux | grep cloudflared | grep -v grep | awk '{print $2}')
    
    if [ -z "$pid" ]; then
        log "❌ Cloudflare tunnel not running"
        return 1
    fi
    
    # Check tunnel connections (simplified - just check process)
    local connections=$(ps aux | grep cloudflared | grep -v grep | wc -l)
    
    if [ "$connections" -gt 0 ]; then
        log "✅ Cloudflare tunnel: PID $pid, connections detected"
        return 0
    else
        log "❌ Cloudflare tunnel process exists but no connections"
        return 1
    fi
}

# Check public URL accessibility
check_public_url() {
    log "🔍 Checking public URL..."
    
    local response=$(curl -s -o /dev/null -w "%{http_code}" https://hermes.sqncr.ai/Patent_report_kw14/ 2>/dev/null || echo "FAILED")
    
    if [ "$response" = "200" ]; then
        log "✅ Public URL accessible: HTTP $response"
        return 0
    elif [ "$response" = "530" ]; then
        log "⚠️ Public URL Cloudflare error: HTTP $response (tunnel issue)"
        return 1
    elif [ "$response" = "404" ]; then
        log "❌ Public URL not found: HTTP $response"
        return 1
    else
        log "❌ Public URL check failed: $response"
        return 1
    fi
}

# Check database
check_database() {
    log "🔍 Checking database..."
    
    local db_path="$SKILL_DIR/data/patents.db"
    
    if [ ! -f "$db_path" ]; then
        log "❌ Database file not found: $db_path"
        return 1
    fi
    
    # Try to query the database
    local count=$(python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('$db_path')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM patents')
    result = cursor.fetchone()[0]
    print(result)
    conn.close()
except Exception as e:
    print('ERROR')
" 2>/dev/null)
    
    if [[ "$count" =~ ^[0-9]+$ ]]; then
        log "✅ Database healthy: $count patents"
        return 0
    else
        log "❌ Database query failed"
        return 1
    fi
}

# Auto-recovery function
auto_recover() {
    log "🚀 Attempting auto-recovery..."
    
    # Kill existing processes
    pkill -f "python3.*http.server" 2>/dev/null || true
    pkill cloudflared 2>/dev/null || true
    sleep 2
    
    # Start services
    cd "$SKILL_DIR/scripts"
    bash start_cloudflare_tunnel.sh > /tmp/recovery.log 2>&1 &
    
    log "✅ Auto-recovery initiated. Check /tmp/recovery.log for details."
}

# Main monitoring function
main() {
    log "=== Enhanced Patent Dashboard Monitoring ==="
    
    local failures=0
    
    # Run checks
    check_http_server || failures=$((failures + 1))
    check_cloudflare_tunnel || failures=$((failures + 1))
    check_public_url || failures=$((failures + 1))
    check_database || failures=$((failures + 1))
    
    # Determine overall status
    if [ "$failures" -eq 0 ]; then
        log "✅ All systems operational"
        reset_failure
    else
        log "⚠️ $failures check(s) failed"
        local failure_count=$(increment_failure)
        log "Failure count: $failure_count"
        
        # Check if we should alert
        if [ "$failure_count" -ge "$ALERT_THRESHOLD" ]; then
            alert "Patent Dashboard has been unhealthy for $failure_count consecutive checks. $failures issues detected." "CRITICAL"
            
            # Auto-recover if enabled
            if [ "$AUTO_RECOVER" = true ] && [ "$failure_count" -ge "$ALERT_THRESHOLD" ]; then
                auto_recover
            fi
        elif [ "$failure_count" -eq 1 ]; then
            alert "Patent Dashboard is unhealthy. $failures issues detected." "WARNING"
        fi
    fi
    
    log "=== Monitoring complete ==="
}

# Run main function
main "$@"