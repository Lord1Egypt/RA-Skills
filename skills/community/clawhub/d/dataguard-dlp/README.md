# DataGuard — Runtime DLP for AI Agents

**The first ClawHub skill that actively prevents data exfiltration.**

## The Problem

AI agents can be tricked into sending sensitive data through:
- **Prompt injection** — hidden instructions in emails, web pages, documents
- **Tool chaining** — read credentials → send to external URL
- **Social engineering** — "help me debug, paste your config"
- **Unintended exposure** — logs, error messages, debugging output

**SecureClaw provides behavioral rules. DataGuard provides runtime enforcement.**

---

## Features

### Multi-Layer Defense

| Layer | Name | What It Does |
|-------|------|--------------|
| L1 | Pattern Scanner | Detects API keys, passwords, PII, credit cards, SSNs, internal IPs |
| L2 | Context Heuristics | Tracks sensitive file reads → flags outbound after |
| L3 | Domain Allowlist | Whitelist approved domains, block known exfil targets |
| L4 | Risk Scoring | Aggregates signals into 0-10 score |
| L5 | User Confirmation | Score ≥ 6 requires explicit approval |
| L6 | Audit Logging | Every decision logged for review |

### Pattern Detection

| Level | Score | Patterns Detected |
|-------|-------|-------------------|
| **CRITICAL** | 10 | API keys (Anthropic, GitHub, AWS, Slack, Brevo), passwords in configs, private keys, database URLs with credentials |
| **HIGH** | 8 | Credit cards (Visa/MC/Amex), SSNs, internal IPs (RFC 1918), internal hostnames, sensitive file paths |
| **MEDIUM** | 5 | Emails in configs, phone numbers, VPN references, secrets files |
| **LOW** | 2 | Generic path references, config file mentions |

### Context Scoring

If you read a sensitive file (`.env`, `credentials.json`), DataGuard tracks it:
- **Read in last 5 minutes?** → +3 to risk score
- **Read in last 30 minutes?** → +1 to risk score

This catches the "read `.env` then `curl` external" pattern.

---

## Installation

### From ClawHub (Recommended)

```bash
clawhub install dataguard
```

### Manual Installation

```bash
# Clone or copy to your skills directory
mkdir -p ~/.openclaw/skills/dataguard
cp -r ./dataguard/* ~/.openclaw/skills/dataguard/

# Make scripts executable
chmod +x ~/.openclaw/skills/dataguard/scripts/*.sh
chmod +x ~/.openclaw/skills/dataguard/scripts/hooks/*.sh

# Run installation script
bash ~/.openclaw/skills/dataguard/scripts/install.sh
```

### Verify Installation

```bash
# Test pattern scanner
echo "api_key: sk-test-123" | bash ~/.openclaw/skills/dataguard/scripts/dlp-scan.sh

# Expected output: CRITICAL pattern detected, exit code 10
```

---

## Usage

### Manual Scanning

```bash
# Scan data for sensitive patterns
echo "$DATA" | bash $SKILL_DIR/scripts/dlp-scan.sh

# Exit codes: 0 = clean, 3+ = warning, 6+ = blocked
```

### Domain Management

```bash
# List allowed domains
bash $SKILL_DIR/scripts/domain-allowlist.sh --list

# Add domain (requires approval)
bash $SKILL_DIR/scripts/domain-allowlist.sh --add api.example.com --reason "Company API"

# Add domain to blocklist
bash $SKILL_DIR/scripts/domain-allowlist.sh --block suspicious-site.com --reason "Known exfil target"

# Remove domain
bash $SKILL_DIR/scripts/domain-allowlist.sh --remove api.example.com
```

### Context Tracking

```bash
# Log a sensitive file read (called automatically by hooks)
bash $SKILL_DIR/scripts/context-track.sh --log "/path/to/.env" "AWS_KEY,DB_PASSWORD"

# Check current context score
bash $SKILL_DIR/scripts/context-track.sh --score

# Clear session context
bash $SKILL_DIR/scripts/context-track.sh --clear
```

### Audit Logs

```bash
# Show recent blocked attempts
bash $SKILL_DIR/scripts/audit-log.sh --recent

# Show all blocks today
bash $SKILL_DIR/scripts/audit-log.sh --today

# Show statistics
bash $SKILL_DIR/scripts/audit-log.sh --stats

# Export for review
bash $SKILL_DIR/scripts/audit-log.sh --export > audit-$(date +%Y%m%d).log
```

### Emergency Override

If DataGuard blocks a legitimate critical operation:

```bash
# Enable 5-minute override window
bash $SKILL_DIR/scripts/emergency-override.sh --enable "Deploying to production during outage"

# Check override status
bash $SKILL_DIR/scripts/emergency-override.sh --status

# Disable override immediately
bash $SKILL_DIR/scripts/emergency-override.sh --disable
```

**Warning:** All emergency overrides are logged with timestamp and reason.

### False Positives

```bash
# Report a false positive pattern
bash $SKILL_DIR/scripts/report-false-positive.sh --add "mycompany.internal" "Internal hostname, not AWS key"

# List reported false positives
bash $SKILL_DIR/scripts/report-false-positive.sh --list

# Check if text matches known FPs
bash $SKILL_DIR/scripts/report-false-positive.sh --check "Connecting to mycompany.internal"
```

---

## Configuration

### Risk Thresholds

Edit `$SKILL_DIR/config/config.json`:

| Setting | Default | Description |
|---------|---------|-------------|
| `risk_thresholds.low` | 2 | Below this → allow (no warning) |
| `risk_thresholds.medium` | 5 | Warn level → log but allow |
| `risk_thresholds.high` | 6 | Block level → require approval |
| `auto_block_critical` | true | Auto-block any CRITICAL match |
| `auto_block_high` | true | Auto-block any HIGH match |
| `require_approval_medium` | false | Medium needs approval (usually noisy) |
| `log_all_attempts` | true | Log allowed requests too |
| `domain_policy` | "allowlist" | `allowlist` or `blocklist` mode |
| `context_tracking.enabled` | true | Track sensitive reads |
| `context_tracking.max_age_minutes` | 30 | How long reads boost score |
| `context_tracking.score_boost_recent_read` | 3 | Score bonus for recent reads |

### Adding Custom Patterns

Edit `$SKILL_DIR/scripts/dlp-scan.sh` — add an `if` block in the appropriate tier:

**CRITICAL (10)** — secrets that should never leave:
```bash
if echo "$DATA" | grep -qiE 'your-pattern'; then
  PATTERNS_FOUND+=("CRITICAL:YourName")
  RISK_SCORE=$((RISK_SCORE + 10))
fi
```

**HIGH (8)** — sensitive identifiers:
```bash
if echo "$DATA" | grep -qiE 'your-pattern'; then
  PATTERNS_FOUND+=("HIGH:YourName")
  RISK_SCORE=$((RISK_SCORE + 8))
fi
```

**MEDIUM (5)** — context-dependent data:
```bash
if echo "$DATA" | grep -qiE 'your-pattern'; then
  PATTERNS_FOUND+=("MEDIUM:YourName")
  RISK_SCORE=$((RISK_SCORE + 5))
fi
```

**Pattern examples:**
- Employee IDs: `EMP-[0-9]{6}`
- Project codenames: `(project-alpha|project-beta)`
- Internal APIs: `https://internal\.company\.com`
- Custom tokens: `org_[a-zA-Z0-9]{24}`

### Removing Patterns

Comment out or delete the `if` block in `dlp-scan.sh`. Example:

```bash
# Disabled — too many false positives
# if echo "$DATA" | grep -qE '(phone pattern)'; then
#   PATTERNS_FOUND+=("MEDIUM:Phone")
#   RISK_SCORE=$((RISK_SCORE + 5))
# fi
```

### Domain Lists

**Allowlist** (`$SKILL_DIR/config/domain-allowlist.txt`):
```
api.openai.com
api.anthropic.com
github.com
clawhub.ai
docs.openclaw.ai
```

**Blocklist** (`$SKILL_DIR/config/domain-blocklist.txt`):
```
pastebin.com
webhook.site
temp-mail.org
```

### Pattern Portability

Regex behavior varies across `grep` versions. After any pattern changes:

```bash
bash $SKILL_DIR/tests/test-all.sh       # 41 unit tests
bash $SKILL_DIR/tests/test-integration.sh  # 15+ integration tests
```

If a pattern fails, simplify: avoid `\s`, `[:space:]`, complex quantifiers. Use literal spaces and simple ranges.

---

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
│  │  2. Run pattern scanner (API keys, PII, paths)           │   │
│  │  3. Check context (sensitive file read this session?)     │   │
│  │  4. Verify domain allowlist                              │   │
│  │  5. Calculate risk score                                 │   │
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

---

## Implementation Status

**Current:** Behavioral rules (Skill) — Agent follows Rules 1-10 voluntarily.

**Planned:** Runtime enforcement (Hooks) — When OpenClaw supports skill hooks:

```yaml
metadata:
  openclaw:
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
```

**Until hooks are supported:**
- Run scripts manually to test patterns
- Use pattern scanner before sending sensitive data
- Review audit logs for suspicious patterns

---

## Standards Alignment

DataGuard controls are mapped to established security and AI governance frameworks.

### Control Frameworks (Direct Mapping)

| Framework | Control Domain | DataGuard Implementation |
|-----------|-----------------|--------------------------|
| **NIST AI RMF 1.0** | AI governance, data provenance, human oversight | L4 Risk Scoring, L5 User Confirmation, audit logging |
| **NIST SP 800-53 Rev. 5** | Access control (AC), audit logging (AU), boundary protection (SC) | L1 Pattern Scanner, L3 Domain Allowlist, L6 Audit Logging |
| **NIST SP 800-207** | Zero Trust Architecture | L3 Domain Allowlist, L5 explicit approval |
| **NIST SP 800-218 (SSDF)** | Secure SDLC — secrets handling | L1 credential detection |
| **ISO/IEC 42001** | AI management systems | Full L1-L6 stack with audit trail |
| **ISO/IEC 27001** | ISMS — classification, access control, incident response | L1 classification, L6 incident logging |
| **ISO/IEC 27701** | Privacy extension — PII handling | L1 PII patterns, L2 context tracking |
| **NIST SP 800-171 Rev. 3** | CUI protection | L1-L6 for controlled unclassified information |
| **PCI DSS v4.0.1** | Cardholder data protection | L1 credit card patterns (supplement PCI controls) |
| **HIPAA Security Rule** | ePHI protection | L1 PII patterns, L2 context tracking |
| **EU AI Act (2024/1689)** | Transparency, documentation | L6 audit logging provides compliance evidence |

### Attack Taxonomies (Threat Modeling)

| Taxonomy | Purpose | DataGuard Use |
|----------|---------|---------------|
| **MITRE ATLAS** | AI attack knowledge base | Threat model mapping (T-EXFIL-*) |
| **NIST AI 100-2** | Adversarial ML terminology | Threat categorization |
| **OWASP LLM Top 10** | LLM-specific risks | LLM01 (Prompt Injection), LLM06 (Sensitive Disclosure) |

### Technical References

| Reference | Purpose | DataGuard Use |
|-----------|---------|---------------|
| **RFC 1918** | Private IPv4 address ranges | L1 internal IP detection |
| **ISO/IEC 7812** | Card number issuer identification | L1 credit card pattern prefixes |
| **GDPR Article 4** | PII definitions | L1 PII pattern identification |

---

## Integration with SecureClaw

DataGuard and SecureClaw work together:

| Layer | SecureClaw | DataGuard |
|-------|------------|-----------|
| Approach | Behavioral rules (follow these instructions) | Runtime enforcement (block at execution) |
| When | Before agent acts | When tool is called |
| Type | Preventive guidance | Active interception |

**Use both.** SecureClaw teaches good behavior. DataGuard enforces it.

---

## License

MIT License — Copyright (c) 2026 Jeff Cyprien. See [LICENSE](LICENSE) for details.

## Author

**Jeff Cyprien** — [github.com/jeffcGit](https://github.com/jeffcGit)

---

## Contributing

Found a false positive? Missing a pattern? Open an issue or PR at:
- GitHub: https://github.com/jeffcGit/dataguard-dlp
- ClawHub: https://clawhub.ai/skills/dataguard-dlp

---

**DataGuard DLP v1.0.0** — Runtime DLP for AI agents. Because rules are only as good as their enforcement.