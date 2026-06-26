# Step 3 — Reporting & Fixes

## Report format

For each contradiction found, produce a structured finding:

```
AGENT: <agent-id>
SEVERITY: HIGH | MEDIUM | LOW
PATTERN: <pattern number and name from contradiction-patterns.md>
FILES: <file-a> vs <file-b>
ISSUE: <precise description of what conflicts>
EVIDENCE:
  File A (<path>): "<exact quote>"
  File B (<path>): "<exact quote>"
IMPACT: <what observable behavior this causes or risks>
FIX: <which file should be authoritative and what specific change to make>
```

### Severity guidelines

| Severity | Criteria |
|----------|----------|
| **HIGH** | Actively causing wrong behavior now, or will cause wrong behavior on next format/routing change. Includes: format duplication, cron override, routing mismatch. |
| **MEDIUM** | Latent risk — currently aligned but maintained independently, or causing inconsistent persona/tone. |
| **LOW** | Cosmetic, stale references, or minor wording issues unlikely to affect runtime behavior. |

### Clean report

If no contradictions are found:

```
AUDIT CLEAN — <N> agents scanned, <M> instruction files cross-referenced, <K> cron jobs checked. No contradictions found.
```

## Applying fixes

**All fixes require explicit user confirmation.**

### Fix presentation format

Present each proposed fix as a diff:

```
FIX <n>/<total> — <severity>
Agent: <agent-id>
File: <path>
Action: <edit | delete section | add section>

BEFORE:
  <exact text to be replaced>

AFTER:
  <replacement text>

RATIONALE: <one sentence explaining why>
```

### Fix ordering

Apply fixes in this order:
1. HIGH severity first (actively causing issues)
2. MEDIUM severity (latent risks)
3. LOW severity (cosmetic)

Within the same severity, fix format duplication before routing before persona.

### Post-fix verification

After applying any fix:
1. Re-read the modified file
2. Re-read the file it was contradicting
3. Verify they now agree
4. If the fix introduced a new contradiction, flag it immediately

### What NOT to fix autonomously (even with confirmation)

- Removing entire instruction files
- Changing which agent owns a task
- Altering cron schedules (timing changes affect production)
- Modifying security rules or permission boundaries

These require explicit discussion with the user about intent, not just confirmation of a diff.
