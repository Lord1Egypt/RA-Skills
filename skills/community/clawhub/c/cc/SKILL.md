---
name: cc
description: "Claude Code relay via tmux. Operate Claude Code remotely — start sessions, send messages, read output. Use when the user wants to interact with Claude Code from Telegram or any OpenClaw channel."
metadata: { "openclaw": { "emoji": "⚡", "requires": { "bins": ["tmux", "claude"] } } }
---

# cc — Claude Code Relay

Operate Claude Code remotely from any OpenClaw channel via tmux.

Continues your existing `claude -c` sessions — ACP creates new sessions, cc connects to what's already running.

**Language**: Always reply in the same language the user uses.

## Script

```bash
{baseDir}/scripts/cc.sh <command> [args...]
```

## Commands

| Command | Action |
|---------|--------|
| `/cc on <project>` | Start session (`claude -c` in project dir) |
| `/cc off [project]` | Stop session |
| `/cc ?` | Check Claude Code status (running/idle/dead) |
| `/cc tail [project] [lines]` | Show recent output |
| `/cc projects` | List available projects |
| `/cc status` | List active sessions |
| `/cc config root <path>` | Set project root directory |
| `/cc` | Show help + project list |
| `/cc <message>` | Send message to Claude Code |

## Relay Mode (CRITICAL)

After `/cc on <project>`, you enter relay mode:

1. **ALL user messages are forwarded to Claude Code** — NEVER answer yourself
2. Only messages NOT forwarded: `/cc off`, `/cc ?`, `/cc tail`, `/cc status`, `/cc projects`, `/cc config`
3. Relay mode ends on `/cc off`

**You are a transparent pipe. Never interpret, analyze, or answer the user's question yourself.**

## Starting a Session

1. Run: `scripts/cc.sh on <project>`
2. Report to user:
   ```
   ✅ Claude Code session started for <project>
   Your messages will now be sent directly to Claude Code.
   Send /cc off to exit relay mode.
   ```
3. Enter relay mode

## Sending Messages (relay flow)

When user sends a message in relay mode:

1. **Immediately reply: ⏳** (so user knows message was received)
2. Forward: `scripts/cc.sh <project> "<user's message>"`
3. The script returns the **incremental output** — only content from this reply, not history
4. Return output to user (see Output Formatting below)

## Stopping a Session

1. Run: `scripts/cc.sh off <project>`
2. Report to user:
   ```
   Session ended. You're back to normal chat.
   ```

## Status Check (`/cc ?`)

Run: `scripts/cc.sh check <project>`

Report result to user:
- "🟢 Claude Code is running and waiting for input"
- "🔄 Claude Code is processing..."
- "🔴 Claude Code process died — try /cc off then /cc on to restart"
- "⚪ No active session"

## `/cc` (no arguments)

Run `scripts/cc.sh projects`. Show brief help + project list.

If there's a last-used project (marked with ★), show it first. Keep the response short — just names, no paths.

## First-time Setup

When `scripts/cc.sh projects` outputs `SETUP_NEEDED` (exit 100):

1. Check: `which tmux` and `which claude` — report if missing
2. Ask user: "Where are your projects? (e.g., ~/projects)"
3. Run: `scripts/cc.sh config root <their-answer>`
4. List projects to confirm

## Output Formatting

**If output ≤ 4000 characters**: wrap in one code block and send.

**If output > 4000 characters**: send a summary of the key output (first meaningful paragraph + last 10 lines), then add:
"Full output: send /cc tail to see more"

**Always**: strip ANSI escape codes (the script handles this automatically).

## Requirements

- `tmux` installed
- `claude` CLI installed (`npm i -g @anthropic-ai/claude-code`)
- Any OpenClaw channel (Telegram, Discord, CLI, etc.)
