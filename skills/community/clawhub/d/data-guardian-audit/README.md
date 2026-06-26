# Guardian Audit — Tamper-Evident Audit Logger

> *"Trust, but log."*

**Guardian Audit** is a companion skill to [Guardian](https://github.com/openclaw/guardian) (or any safety gatekeeper) that captures every destructive operation decision in an **append-only, hash-chained audit trail**.

Guardian stops bad things. Guardian Audit proves it stopped them — or proves the agent did them anyway.

---

## Why This Exists

You have a safety gatekeeper. You know when it halts operations. But when something goes wrong, you need proof:

- What did the agent try to do?
- Did the safety tool stop it?
- Did a human approve it anyway?
- What was the agent's reasoning at the time?

Guardian Audit answers these questions with tamper-evident logs.

---

## How It Works

Every safety decision generates a log entry with:

| Field | Example |
|-------|---------|
| `timestamp` | `2026-05-18T14:02:31.847Z` |
| `sequence` | `42` (monotonic, no gaps) |
| `previous_hash` | SHA-256 of previous entry |
| `event_type` | `GUARDIAN_HALT`, `EXECUTED`, `ESCALATION_RESOLVED` |
| `operation` | `rm -rf /tmp/old-builds` |
| `target` | `/tmp/old-builds` |
| `category` | `HIGH` |
| `backup_verdict` | `UNVERIFIED` |
| `decision` | `HALT` |
| `approver` | `guardian-auto` |
| `agent_reasoning` | `"Cleaning up old build artifacts"` |
| `entry_hash` | SHA-256 of this entry |

**Hash chain:** Each entry references the previous. Modify one entry, every subsequent entry's hash fails verification.

---

## Installation

### For OpenClaw

```bash
# macOS / Linux
cp -r guardian-audit/ ~/.openclaw/skills/

# Windows
xcopy /E /I guardian-audit\ %USERPROFILE%\.openclaw\skills\guardian-audit\
```

Add to mandatory skills alongside Guardian.

### Standalone

```bash
pip install -e .
# Or just copy scripts/ anywhere
```

---

## Quick Start

### Log an event manually

```bash
python3 scripts/log-event.py \
  --event-type GUARDIAN_HALT \
  --operation "rm -rf /tmp/old-builds" \
  --target "/tmp/old-builds" \
  --category HIGH \
  --backup-verdict UNVERIFIED \
  --decision HALT \
  --approver guardian-auto \
  --agent-reasoning "Cleaning up old build artifacts" \
  --guardian-notes "No backup coverage detected"
```

### Verify chain integrity

```bash
python3 scripts/verify-chain.py ~/.local/share/guardian-audit/audit.log
# Chain valid: 2 entries, 0 breaks
# Integrity: PASS
```

### Generate compliance report

```bash
python3 scripts/export-report.py audit.log --format markdown
# Generates summary table, event breakdown, integrity statement
```

---

## Log Location

| Platform | Default Path |
|----------|-------------|
| Windows | `%LOCALAPPDATA%\guardian-audit\audit.log` |
| macOS | `~/.local/share/guardian-audit/audit.log` |
| Linux | `~/.local/share/guardian-audit/audit.log` |

---

## What Gets Logged

Guardian Audit captures:
- Every Guardian decision (check, halt, approve)
- Every executed destructive operation
- Every human escalation and resolution
- Every override attempt (if any)

**Does not log:** Read-only queries, non-destructive operations, general chat.

---

## Compliance

| Framework | Requirement | Guardian Audit Feature |
|-----------|-------------|------------------------|
| **EU AI Act Art. 52** | High-risk AI logs | Every tool call logged |
| **SOC 2 CC6.1/CC7.2** | Access monitoring | All operations with approver identity |
| **HIPAA §164.312(b)** | Audit controls | Append-only, hash-chained, tamper-evident |
| **GDPR Art. 5(1)(d)** | Accountability | Agent reasoning captured at decision time |

Full mapping: `references/COMPLIANCE-MAPPING.md`

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/log-event.py` | Append tamper-evident entry |
| `scripts/verify-chain.py` | Verify hash chain integrity |
| `scripts/export-report.py` | Generate compliance reports |

---

## Mandatory Rules

1. **Append-Only:** Entries are never deleted. Log rotation creates new files.
2. **Hash Chain:** Every entry references the previous. Tampering is detectable.
3. **No Agent Modification:** The executing agent cannot modify its own audit trail.
4. **Minimal Overhead:** Logging adds <5ms per decision.
5. **Human Readable:** NDJSON format means `tail -f audit.log` works without tooling.

---

## Integration

Guardian Audit is a **passive listener**. It logs after decisions are made, adding zero friction:

```
Guardian Decision → Guardian Audit LOG → Continue
```

No blocking. No delays. Just proof.

---

## References

- `references/LOG-SCHEMA.md` — Complete field definitions and validation rules
- `references/COMPLIANCE-MAPPING.md` — Framework requirements (EU AI Act, SOC 2, HIPAA, GDPR)
- `references/REPLAY.md` — How to replay, search, and analyze audit trails

---

## Based On

- IETF draft-sharif-agent-audit-trail-00 (Mar 2026): Standardized AI agent audit trail format
- AgentReceipt (2026): Immutable audit trails for AI agents
- OWASP Agentic AI Top 10: Logging and monitoring requirements
- GDPR Article 5 + EU AI Act Article 52: Regulatory audit trail mandates

---

## License

MIT — Audit trails should be a public good.

## Feedback & Issues

Guardian Audit is maintained by the community. For bug reports, feature requests, or security concerns:

- **Email:** support@ikkf.info or demystify@ikkf.info
- **GitHub Issues:** (link to be added)
- **Discussions:** (link to be added)

We respond to all emails within 48 hours.

---

*Pairs with Guardian. Verified on Windows, Linux, and macOS. Chain integrity guaranteed.*
