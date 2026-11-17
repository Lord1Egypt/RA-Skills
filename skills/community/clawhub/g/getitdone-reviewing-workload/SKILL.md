---
name: reviewing-workload
description: "Summarizes what is on the user's plate in GetItDone: tasks due, in progress, in review, and blocked, per workspace or project. Use when the user asks 'what's on my plate this week', 'what should I work on next', 'what's due', 'what's blocked right now', 'give me a status update on this project', 'show my to-do list', or wants a workload or project status overview. Read-only."
---

# GetItDone workload review

Turn the workspace's task list into a short, prioritized view of what needs attention. Read only.

## Connecting and calling the tools

Every tool in this skill comes from the `getitdone` MCP server, the GetItDone connector, and is written here as `getitdone:<tool>`.

- **Tools listed by name:** call them directly, for example `getitdone:list_tasks`.
- **Only `getitdone:search_tools` and `getitdone:execute_typescript` listed (Code Mode, the default):** call `getitdone:search_tools` first, then call each tool inside `getitdone:execute_typescript` as `external_<tool>` (for example `external_list_tasks`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `getitdone:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects GetItDone and approves that scope.
- **No `getitdone` tools at all:** GetItDone is not connected yet. Install the GetItDone power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

If the tool list shows only `getitdone:search_tools` and `getitdone:execute_typescript`, the server is in Code Mode: call each operation below inside `getitdone:execute_typescript` as `external_<name>`, and use one program to run several independent reads together.

- `getitdone:list_workspaces`: the workspaces the account belongs to, with their ids. Pass an id as `workspaceId` to target one.
- `getitdone:list_projects`: the projects in the workspace with their ids.
- `getitdone:list_tasks`: the latest version of each task with name, short id, status (`TODO`, `IN_PROGRESS`, `IN_REVIEW`, `COMPLETED`, `BLOCKED`), priority, due date, projects, whether it is blocked, and how many tasks it blocks. Filters by status, priority, and project.
- `getitdone:get_task_details`: notes, attachments, and the dependency chain for one task, when a summary line is not enough.

## Workflow

1. Call `getitdone:list_workspaces`. If the user belongs to more than one and did not name one, ask which, or use the one they usually work in and say which you used.
2. If the user named a project, call `getitdone:list_projects` and use its id as the `getitdone:list_tasks` filter.
3. Call `getitdone:list_tasks`. Leave out `COMPLETED` tasks unless the user asks for them.
4. Present, in this order:
   - Blocked tasks, with how many tasks each one blocks.
   - Overdue tasks and tasks due in the window the user asked about (default: the next 7 days), sorted by due date then priority.
   - In progress and in review.
   - A count of the remaining `TODO` tasks.
5. For the top blocked task, call `getitdone:get_task_details` and name what blocks it.
6. Close with at most three suggested next actions drawn from the list, such as the blocker that unblocks the most tasks.

## Rules

- Do not change anything from this skill: never call `getitdone:create_task`, `getitdone:update_task`, `getitdone:complete_task_occurrence`, `getitdone:link_task_dependency`, or `getitdone:archive_task`. Hand off to `capturing-tasks` for changes.
- Refer to tasks by short id and name so the user can find them in the app.
- If a project the user named is not in `getitdone:list_projects`, say it does not exist. Do not guess another one.
- If a workspace id the user gave is not one of theirs, say so and offer `getitdone:list_workspaces`.
