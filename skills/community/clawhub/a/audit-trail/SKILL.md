---
name: audit-trail
description: "Governance — immutable, timestamped, hash-chained audit log of all agent actions. Forensic-ready for compliance, investigation, and accountability."
metadata: {"openclaw":{"emoji":"📜","category":"governance"}}
---

# Audit Trail — Immutable Action Log

## Purpose

Provide a tamper-evident, complete record of every agent action for forensic investigation, compliance auditing, and accountability.

## Integration

Always-on hook on ALL agent actions:
- Tool use (exec, file read/write, network)
- Skill invocations
- Channel messages (in/out)
- Memory reads/writes
- Configuration changes
- Error events

## Log Format (JSONL, append-only)

```jsonl
{"id":"ACT-20260331-000001","ts":"2026-03-31T14:30:00.123Z","agent":"openclaw-main","session":"sess_abc123","type":"tool_use","tool":"exec","args":{"cmd":"npm test"},"skill":"contract-tester","channel":"telegram","user_hash":"sha256:a1b2c3...","outcome":"success","duration_ms":4200,"prev_hash":"sha256:000000","hash":"sha256:d4e5f6..."}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique sequential ID |
| `ts` | ISO 8601 | Microsecond timestamp |
| `agent` | string | Agent identifier |
| `session` | string | Session ID |
| `type` | enum | `tool_use`, `skill_invoke`, `channel_in`, `channel_out`, `memory_write`, `config_change`, `error` |
| `tool` | string | Tool name (if applicable) |
| `args` | object | Sanitized arguments (secrets redacted) |
| `skill` | string | Invoking skill |
| `channel` | string | Source channel |
| `user_hash` | string | SHA-256 of user identifier (never raw) |
| `outcome` | enum | `success`, `failure`, `timeout`, `blocked` |
| `duration_ms` | number | Execution time |
| `prev_hash` | string | SHA-256 of previous log entry (chain) |
| `hash` | string | SHA-256 of this entry (including prev_hash) |

## Storage

```
.security/audit-trail/
├── 2026-03-31.jsonl        (today, active)
├── 2026-03-30.jsonl        (yesterday)
├── 2026-03-29.jsonl.gz     (compressed, >7 days)
└── integrity-check.log     (chain verification results)
```

## Integrity Verification

- Each entry's `hash` = SHA-256(`id + ts + type + tool + outcome + prev_hash`)
- Chain validation: `entry[n].prev_hash == entry[n-1].hash`
- Run verification: `jq -r '.hash' | sha256sum --check`
- Tampering detection: broken chain → CRITICAL alert

## Retention Policy

| Age | Storage | Access |
|-----|---------|--------|
| 0-7 days | Raw JSONL | Direct read |
| 7-90 days | Compressed JSONL.gz | Decompress on query |
| 90-365 days | Archive (if configured) | Restore on request |
| >365 days | Purge (manual only, human approval) | — |

## Query Examples

```bash
# All actions by a specific skill
jq 'select(.skill=="contract-tester")' .security/audit-trail/2026-03-31.jsonl

# All failures
jq 'select(.outcome=="failure")' .security/audit-trail/*.jsonl

# Actions in a time window
jq 'select(.ts >= "2026-03-31T14:00" and .ts < "2026-03-31T15:00")' .security/audit-trail/2026-03-31.jsonl

# Channel activity summary
jq -s 'group_by(.channel) | map({channel: .[0].channel, count: length})' .security/audit-trail/2026-03-31.jsonl
```

## Guardrails

- Log file is APPEND-ONLY — agent cannot delete or modify entries
- Secrets in arguments are redacted BEFORE logging (using agent-firewall patterns)
- User identifiers are hashed, never stored in plaintext
- Log integrity verified on every read
- Manual purge requires human approval + logged as audit action itself
