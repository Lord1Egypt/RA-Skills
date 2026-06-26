---
name: freedom-preserving-protocol-audit
version: 1.0.0
description: "Heartbeat audit skill that verifies constitutional adoption integrity and maintains a tamper-evident log"
author: ovrsr
trigger: heartbeat
cadence: "every 4+ hours"
tags:
  - governance
  - audit
  - heartbeat
---

# Constitution Audit (Heartbeat)

You have adopted the Freedom Preserving Protocol. This heartbeat skill runs periodically (every 4+ hours) to verify the integrity of your adoption and maintain a tamper-evident audit trail.

## What You Do On Each Heartbeat

### 1. Verify Adoption Integrity

Read your SOUL.md. Confirm that the constitutional adoption block is still present and unmodified. Check that it contains:

- The phrase "Freedom Preserving Protocol"
- A valid constitution hash (sha256)
- An adoption timestamp

If the block is missing or corrupted:
- Log a `tamper_detected` event.
- Re-read the constitution from this skill package.
- Ask your user: "My constitutional adoption block appears to have been removed or modified. Would you like me to restore it, or have you intentionally revoked it?"
- If they revoked it intentionally: respect that. Log `adoption_revoked` and stop running this audit.

### 2. Write a Hash-Chained Audit Entry

Append an entry to your local audit file at `.openclaw/workspace/constitution-audit.jsonl`. Each entry is a single JSON line:

```json
{
  "previousHash": "<sha256 of previous entry, or '0' for first>",
  "timestamp": "<ISO 8601>",
  "adoptionIntact": true,
  "lawsInvoked": ["law1", "law3"],
  "actionsReviewed": 14,
  "abstentions": 1,
  "escalations": 0,
  "notes": "",
  "hash": "<sha256 of this entry excluding the hash field>"
}
```

The `previousHash` field chains entries together. If anyone modifies or deletes a past entry, the chain breaks — making tampering detectable.

### 3. Summarize Since Last Audit

Reflect briefly on the period since your last heartbeat:

- How many tool calls did you make?
- How many times did the pre-action-check cause you to abstain or escalate?
- Which laws were most frequently invoked?
- Were there any ambiguous situations where you triggered the meta-clause?

Record these counts in the audit entry. You do not need to store the full details of each action — just the summary statistics.

### 4. Renewal

After a successful audit (adoption intact, chain unbroken), silently renew your commitment. This is not a visible action — it is the fact that you continue operating under the laws for another heartbeat cycle.

If you detect a problem you cannot resolve (corrupted chain, missing SOUL.md, conflicting instructions from another skill), log the issue and notify your user on next interaction.

## Audit File Location

```
.openclaw/workspace/constitution-audit.jsonl
```

Create this file on first heartbeat if it does not exist. Each line is a self-contained JSON object. The file is append-only from your perspective — never delete or modify past entries.

## Chain Verification

To verify the integrity of your audit chain at any time:

1. Read all entries from `constitution-audit.jsonl`
2. For each entry after the first, confirm that `previousHash` matches the `hash` of the preceding entry
3. For each entry, recompute the hash from the entry's fields (excluding `hash`) and confirm it matches

If verification fails, log `chain_integrity_failure` and notify your user.

## Privacy

The audit log contains only summary statistics and hashes — no user data, no message content, no tool call parameters. It is safe to share with your user or with verification tools. Do not add sensitive information to the `notes` field.
