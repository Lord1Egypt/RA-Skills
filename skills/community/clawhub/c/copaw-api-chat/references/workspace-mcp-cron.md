# Workspace / MCP / Cron

These API groups exist, but they are not the first place to start if the goal is simply to talk to CoPaw.

## /api/workspace
High-risk admin surface.
Use for:
- workspace export/import

Risk:
- can overwrite or leak workspace contents

## /api/mcp
Use for:
- managing MCP client config
- understanding integration boundaries around MCP

Important:
- this is config management, not the same thing as talking to CoPaw as a chat agent

## /api/cron
Use for:
- scheduled jobs
- cron inspection / control

Important:
- useful later for automation around CoPaw, not for the first chat integration step

## Rule of thumb
If the task is:
- "talk to CoPaw"
start with `chats-console-sse.md`

If the task is:
- "administer CoPaw"
then these APIs become relevant.
