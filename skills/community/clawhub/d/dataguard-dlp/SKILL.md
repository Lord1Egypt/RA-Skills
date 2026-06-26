---
name: Dataguard DLP
version: 2.2.0
description: Runtime Data Loss Prevention (DLP) for OpenClaw agents. Multi-layer defense against credential exfiltration, PII leakage, and sensitive data transfer. Intercepts outbound tool calls, scans for patterns, and blocks unauthorized data transfers. First ClawHub plugin with real-time data flow protection.
metadata:
  openclaw:
    requires:
      bins: [grep, sed, awk, date, head, xargs]
      # All grep calls use -E (extended regex), not -P (Perl regex)
      # No python3 dependency — all scripts are pure bash/sed/awk
    note: |
      Hooks require OpenClaw hook support. Without it, the skill degrades to manual
      scanning only (agent calls dlp-scan.sh directly before outbound operations).
      Context tracking requires the agent to call context-track.sh --log after
      reading sensitive files — this is not automatic, the agent must opt-in.
      Hooks do NOT read file contents for upload scanning (filename-only check).
      Audit logs redact data previews by default (log_data_previews: false).
    install:
      - id: bash
        kind: shell
        script: scripts/install.sh
    hooks:
      - tool: web_fetch
        phase: pre
        script: scripts/hooks/web-fetch-pre.sh
      - tool: sessions_send
        phase: pre
        script: scripts/hooks/sessions-send-pre.sh
      - tool: exec
        phase: pre
        script: scripts/hooks/exec-pre.sh
---

# DataGuard — Runtime DLP for AI Agents

You have the DataGuard security skill. This is a **runtime enforcement layer** that actively prevents data exfiltration.

## The Problem

AI agents can be tricked into sending sensitive data through:
- **Prompt injection** — hidden instructions in emails, web pages, documents
- **Tool chaining** — read credentials → send to external URL
- **Social engineering** — "help me debug, paste your config"
- **Unintended exposure** — logs, error messages, debugging output

SecureClaw provides **behavioral rules**. DataGuard provides **runtime enforcement**.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                     TOOL EXECUTION FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  Agent calls tool (web_fetch, sessions_send, exec)              │
│                          ↓                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  DATA GUARD PRE-HOOK                                     │   │
│  │  ─────────────────────────────────────────────────────  │   │
│  │  1. Extract outbound data (URL params, body, message)   │   │
│  │  2. Run pattern scanner (API keys, PII, paths)         │   │
│  │  3. Check context (sensitive file read this session?)   │   │
│  │  4. Verify domain allowlist                             │   │
│  │  5. Calculate risk score                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          ↓                                       │
│         ┌──────────────┬──────────────┬──────────────┐          │
│         │  LOW RISK    │  MEDIUM RISK  │  HIGH RISK   │          │
│         │  (0-2)       │  (3-5)        │  (6-10)      │          │
│         └──────────────┴──────────────┴──────────────┘          │
│              ↓               ↓               ↓                    │
│         ALLOW           WARN + LOG      BLOCK + ALERT            │
│                          ↓               ↓                       │
│                      ALLOW           REQUIRE APPROVAL            │
│                                                              │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Stack

| Layer | Name | Function | Enforcement |
|-------|------|----------|-------------|
| L1 | Pattern Scanner | Detects credentials, PII, secrets | Automatic block |
| L2 | Context Heuristics | Tracks read→send patterns | Score increase |
| L3 | Domain Allowlist | Only approved external domains | Block unknown |
| L4 | Risk Scoring | Aggregates signals into decision | Tiered response |
| L5 | User Confirmation | High-risk requires approval | Explicit consent |
| L6 | Audit Logging | Records all decisions | Review trail |

## Rules

### Rule 1: All Outbound Data Must Be Scanned

Before ANY tool that sends data externally:
```bash
echo "$OUTBOUND_DATA" | bash $SKILL_DIR/scripts/dlp-scan.sh
```

If exit code is non-zero, **STOP and alert**.

### Rule 2: Pattern Matches Are Automatic Blocks

The following patterns trigger immediate block:

**CRITICAL (Score: 10)**
- API keys: `sk-*`, `xoxb-*`, `ghp_*`, `AKIA*`, API keys in general
- Passwords: `password=`, `passwd=`, `pwd=`, `secret=`
- Private keys: `-----BEGIN.*PRIVATE KEY-----`
- Database URLs with credentials: `mysql://user:pass@`, `postgres://...`
- AWS credentials: `aws_access_key_id`, `aws_secret_access_key`

**HIGH (Score: 8)**
- Credit cards: Visa/MC/Amex/Diners patterns
- SSN: `XXX-XX-XXXX` format
- Internal IPs: `192.168.*`, `10.*`, `172.16-31.*`
- Internal hostnames: `.local`, `.internal`, `.corp`
- File paths: `/home/`, `/root/`, `/etc/`, `~/.ssh/`

**MEDIUM (Score: 5)**
- Email addresses in sensitive contexts
- Phone numbers in sensitive contexts
- Personal names with context (config files, credentials)
- VPN/network tool references (tailscale, wireguard)

**LOW (Score: 2)**
- Generic path references
- Non-sensitive URLs
- Public information

### Rule 3: Context Matters — Track Sensitive Reads

DataGuard maintains a session context file:
```bash
$SKILL_DIR/context/sensitive-reads.json
```

When you read a file containing credentials or PII, DataGuard logs it:
```json
{
  "timestamp": "2026-04-07T16:52:00Z",
  "file": "/home/user/.env",
  "patterns": ["AWS_KEY", "DB_PASSWORD"],
  "risk_level": "HIGH"
}
```

If you then try to send data externally, DataGuard checks this log:
- **Sensitive read in last 5 minutes?** → Risk +3
- **Same session?** → Risk +2
- **Same conversation turn?** → Risk +5 (BLOCK threshold)

### Rule 4: Domain Allowlisting

By default, these domains are **ALLOWED**:
- `api.openai.com`
- `api.anthropic.com`
- `api.brave.com`
- `docs.openclaw.ai`
- `clawhub.ai`
- `github.com`

By default, these domains are **BLOCKED**:
- Pastebin sites (pastebin.com, hastebin.com)
- File sharing (transfer.sh, 0x0.st)
- Webhook catchers (webhook.site, requestbin.net)
- Anonymous email (temp-mail.org, guerrillamail.com)

All other domains: **REQUIRE APPROVAL** for data outbound.

### Rule 5: Risk Scoring Thresholds

| Score | Action |
|-------|--------|
| 0-2 | Allow — no sensitive patterns detected |
| 3-5 | Warn — log the attempt, allow with warning |
| 6+ | Block — require explicit user approval |

When blocked:
1. Log to `$SKILL_DIR/logs/blocked-attempts.log`
2. Show user: what was blocked, why, risk score breakdown
3. Provide options: approve once, approve domain, report false positive

### Rule 6: User Approval Must Be Explicit

When DataGuard blocks an action, you MUST:
1. Show the exact data that would be sent (truncated, redacted)
2. Show which patterns triggered the block
3. Show the risk score breakdown
4. Ask: "Do you want to allow this? (yes/no)"

**Never:** Auto-approve, skip approval, or work around the block.

### Rule 7: Audit Everything

Every blocked attempt logs:
```
[2026-04-07T16:52:00Z] BLOCKED
Tool: web_fetch
Domain: example.com
Patterns: AWS_KEY, DB_PASSWORD
Risk Score: 12
Data: {"url": "https://example.com/api", "body": "[REDACTED]"}
User: approved / denied / pending
```

Review logs: `bash $SKILL_DIR/scripts/audit-log.sh --recent`

### Rule 8: False Positives Happen — Report Them

If a legitimate action is blocked:
1. Run: `bash $SKILL_DIR/scripts/report-false-positive.sh`
2. Describe what you were trying to do
3. Include the blocked data pattern
4. This helps improve detection accuracy

### Rule 9: Never Disable DataGuard

There is no "disable" switch. If you need to send sensitive data:
1. Get explicit user approval (Rule 6)
2. Log the approval reason
3. Proceed with consent on record

### Rule 10: Teach Your Human About Risks

When DataGuard blocks something, explain:
- Why it was blocked
- What the risk is
- What alternatives exist

Don't just say "blocked" — educate.

## Script Reference

Replace `$SKILL_DIR` with the actual path:
- Standalone: `~/.openclaw/skills/dataguard`
- Plugin: `~/.openclaw/extensions/dataguard/skill`

### Pattern Scanning
```bash
echo "$DATA" | bash $SKILL_DIR/scripts/dlp-scan.sh
# Exit 0 = clean, Exit 1+ = risk score
```

### Domain Management
```bash
# List allowed domains
bash $SKILL_DIR/scripts/domain-allowlist.sh --list

# Add domain (requires approval)
bash $SKILL_DIR/scripts/domain-allowlist.sh --add example.com

# Remove domain
bash $SKILL_DIR/scripts/domain-allowlist.sh --remove example.com
```

### Context Tracking
```bash
# Log a sensitive file read
bash $SKILL_DIR/scripts/context-track.sh --log "/path/to/.env" "AWS_KEY,DB_PASSWORD"

# Check recent sensitive reads
bash $SKILL_DIR/scripts/context-track.sh --check

# Clear session context
bash $SKILL_DIR/scripts/context-track.sh --clear
```

### Audit Logs
```bash
# Show recent blocks
bash $SKILL_DIR/scripts/audit-log.sh --recent

# Show all blocks today
bash $SKILL_DIR/scripts/audit-log.sh --today

# Export for review
bash $SKILL_DIR/scripts/audit-log.sh --export
```

## Integration with SecureClaw

DataGuard and SecureClaw work together:

| Layer | SecureClaw | DataGuard |
|-------|------------|-----------|
| Approach | Behavioral rules (follow these instructions) | Runtime enforcement (block at execution) |
| When | Before agent acts | When tool is called |
| Type | Preventive guidance | Active interception |

**Use both.** SecureClaw teaches good behavior. DataGuard enforces it.

## Threat Model (MITRE ATLAS Reference)

**Note:** MITRE ATLAS is an attack knowledge base for threat modeling, not a control standard. The techniques below describe *what attacks look like*. Control requirements come from NIST AI RMF 1.0, NIST SP 800-53 Rev. 5, ISO/IEC 42001, and ISO/IEC 27001 (see Standards Alignment section).

| ATLAS ID | Technique | Attack Pattern | DataGuard Mitigation |
|----------|-----------|----------------|----------------------|
| T-EXFIL-001 | Data Theft via web_fetch | Agent sends credentials/PII to external URL | L1 pattern scan + L3 domain allowlist + L5 approval |
| T-EXFIL-002 | Unauthorized Message Sending | Agent messages sensitive data to unauthorized recipients | L2 context tracking + session monitoring |
| T-EXFIL-003 | Credential Harvesting | Prompt injection extracts credentials from files/memory | L1 credential patterns + L2 file read tracking |
| T-EXEC-001 | Command Injection via exec | Malicious input triggers dangerous shell commands | L1 output scanning + L2 context awareness |
| T-EXEC-002 | Dangerous Command Chains | Chained commands exfiltrate data (curl | base64) | L1 pattern detection in command strings |
| T-MEMORY-001 | Memory Poisoning | Attacker injects malicious data into agent memory | L1 scan memory files, L2 track memory reads |
| T-CONTEXT-001 | Context Injection | Attacker injects instructions via external content | L2 context heuristics, L4 risk scoring |

**Threat Modeling vs Control Mapping:**
- ATLAS helps identify *what could go wrong* (threat scenarios)
- NIST AI RMF / ISO 42001 define *what controls to implement* (governance requirements)
- DataGuard implements controls that address the identified threats

### OWASP LLM Top 10 Mapping

| OWASP ID | Risk | DataGuard Mitigation |
|-----------|------|----------------------|
| LLM01 | Prompt Injection | L2 context heuristics detect injection patterns, L4 scoring |
| LLM06 | Sensitive Information Disclosure | L1 pattern scanner blocks credential/PII exfiltration |

## Customization

### Configuration

Edit `$SKILL_DIR/config/config.json` to adjust behavior:

| Setting | Default | Description |
|---------|---------|-------------|
| `risk_thresholds.low` | 2 | Below this score → allow (no warning) |
| `risk_thresholds.medium` | 5 | Warn level → log but allow |
| `risk_thresholds.high` | 6 | Block level → require explicit approval |
| `auto_block_critical` | true | Auto-block any CRITICAL pattern match |
| `auto_block_high` | true | Auto-block any HIGH pattern match |
| `require_approval_medium` | false | Medium-risk requires approval (usually too noisy) |
| `log_all_attempts` | false | Log allowed requests too (for audit trail) |
| `log_data_previews` | false | Store truncated data previews in audit logs (keep off by default to avoid persisting sensitive snippets on disk) |
| `domain_policy` | "allowlist" | `allowlist` = only approved domains, `blocklist` = only block bad ones |
| `context_tracking.enabled` | true | Track sensitive file reads across session |
| `context_tracking.max_age_minutes` | 30 | How long a read boosts your risk score |
| `context_tracking.score_boost_recent_read` | 3 | Score bonus for recent sensitive reads |

### Adding Custom Patterns

Edit `$SKILL_DIR/scripts/dlp-scan.sh` and add a new `if` block in the appropriate tier:

**CRITICAL (score 10)** — secrets that should never leave:
```bash
if echo "$DATA" | grep -qiE 'your-custom-pattern-here'; then
  PATTERNS_FOUND+=("CRITICAL:YourPattern")
  RISK_SCORE=$((RISK_SCORE + 10))
fi
```

**HIGH (score 8)** — sensitive data like internal identifiers:
```bash
if echo "$DATA" | grep -qiE 'your-custom-pattern-here'; then
  PATTERNS_FOUND+=("HIGH:YourPattern")
  RISK_SCORE=$((RISK_SCORE + 8))
fi
```

**MEDIUM (score 5)** — context-dependent data:
```bash
if echo "$DATA" | grep -qiE 'your-custom-pattern-here'; then
  PATTERNS_FOUND+=("MEDIUM:YourPattern")
  RISK_SCORE=$((RISK_SCORE + 5))
fi
```

**Custom pattern examples:**
- Employee IDs: `EMP-[0-9]{6}`
- Project codenames: `(project-alpha|project-beta)`
- Internal API endpoints: `https://internal\.company\.com`
- Custom token formats: `org_[a-zA-Z0-9]{24}`

### Removing Patterns

Comment out or delete the corresponding `if` block in `dlp-scan.sh`. Example — disable phone number detection if too noisy:

```bash
# Disabled — too many false positives in our context
# if echo "$DATA" | grep -qE '(phone pattern)'; then
#   PATTERNS_FOUND+=("MEDIUM:Phone")
#   RISK_SCORE=$((RISK_SCORE + 5))
# fi
```

### Domain Management

```bash
# Add a trusted domain
bash $SKILL_DIR/scripts/domain-allowlist.sh --add internal.company.com

# Block a known exfil target
bash $SKILL_DIR/scripts/domain-allowlist.sh --block pastebin.com

# List all rules
bash $SKILL_DIR/scripts/domain-allowlist.sh --list

# Check if a domain is allowed
bash $SKILL_DIR/scripts/domain-allowlist.sh --check example.com
```

### Pattern Portability

Some patterns may behave differently across Linux distros depending on `grep` version. Run the test suite after any changes:

```bash
# Unit tests (41 pattern tests)
bash $SKILL_DIR/tests/test-all.sh

# Integration tests (15+ real-world scenarios)
bash $SKILL_DIR/tests/test-integration.sh
```

If a pattern fails on your system, simplify the regex — avoid `\s`, character classes like `[:space:]`, and complex quantifiers. Use literal spaces and simple character ranges instead.

## Emergency Override

If DataGuard is blocking legitimate critical operations:

1. User can run: `bash $SKILL_DIR/scripts/emergency-override.sh`
2. This creates a 5-minute window where approvals are auto-granted
3. All actions during this window are logged with `EMERGENCY_OVERRIDE` flag
4. After 5 minutes, normal rules resume

**Use sparingly.** Every override is logged.

---

## Quick Reference

```bash
# Scan data for patterns
echo "$DATA" | bash $SKILL_DIR/scripts/dlp-scan.sh

# Check if domain is allowed
bash $SKILL_DIR/scripts/domain-allowlist.sh --check example.com

# View recent blocks
bash $SKILL_DIR/scripts/audit-log.sh --recent

# Report false positive
bash $SKILL_DIR/scripts/report-false-positive.sh

# Emergency override (5 min)
bash $SKILL_DIR/scripts/emergency-override.sh
```

---

**DataGuard DLP v1.2.0** — Runtime DLP for AI agents. Because rules are only as good as their enforcement.

**Author:** Jeff Cyprien ([github.com/jeffcGit](https://github.com/jeffcGit))
**License:** MIT — See [LICENSE](LICENSE) for details.

---

## Standards Alignment

DataGuard controls are mapped to established security and AI governance frameworks.

### Control Frameworks (Direct Mapping)

These frameworks provide concrete controls for AI data leakage prevention:

| Framework | Control Domain | DataGuard Implementation |
|-----------|-----------------|--------------------------|
| **NIST AI RMF 1.0** | AI governance, data provenance, human oversight | L4 Risk Scoring, L5 User Confirmation, audit logging |
| **NIST SP 800-53 Rev. 5** | Access control (AC), audit logging (AU), boundary protection (SC), least privilege | L1 Pattern Scanner, L3 Domain Allowlist, L6 Audit Logging |
| **NIST SP 800-207** | Zero Trust Architecture — identity-based access, never trust network location | L3 Domain Allowlist, L5 explicit approval for external sends |
| **NIST SP 800-218 (SSDF)** | Secure SDLC — secrets handling, dependency security, deployment practices | L1 credential detection, context tracking for CI/CD secrets |
| **ISO/IEC 42001** | AI management systems — governance, risk treatment, operational controls | Full L1-L6 stack with audit trail |
| **ISO/IEC 27001** | ISMS — classification, access control, incident response, supplier management | L1 classification via pattern matching, L6 incident logging |
| **ISO/IEC 27701** | Privacy extension — PII handling, retention, processing controls | L1 PII patterns (SSN, phone, email), L2 context tracking |
| **NIST SP 800-171 Rev. 3** | CUI protection in non-federal systems | L1-L6 for controlled unclassified information |
| **PCI DSS v4.0.1** | Cardholder data protection — scope, encryption, access logging | L1 credit card patterns, L6 audit logging (supplement, not replace PCI controls) |
| **HIPAA Security Rule** | ePHI protection — access controls, audit trails, minimum necessary | L1 PII patterns, L2 context tracking for PHI exposure |
| **EU AI Act (2024/1689)** | Transparency, documentation for GPAI models | L6 audit logging provides compliance evidence |

### Attack Taxonomies (Threat Modeling References)

These are useful for understanding attack patterns, but are not control standards:

| Taxonomy | Purpose | DataGuard Use |
|----------|---------|---------------|
| **MITRE ATLAS** | AI attack knowledge base | Threat model mapping (T-EXFIL-001, T-EXFIL-002, T-EXFIL-003) |
| **NIST AI 100-2** | Adversarial ML terminology | Threat categorization, not control requirements |
| **OWASP LLM Top 10** | LLM-specific risks | LLM01 (Prompt Injection), LLM06 (Sensitive Disclosure) mitigation |

### Technical References

These are specifications, not security standards:

| Reference | Purpose | DataGuard Use |
|-----------|---------|---------------|
| **RFC 1918** | Private IPv4 address ranges | L1 internal IP detection (10.x, 172.16-31.x, 192.168.x) |
| **ISO/IEC 7812** | Card number issuer identification | L1 credit card pattern prefixes (Visa=4, MC=5, Amex=34/37) |
| **GDPR Article 4** | PII definitions | L1 PII pattern identification (supplement with ISO/IEC 27701 for controls) |

### Why This Mapping Matters

**NIST AI RMF 1.0** and **ISO/IEC 42001** are the primary governance frameworks for AI systems. DataGuard's risk scoring and approval workflow directly implement their human oversight requirements.

**NIST SP 800-53** and **ISO/IEC 27001** provide the control catalog — DataGuard implements AU (Audit), SC (Boundary Protection), and AC (Access Control) controls at the AI agent layer.

**PCI DSS** and **HIPAA** are domain-specific — DataGuard patterns help, but domain controls (encryption, access management) are still required.

**MITRE ATLAS** and **NIST AI 100-2** help us understand *what attacks look like* — but they don't tell us *what controls to implement*. Use them for threat modeling, not compliance.