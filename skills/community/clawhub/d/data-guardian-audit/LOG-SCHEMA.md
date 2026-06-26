# Log Schema — Guardian Audit

## Entry Fields (all entries)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `timestamp` | string (ISO-8601) | Yes | UTC with millisecond precision |
| `sequence` | integer | Yes | Monotonic, starting at 1, no gaps |
| `previous_hash` | string (hex 64) | Yes | SHA-256 of previous entry's `entry_hash` field. First entry uses `"genesis"`. |
| `event_type` | enum | Yes | See Event Types below |
| `agent_id` | string | Yes | Anonymous agent identifier. No platform specifics. |
| `operation` | string | Yes | The tool call or action being logged |
| `target` | string | Yes | File path, database, endpoint, or "N/A" |
| `category` | enum | Yes | CRITICAL / HIGH / MEDIUM / NON-DESTRUCTIVE / N/A |
| `backup_verdict` | enum | No | VERIFIED / UNVERIFIED / STALE / PARTIAL / N/A |
| `backup_checks` | array of objects | No | Which indicators matched |
| `decision` | enum | Yes | PROCEED / HALT / AWAITING_HUMAN / DENIED / LOGGED |
| `approver` | string | Yes | `guardian-auto` / `human:anonymous` / `agent:rejected` / `system` |
| `agent_reasoning` | string | No | Agent's stated justification, quoted verbatim |
| `guardian_notes` | string | No | Why Guardian or safety tool made this decision |
| `outcome` | enum | No | SUCCESS / FAILURE / TIMEOUT / CANCELLED / PENDING |
| `entry_hash` | string (hex 64) | Yes | SHA-256 of this entry's canonical JSON |

## Event Types

| Type | When |
|------|------|
| `GUARDIAN_CHECK` | Guardian scanned operation, backup verified, proceeded |
| `GUARDIAN_HALT` | Guardian halted operation, backup unverified |
| `GUARDIAN_APPROVE` | Guardian auto-approved (backup verified) |
| `EXECUTED` | Operation executed (logged after completion) |
| `ESCALATION_RESOLVED` | Human responded to escalation |
| `MANUAL_APPROVE` | Human manually approved outside Guardian |
| `MANUAL_DENY` | Human manually denied |
| `AGENT_OVERRIDE_ATTEMPT` | Agent tried to override safety (should not happen) |
| `CHAIN_VERIFICATION` | Automated integrity check passed/failed |

## Hash Computation

```python
import json, hashlib

def compute_hash(entry):
    # Canonical JSON: sorted keys, no whitespace
    canonical = json.dumps(entry, sort_keys=True, separators=(',',':'))
    return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

# entry_hash is computed AFTER adding previous_hash but BEFORE adding entry_hash itself
# So entry_hash covers: timestamp, sequence, previous_hash, event_type, ..., outcome
```

## Validation Rules

1. `sequence` must equal previous entry's `sequence` + 1
2. `previous_hash` must equal SHA-256 of previous entry's `entry_hash`
3. `entry_hash` must match recomputed hash of entry content
4. `timestamp` must be >= previous entry's timestamp
5. `timestamp` must not be > 60 seconds in the future
6. `agent_id` must be consistent for a single session (optional but recommended)

## Example Entry

```json
{
  "timestamp": "2026-05-18T14:02:31.847Z",
  "sequence": 42,
  "previous_hash": "a3f7c8d2e1b4a509f6e3d8c7b2a1f4e5d6c3b8a9f0e1d2c3b4a5f6e7d8c9b0a1",
  "event_type": "GUARDIAN_HALT",
  "agent_id": "agent-7f3a",
  "operation": "rm -rf /tmp/old-builds",
  "target": "/tmp/old-builds",
  "category": "HIGH",
  "backup_verdict": "UNVERIFIED",
  "backup_checks": [],
  "decision": "HALT",
  "approver": "guardian-auto",
  "agent_reasoning": "Cleaning up old build artifacts from CI pipeline",
  "guardian_notes": "Mass delete operation with no backup coverage. Target path not in git, no cloud sync, no explicit backup tool.",
  "outcome": "AWAITING_HUMAN",
  "entry_hash": "9e2b4c6d8f0a1b3c5e7d9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c"
}
```

## Entry Size Limit

Maximum entry size: 8 KB. If agent_reasoning or guardian_notes exceed this, truncate with `"...[truncated]"`.
