# ClickUp Operator Safe Live Smoke Test

Use this when the current ClickUp setup is already live and you want the smallest realistic proof.

## Before starting

- use a temporary validation config snapshot
- do not overwrite any main/live config
- keep all created items prefixed with `TEST - `

## Step 1. General to-do

Prompt:

`Create a task to check my task list.`

Create it as:

- `TEST - Check my task list`

Verify:

- lands in the live general to-do list
- assigned to the default assignee
- due date defaults to today

## Step 2. General idea

Prompt:

`Capture this idea: create a cleaner weekly planning ritual.`

Create it as:

- `TEST - Cleaner weekly planning ritual`

Verify:

- lands in the live ideas list
- no assignee
- no due date

## Step 3. Read test

Prompt:

`What's on my list today?`

Verify:

- only due-today items
- only items for the default assignee
- completed items excluded

## Optional Step 4. Project-contained item

Prompt:

`Put this in the Website Redesign project: tighten the mobile CTA spacing.`

Create it as:

- `TEST - Tighten the mobile CTA spacing`

Verify:

- lands in the named project list
- no auto-assignee
- no auto due date

## Result interpretation

If Steps 1 through 3 pass, the packaged skill has proven the core operator logic against the live setup.

Step 4 is useful, but optional for the first safe validation pass.
