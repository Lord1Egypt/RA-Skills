# references/openclaw-workspace.md

This reference describes the **OpenClaw agent workspace**: what files exist, what gets loaded, and how heartbeat should be used.

## Workspace: what it is
- The workspace is the agent’s home directory and the default working directory for file tools.
- Treat it as private memory and a working repo. Do **not** commit secrets.

## Bootstrap files (loaded into context)

A typical injection order is:

1. `AGENTS.md`
2. `SOUL.md`
3. `TOOLS.md`
4. `IDENTITY.md`
5. `USER.md`
6. `HEARTBEAT.md`
7. `BOOTSTRAP.md`
8. `MEMORY.md` (optional; sometimes `memory.md`)

Notes:
- Sub-agents may receive only `AGENTS.md` and `TOOLS.md` by default. Put cross-cutting safety rules there.

## Heartbeat
- Keep heartbeat cheap and small.
- Prefer “operator dashboard check” energy:
  - If nothing important changed → respond exactly `HEARTBEAT_OK`
  - If something needs attention → send a short alert + next action options

## Security
- Never store credentials, API keys, tokens, or private keys in workspace files.
- Prefer safe operations:
  - preview diffs
  - backups
  - `trash` over `rm`
  - ask before destructive or irreversible changes
