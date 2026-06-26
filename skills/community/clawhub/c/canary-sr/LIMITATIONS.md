# Canary — Limitations

**Last updated:** 2026-02-21

---

## What This Does NOT Do

### 1. Semantic Analysis of Commands

**Limitation:** Canary uses regex pattern matching, not semantic understanding.

**Example:**
```python
# This is blocked:
canary.check_command('rm -rf /')

# This might NOT be blocked (obfuscated):
canary.check_command('r''m -rf /')  # Space in command name
canary.check_command('RM -RF /')    # Case may bypass patterns
```

**Why:** Full semantic analysis requires complex parsing and execution simulation.

**Workaround:**
- Add patterns for common obfuscation techniques
- Use case-insensitive regex (already enabled)
- Review logs for suspicious patterns that weren't caught

---

### 2. Built-In Alerting

**Limitation:** Canary logs violations but doesn't send alerts (email, Slack, etc.).

**Why:** Alerting integrations vary by environment:
- Some use email
- Some use Slack/Discord webhooks
- Some use monitoring platforms

**Workaround:**
```python
from canary import CanaryMonitor

canary = CanaryMonitor()

# Add custom alert handler
def send_alert(violation):
    import requests
    requests.post('https://hooks.slack.com/...', json={
        'text': f"🚨 Canary alert: {violation['message']}"
    })

# Monkey-patch or wrap _log_violation
original_log = canary._log_violation
def log_with_alert(severity, message):
    original_log(severity, message)
    if severity in ['critical', 'high']:
        send_alert({'severity': severity, 'message': message})

canary._log_violation = log_with_alert
```

---

### 3. Cross-Session Rate Limiting

**Limitation:** Rate limits reset when Canary restarts.

**Example:**
- Agent makes 90 file operations
- Crashes and restarts
- Limit resets to 0 (can make another 100)

**Why:** Rate limit state is in-memory only.

**Workaround:**
- Persist rate limit state to disk (add to config)
- Load state on initialization
- Example:

```python
import json
from pathlib import Path

# Save state on exit
def save_rate_limits(canary):
    state = {
        'rate_limits': canary.rate_limits,
        'timestamp': time.time()
    }
    with open('canary_state.json', 'w') as f:
        json.dump(state, f)

# Load state on init
def load_rate_limits():
    if Path('canary_state.json').exists():
        with open('canary_state.json', 'r') as f:
            return json.load(f)
    return {}
```

---

### 4. Tripwire Access Time Precision

**Limitation:** File access time (`atime`) may not update reliably.

**Why:**
- Some filesystems disable `atime` for performance (`noatime` mount option)
- OS may batch `atime` updates
- Not all file access updates `atime`

**Workaround:**
- Rely on modification time and hash checks (more reliable)
- Use filesystem auditing if available (auditd on Linux)
- Consider tripwire access detection "best effort"

---

### 5. No Sandboxing or Isolation

**Limitation:** Canary checks actions but doesn't enforce sandboxing.

**Example:**
- Canary blocks `rm /etc/passwd`
- Agent can still try to run it (Canary just logs it)
- Enforcement depends on agent respecting Canary's response

**Why:** Sandboxing requires OS-level isolation (containers, VMs, chroot).

**Workaround:**
- Run agent in container with limited permissions
- Use Canary + Docker/Podman for defense-in-depth
- Agent code must respect Canary checks (design agents to honor safety)

---

### 6. Pattern Bypass via Encoding

**Limitation:** Patterns can be bypassed with base64, hex, or other encoding.

**Example:**
```bash
# This is blocked:
rm -rf /

# This might NOT be blocked:
echo "cm0gLXJmIC8=" | base64 -d | sh  # Decodes to "rm -rf /"
```

**Why:** Detecting all encoding schemes is intractable.

**Workaround:**
- Add patterns for common encoding patterns (`base64 -d`, `echo | sh`)
- Monitor for unusual command sequences
- Review audit logs for suspicious activity

---

### 7. No Permission Enforcement

**Limitation:** Canary doesn't modify file system permissions.

**Example:**
- Canary protects `~/.ssh/`
- Agent could still access it if OS permissions allow
- Canary logs it, doesn't block at filesystem level

**Why:** Filesystem permissions are OS responsibility.

**Workaround:**
- Use OS permissions + Canary together
- Set restrictive file permissions (`chmod 600 ~/.ssh/id_rsa`)
- Run agent with limited user account

---

### 8. Single-Threaded Monitoring

**Limitation:** Canary is not thread-safe for concurrent operations.

**Why:** Designed for single-agent use cases.

**Workaround:**
- Use one Canary instance per agent
- Add locks if using in multi-threaded agent:

```python
import threading

canary_lock = threading.Lock()

def safe_check(path):
    with canary_lock:
        return canary.check_path(path)
```

---

### 9. Log File Growth

**Limitation:** No built-in log rotation. Logs grow indefinitely.

**Why:** Log rotation strategies vary (size-based, time-based, external tools).

**Workaround:**
- Use `logrotate` (Linux) or similar tool
- Implement custom rotation:

```python
from pathlib import Path

log_file = Path('canary.log')
if log_file.stat().st_size > 10 * 1024 * 1024:  # 10 MB
    log_file.rename('canary.log.old')
    log_file.touch()
```

---

### 10. No Real-Time Process Monitoring

**Limitation:** Canary checks actions when called, not in real-time.

**Example:**
- Agent code must call `canary.check_command(cmd)` before running `cmd`
- If agent bypasses Canary and runs command directly, no protection

**Why:** Real-time process monitoring requires kernel hooks or system-level auditing.

**Workaround:**
- Design agent to route all actions through Canary
- Use OS-level auditing (auditd, sysmon) for belt-and-suspenders
- Review audit logs to verify Canary is being called

---

### 11. Limited Path Traversal Detection

**Limitation:** Path normalization may miss complex traversal.

**Example:**
```python
# Canary normalizes paths, but edge cases exist:
canary.check_path('/tmp/../etc/passwd')  # Likely caught
canary.check_path('/tmp/./../../etc/passwd')  # Should be caught
# Symlink attacks might bypass if not resolved
```

**Why:** Full path resolution requires filesystem access and symlink resolution.

**Workaround:**
- Use `os.path.realpath()` before passing to Canary
- Check both original and resolved paths

---

### 12. No Anomaly Detection

**Limitation:** Canary detects patterns, not anomalies.

**Example:**
- Agent normally accesses 10 files/hour
- Suddenly accesses 1000 files/hour
- Rate limit might catch it, but no anomaly-based detection

**Why:** Anomaly detection requires baseline learning and statistical modeling.

**Workaround:**
- Use `canary_audit.py` to detect patterns manually
- Integrate with external anomaly detection tools
- Review audit logs for unusual spikes

---

## Design Philosophy

**Canary is a safety net, not a jail.**

✅ **Does well:**
- Blocks known-bad patterns
- Logs all actions for audit
- Detects tripwire access
- Auto-halts on excessive violations

❌ **Doesn't do:**
- Semantic analysis of code
- Real-time process monitoring
- OS-level sandboxing
- Anomaly detection

**Recommended architecture:**

```
┌──────────────────────────────────┐
│  OS Permissions + Containers     │  ← Isolation layer
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│  Canary (pattern blocking)       │  ← Safety checks
└────────────┬─────────────────────┘
             │
┌────────────▼─────────────────────┐
│  Agent (honors Canary checks)    │  ← Application layer
└──────────────────────────────────┘
```

Use Canary as part of defense-in-depth, not sole protection.

---

## Python Version Compatibility

**Requires:** Python 3.7+

**Why:** Uses `pathlib`, type hints, f-strings, and `datetime.fromisoformat()`.

---

## Platform Support

**Tested on:**
- Linux (Ubuntu, Debian, Arch)
- macOS 10.15+
- Windows 10+ (WSL recommended)

**Known issues:**
- Windows path handling (use `Path` for cross-platform)
- `atime` updates vary by filesystem

---

## When NOT to Use Canary

**Don't use Canary if:**

- You need real-time kernel-level monitoring → Use OS auditing (auditd, sysmon)
- You need semantic code analysis → Use static analysis tools
- You need guaranteed sandboxing → Use containers or VMs
- You need anomaly detection → Use ML-based monitoring

**Canary is for:**
- Pattern-based safety checks
- Audit logging
- Tripwire detection
- Auto-halt on violations

Know its limits. Use appropriate tools for each layer.

---

## Questions?

If something doesn't work as expected, check:
1. Is it in this limitations doc?
2. Is your config correct? (see config_example.py)
3. Are you using supported Python version (3.7+)?

Still stuck? Review audit logs for clues.
