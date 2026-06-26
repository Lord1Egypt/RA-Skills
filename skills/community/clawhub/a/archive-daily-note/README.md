# archive-daily-note

[![ClawHub](https://img.shields.io/badge/ClawHub-archive--daily--note-blue)](https://clawhub.ai/madebydia/archive-daily-note)

An [OpenClaw](https://openclaw.app) skill that moves yesterday's Obsidian daily note into a `past-days/` archive folder using the Obsidian CLI.

## What It Does

Designed for nightly cron execution, this skill:

- Finds yesterday's daily note (named `MM-DD-YYYY DayOfWeek.md`) at the vault root
- Moves it into `past-days/` using `obsidian move`
- **Keeps all wiki-links updated** — the Obsidian move command rewrites internal references so nothing breaks

## Why `obsidian move`?

A simple `mv` would break every `[[link]]` pointing to the note. The Obsidian CLI's move command updates all backlinks across the vault automatically.

## Cron Setup

Schedule as an isolated cron job shortly after midnight:

```
Schedule: 5 0 * * *  (daily at 00:05)
Target: isolated
```

## Behavior

- **Idempotent** — safe to run multiple times; skips if already archived or missing
- **Link-safe** — uses Obsidian's move command to update all internal links
- **Silent** — no output on skip; only reports errors

## Requirements

- [OpenClaw](https://openclaw.app) with cron support
- Obsidian CLI (`obsidian` binary)
- Daily notes in `MM-DD-YYYY DayOfWeek.md` format
- A `past-days/` folder in your vault

## License

MIT
