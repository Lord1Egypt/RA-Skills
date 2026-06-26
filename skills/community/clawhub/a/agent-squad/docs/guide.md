# agent-squad — Full Guide

## How It Works

```
You (via OpenClaw)          agent-squad              AI Agent (in tmux)
       │                         │                         │
       ├─ "start a squad" ──────►├─ create tmux session ──►├─ AI starts coding
       │                         ├─ register watchdog       │
       │                         │                         │
       ├─ "assign task" ────────►├─ write task file ───────►├─ picks up task
       │                         │                         ├─ codes & commits
       │                         │                         ├─ updates report
       │                         │                         │
       ├─ "check status" ──────►├─ read reports ───────────┤
       │                         │                         │
       │                    watchdog (every 5 min)          │
       │                         ├─ agent alive? ──────────►├─ yes → do nothing
       │                         ├─ agent dead? ───────────►├─ auto-restart
```

Each squad runs an AI engine (Claude Code, Codex, etc.) inside a tmux session. A coordinator prompt tells the AI to follow `PROTOCOL.md` — pick up tasks, write code, update reports. A watchdog cron checks every 5 minutes and restarts the engine if it crashes.

## Operations

### Start a Squad

```
"Start a squad called backend using claude for ~/projects/my-api"
```

Options:
- **`--project <dir>`** — Where the squad writes code. Defaults to `~/.openclaw/workspace/agent-squad/projects/<name>/`.
- **`--restart`** — Reuse an existing squad's data (tasks, reports). Required if the squad name was used before.
- **`--agent-teams`** — Enable Claude Code Agent Teams mode (claude only). The coordinator can spawn sub-agents for parallel work.

Engine-specific checks run automatically:
- `codex` warns if the project is not a git repo
- `gemini` uses Google OAuth login (run `gemini` once to auth before starting a squad)

### Assign a Task

```
"Give backend a task: add JWT authentication"
```

Provide a clear objective. Optionally set priority: critical, high, normal (default), low.

Tasks are written as markdown files to `tasks/pending/`. The squad picks them up and moves them through `in-progress/` → `done/`.

### Check Status

```
"What is backend doing?"
```

Shows engine, running/stopped state, task counts, and the current activity from the squad's report.

### Ping for Update

```
"Ask backend to report"
```

Sends a message to the squad asking it to update its progress report immediately.

### Stop a Squad

```
"Stop backend"
```

Kills the tmux session and removes the watchdog cron. All data (tasks, reports, logs) is preserved. Restart with `--restart`.

### Delete (Archive) a Squad

```
"Delete backend"
```

Archives the squad's coordination data to `.archive/`. The project code directory is **never touched**. Requires confirmation.

### Configure Settings

```
"Change default project directory to ~/code"
```

Sets the default directory for new squad projects. Stored in `config.json`. Existing squads are not affected.

### List All Squads

```
"What squads do I have?"
```

Shows all squads with engine, running/stopped status, and task counts.

## Directory Structure

Code and coordination data are kept separate — deleting a squad never touches your code:

```
~/.openclaw/workspace/agent-squad/
├── squads/<name>/              ← Coordination data
│   ├── tasks/
│   │   ├── pending/            ← New tasks land here
│   │   ├── in-progress/        ← Currently being worked on
│   │   ├── done/               ← Completed tasks
│   │   └── cancelled/          ← Cancelled tasks
│   ├── reports/                ← Progress reports per task
│   ├── logs/                   ← Watchdog and coordinator logs
│   ├── PROTOCOL.md             ← Coordinator instructions
│   ├── CONTEXT.md              ← Project background (optional)
│   └── squad.json              ← Squad metadata
├── projects/<name>/            ← Code output (default, configurable)
├── config.json                 ← Global settings
└── .archive/                   ← Archived (deleted) squads
```

## Watchdog

The watchdog runs every 5 minutes via OpenClaw cron and performs a 3-state check:

1. **tmux session alive + engine running** → healthy, do nothing
2. **tmux session alive + engine dead** → restart engine inside existing session
3. **tmux session gone** → full restart (new session + engine)

On restart, the coordinator is told to read `PROTOCOL.md` and `logs/coordinator-summary.md` to resume where it left off.

Log rotation: watchdog.log is rotated at ~5MB, keeping 1 backup.

## Task Lifecycle

```
New task arrives    → tasks/pending/task-YYYYMMDD-<name>.md
Squad accepts it    → moves to tasks/in-progress/, creates report
Working on it       → updates report continuously (every 15 min minimum)
Finished            → moves to tasks/done/, sets Status: done
```

Each task gets a report file in `reports/` with:
- Current status and progress
- Activity log with timestamps
- Commits table
- Final result summary

## Configuration

Global config is stored at `~/.openclaw/workspace/agent-squad/config.json`:

```json
{
  "projects_dir": "/Users/you/code"
}
```

Settings:
- **`projects_dir`** — Default parent directory for new squad projects. Each squad creates a subdirectory named after itself. Default: `~/.openclaw/workspace/agent-squad/projects/`.

## Engine Reference

All engines run in full-auto mode (no permission prompts) since squads operate unattended.

| Engine | Binary | Full command | Notes |
|--------|--------|-------------|-------|
| Claude Code | `claude` | `claude --dangerously-skip-permissions` | Supports `--agent-teams` for multi-agent |
| Codex | `codex` | `codex --full-auto` | Requires git repo |
| Gemini CLI | `gemini` | `gemini` | Google OAuth login (run `gemini` once to auth) |
| OpenCode | `opencode` | `opencode` | |
| Kimi | `kimi` | `kimi` | |
| Trae | `trae-agent` | `trae-agent` | ByteDance |
| Aider | `aider` | `aider --yes` | |
| Goose | `goose` | `goose` | Block (formerly Square) |

## Security Considerations

- **Full-auto mode** means the AI operates without any permission prompts. It can freely read, write, delete files, and execute commands within the project directory.
- **Keep sensitive files out**: credentials, API keys, `.env` files, and private keys should not be in project directories that squads work on.
- **`--agent-teams`** (Claude only) allows the coordinator to spawn additional AI sub-agents, increasing the scope of autonomous operations.
- Each squad runs in its own isolated tmux session.
- Coordination directory logs are gitignored by default.
