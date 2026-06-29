---
name: cron-to-transcript
description: "Isolated crons, scripts, reminders, and status checkers sent it but the agent forgot? Write deliveries into the session transcript."
metadata: {"openclaw":{"emoji":"⏱️","homepage":"https://github.com/obuchowski/openclaw-cron-to-transcript","os":["linux","darwin"],"requires":{"bins":["bash","python3"]}}}
---

# Cron To Session Transcript

Command crons and scripts can send messages that users see, while the owning
agent never records them. Cron To Session Transcript closes that gap.

Use it when a deterministic `--command` cron, dispatcher, reminder script, or
status checker calls `openclaw message send` and the agent should remember that
delivery in its own session history.

All commands:

```bash
bash "{baseDir}/scripts/send-to-transcript.sh" <flags>
```

## The Problem

`openclaw message send` reaches the chat, but it bypasses the agent run loop.
That means no assistant row is appended to the agent's session transcript. On a
later turn, the agent has no durable record that the cron/script sent anything.

Agent replies and `agentTurn` crons already go through OpenClaw's delivery layer
and are recorded normally. This skill is only for direct command/script sends.

## What It Does

1. Sends the message exactly as before with `openclaw message send ... --json`.
2. Resolves the owning agent's current `sessionFile` from
   `agents/<agent>/sessions/sessions.json`.
3. Appends one transcript-only assistant row containing the delivered text,
   chained to the previous row with `parentId`.
4. Optionally skips duplicate retries with `--idem <key>`.

The row intentionally uses OpenClaw's internal delivery marker:
`provider: "openclaw"`, `model: "delivery-mirror"`, zeroed usage, and
`openclawDeliveryMirror: {kind:"channel-final"}`. Keep that internal model string
unchanged: OpenClaw core recognizes transcript-only delivery rows by it.

Appending is best-effort. If the send succeeds but the transcript cannot be
resolved, the helper exits 0 with a warning so the real user-facing delivery is
not failed by a memory append problem.

## Permissions & Write Scope

This skill performs local filesystem writes and runs the `openclaw` CLI:

- Reads `<openclaw-home>/agents/<agent>/sessions/sessions.json`.
- Appends one JSONL row to the matched session transcript.
- Writes idempotency state and logs under `<openclaw-home>/cron-to-transcript/`.
- Uses an advisory `<sessionFile>.transcript.lock` while appending.
- Executes `openclaw message send`.

It does not run any model, make network calls of its own, edit existing
transcript records, delete data, or read ambient environment variables for
message data. Inputs are passed to the embedded Python as positional `argv`.

Use `--openclaw-home` to confine paths for tests.

## Usage

```bash
scripts/send-to-transcript.sh \
  --agent ula \
  --account ula \
  --to -1003971971641 \
  --thread-id 131 \
  --source agenda-dispatch \
  --idem "agenda:131:$(date +%F):morning" \
  --message "$MSG"
```

Message input can be `--message "..."`, `--message-file PATH`, or
`--message-file -` for stdin.

### In a Command Cron

Replace a bare send:

```bash
openclaw message send --channel telegram -t "$CHAT" --thread-id "$TOPIC" -m "$MSG"
```

with:

```bash
bash ~/.openclaw/skills/cron-to-transcript/scripts/send-to-transcript.sh \
  --agent ula --account ula \
  --to "$CHAT" --thread-id "$TOPIC" \
  --source agenda-dispatch \
  --message "$MSG"
```

### Flags

| flag | meaning |
|------|---------|
| `--message` / `--message-file` | message text (file or `-` for stdin) |
| `--to` | channel target, for example Telegram chat id |
| `--agent` | agent id that owns the transcript |
| `--account` | channel account id for send (default: `--agent`) |
| `--channel` | channel (default `telegram`) |
| `--thread-id` | Telegram forum topic id |
| `--session-key` | explicit session key (else auto-resolved) |
| `--source` | label recorded in helper logs |
| `--idem` | idempotency key; skip if already handled |
| `--openclaw-home` | OpenClaw home (default `$OPENCLAW_HOME` or `~/.openclaw`) |
| `--openclaw-bin` | openclaw binary (default `openclaw` on PATH) |
| `--dry-run` | print the plan, do nothing |
| `--no-send` | append only (testing) |
| `--no-transcript` | send only |

Compatibility alias: `--no-mirror` is accepted and behaves like
`--no-transcript`.

### Exit Codes

| code | meaning |
|------|---------|
| 0 | delivered; transcript append succeeded or was skipped best-effort |
| 2 | bad usage / missing required args |
| 3 | idempotency key already handled |
| 4 | send failed; nothing appended |

## Session Resolution

The helper finds the transcript by explicit `--session-key`, then by
auto-constructed keys:

- `agent:<agent>:<channel>:group:<to>:topic:<thread>`
- `agent:<agent>:<channel>:group:<to>`
- `agent:<agent>:<channel>:direct:<to>`

If no key matches, it scans `sessions.json` for a matching delivery target and
thread id. It appends to the entry's `sessionFile`, so compaction rotation is
followed automatically.

## Caveats

- The transcript row is reproduced from bash because no CLI exposes core's
  internal append function. Re-verify after major OpenClaw upgrades.
- Appends are serialized with `flock`, but the gateway does not take that lock.
  Dispatcher-style schedules where the target agent is idle are the intended
  use case.
- Message text is stored verbatim. Treat the cron/script as the trust source.

## Test

```bash
scripts/send-to-transcript.sh --dry-run --agent X --to <chat> --thread-id <t> --message "hi"
scripts/send-to-transcript.sh --no-send --agent X --to <chat> --thread-id <t> --message "hi"
```
