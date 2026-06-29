# Security Policy — delivery-mirror

## What it touches

- **Reads** `<openclaw-home>/agents/<agent>/sessions/sessions.json` to resolve
  the target session's current `sessionFile`.
- **Appends** exactly one JSONL row to that `sessionFile` (the agent's own
  transcript). It never edits or removes existing rows.
- **Writes** an idempotency state file
  (`<openclaw-home>/delivery-mirror/state/<agent>.seen`), a log
  (`<openclaw-home>/delivery-mirror/mirror.log`), and a lock file
  (`<sessionFile>.mirror.lock`).
- **Executes** `openclaw message send` to deliver the message.

It performs **no network calls of its own**, runs **no model**, and takes **no
destructive action** (no deletes, no overwrites of existing data).

## Trust boundaries

- The message text is passed straight to `openclaw message send` and stored
  verbatim in the transcript row. Treat the caller (the cron/script) as the
  trust source; the helper does not sanitize or interpret content.
- The helper only ever writes into the `sessionFile` of a session it positively
  matched by key or by `deliveryContext`/`route` target + thread id. If no
  session matches, it does nothing to any transcript and exits 0.

## Known risks and mitigations

- **Reproduces a core row from bash.** The `delivery-mirror` row is a first-class
  core concept (written by `appendAssistantMessageToSessionTranscript`, matched by
  core's `isDeliveryMirror` predicate on `provider`+`model`). The coupling is that
  we hand-append the JSONL — including the `openclawDeliveryMirror:{kind:"channel-final"}`
  marker — rather than calling that internal function, because no CLI or tool
  exposes it. *Mitigation:* mirroring is best-effort and isolated to an append;
  re-verify after a major OpenClaw upgrade. A malformed append at worst adds one
  ignorable row; it cannot corrupt earlier records.
- **Concurrent writes.** A live session being written by the gateway at the same
  instant could interleave. *Mitigation:* advisory `fcntl.flock` on a per-session
  lock file; intended use is dispatcher schedules when the agent is idle. Do not
  mirror into a topic whose agent is actively mid-run.
- **State growth.** The `.seen` idempotency file grows by one line per unique
  `--idem` key. *Mitigation:* only used when `--idem` is passed; rotate/clear it
  if you generate unbounded keys.

## Reporting

Open an issue at the project homepage:
https://github.com/obuchowski/openclaw-delivery-mirror
