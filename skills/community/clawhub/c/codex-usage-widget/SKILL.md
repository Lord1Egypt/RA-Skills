---
name: codex-usage-widget
description: Install, update, inspect, or uninstall a local-only Übersicht desktop widget that tracks Codex token usage, recent root sessions, source labels, and context-window pressure. Use when the user asks for a Codex usage widget, desktop usage monitor, Übersicht Codex monitor, local Codex session tracker, or help maintaining this widget.
---

# Codex Usage Widget

## What This Skill Provides

Use this skill to install or maintain a lightweight macOS Übersicht widget for Codex. The widget reads only local Codex files under `~/.codex`:

- `state_5.sqlite` for thread metadata.
- `logs_2.sqlite` for local log byte totals.
- `sessions/**/*.jsonl` and `archived_sessions/*.jsonl` for token-count events, origin labels, and context-window pressure.

It does not call external APIs, does not require a model key, and does not upload data.

## Install

Run:

```bash
scripts/install.sh
```

The script copies `assets/codex-usage.widget/` to:

```text
~/Library/Application Support/Übersicht/widgets/codex-usage.widget/
```

Übersicht should refresh automatically. If it does not, use the Übersicht menu bar item to refresh all widgets.

## Update

Run `scripts/install.sh` again. The script overwrites only this widget directory and does not touch Codex settings or other Übersicht widgets.

## Uninstall

Run:

```bash
scripts/uninstall.sh
```

This removes only:

```text
~/Library/Application Support/Übersicht/widgets/codex-usage.widget/
```

## Behavior Notes

- Recent rows are grouped by root session, so spawned subagents do not appear as separate sessions.
- Source labels prefer rollout `originator`: `codex_vscode` becomes `VSCode`, `Codex Desktop` becomes `Client`, and terminal/CLI-like originators become `Terminal`.
- The right-side row metric is context-window pressure, calculated from the latest `input_tokens`. It uses a 200K window until a session exceeds that level, then uses a 1M window.
- The widget never parses message text. Recent rows are filtered only by Codex's local archived state and root-session relationships.
- The widget is intentionally best-effort because Codex local storage fields may change between Codex releases.

## Validate

After installing, run:

```bash
python3 "$HOME/Library/Application Support/Übersicht/widgets/codex-usage.widget/codex-usage.py"
```

The command should print JSON with `"ok": true`.
