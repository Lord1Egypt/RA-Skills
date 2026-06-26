---
name: blocket-watch
slug: blocket-watch
displayName: Blocket Watch
description: >-
  Poll Swedish Blocket.se via the blocket CLI on a schedule, dedupe listings by ad id,
  and send new matches to Telegram with openclaw message send — no LLM on each poll.
  Use for classified alerts, Blocket search monitoring, or systemd-based OpenClaw notifications.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - blocket
        - openclaw
    os:
      - linux
---

# Blocket Watch

OS-scheduled watcher for **Blocket.se** (Sweden). It runs `blocket` with your search `argv`, tracks seen ad IDs in `seen.json`, and notifies **only** via `openclaw message send` (Telegram by default). **No** hosted model is invoked during polling.

## When to use this skill

- You run **OpenClaw** with the **Telegram** channel configured.
- You have the **`blocket`** CLI installed (`blocket --help`).
- You want **periodic** checks (e.g. systemd user timer), not OpenClaw Gateway cron alone.

## Install (end user)

1. Install [OpenClaw](https://docs.openclaw.ai) and authenticate `openclaw` so `openclaw message send` works.
2. Install **`blocket`** (see upstream docs for your OS).
3. Copy this skill folder to a fixed path, e.g. `~/.openclaw/scripts/blocket-watch/`.
4. `cp config.example.json config.json` and edit:
   - `telegram_target`: your Telegram chat id (DM with the bot).
   - `queries`: one object per search; `argv` is passed to `blocket` after the binary name.
5. `cp seen.example.json seen.json` (or start with `{"ids":[]}`).
6. `chmod +x poll.sh onboard.sh`
7. Optional: install `systemd/blocket-watch.service` and `blocket-watch.timer` — **edit** `WorkingDirectory` and `ExecStart` in the service file to match step 3.
8. `systemctl --user enable --now blocket-watch.timer`

## Operations

| Action | Command |
|--------|---------|
| Poll (normal) | `./poll.sh` |
| Poll without Telegram / without updating seen | `BLOCKET_WATCH_DRY_RUN=1 ./poll.sh` |
| Post current config to Telegram | `./onboard.sh` |
| Preview onboard text locally | `./onboard.sh --dry-run` |

## Config shape

- **`enabled`**: set `true` when ready.
- **`telegram_target`**: recipient for `openclaw message send`.
- **`queries`**: list of `{ "label", "argv", optional "max_price", "max_price_currency" }`.
  If **`max_price`** is set, only listings **≤ max_price** in that currency are notified (default currency **SEK**).

See `README.md` for argv examples (general search, cars, boats).

## Security and etiquette

- **Do not** commit real `config.json` or `seen.json` with personal chat IDs to public repos.
- Respect Blocket’s terms of use and rate limits; this tool is for personal monitoring.
- Telegram targets and search terms are **your** data — keep them private.

## License

This skill is published under **MIT-0** (see `LICENSE`). By publishing or redistributing on ClawHub you agree to the registry’s MIT-0 terms.
