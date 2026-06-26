---
name: codex-history-manager
description: Search, read, export, hand off, clone, move, or rebind local Codex history stored under ~/.codex. Use when the user wants to inspect past Codex sessions, bring a thread into another workspace, export transcripts, generate handoff notes, or change a thread's workspace/provider metadata.
---

# Codex History Manager

Use `codex-history-manager` when the task is about local Codex history, not general ChatGPT or web chat history.

Codex stores local history in two places:

- `~/.codex/state_5.sqlite` for thread metadata
- `~/.codex/sessions/.../rollout-*.jsonl` and `~/.codex/archived_sessions/...` for event logs

The bundled CLI is the source of truth for reading and mutating that state:

- `./codex-history-manager ...`

## Default workflow

1. For discovery, start with `search`.
2. For context, use `show-thread` or `handoff`.
3. For exports, use `export-thread`.
4. For cross-workspace reuse, prefer `clone-thread` over `move-thread`.
5. For writes, run a dry run first, then rerun with `--apply`.
6. For history body rewrites, always do `plan-dangerous-edit`, show the warning and change list to the user, get explicit approval in chat, then run `apply-dangerous-edit`.

## Core commands

- Search threads:
  `./codex-history-manager search --query "payments"`
- Read one thread:
  `./codex-history-manager show-thread --id <thread-id>`
- Export transcript:
  `./codex-history-manager export-thread --id <thread-id> --format markdown --output /tmp/thread.md`
- Create a handoff note:
  `./codex-history-manager handoff --id <thread-id> --output /tmp/handoff.md`
- Plan a dangerous history content rewrite:
  `./codex-history-manager plan-dangerous-edit --id <thread-id> --find "old" --replace "new" --output /tmp/edit-plan.json`
- Clone a thread into another workspace:
  `./codex-history-manager clone-thread --id <thread-id> --to-cwd /abs/path --dry-run`
- Move all threads in one workspace:
  `./codex-history-manager move-workspace --cwd /abs/src --to-cwd /abs/dst --dry-run`
- Clone all threads in one workspace:
  `./codex-history-manager clone-workspace --cwd /abs/src --to-cwd /abs/dst --dry-run`
- Move a thread to another workspace:
  `./codex-history-manager move-thread --id <thread-id> --to-cwd /abs/path --dry-run`
- Rebind provider metadata:
  `./codex-history-manager change-provider --id <thread-id> --provider openai1 --dry-run`
- Rebind provider metadata for one workspace:
  `./codex-history-manager change-provider-workspace --cwd /abs/path --provider openai1 --dry-run`
- Rebind provider metadata for all local threads:
  `./codex-history-manager change-provider-all --provider openai1 --dry-run`

## Safety rules

- Never perform a write first. Use the default dry run or pass `--dry-run`.
- Only use `--apply` after reviewing the plan.
- Prefer cloning over moving unless the user explicitly wants to change ownership.
- Do not hand edit `state_5.sqlite` or rollout files if the CLI can do the job.
- If the user asks to modify message content, stop and confirm. You must first produce a dangerous edit plan, present the warning and change list in the conversation, and wait for explicit user approval before running `apply-dangerous-edit`.

Read these references only when needed:

- Command details: [references/commands.md](references/commands.md)
- Write safety and backups: [references/safety.md](references/safety.md)
- Storage model: [references/storage.md](references/storage.md)
