<div align="center">
  <h1>Awesome Remote Control</h1>
  <p>An <a href="https://github.com/openclaw/openclaw">OpenClaw</a> skill for launching headless Claude Code sessions.<br>Remote control URLs and automatic idle timeout.</p>
  <p>
    <a href="#install"><strong>Install</strong></a>
    ·
    <a href="#usage"><strong>Usage</strong></a>
    ·
    <a href="#how-it-works"><strong>How It Works</strong></a>
  </p>
  <p>
    <img src="https://img.shields.io/github/actions/workflow/status/oobagi/awesome-remote-control/publish.yml?label=ClawHub" alt="ClawHub publish">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
    <img src="https://img.shields.io/badge/openclaw-skill-blue" alt="OpenClaw skill">
  </p>
</div>

---

## Install

```bash
clawhub install awesome-remote-control
```

Or clone manually:

```bash
git clone https://github.com/oobagi/awesome-remote-control.git ~/.openclaw/skills/claude-remote-control
```

Requires `tmux` and `python3`.

Start a new session and the skill is available automatically.

## Usage

Ask your agent:

> "Start a remote session for my-project"

> "Spin up 3 Claude sessions for my-project"

> "Send a task to Fox: do an analysis of the codebase"

> "List my remote sessions"

> "Stop the Fox session"

Each session gets a unique name like `🦊 Fox | my-project`, a remote control URL, and auto-exits after 30 minutes idle. Sessions can be resumed by UUID after shutdown.

## Scripts

| Script | Purpose |
|--------|---------|
| `start_session.sh` | Launch a single session |
| `start_sessions.sh` | Launch N sessions in parallel |
| `send_task.sh` | Send a task to a running session |
| `stop_session.sh` | Stop a session by name |
| `list_sessions.sh` | List active/dead sessions |

Shared internals: `registry.py` (session registry), `on_session_end.sh` (hook handler).

## How It Works

Sessions launch with `--dangerously-skip-permissions --remote-control` and `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` for automatic idle timeout. A JSON registry tracks active/dead sessions with UUIDs for resumption.

**What this skill modifies on your system:**

- **`~/.claude.json`** — sets `hasTrustDialogAccepted: true` for the target project directory so headless sessions skip the workspace trust prompt
- **`~/.local/share/claude-rc/sessions.json`** — registry of active/dead sessions with captured UUIDs
- **`~/.claude/projects/`** — reads `.jsonl` files to capture session UUIDs on shutdown

All modifications are scoped to the project you launch a session for. Nothing runs outside of what you explicitly start.

## License

MIT

