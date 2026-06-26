# daily-memory-save

[![ClawHub](https://img.shields.io/badge/ClawHub-daily--memory--save-blue)](https://clawhub.ai/madebydia/daily-memory-save)

An OpenClaw skill that gives AI agents persistent memory across sessions. Periodically reviews conversation history and writes memory files using a dual-layer system.

## How It Works

Runs as a recurring system event in the main session. Reviews recent conversations and captures what matters into two layers:

### Daily Notes (`memory/YYYY-MM-DD.md`)
Raw daily logs — decisions made, preferences expressed, project updates, lessons learned, notable interactions.

### Long-Term Memory (`MEMORY.md`)
Curated, distilled insights that persist beyond daily context. Updated only when something is significant enough to remember long-term.

## Cron Setup

Schedule as a main-session system event during waking hours:

```
Schedule: 0 9,11,13,15,17,19,21,23 * * *
Target: main (system event)
```

The skill runs silently by default — no user notifications. See `SKILL.md` for notification mode opt-in.

## Key Design Decisions

- **Main session target** — runs as a system event so it has access to conversation history
- **Silent by default** — configurable notification mode available
- **Selective capture** — signal over noise; skips quiet periods entirely
- **Dual-layer memory** — daily notes for raw context, MEMORY.md for distilled wisdom

## ⚠️ Privacy Notice

- Reads your conversation history to extract memories
- Writes summaries to local files only — **no network access**
- No credentials used or stored
- Review saved memory files periodically; delete anything you don't want persisted

## Requirements

- OpenClaw with cron support
- Main session system event capability
- Writable `memory/` directory in workspace

## License

MIT
