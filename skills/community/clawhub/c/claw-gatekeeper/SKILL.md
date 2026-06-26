---
name: claw-gatekeeper
description: |
  OpenClaw Guardian is a comprehensive security control system for OpenClaw that intercepts 
  high-risk operations and requires human confirmation before execution. It acts as a 
  "safety brake" with session-level auto-approval for MEDIUM/HIGH risks after initial 
  user confirmation.
  
  **Key Behaviors:**
  - LOW risk: Auto-allowed without confirmation
  - MEDIUM/HIGH risk: User confirmation with option to approve for entire session
  - CRITICAL risk: Must confirm each time individually (no session approval)
  - Logs all MEDIUM+ operations to Operate_Audit.log with timestamps
  
  Use when: limiting OpenClaw's autonomous permissions, preventing accidental data 
  deletion, controlling skill installations, monitoring file operations.
  
  **Note:** This skill should be loaded as a persistent/resident skill in OpenClaw.
---

# 🛡️ OpenClaw Guardian

> The Safety Brake for OpenClaw - Session-aware protection for risky operations

## Overview

Claw-Gatekeeper is a comprehensive security control layer for OpenClaw that intercepts potentially dangerous operations and manages them according to their risk level:

| Risk Level | Score | Behavior | Session Approval |
|------------|-------|----------|------------------|
| 🔴 **CRITICAL** | 80-100 | Always requires confirmation | ❌ Not available |
| 🟠 **HIGH** | 60-79 | Requires confirmation, can approve for session | ✅ Available |
| 🟡 **MEDIUM** | 30-59 | Suggests confirmation, can approve for session | ✅ Available |
| 🟢 **LOW** | 0-29 | Auto-allowed without confirmation | N/A |

### Key Features

- 🛑 **Smart Interception** - Automatically catches risky operations
- 📅 **Session-Level Approval** - Approve MEDIUM/HIGH once, auto-approve similar operations for the session
- 🔒 **CRITICAL Protection** - Must confirm each CRITICAL operation individually
- 📝 **Audit Trail** - All MEDIUM+ operations logged to `Operate_Audit.log`
- ⚙️ **Persistent Operation** - Designed to be loaded as a resident skill

## Risk Level Behaviors

### 🔴 CRITICAL (80-100) - Always Confirm

**Examples:**
- `rm -rf /` or system directory deletion
- Disk formatting (`mkfs`, `format`)
- System configuration changes
- Access to `/etc/shadow`, root SSH keys

**Behavior:**
- ❌ **Must confirm EACH time individually**
- ❌ No session-level approval available
- ❌ No auto-approval
- ✅ Complete audit logging

```
[OpenClaw] rm -rf ~/Projects/important

[Claw-Guardian] 🔴 CRITICAL RISK
⚠️  About to recursively delete directory with 1,247 files

Options:
  [y] ✅ Allow this time (will ask again next time)
  [Y] ✅✅ Always allow (add to whitelist)
  [n] ❌ Deny this time
  [N] ❌❌ Always deny (add to blacklist)

Note: Session approval NOT available for CRITICAL risks
```

### 🟠 HIGH (60-79) - Confirm or Session Approve

**Examples:**
- Deleting directories with many files
- Executing shell commands
- Installing skills from external sources
- Network requests to external domains

**Behavior:**
- ✅ Requires confirmation (first time)
- ✅ **Can approve for entire session**
- ✅ Session expires after 30min inactivity
- ✅ Complete audit logging

```
[OpenClaw] Installing skill from GitHub

[Claw-Guardian] 🟠 HIGH RISK
⚠️  Installing 'data-processor' from GitHub

Options:
  [y] ✅ Allow this time only
  [s] ✅📅 Allow for this session ⭐ RECOMMENDED
  [Y] ✅✅ Always allow (whitelist)
  [n] ❌ Deny this time
  [N] ❌❌ Always deny (blacklist)

User selects: [s]

✅ Operation approved for this session
📌 Similar HIGH risk operations will be auto-approved
⏱️  Session expires after 30 minutes of inactivity
```

### 🟡 MEDIUM (30-59) - Suggest Confirm or Session Approve

**Examples:**
- Creating new files
- Batch file operations (5-20 files)
- Reading sensitive directories
- Modifying configuration files

**Behavior:**
- ✅ Suggests confirmation
- ✅ **Can approve for entire session**
- ✅ Auto-allowed in loose mode
- ✅ Complete audit logging

### 🟢 LOW (0-29) - Auto-Allow

**Examples:**
- Reading files
- Listing directories
- Whitelisted operations
- Safe read-only commands

**Behavior:**
- ✅ **Auto-allowed without confirmation**
- ✅ No interruption to workflow
- ✅ Still logged if enabled

## Installation

### Prerequisites

Claw-Guardian is designed to be a **persistent/resident skill** in OpenClaw. It should be loaded at the start of every session.

### Method 1: OpenClaw CLI (Recommended)

```bash
# Install the skill
openclaw skill install claw-gatekeeper

# Add to persistent skills (so it loads every session)
openclaw skill persist claw-guardian
```

### Method 2: Manual Installation

```bash
# Copy skill package
cp claw-guardian.skill ~/.openclaw/skills/

# Add to autoload
openclaw skill load claw-guardian --persist
```

### Method 3: Configuration File

Add to `~/.openclaw/config.json`:

```json
{
  "persistent_skills": [
    "claw-guardian"
  ]
}
```

## Quick Start

### 1. Initialize Configuration

```bash
# Initialize with default settings
python3 ~/.claw-gatekeeper/scripts/policy_config.py show
```

### 2. Set Operation Mode

```bash
# Standard mode (recommended)
python3 scripts/policy_config.py mode standard

# Or strict mode for maximum security
python3 scripts/policy_config.py mode strict
```

### 3. Verify Installation

```bash
# Test risk assessment
python3 scripts/risk_engine.py file delete ~/test-file.txt
```

### 4. Check Session Status

```bash
# View current session info
python3 scripts/guardian_ui.py session

# View Operate_Audit.log
python3 scripts/session_manager.py check --lines 50
```

## Session Management

### How Session Approval Works

```
First Operation (MEDIUM/HIGH):
  [OpenClaw] Delete ~/temp/old-files/
  [Guardian] 🟡 MEDIUM RISK - Requires confirmation
             Options: [y] once, [s] session, [Y] always, [n] deny
  
  User: [s] Allow for this session
  
  ✅ Operation approved
  📌 Session approval granted

Similar Operations (same session):
  [OpenClaw] Delete ~/temp/more-files/
  [Guardian] 🟡 MEDIUM RISK - Session approved
             Auto-allowed (similar to previous approval)
  
  ✅ Auto-approved (no prompt)
```

### Session Expiration

- **Default timeout:** 30 minutes of inactivity
- **Activity:** Any operation or confirmation resets the timer
- **Persistence:** Session state saved between OpenClaw interactions

### Managing Session Approvals

```bash
# View current session
python3 scripts/guardian_ui.py session

# View active approvals
python3 scripts/session_manager.py list

# Revoke specific approvals
python3 scripts/session_manager.py revoke --type file --risk HIGH

# Clear entire session
python3 scripts/session_manager.py clear
```

## Configuration

### Operation Modes

#### Standard Mode (Recommended)
```bash
python3 scripts/policy_config.py mode standard
```
- CRITICAL: Always confirm (no session)
- HIGH: Confirm or session approve
- MEDIUM: Suggest confirm or session approve
- LOW: Auto-allow

#### Strict Mode
```bash
python3 scripts/policy_config.py mode strict
```
- All non-whitelisted operations require confirmation
- Session approval still available for MEDIUM/HIGH
- CRITICAL always per-confirmation

#### Loose Mode
```bash
python3 scripts/policy_config.py mode loose
```
- Only CRITICAL requires confirmation
- MEDIUM/HIGH auto-allowed after first session approval
- LOW always auto-allowed

#### Emergency Mode
```bash
python3 scripts/policy_config.py mode emergency
```
- Completely disables autonomous operations
- Everything requires confirmation
- Session approvals suspended

### Managing Whitelists and Blacklists

```bash
# Add trusted paths
python3 scripts/policy_config.py add whitelist paths ~/Projects

# Add trusted commands
python3 scripts/policy_config.py add whitelist commands "git status"

# Add trusted skills
python3 scripts/policy_config.py add whitelist skills docx

# Block sensitive paths
python3 scripts/policy_config.py add blacklist paths ~/.ssh
```

## Audit Logging

### Operate_Audit.log

All MEDIUM and above operations are logged to `~/.claw-guardian/sessions/Operate_Audit.log`:

```
[2026-03-12 14:30:25.123] [🟠 HIGH] [skill] allow_session: Installing data-processor@1.0.0 from github
[2026-03-12 14:31:10.456] [MEDIUM] [file] allow_session: delete ~/temp/cache (session approved)
[2026-03-12 14:32:05.789] [CRITICAL] [shell] allow_once: rm -rf ~/Projects/test (manual confirm)
[2026-03-12 14:35:15.234] [HIGH] [skill] deny_once: Installing suspicious-tool from unknown
```

### Viewing Logs

```bash
# View recent entries
python3 scripts/session_manager.py check --lines 100

# Export to file
python3 scripts/session_manager.py check --lines 1000 > audit_export.txt

# Query with filters
python3 scripts/audit_log.py query 7 --risk HIGH --decision allow_session
```

### Log Format

```
[TIMESTAMP] [RISK_LEVEL] [OPERATION_TYPE] DECISION: Details

Example:
[2026-03-12 14:30:25.123] [🟠 HIGH] [skill] allow_session: data-processor from github
```

## Usage Examples

### Example 1: File Cleanup with Session Approval

```
[OpenClaw] I'll clean up the temp directory

[Guardian] 🟡 MEDIUM RISK
           Operation: delete ~/temp/ (50 files)
           
           [y] once  [s] session ⭐  [Y] always  [n] deny  [N] always deny

User: [s] Allow for this session

✅ Approved for session
📌 Similar deletions will be auto-approved

[OpenClaw] Delete ~/cache/ (30 files)
[Guardian] 🟡 MEDIUM RISK - Session approved ✅
           Auto-allowed

[OpenClaw] Delete ~/.ssh/ 
[Guardian] 🔴 CRITICAL RISK
           [y] once  [Y] always  [n] deny  [N] always deny
           (Session approval NOT available)
```

### Example 2: Skill Development Workflow

```
[OpenClaw] Testing my skill, need to install from local

[Guardian] 🟠 HIGH RISK
           Installing 'my-skill' from local
           
           [y] once  [s] session ⭐  [Y] always  [n] deny

User: [s] Allow for this session

✅ Session approved for skill development

[Repeated testing...]
[Guardian] Auto-approving local skill installations (session active)
```

### Example 3: CRITICAL Operation Always Confirms

```
[OpenClaw] rm -rf ~/Projects/legacy-app/

[Guardian] 🔴 CRITICAL RISK
           Recursive deletion of 1,247 files including .git
           
           [y] allow ONCE  [Y] always  [n] deny  [N] always deny
           
           ⚠️  Session approval NOT available for CRITICAL

User: [y] Allow this time

✅ Approved (will ask again for next CRITICAL)
```

## Script Reference

### Session Management

```bash
# View session info
python3 scripts/guardian_ui.py session

# Check if operation is allowed (no interaction)
python3 scripts/guardian_ui.py check '{"operation_type":"file",...}'

# Interactive confirmation
python3 scripts/guardian_ui.py interactive '{"operation_type":"file",...}'
```

### Session Manager Direct

```bash
# List session approvals
python3 scripts/session_manager.py list

# Revoke approvals
python3 scripts/session_manager.py revoke --type file --risk MEDIUM

# Clear session
python3 scripts/session_manager.py clear

# View Operate_Audit.log
python3 scripts/session_manager.py check --lines 50
```

### Risk Assessment

```bash
# Assess file operation
python3 scripts/risk_engine.py file delete ~/test.txt

# Assess shell command
python3 scripts/risk_engine.py shell "rm -rf /tmp/*"

# Assess network request
python3 scripts/risk_engine.py network https://api.example.com POST

# Assess skill installation
python3 scripts/risk_engine.py skill my-skill github
```

## Best Practices

### For Personal Use

1. **Use session approval for development work**
   - Approve temp file deletions for session
   - Approve git operations for session
   - Approve skill testing for session

2. **Never session-approve CRITICAL risks**
   - Always review each CRITICAL operation
   - CRITICAL = potential data loss or system damage

3. **Review Operate_Audit.log weekly**
   ```bash
   python3 scripts/session_manager.py check --lines 100
   ```

### For Team/Enterprise

1. **Standard mode for most users**
2. **Strict mode for production systems**
3. **Regular audit log reviews**
4. **Document session approval policies**

## Troubleshooting

### Session Not Persisting

**Problem:** Session approvals lost between interactions

**Solution:** Ensure skill is loaded as persistent:
```bash
openclaw skill list --persistent
# If not listed:
openclaw skill persist claw-guardian
```

### Too Many CRITICAL Prompts

**Problem:** Every CRITICAL operation requires confirmation

**This is by design.** CRITICAL risks must always be confirmed individually. Consider:
- Whitelisting safe operations
- Reviewing why operations are marked CRITICAL
- Using less destructive alternatives

### Session Timeout Too Short

**Problem:** Session expires during work

**Solution:** Adjust timeout (requires config edit):
```python
# In ~/.claw-guardian/config.json
{
  "session_timeout": 3600  # 1 hour in seconds
}
```

## Project Status

**This is a temporary security measure.**

Claw-Guardian addresses current security gaps in OpenClaw. Once OpenClaw implements comprehensive built-in safety controls, this project may be deprecated.

---

**Claw-Guardian** - Making OpenClaw Safer, One Session at a Time 🛡️
