---
name: clickup-task
description: Create tasks in Vision Play ClickUp lists (visionplay or inbox).
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["bash","curl"],"env":["CLICKUP_TOKEN","CLICKUP_LIST_VISIONPLAY","CLICKUP_LIST_INBOX"]}}}
---

## Usage (Telegram / Chat)
Use the slash command:

/clickup-task <list> "<title>" "<description>"

- <list> must be: visionplay OR inbox
- title is required
- description is optional (use "" if you want blank)

Examples:
/clickup-task visionplay "Follow up with Rahul" "Ask for proposal + timeline"
/clickup-task inbox "Review tax doc" ""

## What this skill does
It runs this script on the server:

/usr/local/bin/clickup_create_task.sh <list> "<title>" "<description>"

## Execution instructions (for the agent)
When the user invokes this command:
1) Parse list/title/description exactly.
2) Run:

bash -lc '/usr/local/bin/clickup_create_task.sh "<list>" "<title>" "<description>"'

3) Return ClickUp API response (or any error text) to the user.

