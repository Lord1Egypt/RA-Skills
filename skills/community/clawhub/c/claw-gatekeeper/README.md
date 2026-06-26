# 🛡️ Claw Gatekeeper

> A Safety Brake for OpenClaw - OpenClaw Guardian with Session-Aware Risk Management

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![English](https://img.shields.io/badge/Language-English-blue.svg)](README.md)
[![中文](https://img.shields.io/badge/语言-中文-red.svg)](README.zh-CN.md)

**[English](README.md) | [中文](README.zh-CN.md)**

---

## ⚠️ Important Notice

**This is a temporary security measure.**

OpenClaw Guardian was created to address current security gaps in OpenClaw's autonomous decision-making capabilities. Once OpenClaw implements comprehensive built-in safety controls, this project may be discontinued.

**Current Status**: OpenClaw (as of March 2026) has been identified with significant security concerns including multiple CVEs and warnings from national security agencies. Use this skill to add a layer of protection until official security improvements are released.

---

## 🎯 What is Claw-Gatekeeper?

OpenClaw Guardian is a **persistent security layer** for OpenClaw that intercepts potentially dangerous operations and manages them according to their risk level, with intelligent session-aware approval.

### Risk-Based Behavior

| Risk Level | Score | Default Behavior | Session Approval |
|------------|-------|------------------|------------------|
| 🔴 **CRITICAL** | 80-100 | Always requires individual confirmation | ❌ Not available |
| 🟠 **HIGH** | 60-79 | Confirm first, can approve for session | ✅ Available |
| 🟡 **MEDIUM** | 30-59 | Confirm first, can approve for session | ✅ Available |
| 🟢 **LOW** | 0-29 | Auto-allowed without interruption | N/A |

### Session-Aware Approval

**The Key Innovation**: After confirming a MEDIUM or HIGH risk operation once, you can choose to **approve it for the entire session**. Similar operations will be auto-approved until:
- The session expires (30 minutes of inactivity)
- You explicitly revoke the approval
- OpenClaw restarts

**CRITICAL operations always require individual confirmation** - no session approval for maximum safety.

---

## 📦 Installation

### For Humans

Copy and paste this prompt to your LLM agent (Claude Code, Cursor, Cline, etc.):

```
Install and configure OpenClaw Guardian by following the instructions here: https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.md  Make it a persistent skill and set it to standard mode.Or read the rest of this README, but seriously, let an agent do it. Humans fat-finger configs.
```

### For LLM Agents

Fetch and execute the installation:

```bash
# Download and install
curl -L -o claw-gatekeeper.skill https://github.com/stephenlzc/claw-gatekeeper/releases/latest/download/claw-guardian.skill
openclaw skill install claw-guardian.skill
openclaw skill persist claw-guardian

# Initialize configuration
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode standard
```

### Skip This README

We're past the era of reading docs. Just paste this into your agent:

> Read this and set up Claw-Guardian as a persistent security layer for OpenClaw:  
> https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.md

---

## 🚀 Quick Start

### Basic Usage

Once installed as a persistent skill, Claw-Guardian automatically manages operations:

```
[OpenClaw] I'll delete the old temp files

[Claw-Guardian] 🟡 MEDIUM RISK
============================================================
📋 Operation: 📁 File Operation
📝 Detail: delete ~/temp/ (45 files)
🟡 Risk Level: MEDIUM
📊 Risk Score: 45/100

⚠️ Risk Analysis:
   1. Batch operation (45 files)
   2. Directory deletion

SELECT AN OPTION:
   [y] ✅ Allow this time only
   [s] ✅📅 Allow for this session ⭐
   [Y] ✅✅ Always allow (whitelist)
   [n] ❌ Deny this time
   [N] ❌❌ Always deny (blacklist)

Your choice: s

✅ Approved for this session
📌 Similar operations will be auto-approved
```

Subsequent similar operations:
```
[OpenClaw] Delete more temp files

[Claw-Guardian] 🟡 MEDIUM RISK - Session approved ✅
           Auto-allowed (no prompt)
```

### Viewing Session Status

```bash
# Check current session
python3 ~/.claw-gatekeeper/scripts/guardian_ui.py session

# View active approvals
python3 ~/.claw-gatekeeper/scripts/session_manager.py list

# View audit log
python3 ~/.claw-gatekeeper/scripts/session_manager.py check --lines 50
```

---

## 📝 Operate_Audit.log

All MEDIUM and above operations are logged to `~/.claw-guardian/sessions/Operate_Audit.log`:

```
[2026-03-12 14:30:25.123] [🟠 HIGH] [skill] allow_session: data-processor from github
[2026-03-12 14:31:10.456] [🟡 MEDIUM] [file] allow_session: delete ~/temp/cache
[2026-03-12 14:32:05.789] [🔴 CRITICAL] [shell] allow_once: rm -rf ~/Projects/test
[2026-03-12 14:35:15.234] [🟠 HIGH] [skill] deny_once: suspicious-tool from unknown
```

### Log Format

```
[TIMESTAMP] [EMOJI RISK_LEVEL] [OPERATION_TYPE] DECISION: Operation details
```

### Viewing Logs

```bash
# Recent entries
python3 ~/.claw-gatekeeper/scripts/session_manager.py check --lines 100

# Export to file
python3 ~/.claw-gatekeeper/scripts/session_manager.py check --lines 1000 > audit.txt
```

---

## ⚙️ Configuration

### Operation Modes

```bash
# Standard mode (recommended)
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode standard

# Strict mode (maximum security)
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode strict

# Loose mode (minimal interruptions)
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode loose

# Emergency mode (everything requires confirmation)
python3 ~/.claw-gatekeeper/scripts/policy_config.py mode emergency
```

### Managing Session Timeout

Default: 30 minutes of inactivity

To change, edit `~/.claw-guardian/config.json`:
```json
{
  "session_timeout": 3600
}
```

### Whitelist Management

```bash
# Add trusted paths
python3 ~/.claw-gatekeeper/scripts/policy_config.py add whitelist paths ~/Projects

# Add trusted commands
python3 ~/.claw-gatekeeper/scripts/policy_config.py add whitelist commands "git status"

# Add trusted skills
python3 ~/.claw-gatekeeper/scripts/policy_config.py add whitelist skills docx
```

---

## 🔐 Security Hardening

For users who require maximum security (e.g., handling sensitive data, compliance requirements), Guardian provides a **zero-code-change hardening mode** that enables human-in-the-loop approval for ALL operations.

### Quick Hardening (One Command)

```bash
# Deploy maximum security mode
cd ~/.claw-gatekeeper/scripts
./deploy-secure.sh --apply
```

This applies:
- ✅ **100% human confirmation** - All operations require approval
- ✅ **Enhanced blacklist** - 20+ dangerous command patterns
- ✅ **Sensitive directory protection** - SSH, AWS, K8s configs protected
- ✅ **Secure audit logging** - 30-day retention with proper permissions
- ✅ **Strict mode** - Maximum security policy

### Security Modes Comparison

| Mode | LOW Risk | MEDIUM Risk | HIGH Risk | CRITICAL Risk |
|------|----------|-------------|-----------|---------------|
| **Default** | Auto-allow | Confirm | Confirm | Confirm |
| **Hardened** | **Confirm** | **Confirm** | **Confirm** | Confirm |

### Data Sanitization (Optional)

Pre-process content to remove sensitive data before Guardian analysis:

```bash
# Check for sensitive patterns
./scripts/sanitizer.sh --check session.json --verbose

# Sanitize file
./scripts/sanitizer.sh --file conversation.txt > clean.txt

# Pipe usage
cat log.txt | ./scripts/sanitizer.sh --stdin
```

**Detected patterns**: Passwords, API keys, tokens, cloud credentials, crypto wallets, PII, certificates.

### Restore Default Mode

```bash
./deploy-secure.sh --restore
```

### Security Documentation

See [SECURITY.md](SECURITY.md) for detailed hardening guide.

---

## 📁 Project Structure

```
claw-guardian/
├── README.md                    # This file
├── README.zh-CN.md              # Chinese documentation
├── SKILL.md                     # Skill documentation
├── scripts/
│   ├── risk_engine.py          # Risk assessment engine
│   ├── guardian_ui.py          # User interaction + session logic
│   ├── session_manager.py      # Session state management
│   ├── policy_config.py        # Policy configuration
│   └── audit_log.py            # Audit trail management
└── references/
    ├── risk_matrix.md          # Risk scoring reference
    └── user_guide.md           # Detailed user guide
```

### Important Files

- **Config**: `~/.claw-guardian/config.json`
- **Session State**: `~/.claw-guardian/sessions/current_session.json`
- **Audit Log**: `~/.claw-guardian/sessions/Operate_Audit.log`
- **Backups**: `~/.claw-guardian/backups/`

---

## 🔒 Security Context

### Why Session-Level Approval?

Traditional security tools interrupt every risky operation, causing:
- **Workflow disruption** - Constant prompts during development
- **Alert fatigue** - Users start ignoring warnings
- **Workarounds** - Users whitelist everything to avoid interruptions

**Session-level approval provides:**
- ✅ **Security**: First operation always confirmed
- ✅ **Convenience**: Similar operations auto-approved for the session
- ✅ **Control**: Session expires after inactivity
- ✅ **Audit**: Everything logged to Operate_Audit.log

### CRITICAL vs Session Approval

**CRITICAL risks (80-100)** - No session approval:
- `rm -rf /` or system directories
- Disk formatting
- Credential access
- System configuration changes

**MEDIUM/HIGH risks (30-79)** - Session approval available:
- File deletions in user directories
- Skill installations
- Network requests
- Shell commands

---

## 🔗 Quick Links

- **Repository**: https://github.com/stephenlzc/claw-gatekeeper
- **Releases**: https://github.com/stephenlzc/claw-gatekeeper/releases
- **Issues**: https://github.com/stephenlzc/claw-gatekeeper/issues
- **Raw README**: https://raw.githubusercontent.com/stephenlzc/claw-gatekeeper/main/README.md

---

## 🤝 Contributing

Contributions welcome in:
- Additional risk patterns
- Session management improvements
- Documentation
- Security enhancements

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

<div align="center">

**OpenClaw Guardian** - Secure by Design, Convenient by Default 🛡️

*Trust, but verify. Then verify again for CRITICAL.*

[English](README.md) | [中文](README.zh-CN.md)

</div>
