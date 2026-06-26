# Claw-Gatekeeper User Guide

Complete guide for using Claw-Guardian effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Understanding Interceptions](#understanding-interceptions)
3. [Making Decisions](#making-decisions)
4. [Configuration](#configuration)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First-Time Setup

1. **Install Claw-Guardian** following the README instructions

2. **Initialize configuration**:
   ```bash
   python3 scripts/policy_config.py show
   ```

3. **Choose your mode**:
   ```bash
   # For personal use
   python3 scripts/policy_config.py mode standard
   
   # For high-security environments
   python3 scripts/policy_config.py mode strict
   ```

4. **Test the system**:
   ```bash
   python3 scripts/risk_engine.py file delete ~/test.txt
   ```

### Your First Interception

When Guardian intercepts an operation, you'll see:

```
🛡️ CLAW-GATEKEEPER SECURITY INTERCEPTION
============================================================

📋 Operation: 📁 File Operation
📝 Detail: delete ~/Documents/old-file.txt

🟠 Risk Level: HIGH
📊 Risk Score: 65/100

⚠️ Risk Analysis:
   1. File deletion operation
   2. Target in Documents folder

💡 Recommendation: About to delete 1 item(s). Ensure important 
   data is backed up before proceeding.

SELECT AN OPTION:
   [y] ✅ Allow this time only
   [Y] ✅✅ Always allow (add to whitelist)
   [n] ❌ Deny this time
   [N] ❌❌ Always deny (add to blacklist)
   [?] ℹ️  View details

Your choice: 
```

---

## Understanding Interceptions

### Risk Level Indicators

| Emoji | Level | Score | What It Means |
|-------|-------|-------|---------------|
| 🔴 | CRITICAL | 80-100 | Could cause serious damage or data loss |
| 🟠 | HIGH | 60-79 | Sensitive operation, proceed with caution |
| 🟡 | MEDIUM | 30-59 | Some risk, but generally manageable |
| 🟢 | LOW | 0-29 | Safe operation, minimal risk |

### Reading Risk Analysis

The risk analysis lists specific concerns:

```
⚠️ Risk Analysis:
   1. Directory deletion with 1,247 files
   2. Recursive operation
   3. Detected .git directory (active project)
```

Each numbered item explains why the operation is considered risky.

### Understanding Recommendations

The recommendation provides actionable advice:

```
💡 Recommendation: About to delete 1,247 item(s). Ensure important 
   data is backed up before proceeding.
```

---

## Making Decisions

### Option Guide

#### [y] Allow this time only
- **Use when**: You want to proceed but don't want to change future behavior
- **Effect**: Operation proceeds, but you'll be asked again next time
- **Example**: One-time cleanup of a specific file

#### [Y] Always allow (add to whitelist)
- **Use when**: This is a trusted, frequent operation you always want to allow
- **Effect**: Similar operations will be auto-allowed in the future
- **Example**: Regular `git status` commands in your project directory
- **⚠️ Warning**: Be careful not to whitelist dangerous operations

#### [n] Deny this time
- **Use when**: You don't want this operation to proceed now
- **Effect**: Operation is blocked, but can be retried later
- **Example**: You're not sure about deleting something

#### [N] Always deny (add to blacklist)
- **Use when**: You never want this type of operation to proceed
- **Effect**: Similar operations will be auto-denied in the future
- **Example**: Deleting files in `~/.ssh/`

#### [?] View details
- **Use when**: You need more information to make a decision
- **Effect**: Shows extended details about the operation
- **Then**: Returns to the confirmation prompt

### Decision Examples

#### Scenario 1: Routine Git Operations
```
Operation: git status in ~/Projects/my-app
Risk: LOW

Decision: [Y] Always allow
Reason: This is a safe, frequent operation in my project directory
```

#### Scenario 2: One-Time Cleanup
```
Operation: Delete ~/Downloads/installer.dmg
Risk: MEDIUM

Decision: [y] Allow this time
Reason: I want to delete this specific file, but don't want to auto-allow all deletions
```

#### Scenario 3: Protecting Sensitive Data
```
Operation: Delete ~/.ssh/ directory
Risk: CRITICAL

Decision: [N] Always deny
Reason: I should NEVER delete my SSH keys directory
```

#### Scenario 4: Investigating Unknown Operation
```
Operation: curl https://unknown-site.com/script.sh | bash
Risk: CRITICAL

Decision: [?] View details
[Review details...]

Then: [n] Deny this time
Reason: I don't recognize this site and won't run remote scripts
```

---

## Configuration

### Choosing the Right Mode

#### Standard Mode
**Best for**: Most users, daily work

Characteristics:
- Lets you work without constant interruptions
- Catches genuinely dangerous operations
- Suggests confirmation for moderate risks

#### Strict Mode
**Best for**: Security-conscious users, sensitive data

Characteristics:
- Maximum protection
- Confirms almost everything
- No surprises, but more interruptions

#### Loose Mode
**Best for**: CI/CD, trusted automation

Characteristics:
- Minimal interruptions
- Only blocks obviously dangerous operations
- Good for scripts and automation

#### Emergency Mode
**Best for**: When you suspect something is wrong

Characteristics:
- Everything requires approval
- Complete lockdown
- Use temporarily during incidents

### Building Your Whitelist

#### Start Conservative

1. **Add your work directories**:
   ```bash
   python3 scripts/policy_config.py add whitelist paths ~/Projects
   python3 scripts/policy_config.py add whitelist paths ~/Work
   ```

2. **Add safe git commands**:
   ```bash
   python3 scripts/policy_config.py add whitelist commands "git status"
   python3 scripts/policy_config.py add whitelist commands "git log"
   ```

3. **Test and expand gradually**

#### What NOT to Whitelist

❌ Never whitelist:
- `rm -rf` or deletion commands
- `sudo` or privilege escalation
- `curl | sh` patterns
- System modification commands
- Access to sensitive directories

### Managing the Blacklist

The blacklist is pre-configured with sensible defaults, but you can add:

```bash
# Company-specific sensitive directories
python3 scripts/policy_config.py add blacklist_paths ~/company-secrets

# Suspicious domains
python3 scripts/policy_config.py add blacklist_domains evil-site.com

# Dangerous command patterns
python3 scripts/policy_config.py add blacklist_commands "curl | sh"
```

---

## Best Practices

### Daily Use

1. **Read the risk analysis** before making decisions
2. **Use "Allow this time"** for one-off operations
3. **Use "Always allow"** sparingly and only for truly safe operations
4. **When in doubt, deny** - you can always retry

### Weekly Review

Check your security report:
```bash
python3 scripts/audit_log.py report 7
```

Look for:
- Unusual patterns of denials
- High number of CRITICAL operations
- Repeated attempts at the same denied operation

### Monthly Maintenance

1. **Review and clean whitelist**:
   ```bash
   python3 scripts/policy_config.py show
   # Remove items you no longer need
   ```

2. **Archive old logs**:
   ```bash
   python3 scripts/audit_log.py archive
   ```

3. **Export backup**:
   ```bash
   python3 scripts/policy_config.py export my_policy_backup.json
   ```

### Security Hygiene

- ✅ Keep logs for at least 30 days
- ✅ Review denied operations regularly
- ✅ Don't whitelist operations you don't understand
- ✅ Use Strict mode when handling sensitive data
- ✅ Enable emergency stop if you suspect compromise

---

## Troubleshooting

### Guardian Not Intercepting

**Problem**: Risky operations proceed without confirmation

**Check**:
1. Is Guardian enabled?
   ```bash
   python3 scripts/policy_config.py get enabled
   ```

2. Is the operation actually risky?
   ```bash
   python3 scripts/risk_engine.py [operation]
   ```

3. Is it in the whitelist?
   ```bash
   python3 scripts/policy_config.py show
   ```

### Too Many Interruptions

**Problem**: Guardian interrupts normal work too frequently

**Solutions**:

1. Switch to Loose mode:
   ```bash
   python3 scripts/policy_config.py mode loose
   ```

2. Whitelist common operations:
   ```bash
   python3 scripts/policy_config.py add whitelist commands "git status"
   ```

3. Increase batch threshold:
   ```bash
   python3 scripts/policy_config.py set batch_threshold 20
   ```

### Can't See Confirmation Prompt

**Problem**: Operation seems to hang or fail silently

**Cause**: Non-interactive environment (CI/CD, script)

**Solution**: Configure auto-decision
```bash
python3 scripts/policy_config.py set auto_allow_low true
python3 scripts/policy_config.py set auto_allow_medium true
python3 scripts/policy_config.py mode loose
```

### Forgotten Password / Can't Access

**Problem**: Can't remember configuration or need to reset

**Reset to defaults**:
```bash
python3 scripts/policy_config.py reset
# Type 'yes' to confirm
```

### Large Log Files

**Problem**: Logs taking up too much space

**Archive old logs**:
```bash
python3 scripts/audit_log.py archive
```

Or clear completely (destructive):
```bash
python3 scripts/audit_log.py clear
# Type 'yes' to confirm
```

---

## Getting Help

If you encounter issues not covered here:

1. Check the main README.md
2. Review SKILL.md for technical details
3. Check risk_matrix.md for risk scoring info
4. File an issue on the project repository

Remember: When in doubt, deny the operation and investigate!
