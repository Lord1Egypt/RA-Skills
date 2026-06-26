# Task Edge Cases

Read this file only when the task request involves field semantics or workflows outside the common create/update/member path.

## Time Fields

- `start` and `due` accept either an all-day date or a precise datetime.
- Clear them explicitly; do not rely on omission.
- Use the CLI flags that map to these cases instead of editing raw payloads first.

## Completion Semantics

- Use `complete` and `reopen` commands instead of editing `completed_at` directly.
- A completed task cannot be completed again with a different non-zero timestamp without reopening first.

## Origin

- `origin` is create-only in this skill.
- If you need to set it, prefer `create` arguments instead of retrofitting it into update logic.

## Deferred Features

These are intentionally deferred from v1 and should not be improvised through raw payloads unless the user explicitly wants toolkit changes:

- reminders
- tasklists
- dependencies
- repeat rules
- custom complete
- attachments
