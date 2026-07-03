---
description: "Execute a task from tasks.md by task ID (e.g., T-008). Reads the spec, dispatches to the assigned subagent via Task tool."
argument-hint: "Task ID, e.g. T-008"
---

Execute the following task from the project task list.

## Steps

1. **Read task list**: Read `.spec-flow/active/{{PROJECT_SLUG}}/tasks.md` and find the task matching `$ARGUMENTS`. Extract its:
   - `description` (the actual work to do)
   - `dependencies` (other task IDs that must be ✅ Done first)
   - `status` (must not be ✅ Done; if Done, report and stop)
   - `complexity` (informational)
   - `assigned_agent` (the subagent name to dispatch to)
   - `module` (the target module path)

2. **Dependency check**: For each task in `dependencies`, verify its status is ✅ Done in `tasks.md`. If any are not done, stop and report which are blocking. Do not proceed.

3. **Read module CLAUDE.md**: Read `<module>/CLAUDE.md` (resolve `module` from the task). If the file doesn't exist, warn but continue.

4. **Dispatch to subagent**: Use the Task tool with:
   - `subagent_type`: `assigned_agent` (e.g., `backend-developer`)
   - `prompt`: A prompt containing:
     - The task `description` verbatim
     - Relevant context from `design.md` (cite specific sections)
     - Reference to the module's `CLAUDE.md`
     - Instruction to follow the module's CLAUDE.md conventions
     - Instruction to update the module's `CLAUDE.md` if functionality changes

5. **Verify completion**: After the subagent returns, the SubagentStop hook will automatically run quality checks. The main agent does not need to re-run lint/type-check/tests manually.

6. **Report back**: Summarize:
   - What was done (files changed, key decisions)
   - Test results (if subagent ran them)
   - Whether the module's `CLAUDE.md` was updated
   - Whether follow-up tasks are needed (e.g., related T-IDs)

## Error handling

- If `$ARGUMENTS` is empty, respond: "Usage: /run-task T-XXX (e.g., /run-task T-008)"
- If the task ID is not found in `tasks.md`, list all available task IDs and ask which one
- If dependencies are not done, list blocking IDs and ask whether to wait or proceed anyway

## Example

User types: `/run-task T-003`

Expected flow:
1. Read `tasks.md`, find T-003 (assigned to `backend-developer`, module `src/api/users/`)
2. Check T-001 and T-002 are Done (dependencies)
3. Read `src/api/users/CLAUDE.md`
4. Call Task tool with subagent_type=`backend-developer`, prompt containing the T-003 description + relevant design.md context + reference to module CLAUDE.md
5. Wait for subagent, SubagentStop hook runs quality gate
6. Report results
