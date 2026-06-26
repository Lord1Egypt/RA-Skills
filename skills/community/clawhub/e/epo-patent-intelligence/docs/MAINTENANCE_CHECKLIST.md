# System Maintenance Checklist
**Last Updated:** April 4, 2026 - 19:56 UTC

## Daily Checks (Automated via Heartbeat)

### Process Health
- [ ] HTTP Server (port 8080) - `ss -tlnp | grep 8080`
- [ ] Cloudflare Tunnel - `ps aux | grep cloudflared`
- [ ] Database Integrity - `sqlite3 data/patents.db "PRAGMA integrity_check;"`

### Dashboard Accessibility
- [ ] KW14: https://hermes.sqncr.ai/Patent_report_kw14
- [ ] KW15: https://hermes.sqncr.ai/Patent_report_kw15

### Database Health
- [ ] Patent count matches expected (48 real patents)
- [ ] No corruption in `data/patents.db`
- [ ] Indexes present (`idx_patent_id`, `idx_company`, etc.)

## Weekly Rotation Tasks (Every Monday)

### Pre-Rotation
- [ ] Verify KW16 directory exists
- [ ] Check `restart_tunnel_kw16.sh` is executable
- [ ] Backup current database

### Execute Rotation
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
bash scripts/rotate_weekly.sh 17  # Week number
```

### Post-Rotation
- [ ] Update `WEEKLY_ROTATION_GUIDE.md`
- [ ] Verify new dashboard accessible
- [ ] Test database integrity

## Monthly Tasks

### Data Management
- [ ] Purge old sample data (keep only real EPO patents)
- [ ] Vacuum database for optimization
- [ ] Review and update company tracking list

### Documentation
- [ ] Update system architecture docs
- [ ] Review and update credentials (EPO API key)
- [ ] Check skill version and dependencies

## Troubleshooting

### Server Down
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
python3 scripts/report_server.py &
```

### Tunnel Down
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
bash scripts/restart_tunnel.sh
```

### Database Corruption
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
sqlite3 data/patents.db "PRAGMA integrity_check;"
# If corrupted: restore from backup
```

## Health Check Script

Run comprehensive check:
```bash
cd /root/.openclaw/workspace/skills/epo-patent-intelligence
python3 -c "
import sqlite3
import os
db = 'data/patents.db'
conn = sqlite3.connect(db)
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM patents')
print(f'Patents: {cursor.fetchone()[0]}')
cursor.execute('PRAGMA integrity_check')
print(f'Integrity: {cursor.fetchone()[0]}')
conn.close()
"
```

---
**Skill:** epo-patent-intelligence
**Version:** 1.0.0
**Database:** 48 patents (real EPO data)
