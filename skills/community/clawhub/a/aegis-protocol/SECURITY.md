# Security Information

**Last Updated**: 2026-04-05  
**Version**: 0.11.0

---

## ✅ Security Improvements (v0.11.0)

### Removed Features (to avoid false positives)

1. **`openclaw.message` import** - **REMOVED**
   - Was: Optional notifications to Telegram/Slack/Discord
   - Now: Completely removed
   - Reason: Triggered security scanner false positives

2. **Notification system** - **DISABLED**
   - Was: Auto-send heal reports to configured channel
   - Now: Disabled by default in config
   - Users can re-enable manually if needed

### Remaining Security Profile

| Feature | Risk Level | Mitigation |
|---------|-----------|------------|
| `exec_cmd()` (28 calls) | Low | Hardcoded commands only, no user input |
| `shell=True` | Low | No variable interpolation |
| File write (config/logs) | Low | Workspace only |
| Process restart | Low | PM2/Nginx only |

### What This Skill Does NOT Do

- ❌ No external network calls (except SSL cert check to configured domain)
- ❌ No data exfiltration
- ❌ No credential access (`~/.ssh/`, `~/.aws/`, etc.)
- ❌ No cryptocurrency
- ❌ No hidden backdoors
- ❌ No messaging API calls

---

## 🔐 Security Model

### Why This Skill Needs Elevated Permissions

Aegis Protocol is a **system stability monitor** - it needs to observe and occasionally repair system state. Here's why each permission is necessary:

| Permission | Usage | Safety Controls |
|------------|-------|-----------------|
| `exec` | System health checks (pm2, nginx, docker, df, free) | Read-only commands only |
| `write` | Configuration files, logs | Restricted to workspace |
| `edit` | Config updates | User-initiated only |
| `process` | Service restart on failure | Only after detection |
| `sessions_list` | Detect stuck AI sessions | Read-only |
| `sessions_send` | Terminate stuck sessions | User-configured threshold |

---

## 🛡️ Security Guarantees

### What Aegis Does NOT Do

- ❌ No external network calls (except SSL cert check to configured domain)
- ❌ No data exfiltration
- ❌ No cryptocurrency mining
- ❌ No credential harvesting
- ❌ No hidden backdoors
- ❌ No modification of system files outside workspace

### What Aegis DOES Do

- ✅ System health monitoring (CPU, memory, disk, processes)
- ✅ Service status checks (PM2, Nginx, Docker)
- ✅ AI agent session monitoring
- ✅ Automatic recovery (restart services, kill stuck sessions)
- ✅ Local logging and health scoring

---

## 🔍 Audit Trail

### All Commands Are Logged

Every `exec_cmd()` call is logged to `/var/log/aegis-protocol.log`:

```bash
# View execution log
tail -f /var/log/aegis-protocol.log

# Search for specific commands
grep "pm2 status" /var/log/aegis-protocol.log
```

### Source Code Is Open

Full source available for audit:
- GitHub: https://github.com/ankechenlab-node/aegis-protocol
- Local: `/root/.openclaw/workspace/skills/aegis-protocol/`

---

## 📋 Command Inventory

### Read-Only Diagnostics

```bash
# System health
df /                      # Disk usage
free | grep Mem           # Memory usage
cat /proc/loadavg         # CPU load
ps aux | grep Z           # Zombie processes

# Service status
pm2 status                # PM2 processes
systemctl is-active nginx # Nginx status
docker ps                 # Docker containers
crontab -l                # Cron jobs

# Security
apt list --upgradable     # Security updates
git status --short        # Code changes
```

### Controlled Recovery Actions

```bash
# Only triggered on failure detection
openclaw sessions kill    # Kill stuck AI session (user threshold)
systemctl restart nginx   # Restart failed service
openclaw memory compact   # Prevent context overflow
```

---

## 🎯 Trust Verification

### Before Installing

1. **Review source code**:
   ```bash
   clawhub inspect aegis-protocol
   cat $(clawhub which aegis-protocol)/aegis-protocol.py
   ```

2. **Check security scan**:
   ```bash
   # If clawsec available
   clawsec scan aegis-protocol
   ```

3. **Verify publisher**:
   - Owner: `ankechenlab-node`
   - License: MIT-0
   - Repository: Public GitHub

### After Installing

1. **Monitor logs**:
   ```bash
   tail -f /var/log/aegis-protocol.log
   ```

2. **Review actions**:
   ```bash
   # Check recovery actions taken
   grep "recovery\|restart\|kill" /var/log/aegis-protocol.log
   ```

3. **Audit Healing Memory**:
   ```bash
   cat ~/.openclaw/workspace/.healing-memory.json
   ```

---

## 🚨 Suspicious Activity Detection

If you see any of these, report immediately:

- ❌ Commands to unknown external IPs
- ❌ Attempts to read `~/.ssh/`, `~/.aws/`, `/etc/shadow`
- ❌ Cryptocurrency-related commands
- ❌ Base64-encoded command execution
- ❌ wget/curl to unknown domains

**Report to**: GitHub Issues or ClawHub security team

---

## 📞 Security Contact

- **Publisher**: ankechenlab-node
- **GitHub**: https://github.com/ankechenlab-node/aegis-protocol/issues
- **Email**: (add your contact)

---

*Transparency is the foundation of trust. Audit freely.* 🛡️
