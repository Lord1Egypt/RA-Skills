# Web Research — Classic Workflows + WF4 Substrate

A consolidated, citation-backed reference distilled from official Microsoft
Learn documentation. **Consult this before guessing** when a behavioral
question comes up that isn't already answered in the other reference docs.

> All citations are stable Microsoft Learn URLs. The `power-automate/`,
> `power-apps/`, and `power-platform/` subdomains all describe the same
> Dataverse Classic Workflow engine — the docs were re-published as the
> product was renamed (CRM → Dynamics 365 → Common Data Service →
> Dataverse). Behavior is identical across them; pick whichever URL is
> most current.

---

## 1. Engine substrate — what's WF4 and what's not

Dataverse Classic Workflows are persisted as Windows Workflow Foundation 4
(WF4) `Activity` definitions in XAML, but Dataverse only uses a *subset*
of WF4. Knowing where the line is keeps you from chasing irrelevant WF4
features.

### What Dataverse uses from WF4

| WF4 feature | How Dataverse uses it |
|---|---|
| XAML serialization (`System.Activities.XamlIntegration.ActivityXamlServices`) | The on-disk format. Load via `ActivityXamlServices.Load`; round-trip via `ActivityXamlServices.CreateBuilderReader` / `CreateBuilderWriter`. |
| `Activity` / `CodeActivity` / `NativeActivity` base classes | Custom workflow activities derive from `CodeActivity` (and only `CodeActivity`). |
| `InArgument<T>`, `OutArgument<T>`, `InOutArgument<T>` | The contract for parameters on every step. |
| `VisualBasicValue<TResult>` (r-value) and `VisualBasicReference<TResult>` (l-value) | Every dynamic value in a Classic Workflow is a `VisualBasicValue` whose `ExpressionText` is the bracketed VB expression you see in the XAML. |
| `ActivityBuilder` (design-time mutable form) and `DynamicActivity` (runtime form) | The WF4 model the Dataverse engine uses internally to load and validate the XAML. |
| `CacheMetadata` lazy validation | Why a malformed workflow may import successfully and only fail on first execution — the XAML isn't fully validated until invoked. |

### What Dataverse does NOT use from WF4

- **WCF messaging activities** (`Receive`, `Send`, `TransactedReceiveScope`,
  workflow services) — none of this exists in Classic Workflows.
- **State machines** (`StateMachine`, `State`, `Transition`) — Classic
  Workflows are sequential (`Sequence`) only.
- **Flowcharts** (`Flowchart`, `FlowDecision`, `FlowSwitch`) — not used.
- **Compensation activities** (`CompensableActivity`, `Compensate`,
  `Confirm`) — not used. Dataverse uses transaction rollback (real-time)
  or no rollback (background) instead.
- **C# expressions** (`CSharpValue<T>` / `CSharpReference<T>`) — Dataverse
  expressions are VB only. There is no `CompileExpressions=true` setting
  for Classic Workflow XAML.
- **Lambda expressions in code-built workflows** — irrelevant; Dataverse
  workflows are always XAML, never code-defined.
- **Bookmark resumption via custom `NativeActivity`** — Wait Conditions are
  the only resumption pattern, and they're modeled via `ConditionSequence`,
  not user-defined bookmarks.
- **Workflow tracking via `TrackingParticipant`** — Dataverse uses its own
  System Job + WorkflowLog tables instead.

> The deprecated `System.Workflow.*` namespaces (WF3, WF 3.5) are
> **completely** unrelated to Classic Workflows. If you see
> `WorkflowMarkupSerializer` or `ActivityMarkupSerializer` mentioned in
> documentation, that is WF3 and does not apply.

**Sources:**
- [Authoring Workflows, Activities, and Expressions Using Imperative Code](https://learn.microsoft.com/dotnet/framework/windows-workflow-foundation/authoring-workflows-activities-and-expressions-using-imperative-code)
- [Serialize Workflows and Activities to and from XAML](https://learn.microsoft.com/dotnet/framework/windows-workflow-foundation/serializing-workflows-and-activities-to-and-from-xaml)
- [`VisualBasicValue<TResult>`](https://learn.microsoft.com/dotnet/api/microsoft.visualbasic.activities.visualbasicvalue-1)
- [`VisualBasicReference<TResult>`](https://learn.microsoft.com/dotnet/api/microsoft.visualbasic.activities.visualbasicreference-1)
- [Variables and Arguments](https://learn.microsoft.com/dotnet/framework/windows-workflow-foundation/variables-and-arguments)

---

## 2. VB expressions — what the engine actually evaluates

Every `[bracketed]` expression in a Classic Workflow XAML lands in a
`VisualBasicValue<T>.ExpressionText`. The engine compiles it to a
**LINQ-to-Entities** expression at activation time.

Practical implications:

- **No reflection, no late binding** — every type and member must resolve
  at compile time against the assemblies the workflow runtime knows about
  (the SDK, `mscorlib`, `System`, and the entities defined in the org's
  metadata).
- **No `If` block / no statements** — VB expressions in a workflow are
  *single expressions* (r-values for `VisualBasicValue`, l-values for
  `VisualBasicReference`). Use `IIf(cond, a, b)` for conditionals.
- **`VisualBasicValue` cannot reference workflow variables or arguments by
  reflection** — it can only reference what's been declared as an
  `InArgument`, `OutArgument`, or `Variable` *in scope at that point in the
  activity tree*. The Dataverse engine wires the standard `InputEntities`,
  `CreatedEntities`, and `LocalParameters` containers into every
  `mxswa:ActivityReference` it emits.
- **Lambda expressions are not XAML-serializable** — irrelevant for
  hand-written workflows, but if you ever see code-generated workflows that
  use `ExpressionServices.Convert(lambda)`, the workflow designer will
  display the expression as blank.

**Sources:**
- [`VisualBasicValue<TResult>` — Remarks](https://learn.microsoft.com/dotnet/api/microsoft.visualbasic.activities.visualbasicvalue-1)
- [Authoring Workflows, Activities, and Expressions Using Imperative Code](https://learn.microsoft.com/dotnet/framework/windows-workflow-foundation/authoring-workflows-activities-and-expressions-using-imperative-code)

---

## 3. The `AsyncOperation` (System Job) state machine

Background workflows live and die through the `AsyncOperation` table.
Knowing the state codes makes triage and the `analyze-workflow` skill far
more precise.

| `StateCode` | Label | `StatusCode` values |
|---|---|---|
| 0 | Ready | 0 (Waiting For Resources) |
| 1 | Suspended | 10 (Waiting) |
| 2 | Locked | 20 (In Progress), 21 (Pausing), 22 (Canceling) |
| 3 | Completed | 30 (Succeeded), 31 (Failed), 32 (Canceled) |

### Lifecycle actions and the states they're valid in

| Action | Valid in `StateCode` | Result |
|---|---|---|
| Cancel | 0, 1, 2 | → 3 / 32 (or 3 / 31) |
| Pause | 2 | → 1 |
| Resume | 1 | → 0 |
| Postpone | 0, 2 | Sets `PostPoneUntil`; returns to 0 (Ready) at that time |
| Delete | any | Row removed; backing files deleted with it |

### What you can update on an `AsyncOperation`

Only **three** columns are end-user writable: `StateCode`, `StatusCode`,
`PostPoneUntil`. Even though the schema marks other columns as writable,
platform-level checks block updates to internal execution data.

### Backoff behavior

If an asynchronous workflow job fails repeatedly on the same record, the
engine **automatically lengthens the retry interval** to give administrators
time to investigate. Once it starts succeeding again, intervals return to
normal. This is engine-managed — no configuration knob.

### Storage shape (post-2021)

The serialized workflow context for an `AsyncOperation` is stored in the
**file store** (not the relational `AsyncOperationBase.Data` column),
which means:
- Workflow log volume eats **file capacity**, not database capacity.
- Files are deleted automatically when the parent `AsyncOperation` row is
  deleted — there is no separate file-cleanup step.

**Sources:**
- [Asynchronous service — Manage system job states](https://learn.microsoft.com/power-apps/developer/data-platform/asynchronous-service#manage-system-job-states)
- [Asynchronous service — Managing system jobs](https://learn.microsoft.com/power-apps/developer/data-platform/asynchronous-service#managing-system-jobs)
- [Delete completed system jobs and process log](https://learn.microsoft.com/power-platform/admin/cleanup-asyncoperationbase-table)

---

## 4. Infinite-loop protection (the "16 in a short window" rule)

The engine includes built-in cycle detection for background workflows:

> If a background workflow process is run more than a certain number of
> times on a specific row in a short period of time, the process fails
> with the following error: **"This workflow job was canceled because the
> workflow that started it included an infinite loop. Correct the workflow
> logic and try again."** The limit of times is **16**.

This is per-row, per-workflow. The classic trigger for it is a workflow
that fires on Update of a column and then itself updates that same column.

**Mitigations to recommend in `analyze-workflow`:**
1. Tighten `triggeronupdateattributelist` so only the columns the user
   would change trigger the workflow.
2. Add a Check Condition that compares the existing value to the proposed
   new value before issuing the `UpdateEntity`.
3. Use a guard column ("WorkflowProcessed") that the workflow sets and
   checks before re-running.

**Source:** [Best practices for background workflow processes — Avoid infinite loops](https://learn.microsoft.com/power-automate/best-practices-workflow-processes#avoid-infinite-loops)

---

## 5. Authoritative best-practice list (from MS Learn)

These are documented Microsoft recommendations — surface them in
`analyze-workflow` whenever they apply.

| # | Practice | Source |
|---|---|---|
| 1 | Avoid infinite loops (16-run kill switch will fire) | [best-practices-workflow-processes](https://learn.microsoft.com/power-automate/best-practices-workflow-processes#avoid-infinite-loops) |
| 2 | Don't run multiple background workflows that update the same table — causes resource lock contention and `SQL Timeout: Cannot obtain lock on resource …` errors | [best-practices-workflow-processes](https://learn.microsoft.com/power-automate/best-practices-workflow-processes#limit-the-number-of-workflows-that-update-the-same-table) |
| 3 | Use the **Notes** tab on the workflow record to record what you changed and why | [best-practices-workflow-processes](https://learn.microsoft.com/power-automate/best-practices-workflow-processes#use-notes-to-keep-track-of-changes) |
| 4 | Use **child workflows** for shared logic so it's maintained in one place | [best-practices-workflow-processes](https://learn.microsoft.com/power-automate/best-practices-workflow-processes#use-child-workflows) |
| 5 | Use **workflow templates** when you have several similar workflows | [best-practices-workflow-processes](https://learn.microsoft.com/power-automate/best-practices-workflow-processes#use-background-workflow-templates) |
| 6 | Enable **Automatically delete completed workflow jobs** for background workflows — successful jobs are pruned automatically; failures are always retained | [best-practices-workflow-processes](https://learn.microsoft.com/power-automate/best-practices-workflow-processes#automatically-delete-completed-background-workflow-jobs) |
| 7 | Real-time workflows have **no log for successful operations** — only errors are logged. Enable error logging via **Workflow Log Retention → Keep Logs for workflow jobs that encountered errors** | [monitor-manage-processes](https://learn.microsoft.com/power-automate/monitor-manage-processes) |
| 8 | Background workflows write **System Job** records; view them at **Settings → System Jobs** filtered to `System Job Type = Workflow` | [monitor-manage-processes](https://learn.microsoft.com/power-automate/monitor-manage-processes) |

---

## 6. Real-time workflow stage timing

When a real-time workflow runs against an SDK message, it slots into the
event pipeline at a fixed stage:

| Message | Stage |
|---|---|
| Create | PostOperation |
| Delete | PreOperation |
| Update | PreOperation **or** PostOperation (chosen via the **Before / After** option in the designer) |

**Implications:**
- A real-time workflow on Create cannot stop the create — it always runs
  after the row exists. Use a plug-in for true PreValidation/PreOperation
  Create logic.
- A real-time workflow on Delete is **PreOperation** by default — it can
  read the row's data and cancel the delete.
- For Update, only the PreOperation (Before) form can cancel the save and
  prevent downstream side effects in plug-ins or external systems.

Custom workflow activities running inside a real-time workflow can read
the stage at runtime via `IWorkflowContext.StageName`.

**Sources:**
- [Configure real-time workflow stages and steps — Initiating real-time workflows before or after status changes](https://learn.microsoft.com/power-apps/maker/data-platform/configure-workflow-steps#initiating-real-time-workflows-before-or-after-status-changes)
- [Workflow extensions — Real-time workflow stages](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions#real-time-workflow-stages)

---

## 7. Real-time vs Background — the constraints matrix

| Capability | Background | Real-Time |
|---|---|---|
| Wait Condition (`ConditionSequence Wait="[True]"`) | ✅ Supported | ❌ Not supported — workflow becomes invalid on conversion until the Wait is removed |
| Parallel Wait Branch | ✅ Supported | ❌ Not supported |
| Looping | ❌ Not supported | ❌ Not supported |
| Parallel branches at the same level | ❌ Not supported | ❌ Not supported |
| Run on a schedule | ❌ Not supported (use Power Automate) | ❌ Not supported |
| Trigger before save (cancel the save) | ❌ Not possible (always after) | ✅ Update/Delete only, with **Before** option |
| Access to pre-image of row | ✅ Yes | ✅ Yes |
| Run child workflows | ✅ Background → Background or Real-Time | ⚠️ Real-Time → Real-Time only |
| Run custom workflow activities | ✅ Yes (sandboxed in cloud) | ✅ Yes |
| Group steps in a transaction | ❌ Not supported (use changesets via Power Automate) | ✅ Implicit — the whole workflow shares the trigger's transaction |

**Conversion rules:**
- Background → Real-Time: must remove all Wait Conditions, Parallel Wait
  Branches, and `StartChildWorkflow` calls to background workflows; remove
  any `Persist` activities.
- Real-Time → Background: always safe.

**Source:** [Replace classic Microsoft Dataverse workflows with flows — feature comparison](https://learn.microsoft.com/power-automate/replace-workflows-with-flows)

---

## 8. Hierarchical operators (`Under` / `Not Under`)

The Check Condition operators `Under` and `Not Under` are valid **only on
tables that have a hierarchical relationship defined**. Activating a
workflow that uses these operators on a non-hierarchical table fails with:

> "You're using a hierarchical operator on a table that doesn't have a
> hierarchical relationship defined. Either make the table hierarchical
> (by marking a relationship as hierarchical) or use a different operator."

When `analyze-workflow` sees an `EvaluateCondition` with `ConditionOperator`
of `Under` or `NotUnder`, surface this dependency in the deployment notes —
it will fail at activation in target orgs that don't have the same
relationship configured as Hierarchical.

**Source:** [Configure background workflow stages and steps — Setting conditions](https://learn.microsoft.com/power-automate/configure-workflow-steps#setting-conditions-for-background-workflow-actions)

---

## 9. Custom workflow activities — the binding rules

A custom workflow activity (a "workflow assembly") is a class that
**derives from `System.Activities.CodeActivity`** and lives in an assembly
registered through the Plug-in Registration Tool (PRT) or via spkl
attribute-driven registration. Key non-obvious rules:

| Rule | Why |
|---|---|
| Target **.NET Framework 4.6.2** | The Dataverse runtime hosts WF4 on this version. Later targets work for features that existed in 4.6.2 but throw at runtime for anything newer. |
| Use the `Microsoft.CrmSdk.Workflow` NuGet package | It pulls in `Microsoft.CrmSdk.CoreAssemblies` transitively. |
| **Never store state in member or static variables** — the engine **caches CodeActivity instances** and reuses them across concurrent invocations on multiple threads | The constructor does **not** run on every invocation. Two parallel workflow runs share the same instance. |
| Read everything you need from the `CodeActivityContext` parameter passed to `Execute` | It's the only thread-safe handle on the current invocation. |
| Use `context.GetExtension<IWorkflowContext>()` — **not** `IPluginExecutionContext` | Plugins and workflow activities use different context interfaces; `IPluginExecutionContext` is null in workflow extensions. |
| Use `context.GetExtension<ITracingService>()` for diagnostics | Traces show up in the Process Session error log when the workflow fails. |
| When you register the assembly in PRT, you **don't register steps** like you would for a plug-in | Workflow activity discovery is by class derivation, not by step registration. The `Name`, `FriendlyName`, `WorkflowActivityGroupName`, and `Description` properties drive the designer UX. |
| Don't include logic that depends on `IExecutionContext.InputParameters` / `OutputParameters` | The configured input/output parameters of the activity are the supported contract; relying on hidden context data makes the activity opaque to designers. |
| Output behavior must be a pure function of the input parameters | Learn explicitly forbids context-dependent branching: *"the output value or behavior of the custom activity should always be determined solely by the input parameters."* |

### 9a. Allowed parameter types

The full list of types that may be used as `InArgument<T>`,
`OutArgument<T>`, or `InOutArgument<T>` on a custom workflow activity
(nothing else — no `Guid`, no `Uri`, no custom enums, no collections,
no nullable wrappers):

| .NET type | `[Default(...)]` string format |
|---|---|
| `bool` | `"True"` |
| `DateTime` | `"2004-07-09T02:54:00Z"` (ISO 8601 UTC) |
| `Decimal` | `"23.45"` |
| `Double` | `"23.45"` |
| `EntityReference` | `"<guid>", "<entitylogicalname>"` (two-arg `[Default]`) |
| `int` | `"23"` |
| `Money` | `"23.45"` |
| `OptionSetValue` | `"3"` (the integer option value as a string) |
| `string` | `"string default"` |

A single property can be both an input and an output:

```csharp
[Input("X")]
[Output("X")]
public InOutArgument<int> X { get; set; }
```

### 9b. Required parameter decorations

- `[Input("Display name")]` and/or `[Output("Display name")]` on every
  argument property.
- `[RequiredArgument]` on inputs the activity cannot run without.
- `[Default("…")]` to pre-populate the designer (see table above).
- `[ReferenceTarget("<entitylogicalname>")]` on every
  `EntityReference` parameter — without it, the designer picker is
  unbounded and users can't reliably choose the right table.
- `[AttributeTarget("<entitylogicalname>", "<columnlogicalname>")]` on
  every `OptionSetValue` parameter — without it, the designer falls back
  to a raw integer text box.

### 9c. Registration metadata (designer UX)

Whichever registration path you use (PRT GUI or spkl attribute), four
strings drive what the workflow designer shows:

| Property | What the user sees |
|---|---|
| `Name` | Internal name; canonical identifier of the activity. |
| `FriendlyName` | Label in the activity picker / Add Step menu. |
| `Description` | Hover/help text next to the activity. |
| `WorkflowActivityGroupName` | Category header that groups your activities in the picker (e.g. "Contoso - Strings"). |

For spkl attribute-driven registration, this becomes:

```csharp
[CrmPluginRegistration(
    "Display Name",            // Name
    "Friendly Name",           // FriendlyName
    "Description string",      // Description
    "Activity Group Name",     // WorkflowActivityGroupName
    IsolationModeEnum.Sandbox)] // always Sandbox in cloud
```

This is the **workflow-activity** 5-arg constructor; it is **not** the
plug-in step constructor. Workflow activities have no step registration.

### 9d. Cross-link

For end-to-end scaffolding of a new custom workflow activity (project
layout, class shape, parameter table, registration, call-site snippet,
common-mistake checklist), see the
[**write-custom-activity** skill](../skills/write-custom-activity/SKILL.md).

**Sources:**
- [Workflow extensions — Technology used](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions#technology-used)
- [Workflow extensions — Add parameters](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions#add-parameters)
- [Workflow extensions — Add your code to the Execute method](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions#add-your-code-to-the-execute-method)
- [Workflow extensions — Create a custom workflow activity assembly](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions#create-a-custom-workflow-activity-assembly)
- [Tutorial: Create workflow extension](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/tutorial-create-workflow-extension)
- [Debug Workflow Activities](https://learn.microsoft.com/power-apps/developer/data-platform/workflow/debug-workflow-activites)
- [Add custom workflow assembly to a solution](https://learn.microsoft.com/power-platform/alm/plugin-component#register-a-plug-in-or-custom-workflow-activity-in-a-custom-unmanaged-solution)

---

## 10. Cleanup and storage hygiene

If a tenant's `AsyncOperationBase` and `WorkflowLogBase` tables are
ballooning, the supported cleanup paths are:

1. **Per-workflow setting:** "Automatically delete completed workflow jobs"
   on the workflow record. Successful runs are pruned automatically;
   failures are retained for troubleshooting.
2. **Org-wide bulk delete job** for `System Jobs` filtered by `System Job
   Type = Workflow`, `Status = Completed`, `Status Reason = Succeeded`,
   and `Completed On older than X days`. Schedule this recurringly.
3. **Immediate bulk delete** for one-off cleanups — uses direct SQL rather
   than the per-row delete pipeline, much faster.

Files attached to `AsyncOperation` rows cannot be deleted independently —
they get deleted automatically when the parent row is deleted.

**Source:** [Delete completed system jobs and process log](https://learn.microsoft.com/power-platform/admin/cleanup-asyncoperationbase-table)

---

## 11. Why `Trigger=OnUpdate` + empty filtering attributes is a critical finding

Confirmed by the Dataverse trigger documentation: the **filter columns**
list is what tells the engine which Update operations should re-evaluate
the workflow. With no filter columns:

- The workflow re-evaluates on **every** update to a row, including
  internal/system updates (last modified by, last sync at, etc.).
- Combined with the infinite-loop guard (16 runs/short window), the
  workflow will get killed mid-execution rather than failing cleanly.
- Even if it doesn't loop, it consumes async-service capacity for no
  business value.

Always require a non-empty filtering attributes list when the trigger
includes Update.

**Source:** [Trigger flows when a row is added, modified, or deleted — Filter columns](https://learn.microsoft.com/power-automate/dataverse/create-update-delete-trigger#filter-columns)

> The Power Automate trigger doc isn't *exactly* the Classic Workflow doc,
> but the underlying Dataverse subscription is the same callback
> registration mechanism. The same column-filter semantics apply.

---

## 12. Modernization signals

Microsoft's official guidance is to **prefer Power Automate cloud flows
over new Classic Workflows** when feasible. The capabilities Classic
Workflows still uniquely provide are:

- **Wait conditions on columns** (cloud flows can't wait on a column
  changing).
- **Synchronous (real-time) execution** with the ability to cancel a save.
- **Custom CodeActivity workflow assemblies** (cloud flows have no
  equivalent — they run only out-of-the-box and connector actions).

Conversely, cloud flows uniquely provide: looping, parallel branches,
external connectors, scheduling, run analytics, AI-assisted authoring,
approvals, and a modern designer.

When `analyze-workflow` is asked for general improvement suggestions and
the workflow is a background workflow that doesn't use any of the three
Classic-Workflow-only capabilities above, recommend evaluating a
Power Automate replacement.

**Source:** [Replace classic Microsoft Dataverse workflows with flows](https://learn.microsoft.com/power-automate/replace-workflows-with-flows)

---

## Quick citation index

| Topic | URL |
|---|---|
| Classic Background workflows landing | <https://learn.microsoft.com/power-automate/workflow-processes> |
| Real-time workflows landing | <https://learn.microsoft.com/power-apps/maker/data-platform/overview-realtime-workflows> |
| Configure background steps | <https://learn.microsoft.com/power-automate/configure-workflow-steps> |
| Configure real-time steps | <https://learn.microsoft.com/power-apps/maker/data-platform/configure-workflow-steps> |
| Best practices | <https://learn.microsoft.com/power-automate/best-practices-workflow-processes> |
| Monitor / manage processes | <https://learn.microsoft.com/power-automate/monitor-manage-processes> |
| Replace with cloud flows (capability matrix) | <https://learn.microsoft.com/power-automate/replace-workflows-with-flows> |
| Workflow extensions (custom CodeActivity) | <https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions> |
| Tutorial: Create workflow extension | <https://learn.microsoft.com/power-apps/developer/data-platform/workflow/tutorial-create-workflow-extension> |
| Asynchronous service / `AsyncOperation` | <https://learn.microsoft.com/power-apps/developer/data-platform/asynchronous-service> |
| Cleanup `AsyncOperationBase` / `WorkflowLogBase` | <https://learn.microsoft.com/power-platform/admin/cleanup-asyncoperationbase-table> |
| WF4 — Variables and Arguments | <https://learn.microsoft.com/dotnet/framework/windows-workflow-foundation/variables-and-arguments> |
| WF4 — Serialize to/from XAML | <https://learn.microsoft.com/dotnet/framework/windows-workflow-foundation/serializing-workflows-and-activities-to-and-from-xaml> |
| WF4 — Authoring with imperative code | <https://learn.microsoft.com/dotnet/framework/windows-workflow-foundation/authoring-workflows-activities-and-expressions-using-imperative-code> |
| `VisualBasicValue<T>` reference | <https://learn.microsoft.com/dotnet/api/microsoft.visualbasic.activities.visualbasicvalue-1> |
| `VisualBasicReference<T>` reference | <https://learn.microsoft.com/dotnet/api/microsoft.visualbasic.activities.visualbasicreference-1> |
