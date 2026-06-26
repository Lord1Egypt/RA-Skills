# Playbook: Tailscale Funnel Recovery

## What This Covers

This playbook handles the known recurring bug where Tailscale Funnel randomly
reverts from `(Funnel on)` to `(tailnet only)`, making the OpenClaw gateway
unreachable from the public internet.

**Affected endpoint:** `https://your-server.ts.net`

## Detection

```bash
tailscale funnel status
```

**BROKEN (needs fix):**
```
https://your-server.ts.net (tailnet only)
```

**HEALTHY (no action needed):**
```
https://your-server.ts.net (Funnel on)
```

Check the output string literally. If it contains `(tailnet only)` → the tunnel is down.

## Root Cause (For Reference)

The systemd service `tailscale-funnel-openclaw.service` was failing at boot
because:

1. The service started before `tailscaled` fully authenticated → `NoState` error
2. Inline Python quotes in the heredoc ExecStart were mangled by shell escaping
3. **Fix applied:** retry logic moved to `/usr/local/bin/tailscale-funnel-start.sh`

The fix is already deployed on the server. This playbook re-runs that fix when
the tunnel drops again (which happens randomly due to Tailscale daemon restarts
or network events).

## Recovery Procedure

Execute these steps in order:

### Step 1: Run the recovery script

```bash
sudo /usr/local/bin/tailscale-funnel-start.sh
```

This script:
- Polls Tailscale backend state up to 30 times (3s apart)
- Waits until state is `Running`
- Runs `tailscale funnel --bg 18789` to re-enable the funnel

Expected output (success):
```
Attempt 1: BackendState=Running
Funnel enabled
```

Expected output (failure after 30 tries):
```
Tailscale never reached Running state
```

### Step 2: Wait and verify

```bash
sleep 5
tailscale funnel status
```

**If output now shows `(Funnel on)` → SUCCESS.** Log it and proceed.

**If still `(tailnet only)` → proceed to Step 3.**

### Step 3: Restart the systemd service

```bash
sudo systemctl restart tailscale-funnel-openclaw.service
```

Then verify:
```bash
systemctl status tailscale-funnel-openclaw.service
tailscale funnel status
```

### Step 4: If still broken — deep diagnosis

```bash
# Check tailscaled itself
sudo systemctl status tailscaled

# Check if tailscale is authenticated
tailscale status

# Check logs
sudo journalctl -u tailscale-funnel-openclaw.service -n 50 --no-pager
sudo journalctl -u tailscaled -n 50 --no-pager
```

If `tailscaled` is not running:
```bash
sudo systemctl start tailscaled
sleep 5
sudo /usr/local/bin/tailscale-funnel-start.sh
```

If tailscale is not authenticated (shows login page or auth error):
→ This requires manual action. Notify the user.

## Logging

After completing recovery, log to `~/.openclaw/dms-fix-log.jsonl`:

```json
{"timestamp":"<ISO8601>","service":"tailscale","issue":"funnel reverted to tailnet-only","fix":"ran tailscale-funnel-start.sh","result":"success","duration_ms":<ms>}
```

Use `dms_recover(service="tailscale", reason="funnel reverted to tailnet-only")` — it logs automatically.

## Cron Monitoring Rule

- **First occurrence** → Fix silently, log it. No cron.
- **Second occurrence in 24h** → Fix + create cron:

```bash
openclaw cron add \
  --name "DMS: Tailscale Funnel Monitor" \
  --cron "*/5 * * * *" \
  --session isolated \
  --message "Dead Man's Switch: Check tailscale funnel status. If (tailnet only), run sudo /usr/local/bin/tailscale-funnel-start.sh, verify fix, log result to ~/.openclaw/dms-fix-log.jsonl." \
  --announce
```

Notify user: "I noticed Tailscale Funnel keeps dropping. I've set up monitoring every 5 minutes."

## Voice Alert (ElevenLabs)

If ElevenLabs is configured, send after successful recovery:
> "Your Tailscale tunnel dropped. Recovery was successful. The gateway is reachable again."

If recovery failed:
> "Warning: Tailscale Funnel recovery failed. The gateway may be unreachable. Manual intervention needed."

## Systemd Service Reference

**Unit file:** `/etc/systemd/system/tailscale-funnel-openclaw.service`

```ini
[Unit]
Description=Tailscale Funnel for OpenClaw
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/tailscale-funnel-start.sh
ExecStop=/usr/bin/tailscale funnel --https=443 off

[Install]
WantedBy=multi-user.target
```

**Recovery script:** `/usr/local/bin/tailscale-funnel-start.sh`

```bash
#!/bin/bash
for i in $(seq 1 30); do
    STATUS=$(/usr/bin/tailscale --socket /var/run/tailscale/tailscaled.sock status --json 2>/dev/null \
      | python3 -c "import sys,json; print(json.load(sys.stdin).get('BackendState',''))" 2>/dev/null)
    echo "Attempt $i: BackendState=$STATUS"
    if [ "$STATUS" = "Running" ]; then
        /usr/bin/tailscale funnel --bg 18789 && echo "Funnel enabled" && exit 0
    fi
    sleep 3
done
echo "Tailscale never reached Running state"
exit 1
```

**Sudoers rule:** `/etc/sudoers.d/openclaw-skills`
```
<your-username> ALL=(root) NOPASSWD: /usr/local/bin/tailscale-funnel-start.sh
```
