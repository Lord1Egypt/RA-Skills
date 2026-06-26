# read-workflow

**Parse a Dataverse Classic Workflow XAML file and produce a human-readable
summary.** This is almost always the first skill to invoke — every other skill
depends on understanding the workflow's structure first.

---

## When to use

- "What does this workflow do?"
- "Summarize the workflow at `<path>`"
- "List the steps in this workflow"
- "What entity does this workflow run on?"
- "Show me the trigger conditions"
- Any time another skill (analyze, compare, write) needs to first understand
  the workflow before acting.

## Inputs

- **Required:** Path to a `.xaml` file containing a Classic Workflow.
- **Optional:** Path to the sibling `.xaml.data.xml` metadata file. If
  present, it provides the workflow's name, primary entity, trigger
  bitmask, scope, mode, run-as, and statecode in friendlier form than the
  XAML.

## Outputs

A structured summary containing:
1. **Header** — name, primary entity, category (must be Classic Workflow), mode.
2. **Activation context** — trigger(s), filtering attributes, scope, run-as.
3. **State** — Draft vs Activated.
4. **Step list** — ordered, friendly descriptions of each user-visible step.
5. **Findings** — any patterns from `reference/trigger-types.md` worth
   flagging (e.g. OnUpdate without filters).

---

## Procedure

### Step 1 — Locate and confirm the file

1. If the user gave a path, read it. If they didn't, ask: "Which workflow
   file? They're typically under `<solution>/src/Workflows/*.xaml` after
   `pac solution unpack`."
2. Read the file's first ~50 lines.
3. Confirm it's a Classic Workflow:
   - Root must be `<mxswa:Activity>` containing `<mxswa:Workflow>`.
   - If you see `BusinessProcessFlow` or `BusinessRule` in the root,
     **stop** and tell the user: "This is a [BPF/Business Rule], not a
     Classic Workflow. This agent doesn't handle that category."

### Step 2 — Read the metadata sibling (if present)

Look for a `<file-stem>.xaml.data.xml` next to the XAML. It typically
contains XML elements for `name`, `primaryentity`, `category`, `mode`,
`scope`, `runas`, `triggertypemask`, `triggeronupdateattributelist`,
`statecode`, `statuscode`. Use these as the canonical source for header
metadata; fall back to the XAML root attributes if the sibling is missing.

### Step 3 — Parse the activity tree

Read the entire XAML. Walk the tree from `<mxswa:Workflow>` → `<Sequence>`
and collect activities. Apply these rules from
[reference/xaml-anatomy.md](../../reference/xaml-anatomy.md):

- **Direct `mxswa:*` elements** → user-visible steps.
- **Direct `mcwc:*` elements** → user-visible form-side steps.
- **`mxswa:ActivityReference`** → look at `AssemblyQualifiedName`:
  - `…ConditionSequence…` → "Check Condition" (or "Wait Condition" if
    `Wait="True"`).
  - `…ConditionBranch…` → branch under a condition; render each branch's
    children as a nested list.
  - `…Composite…` → step group; render the group's children as nested
    steps under the Composite's `DisplayName`.
  - `…TerminateWorkflow…` → "Stop Workflow" with success/cancel reason.
- **Internal helpers** (`EvaluateExpression`, `EvaluateCondition`,
  `EvaluateLogicalCondition`, `GetEntityProperty`, `SetEntityProperty`,
  `RetrieveEntity`, `Persist`, `ConvertCrmXrmTypes`) → **collapse** into
  the user-visible step they belong to. Don't emit them as separate steps.

### Step 3a — Recognize user-visible steps by their activity-tree fingerprint

The legacy designer treats certain combinations of low-level activities as
a single user-visible step. When you see one of these fingerprints inside a
`Sequence` or `Composite`, render it as **one** step and skip the children
you rolled up:

| Fingerprint (activities present in the same Sequence/Composite) | Render as |
|---|---|
| `mxswa:UpdateEntity` + one or more `mxswa:SetEntityProperty` (and the `EvaluateExpression` instances feeding them) | **"Update Record"** — one step. Surface the entity name from `UpdateEntity` and the field/value pairs in friendly form. |
| `mxswa:CreateEntity` + one or more `mxswa:SetEntityProperty` | **"Create Record"** — one step. Same field/value rendering as Update. |
| `mxswa:CreateEntity` (with `EntityName="email"`) + `mxswa:SendEmail` | **"Send Email"** — one step. Surface To / Cc / Subject / Body. |
| Bare `mxswa:SendEmail` referencing a previously-created email variable | **"Send Email"** (using existing email record) |
| `mxswa:ActivityReference` AQN starts with `…ConditionSequence` and `Wait` is `[False]` or absent | **"Check Condition"** — render its branches |
| Same shape, but `Wait="[True]"` | **"Wait Condition"** — background-only; render the wait predicate |
| `mxswa:ActivityReference` AQN starts with `…TerminateWorkflow` or `…StopWorkflow` | **"Stop Workflow"** — surface success/cancel + reason |
| `mxswa:ActivityReference` to `…PerformAction` | **"Run Action: <ActionName>"** — surface the input parameter mapping |
| `mxswa:ActivityReference` to a Composite with a `DisplayName` | A **named step group** — render the DisplayName as a heading and recurse into its children |
| `mxswa:ActivityReference` to a Composite **without** a DisplayName | An anonymous group — render its children inline at the parent level |

If you see an unrecognized AQN class name (one not listed in
[reference/activity-types.md §4](../../reference/activity-types.md#4-conditions-and-branching)
or any of the BPF-internal classes called out there), treat it as a
Custom CodeActivity and surface the AQN to the user.

### Step 4 — Render expressions in friendly form

For any VB bracket expression you encounter (subject lines, condition
operands, field assignments), render it in friendly token form per
[reference/vb-expressions.md](../../reference/vb-expressions.md):

- `GetVariableValue(EntityProperty("name", "account"), "")` → `{Account: Name}`
- `[True]` / `[False]` → `True` / `False`
- A literal string → render the literal in quotes.
- An expression you can't simplify → render as `{expression: <truncated VB code>}`.

### Step 5 — Surface findings

Run the workflow against the patterns table in
[reference/trigger-types.md §"Patterns to flag in summaries / reviews"](../../reference/trigger-types.md#patterns-to-flag-in-summaries--reviews).
Report any matches as a "Findings" section at the bottom of the summary.

---

## Output template

````
# {Workflow Display Name}

**Primary entity:** `{logical_name}`
**Category:** Classic Workflow
**Mode:** Background | Real-Time
**State:** Draft | Activated

## Trigger
- Trigger types: {OnCreate, OnUpdate, …}
- Filtering attributes (for OnUpdate): {list, or "(none — fires on every update)"}
- Scope: {User | BusinessUnit | ParentChildBU | Organization}
- Run as: {Owner | CallingUser}

## Steps

1. **{Step display name}** — {plain-English description}
   - {sub-detail like "Set name to {Account: Name} & ' (reviewed)'"}
2. **Check Condition: {description}**
   - **If True:**
     1. {nested step}
     2. {nested step}
   - **Else:**
     1. {nested step}
3. **Stop Workflow** — Status: Canceled. Reason: "{message}"

## Findings

- ⚠️ {finding} ({severity})
- …

(Or "No issues detected." if the workflow looks clean.)
````

---

## Error handling

- **File not found** → ask the user to confirm the path. Suggest running
  `pac solution unpack` if they haven't.
- **Invalid XAML** (parse error) → report the parse error verbatim. Do
  not try to "fix" it silently. Ask the user to share the error message
  with the source they exported from.
- **Wrong category** (BPF, Business Rule, Modern Flow) → as in Step 1,
  stop and explain.
- **Activity types you don't recognize** → look them up in
  [reference/activity-types.md](../../reference/activity-types.md). If
  still unknown, treat them as Custom CodeActivity (Section 8 of that
  reference) and surface the AssemblyQualifiedName.

---

## Don't

- Don't emit XAML in your summary unless the user asks for it. The point
  of this skill is human-readable output.
- Don't echo the user's real entity logical names back into a generated
  example. References in prose are fine; synthetic XAML examples must use
  placeholders.
- Don't silently drop activity types. If you collapse a helper, mention
  it ("Includes a checkpoint after step 3"). If you skip something
  unrecognized, say so.
