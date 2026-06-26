# Browser Recovery Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Recovery Script Doesn't Kill Processes

**Symptoms:**
- `check_state.sh` shows browser processes
- `recover.sh` runs but processes remain

**Diagnosis:**
```bash
# Check if processes are owned by current user
ps -ef | grep -E 'chromium|chrome' | grep -v grep

# Check process details
ps aux | grep chromium
```

**Solutions:**
1. Processes owned by different user → Don't kill (safety)
2. Processes are system browsers → Don't kill (safety)
3. Processes are zombies → Try `kill -9` manually
4. Permission denied → Check user permissions

### Issue 2: Ports Still in Use After Recovery

**Symptoms:**
- Browser fails to start with "Address already in use"
- `check_state.sh` shows ports occupied

**Diagnosis:**
```bash
# Check what's using the port
lsof -iTCP:9222 -sTCP:LISTEN -P
netstat -tuln | grep 9222

# Check if it's a browser process
ps -p <PID>
```

**Solutions:**
1. Non-browser process using port → Change browser port in config
2. Browser process from different instance → Kill manually if safe
3. Port in TIME_WAIT state → Wait 60 seconds or change port
4. Firewall/proxy using port → Reconfigure or use different port

### Issue 3: Lock Files Persist

**Symptoms:**
- Browser fails with "Profile in use" error
- `check_state.sh` shows lock files

**Diagnosis:**
```bash
# List all lock files
find ~/.openclaw/browser -name "Singleton*"

# Check if any process is holding the lock
lsof ~/.openclaw/browser/*/SingletonLock
```

**Solutions:**
1. Process still running → Kill process first, then remove locks
2. Stale lock (no process) → Safe to remove
3. Permission denied → Check file ownership and permissions
4. Lock in use by another instance → Don't remove (safety)

### Issue 4: Recovery Fails with "Command not found"

**Symptoms:**
- Script errors: `fuser: command not found` or `lsof: command not found`

**Diagnosis:**
```bash
# Check available commands
command -v fuser
command -v lsof
command -v pkill
```

**Solutions:**
1. Install missing tools:
   ```bash
   # Debian/Ubuntu
   sudo apt-get install psmisc lsof procps
   
   # RHEL/CentOS
   sudo yum install psmisc lsof procps-ng
   
   # macOS
   # lsof is built-in, fuser not available (script handles this)
   ```

2. Use alternative commands (script should handle this automatically)

### Issue 5: Multiple Recovery Attempts Fail

**Symptoms:**
- First recovery succeeds, but browser still fails
- Second recovery attempt also fails

**Diagnosis:**
```bash
# Check for deeper issues
journalctl -xe | grep -i chrome
dmesg | grep -i chrome

# Check system resources
df -h  # Disk space
free -h  # Memory
ulimit -a  # Process limits
```

**Possible Causes:**
1. **Insufficient resources**: Out of memory, disk full
2. **Missing dependencies**: Browser libraries not installed
3. **Corrupted profile**: Profile data is corrupted
4. **System-level issues**: SELinux, AppArmor blocking browser

**Solutions:**
1. Free up resources
2. Reinstall browser
3. Delete and recreate profile directory
4. Check system security policies

### Issue 6: Wrong Browser Instance Killed

**Symptoms:**
- User's personal browser closed unexpectedly
- Wrong profile data deleted

**Prevention:**
- Always check process command line before killing
- Verify profile path matches OpenClaw's directory
- Use more specific process matching patterns

**Recovery:**
1. Apologize to user
2. Explain what happened
3. Help restore lost work if possible
4. Update script to prevent recurrence

## Diagnostic Commands Reference

### Process Inspection
```bash
# List all browser processes with full command
ps -ef | grep -E 'chromium|chrome' | grep -v grep

# Show process tree
pstree -p | grep -E 'chromium|chrome'

# Check process details
ps aux | grep chromium
```

### Port Inspection
```bash
# Check specific port
lsof -iTCP:9222 -sTCP:LISTEN -P
netstat -tuln | grep 9222
ss -tuln | grep 9222

# Check all browser-related ports
lsof -iTCP -sTCP:LISTEN -P | grep -E 'chrome|chromium'
```

### File System Inspection
```bash
# Find all lock files
find ~/.openclaw/browser -name "Singleton*"

# Check profile directory size
du -sh ~/.openclaw/browser/*

# Check for open file handles
lsof +D ~/.openclaw/browser
```

### System Resource Check
```bash
# Memory usage
free -h
ps aux --sort=-%mem | head

# Disk space
df -h
du -sh ~/.openclaw/browser

# Process limits
ulimit -a
cat /proc/sys/kernel/pid_max
```

## When to Escalate to Human

Escalate if:
1. Recovery fails twice in the same session
2. System-level issues detected (permissions, resources)
3. Risk of data loss or affecting other processes
4. Unfamiliar error messages or behaviors
5. User explicitly requests manual intervention

## Logging and Debugging

### Enable Verbose Logging
```bash
# Run scripts with bash debug mode
bash -x scripts/recover.sh --full

# Capture full output
scripts/recover.sh --full 2>&1 | tee recovery.log
```

### Check OpenClaw Logs
```bash
# Find OpenClaw log directory
ls -la ~/.openclaw/logs/

# Check recent browser-related logs
grep -i browser ~/.openclaw/logs/*.log | tail -50
```

## Preventive Measures

1. **Regular cleanup**: Run recovery during idle times
2. **Monitor resources**: Check disk space and memory regularly
3. **Update scripts**: Keep recovery scripts updated with new edge cases
4. **Test changes**: Always test script modifications in safe environment
5. **Document incidents**: Record unusual failures for future reference
