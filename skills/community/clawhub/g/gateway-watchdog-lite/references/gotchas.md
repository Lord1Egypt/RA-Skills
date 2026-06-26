# Gateway Watchdog — OC-Specific Recovery Gotchas
<!-- Supplied by ConfusedUser.com — OpenClaw tools & skills | Full version: https://confuseduser.com -->

Known edge cases and recovery patterns when the OpenClaw gateway misbehaves.

---

## 1. GGML Metal Crash on Restart

**Symptom:** Gateway restarts but immediately crashes with a Metal/GPU-related error.  
**Cause:** The GGML Metal backend can fail after a rapid restart cycle on Apple Silicon.

**Fix:** Add `GGML_NO_METAL=1` to the gateway's `EnvironmentVariables` in its LaunchAgent plist, or set it in `openclaw.json` env vars, then force-reinstall:

```bash
GGML_NO_METAL=1 openclaw gateway start
```

Or permanently via the plist:
```xml
<key>EnvironmentVariables</key>
<dict>
  <key>GGML_NO_METAL</key>
  <string>1</string>
</dict>
```

---

## 2. Force-Reinstall After Config Changes

**Symptom:** Gateway won't pick up new config options (port, model, env vars).  
**Cause:** The LaunchAgent is still loaded with stale config.

**Fix:**
```bash
openclaw gateway install --force
```

This regenerates the plist, boots out the old agent, and bootstraps fresh. Run this after any `openclaw.json` changes.

---

## 3. Bootout + Bootstrap Recovery Sequence

When launchctl gets into a stuck state (service listed but unresponsive):

```bash
# Step 1: Remove the service from launchd's registry
launchctl bootout gui/$UID/ai.openclaw.gateway

# Step 2: Wait for the process to fully die
sleep 3

# Step 3: Re-register and start
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Step 4: Verify
launchctl list | grep ai.openclaw.gateway
```

> **Note:** `bootout` vs `unload` — always use `bootout`/`bootstrap` on macOS 10.11+. The old `load`/`unload` commands are deprecated and can leave orphaned service records.

---

## 4. Cooldown Logic (5-Minute Anti-Thrash)

The watchdog enforces a **5-minute cooldown** between auto-recovery attempts.

- Cooldown state stored in: `/tmp/openclaw/watchdog-last-recovery`
- If the file exists and was written < 300 seconds ago, the watchdog exits silently
- This prevents a crash loop from hammering the gateway repeatedly

**To reset the cooldown manually** (e.g. you want the watchdog to retry immediately):
```bash
rm -f /tmp/openclaw/watchdog-last-recovery
```

---

## 5. Log Location

All watchdog activity is logged to:

```
/tmp/openclaw/gateway-watchdog.log
```

Standard error (launchd output) goes to:

```
/tmp/openclaw/gateway-watchdog-err.log
```

Note: `/tmp` is cleared on reboot. For persistent logging, symlink to a path under `~/.openclaw/workspace/logs/` and update the plist paths accordingly.

**Live tail:**
```bash
tail -f /tmp/openclaw/gateway-watchdog.log
```

**Recent activity:**
```bash
tail -50 /tmp/openclaw/gateway-watchdog.log
```

---

## 6. "Already Loaded" Bootstrap Error

**Symptom:** `launchctl bootstrap` returns an error like `Load failed: 5: Input/output error` or `service already exists`.

**Fix:** Always bootout before bootstrapping:
```bash
launchctl bootout gui/$UID/ai.openclaw.gateway-watchdog 2>/dev/null || true
sleep 1
launchctl bootstrap gui/$UID ~/Library/LaunchAgents/ai.openclaw.gateway-watchdog.plist
```

The `install.sh` script handles this automatically.

---

## 7. Telegram Alerts Not Arriving

**Symptom:** Watchdog recovers gateway but no Telegram message is received.

**Checks:**
1. Verify `gog` is on PATH: `which gog` (should be `/opt/homebrew/bin/gog`)
2. Check Telegram auth: `gog telegram status`
3. Verify TELEGRAM_ID is correct in the watchdog script
4. Check for errors: `cat /tmp/openclaw/gateway-watchdog-err.log`

The watchdog uses `|| true` on the Telegram send so a failed alert never blocks recovery.
