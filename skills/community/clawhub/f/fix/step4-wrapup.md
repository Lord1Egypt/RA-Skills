# Step 4: Wrap-up (Report + Task Pruning)

**⚠️ Chained /fix Resume integrated execution gate (HARD STOP)**:

If /fix has been invoked 2+ times in this session, **before** marking fix-* tasks deleted in Step 4, collect **all 🔄 Resume tasks** in TaskList and verify outstanding work.

| # | Don't | Do |
|---|-------|-----|
| 1 | completed→deleted only the current fix's fix-2 | Collect **every** task in TaskList containing the `🔄 Resume` keyword |
| 2 | Ignore and delete a prior fix's Resume that is in_progress | **Split prior Resume's outstanding work into separate tasks** before deleting |
| 3 | Mark each fix complete independently | **Integrate and clean up** outstanding work from all Resumes before bulk-deleting |

**Procedure**:
1. Call `TaskList` → collect every task containing `🔄 Resume` or `Resume`
2. Extract outstanding work from each Resume task's description
3. **Register outstanding work as new tasks** (without the fix-* prefix)
4. Only after new tasks are registered, **bulk-delete all fix-* tasks**

```text
Fix complete:
- 🔍 Root cause: {what was missing}
- 🔧 Improvement: {which file was modified and how}
- 🔄 Current fix: {result of fixing the current issue}
- 📋 Wrap-up: {fix-* tasks deleted, outstanding work separated}
```

**Section emoji prefix matches fix-* task emojis (HARD STOP)**: The report's section prefix must use the same emojis as the fix-0/1/2/3 task emojis registered in Step 0. This keeps section identity consistent between the registered task and its report deliverable. Do not omit the emoji or substitute different ones.

| Task (Step 0) | Report section |
|---------------|---------------|
| 🔍 fix-0 (root cause analysis) | 🔍 Root cause |
| 🔧 fix-1 (root cause fix) | 🔧 Improvement |
| 🔄 fix-2 (Resume original work) | 🔄 Current fix |
| 📋 fix-3 (Wrap-up: report + task pruning) | 📋 Wrap-up |

**Outstanding-work separation guard (HARD STOP — required before deleting fix-* tasks)**:

If fix-2 (Resume Original Work) contains outstanding work, **separate by medium per status** before deleting fix-* tasks:

## Medium separation principle (HARD STOP)

| Status | Example | Medium (TaskList vs checklist) |
|--------|---------|--------------------------------|
| Hold (user decision) | "Track B is next session", "Playwright on hold" | **TaskList**: when actionable |
| Partial completion | Track A done, Track B not run | **TaskList**: separate task for Track B |
| Awaiting follow-up verification | Awaiting CI pass, awaiting merge review | **TaskList**: can trigger verification |
| **Awaiting external response (BLOCKED)** | Awaiting owner reply, external API lock, awaiting permission grant | **Register in fix_plan.md hold section (no task)** |
| **Cannot proceed autonomously** | Items that cannot move one step without user decision/external action | **fix_plan.md hold section** |

**Why is BLOCKED forbidden as a task?**
- TaskList = "tracking actionable work" medium. Only register items that can be auto-triggered
- BLOCKED = no external trigger means no progress → tracking it as a task adds no value beyond "still BLOCKED" reports each session
- fix_plan.md hold section = "carry over to next session + trigger when external response arrives" information preservation
- Registering an item in both media only adds sync burden

## Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Register external-wait items in both a separate task and fix_plan | Register only in fix_plan.md hold section. No task creation |
| 2 | Create a task with subject "[BLOCKED] awaiting reply on xxx" | Use fix_plan.md `## Hold` section in the form `- [ ] [BLOCKED] xxx (... awaiting reply, trigger: ...)` |
| 3 | "Register as task so the user doesn't forget" thinking | fix_plan.md is reloaded at each session start, so it won't be forgotten. The checklist is sufficient |
| 4 | Keep both checklist and task entries to "strengthen safety" | Duplicate media = mismatch risk. Unify to a single medium |

## Self-check procedure (before deleting fix-3)

1. Re-read fix-2 subject + body → extract the full list of original work
2. Classify each item's status:
   - (a) Done — task completed
   - (b) Actionable hold / partial completion / verification needed — register as a separate task in **TaskList**
   - (c) **BLOCKED (external response/permission)** — register in **fix_plan.md hold section (no task)**
3. fix-* tasks may only be deleted after (b) and (c) are reflected in their media
4. If a wrong BLOCKED task is found → immediately delete + transfer to fix_plan.md

**Violation patterns**:
- fix-2 "resume original work" scope had Track A + B; completed only Track A and marked fix-2 completed → deleted
- Misclassifying a user-held item as "done"
- Losing outstanding-work information for the sake of TODO list cleanliness

**Correct flow** (example):
- Before marking fix-2 complete: register Track B (the unfinished verification) as a separate task → fix-2 completed → fix-* deleted

**After reporting + outstanding-work separation verified, delete all `fix-*` TODO items created in Step 0** — fix TODOs are temporary session-level tracking only; outstanding work is preserved in separate tasks while only `fix-*` are cleaned up.

**[Measure 3] Status-based pruning of completed tasks (MANDATORY — HARD STOP)**:

The cleanup-step prune target is **status-based, not prefix-based**. Cleaning up only `fix-*` and leaving the original-work tasks behind is a violation.

## Prune target matrix

| Task kind | Status | Cleanup target? |
|-----------|--------|-----------------|
| **fix-\*** | completed | ✅ mark deleted |
| **fix-\*** | in_progress / pending | ❌ keep (work incomplete) |
| **original-work tasks** (created this session) | completed | ✅ mark deleted |
| **original-work tasks** (created this session) | in_progress / pending | ❌ keep (outstanding work) |
| **remaining actionable task** (not awaiting external response) | pending | ❌ keep |
| **BLOCKED task** (awaiting external response) | pending | ❌ keep + consider transferring to the fix_plan.md hold section |
| **stale tasks from a prior session** | any status | delete only on explicit user instruction (no autonomous deletion) |

## Don't / Do table

| # | Don't | Do |
|---|-------|-----|
| 1 | Mark only `fix-*` tasks deleted and keep the completed original-work tasks | Mark **all completed tasks created this session** deleted (both `fix-*` and original work) |
| 2 | Assume "only the `fix-*` prefix is the cleanup target" | The prefix is just an identifier. The criteria are **status (completed) + creation time (this session)** |
| 3 | Keep completed original-work tasks "just in case, for history tracking" | TaskList is for tracking active work. Completed history is preserved in git log / fix_plan.md / report text. Keeping it in TaskList is stale noise |
| 4 | Bulk-delete down to remaining pending tasks too | pending = outstanding work. Keeping it is correct. Distinguish status clearly |
| 5 | Clean up stale tasks from a prior session along with these | Only this session's tasks are cleanup targets. Prior-session tasks need a separate decision (user instruction) |

## Self-check (every time before marking fix-3 deleted)

1. **Call `TaskList`** to read the full task state
2. Identify the tasks created this session (both `fix-*` and original work)
3. Classify by status:
   - completed → cleanup target
   - in_progress / pending → keep
4. Mark all completed (`fix-*` + original work) tasks deleted
5. State the keep reason for remaining pending tasks in the report

## Case history

A session completed all of its original-work tasks plus the fix-* tasks, but only fix-* were pruned — the completed original-work tasks lingered as stale noise. This is what the status-based (not prefix-based) rule prevents. (See failed-attempts.md "status-based prune".)
