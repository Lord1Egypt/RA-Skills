# Codex Usage Widget

A local-only Übersicht desktop widget for tracking Codex usage, recent root sessions, and context-window pressure.

The widget reads local Codex state from `~/.codex` and renders a small macOS desktop card through [Übersicht](https://tracesof.net/uebersicht/). It does not use network requests, API keys, or external services.

The widget reads token-count events and thread metadata only. It does not parse message text, prompts, or responses.

## What It Shows

- Today's token usage and all-time token usage, with automatic K/M/B units.
- Today's touched root sessions and sessions active in the last 10 minutes.
- Recent root sessions grouped with their subagents.
- Source labels based on Codex origin: `VSCode`, `Client`, or `Terminal`.
- Context-window pressure as a percentage, based on latest `input_tokens`.
- A 7-day local usage bar chart.

## Install

1. Install and open Übersicht.
2. From the installed skill folder, run:

```bash
scripts/install.sh
```

If the widget does not appear immediately, refresh all widgets from the Übersicht menu bar icon.

## Validate

```bash
python3 "$HOME/Library/Application Support/Übersicht/widgets/codex-usage.widget/codex-usage.py"
```

Expected output is JSON with `"ok": true`.

## Uninstall

```bash
scripts/uninstall.sh
```

## Privacy

This widget reads only local files:

- `~/.codex/state_5.sqlite`
- `~/.codex/logs_2.sqlite`
- `~/.codex/sessions/**/*.jsonl`
- `~/.codex/archived_sessions/*.jsonl`

It does not upload data. It does not read credentials. It does not modify Codex settings.

## Compatibility

This is an unofficial local widget. It depends on Codex local storage fields and may need updates if Codex changes its on-disk schema.

## License

MIT-0, as required for ClawHub distributions.
