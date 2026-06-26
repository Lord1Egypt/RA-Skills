# Phase 4: Alignment

## Goal

Confirm that all designed check rules are correct, feasible, and do not conflict with existing systems or analysis plans. Resolve any issues before drafting.

## Read Previous Phase

Before starting Phase 4 work, read these files from `dvp_workspace/`:

- `checks.md` (Phase 3) — The check list to be aligned
- `check-rationale.md` (Phase 3) — Design decisions to review
- `unresolved.md` (Phase 3) — Items to resolve in this phase
- `scope.md` (Phase 2) — Scope boundaries for alignment verification
- `key-data.md` (Phase 2) — Key data for coverage verification
- `risk-assessment.md` (Phase 2) — Risk areas for coverage verification
- `materials-received.md` (Phase 1) — Available materials (for checking evidence)
- `assumptions-and-gaps.md` — Resolve what you can here

Resolve items from `unresolved.md` during this phase. For each resolved item, update `assumptions-and-gaps.md` to mark it as Resolved.

## Deliverables

Before the [Done] step, write the following files to `dvp_workspace/`:

| File | Content |
|------|---------|
| `checks-final.md` | Aligned final check list (replaces `checks.md` from Phase 3). Same 10-field structure per check. This is the authoritative check list for downstream phases. |
| `alignment-report.md` | Corrections made: which checks were deleted, merged, or modified and why; conflict resolution results |
| `edit-check-overlap.md` | Overlap analysis with existing Edit Checks and handling decision for each overlap |

Also update `assumptions-and-gaps.md` to mark resolved items and add any new items discovered during alignment.

## Interaction Guide

Follow the Interaction Protocol defined in `SKILL.md`. This phase primarily uses **[Conflict]**, **[Confirm]**, and **[Done]** question types.

| Decision point | Level | Notes |
|----------------|-------|-------|
| Overlapping check resolution (keep/merge/remove) | Must-ask | Affects DVP structure |
| Feasibility issue trade-offs | Must-ask | Affects whether checks can execute |
| Contradictory checks | Must-ask | Must be resolved before drafting |
| Query burden assessment | Recommend | Suggest consolidation, user confirms |
| Low-priority rule consolidation | Recommend | Suggest removal, user confirms |
| Numbering corrections | Self-decide | Fix automatically |
| Wording refinements | Self-decide | Improve automatically |

## Sub-Tasks

At the start of this phase, create the following sub-tasks. Each should `addBlockedBy` the Phase 4 task ID. Mark each `completed` when its step finishes.

| # | subject | description |
|---|---------|-------------|
| 1 | Protocol Alignment Review | Verify check logic aligns with protocol requirements |
| 2 | SAP/Analysis Alignment | Verify checks support analysis needs |
| 3 | Edit Check Conflict Check | Identify and resolve overlaps with existing edit checks |
| 4 | Database Feasibility | Assess whether checks can execute against the database |
| 5 | Query Burden Assessment | Evaluate and optimize query volume |
| 6 | Present Alignment Results | Output alignment report and confirm completion |

#### Decomposition

- **Sub-task 1: Protocol Alignment Review** — Decompose by module when total check count exceeds 15 (e.g., `Protocol Alignment Review: AE/SAE`).
- **Sub-task 4: Database Feasibility** — Decompose by module when total check count exceeds 15 (e.g., `Database Feasibility: Lab`).

## Steps

### Step 1: Protocol Alignment Review

**[Self-decide]** For each check rule, perform these verifications:
- Logic verification: Extract the protocol requirement text that supports the check logic. If no supporting text exists, flag for [Must-ask].
- Trigger verification: Confirm the Trigger Condition corresponds to a protocol-defined event (data entry, scheduled visit, external data receipt). If the trigger has no protocol basis, flag for [Must-ask].
- Scope verification: Confirm the Applicable Scope population is a subset of the study population defined in `study-overview.md`. If the scope references visits or conditions not in `visit-schedule.md`, flag for [Must-ask].
- Contradiction check: For each pair of checks in the same module, confirm both checks CAN simultaneously pass. If they cannot, flag as a conflict.

**[Must-ask]** If any checks cannot be verified from the protocol, flag for confirmation:
```
[Conflict] [Check ID] Protocol alignment issue
  Finding: [This check's logic depends on protocol requirement X, but the protocol text is ambiguous]
  Suggested resolution: [Interpret as Y / Remove this check]
  Please confirm: adopt suggestion / provide the correct interpretation
```

### Step 2: SAP/Analysis Alignment

**[Self-decide]** If SAP is available:
- Verify that checks support (not conflict with) analysis needs
- Confirm that endpoint-related checks match SAP definitions
- Check that derived variables are validated consistently with analysis derivation rules

### Step 3: Edit Check Conflict Check

**[Must-ask]** Compare DVP checks against known edit checks. For each conflict found:
```
[Conflict] [Check ID] Overlap with existing Edit Check
  Finding: [DVP check logic duplicates Edit Check #EC-XXX]
  Suggested resolution: Remove — [this logic is already covered by the edit check]
  Alternative: Keep as a supplementary check
  Please confirm: adopt suggestion / keep / merge
```

Batch all conflict items into one prompt.

### Step 4: Database Feasibility

**[Self-decide]** For each check, assess:
- Can the required fields be queried from the database?
- Are the referenced variables available and correctly named?
- Is the execution method feasible (SAS, listing, manual)?

**[Must-ask]** If feasibility issues are found:
```
[Conflict] [Check ID] Database feasibility issue
  Finding: [Required field Y does not exist in the database / execution method is not feasible]
  Suggested resolution: [Change execution method / Remove this check / Adjust logic]
  Please confirm: adopt suggestion / other approach
```

### Step 5: Query Burden Assessment

**[Recommend]** Evaluate:
- Are there checks that would generate excessive queries?
- Can any checks be consolidated to reduce query volume?
- Are query wordings clear enough to avoid back-and-forth with sites?

```
[Confirm] Query burden assessment
  Recommendation: Merge [Check A] and [Check B] to reduce query volume
  Rationale: Both checks share similar logic; merging preserves coverage while reducing ~[N] queries
  Alternative: Keep them separate
  Please confirm whether to adopt the recommendation.
```

### Step 6: Present Alignment Results

Before presenting the summary, write all three deliverable files listed in the Deliverables section above to `dvp_workspace/`. Also update `assumptions-and-gaps.md` to mark resolved items.

**[Done]** Output a structured alignment report:

```
[Done] Phase 4: Alignment
  Deliverables written to dvp_workspace/:
  - checks-final.md — Aligned final check list
  - alignment-report.md — Corrections and resolution log
  - edit-check-overlap.md — Edit check overlap analysis
  - assumptions-and-gaps.md — [Updated / No changes]

  Output summary:
  - Protocol alignment: [N] confirmed / [N] corrected
  - Edit Check conflicts: [N] overlaps resolved ([N] removed / [N] merged / [N] kept)
  - Feasibility issues: [N] resolved
  - Query burden: [N] optimizations applied
  - Final check rule count: [N]

  Next: Phase 5: Draft
  Will proceed after your confirmation. Let me know if adjustments are needed.
```

Wait for user confirmation before proceeding to Phase 5.

**Task update**: Mark Phase 4 task as `completed`. Mark Phase 5 task as `in_progress`.

## Rules

- If a [Must-ask] conflict cannot be resolved in one exchange, MUST continue the discussion until resolution. MUST NOT skip unresolved items.
- When flagging a protocol alignment issue, MUST cite the specific protocol section number or page in the Finding description.
- If a check is rated Minor severity AND its estimated trigger rate exceeds 30% of records, MUST recommend removal at the [Done] step with rationale.
- MUST record every alignment decision (keep/merge/remove) and its rationale in `alignment-report.md`. MUST NOT make silent changes without a corresponding entry.
