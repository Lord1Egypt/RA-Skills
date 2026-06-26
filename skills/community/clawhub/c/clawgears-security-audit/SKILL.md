---
name: security-audit
description: "Comprehensive OpenClaw security audit — checks gateway binding, credential exposure, channel policies, tool sandboxing, network/IP leaks, and macOS system security (SIP, FileVault, TCC)."
version: 1.0.0
metadata:
  openclaw:
    emoji: "\U0001F512"
    os:
      - macos
      - linux
    homepage: https://github.com/sunt23310-ops/openclaw-security-audit
    requires:
      anyBins:
        - python3
        - python
      bins:
        - bash
        - curl
    install:
      - kind: brew
        formula: python3
        bins:
          - python3
---

# OpenClaw Security Audit

Run a comprehensive security audit on your local OpenClaw installation. Covers 6 security domains mapped to MITRE ATLAS threat categories.

## When to Use

- User asks to "check security", "audit my openclaw", "is my config secure?"
- User mentions concerns about API key leaks, exposed ports, or privacy
- After changing OpenClaw configuration (gateway, channels, tools, etc.)
- User wants a security report (HTML or JSON)

## When NOT to Use

- General system security questions unrelated to OpenClaw
- User is asking about a different application
- User just wants to know what OpenClaw is

## Setup

Check if the audit tool is installed:

```bash
ls ~/openclaw-security-audit/audit.sh 2>/dev/null || echo "NOT_INSTALLED"
```

If not installed, clone it:

```bash
git clone https://github.com/sunt23310-ops/openclaw-security-audit.git ~/openclaw-security-audit
```

## Running Checks

```bash
AUDIT_DIR="$HOME/openclaw-security-audit"
```

### Quick Check (critical items only, ~5 seconds)

```bash
bash "$AUDIT_DIR/checks/gateway.sh" && bash "$AUDIT_DIR/checks/credentials.sh"
```

### Full Audit (all 6 modules)

```bash
for check in gateway credentials channels tools network system; do
  bash "$AUDIT_DIR/checks/${check}.sh"
done
```

### Individual Checks

Match the user's concern to the right module:

| User asks about | Command |
|----------------|---------|
| Gateway, ports, binding, auth, TLS | `bash "$AUDIT_DIR/checks/gateway.sh"` |
| API keys, passwords, file permissions, history leaks | `bash "$AUDIT_DIR/checks/credentials.sh"` |
| WhatsApp, Telegram, DM policy, allowFrom | `bash "$AUDIT_DIR/checks/channels.sh"` |
| Sandbox, denyCommands, tool restrictions | `bash "$AUDIT_DIR/checks/tools.sh"` |
| IP leak, exposed ports, firewall, Shodan/Censys | `bash "$AUDIT_DIR/checks/network.sh"` |
| macOS SIP, FileVault, TCC, iCloud sync | `bash "$AUDIT_DIR/checks/system.sh"` |

### Auto-Fix (requires explicit user confirmation for each fix)

```bash
bash "$AUDIT_DIR/fixes/interactive-fix.sh"
```

Specific fixes:
- `bash "$AUDIT_DIR/fixes/gateway-fix.sh"` — bind gateway to localhost, generate strong token
- `bash "$AUDIT_DIR/fixes/permission-fix.sh"` — fix file/directory permissions
- `bash "$AUDIT_DIR/fixes/channel-fix.sh"` — fix DM policy, allowFrom, requireMention

### Generate Report

```bash
bash "$AUDIT_DIR/audit.sh"
```

Then select option 5 for HTML or JSON report output.

## Output Format

Each check outputs lines prefixed with:
- `[PASS]` — check passed, no action needed
- `[WARN]` — potential issue, review recommended
- `[FAIL]` — security issue found, fix recommended
- `[SKIP]` — check skipped (component not installed or not applicable)

After running checks, summarize results clearly. If there are FAIL items, recommend the appropriate fix script and explain what it will do before the user confirms.

## Important Notes

- This tool is **read-only by default**. Fix scripts require explicit user confirmation for each change.
- The **IP leak check** (network module) will ask before sending your IP to external services (Shodan, Censys).
- All checks gracefully skip if OpenClaw is not installed or a component is missing.
- On Linux, macOS-specific checks (SIP, FileVault, TCC) are automatically skipped.
