# Maintenance Procedures - Patent Bot
**Last Updated:** April 5, 2026  
**System Status:** ✅ Production Ready

---

## Overview

This document outlines maintenance procedures for the Patent Bot system, including weekly automation, health monitoring, troubleshooting, and backup procedures.

## System Architecture

### Components
1. **HTTP Server:** Python HTTP server on port 8080
2. **Cloudflare Tunnel:** Public access via hermes.sqncr.ai
3. **Database:** SQLite at `data/patents.db`
4. **Automation:** Weekly cron job (Monday 9:00 AM)
5. **Monitoring:** Health check script
6. **Dashboards:** Weekly reports (KW14-KW17)

### Directory Structure
```
epo-patent-intelligence/
├── data/                    # Database and backups
├── reports/                 # Weekly dashboards
├── logs/                    # System logs
├── scripts/                 # Automation scripts
├── docs/                    # Documentation
└── .env                     # Configuration (SECURE)
```

## Weekly Maintenance

### Monday 9:00 AM (Automated)
The system automatically runs weekly automation:

1. **Script:** `weekly_automation_enhanced.sh`
2. **Actions:**
   - Fetch new patents from EPO API
   - Update database with deduplication
   - Generate technology trend analysis
   - Update current week's dashboard
   - Create analysis request for LLM agent
3. **Logs:** `logs/cron.log`

### Manual Verification (Monday 10:00 AM)
After automated run, verify:
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Check if automation ran
tail -20 logs/cron.log

# Verify dashboard updated
curl -s http://localhost:8080/Patent_report_kw$(date +%V)/ | grep -q "Technology Focus Analysis" && echo "✅ Dashboard updated"

# Check database
python3 -c "import sqlite3; conn=sqlite3.connect('data/patents.db'); c=conn.cursor(); c.execute('SELECT COUNT(*) FROM patents'); print(f'Total patents: {c.fetchone()[0]}')"
```

## Daily Health Monitoring

### Automated Monitoring
Run health check manually or schedule via cron:
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
./scripts/health_monitor.sh
```

### Health Check Components
1. **HTTP Server:** Process running and responding
2. **Cloudflare Tunnel:** Process running
3. **Database:** File exists, integrity OK, not empty
4. **Disk Space:** >10% free
5. **Memory Usage:** <90% used
6. **Cron Job:** Configured correctly
7. **Logs:** No critical errors

### Alert Thresholds
- **Warning:** First failure detected
- **Critical:** 3 consecutive failures
- **Current:** Logs to `logs/alerts.log` (extend for email/Slack)

## Monthly Maintenance

### 1. Archive Old Reports (1st of month)
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Keep only last 4 weeks, archive older
current_week=$(date +%V)
for week in $(seq 1 $((current_week - 4))); do
    if [ -d "reports/Patent_report_kw${week}" ]; then
        tar -czf "reports/archive_kw${week}.tar.gz" "reports/Patent_report_kw${week}"
        rm -rf "reports/Patent_report_kw${week}"
    fi
done
```

### 2. Database Maintenance
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Backup database
cp data/patents.db "data/backups/patents_$(date +%Y%m).db"

# Vacuum database (reclaim space)
python3 -c "
import sqlite3
conn = sqlite3.connect('data/patents.db')
conn.execute('VACUUM')
conn.close()
print('Database vacuumed')
"

# Clean old backups (keep 3 months)
find data/backups/ -name "*.db" -mtime +90 -delete
```

### 3. Log Rotation
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Compress logs older than 30 days
find logs/ -name "*.log" -mtime +30 -exec gzip {} \;

# Delete compressed logs older than 90 days
find logs/ -name "*.log.gz" -mtime +90 -delete
```

## Quarterly Maintenance

### 1. Technology Keyword Update
Review and update technology categorization keywords in `generate_tech_trend_report.py`:
- Check for new technology terms
- Update categorization logic
- Test with recent patents

### 2. Competitor List Review
Update competitor list in `weekly_automation_enhanced.sh`:
- Add new competitors
- Remove inactive companies
- Adjust search queries

### 3. Performance Review
```bash
# Check system performance trends
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Database growth
ls -lh data/patents.db

# Log size analysis
du -sh logs/

# Response time trend
grep "response" logs/health_monitor.log | tail -10
```

## Troubleshooting Guide

### Issue: HTTP Server Not Responding
**Symptoms:** Dashboard inaccessible, health check fails
**Resolution:**
```bash
# Check if process exists
ps aux | grep "python3.*8080"

# Restart if needed
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
pkill -f "python3.*8080"
python3 -m http.server 8080 &
```

### Issue: Cloudflare Tunnel Down
**Symptoms:** Public URL inaccessible, health check fails
**Resolution:**
```bash
# Check tunnel status
ps aux | grep cloudflared

# Restart tunnel
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
pkill cloudflared
./scripts/start_tunnel.sh &
```

### Issue: Database Corruption
**Symptoms:** Health check reports database issues, queries fail
**Resolution:**
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Restore from backup
if [ -f "data/backups/patents_latest.db" ]; then
    cp data/backups/patents_latest.db data/patents.db
    echo "Database restored from backup"
else
    # Recreate database
    rm -f data/patents.db
    python3 scripts/epo_data_mapper.py "pa=IBM" 1 5
    echo "Database recreated with sample data"
fi
```

### Issue: Cron Job Not Running
**Symptoms:** No weekly reports, empty cron.log
**Resolution:**
```bash
# Check cron configuration
crontab -l | grep "weekly_automation"

# Reinstall cron job
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
./scripts/setup_cron.sh

# Test manually
./scripts/weekly_automation_enhanced.sh
```

### Issue: EPO API Authentication Failed
**Symptoms:** No new patents collected, API errors in logs
**Resolution:**
```bash
# Check .env file
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
head -10 .env

# Test API credentials
python3 -c "
import os
from scripts.epo_data_mapper import EPODataMapper

mapper = EPODataMapper()
try:
    patents = mapper.search_patents('pa=IBM', 1, 2)
    print(f'✅ API working: {len(patents)} patents found')
except Exception as e:
    print(f'❌ API error: {e}')
"
```

## Backup Procedures

### Automated Backups
Configure in cron (add to crontab):
```bash
# Daily database backup at 2:00 AM
0 2 * * * cd /root/.openclaw/workspace/skills/epo-patent-intelligence && cp data/patents.db "data/backups/patents_$(date +\%Y\%m\%d).db"

# Weekly full backup at 3:00 AM Sunday
0 3 * * 0 cd /root/.openclaw/workspace/skills/epo-patent-intelligence && tar -czf "/root/backups/patent_bot_$(date +\%Y\%m\%d).tar.gz" . --exclude=".env" --exclude="data/backups"
```

### Manual Backup
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Database only
cp data/patents.db "data/backups/patents_manual_$(date +%Y%m%d_%H%M).db"

# Full system (excluding credentials)
tar -czf "/tmp/patent_bot_backup_$(date +%Y%m%d).tar.gz" . \
    --exclude=".env" \
    --exclude="data/backups/*" \
    --exclude="logs/*.log" \
    --exclude="*.pyc" \
    --exclude="__pycache__"
```

### Restore Procedure
```bash
# Stop services
pkill -f "python3.*8080"
pkill cloudflared

# Restore from backup
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
tar -xzf /path/to/backup.tar.gz

# Restart services
python3 -m http.server 8080 &
./scripts/start_tunnel.sh &
```

## Security Procedures

### Credential Management
- **.env file:** Never commit to version control
- **Permissions:** chmod 600 .env
- **Rotation:** Change EPO API keys quarterly
- **Backup:** Exclude from system backups

### Access Control
- **SSH:** Key-based authentication only
- **Firewall:** Allow only necessary ports (22, 8080 local)
- **Monitoring:** Log all access attempts

### Audit Logging
```bash
# Review access logs
grep "Accepted\|Failed" /var/log/auth.log

# Check system logs
journalctl -u cron --since "1 week ago"

# Review application logs
tail -100 /root/.openclaw/workspace/skills/epo-patent-intelligence/logs/cron.log
```

## Performance Optimization

### Database Optimization
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence

# Create indexes (if not exists)
python3 -c "
import sqlite3
conn = sqlite3.connect('data/patents.db')
c = conn.cursor()

indexes = [
    'CREATE INDEX IF NOT EXISTS idx_patent_id ON patents(patent_id)',
    'CREATE INDEX IF NOT EXISTS idx_company ON patents(company)',
    'CREATE INDEX IF NOT EXISTS idx_date ON patents(publication_date)',
    'CREATE INDEX IF NOT EXISTS idx_category ON patents(category)'
]

for idx in indexes:
    c.execute(idx)

conn.commit()
conn.close()
print('Indexes created/verified')
"
```

### Log Optimization
```bash
# Configure log rotation
cat > /etc/logrotate.d/patent-bot << EOF
/root/.openclaw/workspace/skills/epo-patent-intelligence/logs/*.log {
    weekly
    rotate 4
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
EOF
```

## Emergency Contact

### Primary Contact
- **System:** Heartbeat Agent (auto-detects issues)
- **Logs:** `logs/alerts.log`
- **Dashboard:** https://hermes.sqncr.ai/Patent_report_kw14

### Escalation Path
1. **Automated Alert:** Heartbeat agent detects issue
2. **Manual Check:** Run `./scripts/health_monitor.sh`
3. **Troubleshoot:** Follow procedures in this document
4. **Manual Recovery:** Use backup and restore procedures

### Success Metrics
- **Uptime:** >99% (monitored via health checks)
- **Response Time:** <100ms (HTTP server)
- **Data Freshness:** Weekly updates (Monday 9:00 AM)
- **Error Rate:** <1% of operations

---

## Appendix

### A. Quick Reference Commands

```bash
# Start all services
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
python3 -m http.server 8080 &
./scripts/start_tunnel.sh &

# Stop all services
pkill -f "python3.*8080"
pkill cloudflared

# Check status
./scripts/health_monitor.sh

# Run weekly automation manually
./scripts/weekly_automation_enhanced.sh

# View logs
tail -f logs/cron.log
tail -f logs/health_monitor.log
```

### B. File Locations
- **Configuration:** `.env` (secure credentials)
- **Database:** `data/patents.db`
- **Logs:** `logs/` directory
- **Scripts:** `scripts/` directory
- **Reports:** `reports/` directory
- **Documentation:** `docs/` directory

### C. Dependencies
- **Python 3:** scripts and API client
- **SQLite3:** database
- **curl:** HTTP testing
- **cloudflared:** tunnel service
- **cron:** scheduling

---

**Maintenance Schedule Summary:**
- **Daily:** Health monitoring (automated)
- **Weekly:** Patent collection (Monday 9:00 AM)
- **Monthly:** Archive, backup, log rotation
- **Quarterly:** Technology review, performance check

**System Owner:** Heartbeat Agent (auto-maintenance)  
**Last Verified:** April 5, 2026 - 02:35 UTC  
**Next Review:** July 5, 2026