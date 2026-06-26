# Playbook: Disk Space Recovery

## What This Covers

Detection and recovery for disk space exhaustion on the server. Acts when any
filesystem is at 85% or higher utilization.

## Detection

```bash
# Check root filesystem
df -h /

# Check all major filesystems
df -h / /var /tmp /home 2>/dev/null

# Find largest directories
du -sh /var/log/* 2>/dev/null | sort -rh | head -20
du -sh /tmp/* 2>/dev/null | sort -rh | head -10
```

**Threshold:** Alert and act when `Use%` is ≥ 85%.

**Critical threshold:** At 95%+ many services will fail. Act immediately.

## Safe Cleanup Targets (In Priority Order)

### 1. Package Manager Cache (safest)

```bash
# Apt cache (Ubuntu/Debian)
sudo apt-get clean
sudo apt-get autoclean

# Check size recovered
df -h /
```

Typically recovers 500MB–2GB. Always safe.

### 2. Old Log Files

```bash
# Rotate and vacuum systemd journal (keep last 7 days)
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=500M

# Check /var/log size
du -sh /var/log/

# Truncate large nginx logs (NOT delete — just truncate)
sudo find /var/log/nginx/ -name "*.log" -size +100M -exec truncate -s 50M {} \;

# Remove compressed/rotated logs older than 30 days
sudo find /var/log -name "*.gz" -mtime +30 -delete
sudo find /var/log -name "*.1" -mtime +30 -delete
```

### 3. Temp Files

```bash
# Clear /tmp (only files older than 24h to be safe)
sudo find /tmp -type f -atime +1 -delete 2>/dev/null || true

# Clear stale apt lists
sudo rm -rf /var/lib/apt/lists/*
sudo apt-get update  # Regenerates them
```

### 4. Docker Artifacts (if Docker is installed)

```bash
# Check if Docker is present
which docker 2>/dev/null

# Remove unused images, containers, volumes
sudo docker system prune -f 2>/dev/null || true

# More aggressive: also remove unused images
sudo docker image prune -af 2>/dev/null || true
```

### 5. Old Kernels (Ubuntu)

```bash
# List installed kernels
dpkg -l 'linux-image-*' | grep '^ii'

# Remove old kernels (keeps current + 1 previous)
sudo apt-get autoremove --purge -y
```

### 6. Application Logs

Check application-specific log directories:

```bash
# Find large files under /var/www, /opt, /home
sudo find /var/www -name "*.log" -size +50M 2>/dev/null | head -10
sudo find /opt -name "*.log" -size +50M 2>/dev/null | head -10
sudo find /home -name "*.log" -size +50M 2>/dev/null | head -10
```

Report large log files to the user but do NOT delete application logs
without confirmation — they may be needed for debugging.

## Recovery Sequence

Run in this order, checking disk usage after each step:

```bash
# Step 1: Check current usage
df -h /

# Step 2: Apt cache cleanup
sudo apt-get clean && sudo apt-get autoclean

# Step 3: Journal vacuum
sudo journalctl --vacuum-time=7d --vacuum-size=500M

# Step 4: Old rotated logs
sudo find /var/log -name "*.gz" -mtime +30 -delete 2>/dev/null || true

# Step 5: Temp files
sudo find /tmp -type f -atime +1 -delete 2>/dev/null || true

# Step 6: Docker (if present)
which docker && sudo docker system prune -f 2>/dev/null || true

# Step 7: Check final usage
df -h /
```

Use `dms_recover(service="disk", reason="disk at X% on /")` which runs the
full cleanup script automatically.

## What NOT to Delete

- Application code directories (e.g., `/var/www`, `/opt/<app>`)
- Database files (`/var/lib/postgresql`, `/var/lib/mysql`, etc.)
- Active configuration files (`/etc`)
- SSH keys (`~/.ssh`)
- The fix log itself (`~/.openclaw/dms-fix-log.jsonl`)

## Logging

After recovery, log to `~/.openclaw/dms-fix-log.jsonl`:

```json
{"timestamp":"<ISO8601>","service":"disk","issue":"disk at 91% on /","fix":"cleared apt cache, journal logs, rotated logs — freed 2.3GB","result":"success","duration_ms":<ms>}
```

Include the amount freed in the `fix` field when possible.

## Cron Monitoring Rule

- First disk alert at ≥85% → Clean, log, no cron.
- Second alert within 24h OR alert at ≥92% → Clean + create cron:

```bash
openclaw cron add \
  --name "DMS: Disk Space Monitor" \
  --cron "0 * * * *" \
  --session isolated \
  --message "Dead Man's Switch: Check disk usage on /. If above 85%, run disk cleanup playbook. Report current usage." \
  --announce
```

Note: Disk monitoring uses hourly (`0 * * * *`) rather than every 5 minutes.

## Voice Alert (ElevenLabs)

On successful cleanup:
> "Warning: disk space was at [X]%. I cleared old logs and cache. You have [Y] gigabytes free now."

If disk is critically full (≥95%) and cleanup was insufficient:
> "Critical: disk space is at [X]% and I was unable to free enough space automatically. Manual intervention required."
