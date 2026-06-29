---
name: delivery-mirror
description: Mirror cron/script deliveries into agent session transcripts so scheduled and isolated-cron messages persist in context. Session continuity, no core changes.
metadata: {"openclaw":{"emoji":"🪞","homepage":"https://github.com/obuchowski/openclaw-delivery-mirror","os":["linux","darwin"],"requires":{"bins":["bash","python3"]}}}
---

# delivery-mirror

A deterministic, **no-core-changes** helper for the gap between *delivering* a
message and the agent *remembering* it.

All commands: `bash "{baseDir}/scripts/send-mirrored.sh" <flags>`

## The problem

`--command` crons and external scripts call `openclaw message send …` directly.
The message reaches the chat — but it **bypasses the agent's run loop**, so the
agent's session JSONL never records it. Next time that agent wakes in the
chat/topic, it has no idea the message was ever sent. Classic case: calendar
agenda dispatchers and reminder scripts whose sessions run with
`delivery.mode: none` and send via CLI.

Messages delivered through OpenClaw's own delivery layer (agent replies,
isolated/cron `agentTurn` delivery) don't have this problem: that layer passes a
*mirror context* and core calls `appendAssistantMessageToSessionTranscript`,
which writes a `delivery-mirror` row. A plain `openclaw message send` from a
script passes no mirror context — and the CLI has no flag to set one — so nothing
is mirrored. This skill closes that one gap, **without touching OpenClaw core**.

## What it does

1. Sends the message exactly as before (`openclaw message send … --json`).
2. On success, resolves the owning agent's current session file from
   `agents/<agent>/sessions/sessions.json` (`.sessionFile` — follows compaction
   rotation).
3. Appends one `delivery-mirror` assistant row to that transcript — the **same
   shape** core produces via `appendAssistantMessageToSessionTranscript`
   (`provider: "openclaw"`, `model: "delivery-mirror"`, zeroed usage,
   `stopReason: "stop"`), `parentId`-chained to the last record. It also attaches
   the `openclawDeliveryMirror: {kind:"channel-final"}` marker that core adds
   optionally on real deliveries, with `sourceMessageId` when the send returns one.
4. Optional idempotency: `--idem <key>` skips the whole op if that key was
   already handled (guards against double-delivery on cron retry).

Mirroring is **best-effort**: if the session can't be resolved, delivery still
succeeded and the helper exits 0 with a warning — it never fails a send because
of a mirror problem.

## Why a skill, not a plugin

A true runtime plugin would mean changing/extending OpenClaw core. This stays a
self-contained script you drop next to your other command-cron scripts, so it
works on any OpenClaw host and upgrades independently.

## Permissions & write scope

This skill performs **local filesystem writes** and runs the `openclaw` CLI.
Exactly what it touches, and nothing else:

- **Reads:** `<openclaw-home>/agents/<agent>/sessions/sessions.json` — only to
  resolve the target session's `sessionFile`.
- **Appends (never edits or deletes):** one JSONL line to that `sessionFile` —
  the agent's own transcript.
- **Writes:** idempotency state `…/delivery-mirror/state/<agent>.seen`, a log
  `…/delivery-mirror/mirror.log`, and advisory lock files (`*.mirror.lock`,
  `<agent>.seen.lock`).
- **Executes:** `openclaw message send` to deliver the message.
- **Does NOT:** make network calls of its own, run any model, read ambient
  environment for data (all inputs come from this script's flags and are passed
  to the embedded Python as positional `argv`, not env), or modify/delete any
  existing transcript record.

`--openclaw-home` confines every path above — point it at a scratch dir to dry-run
safely. Treat the **caller** (your cron/script) as the trust source: message text
is stored verbatim. Full threat model in [SECURITY.md](SECURITY.md).

## Usage

```bash
scripts/send-mirrored.sh \
  --agent ula \                       # agent id that owns the session (sessions dir)
  --account ula \                     # channel account for send (defaults to --agent)
  --to -1003971971641 \               # telegram chat id
  --thread-id 131 \                   # telegram forum topic (omit for non-forum)
  --source agenda-dispatch \          # label for logs / tracing
  --idem "agenda:131:$(date +%F):morning" \  # optional dedupe key
  --message "$MSG"
```

Message input: `--message "…"`, `--message-file PATH`, or `--message-file -`
(stdin).

### In a `--command` cron

Replace a bare `openclaw message send …` with:

```bash
/home/opc/.openclaw/skills/delivery-mirror/scripts/send-mirrored.sh \
  --agent ula --account ula --to -1003971971641 --thread-id 131 \
  --source agenda-dispatch --message "$MSG"
```

### Flags

| flag | meaning |
|------|---------|
| `--message` / `--message-file` | message text (file or `-` for stdin) |
| `--to` | channel target (telegram chat id) — required |
| `--agent` | agent id owning the session — required |
| `--account` | channel account id for send (default: `--agent`) |
| `--channel` | channel (default `telegram`) |
| `--thread-id` | telegram forum topic id |
| `--session-key` | explicit session key (else auto-resolved) |
| `--source` | label recorded in the helper log (not in the row) |
| `--idem` | idempotency key; skip if already handled (exit 3) |
| `--openclaw-home` | OpenClaw home (default `$OPENCLAW_HOME` or `~/.openclaw`) |
| `--openclaw-bin` | openclaw binary (default `openclaw` on PATH) |
| `--dry-run` | print the plan, do nothing |
| `--no-send` | mirror only (testing) |
| `--no-mirror` | send only (= plain send) |

### Exit codes

| code | meaning |
|------|---------|
| 0 | delivered (mirrored, or mirror skipped best-effort with warning) |
| 2 | bad usage / missing required args |
| 3 | idempotency: `--idem` key already handled, nothing done |
| 4 | send failed (nothing mirrored) |

## Session resolution

The helper finds the transcript by, in order: explicit `--session-key`;
auto-constructed key (`agent:<agent>:<channel>:group:<to>:topic:<thread>`, then
`:group:<to>`, then `:direct:<to>`); finally a scan of `sessions.json` matching
`deliveryContext.to` / `route.target.to` (substring on `--to`) + thread id.
It always appends to the entry's `sessionFile`, so it follows compaction
rotation automatically.

## Caveats (read before trusting it blindly)

- **It reproduces a core row from bash.** The `delivery-mirror` row is a
  first-class core concept (written by `appendAssistantMessageToSessionTranscript`,
  matched by core's `isDeliveryMirror` predicate, which keys only on
  `provider`+`model`). The coupling is only that we **hand-append the JSONL**
  instead of calling that internal function — no CLI or tool exposes it. We
  reproduce core's `usage` shape and attach the optional
  `openclawDeliveryMirror` marker; the append is newline-safe; re-verify after a
  major OpenClaw upgrade. `--source` is recorded only in the helper's log, not in
  the row.
- **Concurrency.** Appends are serialized with `flock` on
  `<sessionFile>.mirror.lock`. The gateway may not take that lock, so avoid
  mirroring into a topic while its agent is actively mid-run; dispatcher-style
  schedules (agent idle) are the safe, intended case.
- **State.** Idempotency keys live in
  `<openclaw-home>/delivery-mirror/state/<agent>.seen`; log in
  `<openclaw-home>/delivery-mirror/mirror.log`.

## Test

```bash
scripts/send-mirrored.sh --dry-run  --agent X --to <chat> --thread-id <t> --message "hi"
scripts/send-mirrored.sh --no-send  --agent X --to <chat> --thread-id <t> --message "hi"  # mirror only
```
