# Phase 6: Internal Review

## Goal

Perform comprehensive internal review of the DVP to identify omissions, inconsistencies, and quality issues before finalization.

## Read Previous Phase

Before starting Phase 6 work, read these files from `dvp_workspace/`:

- `dvp_content.json` (Phase 5) — The DVP content to review
- `checks-final.md` (Phase 4) — The authoritative check list (for cross-referencing)
- `scope.md` (Phase 2) — Scope definition for completeness check
- `key-data.md` (Phase 2) — Key data for coverage verification
- `risk-assessment.md` (Phase 2) — Risk areas for coverage verification
- `assumptions-and-gaps.md` — Assumptions for review

## Deliverables

Before the [Done] step, write the following files to `dvp_workspace/`:

| File | Content |
|------|---------|
| `review-report.md` | Review findings organized by severity (Must Fix / Should Fix / Nice to Have), with handling results for each finding |

If corrections were made during the review:
- Update `dvp_content.json` with the corrected content
- Re-run `scripts/generate_xlsx.py` to regenerate the Excel
- Update `checks-final.md` if any checks were added, removed, or modified

## Interaction Guide

Follow the Interaction Protocol defined in `SKILL.md`. This phase primarily uses **[Conflict]**, **[Confirm]**, and **[Done]** question types.

| Decision point | Level | Notes |
|----------------|-------|-------|
| Must-fix item changes | Must-ask | Must get approval before modifying |
| Should-fix item adoption | Recommend | Suggest fix, user confirms |
| Nice-to-have improvements | Self-decide | Default: no change unless user requests |
| Numbering/ID fixes | Self-decide | Fix automatically |

## Review Dimensions

For each dimension, perform the verification method specified. If any check item fails, record it as a finding with the severity level indicated.

### 1. Completeness Check

Verification method: Cross-reference `checks-final.md` against `scope.md`, `key-data.md`, and `risk-assessment.md`.

- [ ] All modules classified as `DVP Check` in `scope.md` have at least one check in `checks-final.md`. **Fail condition: Module with no checks → Must Fix.**
- [ ] All variables listed in `key-data.md` have at least one associated check. **Fail condition: Key variable with no check → Must Fix.**
- [ ] All areas rated `High` in `risk-assessment.md` have at least 3 checks. **Fail condition: High-risk area with fewer than 3 checks → Should Fix.**
- [ ] At least one Cross-Module category check exists per pair of related modules. **Fail condition: No cross-module check between related domains → Should Fix.**
- [ ] If external data sources are listed in `scope.md`, at least one Reconciliation check exists per source. **Fail condition: External source with no reconciliation check → Should Fix.**

### 2. Logic Consistency

Verification method: Compare every pair of checks within the same module for duplicate or contradictory logic.

- [ ] No two checks have identical `logic` field values. **Fail condition: Duplicate logic found → Must Fix (merge or remove).**
- [ ] No two checks produce contradictory requirements (one requires X, another requires not-X for the same condition). **Fail condition: Contradiction found → Must Fix.**
- [ ] No DVP check duplicates logic already covered by edit checks in `edit-check-overlap.md` unless marked as intentional. **Fail condition: Unintentional overlap → Should Fix.**
- [ ] Date comparison logic uses consistent reference dates across modules. **Fail condition: Inconsistent date baseline across modules → Should Fix.**
- [ ] Checks with the same category and similar scope have consistent severity grading. **Fail condition: Similar checks with different severity and no documented rationale → Should Fix.**

### 3. Expression Quality

Verification method: Read each check's description, logic, and query wording.

- [ ] Every Description follows the pattern `{Category}: {specific finding}`. **Fail condition: Description does not state the category or is vague → Should Fix.**
- [ ] Every Logic Rule is a boolean expression using field names. **Fail condition: Logic is narrative text rather than a testable condition → Must Fix.**
- [ ] Every Query Wording follows the template `[Specific finding]. Please [expected action].` **Fail condition: Query uses generic phrase without specifics → Should Fix.**
- [ ] No undefined abbreviations in any field. **Fail condition: Undefined abbreviation → Nice to Have.**

### 4. Numbering Standards

Verification method: Extract all Check IDs, group by module prefix, and verify sequential ordering.

- [ ] Every Check ID matches the format `{MODULE_PREFIX}-{NNN}`. **Fail condition: Non-standard format → Must Fix.**
- [ ] Within each module prefix, NNN values are sequential with no gaps. **Fail condition: Gap in numbering → Must Fix.**
- [ ] No two checks share the same Check ID. **Fail condition: Duplicate ID → Must Fix.**
- [ ] All checks for the same module use the same prefix. **Fail condition: Mixed prefixes for one module → Must Fix.**

### 5. Risk Coverage

Verification method: Map checks to risk areas from `risk-assessment.md` and verify density.

- [ ] Safety-critical data (AE/SAE, Death, Discontinuation) has at least one Critical-severity check. **Fail condition: Safety module with no Critical check → Must Fix.**
- [ ] Primary endpoint data identified in `key-data.md` has at least 2 checks. **Fail condition: Primary endpoint with fewer than 2 checks → Must Fix.**
- [ ] SAE/Death reporting timeline requirements have a corresponding Timeline check. **Fail condition: No SAE timeline check → Must Fix.**
- [ ] Inclusion/exclusion violation detection has at least one Consistency check. **Fail condition: No I/E violation check → Should Fix.**

## Sub-Tasks

At the start of this phase, create the following sub-tasks. Each should `addBlockedBy` the Phase 6 task ID. Mark each `completed` when its step finishes.

| # | subject | description |
|---|---------|-------------|
| 1 | Automated Review | Run through all review dimensions systematically |
| 2 | Present Findings | Present Must Fix, Should Fix, and Nice to Have items |
| 3 | Address Issues | Apply approved changes and verify no regressions |
| 4 | Final Verification | Re-verify IDs, counts, and regenerate Excel if needed |
| 5 | Present Final DVP | Present finalized DVP with review completion summary |

#### Decomposition

- **Sub-task 1: Automated Review** — Decompose by review dimension (Completeness, Logic Consistency, Expression Quality, Numbering Standards, Risk Coverage). Always decompose this sub-task — there are always exactly 5 dimensions.
- **Sub-task 3: Address Issues** — Decompose by finding when 3+ findings exist (e.g., `Address Issues: AE-008 duplicate logic`).

## Steps

### Step 1: Automated Review

**[Self-decide]** Run through the review checklist above systematically. For each dimension:
- Flag specific issues with Check IDs
- Categorize by severity (Must Fix, Should Fix, Nice to Have)
- Provide specific recommendations

### Step 2: Present Findings

**[Conflict]** For Must Fix items, present one by one for approval:
```
[Conflict] [Check ID] [issue — e.g., Duplicate logic]
  Finding: [AE-008 and AE-012 share the same logic]
  Suggested resolution: Merge into one check — [keep AE-008, remove AE-012]
  Please confirm: adopt suggestion / other approach
```

**[Confirm]** For Should Fix items, batch into one recommendation:
```
[Confirm] Should Fix items (recommended changes)
  The following issues are recommended for fixing but do not affect core correctness:
  1. [CM-003] Query wording is too generic, recommend changing to "[specific wording]"
  2. [VS-005] Visit window definition conflicts with VS-009, recommend unifying to [...]
  ...
  Please confirm: adopt all / adopt selected (please specify) / skip for now
```

Nice to Have items are listed but not actioned by default.

### Step 3: Address Issues

**[Self-decide]** For each approved change:
1. Apply the change
2. Re-run the relevant Review Dimension checks for the affected module: verify no new duplicate IDs, no new logic contradictions, and no broken sequential numbering. If a new issue is introduced, revert the change and flag for [Must-ask].

### Step 4: Final Verification

**[Self-decide]** After all issues are resolved:
1. Re-verify Check ID sequence
2. Confirm total check count
3. If any corrections were made:
   a. Update `dvp_content.json` in `dvp_workspace/`
   b. Re-run `scripts/generate_xlsx.py` to regenerate the Excel
   c. Update `checks-final.md` if checks changed

### Step 5: Present Final DVP

Before presenting the summary, write the `review-report.md` deliverable to `dvp_workspace/`. If corrections were made, also update `dvp_content.json` and regenerate the Excel.

**[Done]** Present the finalized DVP:
- Final check count summary
- Review completion confirmation
- Updated Excel file path
- List of changes made during review

```
[Done] Phase 6: Internal Review
  Deliverables written to dvp_workspace/:
  - review-report.md — Review findings and handling results
  - dvp_content.json — [Updated / No changes]
  - DVP_<ProtocolNumber>_v1.0.xlsx — [Regenerated / No changes]

  Output summary:
  - Final check rule count: [N]
  - Review results: [N] Must Fix corrected / [N] Should Fix adopted / [N] Nice to Have unchanged
  - Output file: dvp_workspace/DVP_<ProtocolNumber>_v1.0.xlsx
  - Review complete — DVP is ready for distribution and team review
```

The DVP is now ready for distribution and team review.

**Task update**: Mark Phase 6 task as `completed`. All tasks are now done.

## Tips

- Review should be thorough but practical — not every check needs to be perfect on first draft.
- Prioritize must-fix issues (duplicates, contradictions, missing safety checks).
- Document all review findings for audit trail purposes.
- If the user wants to skip certain review items, document the decision and rationale.
