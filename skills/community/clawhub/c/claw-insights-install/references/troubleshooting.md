# Troubleshooting

> Paths below use default locations. If you customized `CLAW_INSIGHTS_DIR`, `CLAW_INSIGHTS_DB`, or other path variables, substitute accordingly.

## Port Conflict — `EADDRINUSE`

**Symptom:** `Error: listen EADDRINUSE: address already in use :::41041`

**Diagnosis:**

```bash
lsof -i :41041
# or
claw-insights stop
```

**Fix:**

- Stop existing instance: `claw-insights stop`
- Or use a different port: `claw-insights start --port 8080`

---

## Gateway Connection Failed

**Symptom:** Dashboard shows "Gateway: disconnected" or data panels are empty.

**Diagnosis:**

```bash
# Check if OpenClaw gateway is running
openclaw gateway status

# Check if sessions file exists
ls ~/.openclaw/agents/main/sessions/sessions.json
```

**Fix:**

- Start gateway: `openclaw gateway start`
- If sessions file missing: ensure OpenClaw is configured and has run at least once
- Check `CLAW_INSIGHTS_DIR` points to the correct OpenClaw directory

---

## Authentication Issues

### 401 Unauthorized

**Symptom:** API calls return `401` status.

**Diagnosis:**

```bash
# Check configured token
echo "$CLAW_INSIGHTS_API_TOKEN"
# Or check auth-secret file
cat ~/.claw-insights/auth-secret 2>/dev/null

# Test token against an authenticated endpoint
TOKEN="${CLAW_INSIGHTS_API_TOKEN:-$(cat ~/.claw-insights/auth-secret 2>/dev/null)}"
curl -s -o /dev/null -w "%{http_code}" \
  -X POST http://127.0.0.1:41041/api/snapshot \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{}'
# → 200 = token valid, 401 = token invalid
```

> Note: `/health` does not require auth and cannot be used to verify tokens.

**Fix:**

- Ensure Bearer token matches `CLAW_INSIGHTS_API_TOKEN` or the value in `~/.claw-insights/auth-secret`
- Token must be ≥ 32 characters
- Or disable auth: `claw-insights start --no-auth`

### Cookie / Session Expired

**Symptom:** Web UI suddenly asks for re-authentication.

**Fix:** This is normal — session cookies rotate every 24h by default. Re-enter the token. To extend: increase `CLAW_INSIGHTS_TOKEN_ROTATION_INTERVAL_MS`.

---

## Database Issues

### Permission Denied

**Symptom:** `SQLITE_CANTOPEN` or permission errors on startup.

**Diagnosis:**

```bash
ls -la ~/.claw-insights/metrics.db
```

**Fix:**

- Ensure the user running claw-insights has read/write access
- Or set a custom path: `CLAW_INSIGHTS_DB=/path/to/writable/metrics.db`

### Database Corruption

**Symptom:** Queries fail with `SQLITE_CORRUPT` errors.

**Fix:**

```bash
# Stop the service
claw-insights stop

# Back up corrupted file
mv ~/.claw-insights/metrics.db ~/.claw-insights/metrics.db.bak

# Restart — a fresh database will be created
claw-insights start
```

Historical data will be lost, but new data collection starts immediately.

---

## Node.js Version Incompatibility

**Symptom:** `SyntaxError: Unexpected token` or import errors on startup.

**Diagnosis:**

```bash
node --version
# Must be ≥ 22.5
```

**Fix:**

- Upgrade Node.js: `nvm install 22` or download from https://nodejs.org
- Claw Insights uses Node.js native features (ESM, fetch, etc.) that require ≥ 22.5

---

## Remote Access

**Symptom:** Cannot access dashboard from another machine on the network.

**Diagnosis:**

```bash
# Check if listening on all interfaces
curl http://YOUR_IP:41041/health
```

**Fix:**

- By default, claw-insights binds to `127.0.0.1` (localhost only)
- For LAN access, use a reverse proxy (nginx, caddy) or SSH tunnel:
  ```bash
  ssh -L 41041:127.0.0.1:41041 user@remote-host
  ```
- **Security note:** Do not expose claw-insights directly to the internet without authentication enabled
