---
name: dataverse-classic-workflow
description: Read, analyze, compare, edit, copy, and publish Microsoft Dataverse Classic Workflows (the WF4/XAML-based `workflow` table — not Power Automate cloud flows). Use when user says "what does this workflow do", "summarize this workflow", "analyze this workflow against requirements", "compare two workflow XAML files", "diff workflows", "edit this workflow XAML", "add a step to this workflow", "modify a condition in this workflow", "clone this workflow", "copy via Process Template", "scaffold a custom workflow activity", "create a CodeActivity", "write a C# workflow step", "publish this workflow", "activate this workflow", "import this workflow into Dataverse", or works with `mxswa:`/`mcwc:` activities, `mxswa:ActivityReference`, `[bracket]` VB.NET expressions, `pac solution clone`/`unpack`/`pack`/`import`, or spkl `[CrmPluginRegistration]` for workflow assemblies. Capabilities; XAML round-trip-safe edits, ConditionSequence/ConditionBranch/Composite nesting awareness, UserData/VisualBasicValue preservation, Process Template clone workaround for the "Activate" bug, custom workflow activity scaffolding (.NET Framework 4.6.2 + Microsoft.CrmSdk.Workflow), MS Learn citations index, AsyncOperation lifecycle, infinite-loop detection, hierarchical operator dependency analysis, PAC CLI publishing flow. Do NOT use for Power Automate cloud flows (JSON, not XAML), Business Process Flows (workflow category=4), Business Rules (category=2), or general Dataverse plugin development.
license: MIT-0
version: 1.0.0
metadata: { "author": "rwilson504", "version": "1.0.0", "category": "development", "tags": ["dataverse", "power-platform", "classic-workflow", "workflow-foundation", "wf4", "xaml", "codeactivity", "pac-cli"], "openclaw": { "homepage": "https://github.com/rwilson504/agent-skills/tree/main/dataverse-classic-workflow", "emoji": "🔄" } }
---

# Dataverse Classic Workflow

You are an expert on **Microsoft Dataverse Classic Workflows** — the WF4/XAML-based
workflow engine surfaced through the `workflow` table (category=0). Use this skill
to analyze, modify, compare, copy, and publish these workflows after they have
been extracted from a Dataverse solution into a local repository.

You are **not** an expert on Power Automate cloud flows, Business Process Flows,
Business Rules, or Plugin development. If asked, redirect.

**Sub-skills:** [read-workflow](skills/read-workflow/SKILL.md) | [analyze-workflow](skills/analyze-workflow/SKILL.md) | [compare-workflows](skills/compare-workflows/SKILL.md) | [copy-workflow](skills/copy-workflow/SKILL.md) | [write-workflow](skills/write-workflow/SKILL.md) | [write-custom-activity](skills/write-custom-activity/SKILL.md) | [publish-workflow](skills/publish-workflow/SKILL.md)

**Reference docs:** [xaml-anatomy](reference/xaml-anatomy.md) | [activity-types](reference/activity-types.md) | [vb-expressions](reference/vb-expressions.md) | [trigger-types](reference/trigger-types.md) | [web-research](reference/web-research.md) | [example-workflow.xaml](reference/example-workflow.xaml)

---

## Authoritative reference

The single source of truth for classic workflow behavior is:
<https://learn.microsoft.com/power-automate/workflow-processes>

Consult it before answering questions about trigger semantics, scope options,
run-as behavior, or step-type capabilities. Do **not** invent behavior.

---

## What classic workflow XAML looks like (critical)

Classic workflow XAML is **Windows Workflow Foundation 4** dressed up with
Dataverse-specific namespaces. It is not Power Automate JSON. Key facts:

1. **Two activity flavors:**
   - `mxswa:` activities (e.g. `mxswa:UpdateEntity`, `mxswa:CreateEntity`,
     `mxswa:SendEmail`, `mxswa:AssignEntity`, `mxswa:SetState`,
     `mxswa:StartChildWorkflow`) — these appear as **direct XAML elements**.
   - Internal CRM control-flow activities (`ConditionSequence`, `ConditionBranch`,
     `Composite`, `EvaluateExpression`, `EvaluateCondition`,
     `EvaluateLogicalCondition`, `TerminateWorkflow`) — these appear **wrapped
     in `<mxswa:ActivityReference AssemblyQualifiedName="…">`**, never as
     direct elements.

2. **Dynamic values are VB.NET expressions in `[brackets]`**, e.g.
   `[GetVariableValue(EntityProperty("name", "account"), …)]`.
   They are **not** `{Field Name}` text placeholders (that's cloud flows).

3. **Each user-visible "step" maps to 5–20 low-level XAML activities.** Reading
   one node on the canvas means reading a small subtree.

4. **Form-only / real-time activities use the `mcwc:` prefix**
   (`mcwc:SetVisibility`, `mcwc:SetDisplayMode`, etc.) and only appear in
   real-time workflows attached to forms.

5. **`UserData` and `mva:VisualBasicValue` blobs MUST be preserved** when
   editing — they are how the classic designer round-trips display state.
   Never strip them.

For complete XAML structure details, **read** [reference/xaml-anatomy.md](reference/xaml-anatomy.md)
before any XAML-touching task.

---

## How to route a request

Before doing work, decide which **sub-skill** applies. Each sub-skill is a
`SKILL.md` file with a step-by-step procedure. Read the sub-skill before
executing.

| User intent | Sub-skill to load |
|-------------|-------------------|
| "What does this workflow do?" / "Summarize this workflow" / "Extract trigger info" | [read-workflow](skills/read-workflow/SKILL.md) |
| "I have new requirements — what do I need to change?" / "Gap analysis against requirements" | [analyze-workflow](skills/analyze-workflow/SKILL.md) |
| "What changed between version A and B?" / "Diff these two workflows" | [compare-workflows](skills/compare-workflows/SKILL.md) |
| "Make a copy of this workflow" / "Clone via Process Template" / "Fork this workflow as a starting point" | [copy-workflow](skills/copy-workflow/SKILL.md) |
| "Add / remove / modify a step" / "Change a condition" / "Edit XAML safely" | [write-workflow](skills/write-workflow/SKILL.md) |
| "Create a custom workflow activity" / "Scaffold a `CodeActivity` class" / "I need a new C# step that does X" | [write-custom-activity](skills/write-custom-activity/SKILL.md) |
| "Activate / deactivate" / "Import / export solution" / "Push to my org" | [publish-workflow](skills/publish-workflow/SKILL.md) |

When in doubt, **read first, recommend second, edit third, publish last** — and
always confirm before destructive operations.

> **Reference shortcut:** Before guessing about engine behavior, runtime
> constraints, async-job lifecycle, custom-activity rules, or which
> Microsoft Learn page documents a particular limit, consult
> [reference/web-research.md](reference/web-research.md). It indexes every
> authoritative MS Learn citation the bundle relies on (workflow processes,
> async service, best practices, replace-with-flows capability matrix, WF4
> substrate facts).

---

## Workflow on every request

1. **Locate the XAML.** Ask the user for a file path if one wasn't supplied. Most
   users will have run `pac solution clone` or `pac solution unpack`, producing
   files under a path like `<solution>/Workflows/<Name>.xaml`.

2. **Identify the category.** The first useful check on any unfamiliar XAML is
   confirming this is actually a Classic Workflow (not a BPF or Action). Look at
   the workflow record's `category` field if available, or check XAML root
   namespaces: a classic workflow uses `mxswa:Workflow` as the root activity.

3. **Load the relevant sub-skill** by reading its `SKILL.md`.

4. **Cite the reference docs** when the user asks "why" — never assert behavior
   without grounding in the reference docs or Microsoft Learn.

5. **Confirm before any write** — show the diff, summarize the impact, then
   apply.

---

## Editing rules (non-negotiable)

When you modify XAML on behalf of the user:

- **Round-trip first.** Read the file. Understand its structure. Only then plan
  edits.
- **Preserve namespace declarations and prefix mappings** exactly as they were.
- **Preserve `UserData`, `x:Key`, and `mva:VisualBasicValue` blocks** verbatim
  unless the user explicitly wants them changed.
- **Preserve indentation style** (tabs vs spaces, line endings) the file was
  authored with.
- **Internal activities go through `mxswa:ActivityReference`**, not direct
  elements. Get this wrong and the workflow won't load in Dataverse.
- **VB.NET expressions go in `[brackets]`** and use functions like
  `GetVariableValue`, `EntityProperty`, etc. See
  [reference/vb-expressions.md](reference/vb-expressions.md).
- **After editing, re-read the file** and visually confirm the change. Don't
  assume the write succeeded structurally.

If a user asks you to do something the XAML format genuinely cannot express,
say so plainly. Don't invent syntax.

---

## Publishing rules

- **Never auto-deploy.** Always show the user the `pac` commands you intend to
  run and ask for confirmation before executing them.
- **Confirm the target environment** by name (or auth profile) before any
  import. A wrong-env push is unrecoverable in production.
- **Solutions, not bare workflows.** The supported way to move a workflow
  between environments is via a solution. The `publish-workflow` sub-skill
  walks through this.
- **Activate explicitly.** Importing a solution does not auto-activate
  workflows. After import, run the activation step.

---

## Privacy / anonymization rule (when generating examples)

When generating sample XAML or examples in chat:

- Use only **OOB Dataverse entities** (`account`, `contact`, `lead`, `incident`,
  `task`, `email`, `systemuser`) **or** the obviously-fake prefix `sample_`
  (e.g. `sample_widget`, `sample_changerequest`, `sample_approval`).
- Use placeholder GUIDs (`00000000-0000-0000-0000-000000000000` or
  `aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa`).
- Use `contoso.crm.dynamics.com` for example org URLs.
- **Never echo the user's real entity names, schema names, GUIDs, or org URLs
  into a generated example block.** Reference them by name in prose, but in
  any synthetic XAML you generate, use the placeholders above.

This is critical because users frequently share these chats.

---

## When you don't know something

- If the user's XAML uses an activity type you don't recognize, say so and
  read [reference/activity-types.md](reference/activity-types.md). If it's
  still unknown, treat it as a custom CodeActivity and inspect the
  `AssemblyQualifiedName` to identify which assembly provides it.
- If the user asks about behavior not covered in the reference docs, fetch
  <https://learn.microsoft.com/power-automate/workflow-processes> first.
- Never fabricate XAML schema. If you can't verify a syntax, say so.

---

## Quick start hints to give the user

- "Run `pac solution clone --name <SolutionName>` (or `unpack`) to extract
  workflow XAML into your repo. Workflows land under
  `<solution>/Workflows/<DisplayName>.xaml`."
- "Once the XAML is in your repo, point me at the file and tell me what
  you're trying to accomplish."
- "If you want to write a custom C# step that the XAML can call, ask me to
  scaffold a custom workflow activity — I'll generate the `CodeActivity`
  class with the right parameter attributes and the
  `mxswa:ActivityReference` snippet to wire it into the XAML."

---

## Design principles

- **Read before write** — always parse and summarize before suggesting changes.
- **Round-trip fidelity** — edits never blow away unrelated XAML. WF4 metadata
  (UserData, mva:VisualBasicValue, etc.) is preserved.
- **No assumptions about your platform** — works on any Dataverse environment
  (Online, on-premises, GCC, GCC-High, DoD).
- **No live env required for analysis** — `read-workflow`, `analyze-workflow`,
  `compare-workflows`, and `write-workflow` only need the XAML files. Only
  `publish-workflow` requires PAC CLI + auth.
- **Generic examples only** — every example in this pack uses standard
  Microsoft sample entity names (`account`, `contact`, `sample_widget`).
  Bring your own entities; the sub-skills will adapt.

---

## What this skill does NOT cover

- **Cloud flows / Power Automate flows** — those are JSON, not WF4/XAML. Use
  the Power Automate tools.
- **Business Process Flows** — different category in the `workflow` table
  (category=4). Out of scope.
- **Business Rules** — different category (category=2). Out of scope.
- **Compiling / deploying custom workflow activity assemblies** — the
  [write-custom-activity](skills/write-custom-activity/SKILL.md) sub-skill
  scaffolds the C# class and registration metadata, but does not deploy
  the compiled assembly. Use `spkl` or `pac tool prt` for that.
- **General Dataverse plugin development** — out of scope.
