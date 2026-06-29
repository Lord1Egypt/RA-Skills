# Security Policy — Cron To Session Transcript

## What It Touches

- Reads `<openclaw-home>/agents/<agent>/sessions/sessions.json` to resolve the
  target session's current `sessionFile`.
- Appends exactly one JSONL row to that `sessionFile`. It never edits or removes
  existing rows.
- Writes idempotency state and logs under
  `<openclaw-home>/cron-to-transcript/`, plus a
  `<sessionFile>.transcript.lock` advisory lock file.
- Executes `openclaw message send` to deliver the message.

It performs no network calls of its own, runs no model, and takes no destructive
action.

## Trust Boundaries

The message text is passed straight to `openclaw message send` and stored
verbatim in the transcript row. Treat the caller (the cron/script) as the trust
source; the helper does not sanitize or interpret content.

The helper only writes into the `sessionFile` of a session it positively matched
by key or by delivery target + thread id. If no session matches, it does nothing
to any transcript and exits 0.

## Known Risks and Mitigations

- **Reproduces a core row from bash.** The internal row uses
  `provider: "openclaw"` and `model: "delivery-mirror"` because OpenClaw core
  recognizes that delivery marker. No CLI exposes the internal append function.
  Mitigation: the append is isolated to one newline-safe JSONL row; re-verify
  after major OpenClaw upgrades.
- **Concurrent writes.** A live gateway write could interleave. Mitigation:
  advisory `fcntl.flock` on a per-session lock file; intended use is dispatcher
  schedules when the target agent is idle.
- **State growth.** The `.seen` idempotency file grows by one line per unique
  `--idem` key. Rotate/clear it if you generate unbounded keys.

## Reporting

Open an issue at:
https://github.com/obuchowski/openclaw-cron-to-transcript
