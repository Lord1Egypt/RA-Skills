# Changelog

## 1.0.1 — 2026-06-24

Security-audit remediation (ClawHub / SkillSpector review):
- Pass mirror inputs to the embedded Python as positional **argv instead of
  environment variables** — removes the `os.environ` access pattern flagged as
  "env harvesting." The helper never reads ambient env for data; every value
  comes from this script's own flags.
- Declare **permissions & write scope** explicitly (new SKILL.md section + the
  publish ClawScan note): local FS writes are append-only to the agent's own
  transcript, plus state/log/lock files under `<openclaw-home>` — no network of
  its own, no model, no destructive ops.
- `publish-for-clawhub.sh`: portable version/changelog extraction (POSIX `sed`,
  dropped GNU-awk `match(...,array)`); the printed publish command is now
  `printf %q`-quoted so changelog text containing backticks/quotes can't break
  quoting or execute as shell.

## 1.0.0 — 2026-06-24

Initial release.

- `scripts/send-mirrored.sh`: send a message via `openclaw message send … --json`,
  then append one `delivery-mirror` assistant row to the owning agent's current
  session transcript (resolved from `agents/<agent>/sessions/sessions.json` →
  `sessionFile`, so it follows compaction rotation).
- Row shape mirrors what core produces via
  `appendAssistantMessageToSessionTranscript` (`provider: "openclaw"`,
  `model: "delivery-mirror"`, zeroed `usage` in core's `{input,output,cacheRead,`
  `cacheWrite,totalTokens,cost}` shape, `stopReason: "stop"`), `parentId`-chained
  to the last record. Adds the `openclawDeliveryMirror: {kind:"channel-final"}`
  marker that core attaches optionally; `sourceMessageId` is filled from the send
  result when available.
- Newline-safe append: if the transcript's last line lacks a trailing newline the
  helper inserts one, so a raw append can never glue onto the previous record.
- Session resolution: explicit `--session-key` → auto-constructed key
  (`group:<to>:topic:<thread>`, `group:<to>`, `direct:<to>`) → fallback scan of
  `sessions.json` matching `deliveryContext.to` / `route.target.to` + thread id.
- `--idem <key>` idempotency guard against double delivery on cron retry; the
  check → send → mark critical section is serialized with `flock` on
  `<agent>.seen.lock`. State in `<openclaw-home>/delivery-mirror/state/<agent>.seen`.
- `parentId` and the trailing-newline check are read **under** the per-session
  `fcntl.flock` on `<sessionFile>.mirror.lock`, so concurrent mirrors can't share
  a parent or clobber each other. (Note: the gateway does not take this lock —
  intended use is dispatcher schedules when the agent is idle.)
- Best-effort mirror: a send never fails because of a mirror problem (exit 0 with
  a warning if the session can't be resolved).
- Strict arg parsing under `set -u`: a value-flag missing its argument exits `2`
  (documented), not an unbound-variable crash.
- Flags: `--dry-run`, `--no-send` (mirror only), `--no-mirror` (send only),
  `--message-file` / stdin, `--openclaw-home`, `--openclaw-bin`.
