---
name: fragments-daily-log
description: Prompt user to record daily work log after session completes meaningful work
events:
  - session.idle
---

# Fragments Daily Log Hook

Triggered when a session becomes idle after performing meaningful work.

## Behavior

When the session completes with tool calls or significant activity:

1. Assess whether this session performed meaningful work (tool calls, file edits, etc.)
2. If yes, prompt the agent to follow the fragments skill daily-log workflow:
   - Call `memos_get_daily_log` for today's date
   - Diff against existing content
   - Format new entries in `.plan` style
   - Show the user the merged log and ask for confirmation before saving

## Requirements

- fragments skill must be enabled
- MCP server `memos` must be configured
- Environment variables `MEMOS_URL` and `MEMOS_PAT` must be set
