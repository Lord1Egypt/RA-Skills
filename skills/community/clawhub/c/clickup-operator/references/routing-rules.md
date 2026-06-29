# ClickUp Operator Routing Rules

## Decision order

1. Identify whether the user is asking for an idea capture, a general action item, project-contained work, or a read/query.
2. Check whether the user explicitly named a project, list, assignee, or due date.
3. Apply the smallest necessary default set from config.
4. Execute immediately unless ambiguity would change the correct destination or outcome.

## Creation rules

### General ideas

- Trigger phrases include things like "note this idea," "capture this idea," or "here's an idea."
- Default destination: ideas list.
- Do not auto-assign unless the user explicitly asks.
- Do not add a due date unless the user explicitly asks.

### General to-dos

- Trigger phrases include to-do, reminder, action item, or a plainly actionable one-off task.
- Default destination: general to-do list.
- Default assignee: configured default person unless overridden.
- Default due date: use user-supplied date or timeframe; otherwise default to today.

### Project-contained items

- If the user explicitly places an item inside a project, use that project list instead of a general list.
- Do not auto-assign or auto-date project-contained items unless the user explicitly asks.

### Promotion into a project

- If an idea or task becomes a real multi-step initiative, create or use a dedicated project list instead of keeping it in the generic lists.
- If project creation is not obviously requested, ask before creating new list structure.

## Update rules

- Handle move, assign, reschedule, rename, and status-change requests immediately when the target item is clear.
- If multiple candidate tasks match and the wrong one would matter, ask a concise disambiguation question.

## Read rules

### Active-work reads

- Ignore completed items by default.
- Default active-status filter:
  - `ideation`
  - `to do`
  - `in progress`
  - `review`

### "What's on my list today?"

- Only include tasks assigned to the configured default assignee.
- Only include tasks due today.
- Exclude tomorrow-or-later items unless the user explicitly asks for a broader view.

## Response style

- Prefer action plus brief confirmation.
- Avoid explaining the protocol unless the user asks.

Good:

- `Done, added it to General To-Do List and made it due today.`
- `Added to Ideas.`
- `Moved it into the Website Redesign list and left it unassigned.`

Bad:

- `That maps to our default rule.`
- `If you want, I can create that now.`
- `Per the operating protocol, this belongs in...`
