# Playbook: Nginx + Website Monitoring

## What This Covers

Detection and recovery for nginx failures, website outages, and upstream application
crashes on the configured websites (e.g., `your-site.com`, `your-other-site.com`).

## CRITICAL: Check Tailscale First

Before diagnosing nginx, **always verify that Tailscale Funnel is healthy.**

If Tailscale shows `(tailnet only)`, the external requests cannot reach the server
at all — nginx will appear to return timeouts or 502s, but the real problem is
the tunnel. Fix Tailscale first (see `tailscale.md`), then re-check websites.

## Detection

Check each configured website:

```bash
curl -sI --max-time 10 https://your-site.com
curl -sI --max-time 10 https://your-other-site.com
```

Also check nginx directly:
```bash
sudo systemctl status nginx
sudo nginx -t
```

## Response by Status Code

### HTTP 200 — Healthy

No action needed. Log as OK.

### HTTP 502 Bad Gateway — Upstream Application Dead

The upstream application that nginx proxies to has crashed or is not listening.

```bash
# Check nginx error log for upstream info
sudo tail -50 /var/log/nginx/error.log

# Find which upstream app is configured
grep -r "proxy_pass" /etc/nginx/sites-enabled/

# Check if the upstream process is running
sudo systemctl status <app-name>

# Restart the upstream process
sudo systemctl restart <app-name>

# Wait and verify
sleep 10
curl -sI --max-time 10 https://<site>
```

Use `dms_recover(service="process", reason="upstream app dead — nginx returning 502", processName="<app-name>")`.

### HTTP 503 Service Unavailable — Nginx Overloaded or in Maintenance

```bash
# Check nginx status
sudo systemctl status nginx

# Check config validity FIRST
sudo nginx -t

# If config is valid, reload (zero-downtime)
sudo nginx -s reload

# If nginx is dead, restart
sudo systemctl restart nginx
```

**NEVER reload nginx without running `nginx -t` first.** A broken config will
take down all sites permanently until manually fixed.

### HTTP 504 Gateway Timeout — Upstream Too Slow

```bash
# Check if Tailscale is the bottleneck
tailscale funnel status

# Check upstream app responsiveness
curl -sI --max-time 30 http://localhost:<upstream-port>/

# Check nginx upstream timeout settings
grep -r "proxy_read_timeout\|proxy_connect_timeout" /etc/nginx/

# Check system resources
top -bn1 | head -20
free -h
```

If the upstream app is responding slowly, check its logs and consider restarting it.

### Timeout (No Response) — Nginx or Tunnel Down

If `curl` times out with no response:

1. **Check Tailscale first:**
   ```bash
   tailscale funnel status
   ```
   If `(tailnet only)` → fix Tailscale (see `tailscale.md`), then re-check.

2. **Check nginx process:**
   ```bash
   sudo systemctl status nginx
   ```
   If dead:
   ```bash
   sudo nginx -t
   # Only restart if config is valid
   sudo systemctl restart nginx
   ```

3. **Check nginx error logs:**
   ```bash
   sudo tail -50 /var/log/nginx/error.log
   sudo tail -50 /var/log/nginx/access.log
   ```

### HTTP 404 Not Found — Wrong nginx Config

```bash
# List active sites
ls /etc/nginx/sites-enabled/

# Check the relevant site config
cat /etc/nginx/sites-enabled/<site>

# Check nginx error log
sudo tail -20 /var/log/nginx/error.log

# Validate config (do not reload if broken)
sudo nginx -t
```

If the config is missing the correct `root` path or `server_name`, the fix
requires editing the nginx config manually. Notify the user with the details.

## General Nginx Recovery Commands

```bash
# Test config validity (ALWAYS before any reload)
sudo nginx -t

# Reload config (zero-downtime, only if nginx -t passes)
sudo nginx -s reload

# Full restart
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx

# List active sites
ls /etc/nginx/sites-enabled/

# Check error log
sudo tail -50 /var/log/nginx/error.log

# Check access log
sudo tail -50 /var/log/nginx/access.log
```

## Script: nginx-check.sh

The privileged script checks a given URL and dumps diagnostic info if it's not 200:

```bash
sudo /usr/local/bin/openclaw-skills/nginx-check.sh https://your-site.com
```

Or use the tool:
```
dms_recover(service="nginx", reason="502 on your-site.com")
```

## Logging

After recovery, log to `~/.openclaw/dms-fix-log.jsonl`:

```json
{"timestamp":"<ISO8601>","service":"nginx","issue":"502 on your-site.com","fix":"restarted upstream process","result":"success","duration_ms":<ms>}
```

## Cron Monitoring Rule

- First website failure → Fix, log, no cron.
- Two or more failures in 24h → Fix + create cron:

```bash
openclaw cron add \
  --name "DMS: Nginx Monitor" \
  --cron "*/5 * * * *" \
  --session isolated \
  --message "Dead Man's Switch: Check configured websites. Check Tailscale first. If any site returns non-200, diagnose and fix using nginx playbook." \
  --announce
```

## Voice Alert (ElevenLabs)

On successful recovery:
> "Nginx returned a 502 on [site]. I restarted the upstream process. The site is back online."

On failure:
> "Warning: [site] is still down after attempting recovery. Manual investigation needed."
