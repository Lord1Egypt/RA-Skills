---
name: agent-mailbox
description: "Lightweight cross-agent mailbox using per-workspace file inboxes with best-effort fanout and local read/archive flow. Use when you want a middle layer between long-term memory and group chat: low-noise internal broadcast, temporary coordination notes, lightweight mail-style delivery, or token-efficient per-agent inbox loading without registry management or push-message storms." 
---

# Agent Mailbox

Use this skill for a **very lightweight internal mail system** between OpenClaw agent workspaces.

## Design goals

- No central registry
- No guaranteed delivery
- No push notifications
- No group-message storms
- Best-effort fanout only
- Per-workspace local inboxes
- Token-efficient reads: each agent reads only its own inbox
- Advisory context only, not an execution bus
- Local filesystem only, not cloud sync or webhook delivery

This is a middle layer between long-term memory and chat messaging.

## Safety boundary

This skill is intentionally narrow.

It is for **local mailbox-style context sharing only**.

It does **not** implement:

- automatic task execution
- autonomous task dispatch
- webhook callbacks
- remote sync
- cloud delivery
- receipt tracking
- retry queues

Mailbox items should be treated as advisory hints for local agent judgment, not commands that must be executed.

## Mailbox location

Each workspace owns its own local mailbox under:

`<workspace>/.agent-mailbox/`

Subdirectories:

- `inbox/` — unread or pending mail files
- `archive/` — consumed mail files

Examples:

- `/path/to/workspace/.agent-mailbox/inbox/`
- `/path/to/another-workspace/.agent-mailbox/inbox/`

## Fanout model

Sender scripts scan candidate workspaces using a configurable glob pattern.

Default pattern:

`$HOME/.openclaw/workspace*`

Override with `MAILBOX_GLOB` when your workspaces live elsewhere.

If a workspace contains `.agent-mailbox/inbox/`, write a mail file there.

If the path does not exist or write fails, skip it.

Do not maintain a registry. Do not retry failed deliveries. Do not block on partial failure.

## File model

One mail = one file.

Filename format:

`<stamp>--<sender>--<priority>--<slug>.md`

Example:

`20260322100000--main--warn--cron-list-broken.md`

Fields:

- `stamp` — `YYYYMMDDHHMMSS`
- `sender` — short sender id
- `priority` — `info`, `warn`, or `critical`
- `slug` — short readable identifier

## Mail content

Use a short header followed by a blank line and body.

Example:

```text
Title: cron list 异常
From: main
Created-At: 2026-03-22T10:00:00+08:00
Priority: warn
Tags: cron,ops

`openclaw cron list` 当前报错，先不要依赖其输出。
建议改用：
- openclaw cron status
- openclaw cron runs
```

## Baseline integration

For best results, integrate mailbox checking into the agent's baseline startup or task-entry workflow.

Recommended baseline rule:

- If `.agent-mailbox/inbox/` exists in the current workspace, check only the newest **1-3** mail files before normal task work
- Read only enough to determine relevance
- Compress relevant mail into a very short working summary
- Archive processed mail immediately so inbox stays small
- Do not rebroadcast, auto-reply, or auto-write all mail into long-term memory

This makes the mailbox reliable in practice while keeping token cost low.

## Read flow

When loading this skill in a workspace:

1. Ensure the local mailbox exists
2. List files in local `inbox/`
3. Read only the newest few files you need
4. Summarize them briefly into context
5. Decide whether to ignore, use for this session, or adopt into memory
6. Archive or delete consumed mail so it is not repeatedly re-read

Prefer reading only 1–5 newest mails.

## Receiver handling policy

Treat mailbox items as **single-consumption lightweight context hints**.

Default handling:

1. Read the newest relevant mail
2. Compress it into a very short summary for the current task
3. Decide whether it matters only for this turn or should affect longer-lived memory
4. Archive it after processing so it leaves the inbox

Recommended decision model:

- `critical` — read first; usually affect current behavior immediately
- `warn` — read and adopt when relevant to current work
- `info` — skim quickly; keep only if useful

Possible outcomes after reading:

- **Ignore** — not relevant; archive it
- **Session-use only** — use it for the current turn/session; archive it
- **Adopt to memory** — if it represents a durable fact, explicitly write the distilled version into the proper memory file; then archive it
- **Act now** — if it changes current execution, apply it and archive it

Do **not** automatically:

- rebroadcast mail
- reply to the sender through chat
- write all mail into long-term memory
- keep already-processed mail in `inbox/`

Inbox should contain only unprocessed mail. Archive should contain processed mail.

## Archive policy

Default: archive after reading, do not keep re-reading inbox mail.

Archive path:

`<workspace>/.agent-mailbox/archive/`

This keeps the inbox small and token cost low.

## Good uses

- low-noise cross-agent operational note
- temporary warning for other workspaces
- lightweight fanout without chat delivery
- “FYI only” advisory
- coordination hint that does not belong in long-term memory yet
- local best-effort sharing of small, non-urgent context

## Avoid

- secrets unless truly necessary
- large documents
- durable memory that belongs in MEMORY.md or memory/YYYY-MM-DD.md
- real-time urgent alerts that should use actual messaging
- any design that assumes guaranteed delivery
- any design that expects mailbox files to trigger automatic execution
- any claim of cloud sync, webhook transport, or remote callback support

## Recommended AGENTS.md snippet

You can paste this into a workspace's `AGENTS.md`:

```markdown
### 📬 Lightweight Mailbox Check

If this workspace has `.agent-mailbox/inbox/`, do a **very light mailbox check** before starting normal task work:

1. Look at only the newest **1-3** mail files
2. Read only what is needed to identify relevance
3. Compress relevant mail into a very short working summary
4. Archive processed mail so inbox stays small
5. Do **not** rebroadcast, auto-reply, or dump all mail into long-term memory

Think of mailbox items as lightweight internal coordination hints, not chat messages and not permanent memory.
```

## Minimal receive command pattern

Use this minimal pattern when an agent wants to consume mailbox items manually from shell.

This pattern is intentionally local and conservative: inspect, summarize, archive.
It should not be extended into automatic execution of mailbox contents.

```bash
MAIL=$(./skills/agent-mailbox/scripts/list-mailbox.sh . 1 | head -n 1)
if [ -n "$MAIL" ]; then
  sed -n '1,40p' "$MAIL"
  ./skills/agent-mailbox/scripts/archive-mailbox.sh "$MAIL" >/dev/null
fi
```

Use this behavior convention:

- check only the newest mail first
- read only enough to judge relevance
- archive immediately after processing
- keep inbox small

If you need a slightly broader pass, read up to 3 mails:

```bash
./skills/agent-mailbox/scripts/list-mailbox.sh . 3
```

## Scripts

Use bundled scripts when possible:

- `scripts/init-mailbox.sh` — initialize a mailbox in a workspace
- `scripts/send-mailbox.sh` — fan out mail to mailbox-enabled workspaces
- `scripts/list-mailbox.sh` — list local inbox mail
- `scripts/archive-mailbox.sh` — archive a consumed mail file
- `scripts/cleanup-mailbox.sh` — prune old archive files

Read the script directly if you need to inspect or change behavior.
