# agent-squad

**Your AI coding squad works 24/7 — non-stop coding in the background, ready for your review anytime.**

An [OpenClaw](https://openclaw.ai) skill that runs persistent AI coding agents in [tmux](https://github.com/tmux/tmux) sessions. Assign tasks, they code around the clock. Check in whenever you want. If they crash, they auto-restart.

Built on tmux instead of ACP — because you can't monitor, peek at, or auto-restart what you can't see. OpenClaw's built-in ACP agents work well for short tasks, but 24/7 coding needs agents that stay alive, accept new orders anytime, and survive crashes.

## Highlights

- **24/7 non-stop** — Your squad keeps coding while you sleep
- **Peek & command** — See the agent's live screen without interrupting it, or send instructions anytime
- **8 AI engines** — Claude Code, Codex, Gemini, OpenCode, Kimi, Trae, Aider, Goose
- **Crash-proof** — Watchdog auto-restarts agents if they go down
- **Task queue** — Drop tasks in, the squad works through them
- **Token tracking** — Monitor token usage per task across all engines
- **Natural language** — Manage squads through conversation via OpenClaw

## Install

```bash
# Inside OpenClaw
/skill install agent-squad

# Or via CLI
npx clawhub@latest install agent-squad
```

**Requirements:** tmux, python3, and at least one AI engine CLI.

## Quick Start

```
You:      "Start a squad called backend using claude for ~/projects/my-api"
OpenClaw:  Squad "backend" started (claude). Watchdog active.

You:      "Give backend a task: add JWT authentication"
OpenClaw:  Task assigned and squad notified.

You:      "What is backend doing?"
OpenClaw:  backend is running. Working on JWT auth — implementing token
           refresh. ~60% complete.

You:      "Stop backend"
OpenClaw:  Stopped. All data preserved. Restart anytime.
```

## Supported Engines

| Engine | CLI | Auto-mode |
|--------|-----|-----------|
| Claude Code | `claude` | `--dangerously-skip-permissions` |
| Codex | `codex` | `--full-auto` |
| Gemini CLI | `gemini` | built-in |
| OpenCode | `opencode` | built-in |
| Kimi | `kimi` | built-in |
| Trae | `trae-agent` | built-in |
| Aider | `aider` | `--yes` |
| Goose | `goose` | built-in |

## Security

Squads run in **full-auto mode** — the AI can read, write, and execute anything in the project directory without asking. Only run squads on projects you trust. Keep credentials and `.env` files out of squad project directories.

## Documentation

See [docs/guide.md](docs/guide.md) for full details on operations, directory structure, configuration, and architecture.

## License

MIT
