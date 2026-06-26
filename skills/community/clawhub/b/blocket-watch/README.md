# Blocket Watch

Standalone **Blocket.se** watcher for [OpenClaw](https://openclaw.ai): periodic `blocket` CLI runs, JSON dedupe by listing id, Telegram notifications via `openclaw message send` — **no LLM** per poll.

## Requirements

- **Linux** (systemd user timer examples included).
- **`openclaw`** on `PATH` (message send to Telegram).
- **`blocket`** on `PATH` — [blocket CLI](https://github.com/blocket-se/blocket) or your install source.
- **`python3`** (stdlib only; no pip deps).

## Quick setup

```bash
mkdir -p ~/.openclaw/scripts
cp -r blocket-watch ~/.openclaw/scripts/
cd ~/.openclaw/scripts/blocket-watch
cp config.example.json config.json
cp seen.example.json seen.json
chmod +x poll.sh onboard.sh
# Edit config.json: telegram_target, queries, enabled
```

Validate:

```bash
BLOCKET_WATCH_DRY_RUN=1 ./poll.sh
```

## Optional per-query price cap

Add **`max_price`** (number) and optionally **`max_price_currency`** (default `"SEK"`) on any query. Only listings **at or below** that price in the given currency are notified. Others are still marked **seen** so they are not retried every poll.

```json
{
  "label": "Lego 10255",
  "argv": ["search", "lego 10255", "-n", "20", "-o", "json"],
  "max_price": 1600,
  "max_price_currency": "SEK"
}
```

Use **`1599`** for “strictly under 1600” if you need exclusion of exactly 1600.

## Example `argv` arrays

General:

```json
["search", "soffa", "-l", "stockholm", "--price-max", "3000", "-n", "25", "-o", "json"]
```

Cars:

```json
["cars", "volvo xc60", "--year-min", "2018", "-n", "15", "-o", "json"]
```

Boats:

```json
["boats", "segelbat", "--sort", "price-asc", "-n", "10", "-o", "json"]
```

Run `blocket --help` for your CLI version.

## systemd

Copy `systemd/blocket-watch.service` and `systemd/blocket-watch.timer` into `~/.config/systemd/user/`. **Edit** the `.service` file so `WorkingDirectory` and `ExecStart` point to your install path (defaults assume `~/.openclaw/scripts/blocket-watch`).

```bash
systemctl --user daemon-reload
systemctl --user enable --now blocket-watch.timer
```

## Files

| File | Purpose |
|------|---------|
| `poll.py` / `poll.sh` | Scheduled poll |
| `onboard.py` / `onboard.sh` | Push current config summary to Telegram (optional) |
| `config.json` | **You** create from `config.example.json` |
| `seen.json` | Persisted ad IDs (from `seen.example.json`) |

## Publishing on ClawHub

Bundle this folder (zip or git). Validation checklist:

- **Slug**: `blocket-watch` (folder name).
- **Display name**: Blocket Watch (in `SKILL.md` frontmatter).
- **SKILL.md**: required.
- **License**: MIT-0 — accept registry terms when publishing; include root `LICENSE`.
- **At least one file** besides `SKILL.md`: satisfied (`poll.py`, `README.md`, etc.).

## License

MIT-0 — see `LICENSE`.
