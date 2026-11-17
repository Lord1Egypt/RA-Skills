---
type: Reference
title: "Camofox Default Browser — Troubleshooting Guide"
timestamp: 2026-07-30T13:06:00+07:00
version: 1.0.0
---

# Camofox Default Browser — Troubleshooting Guide

## Table of Contents

- [Common Issues](#common-issues)
- [Performance Issues](#performance-issues)
- [Platform-Specific Issues](#platform-specific-issues)
- [Debug Mode](#debug-mode)
- [Getting Help](#getting-help)

---

## Common Issues

### 1. "Camoufox binary not found"

**Problem:** Tool calls return errors about the Camoufox executable being missing.

**Cause:** The binary isn't installed, or `CAMOUFOX_EXECUTABLE` env var points to wrong path.

**Solution:**

Verify the expected location:

```bash
ls -la /root/.cache/camoufox/camoufox
```

If missing, reinstall via npm (the camoufox package handles this):

```bash
npm install -g @jo-inc/camofox
```

Set the correct path if it's elsewhere:

```bash
export CAMOUFOX_EXECUTABLE=/path/to/camoufox
```

Restart the OpenClaw Gateway after changing env vars:

```bash
openclaw gateway restart
```

---

### 2. "Port 9377 already in use"

**Problem:** Server refuses to start because port 9377 is occupied.

**Cause:** A previous Camoufox server instance didn't shut down cleanly, or another process bound the port.

**Solution:**

Find and kill the offending process:

```bash
lsof -i :9377
# or
ss -tlnp | grep 9377
```

Then kill it:

```bash
kill -9 <PID>
```

If nothing shows up but the port is still blocked, check for zombie processes:

```bash
ps aux | grep -i camo
```

Clean any stale socket files that may linger:

```bash
rm -f /tmp/camofox-server.sock
```

Restart the server:

```bash
openclaw gateway restart
```

---

### 3. "Browser crashes on startup"

**Problem:** Tabs fail to create; snapshot returns empty or errors.

**Cause:** Missing system libraries, insufficient display environment, or corrupted cache.

**Solution:**

Install required dependencies on Linux:

```bash
apt-get update && apt-get install -y \
  libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 \
  libxt6 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libatk-bridge2.0-0 libdrm2 libgbm1 xvfb
```

If running headless (no display), use Xvfb:

```bash
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
```

Clear corrupted browser cache:

```bash
rm -rf /root/.cache/camoufox/cache-*
```

Check crash logs for specifics:

```bash
cat ~/.local/share/camofox/logs/crash.log
```

---

### 4. "Cookie import fails"

**Problem:** `camofox_import_cookies` returns an error or cookies don't load.

**Cause:** Netscape format violation, permission denied, or expired session tokens.

**Solution:**

Validate cookie file format — each line must follow:

```
.domain   .flag   .path   .secure   .expiration   .name   .value
```

Example valid entry:

```
.youtube.com    TRUE    /    TRUE    1735689600    SID    abc123def456
```

Check file permissions:

```bash
chmod 644 cookies.txt
ls -la cookies.txt
```

Ensure the cookie file exists and is readable:

```bash
head -n 5 cookies.txt
wc -l cookies.txt
```

If importing from a site like LinkedIn where sessions expire quickly, refresh the cookies first. Imported cookies are bearer tokens — expired ones won't authenticate.

Use `domainSuffix` filter for selective import:

```bash
# Only import cookies for a specific domain
camofox_import_cookies(cookiesPath="/path/cookies.txt", domainSuffix=".linkedin.com")
```

---

### 5. "Tabs not closing"

**Problem:** Old tabs accumulate; memory grows; `camofox_close_tab` appears ineffective.

**Cause:** Session state drift between client and server, or tab references become stale after navigation errors.

**Solution:**

Always verify tab state before and after closing:

```bash
# List active tabs first
camofox_list_tabs()
```

Close by tabId explicitly:

```bash
camofox_close_tab(tabId="t1")
```

Force cleanup by restarting the server if orphaned tabs persist:

```bash
openclaw gateway restart
```

Implement proper lifecycle in your automation flows:

```
create_tab → work → close_tab → verify list
```

Don't rely on auto-shutdown alone — always call `close_tab` explicitly after tasks complete.

---

## Performance Issues

### High Memory Usage

**Symptoms:** System slowdown, browser becomes unresponsive, OOM kills occur.

**Causes:** Too many open tabs, large page resources, no idle timeout tuning.

**Solutions:**

Reduce the idle timeout if tabs aren't needed long:

```bash
# Set shorter idle period (e.g., 2 minutes instead of 5)
export CAMOUFOX_IDLE_TIMEOUT_MS=120000
```

Close tabs you're done with immediately — don't leave them sitting.

Limit concurrent snapshots: avoid calling `snapshot` more than once per tab while actively automating. Each snapshot captures the full accessibility tree which has overhead.

Monitor memory usage:

```bash
# Check Camoufox-related processes
ps aux --sort=-%mem | head -20 | grep -E 'camo|firefox'
free -m
```

If running multiple automation sessions, stagger their start times to avoid simultaneous browser launches.

---

### Slow Tab Creation

**Symptoms:** `camofox_create_tab` takes several seconds or hangs.

**Causes:** Cold browser launch, network latency to CDN, limited CPU during spawn.

**Solutions:**

Keep at least one tab alive when running batch operations — reuse existing tabs instead of creating new ones repeatedly. The browser engine only launches lazily on first request.

Pre-warm the browser before heavy workloads:

```bash
# Create a disposable warm-up tab
# Then close it — subsequent creates will be much faster
```

Check disk I/O — cache downloads during cold start go to disk:

```bash
iotop -o -b -n 3
```

If on a constrained VPS, ensure swap isn't being thrashed:

```bash
swapon --show
dmesg | grep -i oom
```

---

### Connection Timeouts

**Symptoms:** `camofox_navigate`, `snapshot`, or `act` commands hang and eventually timeout.

**Causes:** Network issues, firewall blocking port 9377, or target website slowness.

**Solutions:**

Test connectivity to the Camoufox server:

```bash
curl http://localhost:9377/health
# Expected: {"status":"ok"}
```

Check for proxy settings interfering:

```bash
env | grep -i proxy
```

Disable proxies if present and not needed:

```bash
unset HTTP_PROXY
unset HTTPS_PROXY
unset NO_PROXY
```

If the target site itself is slow (e.g., loading heavy JavaScript), wait for page load before interacting:

```bash
# After navigate, take a quick snapshot to confirm rendering
camofox_snapshot(tabId="t1")
```

---

## Platform-Specific Issues

### Linux: Missing Libraries

When installing on fresh Debian/Ubuntu systems:

```bash
# Full dependency set for headless Camoufox
apt-get install -y \
  libgtk-3-0 libgdk-pixbuf2.0-0 libdbus-glib-1-2 \
  libxt6 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
  libatk-bridge2.0-0 libdrm2 libgbm1 xvfb \
  fonts-liberation fonts-dejavu-core curl wget
```

For display-less servers, always use Xvfb:

```bash
Xvfb :99 -ac -screen 0 1920x1080x24 &
export DISPLAY=:99
```

To make Xvfb persistent across reboots, add to `/etc/rc.local`:

```bash
/usr/bin/Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
```

### Docker: Volume Mounts and Networking

When running inside Docker, the host machine needs access to the Camoufox server API.

Ensure the container exposes the API port:

```yaml
services:
  app:
    ports:
      - "9377:9377"
    environment:
      - CAMOUFOX_EXECUTABLE=/usr/local/bin/camoufox
```

If using Docker Compose with separate Camoufox service, mount shared cache:

```yaml
volumes:
  - ./data/camofox-cache:/root/.cache/camoufox
```

In Docker networks, `localhost` refers to the container itself. Use the service name as hostname instead:

```python
# Wrong — localhost inside the container
# Right — use compose service name
base_url = "http://camofox-server:9377"
```

### ARM64: Compatibility Notes

Camoufox requires x86_64 binaries. On ARM64 machines (Apple Silicon Macs, ARM cloud instances):

- **Native support not available.** The pre-built binary targets x86_64 Linux only.
- Workarounds:
  1. Run under QEMU emulation (slow but functional):
     ```bash
     docker run --platform linux/amd64 -p 9377:9377 jo/inc/camofox-server
     ```
  2. Use the standard `browser` tool (Playwright/Chromium) on ARM64 hardware instead.
  3. Deploy to an x86_64 machine for production workloads.

---

## Debug Mode

### Enable Verbose Logging

Set environment variable before starting the Gateway:

```bash
export CAMOUFOX_LOG_LEVEL=verbose
openclaw gateway restart
```

Log levels (lowest to highest verbosity):

| Level | Output |
|-------|--------|
| `error` | Crashes and failures only |
| `warn` | Warnings + errors |
| `info` | Standard operation + warnings |
| `debug` | Detailed step-by-step logging |
| `verbose` | Full request/response traces |

### Check Server Logs

Primary log locations:

```bash
# Gateway-integrated logs
journalctl -u openclaw-gateway --since "1 hour ago"

# Direct Camoufox server logs
~/.openclaw/workspace/log/camofox*.log

# Crash dumps (if enabled)
~/.local/share/camofox/logs/crash.log
```

Search for specific errors:

```bash
grep -i "error\|fail\|crash" ~/.openclaw/workspace/log/camofox*.log
```

### Health Endpoint Usage

The health endpoint helps diagnose server status remotely:

```bash
curl -s http://localhost:9377/health | python3 -m json.tool
```

Expected healthy response:

```json
{"status": "ok", "browser": "idle", "tabs": 0}
```

Response variations indicate status:

| Response | Meaning |
|----------|---------|
| `{"status":"ok","browser":"idle"}` | Running, browser ready |
| `{"status":"ok","browser":"active","tabs":3}` | Running, 3 tabs open |
| `{"status":"degraded","reason":"high_memory"}` | Running but strained |
| Connection refused | Server not running — check if Gateway is up |

---

## Getting Help

### GitHub Issues

Report bugs or request features:

- **Repository:** https://github.com/jo-inc/camofox-browser/issues
- Include: version info, logs, reproduction steps, platform details.

### Log File Locations

| Purpose | Path |
|---------|------|
| General logs | `~/.openclaw/workspace/log/camofox*.log` |
| Crash dumps | `~/.local/share/camofox/logs/crash.log` |
| Cache data | `/root/.cache/camoufox/` |
| Socket file | `/tmp/camofox-server.sock` |

### Diagnostic Commands

Run these before reporting issues — they provide the essentials:

```bash
# 1. Verify binary
ls -la "$CAMOUFOX_EXECUTABLE"

# 2. Check server health
curl -s http://localhost:9377/health

# 3. List running browser processes
ps aux | grep -iE 'camo|firefox.*headless'

# 4. Check disk space for cache
du -sh /root/.cache/camoufox/
df -h

# 5. Check memory
free -m
```

Share the output of all five commands along with your issue report for fastest triage.
