# ClickUp Operator Internal Smoke Test

Run this after filling the config with a real ClickUp workspace.

## Task creation

Prompt:

`Create a task to check my task list.`

Verify:

- created in general to-do list
- assigned to default assignee
- due date defaults to today

## Idea capture

Prompt:

`Capture this idea: create a cleaner weekly planning ritual.`

Verify:

- created in ideas list
- no assignee
- no due date

## Project-contained work

Prompt:

`Put this in the Website Redesign project: tighten the mobile CTA spacing.`

Verify:

- created in the named project list
- no auto-assignee
- no auto due date

## Read behavior

Prompt:

`What's on my list today?`

Verify:

- only assigned-to-default-assignee items
- only due-today items
- completed items excluded

## Failure logging

If any step fails, capture:

- the exact prompt
- expected behavior
- actual behavior
- whether the issue came from routing logic, config, or ClickUp/MCP behavior
