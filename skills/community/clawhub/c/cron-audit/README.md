# openclaw-cron-audit

Find the [OpenClaw](https://github.com/openclaw/openclaw) cron jobs that fail without telling anyone.

On one real install, a shopping-alert job failed **35 runs in a row** and another **66**, and nobody
noticed for a month. Both announced to `delivery.channel: "last"`. A cron job runs in an isolated
session with no chat history, so there is no "last" channel to resolve. The failure notification
fell back to the same unroutable target, so the failure alert failed too.

This script reads `openclaw cron list --all --json` and flags every job in that situation and its
relatives. It is also an [OpenClaw skill](SKILL.md), so an agent can run it and explain the findings.

- Python 3 standard library, no dependencies
- read-only by default; `--heal` is opt-in
- built to run as a cron job itself: it reports changes, not state, so it never spams

## What it checks

| Check | Severity | Why it is silent |
|---|---|---|
| `route` | 🔴 | `announce` to `last` or unset channel, Discord/Slack/Mattermost/Matrix with no `to`, or a Discord `to` without the `channel:`/`user:` prefix. Every run fails at delivery, and the failure alert usually falls back to the same broken target. |
| `errors` | 🔴 | `consecutiveErrors > 0`. Keyed on the error text, so a climbing counter is reported once but a *different* error is new. |
| `alert-failed` | 🔴 | The last failure notification itself was not delivered. |
| `alert-route` | 🔴 | The per-job `failureAlert` points at `last` or at a channel without a valid recipient. |
| `delivery` | 🟡 | The run succeeded but its output was not delivered (intentional `NO_REPLY` silence is ignored). |
| `no-alert` | 🟡 | No per-job failure alert. |
| `best-effort` | 🟡 | `delivery.bestEffort: true` suppresses the failure notification entirely. |
| `overdue` | 🟡 | `nextRunAtMs` is more than `--overdue-hours` in the past: the scheduler stopped firing it. |
| `never-ran` | 🟡 | A recurring job enabled for `--never-ran-days` that has never run. |
| — | 🔴 | `cron list` returned only part of the jobs (`hasMore`; the CLI has no offset flag). |

Problems on disabled jobs are listed as ⚪ notes: they cannot fire now, but they will the moment
someone re-enables the job.

## Install

As a skill:

```bash
clawhub install cron-audit
```

(ClawHub reserves the `openclaw-` slug prefix, so the skill is published as `cron-audit`.)

Or just the script:

```bash
git clone https://github.com/cprite/cron-audit
python3 cron-audit/scripts/cron_audit.py --full
```

## Usage

```bash
cron_audit.py --full            # every current finding
cron_audit.py --json            # machine-readable
cron_audit.py                   # change report (for scheduling); prints NO_REPLY when nothing changed
cron_audit.py --full --strict   # exit 1 on any error-level finding (CI, scripts)
cron_audit.py --input jobs.json # audit a saved `cron list --all --json` instead of the gateway
```

Example:

```
**🧭 Cron audit** — 3 finding(s) across 71 jobs

__Errors__
🔴 `goods-hunt` (shopping, 5f3c2a10) — fails on every run: delivery.channel is "last" or unset, and an isolated cron session has no last channel

__Warnings__
🟡 `weekly-review` (main, 9b1e44d7) — no failure alert configured

__Disabled jobs__
⚪ `weekly-report` (fitness, 0c7d8e21) — disabled, route broken (delivery.to "123456789012345678" has no "channel:" or "user:" prefix, which Discord rejects); fix before re-enabling
```

### As a watchdog

Schedule it as a command-payload cron job. It stays silent while nothing changes, posts new and
resolved findings, and sends a digest weekly (`--digest-hours`). The digest says "all N cron jobs
look healthy" when there is nothing to report, so silence never means the audit died.

```bash
openclaw cron add --name cron-audit --cron "17 */6 * * *" --session isolated \
  --command "python3 /path/to/cron_audit.py --heal" --timeout-seconds 180 \
  --announce --channel discord --account <accountId> --to "channel:<id>"
```

State lives in `~/.openclaw/state/cron-audit.json` (`--state`, `$CRON_AUDIT_STATE`). If the gateway
cannot be reached, the audit reports that once and keeps its previous findings, so recovery does not
re-announce everything as new.

### `--heal`

`--heal` edits live jobs. It does two things, each only when configured:

1. **Broken routes on enabled jobs** are re-pointed at the agent's default route from
   `~/.openclaw/cron-routes.json` (`--routes`; see [the example](references/cron-routes.example.json)).
   The repair is reported loudly: the agent's home channel is a safe landing spot, not necessarily
   the right thread.
2. **Missing failure alerts** are armed when you give a destination:

   ```bash
   cron_audit.py --heal --alert-channel discord --alert-to channel:<id> --alert-account <accountId>
   ```

   or `CRON_AUDIT_ALERT_CHANNEL`, `CRON_AUDIT_ALERT_TO`, `CRON_AUDIT_ALERT_ACCOUNT`.
   Defaults: alert after 3 errors (`--alert-after`), 12h cooldown (`--alert-cooldown`), skipped runs excluded.

## Choosing the right fix

Do not answer every `route` finding with `--announce`. Decide what the job is:

- **The agent posts its own results** (monitors, hunts, anything that must stay quiet when there is
  nothing new) → `openclaw cron edit <id> --no-deliver`. `--announce` is a *fallback* that ships the
  final turn text whenever the agent sent nothing, which means every quiet cycle.
- **The runner delivers** (digests, reports, reminders) → pin the whole route:
  `--announce --channel <ch> --account <accountId> --to "channel:<id>" --no-best-effort-deliver`.

Verify with `openclaw cron list`: Delivery should read `not requested` or end in `(explicit)`.

## Limits

- `no-alert` looks at the per-job `failureAlert` only. A global `cron.failureAlert` in `openclaw.json`
  is not visible in `cron list`, so jobs covered only by it are still reported.
- Only the fields exposed by `cron list --json` are checked; tested against OpenClaw 2026.9.3.

## Tests

```bash
python3 -m unittest discover -s tests
```

## License

[MIT-0](LICENSE)
