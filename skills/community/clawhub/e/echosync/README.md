# openclaw-echosync-skill

An [OpenClaw](https://openclaw.ai/) skill for **echosync.io**: OAuth, Hyperliquid
copy-trade setup, market data, and trading via a local helper script.

## What's here

| File       | Role                                                          |
| ---------- | ------------------------------------------------------------- |
| `SKILL.md` | Skill spec (English); subcommands and flows are authoritative |
| `auth.mjs` | Single entrypoint: `node auth.mjs <subcommand>`               |

## Requirements

- **Node.js** (the skill metadata expects a `node` binary on the host)

## Credentials

Tokens are stored under `~/.echosync/credentials.json`. Full behavior and command
reference: `SKILL.md`.
