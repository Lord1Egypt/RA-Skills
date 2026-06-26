# claw2claude

Bridges OpenClaw and Claude Code CLI — letting your OpenClaw AI act as an **orchestrator** that delegates complex tasks to a local Claude Code session. Works on any platform OpenClaw supports: Discord, WhatsApp, Telegram, Slack, and more.

---

## How it works

```
User sends a message (Discord / WhatsApp / Telegram / …)
    ↓
OpenClaw AI reads the claw2claude skill and invokes launch.sh
    ↓
launch.sh auto-detects the user's active channel session
launch.sh starts notifier.py in the background (polls every 2s)
launch.sh starts Claude Code (claude CLI) in the project directory
    ↓
Claude reads/writes files, executes code, reasons through the task
    ↓
parse_stream.py collects Claude's stream output and writes .claude-notify.json
    ↓
notifier.py detects the file, splits the summary into ≤500-char chunks,
and delivers each chunk to the user's channel via the OpenClaw message tool
    ↓
Session ID saved → next message resumes the same Claude session via --resume
```

---

## Modes

| Mode | When to use | Behaviour |
|------|-------------|-----------|
| `discuss` | Requirements are unclear; user wants to explore options | Claude advises, no code written |
| `execute` | Task is clear; user wants code written or changed | Claude implements directly |
| `continue` | Pick up where we left off | Resumes previous session, same mode |
| `background` | User doesn't want to wait for the result | Runs detached; notified on completion |

**Session continuity:** `execute` mode always resumes the last session (whether it was `discuss` or `execute`), keeping all messages in one continuous Claude conversation per project.

---

## Requirements

- `claude` CLI on PATH — [Claude Code](https://claude.ai/code)
- `python3` on PATH
- OpenClaw gateway running

---

## Installation

```bash
cp -r claw2claude ~/.openclaw/skills/
```

Then apply the required `openclaw.json` changes below and restart the gateway.

---

## Required openclaw.json changes

Two settings must be added. Open `~/.openclaw/openclaw.json` and apply:

### 1. Allow the `message` tool through the gateway

The notifier process sends results by calling the gateway's `message` tool directly (as an external process, not inside an AI turn). By default the gateway restricts which tools external callers can invoke.

```json
"gateway": {
  "tools": {
    "allow": [
      "sessions_send",
      "message"
    ]
  }
}
```

> Without this, the notifier cannot deliver results on any platform.

### 2. Allow cross-session messaging

The notifier runs outside the original AI session tree, so openclaw's session visibility check blocks it by default.

```json
"tools": {
  "sessions": {
    "visibility": "all"
  }
}
```

> Without this, any `sessions_send` call from the notifier returns `forbidden`.

### Complete minimal diff

```json
{
  "gateway": {
    "tools": {
      "allow": ["sessions_send", "message"]
    }
  },
  "tools": {
    "sessions": {
      "visibility": "all"
    }
  }
}
```

Restart the gateway after saving:

```bash
openclaw gateway restart
```

---

## Delivery pipeline

Results are delivered by `notifier.py`, which runs in the background while Claude works. Priority order:

| Priority | Method | Coverage |
|----------|--------|----------|
| 1 | OpenClaw `message` tool via gateway | All platforms (Discord, WhatsApp, Telegram, Slack, Signal, Line, Matrix, …) |
| 2 | Discord bot API directly | Discord only — fallback when gateway is unreachable |
| 3 | macOS native notification | Last resort — always available locally |

The notifier auto-detects which channel to deliver to by reading `~/.openclaw/agents/main/sessions/sessions.json` at launch time and picking the most recently active user session. No manual configuration needed.

Long summaries are split into ≤ 500-character chunks (split at markdown section headings first, then sentence boundaries) and sent as separate messages so nothing gets truncated.

---

## Session state

Each project keeps a `.openclaw-claude-session.json` file in its directory:

```json
{
  "session_id": "abc123…",
  "mode": "execute",
  "project_path": "/Users/you/Projects/myapp",
  "updated_at": "2026-04-06T10:00:00"
}
```

This is used by `launch.sh` to resume the correct Claude session on the next invocation. The file is git-ignored automatically.

---

## Script reference

| Script | Role |
|--------|------|
| `launch.sh` | Main entry point. Reads session state, builds `claude` CLI args, starts notifier, runs Claude. |
| `parse_stream.py` | Parses Claude's `stream-json` output. Extracts the `---CHAT_SUMMARY---` block and writes `.claude-notify.json` when Claude finishes. |
| `notifier.py` | Background process. Polls for `.claude-notify.json`, chunks the summary, delivers to user via gateway. Self-terminates on delivery or Claude exit. |
| `find_session.py` | Reads `sessions.json` and returns the most recently active user-facing session key. Used by `launch.sh` for auto-detection. |
| `projects.py` | Registry of known project paths (up to 20), sorted by last-active time. Used for "continue" disambiguation. |
| `heartbeat.py` | Used in `background` mode only. Monitors the background Claude PID and notifies when done. |
| `check_token.py` | Checks API token health before Claude starts. |
| `read_session.py` / `write_session.py` | Atomic read/write helpers for `.openclaw-claude-session.json`. |

---

## Adding usage rules to your USER.md

Add this block to your agent's `USER.md` to control when and how the skill fires:

```markdown
## Tool routing with claw2claude

- **Route code tasks to Claude Code** — for any task involving code (reading,
  reviewing, writing, refactoring, architecture design), use the `claw2claude`
  skill to delegate to the local Claude Code CLI. Claude Code has direct
  filesystem access and is purpose-built for these tasks.

- **Check in before starting large projects** — when the user proposes a
  substantial new project (software, business plan, long-form document, etc.),
  ask first: "This looks like a multi-round project — would you like me to set
  up a Claude Code project directory?" Delegate only after the user confirms.

- For tasks within `claw2claude`'s scope, act as a coordinator: clarify the
  request, choose the right mode (discuss / execute), and deliver the result.
  Do not duplicate work that Claude Code will handle.
```
