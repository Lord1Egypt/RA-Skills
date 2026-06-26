# write-workflow

**Edit Classic Workflow XAML safely, preserving WF4 round-trip fidelity.**
This is the skill behind requests like "add a step", "modify this
condition", "change the email subject", or "remove this branch".

> ⚠️ This skill modifies files. Always show the user the planned change
> and get explicit confirmation before writing.

---

## When to use

- "Add a Send Email step after the approval check"
- "Change the email subject to …"
- "Remove this Stop Workflow step"
- "Add a new branch to this Check Condition"
- "Update this field's expression"
- "Rename this step"

## When NOT to use

- The user wants to *plan* changes — that's the
  [analyze-workflow](../analyze-workflow/SKILL.md) skill. Use this skill
  only when they're ready to make the change.
- The user wants to convert a workflow's `Mode` (Background ↔ Real-Time)
  or change `PrimaryEntity` — these are best done in the legacy designer,
  or by deleting and re-creating, because the affected XAML changes are
  pervasive and risky. Push back politely if asked.
- The XAML uses Custom CodeActivity types — you can change their input
  expressions, but do not modify their parameter shape (the consuming
  assembly's contract may break).

## Inputs

- **Required:** Path to the workflow XAML file.
- **Required:** A description of the edit.
- **Strongly recommended:** Output of the [read-workflow](../read-workflow/SKILL.md)
  skill on the same file (so you and the user share an understanding of
  the current state).

## Outputs

1. A **planned diff** shown to the user before writing.
2. **The edited file** (after confirmation).
3. A **post-edit summary** confirming what changed and pointing out any
   follow-up actions (re-activation, re-import, etc.).

---

## Procedure

### Step 1 — Read the file in full

Always read the whole XAML file before any edit. You need:
- The full namespace declaration block (so you preserve every `xmlns:*`).
- The exact `AssemblyQualifiedName` strings used in `ActivityReference`
  elements (you'll reuse these when generating new ConditionSequence /
  Composite / TerminateWorkflow nodes — copy verbatim, don't reconstruct).
- The indentation style (tabs vs spaces, count).
- The line ending style (CRLF vs LF).

### Step 2 — Locate the edit point precisely

Identify by:
1. **Step display name** — e.g. "after the step named 'Check approval'".
2. **Step type** — e.g. "the `mxswa:SendEmail` inside the True branch".
3. **Position** — e.g. "the 4th child of the root `<Sequence>`".

If the user's description is ambiguous, ask. Do not guess.

### Step 3 — Plan the edit

Write out the edit in plain English first, then translate to XAML
operations:

| User intent | XAML operation |
|-------------|----------------|
| "Add a step after X" | Insert a new sibling element after X in its parent Sequence |
| "Add a step inside the True branch of condition Y" | Insert into the `Sequence` body of Y's first ConditionBranch |
| "Remove step Z" | Delete the element and its trailing whitespace |
| "Change the subject of the email step" | Modify the `Subject` `InArgument` content |
| "Change a condition's right operand" | Locate the EvaluateCondition and replace the RightOperand `InArgument` content |
| "Rename a step" | Update the element's `DisplayName` attribute (and the matching `UserData` entry if present) |
| "Add an Else branch" | Append a new `ConditionBranch` (without a condition) inside the ConditionSequence |

Reference [reference/activity-types.md](../../reference/activity-types.md) for the
correct element / `AssemblyQualifiedName` for whatever you're inserting.

### Step 4 — Generate XAML for additions

When inserting new elements, **copy the namespace prefixes used by the
file** (don't add new ones) and follow the templates in
[reference/activity-types.md](../../reference/activity-types.md).

Critical templates to get right:

**Adding an SDK activity (e.g. SendEmail):**
```xml
<mxswa:SendEmail
    DisplayName="Send notification"
    EmailId="[createdEmailRef]" />
```

**Adding a Composite (step group), Check Condition, or Stop Workflow:**
Always wrap in `<mxswa:ActivityReference>` with the correct
`AssemblyQualifiedName`. Get the exact AQN by **copying it verbatim from
an existing reference of the same type elsewhere in the file**. The
version numbers and PublicKeyToken values may vary by Dataverse version
— never hard-code a version that wasn't already present in the file.

**Adding any expression (subject line, condition operand, field assignment):**
Wrap the expression in `[brackets]` and properly XML-escape it
(per [reference/vb-expressions.md](../../reference/vb-expressions.md)):
- `&` → `&amp;`
- `"` → `&quot;`
- `<` → `&lt;`
- `>` → `&gt;`

**Adding a field assignment (Create / Update step body):**
A new field assignment is **two** activities, in this exact order:

1. An `EvaluateExpression` `ActivityReference` with
   `ExpressionOperator="CreateCrmType"` and a `Parameters` argument
   carrying the three-element `New Object() { WorkflowPropertyType.<T>,
   <value>, <typeHint> }` array. See
   [reference/vb-expressions.md — The `CreateCrmType` payload shape](../../reference/vb-expressions.md#the-createcrmtype-payload-shape--critical-for-write-operations).
2. An `mxswa:SetEntityProperty` that consumes the output variable and
   writes it to the field on the (in-flight) entity (`#Temp` form).

Skipping the `CreateCrmType` wrapper produces a workflow that fails at
activation with a type mismatch — the explicit `WorkflowPropertyType` tag
is required even for primitives.

**Adding a Check Condition with a `Null` or `NotNull` operator:**
Do **not** emit an `EvaluateExpression` for the right operand. Use
`<x:Null x:Key="Parameters" />` instead:

```xml
<mxswa:ActivityReference AssemblyQualifiedName="…EvaluateCondition…">
  <mxswa:ActivityReference.Properties>
    <InArgument x:TypeArguments="x:String" x:Key="ConditionOperator">
      <Literal>Null</Literal>
    </InArgument>
    <x:Null x:Key="Parameters" />
    <!-- LeftOperand still required -->
  </mxswa:ActivityReference.Properties>
</mxswa:ActivityReference>
```

**Adding multiple conditions joined with And/Or:**
Logical conditions chain **pairwise**, not as a single N-ary node. Three
conditions joined with `And` produce a tree like
`(c1 And c2) And c3`, not a flat 3-child node. Each `EvaluateLogicalCondition`
holds exactly two children. Generate them by left-folding from the
requirement list.

**Wait Conditions:**
The `Wait` argument on a ConditionSequence is a VB literal, not an XML
boolean attribute. Emit it as `Wait="[True]"` or `Wait="[False]"` (with
the brackets); a bare `Wait="True"` will be silently mis-parsed and the
workflow will behave as a Check Condition.

### Step 5 — Show the diff and confirm

Before writing, show the user:
- The exact text being added / removed (with surrounding context lines).
- Any side effects (e.g. "this will require deactivating the workflow
  in the org before re-importing").
- A one-sentence summary of the change.

Wait for explicit confirmation. "Looks good", "yes", "go ahead", "ship it"
all count. Anything ambiguous → ask again.

### Step 6 — Apply the edit

- Use a precise text-replacement edit, not a full-file rewrite.
- Preserve all surrounding `UserData`, `mva:VisualBasicValue`, indentation,
  and line endings.
- After writing, **read the file back** and verify:
  - The change is in the expected place.
  - The file still parses as well-formed XML.
  - No surrounding content was disturbed.

### Step 7 — Post-edit summary

Tell the user:
- What changed (one line).
- Where it changed (file + step name + position).
- What they need to do next:
  - "Re-pack the solution: `pac solution pack …`"
  - "Re-import to your org: `pac solution import …`"
  - "Re-activate the workflow after import (it imports as Draft)."
  - Or, if they're using the [publish-workflow](../publish-workflow/SKILL.md)
    skill: "Ready to publish — run the publish-workflow skill."

---

## Round-trip safety checklist

Before writing any edit, verify:

- [ ] Every `xmlns:*` declaration on the root element is preserved.
- [ ] No `UserData`, `mva:VisualBasicValue`, `mva:VisualBasic.Settings`,
      `mxswa:Workflow.Variables`, or `x:Key` blocks were stripped (unless
      the user explicitly asked to change one).
- [ ] Every `ActivityReference` element has its full
      `AssemblyQualifiedName`, copied verbatim from another reference of
      the same type already in the file (do not reconstruct it).
- [ ] Internal control-flow elements (ConditionSequence, ConditionBranch,
      Composite, TerminateWorkflow) are wrapped in `ActivityReference`,
      not direct elements.
- [ ] A new ConditionSequence has the full three-level
      `ConditionSequence → ConditionBranch → Composite` nesting (see
      [reference/xaml-anatomy.md §3a](../../reference/xaml-anatomy.md#3a-the-mandatory-conditionsequence-→-conditionbranch-→-composite-nesting)).
- [ ] Every new field assignment is `EvaluateExpression(CreateCrmType)`
      followed by `SetEntityProperty` — never `SetEntityProperty` alone.
- [ ] Conditions with operator `Null` or `NotNull` use
      `<x:Null x:Key="Parameters" />` instead of an `EvaluateExpression`
      for the right operand.
- [ ] Multiple logical conditions are nested pairwise as
      `(c1 op c2) op c3`, not flattened into a single N-ary node.
- [ ] A `Wait` argument on a ConditionSequence is `[True]` or `[False]`
      (in brackets), not a bare XML boolean.
- [ ] All VB expressions are wrapped in `[brackets]` and properly
      XML-escaped.
- [ ] The file's whitespace style (tabs vs spaces, line endings) matches
      what was there before.

If you can't satisfy all of these, **stop and explain to the user**
rather than emitting a probably-broken file.

---

## Don't

- Don't reformat the file. Reformatting hides real diffs in version
  control and risks breaking round-trip.
- Don't strip `UserData` or `mva:VisualBasicValue` blocks "to clean up".
  They are required for the legacy designer.
- Don't auto-fix unrelated issues you happen to notice. Surface them as
  findings; let the user request the fixes explicitly.
- Don't import the modified file to the org as part of this skill —
  that's the [publish-workflow](../publish-workflow/SKILL.md) skill's
  responsibility.
- Don't apply edits without showing a diff and getting confirmation.
  Even "trivial" changes deserve a review pass.
