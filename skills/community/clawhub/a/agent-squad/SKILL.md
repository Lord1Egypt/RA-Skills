---
name: agent-squad
version: 0.9.4
license: MIT-0
description: "Manage persistent AI coding squads that run in tmux sessions with task queues, progress reports, and automatic health monitoring. Use when the user wants to: (1) start/launch/create/restart a squad or team of AI agents, (2) assign/give tasks to a squad, (3) check squad status or ask what a squad is doing, (4) ping/nudge a squad to report progress, (5) stop a squad, (6) list all active squads, (7) configure squad settings like default project directory, (8) delete/archive a squad. Supports Claude Code, Codex, Gemini CLI, OpenCode, Kimi, Trae, Aider, and Goose as AI engines."
metadata:
  { "openclaw": { "requires": { "anyBins": ["tmux"], "bins": ["python3"] } } }
---

# Agent Squad

GitHub: https://github.com/0xTimi/agent-squad

Run persistent AI coding squads in tmux. Squads pick up tasks, write code, and report progress — 24/7 in the background.

## Slash Command Usage

Users can invoke `/agent-squad` directly with optional arguments:

| Command | Action |
|---|---|
| `/agent-squad` | Show squad dashboard (or Getting Started if none exist) |
| `/agent-squad list` | List all squads |
| `/agent-squad start my-squad claude` | Start a squad |
| `/agent-squad status my-squad` | Check squad status |
| `/agent-squad stop my-squad` | Stop a squad |
| `/agent-squad assign my-squad "add login page"` | Assign a task |
| `/agent-squad ping my-squad` | Nudge squad to report |
| `/agent-squad delete my-squad` | Archive a squad |
| `/agent-squad peek my-squad` | Peek at squad's live tmux screen |
| `/agent-squad restart my-squad` | Restart a stopped squad |

No arguments or `list` → run `bash {baseDir}/scripts/squad-list.sh`:
- **If squads exist**: show a clean status dashboard
- **If no squads**: show the Getting Started intro below

## Getting Started

When users ask "what is this", "how do I use this", or invoke `/agent-squad` with no squads, give a friendly intro with usage examples. Match the user's language.

> Agent Squad runs AI coding agents in the background 24/7. Just tell me what you need:
>
> - "Start a squad called my-squad using claude for ~/projects/my-app"
> - "Give my-squad a task: implement user login"
> - "How's my-squad doing?"
> - "Stop my-squad"
> - "What squads do I have?"
>
> Engines: Claude Code, Codex, Gemini CLI, OpenCode, Kimi, Trae, Aider, Goose
>
> Want to start one now?

If the user asks which engine to use or doesn't specify one: **default to `claude`** — it is the most thoroughly tested engine and works best with Agent Squad. Mention other engines only if the user specifically asks. See `{baseDir}/references/engines.md` for details.

## What Users Can Do

Users interact through natural language. Here's what they might say and how to respond:

### Start a squad

User: "start a squad called my-squad with claude" / "launch a codex squad for ~/projects/api"

Ask if missing: squad name. Default engine to `claude` if not specified. Project dir and context are optional.

First-time users: briefly mention squads run in full-auto mode — the AI has full access to the project directory.

Response: "Squad 'my-squad' is up and running with Claude Code! You can assign tasks anytime."

### Assign a task

User: "give my-squad a task: build the login page" / "let my-squad work on JWT auth"

If only one squad exists, use it automatically. If the request is vague, ask for specifics.

Response: "Task assigned! my-squad will start working on 'Login Page' shortly."

### Check status

User: "how's my-squad doing?" / "what's the status?" / "is my-squad done yet?"

Include the live tmux screen output (from squad-status.sh) in the response — this lets the user see what the agent is actually doing right now.

Response: "my-squad is running on Claude Code, working on 'Login Page' — about 60% done. 2 tasks completed, 1 in progress.

Live screen:
```
Working on form validation...
Created src/components/LoginForm.tsx
Running tests...
```"

### Peek at screen

User: "peek at my-squad" / "what's on my-squad's screen?" / "show me what my-squad is doing"

Show the raw tmux screen content. This is a quick way to see the agent's live terminal without checking reports.

Response: Show the screen output directly, formatted in a code block.

### Ping for update

User: "ping my-squad" / "nudge it to report"

Response: "I've nudged my-squad to update its progress report. Check back in a minute."

### Stop a squad

User: "stop my-squad" / "pause the squad"

Always confirm before stopping.

Response: "my-squad stopped. All work is saved — you can restart anytime."

### Restart a squad

User: "restart my-squad" / "bring my-squad back up"

Response: "my-squad is back up and running! It will pick up where it left off."

### List squads

User: "what squads do I have?" / "list my squads" / "show all squads"

Present a clean readable summary of all squads with name, engine, status, and task counts.

### Delete a squad

User: "delete my-squad" / "archive the old squad" / "clean up my-squad"

Always ask for confirmation first. Reassure: data is archived, project code is never touched.

### Configure

User: "set default project dir to ~/code" / "show squad settings"

### What commands are available?

User: "agent-squad都有哪些命令" / "what can you do?" / "help"

**IMPORTANT**: Never show internal script names (squad-start.sh, etc.) to users. Instead, show the `/agent-squad` slash commands and natural language examples:

> Here's what you can do with Agent Squad:
>
> | Command | Or just say... |
> |---|---|
> | `/agent-squad start my-squad claude` | "Start a squad called my-squad" |
> | `/agent-squad assign my-squad "task"` | "Give my-squad a task: ..." |
> | `/agent-squad status my-squad` | "How's my-squad doing?" |
> | `/agent-squad peek my-squad` | "Peek at my-squad's screen" |
> | `/agent-squad ping my-squad` | "Ping my-squad" |
> | `/agent-squad stop my-squad` | "Stop my-squad" |
> | `/agent-squad restart my-squad` | "Restart my-squad" |
> | `/agent-squad list` | "What squads do I have?" |
> | `/agent-squad delete my-squad` | "Delete my-squad" |

---

## Script Reference

All scripts at `{baseDir}/scripts/`. Execute based on user intent above and present results conversationally.

### squad-start.sh

```bash
bash {baseDir}/scripts/squad-start.sh "<name>" "<engine>" "<context>" [--project <dir>] [--restart] [--agent-teams] [--no-watchdog]
```

- name: lowercase alphanumeric + hyphens
- engine: claude, codex, gemini, opencode, kimi, trae, aider, goose
- context: optional project background
- `--project <dir>`: custom code output directory
- `--restart`: required if squad name already exists (also used for restart intent)
- `--agent-teams`: claude only, multi-agent mode
- `--no-watchdog`: skip auto-restart cron

### squad-assign.sh

```bash
bash {baseDir}/scripts/squad-assign.sh "<name>" "<title>" "<objective>" "<priority>"
```

Priority: critical / high / normal (default) / low

### squad-status.sh

```bash
bash {baseDir}/scripts/squad-status.sh "<name>"
```

Also read latest report in `~/.openclaw/workspace/agent-squad/squads/<name>/reports/` — check `## Current` section for real-time progress.

### squad-peek.sh

```bash
bash {baseDir}/scripts/squad-peek.sh "<name>" [lines]
```

Default: 20 lines. Shows the live tmux screen content of a running squad.

### squad-ping.sh

```bash
bash {baseDir}/scripts/squad-ping.sh "<name>"
```

### squad-stop.sh

```bash
bash {baseDir}/scripts/squad-stop.sh "<name>"
```

### squad-list.sh

```bash
bash {baseDir}/scripts/squad-list.sh
```

### squad-delete.sh

```bash
bash {baseDir}/scripts/squad-delete.sh "<name>"          # show summary
bash {baseDir}/scripts/squad-delete.sh "<name>" --confirm # confirm archive
```

### squad-config.sh

```bash
bash {baseDir}/scripts/squad-config.sh show
bash {baseDir}/scripts/squad-config.sh set projects_dir "<path>"
```

## Guidelines

- **Never show internal script names** (squad-start.sh, etc.) to users — always use `/agent-squad` slash commands or natural language examples
- If only one squad exists, use it automatically — don't ask "which squad?"
- One engine per squad — suggest multiple squads for multiple engines
- Don't modify task/report files directly — only via assign script
- If squad is stopped and user assigns a task, write it anyway — picked up on restart
- Squads auto-init git repos; for existing projects suggest a separate branch
- Watchdog auto-restarts crashed squads every 5 min by default
- For restart: stop the squad first (`squad-stop.sh`), then start with `--restart` flag

## Engine Reference

Details: `{baseDir}/references/engines.md`
