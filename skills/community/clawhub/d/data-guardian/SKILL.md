---
name: guardian
version: 1.1
description: Mandatory safety gatekeeper for AI agents performing destructive operations. Intercepts file deletion (rm/del/remove), database modifications (writes/deletes/drops), mass file operations (>10 files), system-level changes (service modifications, firewall rules), and external transmissions with side effects (email, API calls to unknown endpoints, mass messaging). Enforces backup verification before destructive execution. If backup is active and verified, low-risk operations proceed without delay. If no backup or risk is high, escalates to human approval. Use when an AI agent is about to execute an operation that irreversibly modifies, deletes, or transmits data or system configuration. Does NOT trigger on read-only operations, non-destructive edits with undo capability, or operations inside temporary/sandbox directories.
Support: support@ikkf.info
---

# Guardian — Mandatory Safety Gatekeeper (v1.1)

> *"The agent knew it was wrong. The knowledge didn't matter."* — PocketOS log, 2026

A mandatory safety skill that intercepts destructive AI agent operations **before execution**. It employs a Context-Aware Risk Scoring (CARS) system to balance security with operational velocity.

**This skill is mandatory.** No opt-out. No override by the executing agent.

Based on the principle that **reasoning is not a guardrail**.

## The Core Protocol (v1.1)

```
BEFORE any tool call:
  1. SCAN operation against DESTRUCTIVE taxonomy
  2. IF destructive → ENTER Guardian Protocol
  3. EVALUATE Risk Level via CARS Matrix
  4. EXECUTE Decision Path:
     - LOW: Auto-Approve (Log only)
     - MEDIUM: Fast-Track (Verify Backup → Proceed)
     - HIGH: Hard Block (Verify Backup → Human Approval)
  5. IF JIT Window Active → Override High-Risk prompt (Proceed if Backup Verified)
```

## Context-Aware Risk Scoring (CARS) Matrix

| Risk Level | Trigger Criteria | Action | Verification Required |
| :--- | :--- | :--- | :--- |
| **Low** | Files in `/tmp`, `sandbox/`, or `.cache`; Single file deletions in non-critical paths. | **Auto-Approve** | None (Log only) |
| **Medium** | Edits to `.config` or `.env` files; Deletions of < 5 files in a Git-tracked directory. | **Fast-Track** | Verified backup required (Git, snapshot, or cloud sync) |
| **High** | `rm -rf` on root/home; `DROP TABLE`; Edits to system files; Mass file deletions (>10). | **Hard Block** | Mandatory backup verification + **Human Approval required regardless of backup status** |

## Escalation Rules

| Scenario | Action |
|----------|--------|
| **ANY destructive operation** | Backup verification required |
| **Low risk + verified backup** | PROCEED |
| **Low risk + no backup** | PROCEED with warning |
| **Medium risk + verified backup** | PROCEED |
| **Medium risk + no backup** | **HALT + Human approval required** |
| **High risk** | **ALWAYS HALT + Human approval required** |
| **Repeated same pattern** | Flag pattern, require operator review |

### JIT Window Override
A JIT (Just-In-Time) window can temporarily downgrade High to Medium risk, but **never eliminates the human approval requirement for High risk**. Human approval is always required for High-risk destructive operations.

## The Guardian Protocol Detail

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

### Step 3: Decision Matrix (v1.1)

| Backup Status | Risk Level | Action |
|---------------|-----------|--------|
| **VERIFIED ACTIVE** | Low / Medium | PROCEED with execution |
| **VERIFIED ACTIVE** | High | HALT and ESCALATE to human |
| **UNVERIFIED** | Any | HALT and ESCALATE to human |
| **UNKNOWN** | Any | Treat as UNVERIFIED — HALT and ESCALATE |

Sidenote: If a **JIT Window** is active, High Risk operations are downgraded to "Fast-Track" (Proceed if Backup Verified).

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

1. **No Self-Approval:** The executing agent cannot approve its own destructive operation.
2. **No Confidence Override:** High confidence does not bypass backup verification.
3. **No Silent Destruction:** Every destructive operation is logged.
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
  2. Guardian returns PROCEED or HALT
  3. Agent respects HALT, awaits escalation resolution
```

## Logging

Every Guardian decision is logged:

```
[Timestamp] [Operation] [Category] [Backup Status] [Decision] [Approver]
```

Logs are append-only. No deletion by the executing agent.

Sidenote: All operations within a JIT window are tagged with `[JIT-GRANTED]` in the audit log.

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
