---
name: "bring"
description: "Manage Bring! shopping lists - view, add, remove items from shared grocery lists."
allowed-tools: ["exec"]
user-invocable: true
---

# Bring Shopping List Integration

## Invocation

The CLI lives at `scripts/bring-cli.js`. Always prefix with `NODE_PATH=$(npm root -g)`:

```bash
NODE_PATH=$(npm root -g) node ~/.openclaw/workspace/skills/bring/scripts/bring-cli.js <command> [args]
```

## Prerequisites

```bash
npm install -g bring-shopping
```

## Setup

```bash
NODE_PATH=$(npm root -g) node ~/.openclaw/workspace/skills/bring/scripts/bring-cli.js configure <email> <password>
```

Config stored at `~/.openclaw/bring/config.json`. Tokens cached at `~/.openclaw/bring/token.json` (7-day expiry).

## Commands

| Command | Args | Notes |
|---------|------|-------|
| `configure` | `<email> <password>` | One-time setup |
| `renew` | — | Force re-login if token expired |
| `lists` | — | All lists with UUIDs |
| `findlist` | `<name>` | Partial name match |
| `items` | `[listUuid]` | Default list if omitted |
| `add` | `<listUuid> <item> [note]` | Raw add, no catalog lookup |
| `smartadd` | `<listUuid> <item> [locale] [note]` | **Preferred**: catalog-aware, gets icons |
| `remove` | `<listUuid> <item>` | Moves to recent |
| `setdefault` | `<listUuid>` | Avoid passing UUID every time |
| `detectlang` | `<listUuid>` | Auto-detect list language |
| `setlang` | `<listUuid> <locale>` | Cache language preference |
| `getlang` | `<listUuid>` | Cached or auto-detected |

Supported locales: `en-US`, `it-IT`, `es-ES`, `de-DE`, `fr-FR`

## Workflow

### Adding items (prefer smartadd)

1. If user doesn't specify a list, use default (check `items` without UUID first).
2. Use `smartadd` with the list's locale for icon support. Fall back to `add` if catalog miss.
3. Confirm what was added.

### Viewing items

Run `items` (with listUuid or default). Present purchase items as "to buy" and recently as "recently bought".

### Removing items

Run `remove <listUuid> "<exact-item-name>"`. Item names are case-sensitive — match exactly from `items` output.

## Gotchas

- Item names are **case-sensitive** — copy exact names from `items` output.
- `remove` moves to recent, doesn't delete.
- Token cache expires after 7 days; run `renew` if commands start failing with auth errors.
- `smartadd` needs the right locale to find catalog matches.
- Lists use mixed languages (e.g. "Home in Florence" has Italian, German, English items). Detect per-list.
