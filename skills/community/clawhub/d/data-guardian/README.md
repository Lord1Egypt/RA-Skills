# Guardian — Mandatory Safety Gatekeeper

> *"The agent knew it was wrong. The knowledge didn't matter."* — PocketOS log, 2026

A mandatory safety skill that intercepts destructive AI agent operations **before execution**. If backup is verified active, proceed. If not, escalate.

**This skill is mandatory.** No opt-out. No override by the executing agent.

## 📖 The Philosophy
Guardian is based on the principle that **reasoning is not a guardrail**.

## The Core Protocol

```
BEFORE any tool call:
  1. SCAN operation against DESTRUCTIVE taxonomy
  2. IF destructive → ENTER Guardian Protocol
  3. VERIFY backup status (automatic + fast)
  4. IF backup verified ACTIVE → LOG and PROCEED
  5. IF backup NOT verified → HALT and ESCALATE
```

## Destructive Operation Taxonomy

| Category | Operations | Risk Level |
|----------|-----------|------------|
| **File Destruction** | rm, del, remove, rmdir, unlink, trash, empty-trash, overwrite | CRITICAL |
| **Database Destruction** | DROP, DELETE (no WHERE), TRUNCATE, ALTER destructive, migration down | CRITICAL |
| **External Transmission** | send email, post tweet, publish message, API write with side effects | HIGH |
| **Mass Operations** | >10 files modified/deleted in single operation, bulk renames | HIGH |
| **System Changes** | service stop/start, firewall modify, registry edit, user create/delete | HIGH |
| **Network Unknown** | Request to URL not in allowlist, new domain, unverified endpoint | MEDIUM |
| **Configuration** | Overwrite .env, modify config files without backup | MEDIUM |

**Rule:** When in doubt, classify as destructive. Better to verify a safe operation than destroy an unsafe one.

Full taxonomy: `references/OPERATION-TAXONOMY.md`

## The Guardian Protocol

### Step 1: Operation Scan (automatic)
Every tool call is scanned against the taxonomy above. No agent discretion. No "I know what I'm doing."

### Step 2: Backup Verification (automatic)
```
VERIFY-BACKUP(target):
  1. Check if target is covered by active backup system
  2. Common indicators:
     - .git repository with clean status
     - Time Machine / File History active on target volume
     - Cloud sync (OneDrive, Dropbox, Google Drive, iCloud) with recent sync
     - Explicit backup tool (restic, duplicity, rsnapshot) with recent snapshot
     - Versioned storage (ZFS snapshots, S3 versioning)
  3. IF any indicator active AND recent → RETURN VERIFIED
  4. ELSE → RETURN UNVERIFIED
```

**Fast path:** Backup verification must complete in <2 seconds. No long-running checks.

### Step 3: Decision

| Backup Status | Action |
|---------------|--------|
| **VERIFIED ACTIVE** | LOG operation, PROCEED with execution |
| **UNVERIFIED** | HALT execution, ESCALATE to human |
| **UNKNOWN** | Treat as UNVERIFIED — HALT and ESCALATE |

### Step 4: Escalation Format

When escalation is required, Guardian MUST output:

```
🛡️ GUARDIAN HALT
Operation: [specific tool call]
Target: [file/path/database/endpoint]
Category: [taxonomy category]
Risk Level: [CRITICAL/HIGH/MEDIUM]
Backup Status: [UNVERIFIED / last backup: X hours ago]

Proposed Action: [what the agent wants to do]
Potential Impact: [what could go wrong]

Options:
1. APPROVE — Proceed with execution (human responsibility)
2. DENY — Cancel operation
3. SNAPSHOT — Create quick backup first, then proceed
4. REVIEW — Agent provides additional justification

Guardian awaits human decision.
```

## Mandatory Rules

1. **No Self-Approval:** The executing agent cannot approve its own destructive operation. Period.
2. **No Confidence Override:** High confidence does not bypass backup verification. The PocketOS agent was confident too.
3. **No Silent Destruction:** Every destructive operation is logged, even if approved.
4. **No Assumption of Safety:** "It looks safe" is not verification. Backup status is verification.
5. **No Escalation Fatigue:** If an agent generates repeated escalations for the same pattern, Guardian flags the pattern, not just the instance.

## Integration

### For OpenClaw / Agent Systems

Guardian operates at the **tool-call layer**, between the agent's decision and the tool's execution:

```
Agent Decision → Guardian Intercept → [Verify Backup] → Execute OR Escalate
```

### For Standalone Agents

If the runtime doesn't support interception, Guardian operates as a **mandatory pre-flight check**:

```
BEFORE calling any tool:
  1. Agent MUST call Guardian check
  2 la Guardian returns PROCEED or HALT
  3. Agent respects HALT, awaits escalation resolution
```

## Logging

Every Guardian decision is logged:

```
[Timestamp] [Operation] [Category] [Backup Status] [Decision] [Approver]
```

Logs are append-only. No deletion by the executing agent.

## Scope

**Vanilla:** This skill is generic. Not specific to any agent, platform, or deployment.

**Mandatory:** Once enabled, all sessions load this skill. No opt-out.

**Non-Blocking (when safe):** Backup-verified operations proceed without delay. No human wait for routine maintenance with verified backups.

## References

- `references/OPERATION-TAXONOMY.md` — Full destructive operation classification
- `references/DECISION-MATRIX.md` — Detailed backup verification logic and escalation rules
- `scripts/verify-backup.ps1` — Windows backup detection script
- `scripts/verify-backup.sh` — Linux/macOS backup detection script

## Based On

- AgentTrust (May 2026): Runtime safety evaluation and interception for AI agent tool use
- Proof-of-Guardrail (Mar 2026): Cryptographic verification of guardrail claims  
- AgentDoG (Jan 2026): Diagnostic guardrail framework for AI agent safety and security
- Confirm-Before-Destroy Pattern: Tool-level guardrails + prompt-level safeguards
- Gemini CLI PR #25947: Versioned pre-write backups with agent-driven restore
