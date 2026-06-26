# Dashboard Recovery Procedures

## Overview
This document outlines procedures for recovering the Patent Dashboard when it becomes inaccessible (404/530 errors).

## Quick Recovery Steps

### 1. Check Current Status
```bash
# Check if HTTP server is running
ps aux | grep "python3.*http.server" | grep -v grep

# Check if Cloudflare tunnel is running
ps aux | grep cloudflared | grep -v grep

# Test local access
curl -I http://localhost:8080/Patent_report_kw14/

# Test public access
curl -I https://hermes.sqncr.ai/Patent_report_kw14/
```

### 2. Restart Services
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence/scripts
bash start_cloudflare_tunnel.sh
```

### 3. Verify Recovery
```bash
# Wait 30 seconds for tunnel to establish
sleep 30

# Test both endpoints
LOCAL_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/Patent_report_kw14/)
PUBLIC_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://hermes.sqncr.ai/Patent_report_kw14/ 2>/dev/null || echo "FAILED")

echo "Local: $LOCAL_STATUS, Public: $PUBLIC_STATUS"
```

## Monitoring Procedures

### Health Check Script
The health monitor script runs checks and logs issues:
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence/scripts
bash health_monitor.sh
```

### Alert Thresholds
- **Warning**: Single check failure
- **Critical**: 3 consecutive failures
- **Auto-recovery**: Script can attempt restart after critical alert

### Manual Monitoring Commands
```bash
# Check recent alerts
tail -20 /root/.openclaw/workspace/skills/epo-patent-intelligence/logs/alerts.log

# Check health monitor logs
tail -20 /root/.openclaw/workspace/skills/epo-patent-intelligence/logs/health_monitor.log

# Check failure count
cat /root/.openclaw/workspace/skills/epo-patent-intelligence/logs/failure_count.txt
```

## Automation Readiness

### Before Monday 09:00 UTC Automation
1. **Verify server is running** (at least 30 minutes before automation)
2. **Test both endpoints** (local and public)
3. **Check database health** (48 patents expected)
4. **Verify automation script** (`weekly_automation_enhanced.sh`)

### Automation Failure Recovery
If automation fails:
1. Check logs: `/root/.openclaw/workspace/skills/epo-patent-intelligence/logs/weekly_report.log`
2. Verify EPO API credentials in `.env` file
3. Check database connectivity
4. Manual restart: `cd /root/.openclaw/workspace/skills/epo-patent-intelligence && ./scripts/weekly_automation_enhanced.sh`

## Troubleshooting

### Common Issues

#### 1. HTTP Server Not Running
```bash
# Kill any existing server
pkill -f "python3.*http.server"

# Start fresh
cd /root/.openclaw/workspace/skills/epo-patent-intelligence/reports
python3 -m http.server 8080 > /tmp/http_server.log 2>&1 &
```

#### 2. Cloudflare Tunnel Issues
```bash
# Kill existing tunnel
pkill cloudflared

# Restart with token
export TUNNEL_TOKEN="eyJhIjoiNmRiMjNkNDYxZjU5YjkyZjdmM2UyM2RkZjYwNjZkYzAiLCJ0IjoiZmE1M2NmZGEtOTYzMy00NDQ0LWJiMzItZDI4ZjllMTI3NTkyIiwicyI6IllUWmlaalk0Tm1NdFptRTNNQzAwTmpoaExUbGhaREF0WkRrNU1XWTFPRFExWW1VNCJ9"
cloudflared tunnel --no-autoupdate run --token "$TUNNEL_TOKEN" --url http://localhost:8080 2>&1 &
```

#### 3. Database Issues
```bash
# Check patent count
python3 -c "
import sqlite3
conn = sqlite3.connect('/root/.openclaw/workspace/skills/epo-patent-intelligence/data/patents.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM patents')
print(f'Patents: {cursor.fetchone()[0]}')
conn.close()
"
```

## Prevention

### Scheduled Maintenance
- **Daily**: Health checks at 06:00 UTC
- **Weekly**: Automation at 09:00 UTC Monday
- **Monthly**: Database backup verification

### Monitoring Enhancements
- Implement automated tunnel health checks
- Add fallback origin routing
- Set up notification alerts for critical failures

## Contact & Escalation
- Primary: Heartbeat agent (runs every 60 minutes)
- Backup: Manual intervention via Telegram
- Critical: System administrator notification

---
*Last Updated: 2026-04-06*
*Version: 1.0*