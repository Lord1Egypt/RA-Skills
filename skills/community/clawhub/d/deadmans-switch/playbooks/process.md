# Playbook: Generic Crashed Process Recovery

## What This Covers

Detection and recovery for any named systemd service that has crashed or is
not running. Used when a specific application process needs to be restarted.

## Detection

### Check if a specific service is running

```bash
sudo systemctl status <service-name>

# Look for:
# - "Active: active (running)" → healthy
# - "Active: failed" → crashed, needs restart
# - "Active: inactive (dead)" → stopped
# - "Active: activating" → starting up
```

### Find what's failing

```bash
# Recent logs for the service
sudo journalctl -u <service-name> -n 50 --no-pager

# Exit code of last run
sudo systemctl show <service-name> --property=ExecMainStatus
```

### List all failed services

```bash
sudo systemctl --failed --no-pager
```

### Check process by name (if not a systemd service)

```bash
pgrep -a <process-name>
ps aux | grep <process-name>
```

## Recovery Procedure

### Standard Systemd Service Restart

```bash
# Step 1: Check current status
sudo systemctl status <service-name>

# Step 2: Attempt restart
sudo systemctl restart <service-name>

# Step 3: Wait for service to start
sleep 5

# Step 4: Verify
sudo systemctl status <service-name>
```

If the service fails to start after restart, check the logs:

```bash
sudo journalctl -u <service-name> -n 100 --no-pager
```

### Service is in Failed State — Reset Before Restart

```bash
# Reset failed state first
sudo systemctl reset-failed <service-name>

# Then restart
sudo systemctl restart <service-name>

# Verify
sleep 5
sudo systemctl status <service-name>
```

### Service Crashes Repeatedly

If a service has crashed multiple times, check for:

```bash
# Check restart count
sudo systemctl show <service-name> --property=NRestarts

# Check if systemd is rate-limiting restarts
sudo journalctl -u <service-name> -n 20 --no-pager | grep -i "start-limit\|too many restarts"

# If rate-limited, reset and restart
sudo systemctl reset-failed <service-name>
sudo systemctl start <service-name>
```

### Non-Systemd Process Recovery

If the process is not managed by systemd:

```bash
# Find and kill zombie/stuck process
pkill -f <process-name>

# Wait and check
sleep 2
pgrep -a <process-name>

# If there's a start script
<path-to-start-script> &
```

Report to user if a non-systemd process keeps crashing — it should be converted
to a systemd service for proper lifecycle management.

## Using the Recovery Script

```bash
sudo /usr/local/bin/openclaw-skills/process-restart.sh <service-name>
```

Or use the tool:
```
dms_recover(service="process", reason="<app> crashed", processName="<service-name>")
```

## Common Services on This Server

When diagnosing website issues (502 etc.), the upstream application is likely
one of:
- A Node.js app managed by PM2 or systemd
- A Python/Gunicorn app
- A custom service under `/etc/systemd/system/`

To discover what's serving a particular domain:
```bash
# Find the proxy_pass target in nginx config
grep -r "proxy_pass" /etc/nginx/sites-enabled/

# Then check what's listening on that port
sudo ss -tlnp | grep <port>

# Match PID to service
sudo systemctl status $(sudo systemctl list-units --type=service | grep <port>)
```

## Logging

After recovery, log to `~/.openclaw/dms-fix-log.jsonl`:

```json
{"timestamp":"<ISO8601>","service":"process","issue":"<service-name> was in failed state","fix":"systemctl restart <service-name>","result":"success","duration_ms":<ms>}
```

## Cron Monitoring Rule

- First crash → Restart, log, no cron.
- Second crash in 24h → Restart + create cron:

```bash
openclaw cron add \
  --name "DMS: <service-name> Monitor" \
  --cron "*/5 * * * *" \
  --session isolated \
  --message "Dead Man's Switch: check if <service-name> systemd service is running. If not, restart it and log the result." \
  --announce
```

## Voice Alert (ElevenLabs)

On successful recovery:
> "The [service name] process had crashed. I restarted it. The service is back online."

On failure:
> "Warning: [service name] failed to start after restart attempt. The error log shows: [brief error]. Manual investigation needed."

## When to Escalate to User

Do not attempt automated recovery and instead notify the user when:

1. The service has crashed 5+ times in the past hour (likely a code bug)
2. The service fails to start after 2 restart attempts
3. The service requires manual configuration or credentials to start
4. The error log contains "out of memory" or OOM killer entries
5. The error is a database connection failure (the database may be the real issue)
