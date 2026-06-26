# Claw Gatekeeper Security Deployment Guide

> **Human-in-the-Loop Security Mode**

---

## 🛡️ Security Mode Overview

| Mode | Auto-Allowed | Human Confirmation | Use Case |
|------|--------------|-------------------|----------|
| **Default** | LOW + MEDIUM | HIGH + CRITICAL | Daily convenience |
| **Hardened** | ❌ None | ✅ All | **Recommended** |
| **Emergency** | ❌ None | ✅ All + Delayed | High-risk environments |

---

## 🚀 Quick Hardening (3 Steps)

### Step 1: Check Current Configuration
```bash
cd ~/.claw-gatekeeper/scripts
./deploy-secure.sh --check
```

### Step 2: Apply Hardened Configuration
```bash
./deploy-secure.sh --apply
```

### Step 3: Verify Deployment
```bash
./deploy-secure.sh --check
```

---

## 📋 Hardened Configuration Details

### Core Security Settings

```json
{
  "strict_mode": true,           // Strict mode enabled
  "auto_allow_low": false,       // Disable auto-allow for LOW risk
  "auto_allow_medium": false,    // Disable auto-allow for MEDIUM risk
  "auto_allow_high": false,      // Disable auto-allow for HIGH risk
  "medium_requires_approval": true,  // MEDIUM requires confirmation
  "confirmation_timeout": 300    // 5-minute confirmation timeout
}
```

### Risk Level Behaviors

| Risk Level | Score Range | Hardened Mode Behavior |
|------------|-------------|------------------------|
| 🔴 **CRITICAL** | 80-100 | Always individual confirmation, no session approval |
| 🟠 **HIGH** | 60-79 | Always confirm, session approval available |
| 🟡 **MEDIUM** | 30-59 | Always confirm, session approval available |
| 🟢 **LOW** | 0-29 | **Always confirm** (different from default mode) |

### Enhanced Blacklist

Hardened configuration includes **20+ dangerous command patterns**:
- System destruction: `rm -rf /`, `mkfs`, `dd if=`
- Pipe execution: `curl | sh`, `wget | bash`
- Code injection: `eval $(`, `python -c 'import os'`
- Reverse shells: `nc -e`, `bash -i >& /dev/tcp`

### Sensitive Directory Protection

```json
"blacklist_paths": [
  "~/.ssh",      // SSH keys
  "~/.aws",      // AWS credentials
  "~/.kube",     // Kubernetes configs
  "~/.gnupg",    // GPG keys
  "~/.docker",   // Docker configs
  "~/.openclaw"  // OpenClaw self configs
]
```

---

## 🔐 Data Sanitization (Optional)

### Using the Sanitizer

```bash
# Check if file contains sensitive data
./scripts/sanitizer.sh --check session.json --verbose

# Sanitize file
./scripts/sanitizer.sh --file session.json > sanitized.json

# Pipe usage
cat conversation.txt | ./scripts/sanitizer.sh --stdin > clean.txt
```

### Supported Sensitive Patterns

| Category | Examples |
|----------|----------|
| Credentials | Password, API Key, Secret Token |
| Cloud Services | AWS Key, GitHub Token, OpenAI Key |
| Databases | MongoDB URI, PostgreSQL URI |
| Personal Information | Email, Credit Card, SSN |
| Cryptocurrency | Bitcoin, Ethereum addresses |
| Certificates | JWT, RSA Key, SSH Key |

---

## 📝 Audit Log Security

### Log Location
```
~/.claw-gatekeeper/sessions/Operate_Audit.log
```

### Permission Settings
```bash
chmod 700 ~/.claw-gatekeeper/sessions
chmod 600 ~/.claw-gatekeeper/sessions/Operate_Audit.log
```

### Automatic Cleanup (30-day retention)

The hardening script automatically adds a cron job:
```cron
0 0 * * * find ~/.claw-gatekeeper/sessions -name '*.log' -mtime +30 -delete
```

### Manual Verification
```bash
# Check log size
ls -lh ~/.claw-gatekeeper/sessions/Operate_Audit.log

# View recent entries
tail -20 ~/.claw-gatekeeper/sessions/Operate_Audit.log

# Check permissions
ls -la ~/.claw-gatekeeper/sessions/
```

---

## 🔄 Restore Default Configuration

```bash
cd ~/.claw-gatekeeper/scripts
./deploy-secure.sh --restore
```

---

## 🎯 Security Best Practices

### 1. Principle of Least Privilege
```bash
# Configuration file permissions
chmod 600 ~/.claw-gatekeeper/config.json

# Directory permissions
chmod 700 ~/.claw-gatekeeper
chmod 700 ~/.claw-gatekeeper/sessions
```

### 2. Regular Auditing
```bash
# Check for unusual denials
python3 ~/.claw-gatekeeper/scripts/policy_config.py stats

# View high-risk operation logs
grep "🔴 CRITICAL" ~/.claw-gatekeeper/sessions/Operate_Audit.log
```

### 3. Session Management
- **Session Approval**: MEDIUM/HIGH risks can be approved once for the session
- **Timeout Mechanism**: Automatically expires after 30 minutes of inactivity
- **CRITICAL Operations**: Always require individual confirmation, excluded from session approval

### 4. Network Isolation (Advanced)
If concerned about LLM data exfiltration:
```bash
# Configure local Ollama as decision backend
export GUARDIAN_MODEL_PROVIDER=ollama://localhost:11434
```

---

## 📊 Security Comparison

| Security Metric | Default Mode | Hardened Mode | Improvement |
|-----------------|--------------|---------------|-------------|
| Human-in-the-loop coverage | 40% | **100%** | +60% |
| Dangerous command interception | 5 patterns | **20+ patterns** | +300% |
| Sensitive directory protection | 4 dirs | **10+ dirs** | +150% |
| Auto-allowed operations | LOW + MEDIUM | **None** | -100% |
| Confirmation timeout | None | **5 minutes** | Added |
| Log retention | Permanent | **30 days** | Compliance |

---

## ⚠️ Important Notes

### Security Trade-offs

Hardened mode provides maximum security but has the following impacts:

1. **Operational Efficiency**: All operations require confirmation, potentially reducing productivity
2. **User Experience**: Frequent confirmation prompts may feel cumbersome
3. **False Positives**: Some safe operations may also be intercepted

### Recommendations

- **Daily use**: Standard mode + key directory protection
- **Handling sensitive data**: Hardened mode
- **Team collaboration**: Unified hardened configuration to prevent security drift

---

## 🔗 Related Files

| File | Purpose |
|------|---------|
| `config/config.hardened.json` | Hardened configuration file |
| `scripts/deploy-secure.sh` | One-click hardening deployment |
| `scripts/sanitizer.sh` | Data sanitization tool |
| `sessions/Operate_Audit.log` | Audit log |

---

## 🆘 Troubleshooting

### Issue: All operations being denied
```bash
# Check mode settings
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode

# If in emergency mode, switch back to standard
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode standard
```

### Issue: Log file too large
```bash
# Manually clean old logs
find ~/.claw-gatekeeper/sessions -name '*.log' -mtime +7 -delete
```

### Issue: Recover accidentally deleted configuration
```bash
# View backup list
ls -la ~/.claw-gatekeeper/backups/

# Manual restore
cp ~/.claw-gatekeeper/backups/config.json.bak.XXXX ~/.claw-gatekeeper/config.json
```

---

**Last Updated**: 2026-03-12  
**Version**: v0.1.1-hardened
