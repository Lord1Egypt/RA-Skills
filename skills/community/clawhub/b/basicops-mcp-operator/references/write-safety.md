# BasicOps write safety

Use this reference before non-trivial writes or whenever the requested mutation may be ambiguous or risky.

## Shared rules

- Write only when the target object is clear.
- Write only when the requested mutation is clear.
- In shared or demo workspaces, confirm you are operating on the intended workspace, project, task, or user context before non-trivial writes.
- Ownership is not a reason to block valid edits by itself, but it is a useful signal that you may be looking at the wrong object or workspace.
- If either target or mutation is unclear, ask one concise clarifying question.
- Prefer the smallest valid write that satisfies the request.
- After writing, summarize what changed.

## Assignment changes

Before assigning:
- resolve the requested person clearly
- avoid guessing between multiple similar names
- if there are multiple plausible matches, ask one question

Good question:
- "Do you mean Amanda Lee or Amanda Chen?"

## Status changes

Map casual language to likely valid statuses when the meaning is obvious.

Examples:
- start this -> In Progress
- mark complete -> Complete
- put this on hold -> On Hold

If the workspace uses custom statuses and the mapping is not obvious, inspect current valid values first or ask briefly.

## Subtask and checklist creation

Create a sensible, modest set.

Default range:
- usually 3 to 7 items

Do not create a giant list unless the user explicitly asks for one.

## Reviews

Request review when the task is ready for sign-off or feedback and the reviewer target is clear.

If the user names a reviewer ambiguously, resolve the person first.

## Message posting and replying

Prefer replying in the current thread or on the current object.

Avoid creating extra top-level messages when an in-thread reply is the natural fit.

## Destructive actions

Treat these as high caution:
- delete
- archive
- broad cross-project mutations
- irreversible cleanup

Require explicit user intent. Do not infer destructive intent from vague language.

## Good completion summaries

- "Assigned the task to Amanda and set the status to In Progress."
- "Posted the summary to the task thread and requested review from Kai."
- "Created 5 subtasks based on the rollout plan."
