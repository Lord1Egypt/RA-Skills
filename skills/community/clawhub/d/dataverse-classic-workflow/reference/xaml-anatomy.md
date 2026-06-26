# XAML Anatomy — Dataverse Classic Workflows

This document explains the structure of a Dataverse Classic Workflow XAML file
(WF4-based, stored in the `clientdata` field of the `workflow` record). It is
the reference the skills cite when they say "see xaml-anatomy.md".

> **Source of truth:** Microsoft Learn — Dataverse classic workflow processes:
> <https://learn.microsoft.com/power-automate/workflow-processes>
>
> **Engine substrate caveat:** Classic Workflows use only a *subset* of
> Windows Workflow Foundation 4. State machines, flowcharts, WCF messaging
> activities, compensation activities, and C# expressions are all part of
> WF4 but are **not** used by Dataverse — don't apply patterns from generic
> WF4 docs without verifying. See [`web-research.md`](./web-research.md#1-engine-substrate--whats-wf4-and-whats-not)
> for the full subset/superset map.

---

## 1. The root element

A classic workflow's root is `<mxswa:Activity>` containing exactly one child
`<mxswa:Workflow>`. Example skeleton (anonymized — uses the OOB `account`
entity):

```xml
<?xml version="1.0" encoding="utf-16"?>
<mxswa:Activity
    x:Class="ContosoExamplePublisher.Workflow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:mxs="http://schemas.microsoft.com/2014/xrm/activities"
    xmlns:mxswa="http://schemas.microsoft.com/2014/xrm/activities"
    xmlns:s="clr-namespace:System;assembly=mscorlib"
    xmlns:scg="clr-namespace:System.Collections.Generic;assembly=mscorlib"
    xmlns:mva="clr-namespace:Microsoft.VisualBasic.Activities;assembly=System.Activities"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

  <mxswa:Workflow Trigger="OnUpdate" Scope="Organization" RunAs="Owner"
                  PrimaryEntity="account" Mode="Background">
    <!-- Workflow body: a Sequence containing the user-visible steps -->
    <Sequence>
      <!-- ...step activities here... -->
    </Sequence>
  </mxswa:Workflow>

</mxswa:Activity>
```

Key root-level attributes on `<mxswa:Workflow>`:

| Attribute | Values | Meaning |
|-----------|--------|---------|
| `Trigger` | `Manual`, `OnCreate`, `OnUpdate`, `OnDelete`, `OnAssign`, `OnStateChange` (combinable as bitmask in metadata) | What starts the workflow |
| `Scope` | `User`, `BusinessUnit`, `ParentChildBusinessUnit`, `Organization` | Whose records trigger it |
| `RunAs` | `Owner`, `CallingUser` | Whose privileges execute steps |
| `PrimaryEntity` | logical name (e.g. `account`, `incident`, `sample_widget`) | The triggering entity |
| `Mode` | `Background`, `RealTime` | Async (rollback-safe) vs sync (form-blocking) |

---

## 2. Two classes of activity — the critical distinction

Inside the `<Sequence>`, you will see two **fundamentally different** kinds of
XAML elements. Knowing which is which is the #1 thing that trips up parsers.

### 2a. SDK activities — direct elements

The Dataverse SDK ships a fixed set of strongly-typed activities. These appear
as **direct XAML elements** with their `mxswa:` prefix:

| Element | What it does |
|---------|--------------|
| `<mxswa:UpdateEntity>` | Update a record |
| `<mxswa:CreateEntity>` | Create a record |
| `<mxswa:AssignEntity>` | Assign record owner |
| `<mxswa:SetState>` | Change statecode/statuscode |
| `<mxswa:SendEmail>` | Send an email |
| `<mxswa:StartChildWorkflow>` | Trigger another workflow |
| `<mxswa:RetrieveEntity>` | Look up a record by ID |
| `<mxswa:GetEntityProperty>` | Read a single field value |
| `<mxswa:SetEntityProperty>` | Write a single field on the in-memory entity |
| `<mxswa:Persist>` | Commit a checkpoint (background only) |

There are also **form-side** activities (real-time workflows attached to a
form) under the `mcwc:` prefix:

| Element | What it does |
|---------|--------------|
| `<mcwc:SetVisibility>` | Show/hide a form control |
| `<mcwc:SetDisplayMode>` | Lock/unlock a field |
| `<mcwc:SetFieldRequiredLevel>` | Change required level |
| `<mcwc:SetAttributeValue>` | Set field value on form (no save) |

### 2b. Internal control-flow activities — wrapped in ActivityReference

Conditional branching, expression evaluation, and step grouping are
implemented as internal CRM activities. These do **NOT** appear as direct
elements. They are always wrapped:

```xml
<mxswa:ActivityReference
    AssemblyQualifiedName="Microsoft.Crm.Workflow.Activities.ConditionSequence,
                           Microsoft.Crm.Workflow, Version=…, Culture=neutral,
                           PublicKeyToken=…"
    DisplayName="Check approval">
  <mxswa:ActivityReference.Properties>
    <!-- Properties for ConditionSequence (e.g. Conditions, Branches) -->
  </mxswa:ActivityReference.Properties>
</mxswa:ActivityReference>
```

The internal activities you'll see wrapped this way:

| AssemblyQualifiedName starts with… | Purpose |
|-----------------------------------|---------|
| `Microsoft.Crm.Workflow.Activities.ConditionSequence` | A whole `if/elseif/else` (or `wait`) block |
| `Microsoft.Crm.Workflow.Activities.ConditionBranch` | A single branch within a ConditionSequence |
| `Microsoft.Crm.Workflow.Activities.Composite` | A "step group" container (named subtree of activities) |
| `Microsoft.Crm.Workflow.Activities.EvaluateExpression` | Compute a value (often used for left-hand-side of a check) |
| `Microsoft.Crm.Workflow.Activities.EvaluateCondition` | Evaluate a single comparison |
| `Microsoft.Crm.Workflow.Activities.EvaluateLogicalCondition` | Combine sub-conditions with AND / OR |
| `Microsoft.Crm.Workflow.Activities.TerminateWorkflow` | Stop the workflow with success or cancel |

If you generate XAML and try to use these as direct elements (e.g.
`<ConditionSequence>`), Dataverse will reject the import.

---

## 3. The user-step → activity-tree mapping

A single step on the legacy classic workflow designer canvas typically expands
to **5–20** XAML activities. For example, a single "Update Record" step that
updates one field on the triggering record produces:

```
Composite (step group, wrapped in ActivityReference)
└── Sequence
    ├── GetEntityProperty (load current value if needed for an expression)
    ├── EvaluateExpression (compute the new value)
    ├── SetEntityProperty (set the in-memory field)
    └── UpdateEntity (commit to the platform)
```

A "Check Condition" step expands to:

```
ConditionSequence (wrapped in ActivityReference)
├── ConditionBranch  (the True / "if" branch)
│   ├── EvaluateLogicalCondition / EvaluateCondition tree
│   └── Sequence of child step activities
└── ConditionBranch  (the Else branch — optional)
    └── Sequence of child step activities
```

**Implication:** When you "add a step" you are adding one of these subtrees,
not a single element. The `write-workflow` skill handles the templating.

### 3a. The mandatory ConditionSequence → ConditionBranch → Composite nesting

Even a Check Condition with a **single** True branch and no Else uses the full
three-level wrapping. It is **not** optional and you cannot flatten it:

```xml
<mxswa:ActivityReference AssemblyQualifiedName="…ConditionSequence…">
  <mxswa:ActivityReference.Properties>
    <ActivityReference.Activities>
      <mxswa:ActivityReference AssemblyQualifiedName="…ConditionBranch…">
        <mxswa:ActivityReference.Properties>
          <Composite>
            <!-- the actual child steps go inside here -->
          </Composite>
        </mxswa:ActivityReference.Properties>
      </mxswa:ActivityReference>
    </ActivityReference.Activities>
  </mxswa:ActivityReference.Properties>
</mxswa:ActivityReference>
```

If you generate XAML that puts step activities directly under a
`ConditionBranch` (skipping the `Composite`), Dataverse will reject the
workflow on import.

### 3b. Whether a ConditionSequence is a Wait or a Check

The same `ConditionSequence` activity backs **both** Check Condition (run
branch on match) and Wait Condition (pause until match). The discriminator
is a `Wait` argument inside the ActivityReference's properties:

- `Wait="[True]"` (note the brackets — it is a VB literal, not an XML
  boolean) → Wait Condition. Background workflows only.
- `Wait="[False]"` or absent → Check Condition.

### 3c. Pattern signatures for collapsing activity trees back into user steps

Each user-visible step on the legacy designer canvas has a recognizable
activity-tree fingerprint. When summarizing or diffing, recognize these
shapes and roll the helpers up under the user-visible parent:

| User-visible step | Tell-tale activity combination inside the same Composite/Sequence |
|---|---|
| **Update Record** | Both `mxswa:UpdateEntity` and `mxswa:SetEntityProperty` present |
| **Create Record** | `mxswa:CreateEntity` with one or more preceding `mxswa:SetEntityProperty` |
| **Send Email** | A `CreateEntity` with `EntityName="email"` followed by an `mxswa:SendEmail`, OR a bare `mxswa:SendEmail` referencing a previously-created email |
| **Check Condition** | `mxswa:ActivityReference` whose AQN starts with `…ConditionSequence` and whose `Wait` argument is False/absent |
| **Wait Condition** | Same as above but `Wait="[True]"` |
| **Stop Workflow** | `mxswa:ActivityReference` whose AQN starts with `…TerminateWorkflow` (or `…StopWorkflow` in some Dataverse builds) |
| **Custom step** | Any direct element whose XML namespace is a `clr-namespace:` not in the table in §5 — treat as a Custom CodeActivity |

---

## 4. UserData and design-time metadata

Every Composite, ConditionSequence, ConditionBranch, and most SDK activities
carry a `UserData` blob. This is base64 / JSON state used by the legacy classic
designer to remember things like "this branch's collapse state" or "the
parameter binding labels".

```xml
<mxswa:ActivityReference.UserData>
  <s:String x:Key="…">…serialized state…</s:String>
</mxswa:ActivityReference.UserData>
```

**Rule:** Never strip these. Modifying them is fine when intentional, but
discarding them is a destructive change — the workflow will still run, but
the legacy designer view in Dataverse will be broken or look wrong.

Similarly, `mva:VisualBasicValue` blocks contain pre-compiled expression
metadata (used for IntelliSense). Preserve them verbatim unless you're
intentionally rewriting an expression.

### 4a. The `mva:VisualBasic.Settings` block

Most workflows have a top-level block that looks like:

```xml
<mva:VisualBasic.Settings>
  <x:Null />            <!-- or a complex settings block -->
</mva:VisualBasic.Settings>
```

This is the WF4 expression-compiler settings block. It must be preserved
verbatim. If you strip it, every VB `[bracket expression]` in the workflow
will fail to compile on activation.

### 4b. Workflow.Variables

Variables declared on the workflow appear in `<mxswa:Workflow.Variables>`
and carry `Name`, `x:TypeArguments`, and optional `Default` attributes.
They are referenced by name in VB expressions elsewhere in the file.
Preserve them — removing a variable that an expression still references
breaks activation.

---

## 5. Namespaces you will commonly see

| Prefix | URI / Assembly | Used for |
|--------|----------------|----------|
| `mxswa` | `http://schemas.microsoft.com/2014/xrm/activities` | All SDK + ActivityReference elements |
| `mxs` | `http://schemas.microsoft.com/2014/xrm/activities` | Variants, sometimes used for properties |
| `mcwc` | (clr-namespace, Microsoft.Crm.Workflow.Client.dll) | Form-side real-time activities |
| `mva` | `clr-namespace:Microsoft.VisualBasic.Activities;assembly=System.Activities` | VB expression compile-time metadata |
| `s` | `clr-namespace:System;assembly=mscorlib` | `s:String`, `s:Int32`, etc. |
| `scg` | `clr-namespace:System.Collections.Generic;assembly=mscorlib` | Generic collections |
| `x` | `http://schemas.microsoft.com/winfx/2006/xaml` | XAML directives (`x:Key`, `x:Class`, `x:TypeArguments`) |

> **Parser caution:** `clr-namespace:` URIs may include spaces and commas
> (`clr-namespace:System;assembly=mscorlib` is fine, but
> `clr-namespace:Microsoft.VisualBasic.Activities;assembly=System.Activities,
> Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a`
> requires URL-encoding the spaces before some XML parsers will accept it).
> Most production XAML you'll see has the simpler form.
>
> **Practical workaround when feeding WF4 XAML to a generic XML parser:**
> URL-encode spaces (` ` → `%20`) and commas (`,` → `%2C`) inside `xmlns:*`
> attribute values **only**, parse, then map the encoded form back to the
> original when writing the file out. Modifying the URI in the file you
> persist will break the round-trip — the original string must come back.

---

## 6. Where the XAML lives

When you `pac solution clone` or `pac solution unpack` a Dataverse solution
containing classic workflows, the XAML is extracted to:

```
<solution-folder>/
└── src/
    └── Workflows/
        ├── <DisplayName>-<workflowId>.xaml
        └── <DisplayName>-<workflowId>.xaml.data.xml   ← metadata sibling
```

The `.xaml.data.xml` sibling holds the workflow record's column values
(name, primary entity, trigger flags, scope, mode, run-as, statecode,
statuscode). When publishing back, both files round-trip together.

---

## 7. Diagnosing "this isn't a classic workflow" XAML

Sometimes a file in `Workflows/` is actually a different category. Quick
identifier:

| Root looks like | Category | Tooling |
|-----------------|----------|---------|
| `<mxswa:Activity>` containing `<mxswa:Workflow>` | Classic Workflow (this agent's scope) | This agent |
| `<Microsoft.Crm.Workflow.BusinessProcessFlow…>` | Business Process Flow | Out of scope |
| `<Microsoft.Crm.Workflow.BusinessRule…>` | Business Rule | Out of scope |

If the `<mxswa:Workflow>` element's `Mode` is `RealTime` and you see `mcwc:*`
activities, it's a **real-time workflow attached to a form**. Some operations
(like `Persist` checkpoints) are not allowed in real-time mode — flag them
when reviewing.
