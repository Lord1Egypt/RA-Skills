---
name: agent-control
description: Manage OpenClaw isolated agents from chat with short commands. Use when the user asks to create/list/switch/bind/delete agents, route channels to a specific agent, or set an agent identity without manually typing full CLI syntax.
---

# Agent Control

Translate short chat commands into OpenClaw CLI agent operations.

## Command grammar

Accept these commands (case-insensitive, trim extra spaces):

- `agent list`
- `agent create <name> [workspace=<path>] [model=<id>]`
- `agent switch <name> [channel=<channel[:accountId]>]`
- `agent bind <name> <channel[:accountId]>`
- `agent unbind <name> <channel[:accountId]>`
- `agent delete <name>`
- `agent identity <name> [display="..."] [emoji=🗡️] [avatar=<path>]`

If input is ambiguous, ask one focused question.

## Execution mapping

Run these exact command patterns:

- List:
  - `openclaw agents list`
- Create:
  - `openclaw agents add <name> --workspace <path> --model <id>`
  - Omit optional flags when missing.
  - Default workspace when omitted: `~/clawd/agents/<name>`.
- Switch (route this channel/account to an agent):
  - `openclaw agents bind --agent <name> --bind <channel[:accountId]>`
  - If channel is omitted, infer from current surface when possible (e.g. `webchat`).
- Bind / unbind:
  - `openclaw agents bind --agent <name> --bind <binding>`
  - `openclaw agents unbind --agent <name> --bind <binding>`
- Delete:
  - Require explicit confirmation in the same turn for destructive action.
  - Then run: `openclaw agents delete <name>`
- Identity:
  - `openclaw agents set-identity --agent <name> [--name <display>] [--emoji <emoji>] [--avatar <path>]`

## Response style

After each operation, return:
1. A one-line result (success/failure)
2. The next useful command for the user

Keep it brief and practical.

## Safety rules

- Treat `agent delete` as destructive: confirm before running.
- Never run unrelated shell commands.
- If a command fails, show the error and one concrete fix.

## scripts/

Use `scripts/example.py` as a deterministic helper wrapper for command parsing/execution when needed.