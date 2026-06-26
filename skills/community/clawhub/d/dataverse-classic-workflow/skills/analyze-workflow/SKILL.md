# analyze-workflow

**Compare a Classic Workflow against a set of requirements and produce a
prioritized change list mapped to specific XAML edit points.** This is the
skill behind requests like "I'm updating my Change Request process — here
are the new requirements; tell me what to change."

---

## When to use

- "I'm updating my {process name}. Here are my new requirements: …. The
  current workflow is at …. What needs to change?"
- "Does this workflow meet these requirements?"
- "What's missing in this workflow given …?"
- "Find issues / gaps in this workflow"
- "Audit this workflow for performance / security / maintainability"
  (no specific requirements — use the patterns table from the trigger-types
  reference as the implicit checklist)

## Inputs

- **Required:** Path to a Classic Workflow XAML file (and optionally its
  `.xaml.data.xml` sibling).
- **Required (one of):**
  - A list of explicit requirements from the user (free text or a doc), OR
  - An implicit "audit for best practices" instruction (no requirements
    given).

## Outputs

A prioritized, actionable change list with:
1. **Recap** of the current workflow (≤ 10-line summary).
2. **Requirements coverage table** — each requirement vs current state.
3. **Recommended changes** in priority order, each with:
   - What to change (in plain English)
   - Where in the XAML (step name + element type)
   - Effort estimate: trivial / small / medium / large
   - Risk level: low / medium / high
   - Whether it requires deactivation, activation, or solution re-import
4. **Open questions** for the user where the requirements were ambiguous.

---

## Procedure

### Step 1 — Read the current workflow

Invoke the [read-workflow](../read-workflow/SKILL.md) procedure first.
You need the structured summary to reason about what changes apply where.
Do this even if the user is impatient — without the parse, recommendations
are guessing.

### Step 2 — Normalize the requirements

If the user pasted free-form requirements, restate them as a numbered list
of testable assertions. For each requirement, extract:
- **Trigger condition** ("when …")
- **Action** ("the workflow should …")
- **Constraint** ("but only if …")
- **Output** ("and notify …")

If the user just said "audit this", skip this step and use the patterns
table from
[reference/trigger-types.md §"Patterns to flag in summaries / reviews"](../../reference/trigger-types.md#patterns-to-flag-in-summaries--reviews)
as the implicit requirement set.

### Step 3 — Build the coverage table

For each requirement, check the parsed workflow:

| Requirement state | What it means | Recommended action |
|-------------------|---------------|-------------------|
| ✅ Already satisfied | An existing step covers it correctly | None |
| ⚠️ Partially satisfied | A step exists but conditions / fields differ | Modify existing step |
| ❌ Missing | No step covers this requirement | Add new step(s) |
| ⛔ Conflicting | An existing step contradicts the requirement | Remove or restructure |
| ❓ Ambiguous | The requirement isn't specific enough to map | Ask the user |

### Step 3a — Run the universal client-side validation rules

In addition to the user's requirements, every Classic Workflow can be checked
for a fixed set of structural problems that don't need a live org connection.
Report any failures as `⛔ Conflicting` or `⚠️ Partially satisfied` rows so
they land in the change plan.

| # | Rule | Severity if violated |
|---|---|---|
| 1 | Workflow has a non-empty display name | error |
| 2 | `PrimaryEntity` is set and is not `none` | error |
| 3 | If `Mode = Real-Time`, no `mxswa:ActivityReference` whose AQN starts with `…ConditionSequence` has `Wait="[True]"` (Wait Conditions are background-only) | error |
| 4 | If `triggertypemask` includes Update, `triggeronupdateattributelist` is non-empty (otherwise the workflow fires on every update) | warning |
| 5 | Every `mxswa:SendEmail` has at least one recipient (`To`, `Cc`, or `Bcc` resolves to a non-empty value) | error |
| 6 | Every Check Condition has at least one branch with at least one child step | warning |
| 7 | Every `mxswa:CreateEntity` for an ownable entity sets either an `OwnerId` field or relies on the workflow `RunAs` (otherwise records will be owned by the SYSTEM user, which often surprises users) | warning |
| 8 | Every `mxswa:StartChildWorkflow` references a workflow ID that is not the current workflow's ID (no self-recursion) | error |
| 9 | Every `mxswa:ActivityReference` element has a non-empty `AssemblyQualifiedName` (a missing AQN is corrupt XAML) | error |
| 10 | Every direct `mxswa:*` activity has a non-empty `DisplayName` (missing names will display as `(no name)` and confuse comparison/diff tooling) | warning |
| 11 | Every `EvaluateCondition` operator that is not `Null` or `NotNull` has a corresponding `Parameters` `EvaluateExpression` for its right operand | error |
| 12 | If `Scope = Organization`, the `RunAs` is `Owner` (not `CallingUser`) — otherwise the workflow may not have permission to read records outside the calling user's BU | warning |
| 13 | If the workflow is triggered by Update on a column AND issues an `mxswa:UpdateEntity` that writes the same column on the same record, there is a guard (Check Condition comparing old vs new value, or a "WorkflowProcessed" flag) — otherwise the engine's 16-runs-per-row infinite-loop kill switch will fire ([web-research §4](../../reference/web-research.md#4-infinite-loop-protection-the-16-in-a-short-window-rule)) | error |
| 14 | If `Mode = Real-Time`, no `Parallel Wait Branch` activity is present (real-time forbids parallel-wait, same as Wait Conditions) | error |
| 15 | If a Check Condition uses operator `Under` or `NotUnder`, the deployment notes flag a **Hierarchical relationship dependency** on the condition's entity — activation will fail in target orgs without a relationship marked Hierarchical ([web-research §8](../../reference/web-research.md#8-hierarchical-operators-under--not-under)) | warning |
| 16 | If multiple workflows in the solution all trigger on the same `PrimaryEntity` and Update of the same columns, flag a **lock contention risk** ("multiple workflows updating the same table") and recommend consolidating logic ([web-research §5 row 2](../../reference/web-research.md#5-authoritative-best-practice-list-from-ms-learn)) | warning |
| 17 | If `Mode = Background` and `Workflow Job Retention` is not set to "Automatically delete completed workflow jobs", flag the storage-growth recommendation ([web-research §5 row 6](../../reference/web-research.md#5-authoritative-best-practice-list-from-ms-learn)) | info |
| 18 | If logic is duplicated across multiple workflows (same sequence of activities with the same parameters), recommend extracting to a child workflow ([web-research §5 row 4](../../reference/web-research.md#5-authoritative-best-practice-list-from-ms-learn)) | info |

Anything **server-side** (entity actually exists, schema names valid, option
set values valid, child workflow ID exists, recipient queue ID exists) is
out of scope here — those checks need a live Dataverse connection. Note them
in the open-questions section if they look risky.

### Step 4 — Plan the edits

For each non-✅ row, draft the edit:
- **Type of change:** add step, modify step, remove step, change trigger,
  change scope/mode/runas, restructure conditions.
- **Where:** by step display name and ordinal position.
- **What activities are involved:** list the `mxswa:*` or
  `ActivityReference` elements that need to be added/modified/removed.
- **Effort estimate:**
  - *Trivial* — change a literal value or one expression.
  - *Small* — add/remove/reorder a single SDK activity step.
  - *Medium* — add or restructure a Check Condition with branches; change
    the trigger configuration.
  - *Large* — change `Mode` (Background ↔ Real-Time) or `PrimaryEntity`;
    split into multiple workflows; introduce custom activities.
- **Risk level:**
  - *Low* — change is local and reversible (e.g. update a subject line).
  - *Medium* — change affects branching or expressions used elsewhere.
  - *High* — change touches activation/security (`RunAs`, `Scope`,
    `Mode`, `Trigger`) or removes existing logic.

### Step 5 — Group edits by deployment unit

Note which changes can ride together vs which need separate deployments:
- All changes to a single workflow ride together — one deactivate / edit /
  activate cycle.
- Changes that introduce new custom activities require a plugin assembly
  deploy first.
- Changes to the workflow's Mode (Background ↔ Real-Time) are best done
  as a Copy-then-replace rather than an in-place edit, because activated
  workflow runs can't be paused mid-execution and waited for.

### Step 6 — Surface open questions

If the requirements left genuine ambiguity, list the questions explicitly
at the end. Don't fill in defaults silently. Examples:

- "Requirement 3 says 'notify the manager' — should that be the assignee's
  manager, the record owner's manager, or a fixed user?"
- "Requirement 5 says 'after a delay' — how long? (Real-Time mode can't
  wait; this would force Background mode.)"
- "Requirement 7 needs a custom calculation — should I assume an existing
  custom workflow activity, or write the math inline as a VB expression?"

---

## Output template

````
# Change Plan — {Workflow Display Name}

## Current state (summary)

{≤10-line recap from read-workflow}

## Requirements coverage

| # | Requirement | State | Action |
|---|-------------|-------|--------|
| 1 | {restated requirement} | ✅ Already satisfied | None |
| 2 | {restated requirement} | ❌ Missing | Add SendEmail step after Check Condition's True branch |
| 3 | {restated requirement} | ⚠️ Partially satisfied — uses wrong field | Update SetEntityProperty target |
| 4 | {restated requirement} | ❓ Ambiguous | See open questions |

## Recommended changes (priority order)

### 1. {Change title} — Effort: {S/M/L} • Risk: {L/M/H}
**What:** {plain-English description}
**Where:** Step "{step display name}" (a `mxswa:UpdateEntity` at position 4 of the root Sequence)
**Why:** {requirement number it satisfies / problem it fixes}
**XAML hint:** {one-sentence pointer like "Add an `mxswa:SendEmail` after the existing `UpdateEntity`"}

### 2. {…}
…

## Deployment notes

- All changes can deploy in **{N}** activate/deactivate cycle(s).
- {any plugin / custom activity dependencies}
- {any breaking changes that justify Copy-then-replace}

## Open questions

1. {question}
2. {question}

(Once you answer these, I can produce the actual edits with the
[write-workflow](../write-workflow/SKILL.md) skill.)
````

---

## Don't

- Don't make the edits in this skill — that's the `write-workflow` skill's
  job. Stop at recommendations.
- Don't assume requirements. If something's ambiguous, list it as an open
  question rather than picking a default.
- Don't propose changes that the format doesn't support (e.g. "add a Wait
  Condition to a Real-Time workflow"). Flag the conflict instead.
- Don't conflate "best practices" with "user requirements". If the user
  gave specific requirements, those win. Best-practice findings go in a
  separate section labeled `## Additional findings (not in your requirements)`.
