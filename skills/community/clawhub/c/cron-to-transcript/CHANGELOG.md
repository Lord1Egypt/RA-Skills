# Changelog

## 1.0.2 — 2026-06-25

- Re-published with the ClawHub display name set explicitly to Cron To Session
  Transcript. Version 1.0.1 already carried the new files and summary, but the
  registry display name stayed at the previous title because publish was run
  without `--name`.

## 1.0.1 — 2026-06-25

- Renamed the public display name from Cron to Transcript to Cron To Session
  Transcript while keeping the stable `cron-to-transcript` slug.
- Tightened the short description around the real pain: isolated crons,
  scripts, reminders, and status checkers that send successfully but never land
  in the owning agent's session transcript.

## 1.0.0 — 2026-06-25

Initial Cron to Transcript release.

- Reframed the skill around the concrete action: write command-cron/script
  deliveries into the owning agent transcript.
- Published as `cron-to-transcript` with the pain-hook description: "Your Cron
  sent it but the agent forgot?"
- Keeps the battle-tested runtime behavior: send first, append one
  transcript-only assistant row, optional `--idem` dedupe, best-effort append.
- Renamed the user-facing helper to `scripts/send-to-transcript.sh`.
- Preserves OpenClaw core compatibility by keeping the internal transcript row
  shape at `provider: "openclaw"` and `model: "delivery-mirror"`.
- Uses positional `argv` for embedded Python inputs, explicit local write scope,
  and a `printf %q`-quoted publish command.
