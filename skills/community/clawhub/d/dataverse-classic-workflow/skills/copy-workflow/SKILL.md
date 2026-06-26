# copy-workflow

**Copy an existing Classic Workflow by promoting it to a Process Template,
then creating a new workflow from that template — and restore the metadata
that the template mechanism does NOT carry over.**

> ⚠️ This is the supported way to clone a workflow in the legacy designer,
> but it has well-known gaps and a UI bug. Read this entire skill before
> walking the user through it.

---

## When to use

- "I want to make a copy of this workflow so I can change it without
  affecting the original."
- "Clone this workflow as a starting point for a new variant."
- "I'm building a new version of an existing process — start me with a copy."
- "Make a workflow template I can spin new workflows off of."

If the user instead wants to **edit** the existing workflow in place, route
to [write-workflow](../write-workflow/SKILL.md). If they want to **diff**
the copy against the original later, route to
[compare-workflows](../compare-workflows/SKILL.md).

---

## Critical context — what the template mechanism does and does not copy

When you convert a workflow to a Process Template and then "New ▸ from
Template", **only the steps, actions, and conditions copy across**. Several
trigger and execution settings are silently reset.

### What DOES copy

- All workflow steps and their ordering
- Conditions and their branches
- Step display names and configured field values
- Custom workflow activity references
- VB.NET expressions inside steps

### What does NOT copy (you must manually re-set these on the new workflow)

| Setting | New workflow default | Action required |
|---------|----------------------|-----------------|
| **Trigger checkboxes** (Record is created / Record status changes / Record is assigned / Record fields change / Record is deleted) | All unchecked | Re-check whatever the original had |
| **Filtering attributes** (the specific fields that trigger "Record fields change") | Empty | Re-add the same field list |
| **Scope** | `User` | Set to whatever the original used (commonly `Organization`) |
| **"As an on-demand process"** (run manually) | Unchecked | Re-check if original allowed manual run |
| **"As a child process"** (callable from another workflow) | Unchecked | Re-check if original allowed child-workflow calls |
| **Run As** (Owner of the workflow vs Calling user) | Often resets — verify | Set to match original |
| **Activate As** (Process vs Process Template) | Process | Leave as Process for normal workflows |

**You MUST verbally walk the user through every one of these settings**
after they create the copy. The single most common mistake is publishing
the new workflow with an empty trigger and wondering why it never fires.

---

## Critical bug — converting a workflow to a Process Template

There is a long-standing bug in the **classic workflow editor** (the legacy
process form, accessed from the solution explorer or via the "Switch to
Classic" link from the maker portal):

**If you switch a process from "Process" to "Process Template" in the
classic editor and then click the "Activate" button in that same editor,
the change is silently discarded — the workflow stays as a regular
Process, not a Template.**

### The workaround (always use this sequence)

1. Open the workflow in the **classic editor** (legacy form).
2. In the **"Activate As"** dropdown (top of the form), change the value
   from `Process` to `Process Template`.
3. Click **Save and Close** (NOT Activate). The change is now committed to
   the workflow record.
4. In the **Power Platform maker portal** (`make.powerapps.com`), navigate
   to **Solutions ▸ <YourSolution> ▸ Processes**, find the workflow, and
   toggle it to **On** (this activates it).
5. The workflow will now activate AND retain its `Process Template` status.

If the user reports "I switched it to a template but it's still a regular
workflow", the cause is almost always that they hit Activate inside the
classic editor instead of Save and Close + activate from the maker portal.

---

## Outputs

- **Pre-flight summary** — the original workflow's trigger / scope /
  on-demand / child-process / run-as settings, captured so you can
  reproduce them on the copy.
- **Step-by-step walkthrough** — each click the user needs to make.
- **Post-copy checklist** — every setting they need to verify on the new
  workflow before activating.

---

## Procedure

### Step 1 — Capture the original's settings (BEFORE doing anything else)

Before promoting anything to a template, **read the original workflow's
metadata** so you can faithfully re-create it on the copy. If you have the
XAML locally, you can pull most of these from the `<mxswa:Workflow>` root
attributes:

- `Trigger="…"` → which triggers were checked (a bitmask — see
  [trigger-types.md](../../reference/trigger-types.md))
- `Scope="…"` → User / BusinessUnit / ParentChildBusinessUnit / Organization
- `Mode="…"` → Background or RealTime
- `RunAs="…"` → Owner or CallingUser
- `PrimaryEntity="…"` → the table the workflow runs against

The "on-demand" and "child process" flags are stored on the workflow
**record** (not in the XAML), so the user has to read those off the
classic editor:

- **On Demand:** check "As an on-demand process"
- **Child:** check "As a child process"

If filtering attributes are configured (Trigger includes "Record fields
change"), they live on the workflow record's `triggeronupdateattributelist`
field. In the classic editor they appear as the field list next to the
"Record fields change" checkbox.

**Present the captured settings to the user as a checklist** they can refer
to after the copy. Example:

```
Original: "Account Onboarding Approval"
  Triggers:           Record is created, Record fields change (creditlimit, statuscode)
  Scope:              Organization
  Run As:             Owner of the workflow
  Mode:               Background
  On-demand allowed:  Yes
  Child process:      No
  Primary entity:     account
```

### Step 2 — Convert the original (or a freshly imported clone) to a Process Template

> If the user wants to keep the original active and unchanged, have them
> **first export → import the solution under a new unique name**, then
> promote *that* copy to a template. Otherwise this step turns the
> original into a template and it will no longer fire on its own.

In the **classic editor**:

1. Open the workflow.
2. If it's currently activated, click **Deactivate** at the top.
3. Change **Activate As** from `Process` → `Process Template`.
4. Click **Save and Close**. (Do **not** click Activate here — that's the
   bug described above.)
5. In **make.powerapps.com**, find the workflow under your solution and
   toggle it **On** to activate it as a template.

The workflow record now has `category=2` (Workflow Template) and is
available as a starting point under "New process ▸ from an existing
template (select from list)".

### Step 3 — Create the new workflow from the template

In **make.powerapps.com** (or via the legacy "New Process" dialog):

1. **Solutions ▸ <YourSolution> ▸ + New ▸ Automation ▸ Process ▸ Workflow**
   (or in the legacy designer: **New Process**).
2. Give the new workflow a **distinct name** — never reuse the original
   name in the same solution.
3. Choose the same **primary table** as the template.
4. Under **Type**, choose **"New process from an existing template (select
   from list)"** and pick the template you just created in Step 2.
5. Click **OK / Create**.

Dataverse opens the new workflow in the classic editor with all the
**steps copied** from the template, but **none of the trigger / scope /
on-demand / child / run-as settings**.

### Step 4 — Restore the trigger, scope, and execution settings

This is the step everyone forgets. Using the checklist from Step 1, set
each of the following on the new workflow in the classic editor:

- [ ] **Activate As:** `Process` (not Template — this is the new working
      copy)
- [ ] **Scope:** match the original (User / BU / Parent:Child BU / Organization)
- [ ] **Run As:** Owner of the workflow vs Calling user
- [ ] **Mode:** Background vs Real-time
- [ ] **Start When checkboxes:** check each trigger from the original
      (Record is created, Record status changes, Record is assigned,
      Record fields change, Record is deleted)
- [ ] **Filtering attributes:** if "Record fields change" is checked,
      click "Select" next to it and re-add the same field list
- [ ] **As an on-demand process:** check if original had it
- [ ] **As a child process:** check if original had it

Click **Save and Close**.

### Step 5 — Activate and verify

1. In **make.powerapps.com**, toggle the new workflow **On** to activate it.
2. Verify on a test record that it fires under the expected conditions.
3. If it doesn't fire: 9 times out of 10 the trigger or scope is still
   wrong. Re-open in the classic editor and recheck against the Step 1
   checklist.

### Step 6 (optional) — Pull the new workflow XAML into source control

If the user wants to track the copy in their repo:

```pwsh
pac solution clone --name <SolutionUniqueName> --outputDirectory "<solution-folder>"
```

The new workflow will land at
`<solution-folder>/src/Workflows/<NewDisplayName>-<workflowId>.xaml`.
At this point you can hand off to [read-workflow](../read-workflow/SKILL.md)
or [write-workflow](../write-workflow/SKILL.md) for further work.

---

## Common gotchas

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| New workflow never fires | Trigger checkboxes still unchecked (didn't carry over) | Re-check them per the Step 1 checklist |
| New workflow fires but only sees current user's records | Scope still defaulted to `User` | Set Scope to match original (often `Organization`) |
| "Run workflow" button missing on the form / view | "As an on-demand process" still unchecked | Re-check it in the classic editor |
| Another workflow can't call this one as a child | "As a child process" still unchecked | Re-check it |
| Workflow stayed as `Process` after I switched to Template | Hit **Activate** inside the classic editor (the bug) | Switch to Template → **Save and Close** → activate from maker portal |
| Filtering attributes empty after copy | They live on the workflow record, not the XAML | Manually re-select the same fields next to "Record fields change" |
| Trigger is right but workflow runs as wrong user | `RunAs` reset | Set Run As back to `Owner of the workflow` (or whatever original used) |
| Two workflows with the same name in the solution | Reused the original name | Rename one — duplicate display names cause user confusion and complicate troubleshooting |

---

## Don't

- **Don't promote the original workflow to a template if you still need it
  to run.** Templates do not fire on their own. Either deactivate-and-keep
  for reference, or import a separate copy of the solution first and
  promote *that* to a template.
- **Don't click Activate from inside the classic editor when switching to
  Process Template.** Always use Save and Close + activate from the maker
  portal (the bug described above).
- **Don't trust that "all the important stuff copied".** It didn't. The
  trigger, scope, on-demand flag, and child-process flag are all reset.
  Walk the checklist every time.
- **Don't auto-fill the new workflow's settings without first asking the
  user to confirm the original's settings.** Some teams intentionally
  change Scope or Run As when forking a workflow — don't assume.
- **Don't generate a new workflow GUID and try to inject it into the XAML
  file directly as a "copy".** The supported path is the template
  mechanism above; manual GUID-and-name munging will produce a workflow
  the platform can't manage cleanly (broken solution layering, missing
  workflow-record metadata).
