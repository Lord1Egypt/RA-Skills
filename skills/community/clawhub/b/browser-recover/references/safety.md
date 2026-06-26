# Safety Guidelines for Browser Recovery

## Core Principles

1. **Isolation First**: Only clean up OpenClaw-managed browser instances
2. **Verify Before Kill**: Check process ownership before terminating
3. **Preserve User Data**: Never delete user's personal browser profiles
4. **Graceful Degradation**: If a cleanup step fails, continue with others

## What NOT to Do

### ❌ Never Kill System-Wide Browsers
```bash
# WRONG: This kills ALL Chrome instances including user's personal browser
killall chrome
pkill chrome
```

### ❌ Never Delete User Profile Directories
```bash
# WRONG: This deletes user's personal browsing data
rm -rf ~/.config/google-chrome
rm -rf ~/.config/chromium
```

### ❌ Never Use kill -9 Without Verification
```bash
# WRONG: Forcefully kills without checking ownership
kill -9 $(pidof chrome)
```

## What TO Do

### ✅ Target OpenClaw-Specific Processes
```bash
# CORRECT: Only kills processes matching OpenClaw patterns
pkill -f "chromium.*--remote-debugging-port"
pkill -f "chrome.*--user-data-dir=$HOME/.openclaw"
```

### ✅ Clean Only OpenClaw Profile Directories
```bash
# CORRECT: Only cleans OpenClaw-managed profiles
rm -f ~/.openclaw/browser/*/SingletonLock
rm -rf ~/.openclaw/browser/*/Cache
```

### ✅ Verify Port Ownership Before Clearing
```bash
# CORRECT: Check what's using the port first
lsof -iTCP:9222 -sTCP:LISTEN -P
# Then decide if it's safe to kill
```

## Multi-Instance Environments

If multiple OpenClaw agents or browser instances are running:

1. **Use workspace-specific profiles**: Each agent should have its own profile directory
2. **Use unique debug ports**: Configure different ports for each instance
3. **Check process ownership**: Verify the process belongs to the current agent before killing

## Emergency Procedures

### If Recovery Script Fails
1. Check logs for specific error messages
2. Run `check_state.sh` to diagnose the issue
3. Manually inspect processes: `ps -ef | grep chrome`
4. If unsure, escalate to human operator

### If Wrong Processes Are Killed
1. Apologize to the user immediately
2. Explain what happened and why
3. Document the incident for future prevention
4. Update the recovery script to prevent recurrence

## Testing Guidelines

Before deploying changes to recovery scripts:

1. Test in a safe environment (VM or container)
2. Verify it doesn't affect user's personal browser
3. Test with multiple browser instances running
4. Test with ports already in use by other services
5. Test with missing directories or permissions issues

## Logging Best Practices

All recovery actions should log to stderr for OpenClaw to capture:

```bash
echo "Killing process PID $pid" >&2
echo "Cleared port $port" >&2
echo "ERROR: Failed to remove lock file" >&2
```

Use color codes for clarity:
- 🟢 Green: Success messages
- 🟡 Yellow: Warning messages
- 🔴 Red: Error messages
