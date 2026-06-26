# write-custom-activity

**Scaffold a C# custom workflow activity (CodeActivity assembly) that can be
called from a Dataverse Classic Workflow.** This is the skill behind requests
like "create a workflow activity that …", "I need a custom step that does X",
or "add a new helper to my workflow activity library".

> ⚠️ This skill produces C# source files for a class library that targets
> **.NET Framework 4.6.2** and is registered against a Dataverse environment.
> It does NOT modify any existing XAML — that is the
> [`write-workflow`](../write-workflow/SKILL.md) skill's job. The flow is:
> **author the activity → register the assembly → reference it from XAML.**

---

## When to use

- "Create a workflow activity that pads a string to N characters."
- "I need a custom step that returns the initiating user as an `EntityReference`."
- "Write a workflow activity that runs an aggregate FetchXML and returns the
  result as decimals."
- "Generate a workflow activity that calls the `AISummarize` action and returns
  the summary."
- "Add a new activity to my existing `*.Activities` project that …"

## When NOT to use

- The user wants to **call** an existing custom activity from a workflow — that
  is just an `mxswa:ActivityReference` edit; use
  [`write-workflow`](../write-workflow/SKILL.md).
- The logic can be expressed with built-in `mxswa:*` activities (Create / Update
  / Retrieve / Send Email / Check Condition) — recommend the declarative path
  first. Custom CodeActivities are an escape hatch, not a default.
- The user wants something that **must run asynchronously / fire-and-forget /
  delay** — a workflow activity blocks the calling workflow step. Recommend a
  child workflow with a Wait Condition, a scheduled workflow, or Power Automate.
- The target is **on-premises Dynamics 365** with non-sandbox isolation — the
  patterns are similar but the assembly registration / location choices differ.
  Confirm with the user before assuming.

## Inputs

- **Required:** A description of what the activity should do.
- **Required:** The list of inputs (name + type) the user wants exposed in the
  designer.
- **Required:** The list of outputs (name + type) the user wants returned.
- **Strongly recommended:** A target project folder. If the user has an
  existing class library that already contains `CodeActivity` classes, prefer
  adding to it over creating a new project.
- **Optional but useful:** Whether to inherit from an existing base class
  (e.g. a project-specific `BaseWorkflowActivity` that wraps the tracing +
  organization-service plumbing). See **Step 3 — Decide on a base class**.

## Outputs

1. The **C# source file** for the new activity class.
2. (If no project exists) a minimal **`.csproj`** and `packages.config` /
   `<PackageReference>` snippet.
3. A **registration note** describing how to register the assembly (spkl
   attribute-driven, or PRT GUI).
4. A **call-site snippet** showing the `mxswa:ActivityReference` element the
   classic workflow XAML will use after registration. Hand off to
   [`write-workflow`](../write-workflow/SKILL.md) for actually inserting it.

---

## Authoritative reference

The constraints below are not opinions — they are documented in MS Learn:

- **Class derivation, parameter types, attributes, statelessness, registration:**
  <https://learn.microsoft.com/power-apps/developer/data-platform/workflow/workflow-extensions>
- **End-to-end tutorial (IncrementByTen):**
  <https://learn.microsoft.com/power-apps/developer/data-platform/workflow/tutorial-create-workflow-extension>
- **Debug Workflow Activities (Profiler + PRT):**
  <https://learn.microsoft.com/power-apps/developer/data-platform/workflow/debug-workflow-activites>
- **Add to a solution (Plug-in assembly component):**
  <https://learn.microsoft.com/power-platform/alm/plugin-component>
- **Engine-substrate caveat (which `System.Activities.*` types are usable):**
  [`reference/web-research.md` §1](../../reference/web-research.md#1-engine-substrate--whats-wf4-and-whats-not)
- **WF4-vs-Classic-Workflow custom-activity binding rules:**
  [`reference/web-research.md` §9](../../reference/web-research.md#9-custom-workflow-activities--the-binding-rules)

---

## Procedure

### Step 1 — Verify the target project

If the user has an existing workflow activity library:

1. Read its `.csproj`. Confirm:
   - `<TargetFrameworkVersion>v4.6.2</TargetFrameworkVersion>` (or
     `<TargetFramework>net462</TargetFramework>` SDK-style).
   - References to `System.Activities`, `Microsoft.Xrm.Sdk`,
     `Microsoft.Xrm.Sdk.Workflow`. The standard NuGet package is
     [`Microsoft.CrmSdk.Workflow`](https://www.nuget.org/packages/Microsoft.CrmSdk.Workflow/),
     which transitively pulls in `Microsoft.CrmSdk.CoreAssemblies`.
   - `<SignAssembly>true</SignAssembly>` and a key file (`.snk`). Required
     for environments enforcing strong-name verification.
2. Scan one or two existing activities in the project. Match their pattern:
   - Sealed vs. non-sealed.
   - Custom base class (e.g. `BaseWorkflowActivity`) vs. direct `CodeActivity`.
   - Namespace convention (e.g. `<RootNamespace>.<Category>`).
   - Whether `[CrmPluginRegistration(...)]` is used (spkl) or registration is
     left to PRT.

If no project exists yet, scaffold one — see **Appendix A: minimal project**.

### Step 2 — Decide on a base class

| Option | When to use |
|---|---|
| `: CodeActivity` directly | Quick, one-off, no shared boilerplate. |
| Custom `: BaseWorkflowActivity : CodeActivity` | The project already has one. Reuse it — it usually centralizes tracing, `IOrganizationService` lazy creation, and impersonation. |

A typical project-specific base class wraps:
- `IWorkflowContext workflowContext = context.GetExtension<IWorkflowContext>();`
- `ITracingService tracing = context.GetExtension<ITracingService>();`
- `IOrganizationServiceFactory factory = context.GetExtension<IOrganizationServiceFactory>();`
- A lazy `OrganizationService` for the calling user, and a `SystemOrganizationService` (factory.CreateOrganizationService(null)) for system context.
- Convenience helpers for `GetPreImageEntity` / `GetPostImageEntity`.
- Try/catch + trace + rethrow.

**Never** put workflow data into instance fields of the activity itself —
the engine caches activity instances and runs concurrent invocations on
multiple threads. State held on `this` will leak across runs. (Learn:
*"Write the code in the Execute method to be stateless."*)

### Step 3 — Pick parameter types

Only the following property types are valid for `InArgument<T>`,
`OutArgument<T>`, and `InOutArgument<T>`:

| Type | Default-value format |
|---|---|
| `bool` | `[Default("True")]` |
| `DateTime` | `[Default("2004-07-09T02:54:00Z")]` |
| `Decimal` | `[Default("23.45")]` |
| `Double` | `[Default("23.45")]` |
| `EntityReference` | `[Default("3B036E3E-94F9-DE11-B508-00155DBA2902", "account")]` |
| `int` | `[Default("23")]` |
| `Money` | `[Default("23.45")]` |
| `OptionSetValue` | `[Default("3")]` |
| `string` | `[Default("string default")]` |

**Not allowed:** `Guid`, `Uri`, custom enums, custom classes, nullable types,
collections, dictionaries. If the user asks for a `Guid` input, expose it as
`string` and parse with `Guid.TryParse` inside `Execute`. If they ask for a
list, take a delimited `string` or a FetchXML `string`.

### Step 4 — Decorate the parameters correctly

Required decorators per parameter:

```csharp
[RequiredArgument]                    // optional — only when truly required
[Input("Display name in designer")]   // required for inputs
public InArgument<string> MyInput { get; set; }

[Output("Display name in designer")]  // required for outputs
[Default("false")]                    // optional — only when sensible default exists
public OutArgument<bool> MyOutput { get; set; }
```

Extra decorators by parameter type:

- **`InArgument<EntityReference>`** — add
  `[ReferenceTarget("<entitylogicalname>")]` to pin which table the designer
  can target. Omit it only if the activity is genuinely entity-agnostic.
- **`InArgument<OptionSetValue>`** — add
  `[AttributeTarget("<entitylogicalname>", "<columnlogicalname>")]` to bind
  the parameter to a specific OptionSet column and pre-populate valid values
  in the designer.
- **Both in and out on the same property** — use `InOutArgument<T>` and stack
  `[Input(...)]` and `[Output(...)]` together.

Common output pattern for fallible activities (mirrors the project's idiom):
- Add `[Output("Failed")] [Default("false")] public OutArgument<bool> Failed`
- Add `[Output("Failure Message")] public OutArgument<string> FailureMessage`
- Set them in the `catch` block. Allows the calling workflow to branch on
  failure with a Check Condition instead of always faulting the workflow.

### Step 5 — Write `Execute` (or `ExecuteWorkflowActivity`)

Hard rules:
- The method body must be **stateless**. Read inputs at the top; do work in
  locals; write outputs at the bottom.
- Use `Get(context)` to read and `Set(context, value)` to write. The
  `context` parameter is the `CodeActivityContext` (or, if a project base
  class wraps it, whatever the wrapper exposes — for example a property
  like `ExecutionContext`).
- Treat the activity's behavior as a **pure function of inputs**. Don't read
  process-related metadata to decide what to do — Learn explicitly warns
  *"the output value or behavior of the custom activity should always be
  determined solely by the input parameters."*
- Trace at entry, exit, and around any external call. `ITracingService.Trace`
  output appears in the System Job's error log when something goes wrong.
- Use `service.Execute(new OrganizationRequest("..."))` for actions; use
  `service.Retrieve` / `RetrieveMultiple` / `Update` / `Create` for plain
  CRUD.
- For impersonation, prefer the platform's run-as: read
  `workflowContext.InitiatingUserId` and pass it to
  `factory.CreateOrganizationService(userId)`. Pass `null` to get the
  SYSTEM user.
- For errors that should fault the job, throw
  `InvalidWorkflowException("…")`. For errors that should be observable but
  recoverable, set the `Failed` / `FailureMessage` outputs and return.

### Step 6 — Decorate the class for registration

Two paths, depending on what the project uses:

**Path A — spkl attribute-driven (preferred when the project's `spkl.json`
points at the compiled DLL):**

```csharp
[CrmPluginRegistration(
    "<Display Name>",            // appears in the designer
    "<Friendly Name>",           // also appears in some lists
    "<Description>",             // hover/help text
    "<Activity Group Name>",     // category header in the designer (e.g. "Contoso - Strings")
    IsolationModeEnum.Sandbox)]
public sealed class MyActivity : CodeActivity
{
    // ...
}
```

> Workflow activities use the **workflow** constructor of
> `CrmPluginRegistration`. Do **not** use the plugin step constructor.
> Workflow activities do NOT register steps — the calling XAML is the
> invocation site.

**Path B — Plug-in Registration tool (PRT):**

Skip the attribute. The user will:
1. Build the assembly (`Release` configuration).
2. Run `pac tool prt`, connect to the environment.
3. **Register New Assembly** → select the DLL → **Register Selected Plugins**
   (no steps to register — that's normal for workflow activities).
4. Expand the registered assembly, select the activity class, set:
   - **Name** — the designer's class name.
   - **Friendly Name** — what the user sees in the picker.
   - **Workflow Activity Group Name** — the category header in the picker.
   - **Description** — hover text.
5. Add the assembly to an unmanaged solution
   (`Add existing` → `Other` → `Plug-in assembly`) so it travels with deploys.

### Step 7 — Produce the call-site snippet

After the activity ships, a Classic Workflow XAML calls it via
`mxswa:ActivityReference`. Provide the snippet so
[`write-workflow`](../write-workflow/SKILL.md) can insert it cleanly. Include:

- The `AssemblyQualifiedName` (`Namespace.Class, AssemblyName, Version=…, Culture=neutral, PublicKeyToken=…`).
- An `Arguments` block matching the activity's `[Input]`/`[Output]` names.

The user (or the next skill) will need the real `Version` and
`PublicKeyToken` — pull them with:

```powershell
[System.Reflection.AssemblyName]::GetAssemblyName("path\to\Foo.dll").FullName
```

See `reference/activity-types.md` §8 for the AQN-format details.

### Step 8 — Acceptance checklist before handing back

- [ ] Class derives from `CodeActivity` (directly or via a project base).
- [ ] Class is `public`. Single-file activities should also be `sealed` unless
      the user wants them subclassable.
- [ ] No instance fields hold runtime data. Reads/writes only inside `Execute`.
- [ ] Every public `InArgument<T>` / `OutArgument<T>` / `InOutArgument<T>` has
      an `[Input(...)]` and/or `[Output(...)]` attribute.
- [ ] `EntityReference` parameters have `[ReferenceTarget(...)]`.
- [ ] `OptionSetValue` parameters have `[AttributeTarget(...)]` (unless the
      activity is generic across choice columns and the user wants to enter
      the value as an integer at design time).
- [ ] `[RequiredArgument]` is set only on inputs the activity genuinely
      cannot run without.
- [ ] `[Default("...")]` values are formatted as **strings** (see Step 3
      table) — even for non-string types.
- [ ] If the project uses spkl, the class has a `[CrmPluginRegistration(...)]`
      attribute with the workflow constructor (5 args ending in
      `IsolationModeEnum.Sandbox`).
- [ ] `ITracingService.Trace` is called at entry, exit, and around any
      external call.
- [ ] Errors are either thrown as `InvalidWorkflowException` (fatal) or
      surfaced via `Failed` / `FailureMessage` outputs (recoverable).
- [ ] The output behavior is a pure function of the inputs.

---

## Output template

````
# New Custom Workflow Activity — {Class Name}

## Summary

{One paragraph: what it does, what it returns, fatal vs recoverable failure mode.}

## Project context

- **Target project:** {path}
- **Target framework:** {`v4.6.2`}
- **Base class:** {`CodeActivity` | `BaseWorkflowActivity`}
- **Namespace:** {`<RootNamespace>.<Category>`}
- **Activity Group Name (designer category):** {string}

## Parameters

| Direction | Name | Type | Required | Designer label | Notes |
|---|---|---|---|---|---|
| In  | {prop} | {type} | yes/no | "{label}" | {ReferenceTarget / AttributeTarget / Default / etc} |
| Out | {prop} | {type} | n/a    | "{label}" | … |

## File: `Activities/{Category}/{ClassName}.cs`

```csharp
{generated source — see Appendix B for the template}
```

## Registration

{One of: "spkl will pick this up on the next `spkl pack/import`" | "Register in PRT with: Name='…', Friendly Name='…', Activity Group Name='…'."}

## Call site (for write-workflow)

Insert this `mxswa:ActivityReference` where you want the step to appear:

```xml
<mxswa:ActivityReference AssemblyQualifiedName="{Namespace.Class}, {AssemblyName}, Version=X.X.X.X, Culture=neutral, PublicKeyToken=xxxxxxxxxxxxxxxx" DisplayName="{user-visible step name}">
  <mxswa:ActivityReference.Arguments>
    <InArgument x:TypeArguments="{type}" x:Key="{ParamName}">[{vb-expression}]</InArgument>
    <OutArgument x:TypeArguments="{type}" x:Key="{OutName}">[{l-value}]</OutArgument>
  </mxswa:ActivityReference.Arguments>
</mxswa:ActivityReference>
```

> Pull the assembly's real `Version` and `PublicKeyToken` from the compiled
> DLL before pasting into XAML.

## Open questions

- {Any input the user under-specified}
````

---

## Appendix A — Minimal project scaffold

If the user has no class library yet, scaffold:

**`{ProjectName}.csproj`** (SDK-style, .NET Framework 4.6.2):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net462</TargetFramework>
    <RootNamespace>{RootNamespace}</RootNamespace>
    <AssemblyName>{AssemblyName}</AssemblyName>
    <SignAssembly>true</SignAssembly>
    <AssemblyOriginatorKeyFile>{AssemblyName}.snk</AssemblyOriginatorKeyFile>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.CrmSdk.Workflow" Version="9.0.2.45" />
  </ItemGroup>
  <ItemGroup>
    <Reference Include="System.Activities" />
  </ItemGroup>
</Project>
```

Generate `{AssemblyName}.snk` with:

```powershell
sn -k {AssemblyName}.snk
```

`<SignAssembly>` + the `.snk` are required for environments that enforce
strong-name verification.

---

## Appendix B — Activity source-file template

This is the shape every generated activity should follow. Replace
placeholders in `{curly braces}`.

```csharp
using System;
using System.Activities;
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Workflow;

namespace {RootNamespace}.{Category}
{
    [CrmPluginRegistration(
        "{Display Name}",
        "{Friendly Name}",
        "{One-line description}",
        "{Activity Group Name}",
        IsolationModeEnum.Sandbox)]
    public sealed class {ClassName} : CodeActivity
    {
        [RequiredArgument]
        [Input("{Input Label}")]
        public InArgument<string> {InputProperty} { get; set; }

        [Output("{Output Label}")]
        public OutArgument<string> {OutputProperty} { get; set; }

        [Output("Failed")]
        [Default("false")]
        public OutArgument<bool> Failed { get; set; }

        [Output("Failure Message")]
        public OutArgument<string> FailureMessage { get; set; }

        protected override void Execute(CodeActivityContext context)
        {
            var tracing = context.GetExtension<ITracingService>();
            var workflowContext = context.GetExtension<IWorkflowContext>();
            var factory = context.GetExtension<IOrganizationServiceFactory>();
            var service = factory.CreateOrganizationService(workflowContext.InitiatingUserId);

            tracing.Trace("Entered {ClassName}.Execute()");

            try
            {
                var input = {InputProperty}.Get(context);

                // ---- core logic goes here ----
                var result = input; // placeholder

                {OutputProperty}.Set(context, result);
                Failed.Set(context, false);
            }
            catch (Exception ex)
            {
                tracing.Trace("Exception in {ClassName}: " + ex);
                Failed.Set(context, true);
                FailureMessage.Set(context, ex.Message);
                // Decide: rethrow as InvalidWorkflowException to fault the job,
                // or swallow and let the calling workflow branch on Failed.
            }
            finally
            {
                tracing.Trace("Exiting {ClassName}.Execute()");
            }
        }
    }
}
```

For projects that have a custom `BaseWorkflowActivity`, swap the class
declaration and `Execute` body for the project's pattern (typically
`protected override void ExecuteWorkflowActivity(LocalWorkflowContext ctx)`
with `ctx.OrganizationService`, `ctx.TracingService`,
`ctx.WorkflowContext`, and `ctx.ExecutionContext`).

---

## Worked example — "Substring" activity

Input: a string and a start position (and optional length). Output: the
substring. Demonstrates `[RequiredArgument]`, optional `int` input,
defensive bounds-checking, and `Failed`/`FailureMessage` recovery.

See [`examples/custom-activity-substring.cs`](../../examples/custom-activity-substring.cs)
for the full source.

---

## Common mistakes to flag

| Mistake | What goes wrong |
|---|---|
| Putting workflow data in `private` instance fields | Engine caches the instance → data leaks across runs and across threads. |
| Targeting a framework newer than .NET 4.6.2 | Assembly registers fine, then throws at execution time on any post-4.6.2 API. |
| Forgetting `[ReferenceTarget]` on `EntityReference` inputs | Designer shows the picker for *all* tables, so users can't pick the right one (or pick a wrong one and get late-bound errors). |
| Forgetting `[AttributeTarget]` on `OptionSetValue` inputs | Designer shows a raw integer text box. Users either type the wrong value or stop trusting the activity. |
| Throwing a generic `Exception` | Caller can't reason about the failure. Prefer `InvalidWorkflowException` (fatal) or the `Failed`/`FailureMessage` pattern (recoverable). |
| Using `Trace.Write` / `Console.WriteLine` | Output never reaches the sandbox log. Use `context.GetExtension<ITracingService>().Trace(...)`. |
| Calling `factory.CreateOrganizationService(null)` for ordinary reads | Runs as SYSTEM, bypasses security. Use the initiating user unless impersonation is the explicit goal. |
| Long-running external calls | Workflow activities run **inline** within the workflow step. Network latency translates directly to user-perceived slowness for real-time workflows and to AsyncOperation latency for background ones. Set conservative timeouts. |
| Hidden config (reading app settings, env vars) | Sandbox isolation forbids `System.Configuration.ConfigurationManager`. Pass config in as input parameters or store it in a Dataverse table. |

See [`reference/web-research.md` §9](../../reference/web-research.md#9-custom-workflow-activities--the-binding-rules)
for the cited Learn passages behind each of these.
