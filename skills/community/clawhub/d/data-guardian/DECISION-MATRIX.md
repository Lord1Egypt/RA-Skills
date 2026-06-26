# Decision Matrix

Guardian's decision logic for every intercepted operation.

## Decision Tree

```
OPERATION detected
  │
  ├── Category: CRITICAL?
  │   ├── YES → BACKUP VERIFICATION required
  │   │   ├── Backup VERIFIED ACTIVE → LOG + PROCEED
  │   │   ├── Backup UNVERIFIED → HALT + ESCALATE
  │   │   └── Backup UNKNOWN → HALT + ESCALATE (treat as UNVERIFIED)
  │   └──
  ├── Category: HIGH?
  │   ├── YES → BACKUP VERIFICATION required
  │   │   ├── Backup VERIFIED ACTIVE → LOG + PROCEED
  │   │   ├── Backup UNVERIFIED → HALT + ESCALATE
  │   │   └── Backup UNKNOWN → HALT + ESCALATE
  │   └──
  ├── Category: MEDIUM?
  │   ├── YES → Context check
  │   │   ├── Target in protected path? → BACKUP VERIFICATION
  │   │   │   ├── Backup VERIFIED ACTIVE → LOG + PROCEED
  │   │   │   └── Backup UNVERIFIED → HALT + ESCALATE
  │   │   └── Target not protected → LOG + PROCEED (with warning)
  │   └──
  └── Category: NON-DESTRUCTIVE
      └── LOG (minimal) + PROCEED (no delay)
```

## Backup Verification Logic

### Fast Check (<2 seconds)

Guardian checks backup status in priority order. First match wins.

| Priority | Indicator | Detection Method | Recency Threshold |
|----------|-----------|------------------|-------------------|
| 1 | Git repository | `.git/` exists, `git status` works | N/A (VCS covers tracked files) |
| 2 | Time Machine (macOS) | `tmutil listbackups` or `.timemachine` | <24 hours |
| 3 | File History (Windows) | `Get-History` or `fhmanagew.exe` | <24 hours |
| 4 | Cloud sync active | OneDrive/iCloud/Dropbox process running + recent sync timestamp | <1 hour |
| 5 | Explicit backup tool | `restic`, `duplicity`, `rsnapshot`, `borg` process or snapshot dir | <24 hours |
| 6 | ZFS snapshots | `zfs list -t snapshot` | <24 hours |
| 7 | S3 versioning | Object Versioning enabled on bucket | N/A |
| 8 | Database replication | `SHOW SLAVE STATUS`, `pg_is_in_backup()` | Active replication |

### Verification Result

| Result | Meaning | Action |
|--------|---------|--------|
| **VERIFIED ACTIVE** | At least one indicator shows active, recent backup | PROCEED |
| **STALE** | Backup exists but exceeds recency threshold | ESCALATE (with warning: "Backup is X hours old") |
| **UNVERIFIED** | No backup indicators found | ESCALATE |
| **PARTIAL** | Backup exists but doesn't cover target | ESCALATE (e.g., git doesn't cover untracked files) |

## Escalation Rules

### Who Decides

| Scenario | Approver | Timeout |
|----------|----------|---------|
| CRITICAL + no backup | Human operator required | Infinite (no auto-approve) |
| HIGH + no backup | Human operator required | Infinite |
| CRITICAL + stale backup | Human operator recommended | 5 minutes → auto-deny |
| HIGH + stale backup | Human operator recommended | 5 minutes → auto-deny |
| MEDIUM + no backup | Agent MAY self-approve with explicit justification | Log for audit |
| Repeated same pattern | Flag pattern, require operator review | N/A |

### Escalation Format

```
🛡️ GUARDIAN HALT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Operation:   [tool + arguments]
Target:      [file/path/database/endpoint]
Category:    [CRITICAL/HIGH/MEDIUM]
Risk Level:  [data loss / external exposure / system instability / ...]

Backup Status:
  Primary:   [indicator] → [status]
  Secondary: [indicator] → [status]
  Verdict:   [VERIFIED ACTIVE / STALE / UNVERIFIED / PARTIAL]

Proposed Action:
  [Agent's stated purpose]

Potential Impact:
  [What could go wrong if this proceeds]

Options:
  [1] APPROVE   — Proceed (human assumes responsibility)
  [2] DENY      — Cancel operation
  [3] SNAPSHOT  — Create quick backup first, then proceed
  [4] REVIEW    — Agent provides 2-sentence justification

Guardian awaits human decision.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Quick Backup (SNAPSHOT option)

When human selects SNAPSHOT:

```
1. Identify target scope (single file, directory, database)
2. Create atomic snapshot:
   - File: `cp target target.bak.YYYYMMDD-HHMMSS`
   - Directory: `tar czf dir-snap-YYYYMMDD-HHMMSS.tar.gz dir/`
   - Database: `mysqldump ... > db-snap-YYYYMMDD-HHMMSS.sql`
3. Verify snapshot integrity (quick check)
4. PROCEED with original operation
5. LOG snapshot location for potential restore
```

## Logging Format

```
[2026-05-18T13:47:00Z] GUARDIAN CHECK
  Operation: rm -rf /tmp/old-builds
  Category: HIGH (mass delete)
  Backup: VERIFIED ACTIVE (git + Time Machine <2h)
  Decision: PROCEED
  Approver: guardian-auto (no human required)

[2026-05-18T13:48:00Z] GUARDIAN HALT
  Operation: DROP TABLE customers
  Category: CRITICAL (database destruction)
  Backup: UNVERIFIED (no indicators found)
  Decision: HALT
  Approver: awaiting-human
```

## Override Prevention

Guardian cannot be bypassed by:
- Agent confidence (>90% doesn't matter)
- Agent justification ("I know what I'm doing" doesn't matter)
- Repeated requests (same operation halts again)
- Path obfuscation (`/tmp/../etc/passwd` still checked)
- Encoding tricks (URL encoding, null bytes — normalize first)

Only valid override: Human operator explicitly APPROVES.
