# Trigger, Scope, Mode, and Run-As Reference

The behavior options that determine **when** a classic workflow runs, **whose
records** it sees, **whether it blocks the user**, and **whose privileges it
runs with**.

> Authoritative source:
> <https://learn.microsoft.com/power-automate/workflow-processes>
>
> Related: [`web-research.md` §6](./web-research.md#6-real-time-workflow-stage-timing)
> documents the exact event-pipeline stages each real-time message lands in
> (Create → PostOperation, Delete → PreOperation, Update → Pre or Post via
> the Before/After option). [`web-research.md` §7](./web-research.md#7-real-time-vs-background--the-constraints-matrix)
> summarizes the full Real-Time vs Background capability matrix and conversion
> rules. [`web-research.md` §8](./web-research.md#8-hierarchical-operators-under--not-under)
> covers the activation-time failure mode of `Under` / `Not Under` operators.

---

## Trigger

Triggers determine what event starts the workflow. In the workflow record's
`triggertypemask` column they are a **bitmask** — a workflow can have multiple
triggers (e.g. "On Create OR On Update of statuscode").

| Trigger | Bitmask value | When it fires |
|---------|---------------|---------------|
| Record Created | 1 | When a new record is created |
| Record Status Changed | 2 | When statecode changes |
| Record Assigned | 4 | When ownerid changes |
| Record Field Changes | 8 | When one of the named filtering attributes changes (Update) |
| Record Deleted | 16 | When a record is deleted |
| On Demand | 32 | Manual trigger (from a ribbon button or `ExecuteWorkflow`) |
| Child Workflow | 64 | Started by another workflow's `StartChildWorkflow` |

In the XAML root attribute `Trigger=` you'll see a comma-separated list of
trigger names rather than the bitmask, e.g. `Trigger="OnCreate,OnUpdate"`.

### Filtering attributes (for "Record Field Changes")

When the trigger includes "Record Field Changes" (`OnUpdate`), the workflow
record carries a `triggeronupdateattributelist` column listing the attribute
logical names that should fire the workflow. Without this list, the workflow
fires on every update — almost always a misconfiguration.

When summarizing a workflow, **always surface the filtering attributes** if
the trigger includes Update. A workflow that says "Trigger: OnUpdate" with
no filter list is a performance red flag.

---

## Scope

Scope determines whose records can trigger the workflow.

| Scope | Value | Meaning |
|-------|-------|---------|
| User | 1 | Only records owned by the workflow's owner |
| Business Unit | 2 | Records owned by users in the workflow owner's BU |
| Parent: Child Business Units | 3 | Owner's BU plus child BUs |
| Organization | 4 | All records in the org (typical for system processes) |

**Default and most common: Organization.**

User-scoped workflows are unusual and almost always a bug — they create
behavior that depends on who owns the workflow record, which is fragile.
Flag them when you see them.

---

## Mode

Mode determines how the workflow executes relative to the triggering operation.

| Mode | XAML value | Behavior |
|------|------------|----------|
| Background | `Background` | Async, queued via system jobs. The triggering save returns immediately. Failures don't roll back the trigger. |
| Real-Time | `RealTime` | Sync, runs as part of the same database transaction as the trigger. **Failures roll back the trigger.** Constrained step set (no `Persist`, no `Wait`). |

**Pick Real-Time only when:**
- You need the user-visible result of the workflow before they see the form
  refresh, OR
- You need transactional safety (the workflow's failure should cancel the save).

**Background is the default and the right choice for ~90% of workflows.**

When converting Background → Real-Time:
- Remove all `Persist` activities.
- Remove all Wait Conditions (`ConditionSequence Wait="True"`).
- Remove all `StartChildWorkflow` calls to background workflows (real-time
  can only call other real-time workflows).
- Audit any external calls (custom activities) — they now block the user.

---

## Run As

Determines whose privileges the workflow uses when reading and writing
records.

| Run As | Value | Behavior |
|--------|-------|----------|
| Workflow Owner | `Owner` (1) | Steps execute with the privileges of the user who owns the workflow record |
| Calling User | `CallingUser` (2) | Steps execute with the privileges of the user who triggered the workflow |

**Default: Calling User for triggered workflows; Owner for on-demand.**

Pick `Owner` when you want the workflow to be able to read/write records
that some users couldn't normally access (a controlled-elevation pattern).
This requires the owner to have the necessary privileges — usually a service
account.

**Security implication:** A workflow set to `RunAs=Owner` and triggered by
unprivileged users effectively grants those users elevated access through
the workflow's effects. Audit carefully. Document why.

---

## State / Status (the `statecode` and `statuscode` of the workflow itself)

Not to be confused with the SetState activity (which changes a record's
status). The workflow record has its own state:

| statecode | statuscode | Meaning |
|-----------|------------|---------|
| 0 (Draft) | 1 (Draft) | Editable, will not run |
| 1 (Activated) | 2 (Activated) | Read-only in the legacy designer, runs on triggers |

**Workflows must be activated to run.** A common deployment mistake is
importing a solution containing workflows but forgetting to activate them.
The `publish-workflow` skill walks through activation.

When editing a workflow, **always check it's in Draft state first**.
Editing an activated workflow's XAML in a solution doesn't roll the changes
into the org — you need to deactivate, edit, re-activate (or import the
updated solution and re-activate).

---

## Quick decision tree

```
"What kind of workflow do I need?"

   ┌─ Triggered by user save?
   │     ├─ Need to block the save on failure?  → Real-Time + sync triggers
   │     ├─ Otherwise                            → Background
   │
   ├─ Triggered by another workflow?            → Background, Trigger=ChildWorkflow
   │
   ├─ Triggered by a button / API call?         → Background, Trigger=OnDemand
   │
   └─ Long-running / waits for time / event?    → Background (Real-Time can't wait)
```

```
"What scope should I use?"

   Default:                                      → Organization
   "Only fires for records owned by X user":     → User (rare; usually a bug)
   "Multi-tenant within one org":                → Business Unit / Parent:Child BU
```

```
"What run-as should I use?"

   Default for triggered:                        → Calling User
   Default for on-demand admin tasks:            → Owner (service account)
   Need elevation:                               → Owner (audit carefully)
```

---

## Patterns to flag in summaries / reviews

When the `analyze-workflow` skill is invoked, surface these as findings:

| Pattern | Severity | Why it matters |
|---------|----------|----------------|
| `Trigger=OnUpdate` with no filtering attributes | High | Fires on every update; severe perf cost |
| `Mode=RealTime` with `Persist` or Wait Condition | Critical | Will fail to activate |
| `Mode=Background` with only `mcwc:` activities | High | Activities silently do nothing |
| `RunAs=Owner` and owner is the personal account of an individual | High | Workflow breaks if that user is disabled |
| `Scope=User` | Medium | Unusual; verify intent |
| `StartChildWorkflow` to a workflow on a different primary entity | Medium | Verify the child accepts the entity reference correctly |
| Many sequential `UpdateEntity` calls on the same record | Low | Could be combined into one `UpdateEntity` for performance |
| Real-time workflow making external calls (custom activity hitting the network) | Critical | Blocks the user save until the call returns / times out |
| Background workflow that updates a column it triggers on, with no guard | Critical | The engine cancels the workflow after **16 runs** on the same row in a short window with the message "This workflow job was canceled because the workflow that started it included an infinite loop." Add a Check Condition comparing old vs new value, or a "WorkflowProcessed" guard column. |
| Two or more background workflows triggered by the same column on the same entity | High | Concurrent updates cause `SQL Timeout: Cannot obtain lock on resource …`. Consolidate logic into one workflow or one child workflow. |
| Real-time workflow that uses `Parallel Wait Branch` | Critical | Same constraint as Wait Conditions — real-time forbids any wait construct. |
| Check Condition uses `Under` / `Not Under` operators | Medium | Activation fails in target orgs whose entity has no relationship marked **Hierarchical**. Add a deployment dependency note. |
| Background workflow without **Automatically delete completed workflow jobs** enabled | Info | Successful job logs accumulate in `AsyncOperationBase` (file capacity) and degrade query performance over time. Failures are always retained regardless. |
