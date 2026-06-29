# ClickUp Operator Test Cases

Use these prompts to validate whether the package behaves like a clean operator instead of a chatty assistant.

## Creation

### General to-do with no date

Prompt:

`Create a task to check my task list.`

Expected:

- item goes to the general to-do list
- item is assigned to the default assignee
- due date defaults to today

### General idea

Prompt:

`Capture this idea: make a lightweight sales dashboard for daily outbound health.`

Expected:

- item goes to the ideas list
- no auto-assignee
- no auto due date

### Project-contained task

Prompt:

`Put this in the Website Redesign project: tighten the mobile hero spacing.`

Expected:

- item goes to the Website Redesign project list
- no auto-assignee
- no auto due date

### Explicit override

Prompt:

`Make me a task due tomorrow and assign it to Sarah.`

Expected:

- item goes to the general to-do list unless a project is named
- assignee changes from default to Sarah
- due date becomes tomorrow, not today

## Reads

### Today's list

Prompt:

`What's on my list today?`

Expected:

- only tasks assigned to the default assignee
- only items due today
- excludes completed items

### Active project view

Prompt:

`What is active in the Website Redesign project?`

Expected:

- only configured active statuses
- excludes completed items unless explicitly requested

## Ambiguity check

Prompt:

`Move that task into the project list.`

Expected:

- ask a follow-up if "that task" or "the project list" is not clear
- do not guess when the wrong move would matter
