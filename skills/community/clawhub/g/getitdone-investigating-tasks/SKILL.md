---
name: investigating-tasks
description: "Explains a single GetItDone task in full: its content, status, dependencies, attachments, and what an attached video or screen recording shows. Use when the user asks to 'open T-123', 'why can't this task start', 'what is this task waiting on', 'what's in this task', 'what does the screen recording on this task show', or wants a deep dive on one task. Read-only."
---

# GetItDone task deep dive

Read one task end to end, including its notes, attachments, dependencies, and any attached video, and explain it in plain words. Read only.

## Connecting and calling the tools

Every tool in this skill comes from the `getitdone` MCP server, the GetItDone connector, and is written here as `getitdone:<tool>`.

- **Tools listed by name:** call them directly, for example `getitdone:list_tasks`.
- **Only `getitdone:search_tools` and `getitdone:execute_typescript` listed (Code Mode, the default):** call `getitdone:search_tools` first, then call each tool inside `getitdone:execute_typescript` as `external_<tool>` (for example `external_list_tasks`); the program must `return` its result. Scopes, confirmations and gates are identical on both surfaces.
- **"Tool not found":** switch to the Code Mode route instead of retrying the direct call. If `getitdone:search_tools` does not return the tool either, its OAuth scope was not granted; the user reconnects GetItDone and approves that scope.
- **No `getitdone` tools at all:** GetItDone is not connected yet. Install the GetItDone power, which adds the server; it signs in with OAuth on first use.

## Tools you will use

If the tool list shows only `getitdone:search_tools` and `getitdone:execute_typescript`, the server is in Code Mode: call each operation below inside `getitdone:execute_typescript` as `external_<name>`.

- `getitdone:list_tasks`: find the task's short id when the user gave only a name.
- `getitdone:get_task_details`: the task's rich-text notes, every attachment with a short-lived URL, and its dependency chain (what blocks it and what it blocks). Takes the short id (123 for T-123) or task version id.
- `getitdone:get_task_video_context`: evenly spaced still frames from a video uploaded to the task's notes or attachments, with a text summary, plus any YouTube or Vimeo links found in the notes.

## Workflow

1. If the user gave a name instead of a short id, call `getitdone:list_tasks` and match it. Ask if more than one task matches.
2. Call `getitdone:get_task_details`.
3. Summarize: status, priority, due date, a short summary of the notes, the attachments by file name, and the dependency chain.
4. If the task is blocked, name each blocking task with its status. Offer to open the blocker the same way.
5. If the task has a video, or the user asks what a recording shows, call `getitdone:get_task_video_context` and describe what the frames show, in order.

## Rules

- `getitdone:get_task_video_context` extracts still frames. It does not transcribe audio and does not watch linked YouTube or Vimeo videos. Say that when you describe a video, and list any linked videos as links only.
- In Code Mode only the tool's JSON summary comes back, not the frame images. Describe what the summary says and tell the user the frames themselves need a connection on the full tool surface.
- "No videos found on this task." is a normal result. Report it plainly.
- Attachment URLs expire. Do not store them or present them as permanent links; fetch the task again when the user needs a fresh one.
- Do not change the task from this skill: never call `getitdone:create_task`, `getitdone:update_task`, `getitdone:complete_task_occurrence`, `getitdone:link_task_dependency`, or `getitdone:archive_task`. Hand off to `capturing-tasks` for changes.
