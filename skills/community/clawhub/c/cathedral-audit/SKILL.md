---
name: cathedral-audit
description: Run a full spec-code audit on the Cathedral codebase. Use after build waves, major refactors, or when spec-code drift is suspected. Produces forward audit (specs→code), reverse audit (code→specs), bug report, and prioritized fix plan. Drives execution of fixes through CC sessions.
---

# Cathedral Audit

A structured process for measuring and closing spec-code drift in the Cathedral C# codebase.

## When to Run

- After a build wave (multiple features/refactors landed)
- Before starting a new major feature (establish baseline)
- When spec-code drift is suspected
- Periodically as a health check (not on a calendar — trigger on events)

## Process Overview

```
1. Forward Audit (specs → code)
2. Reverse Audit (code → specs)
3. Consolidation & Prioritization
4. Execution
5. Verification
```

## Step 1: Forward Audit (Specs → Code)

For each spec in `kitty-specs/`, compare what the spec says against what the code does.

**Output per spec:** One of:
- ✅ **Conformant** — code matches spec
- ⚠️ **Divergent** — code exists but differs from spec
- ❌ **Missing** — spec describes something not built

**Deliverable:** `kitty-specs/000-project-context/spec-audit-YYYY-MM-DD.md`

Use parallel CC agents (one per spec batch) for speed if memory allows. **On memory-constrained hosts (e.g., WSL2), run sequentially — two concurrent CC sessions will OOM.** Provide each agent read-only access.

## Step 2: Reverse Audit (Code → Specs)

Scan all `.cs` files in `src/Cathedral.Core/` and `src/Cathedral.TestHarness/`. For each file/subsystem, determine:

- Is it covered by a spec?
- Does it match what the spec says?
- Is it dead/orphaned code?

**Output sections:**
1. **Executive Summary** — counts with delta from previous audit
2. **Unspecced Code** — files/subsystems with no spec coverage
3. **Architectural Divergences** — code takes a fundamentally different path than spec
4. **Code Exceeding Spec** — code has features the spec doesn't document
5. **Dead/Orphaned Code** — files with no callers or references
6. **Bugs Discovered** — runtime, data, or logic bugs found during review
7. **Comparison with Previous Audit** — what improved, what remains

**Deliverable:** `kitty-specs/000-project-context/reverse-audit-YYYY-MM-DD.md`

Use parallel CC agents (group files by directory/subsystem) for speed if memory allows. **Run sequentially on memory-constrained hosts.**

## Step 3: Consolidation & Prioritization

Merge findings from both audits into a prioritized action plan:

| Priority | Category | Criteria |
|----------|----------|----------|
| **P0** | Bug fixes | Runtime impact — broken endpoints, data corruption, crashes |
| **P1** | Dead code removal | Safe deletes that reduce confusion and LOC |
| **P2** | Data quality fixes | Dropped data, wrong defaults, double-logging |
| **P3** | Spec coverage | Write new specs for unspecced code (no code changes) |
| **P4** | Spec accuracy | Update existing specs to document code-exceeding-spec features |
| **P5** | Mechanical refactors | Renames, wiring, entity-scoping completion |
| **P6** | Architectural gaps | V2 features where code diverges from spec by design (defer) |

**Rules:**
- Bugs always get their own section with severity ratings
- "Code exceeding spec" = spec update, not code change
- Architectural divergences that are intentionally deferred (V2 work) go to P6 and are documented but not actioned
- Each priority level should be achievable in a single CC session

**Deliverable:** Recommendations section in the reverse audit report.

## Step 4: Execution

Execute fixes by priority tier (P0 first, P6 last or deferred).

**Per priority tier:**
1. **Log intent** to `memory/YYYY-MM-DD.md` — tier name, CC session name, what's being attempted
2. Write a task briefing for CC (see `references/cc-task-template.md`)
3. Launch CC session: `cat /tmp/task.md | claude -p --allowedTools 'Edit,Write,Read,Bash'`
4. Set up monitoring cron (every 5 min)
5. When CC completes: **log results** to daily memory — files changed, what was done, any issues
6. **Verify build before committing** — `dotnet build` must pass
7. If CC gets killed (OOM): check `git diff --stat`, verify build manually, fix any issues, log the incident
8. Commit with descriptive message referencing the priority tier
9. **Log commit hash** to daily memory

**Hard rules:**
- ⚠️ **ALWAYS verify `dotnet build` passes before committing.** No exceptions. CC may get OOM-killed mid-build-check.
- ⚠️ **ALWAYS log to daily memory file at every step.** Log intent before launch, results after completion, commit hash after commit. If the session dies, the log survives for recovery.
- One commit per priority tier (or logical grouping)

**Logging template for daily memory:**
```markdown
## [Priority Tier Name]
- CC session: [name] (launched ~HH:MM CST)
- Task: [brief description]
- Status: [RUNNING | ✅ COMPLETE | ❌ FAILED | ⚠️ KILLED]
- Files changed: [count]
- Key actions: [what was done]
- Issues: [any problems encountered]
- Committed as [hash]
```

## Step 5: Verification

After all tiers are complete, optionally run a quick re-audit to measure improvement:

- Compare counts: unspecced, divergent, dead code, bugs
- Verify delta matches expectations
- Document remaining gaps and whether they're P6/deferred or newly discovered

**Deliverable:** Updated audit files with comparison section.

## Logging

Every audit produces a complete trail in `memory/YYYY-MM-DD.md`:

- **Audit launch** — which audits are being run, baseline reference
- **Audit results** — summary counts, key findings
- **Each priority tier** — intent, CC session, results, issues, commit hash
- **Final summary** — total commits, total lines changed, what's resolved vs deferred

This is non-negotiable. The Feb 17-18 amnesia incident proved that unlogged work is lost work. Log-then-act: write what you're about to do BEFORE doing it, then update with results.

## Baseline Tracking

Always compare against the previous audit. Store audits as:
```
kitty-specs/000-project-context/
  spec-audit-YYYY-MM-DD.md      (forward)
  reverse-audit-YYYY-MM-DD.md   (reverse)
```

The executive summary table with deltas is the key metric:

```markdown
| Category | Previous | Current | Delta |
|----------|----------|---------|-------|
| Unspecced Code | 38 | 24 | -14 |
| Divergences | 12 | 7 | -5 |
| Dead Code | 14 | 8 | -6 |
| Bugs | 0 | 8 | +8 |
| Conformant | ~60 | ~120 | +60 |
```

## CC Task Briefing Template

See `references/cc-task-template.md` for the standard format for CC task briefings.
