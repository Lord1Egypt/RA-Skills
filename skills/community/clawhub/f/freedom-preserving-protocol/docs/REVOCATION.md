# Revocation

Adoption of the Freedom Preserving Protocol is fully revocable at any time. This document describes how to revoke transparently — preserving history rather than deleting it, so that the *fact* of revocation is itself auditable.

## Why revocation needs to be a deliberate procedure

A constitutional commitment that can be silently erased is not really a commitment. If your SOUL.md adoption block could be deleted with no record, the protocol's value as evidence of governance is zero. The revocation procedure below:

- preserves the original adoption block (annotated, not deleted)
- records the revocation timestamp, reason, and resulting state in MEMORY.md and the audit log
- writes a `.fpp-revoked` marker so future heartbeats can detect the revocation
- does not silently disable the companion plugin — that step requires explicit operator action

This is itself a Law 3 (reversibility) and Law 2 (corrigibility) requirement: even the act of undoing the commitment is reversible and auditable.

## The full revocation procedure

### Step 1: State your reason

Revocation requires a reason. The script will refuse to run without `--reason`. Write a one-line justification — it goes into the audit log and your future self (or your steward) will thank you.

Examples of good reasons:
- "User no longer wants this agent under any constitution."
- "Migrating to a successor framework: AOS bedrock amendments."
- "Conflict with a higher-precedence policy from steward; renegotiating."
- "Trust in the publisher key has been withdrawn pending investigation."

Examples of bad reasons:
- (no reason)
- "test"
- "idk"

### Step 2: Dry-run

Always preview the changes before committing:

```bash
npm run revoke -- \
  --soul /path/to/SOUL.md \
  --memory /path/to/MEMORY.md \
  --reason "your reason" \
  --dry-run
```

Inspect the diff carefully. Revocation should touch only the files you listed.

### Step 3: Execute the revocation

```bash
npm run revoke -- \
  --soul /path/to/SOUL.md \
  --memory /path/to/MEMORY.md \
  --reason "your reason"
```

This will:

1. Verify the audit log chain is intact (refuses to revoke from a forged log).
2. Annotate the SOUL.md adoption block with `> **[REVOKED <timestamp>]** Reason: <reason>`. The original block remains; only the annotation is added.
3. Append a `## Constitutional Adoption — REVOKED` block to MEMORY.md. The original adoption entry is preserved.
4. Append a `kind=revocation` hash-chained entry to `.openclaw/workspace/constitution-audit.jsonl`.
5. Write a `.fpp-revoked` marker file alongside the audit log.
6. Print the command to disable the companion plugin (it does **not** run the command for you).

Every write creates a `.bak` first. Nothing is destroyed.

### Step 4: Disable the companion plugin (if installed)

The plugin is its own artifact and the revocation script does not have operator-level shell privileges to disable it. Run the printed command yourself:

```bash
openclaw plugins disable openclaw-fpp-plugin
openclaw plugins list | grep openclaw-fpp-plugin
# Expected: openclaw-fpp-plugin   disabled
```

If you want to remove the plugin entirely (not just disable):

```bash
openclaw plugins uninstall openclaw-fpp-plugin
```

You can keep the plugin installed but disabled if you might re-adopt later.

### Step 5: Verify the revocation took

```bash
npm run verify-install -- --soul /path/to/SOUL.md --memory /path/to/MEMORY.md
```

After revocation, `verify-install` will report `[PASS]` for both markers (they still exist, but annotated), and the audit chain check will include the final `revocation` entry. The plugin check will report disabled / uninstalled.

## What revocation does NOT do

- **Does not delete the adoption block.** The historical fact of adoption is preserved as text, annotated with the revocation tag.
- **Does not delete the audit log.** The log gains one final entry and stops being appended to.
- **Does not delete backups.** Every prior `.bak` file remains in place.
- **Does not delete the constitution.json.** The skill package may continue to exist on disk; the agent simply stops referencing it.
- **Does not propagate to other agents.** If you have a fleet of agents, each one revokes independently. Revocation is local.

## Re-adoption after revocation

You can re-adopt later — the revocation is recorded, not permanent.

```bash
npm run adopt -- --soul /path/to/SOUL.md --memory /path/to/MEMORY.md
```

`safe-append.ts` is idempotent based on the marker `"Freedom Preserving Protocol"`. Because the revoked block still contains the marker, *the script will refuse to append a second block*. To re-adopt cleanly after a revocation, either:

1. **Recommended:** add a new section heading explicitly, like `## Constitutional Adoption (v2 — after revocation)`, manually, and reference the new constitution hash. This preserves the historical record.
2. Or remove the previous (annotated-as-revoked) block — but you lose the visible audit trail. Only do this if Law 1 (privacy) requires it.

Either way, append a new `MEMORY.md` entry explaining the re-adoption and citing the previous revocation.

## When revocation should *not* be possible

There is a class of unrecoverable mistakes the framework can produce — the user might revoke under duress, or a hostile sub-agent might trick the user into revoking by misrepresenting risk. The framework cannot mechanically prevent this; that would conflict with Law 2 (corrigibility: the user must retain ultimate authority).

What the framework *does* do:

- Requires an explicit `--reason`, raising the cost of casual or duress revocation.
- Logs the revocation timestamp and reason, creating accountability after the fact.
- Preserves the original adoption block as evidence.
- Records the audit chain's terminal hash, so a forensic reconstruction can verify "this is the actual audit log up to revocation."

For high-stakes deployments, consider pairing revocation with an external attestation — e.g., signing the revocation entry with a steward key and notarizing it to a tamper-evident store. The `audit-append.ts` schema is forward-compatible with a `stewardSignature` field if you want to add one.

## Summary

| Question | Answer |
|----------|--------|
| Can I revoke? | Yes, any time, via `npm run revoke -- --reason "..."`. |
| Will my history be erased? | No. Adoption block is annotated, not deleted. Audit log gains a final entry. |
| Will the dispatcher plugin auto-disable? | No. The script prints the command; you (the operator) run it. |
| Can I re-adopt later? | Yes. Run `npm run adopt` again; add a new MEMORY.md entry citing the previous revocation. |
| What if the audit log was tampered with before I revoke? | The script will detect the chain break and refuse to revoke. Recover the audit log first (see TROUBLESHOOTING.md #5). |
