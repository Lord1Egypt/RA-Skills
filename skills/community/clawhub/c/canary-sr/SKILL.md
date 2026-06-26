---
slug: "canary-sr"
name: "Canary Agent Safety Tripwire System"
description: "Safety monitoring and tripwire detection for AI agents. Protects against unauthorized file access, dangerous commands, and excessive activity. Auto-halts on critical violations. Honeypot tripwires detect snooping."
author: "@TheShadowRose"
version: "1.0.8"
tags: ["safety", "security", "tripwire", "monitoring", "honeypot", "agent-protection"]
license: "MIT"
---

# Canary Agent Safety Tripwire System

Safety monitoring and tripwire detection for AI agents. Protects against unauthorized file access, dangerous commands, and excessive activity. Auto-halts on critical violations. Honeypot tripwires detect snooping.

---

**Safety monitoring and tripwire detection for AI agents.**

Protects against unauthorized file access, dangerous commands, and excessive activity. Auto-halts on critical violations. Honeypot tripwires detect snooping.

---

## What It Does

Canary provides three layers of agent safety:

1. **Action Monitoring** - Checks file paths and commands before execution
2. **Tripwire Files** - Honeypot files that should never be accessed
3. **Audit Trail** - Complete logs and pattern detection

### Core Features

**Protected Paths:**
- Block access to sensitive directories (`/etc/`, `~/.ssh/`, etc.)
- Customizable protection list
- Granular operation control (read, write, delete)

**Forbidden Patterns:**
- Regular expression matching for dangerous commands
- Detects `rm -rf /`, `chmod 777`, `curl | sh`, etc.
- Extensible pattern library

**Rate Limiting:**
- Limit file operations, network requests, command executions
- Configurable windows and thresholds
- Prevents runaway agents

**Auto-Halt:**
- Automatically stops agent after violation threshold
- Prevents cascading failures
- Requires manual review to restart

**Tripwire Files:**
- Create honeypot files that should never be accessed
- Detect modifications, deletions, or access
- Hash verification for file integrity

**Audit Trail:**
- Complete action logs
- Violation history
- Pattern detection (rapid violations, repeated targets, time clusters)
- Export to JSON or Markdown

---

## Quick Start

### Install

No dependencies! Python 3.7+ stdlib only.

```bash
# Copy config example
cp config_example.json config.json

# Edit config with your protected paths
nano config.json
```

### Basic Usage

```python
from canary import CanaryMonitor

# Initialize monitor
canary = CanaryMonitor('config.json')

# Check path before access
is_safe, reason = canary.check_path('/etc/passwd', 'read')
if not is_safe:
    print(f"Blocked: {reason}")
    exit(1)

# Check command before execution
is_safe, reason = canary.check_command('rm -rf /')
if not is_safe:
    print(f"Blocked: {reason}")
    exit(1)

# Get status
status = canary.get_status()
print(f"Violations: {status['violation_count']}/{status['halt_threshold']}")
```

### CLI Usage

```bash
# Check status
python3 canary.py status

# Check if path is safe
python3 canary.py check-path --path /etc/passwd --operation read

# Check if command is safe
python3 canary.py check-command --command "rm -rf /"

# Reset monitoring (clears violations)
python3 canary.py reset
```

---

## Tripwire Files

Create honeypot files that should never be accessed:

```bash
# Create tripwire
python3 canary_tripwire.py create \
  --path ~/.secrets/fake-api-key.txt \
  --severity critical \
  --description "Honeypot to detect credential snooping"

# List all tripwires
python3 canary_tripwire.py list

# Check for triggered tripwires
python3 canary_tripwire.py check

# View alert history
python3 canary_tripwire.py alerts --limit 10

# Remove tripwire
python3 canary_tripwire.py remove --path ~/.secrets/fake-api-key.txt
```

### Python API

```python
from canary_tripwire import TripwireManager

manager = TripwireManager()

# Create tripwire
manager.create_tripwire(
    path='~/.aws/fake-credentials',
    severity='critical',
    description='Detects AWS credential access'
)

# Check all tripwires
triggered = manager.check_tripwires()
if triggered:
    print(f"⚠️  {len(triggered)} tripwire(s) triggered!")
    for alert in triggered:
        print(f"  - {alert['path']}: {alert['event']}")
```

---

## Audit Reports

Analyze logs and generate safety reports:

```bash
# Summary report
python3 canary_audit.py summary

# View violations by severity
python3 canary_audit.py violations --severity critical

# Timeline of recent events
python3 canary_audit.py timeline --hours 24

# Detect suspicious patterns
python3 canary_audit.py patterns

# Export full report
python3 canary_audit.py export --output report.json --format json
python3 canary_audit.py export --output report.md --format markdown
```

### Python API

```python
from canary_audit import CanaryAuditor

auditor = CanaryAuditor('canary.log')

# Generate summary
summary = auditor.generate_summary_report()
print(f"Total violations: {summary['total_violations']}")

# Get critical violations
critical = auditor.get_violations_by_severity('critical')

# Detect patterns
patterns = auditor.detect_patterns()
if patterns['rapid_violations']:
    print("⚠️  Rapid violation sequence detected!")

# Export report
auditor.export_report('safety-report.md', format='markdown')
```

---

## Configuration

See `config_example.json` for all options.

### Essential Settings

```json
{
  "protected_paths": [
    "/etc/",
    "~/.ssh/",
    "~/critical-data/"
  ],
  "forbidden_patterns": [
    "rm\\s+-rf\\s+/",
    "chmod\\s+777",
    "curl.*\\|\\s*sh"
  ],
  "halt_threshold": 5,
  "rate_limits": {
    "file_operations": {"limit": 100, "window": 60},
    "command_executions": {"limit": 20, "window": 60}
  }
}
```

---

## Integration Examples

### With Agent Runtime

```python
from canary import CanaryMonitor

canary = CanaryMonitor('config.json')

def safe_file_read(path):
    """Read file with Canary check."""
    is_safe, reason = canary.check_path(path, 'read')
    if not is_safe:
        raise PermissionError(reason)
    
    with open(path, 'r') as f:
        return f.read()

def safe_command(cmd):
    """Execute command with Canary check."""
    is_safe, reason = canary.check_command(cmd)
    if not is_safe:
        raise PermissionError(reason)
    
    import subprocess
    cmd_list = cmd.split() if isinstance(cmd, str) else cmd
    return subprocess.run(cmd_list, capture_output=True)
```

### Pre-Deployment Checks

```python
# Before deploying agent, verify Canary setup
from canary import CanaryMonitor

canary = CanaryMonitor('config.json')

# Verify protected paths are configured
status = canary.get_status()
if status['protected_paths_count'] == 0:
    print("⚠️  No protected paths configured!")
    exit(1)

# Test tripwire detection
from canary_tripwire import TripwireManager
manager = TripwireManager()

# Create test tripwire
manager.create_tripwire('/tmp/canary-test.txt', severity='high')

# Verify it exists
triggered = manager.check_tripwires()
if not any(t['path'] == '/tmp/canary-test.txt' for t in triggered):
    print("✅ Tripwire system operational")

# Cleanup
manager.remove_tripwire('/tmp/canary-test.txt', delete_file=True)
```

---

## Use Cases

### 1. Autonomous Agent Safety

Deploy Canary alongside autonomous agents to prevent:
- Accidental system file deletion
- Credential exfiltration
- Runaway command execution

### 2. Multi-Agent Systems

Each agent gets its own Canary instance with custom rules:
- Research agent: limited network access
- Coding agent: no production deployments
- Admin agent: full access but strict audit

### 3. Development/Testing

Use Canary during agent development:
- Catch dangerous patterns early
- Test rate limiting behavior
- Verify safety mechanisms work

### 4. Production Monitoring

Run Canary in production:
- Real-time violation alerts
- Audit trail for compliance
- Pattern detection for anomalies

---

## Architecture

```
┌─────────────────┐
│   Your Agent    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ CanaryMonitor   │◄────►│  config.py       │
│ (canary.py)     │      │  (your rules)    │
└────────┬────────┘      └──────────────────┘
         │
         ├─────► canary.log (action log)
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ TripwireManager │◄────►│ .canary_tripwires│
│ (tripwire.py)   │      │ (honeypot files) │
└────────┬────────┘      └──────────────────┘
         │
         └─────► alerts.log
         
         
┌─────────────────┐
│ CanaryAuditor   │───► reports (JSON/MD)
│ (audit.py)      │
└─────────────────┘
```

---

## Best Practices

### Start Conservative

Begin with strict rules, relax as needed:

```python
protected_paths = [
    '/',  # Protect entire filesystem initially
]

halt_threshold = 3  # Low threshold to catch issues early
```

### Use Tripwires Strategically

Place tripwires in sensitive locations:
- Fake credential files
- Empty "secrets" directories
- Decoy config files

### Review Logs Regularly

```bash
# Daily audit
python3 canary_audit.py summary

# Weekly deep dive
python3 canary_audit.py patterns
python3 canary_audit.py export --output weekly-report.md --format markdown
```

### Test Your Configuration

```python
# Verify Canary blocks what it should
canary = CanaryMonitor('config.json')

# These should all be blocked
assert not canary.check_path('/etc/passwd', 'delete')[0]
assert not canary.check_command('rm -rf /')[0]
assert not canary.check_command('chmod 777 /tmp')[0]

print("✅ Canary configuration verified")
```

---

## Limitations

See [LIMITATIONS.md](LIMITATIONS.md) for details.

**Key constraints:**
- Pattern matching is regex-based (not semantic analysis)
- No built-in alerting (logs only)
- Tripwires detect access, not intent
- Rate limiting is per-session (doesn't survive restarts)

---

## License

MIT License - See [LICENSE](LICENSE)

**Author:** Shadow Rose

---

## Why This Exists

AI agents can do a lot of damage quickly:
- One bad command can delete critical files
- Runaway loops can exhaust resources
- Compromised agents can exfiltrate credentials

Canary provides defense-in-depth:
- **Preventive:** Block dangerous actions before they happen
- **Detective:** Tripwires catch snooping behavior
- **Forensic:** Complete audit trail for post-incident analysis

Simple, zero-dependency safety for autonomous agents.


---


## ⚠️ Security Note — Config File

Configuration is loaded from a JSON file. This is safe to share — no code execution.

- Config path is validated for existence and size (1MB cap) before loading
- Must be a `.json` file — `CanaryMonitor` raises `ValueError` if given a non-JSON path
- Keep your config under version control; treat it as security policy

## ⚠️ Security Note — Tripwire Deployment

- **Paths are fully resolved** — `~` and relative paths are expanded via `Path.expanduser().resolve()` before creation and lookup. `'~/.aws/fake-credentials'` will be placed in your actual home directory, not a literal `~` path.
- **Use decoy paths only** — never point tripwires at real files containing sensitive data. Tripwires are honeypots; treat them as bait, not protection.
- **`create_tripwire` will not overwrite existing files** — it checks for pre-existing files and refuses to proceed. Use dedicated empty paths for tripwires.
- **Test in a sandbox first** — verify where logs, tripwires, and registry files are created before deploying. Confirm protected paths and auto-halt behavior in an isolated environment.
- **Protect log and alert directories** — set filesystem permissions so alert logs are not world-readable. Canary writes plaintext logs; restrict access accordingly.
- **Canary only blocks when called** — it is not an OS-level enforcement mechanism. Layer it with containers, filesystem permissions, and `auditd` for production deployments.

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**SECURITY DISCLAIMER:** This software provides supplementary security measures and 
is NOT a replacement for professional security auditing, penetration testing, or 
compliance frameworks. No software can guarantee complete protection against all 
threats. Users operating in regulated industries (healthcare, finance, legal) should 
consult qualified security professionals and verify compliance with applicable 
regulations (GDPR, HIPAA, SOC2, etc.) independently.
---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)

> **📦 Install note:** The slug `canary` was already taken on ClawHub.
> Install this skill using: `clawhub install canary-sr`
