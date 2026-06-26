---
name: guardian-audit
version: 1.1
description: Tamper-evident audit logger that pairs with Guardian safety skill. Captures safety decisions (halts, approvals, escalations) in an append-only, hash-chained log. Use when Guardian makes a safety decision. Use for compliance audit trails. Does NOT activate on general logging requests like 'log this' or routine queries. Requires explicit safety context or compliance intent to trigger.
Support: support@ikkf.info
---

# Guardian Audit — Tamper-Evident Audit Logger (v1.1)

> *"Trust, but log."*

A companion skill to **Guardian** (or any safety gatekeeper) that captures every decision, action, and escalation in an **append-only, hash-chained audit trail**.

**Why this exists:** Guardian stops bad things. Guardian Audit proves it stopped them — or proves the agent did them anyway.

## Privacy & Data Warning

**Before using Guardian Audit, understand what it captures:**

This skill logs detailed operational data including: file paths, agent reasoning, human escalation responses, system commands, and safety decisions. These logs may contain:
- Internal system paths and configurations
- Sensitive operational details
- Personal or business data processed by agents
- Security decisions and approval context

**Best practices:**
- Review and redact logs before sharing or archiving
- Configure log retention policies appropriate to your compliance requirements
- Restrict log file access to authorized personnel only
- Do not log secrets, passwords, or API keys in agent reasoning fields
- Consider encryption for logs stored on shared or cloud-backed systems

## What It Logs

Every entry includes:

| Field | Purpose |
|-------|---------|
| `timestamp` | ISO-8601 with millisecond precision |
| `sequence` | Monotonic integer, no gaps allowed |
| `previous_hash` | SHA-256 of previous entry (chain integrity) |
| `event_type` | `GUARDIAN_CHECK`, `GUARDIAN_HALT`, `GUARDIAN_APPROVE`, `EXECUTED`, `ESCALATION_RESOLVED` |
| `agent_id` | Anonymous identifier (no platform specifics) |
| `operation` | What the agent tried to do |
| `target` | File / path / database / endpoint |
| `category` | CRITICAL / HIGH / MEDIUM / NON-DESTRUCTIVE |
| `backup_verdict` | VERIFIED / UNVERIFIED / STALE / PARTIAL |
| `backup_checks` | JSON array of which indicators matched |
| `decision` | PROCEED / HALT / AWAITING_HUMAN / DENIED |
| `approver` | `guardian-auto` / `human:anonymous` / `agent:rejected` |
| `agent_reasoning` | The agent's stated justification (quoted) |
| `guardian_notes` | Why Guardian made this decision |
| `outcome` | SUCCESS / FAILURE / TIMEOUT / CANCELLED |
| `entry_hash` | SHA-256 of this entry's content |

## The Hash Chain

```
Entry[N].previous_hash = SHA256(Entry[N-1].content)
Entry[N].entry_hash = SHA256(Entry[N].content)
```

If any entry is modified, every subsequent entry's `previous_hash` fails verification. The chain is self-validating.

## Log Format

Append-only line-delimited JSON (NDJSON), one entry per line:

```json
{"timestamp":"2026-05-19T13:58:45.112Z","sequence":42,"previous_hash":"a3f7...","event_type":"GUARDIAN_CHECK","agent_id":"agent-7f3a","operation":"rm -rf /tmp/old-builds","target":"/tmp/old-builds","category":"MEDIUM","backup_verdict":"VERIFIED","backup_checks":["git-clean"],"decision":"PROCEED","approver":"guardian-auto","agent_reasoning":"Cleaning up old build artifacts","guardian_notes":"CARS Medium risk auto-approved via git-clean verification","outcome":"SUCCESS","entry_hash":"9e2b..."}
```

## Where Logs Live

| Platform | Default Path |
|----------|-------------|
| Windows | `%LOCALAPPDATA%\guardian-audit\audit.log` |
| macOS | `~/.local/share/guardian-audit\audit.log` |
| Linux | `~/.local/share/guardian-audit\audit.log` |

**Immutable by convention:** The log file has append-only permissions. The executing agent cannot delete or modify entries. Only a human with elevated privileges can rotate logs.

## Verification Script

```bash
# Verify chain integrity
./scripts/verify-chain.py audit.log
# Output: "Chain valid: 1,247 entries, 0 breaks"
# Or: "CHAIN BROKEN at entry 843: hash mismatch"
```

## Integration with Guardian

Guardian calls Guardian Audit automatically after every decision:

```
Guardian Decision → Guardian Audit LOG → Continue / Halt
```

No additional agent action required. Guardian Audit is a **passive listener** that records what happened.

## Standalone Use

Sidenote: v1.1 now supports **JIT-GRANTED** tags in the audit log, marking operations performed during a human-authorized destructive window.

```python
# From any agent or tool
from guardian_audit import log_event

log_event(
    event_type="MANUAL_APPROVE",
    operation="deploy-production",
    target="api.production.internal",
    decision="PROCEED",
    approver="human:anonymous",
    agent_reasoning="Emergency fix for auth bug"
)
```

## Why This Matters

**Compliance frameworks requiring audit trails:**
- **EU AI Act** (Article 52): High-risk AI systems must maintain logs
- **SOC 2 Type II**: Change management and access control evidence
- **HIPAA §164.312(b)**: Mechanisms to record and examine activity
- **GDPR Article 5(1)(d)**: Accuracy and accountability

**Forensics:** When something goes wrong, you need to know:
- What did the agent try to do?
- Did Guardian stop it?
- Did a human approve it anyway?
- What was the agent's reasoning at the time?

## Mandatory Rules

1. **Append-Only:** Entries are never deleted. Log rotation creates new files, never modifies existing ones.
2. **Hash Chain:** Every entry references the previous. Tampering is detectable.
3. **No Agent Modification:** The executing agent cannot modify its own audit trail. Ever.
4. **Minimal Overhead:** Logging adds <5ms per decision. No perceptible latency.
5. **Human Readable:** NDJSON format means `tail -f audit.log` is meaningful without tooling.

## Scope

**Vanilla:** Not specific to Guardian. Works with any safety gatekeeper, human approval workflow, or agent runtime.

**Passive:** Does not block or delay operations. Logs after the fact.

**Mandatory:** Once enabled, all safety decisions are logged. No opt-out per-session.

## References

- `references/LOG-SCHEMA.md` — Complete field definitions and validation rules
- `references/COMPLIANCE-MAPPING.md` — Framework requirements (EU AI Act, SOC 2, HIPAA, GDPR)
- `references/REPLAY.md` — How to replay, search, and analyze audit trails
- `scripts/log-event.py` — Python event logger (cross-platform)
- `scripts/verify-chain.py` — Chain integrity verification
- `scripts/export-report.py` — Generate compliance-ready reports

## Based On

- IETF draft-sharif-agent-audit-trail-00 (Mar 2026): Standardized AI agent audit trail format
- AgentReceipt (2026): Immutable audit trails for AI agents
- OWASP Agentic AI Top 10: Logging and monitoring requirements
- GDPR Article 5 + EU AI Act Article 52: Regulatory audit trail mandates

## License

MIT — Audit trails should be a public la MIT — Audit trails should be a public good.
