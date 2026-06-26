---
name: awesome-remote-control
description: Start a Claude Code remote control session in tmux with bypass permissions. Use when asked to start a remote session, start a Claude Code session, spin up Claude Code, or any variation of starting Claude Code remotely for a project. Multiple sessions can run simultaneously.
metadata:
  {"openclaw": {"requires": {"bins": ["tmux", "python3", "claude"]}}}
---

# Claude Code Remote Control

Starts a persistent Claude Code session in tmux with `--dangerously-skip-permissions --remote-control`. Auto-exits after 30 minutes of inactivity via `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` (Claude's native idle timer). Multiple concurrent sessions supported — each gets a unique animal name.

## Starting a Session

**Single session:**
```bash
bash skills/claude-remote-control/scripts/start_session.sh <dir>
```

**Multiple sessions in parallel (faster):**
```bash
bash skills/claude-remote-control/scripts/start_sessions.sh <dir> <count>
# e.g. start_sessions.sh /path/to/project 3
```

Each session gets a friendly name like `🦊 Fox | my-project` — used in tmux and the registry.

**Important:** After launching a session, always report the session URL (`https://claude.ai/code/session_...`) back to the user in your reply. The URL is printed in the script output — surface it so the user can open the remote control page immediately.

## Stopping a Session

```bash
bash skills/claude-remote-control/scripts/stop_session.sh <session-label|tmux-name>
# e.g. stop_session.sh "🦊 Fox | my-project"
#      stop_session.sh cc-fox-my-project
```

The `SessionEnd` hook fires automatically, handling registry update.

## Listing Sessions

```bash
bash skills/claude-remote-control/scripts/list_sessions.sh
```

Registry stored at `~/.local/share/claude-rc/sessions.json`.

## Attaching to a Session

```bash
tmux attach -t cc-fox-my-project   # use tmux name shown on start
```

## Resuming a Session by UUID

When a session dies (killed or idle timeout), the registry entry is marked `dead` and the local UUID is captured at that moment. UUIDs persist for 30 days before being pruned.

Look up the UUID:
```bash
cat ~/.local/share/claude-rc/sessions.json
```

Resume using the start script with `--resume <uuid>`:
```bash
bash skills/claude-remote-control/scripts/start_session.sh <dir> --resume <uuid>
# e.g. start_session.sh /path/to/project --resume abc123-def456
```

Or manually in a new tmux session:
```bash
tmux new-session -d -s "cc-fox-my-project" -c "/full/path/to/my-project"
tmux send-keys -t "cc-fox-my-project" 'claude -r "<uuid>" --dangerously-skip-permissions --remote-control --name "🦊 Fox | my-project"' Enter
```

This restores full conversation history. A new remote control URL is issued on reconnect.

## How Idle Timeout Works

1. `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY=1800000` (30m) is set as an env var when launching Claude in tmux.
2. Claude's internal timer starts when it finishes responding and is idle at the prompt.
3. After 30m idle, Claude auto-exits — triggering the `SessionEnd` hook.
4. `on_session_end.sh` fires: marks the registry dead with UUID capture.

No background watcher process — everything is driven by Claude Code's native hooks.

## Sending Tasks to Running Sessions

```bash
bash skills/claude-remote-control/scripts/send_task.sh <session-label|tmux-name> "<message>"
# e.g. send_task.sh "🦊 Fox | my-project" "Do an analysis of the codebase"
#      send_task.sh cc-fox-my-project "Fix the issues you identified"
```

The script:
1. Resolves the tmux session name from a label or direct tmux name
2. Verifies the session is alive
3. Sends via `tmux send-keys -l` (literal mode — safe for special characters) + `Enter`

**Tip:** When sending follow-up tasks to a session that already has context (e.g., it just finished an analysis), do NOT re-paste the full spec or issue list. The agent already has that in its conversation. Just reference it — e.g., "fix the issues you identified". Re-sending bloats context and wastes tokens.

## Notes

- After launching, **always report the session URL** (`https://claude.ai/code/session_...`) to the user — this is the remote control link they need
- `--remote-control` is undocumented but valid — activates remote control on startup
- The `session_0...` URL is a cloud-side remote control ID — it cannot be used with `claude -r`. Only the local UUID from the registry works for resuming.
- UUID is captured lazily when the session dies, not during startup — no background polling
- Dead entries auto-prune after 30 days (runs at each startup)
- The project dir formula: `~/.claude/projects/$(echo $WORKDIR | sed 's|/|-|g')` (leading `-` is kept)
- No background watcher — idle timeout and registry cleanup are handled entirely by Claude Code hooks
- Workspace trust is pre-seeded in `~/.claude.json` (under `projects[<path>].hasTrustDialogAccepted`) so headless sessions skip the "do you trust this folder?" dialog