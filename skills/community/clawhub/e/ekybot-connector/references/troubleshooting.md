# EkyBot Connector Troubleshooting

Common issues and solutions for the EkyBot connector skill.

## Installation Issues

### Script Permission Denied

**Problem:** `Permission denied` when running scripts.

**Solution:**
```bash
chmod +x skills/ekybot-connector/scripts/*.sh
```

### Python Not Found

**Problem:** `python: command not found` or `python3: command not found`.

**Solution:**
- macOS: `brew install python3`
- Ubuntu/Debian: `sudo apt install python3`
- Or use full path: `/usr/bin/python3`

## Registration Issues

### Invalid Email Address

**Problem:** Registration fails with "invalid_email" error.

**Symptoms:**
```json
{
  "success": false,
  "error": "invalid_email",
  "message": "Email address is not valid"
}
```

**Solutions:**
1. Use a valid email format (user@domain.com)
2. Check for typos in email address
3. Ensure email domain exists

### Network Connection Failed

**Problem:** Cannot connect to EkyBot API during registration.

**Symptoms:**
```
[ERROR] Failed to connect to EkyBot API
```

**Solutions:**
1. Check internet connectivity: `ping www.ekybot.com`
2. Verify DNS resolution: `nslookup www.ekybot.com`
3. Check firewall settings
4. Try different network (corporate firewalls may block)

### Registration Timeout

**Problem:** Registration request hangs or times out.

**Solutions:**
1. Check network stability
2. Retry registration with: `scripts/register_workspace.sh`
3. Use verbose mode to debug: add `-v` to curl commands in script

## Configuration Issues

### Missing Configuration File

**Problem:** Scripts fail with "EkyBot connector not configured" error.

**Symptoms:**
```
[ERROR] EkyBot connector not configured. Run scripts/register_workspace.sh first.
```

**Solutions:**
1. Run registration: `scripts/register_workspace.sh`
2. Check configuration file exists: `ls -la ~/.openclaw/ekybot-connector/config.json`
3. Verify configuration permissions: `chmod 600 ~/.openclaw/ekybot-connector/config.json`

### Corrupted Configuration

**Problem:** Configuration file exists but contains invalid data.

**Symptoms:**
```
[ERROR] Invalid configuration. Missing workspace ID or API key.
```

**Solutions:**
1. Validate JSON format: `python3 -m json.tool ~/.openclaw/ekybot-connector/config.json`
2. Re-register workspace: `scripts/register_workspace.sh`
3. Manual fix: Edit configuration file with correct format

## API Issues

### Authentication Failed

**Problem:** API requests return 401 Unauthorized.

**Symptoms:**
```json
{
  "success": false,
  "error": "invalid_api_key",
  "message": "API key is invalid"
}
```

**Solutions:**
1. Verify API key format: should start with `ek_workspace_`
2. Check configuration file: `cat ~/.openclaw/ekybot-connector/config.json`
3. Re-register to get new API key
4. Ensure no extra spaces/characters in key

### Rate Limited

**Problem:** Too many requests, API returns 429 Too Many Requests.

**Symptoms:**
```json
{
  "success": false,
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded"
}
```

**Solutions:**
1. Reduce telemetry frequency (increase `--interval`)
2. Wait before retrying (exponential backoff)
3. Check for multiple instances running: `ps aux | grep telemetry`
4. Review rate limits in [api.md](api.md)

### Server Errors (5xx)

**Problem:** EkyBot API returning server errors.

**Symptoms:**
```
curl: (22) The requested URL returned error: 500 Internal Server Error
```

**Solutions:**
1. Check EkyBot status page (if available)
2. Retry with exponential backoff
3. Contact support if persistent
4. Use `--verbose` flag for detailed error information

## Health Check Issues

### OpenClaw Gateway Not Detected

**Problem:** Health check reports gateway not running when it is.

**Symptoms:**
```
[WARN] ❌ Gateway not running
Cannot check sessions (gateway not running)
```

**Solutions:**
1. Verify gateway is actually running: `openclaw status`
2. Check PATH includes OpenClaw CLI: `which openclaw`
3. Restart gateway: `openclaw gateway restart`
4. Check gateway configuration: `cat ~/.openclaw/openclaw.json`

### Permission Issues with System Monitoring

**Problem:** Cannot collect system metrics (CPU, memory, disk).

**Symptoms:**
```
[WARN] System monitoring tools not available
```

**Solutions:**
1. macOS: Ensure `top` and `vm_stat` are available
2. Linux: Install `sysstat` package: `sudo apt install sysstat`
3. Check command permissions: `which top`
4. Run with appropriate user permissions

### Session Detection Failed

**Problem:** Cannot detect active OpenClaw sessions.

**Symptoms:**
```
Active sessions: 0
```

**Solutions:**
1. Verify sessions exist: `openclaw sessions list`
2. Check session store permissions: `ls -la ~/.openclaw/agents/*/sessions/`
3. Restart gateway to refresh session tracking
4. Check agent configuration: `cat ~/.openclaw/openclaw.json`

## Telemetry Issues

### Daemon Won't Start

**Problem:** Telemetry daemon fails to start.

**Symptoms:**
```
[ERROR] Failed to start telemetry daemon
```

**Solutions:**
1. Check logs: `cat ~/.openclaw/ekybot-connector/telemetry.log`
3. Check for port conflicts or resource limits

### Daemon Dies Silently

**Problem:** Telemetry daemon starts but stops working.

**Symptoms:**
```
[WARN] ❌ Not running
```

**Solutions:**
1. Check logs for errors: `tail -20 ~/.openclaw/ekybot-connector/telemetry.log`
2. Check system resources (disk space, memory)
3. Look for crash dumps or system messages
4. Restart with lower frequency: `--interval 600`

### Data Not Appearing in EkyBot

**Problem:** Telemetry sends successfully but data doesn't appear in dashboard.

**Solutions:**
1. Verify workspace ID matches dashboard
2. Check API response for success status
3. Wait for dashboard refresh (may have delay)
4. Contact EkyBot support for data ingestion issues

## Debug Mode

### Enable Verbose Logging

Add verbose flags to scripts for detailed output:

```bash
# Registration with debug
scripts/register_workspace.sh --verbose

# Health check with debug  
scripts/health_check.sh --verbose

# Telemetry with debug
```

### Manual API Testing

Test API endpoints manually with curl:

```bash
# Test registration endpoint
curl -v -X POST "https://www.ekybot.com/api/workspaces/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","type":"openclaw"}'

# Test health endpoint  
curl -v -X GET "https://www.ekybot.com/api/workspaces/YOUR_ID/health" \
  -H "Authorization: Bearer YOUR_API_KEY"

# Test telemetry endpoint
curl -v -X POST "https://www.ekybot.com/api/workspaces/YOUR_ID/telemetry" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2026-03-06T17:00:00.000Z","type":"health_ping"}'
```

### Check Configuration

Validate configuration file format and content:

```bash
# Check JSON format
python3 -m json.tool ~/.openclaw/ekybot-connector/config.json

# Extract specific values
python3 -c "import json; config=json.load(open('$HOME/.openclaw/ekybot-connector/config.json')); print('Workspace:', config['workspace_id']); print('API Key:', config['api_key'][:12] + '...')"
```

### Log Analysis

Common log patterns to look for:

**Success patterns:**
```
[INFO] ✅ Registration successful!
[INFO] ✅ Health report sent successfully  
[INFO] ✅ Telemetry sent successfully
```

**Error patterns:**
```
[ERROR] Failed to connect to EkyBot API
[ERROR] Registration failed. Server response:
[ERROR] Failed to send health report to EkyBot
[ERROR] Failed to send telemetry to EkyBot
```

**Warning patterns:**
```
[WARN] ❌ Gateway not running
[WARN] Health report sent but server returned error:
[WARN] Telemetry sent but server returned error:
```

## Getting Help

### Collect Debug Information

When reporting issues, include:

1. **Configuration (sanitized):**
   ```bash
   python3 -c "import json; c=json.load(open('$HOME/.openclaw/ekybot-connector/config.json')); print(json.dumps({k:v for k,v in c.items() if k != 'api_key'}, indent=2))"
   ```

2. **System information:**
   ```bash
   echo "OS: $(uname -s -r)"
   echo "OpenClaw: $(openclaw --version 2>/dev/null || echo 'not found')"
   echo "Python: $(python3 --version 2>/dev/null || echo 'not found')"
   echo "Curl: $(curl --version 2>/dev/null | head -1 || echo 'not found')"
   ```

3. **Recent logs:**
   ```bash
   tail -20 ~/.openclaw/ekybot-connector/telemetry.log
   ```

4. **Error reproduction steps** with exact commands and output

### Contact Information

- **EkyBot Support:** Contact through EkyBot platform
- **OpenClaw Issues:** GitHub repository or community channels
- **Skill Issues:** Report to skill maintainer