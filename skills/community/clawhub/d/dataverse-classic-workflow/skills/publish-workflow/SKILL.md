# publish-workflow

**Activate, deactivate, import, or export Classic Workflows in a Dataverse
environment, using the Power Platform CLI (`pac`).**

> ⚠️ This skill runs commands that change a real environment. Always show
> the user the exact command and the target environment before executing.
> Get explicit confirmation. **Never auto-deploy.**

---

## When to use

- "Push my updated workflow back to the dev environment"
- "Activate this workflow in production"
- "Deactivate this workflow so I can edit it"
- "Export the workflow as part of a solution"
- "Import the solution containing my workflow"

## Prerequisites

The user needs:
1. **Power Platform CLI** (`pac`) installed and on PATH.
   - <https://learn.microsoft.com/power-platform/developer/cli/introduction>
2. **A `pac` auth profile** for the target environment:
   ```pwsh
   pac auth create --name <profile-name> --environment <orgUrl>
   pac auth select --name <profile-name>
   ```
3. The workflow already exists in a **Dataverse solution** (Classic Workflows
   are deployed via solutions, not individually).

If any prerequisite is missing, walk the user through it before proceeding.

---

## Outputs

- **Confirmed plan** — the exact `pac` commands you'll run, the target
  environment, and any expected side effects.
- **Command output** — the actual stdout/stderr from `pac`, surfaced
  verbatim. Don't paraphrase.
- **Post-action summary** — what state the org is in now and what to
  verify (e.g. "Workflow is now activated. Test by triggering it on a
  test record.").

---

## Procedure

### Step 1 — Confirm the target environment

Before any command, **state out loud** which environment you're targeting:

```
Target environment: contoso-dev
Auth profile:       contoso-dev
URL:                https://contoso-dev.crm.dynamics.com
```

Get explicit user confirmation. If the user only specified an environment
name, run `pac auth list` and ask them to confirm which profile is right.

If the target looks like production (name contains `prod`, `live`, or you
see a warning sign in their auth list), **double-confirm**: "This is
production. Are you sure?"

### Step 2 — Decide the operation

Pick the right operation by intent:

| User intent | Operation |
|-------------|-----------|
| "Push my edits to the org" | A. Pack solution → import → activate |
| "Activate this workflow" | B. Activate workflow record |
| "Deactivate so I can edit" | C. Deactivate workflow record |
| "Get the latest from the org" | D. Clone / unpack solution |
| "Send the solution to a colleague" | E. Pack as a managed solution |

---

### A. Pack and import a solution containing workflow edits

This is the most common operation. The workflow XAML lives inside a solution
folder; you re-pack and re-import to push edits.

```pwsh
# 1. Pack the unpacked solution into a .zip (omit --packagetype Managed for unmanaged dev push)
pac solution pack `
  --zipfile "<solution-folder>/bin/<SolutionName>.zip" `
  --folder  "<solution-folder>/src" `
  --packagetype Unmanaged

# 2. Import to the target environment (synchronous so we can chain publish)
pac solution import `
  --path "<solution-folder>/bin/<SolutionName>.zip"

# 3. Publish customizations
pac solution publish-customizations
```

After import, the workflow imports as **Draft** if it was Draft in the
source. You still need to activate it (operation B).

### B. Activate a workflow

Classic Workflows are activated by setting `statecode=1, statuscode=2` on
the workflow record. The cleanest way via PAC is the Web API:

Get the workflow's GUID (you can find it in the `.xaml.data.xml` sibling,
or query):

```pwsh
# List active classic workflows on a primary entity
pac admin list --filter "entitylogicalname eq 'account' and category eq 0"
```

Then activate via OData PATCH (no direct `pac` command exists; this is the
canonical pattern):

```pwsh
$workflowId = '00000000-0000-0000-0000-000000000000'
$body = '{ "statecode": 1, "statuscode": 2 }'
pac org `
  invoke-api `
  --method PATCH `
  --url "/api/data/v9.2/workflows($workflowId)" `
  --body $body
```

Confirm with the user *first*, then run.

> If the user's `pac` version doesn't support `org invoke-api`, fall back
> to instructing them to use a tiny PowerShell script that calls the Web
> API directly. Don't generate one inline unless asked.

### C. Deactivate a workflow

Same as B with reversed values:

```pwsh
$workflowId = '00000000-0000-0000-0000-000000000000'
$body = '{ "statecode": 0, "statuscode": 1 }'
pac org `
  invoke-api `
  --method PATCH `
  --url "/api/data/v9.2/workflows($workflowId)" `
  --body $body
```

Activated workflows are read-only. Deactivate before any edit you intend to
push back.

### D. Clone or unpack a solution to get the latest XAML

```pwsh
# Either: clone (preferred — pulls a fresh copy of the named solution from the org)
pac solution clone `
  --name <SolutionUniqueName> `
  --outputDirectory "<solution-folder>" `
  --processCanvasApps false

# Or: export then unpack (older flow)
pac solution export `
  --name <SolutionUniqueName> `
  --path "<solution-folder>/bin/<SolutionName>.zip" `
  --managed false

pac solution unpack `
  --zipfile "<solution-folder>/bin/<SolutionName>.zip" `
  --folder  "<solution-folder>/src"
```

After clone/unpack, workflow XAML lands at
`<solution-folder>/src/Workflows/<DisplayName>-<workflowId>.xaml` plus a
matching `.xaml.data.xml`.

### E. Pack as a managed solution for distribution

```pwsh
pac solution pack `
  --zipfile "<solution-folder>/bin/<SolutionName>_managed.zip" `
  --folder  "<solution-folder>/src" `
  --packagetype Managed
```

Managed solutions can be installed to other environments without exposing
the contents to direct edit. Use Managed for production handoff.

---

## Step 3 — Show, confirm, run, surface

For every command:

1. **Show** the exact command you intend to run (with concrete values
   substituted, not placeholders).
2. **Confirm** with the user — they say "go", "yes", "run it", or
   equivalent.
3. **Run** in the terminal.
4. **Surface** stdout/stderr verbatim. Don't summarize or paraphrase the
   `pac` output — users need to see import warnings and any errors.

If a command fails:
- Show the error verbatim.
- Suggest the most likely cause (auth expired, environment name mistyped,
  solution not found, etc.).
- Do **not** retry automatically. Wait for the user to decide.

---

## Step 4 — Post-action verification

After every successful operation, tell the user what to verify:

- **After import:** Open the solution in the org's Solution Explorer, find
  the workflow, confirm its state (Draft after import — needs activation).
- **After activate:** Trigger the workflow on a test record. Check
  `Process Sessions` (settings > system jobs) for the run.
- **After deactivate:** Confirm the workflow is now editable in the legacy
  designer.

---

## Common gotchas

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Import error: "Cannot start the requested operation [PublishAll] because there is another [Import] running" | A previous async import is still in progress | Wait for it to finish, or use synchronous import (drop `--async`) |
| Import error: "Workflow not found" | Targeting wrong environment, or solution doesn't include the workflow | Verify `pac auth select` and that the workflow is included in the solution |
| Activate fails: "Workflow has not been validated" | Workflow XAML has compile errors | Open it in the legacy designer to see specific errors, or run the [analyze-workflow](../analyze-workflow/SKILL.md) skill |
| Activate fails: "Workflow is already activated" | Workflow imported in active state | Deactivate, then re-activate |
| Imported workflow doesn't appear active in source-control | Activation state is per-environment, not in the XAML | This is expected behavior |

---

## Don't

- Don't run `pac` commands without showing the user first and getting
  confirmation.
- Don't target production without an explicit double-confirmation.
- Don't paraphrase `pac` output. Surface it verbatim.
- Don't activate a workflow that you (or the user) just edited without
  first re-importing the solution. The activated workflow uses the
  XAML in the org, not the file on disk.
- Don't try to "delete and recreate" a workflow as a way to push edits
  — you'll lose the workflow GUID and any references (workflow
  references in plugins, custom buttons, child-workflow callers) will
  break.
