# compare-workflows

**Diff two Classic Workflow XAML files and explain what changed in
human-readable form.** Useful when comparing an old workflow to a new
template-based copy, or comparing two branches of the same workflow.

---

## When to use

- "What changed between version A and B of this workflow?"
- "Compare `old/MyProcess.xaml` to `new/MyProcess.xaml`"
- "I made a copy via the workflow-template route — how does my copy differ
  from the original?"
- "What's different about the workflow in branch `feature/x` vs `main`?"

## Inputs

- **Required:** Two paths to Classic Workflow XAML files.
- **Optional:** The two `.xaml.data.xml` siblings (for metadata-level diff).
- **Optional:** A label for each side (e.g. "old" vs "new", "production"
  vs "draft", "before refactor" vs "after refactor"). Default labels
  are "A" and "B".

## Outputs

A diff report with:
1. **Metadata diff** — name, primary entity, trigger, scope, mode, run-as.
2. **Structural diff** — added / removed / reordered steps.
3. **Step-level diff** — for each step that exists in both, what changed
   inside it (field assignments, conditions, expressions).
4. **Cosmetic diff** — display name changes, comment updates, UserData
   changes (collapsed; user can expand if curious).
5. **Risk-flagged callouts** — changes the user should pay extra attention
   to (Mode change, Scope change, Trigger change, RunAs change, condition
   logic change).

---

## Procedure

### Step 1 — Parse both sides

Run the [read-workflow](../read-workflow/SKILL.md) procedure on each file.
This gives you two structured representations to diff.

### Step 2 — Match steps across the two sides

Steps don't have stable IDs across copies. Match them with this priority:

1. **By DisplayName** — exact match wins.
2. **By position** — if two unmatched steps occupy the same ordinal
   position, treat them as the same step.
3. **By type + key fields** — an `UpdateEntity` step on the same entity
   with overlapping field assignments is probably "the same step renamed".

When matching is ambiguous, surface it as a finding ("Step at position 4
in A could be either step 4 or step 5 in B; treating as renamed.").

### Step 3 — Diff metadata

Compare the metadata sibling fields:

| Field | A | B | Change |
|-------|---|---|--------|
| Name | … | … | (none / renamed) |
| PrimaryEntity | … | … | … |
| Mode | … | … | ⛔ Critical: changes execution semantics |
| Scope | … | … | ⚠️ Affects who can trigger |
| RunAs | … | … | ⚠️ Affects security |
| Trigger | … | … | ⚠️ Changes when it fires |
| Filtering attributes | … | … | … |

### Step 4 — Diff the step list

Produce three lists:

- **Added in B** — steps present in B but not A.
- **Removed from A** — steps present in A but not B.
- **Reordered** — steps present in both but in a different position.

For each entry, give the step type and friendly name.

### Step 5 — Diff matched steps

For each pair of matched steps, dive into the activity:
- **UpdateEntity / CreateEntity:** which fields are now assigned vs were
  assigned before? Which expressions changed?
- **SendEmail:** subject, body, recipients (from / to / cc).
- **Check Condition:** which branches' conditions changed? Did a branch
  get added or removed? Did the contents of a branch's body change?
- **Custom activity:** which input parameters changed?
- **Stop Workflow:** status (Succeeded / Canceled) and message.

For expressions, render in friendly form (per
[reference/vb-expressions.md](../../reference/vb-expressions.md)) — show
the before and after side by side.

### Step 6 — Filter cosmetic differences

The following are usually noise and should be collapsed unless the user
asks for them explicitly:
- `UserData` blob changes (designer state).
- Whitespace and indentation changes.
- `mva:VisualBasicValue` metadata blob changes (if the actual VB
  expression text is unchanged).
- Reordering of attributes within a single element.

Surface a one-line summary: "Plus N cosmetic / metadata changes (collapsed)."

### Step 7 — Flag high-risk diffs

Add a "Critical / Risk callouts" section for any of:
- Mode change (Background ↔ Real-Time).
- Scope change.
- RunAs change.
- Trigger bitmask change (different trigger types).
- Removed Stop Workflow steps.
- Added or removed Check Condition branches (changes the logic flow).
- Added child workflow calls (`StartChildWorkflow`).
- Removed filtering attributes on an OnUpdate trigger.

---

## Output template

````
# Workflow Diff — {Label A} ↔ {Label B}

## Metadata

| Field | {Label A} | {Label B} |
|-------|-----------|-----------|
| Name | … | … |
| Primary entity | … | … |
| Mode | Background | Real-Time ⛔ |
| Scope | Organization | Organization |
| Run as | Owner | Owner |
| Trigger | OnCreate, OnUpdate | OnCreate |
| Filtering attributes | name, statuscode | (removed) ⚠️ |

## Step changes

### Added in {Label B}
- Step 4: **Send approval email** (`mxswa:SendEmail`)
- Step 6: **Check Condition: Region is EU** (`ConditionSequence`)

### Removed from {Label A}
- Step 3 was: **Set legacy flag** (`mxswa:UpdateEntity`)

### Reordered
- "Update status" moved from position 5 → position 7.

## Step-level changes

### Step 2 — "Update account" (`mxswa:UpdateEntity`)
- Field `description`:
  - {Label A}: `"Reviewed by " & {User: Full Name}`
  - {Label B}: `"Reviewed on " & {Now} & " by " & {User: Full Name}`
- Field `prioritycode` removed from assignments.

### Step 5 — "Check Condition: Status changed"
- Branch "Yes":
  - **Added:** SendEmail step.
  - **Modified:** Update step now also sets `lastreviewdate`.
- Branch "Else": unchanged.

## Critical / Risk callouts

- ⛔ **Mode changed Background → Real-Time.** All `Persist` and Wait
  activities must be removed (they were not detected in this workflow,
  so this is safe — but verify external calls don't block the user save).
- ⚠️ **Filtering attributes removed.** The OnUpdate trigger will now
  fire on every update to the entity — significant performance impact.

## Cosmetic / metadata

Plus 14 cosmetic changes (designer state, whitespace, expression metadata).
Run with `--include-cosmetic` to see them.
````

---

## Don't

- Don't show raw XAML diffs unless the user asks for them. The point of
  this skill is human-readable explanation.
- Don't claim a step is "the same" when matching is uncertain — surface
  the ambiguity.
- Don't echo the user's real entity logical names or workflow names into
  generated example output. Diff results that reference the user's actual
  workflow are fine (you're diffing their files); examples in
  documentation must use placeholders.
