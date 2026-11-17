---
name: always-on-agent-ops
description: OpenClaw 24/7 ops — creates crons, deletes old logs, authenticated HTTPS queue poll, event-to-cron dispatch with locks, reads auth-profiles.json expiry. For silent agents.
metadata: {"clawdbot":{"emoji":"🛰️","requires":{"bins":["openclaw","node","curl","python3"]},"homepage":"https://openclaw.ai"}}
---

# OpenClaw Always-On Operations

An always-on agent does not die loudly. It goes quiet — expired auth, an unloaded plugin, a dispatcher pointing at an id that no longer exists. Everything below exists to make silence impossible.

## Access, data, and network — read before running anything

| Item | What this skill needs |
|---|---|
| What the shipped scripts do | `preflight-queue.sh`: one **authenticated HTTPS GET** (Bearer) to a queue URL you configure. `event-dispatch.sh`: runs `openclaw cron get/run` on job ids from a closed, hardcoded list, with `mkdir` locks. `oauth-expiry-check.sh`: **reads `auth-profiles.json`** and prints only key paths and expiry epochs — never a token value. `purge-retention.sh`: **deletes `*.log` files** under `$OPENCLAW_HOME/logs` past 30 days — dry run until you arm it. `cron-message.sh`: prints a status line. |
| What you create with it | Persistent OpenClaw **cron jobs** (§Cron layer), including a daily `gateway restart`. Every job is yours to review before `enabled: true`. |
| Host access | A logged-in GUI desktop session, permanently. The daemon is not headless. |
| Credentials | A gateway token (loopback only), a provider auth profile, and a queue Bearer. The Bearer lives in `~/.config/always-on-agent-ops/secrets.env` (chmod 600) — **outside** the skill directory, never in git, never in the agent workspace. Scope it read-only to the queue count, nothing else. |
| Data persisted | Cron job definitions, run state and run history (the shared SQLite state DB, `~/.openclaw/state/openclaw.sqlite`), the agent workspace and its memory files, logs. |
| Retention — **executed once armed** | Logs: **30 days**, deleted by `scripts/purge-retention.sh` (`cr-22`, weekly) — it ships in dry-run mode and deletes nothing until you set `PURGE_DRY_RUN=0` after reading one dry-run list. Orphaned lock dirs: **15 min** TTL, reclaimed by the dispatcher. Cron run state: life of the job — it goes when you delete the job. Workspace/memory: **no automatic purge** — `cr-22` reports its size so growth cannot stay invisible; the number you keep is yours to set. |
| Network out | Only what YOU configure: the queue you poll (HTTPS only; plain `http://` is refused except to `localhost`/`127.0.0.1`/`[::1]`), the notification channel you name. Default is no network — with no config file, the preflight emits `Human action required` and exits 0. |
| Network in | None. The gateway binds loopback. The optional loopback listener (below) is opt-in and never leaves the host. |
| Notifications | `${NOTIFY_CHANNEL}` receives short status lines. They leave the machine. Never put secrets, PII, or payload dumps in them. |

Everything a cron reaches out to is a system you are responsible for: honour its terms of service, and for any personal data touched, apply GDPR — legal basis, minimisation, and a stated retention window — before you schedule the first run.

## Setup

```bash
# ClawHub ships text, not file modes: the exec bit does NOT survive install. Without this, a
# cron `kind: "command"` dies with exit 126 and NO status line — the silence this skill prevents.
chmod +x scripts/preflight-queue.sh scripts/event-dispatch.sh \
         scripts/oauth-expiry-check.sh scripts/purge-retention.sh   # cron-message.sh is sourced: 644
# Secrets live OUTSIDE the skill directory: a skill folder gets copied, synced, zipped and
# re-published; a config dir does not. The preflight reads nothing from the network until this exists.
install -d -m 700 ~/.config/always-on-agent-ops
( umask 077; cat > ~/.config/always-on-agent-ops/secrets.env <<'EOF'
QUEUE_URL=https://queue.example.com/v1/pending
API_TOKEN=replace-me
EOF
)
ls -l ~/.config/always-on-agent-ops/secrets.env   # expect -rw------- and your user
```

The preflight **refuses** (one `Human action required` line, exit 0, no network) when the file is absent, empty, a symlink, not owned by you, has any group/other bit (`chmod 600` or `400` only), sits inside the skill directory, or when `QUEUE_URL` is not `https://` (loopback `http://` excepted) or carries `user@`. The file is **parsed for two keys, never sourced** — it cannot execute code. The Bearer goes to curl on stdin, never in argv, so it does not show in `ps`. Other path? `AOA_SECRETS_FILE=/abs/path` (absolute only). Prefer the OS keychain? Have a wrapper write the file at boot with `umask 077`; the checks are the same.

| Variable | Where it lives | Who substitutes it |
|---|---|---|
| `QUEUE_URL`, `API_TOKEN` | `~/.config/always-on-agent-ops/secrets.env` (or `$AOA_SECRETS_FILE`) | parsed by the preflight at run time — never sourced |
| `PURGE_DRY_RUN`, `LOG_RETENTION_DAYS`, `LOCK_TTL_MIN` | environment (optional) | the shell; default dry run, `30`, `15` |
| `OPENCLAW_HOME`, `OPENCLAW_AGENT_ID` | environment (optional) | the shell; default `~/.openclaw` and `main` |
| `GATEWAY_TOKEN`, `MODEL_PRIMARY`, `MODEL_FALLBACK`, `RUNTIME_ID`, `PROVIDER`, `*_PLUGIN`, `CHANNEL`, `NOTIFY_CHANNEL` | `openclaw.json` / job definitions below | **you, by hand** — OpenClaw does not interpolate `${...}` in its config. A literal `${GATEWAY_TOKEN}` left in the file is a literal token, and strict validation will not save you from it. |
| *(third-party, beyond `metadata.requires`)* | an authenticated queue endpoint you own or may call, a model provider account, a notification channel | you, before the first run |

## When to use

| Trigger | Action |
|---|---|
| "the agent stopped doing anything" | §OAuth first (silent auth death), then `openclaw cron list` for stuck jobs |
| "gateway won't start after I edited the config" | §Config as contract — strict validation rejects unknown keys |
| "how do I make my SaaS push to the agent?" | §The loopback cascade — you cannot. Invert to outbound poll |
| "my crons burn tokens finding nothing to do" | §Preflight layer — count without an LLM |
| "the cron fires manually but never on its event" | §Gotcha: real UUID job ids vs template ids |
| "setting up a dedicated always-on machine" | §Host constraints, then the `mac-mini` skill for the host itself, then §Ops checklist |
| "doctor wants to fix my config" | §Config as contract — `doctor --lint` first, `--fix` is a human step |

## Host constraints — the daemon is a user-level service tied to a GUI login session

| Constraint | Consequence you must implement |
|---|---|
| Service needs a logged-in session | The gateway is a per-user LaunchAgent (`ai.openclaw.gateway`): it starts at GUI login, not at boot. Unattended recovery after a reboot therefore needs **auto-login**, and on macOS auto-login and FileVault exclude each other. That is a **trade-off, not a hardening step**: FileVault on = a reboot waits for a human (macOS 26 can unlock the disk over SSH, but that opens no GUI session, so the gateway still does not start); FileVault off + auto-login = unattended restart, but physical theft reads the disk. Only take the second on a dedicated machine, physically secured, with no data unrelated to the agent. Decision, verification and the rest of the host checklist: the `mac-mini` skill. |
| Sleep kills the session | Disable disk/display sleep on AC power. |
| Restart is not automatic | A daily `gateway restart` cron (`cr-20`, 06:00) re-arms the loop. |
| A dead job stays dead | A watchdog cron 5 min later (`cr-21`, 06:05) lists jobs and **reports** errored/stuck ones. It reruns nothing on its own — see the gate in §Cron layer. |
| File-lock races | Keep `~/.openclaw` out of any syncing folder (iCloud/Dropbox). |
| Stray env overrides | A `launchctl setenv` gateway token silently overrides config → permanent "unauthorized". Unset it. |
| Node version drift | `nvm install 22 && nvm alias default 22` — check the CURRENT minimum (has been ≥22.x); a version manager keeps it identical across redeploys, the OS package does not. |
| Unpinned global install | `@latest` on a 24/7 host means the next reinstall silently changes the gateway under your crons. **Pin the exact release you tested**: `npm install -g openclaw@<version>` (this skill was last verified on `2026.8.1`), then `openclaw --version`. Upgrade deliberately, then run the §Ops checklist update row. |
| `sharp` fails to install | It compiles against a system libvips. Prefix the pinned install: `SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@<version>`. |
| macOS ships **bash 3.2** | `mapfile`/`readarray` are bash 4+. The shipped scripts avoid them; keep anything you add 3.2-compatible. |

## The loopback cascade — `bind: "loopback"` (§Config) answers only on `127.0.0.1`

An anti-SSRF default, correct, and it decides your whole architecture:

| Consequence | What it forces |
|---|---|
| The gateway is unreachable from the public internet | No cloud service can ever push you a webhook — not your SaaS, not a git host, not a form backend. Their POST cannot arrive. |
| Every integration inverts | The agent **polls outbound**. The host is a client, never a server. |
| Freshness is not free | Push is instant; poll costs one request per interval — and an LLM turn per interval if you are careless. That price is what §Preflight exists to avoid. |
| The source of truth lives on the *other* side | The agent asks "is there work?", takes one item, acts, **acknowledges**. No ack = the item stays queued, so a killed run re-appears as work instead of vanishing. Crash-safety is free from that shape alone. |

OpenClaw does expose an inbound hook (`POST 127.0.0.1:18789/hooks/agent`, Bearer), reachable **only from the host**: useful for a local process to nudge the agent, useless from the internet. Exposing the control plane beyond loopback to "fix" this trades an SSRF-hardened default for a remote-code surface — don't. For local push, run a listener bound to `127.0.0.1` that authenticates a Bearer and accepts **one event name from a closed list hardcoded in the listener**, passing it as the dispatcher's only argument: no request body, no free-form arguments, no raw agent turn. `scripts/event-dispatch.sh` enforces that same closed list — an unrecognised event exits 2 without touching a job.

## Config as contract

`~/.openclaw/openclaw.json` (JSON5) is **strictly validated**: one unknown key, one wrong type, and the gateway refuses to start. OpenClaw keeps a last-known-good copy and restores it when the file is broken — so a bad edit can leave you running yesterday's config while you read today's file. Confirm with a restart, never by reading.

```json5
{
  gateway: {
    port: 18789, mode: "local", bind: "loopback",  // "local" mandatory; anything else = damaged
    auth: { mode: "token", token: "${GATEWAY_TOKEN}" },
    nodes: { commands: { deny: ["camera.snap", "camera.clip", "screen.record",  // capture/publish/agenda
              "sms.send", "sms.search", "contacts.add", "calendar.add", "reminders.add"] } },
  },
  agents: {
    defaults: {
      model: { primary: "${MODEL_PRIMARY}", fallbacks: ["${MODEL_FALLBACK}"] },
      models: {                          // MANDATORY allowlist: primary+fallbacks must appear here
        "${MODEL_PRIMARY}":  { agentRuntime: { id: "${RUNTIME_ID}" } },
        "${MODEL_FALLBACK}": { agentRuntime: { id: "${RUNTIME_ID}" } } },
      workspace: "${OPENCLAW_HOME}/workspace" },
    entries: { main: {} } },               // keyed map; `list: [...]` is the legacy shape
  plugins: { entries: {                  // EXCLUSIVE allowlist — omitted plugin = not loaded, silently
    "${NOTIFY_PLUGIN}": { enabled: true },   // example — your chat/notification transport
    "${PROVIDER_PLUGIN}": { enabled: true }, // example — your model provider
    "${RUNTIME_PLUGIN}": { enabled: true },  // the runtime named by agentRuntime.id above; without
  } },                                       // it, agentRuntime never executes
  tools: { profile: "minimal" },         // minimal|messaging|coding|full — narrowest; jobs inherit THIS
  commands: { native: "auto", restart: true },
}
```

Validate a candidate file **before** it goes live — the gateway never sees it:

```bash
OPENCLAW_CONFIG_PATH=/tmp/candidate.json5 openclaw config validate
# Output: Config valid: /tmp/candidate.json5
# Output: × candidate.json5:5 — gateway.nodes: Unrecognized key: "denyCommands"
openclaw doctor --lint --json; echo "exit=$?"      # live config, read-only: 0 clean, 1 findings, 2 failed
```

The validation error ends with "Run `openclaw doctor --fix` to repair". On a live host, don't — see the first row.

| Rule | Failure mode if ignored |
|---|---|
| Strict validation | Unknown key → gateway won't boot. Diagnose with **`openclaw doctor --lint`** (read-only, exit 0 = clean, 1 = findings, 2 = could not run; `--json` for the finding list) or `openclaw config validate`. **Not `doctor --fix`** on a live host: it deletes unknown keys without asking, and it runs cron-store migrations — a legacy `~/.openclaw/cron/jobs.json` left from a backup or an old host gets imported, and jobs you had retired can come back. `--fix` is a human step: back up, run it, read the stripped-key list and `openclaw cron list` before walking away. |
| `plugins` is an exclusive allowlist | A plugin you forgot simply doesn't load. No error. The feature is just absent. |
| `agents.defaults.models` is an allowlist | Model in `primary`/`fallbacks` but not listed → `Model not allowed`, thrown before any response. |
| `gateway.nodes.commands.deny` | Without it, a default set may allow capture/publish/agenda actions your always-on agent can fire unattended. (`nodes.denyCommands` is **not** a key — it fails validation.) |
| `commands.allowFrom` | If set, it becomes the **only** authorization source for commands and cancels pairing/channel allowlists — an empty list denies everyone. Don't set it without a reason. |
| `commands.ownerAllowFrom` | A separate owner list: it decides who reaches owner-only commands **and who can approve exec requests**. Anyone in it holds the keys to the host. Keep it to one or two identities you control, and re-read it whenever you touch `allowFrom` — the two are easy to confuse: only `allowFrom` replaces pairing (verified on `2026.8.1`). |
| Restart rule | Changes to `gateway.*`, `plugins.*`, `browser.*` need `openclaw gateway restart`. Others may hot-reload. When in doubt: restart. |
| `tools.profile` is inherited | A job with no explicit `payload.tools` runs with the **global** profile. That is why the global must be the narrowest one that boots, never the widest: per-job grain is then a deliberate widening, not a hoped-for restriction. |

## Auth and runtime are two orthogonal axes

**Auth** = which account pays (a provider profile: OAuth or an API key). **Runtime** = which executor runs the agentic turn (`agentRuntime.id`). Configuring one does not configure the other. All four must be present together — miss one and it breaks *before* the first response:

| # | Ingredient | Miss it → |
|---|---|---|
| 1 | `model.primary` in the live provider namespace | wrong/dead provider |
| 2 | `agentRuntime.id` set **per model** in `agents.defaults.models` | no executor |
| 3 | The runtime plugin enabled in `plugins.entries` | runtime never loads (allowlist) |
| 4 | `auth.order.<provider>` lists the profile | a profile outside `order` is **never tried** |

```bash
openclaw models list --provider ${PROVIDER}   # never copy model names from a runbook — enumerate
# Output: no results  <- legacy <provider>-<runtime>/* namespace is dead; `doctor --fix` rewrites it
```

**The runtime carries its own execution posture.** A local `codex` runtime defaults to *no approvals + full host access*, configured below OpenClaw (`~/.codex/config.toml`: `approval_policy`, `sandbox_mode`, trusted dirs). A tool profile narrows what OpenClaw offers, not what that runtime may do. State the shell policy where it is enforced — `tools.exec.mode: "deny"` for an agent that must not run commands — and read the runtime's own config on the host. Proof, not assumption: ask the agent to run `id -un` in a test turn; it must be refused.

**For an unattended host, use an API key.** It is the supported path: pay-per-token, no expiry, no human in the loop. OAuth is subscription-priced but expires in days and needs a browser — on a 24/7 host you trade money against a recurring silent outage, and the outage wins. `auth-profiles.json` (in `~/.openclaw/agents/<agent>/agent/`) is a **credential, not a config file** — treat it like a private key: never in git, no SecretRef support. Copying it to another host is *gray-area and not the recommended path*: only acceptable if your provider's terms allow that account on that machine. Check the terms before you copy.

## Failure #1: OAuth dies silently

A subscription OAuth token expires in **days** and does **not** refresh headless. The daemon keeps running; every turn just fails. Nobody is watching at 03:00. This is the single most common way an always-on agent dies.

```bash
OPENCLAW_HOME=~/.openclaw ./scripts/oauth-expiry-check.sh
# EARLIEST epoch expiry wins: a fresh profile must never mask a dead one, nor a 90-day refresh token
# a dead access token. It names the deciding `field` and NEVER exits non-zero. "Cannot determine" is
# NEVER `ok`: corrupt JSON, no python3, an unreadable (ISO-8601) expiry all emit `warn` — the mtime
# proxy is reached ONLY when the file parses and genuinely carries no expiry field at all.
# Output: {"status":"warn","source":"expires_at","field":"profiles.dead.expires_at","remaining_days":-1,"note":"...relogin..."}
# Output: {"status":"warn","source":"unresolved","reason":"corrupt_json","note":"Cannot verify token expiry..."}
```

Wire it to `cr-23` (below), whose only instruction is: run the script, and if `status` is `warn` or `missing`, alert `${NOTIFY_CHANNEL}` that a **human relogin** is needed. The cron must **not** attempt the login itself — that flow needs a real browser. Alert on warn; stay silent on ok.

## Cron layer

The scheduler is in-process in the gateway (no system crontab). On `2026.8.1`, jobs, run state and history live in the **shared SQLite state DB** — not in `jobs.json`. Legacy `~/.openclaw/cron/jobs.json` files are imported once by `doctor --fix` and renamed `.migrated`; an edit to a `jobs.json` afterwards is ignored. Change jobs only through `openclaw cron add|edit|enable|disable|rm`; inspect with `openclaw cron list` / `cron get <id>`. Never write to the DB.

```json5
{ id: "cr-10-worker", agentId: "main", enabled: true,
  schedule: { kind: "cron", expr: "0 9-18 * * 1-5", tz: "UTC" },  // IANA tz; or kind:"every"/"at"
  sessionTarget: "isolated", wakeMode: "now",   // isolated = inherits no context, no credentials-in-
  payload: { kind: "agentTurn", message: "…",   // conversation, no half-done state from another run
             model: "${MODEL_PRIMARY}", fallbacks: ["${MODEL_FALLBACK}"],
             tools: ["exec", "read"],           // ALWAYS explicit: a read-only audit and a job that
             thinking: "medium",                // pushes branches must not share an authority
             timeoutSeconds: 2400 },            // surface just because they share a host
  delivery: { mode: "announce", channel: "${CHANNEL}", to: "${NOTIFY_CHANNEL}" },
  failureAlert: { after: 2, to: "${NOTIFY_CHANNEL}", cooldownMs: 1800000 } }
```

The four housekeeping jobs the §Ops checklist watches — `argv[0]` is an **absolute path** in every case, a cron's `PATH` is not your shell's — then the laws for anything that runs unattended:

| id | Schedule | Payload |
|---|---|---|
| `cr-20-restart` | `{ kind: "cron", expr: "0 6 * * *", tz: "UTC" }` | `{ kind: "command", argv: ["/opt/homebrew/bin/openclaw", "gateway", "restart"] }` |
| `cr-21-watchdog` | `{ kind: "cron", expr: "5 6 * * *", tz: "UTC" }` | `{ kind: "agentTurn", tools: ["exec"], message: "Run exactly: openclaw cron list. Report errored or stuck job ids in one status line with status Human action required. Do not run, edit, enable, disable or delete any job. Run no other command." }` |
| `cr-22-purge` | `{ kind: "cron", expr: "0 5 * * 0", tz: "UTC" }` | `{ kind: "command", argv: ["/abs/path/to/scripts/purge-retention.sh"] }` — dry run. Armed, after you read one dry-run list: `argv: ["/usr/bin/env", "PURGE_DRY_RUN=0", "/abs/path/to/scripts/purge-retention.sh"]` |
| `cr-23-oauth` | `{ kind: "cron", expr: "0 8 * * *", tz: "UTC" }` | `{ kind: "agentTurn", tools: ["exec"], message: "Run scripts/oauth-expiry-check.sh. If status is warn or missing, alert that a human relogin is needed. Silent on ok." }` |

**The watchdog is report-only by design.** An unattended turn holding `exec` that may rerun "whatever looks stuck" can re-fire a job that pushes, sends or bills — twice. Reruns stay a human decision: read the `cr-21` line, then `openclaw cron run <id>` yourself. If you must automate it, widen deliberately and narrowly: name the rerunnable ids in the message (a closed list of idempotent, read-only jobs), cap it at one rerun per job per day, and never include a job that acts outside the host.

- **Idempotence first.** A cron wakes with no memory. Before acting, read the state: your own index file *and* the remote's. In doubt, SKIP — a skipped run costs nothing, a duplicate action costs trust.
- **Failure = no ack.** If a check goes red, don't acknowledge. The item stays queued and a healthy later run takes it. Never ack to make an alert stop.
- **Bounded backoff, not correction.** The scheduler retries a failed run with bounded backoff (roughly ~30s → 1m → 5m → 15m, ~3 attempts, reset on success). Never *depend* on retry to fix a logic failure — that's what the un-acked queue is for.
- **`announce` is an exit, not a filter.** It delivers the agent's final text as-is, and an isolated job can also call the `message` tool even with `--no-deliver`. A prompt that says "don't quote the input" is not a barrier. For any job that reads private input: `--no-deliver`, keep `message` out of `payload.tools`, and publish from a `kind: "command"` job whose script builds the line from an allowlist of fields. Command stdout is delivered too — print only the status line; print `NO_REPLY` to stay silent.
- **One normalized status line.** Every job and script emits the same shape via `scripts/cron-message.sh`. Without it, ten jobs invent ten formats and the channel becomes unreadable within a week.

## Output format — every job, every script

```text
<job-id> - <Done | Nothing to do | Started | Blocked | Human action required | Error>
Result: <one factual sentence>
Item: <what was touched>
Next action: <what happens next, or "none">
Details: <short key=value context, never a secret>

dispatch - Started               <- emitted by the DISPATCHER when a preflight counts > 0;
Result: Job requested.              the preflight stays silent and execs it. Verified output.
Item: cr-10-worker
Next action: OpenClaw runs it now.
Details: event=work_ready count=2
```

## Preflight layer

Stop paying an LLM turn to discover there is nothing to do. Split every heavy job in two: the preflight counts and, if `count > 0`, calls the dispatcher with a **named event**; the dispatcher runs the matching job(s) now. The heavy job keeps a widely-spaced `every` schedule as a safety net for the day a preflight silently breaks. Result: near-event-driven latency at poll-loop cost, with a floor under it.

| Layer | Kind | Frequency | Cost |
|---|---|---|---|
| `pf-*` preflight | `kind: "command"` (argv → shell script) | every 5–15 min | one curl + a count. **Zero LLM.** |
| `cr-*` heavy job | `kind: "agentTurn"` | `every` 6h **fallback only** | a full agent turn |

```json5
{ id: "pf-10-queue", enabled: true, schedule: { kind: "every", ms: 600000 },   // 10 min
  payload: { kind: "command", argv: ["/abs/path/to/scripts/preflight-queue.sh"] } }  // cron PATH != yours
```

> **THE PREFLIGHT DECIDES NOTHING. IT COUNTS.** It must never claim an item, mutate state, or reason about what to do — the moment a preflight starts judging, you have a second, cheaper, untested agent making production decisions in bash. Count, dispatch, exit.

**`every` does not spread a fleet — it phase-locks it.** The table above tells you to give each heavy job a widely-spaced `every` as its safety net. Do that for five jobs in one provisioning pass and all five fire **together, forever**. Interval schedules do not drift: equal intervals preserve whatever phase the jobs were created with, and a fleet provisioned in one pass was created seconds apart. Pick a round anchor and it is worse — five jobs at `everyMs: 21600000` created on a timestamp that divides evenly by 6h land on the same 00/06/12/18 grid to the second. Five agent turns spawning worktrees, installs and a browser at the same instant on one host is a safety net that has become the outage.

Two things sharpen it. **The fallback bypasses your only concurrency guard**: the scheduler fires the job directly, so it never passes through `event-dispatch.sh` and neither the `mkdir` lock nor the `runningAtMs` check is in the loop — the one moment the fleet is most likely to collide is the one moment nothing is guarding it. And **the daily restart re-anchors**: `cr-20` reloads every job at once, so a fleet you hand-staggered can silently re-converge after a reboot.

| Do | Not |
|---|---|
| Give each heavy fallback an explicit `cron` expression on its own minute — the way `cr-20`…`cr-23` above already are (`0 6`, `5 6`, `0 5`, `0 8`). `openclaw cron list` then **shows** you the phase plan. | Five `every: 6h` jobs and the assumption they will drift apart. They will not. |
| `--stagger 5m` (cron schedules only; `--exact` forces 0). On `2026.8.1`, top-of-hour expressions with a wildcard hour are auto-staggered up to 5 min — `every` schedules never are. Confirm with `openclaw cron get <id>`. | A phase plan that exists only as arithmetic nobody re-derives at 03:00. |

Verify rather than trust the shape: `openclaw cron list`, read the next-run times, and check that no two heavy jobs share a minute. If they do, you have not built a safety net — you have built a thundering herd with a 6-hour period.

```bash
./scripts/preflight-queue.sh
# Tolerant count: numeric `count`, else the SHALLOWEST array anywhere (nested {data:{items:[…]}} still
# counts; an API renaming `items` to `results` degrades to a count, not a crash loop). "Counted zero"
# is NOT "found nothing to count": an empty array is 0, but no-count-and-no-array — a 200 carrying
# {"error":"unauthorized"}, 502 HTML, a captive portal — is an Error. A green "Nothing to do" while the
# queue fills is worse than a crash. No config, open perms, http://, dead host, junk body -> one line, exit 0,
# never a bare shell error. Hence no `set -e`: a broken preflight must still produce a line.
# Output: pf-10-queue - Nothing to do / Result: Queue empty. / ... / Details: count=0
# Output: pf-10-queue - Error / Result: Payload carries no count and no array... / Details: reason=no_countable_field
```

`scripts/event-dispatch.sh` maps events → jobs, with three guards:

1. **`mkdir` lock** per job id — atomic, no race, released with `rmdir` (never a recursive delete) on `RETURN`, `EXIT`, `INT` and `TERM`, plus a TTL. `trap ... RETURN` alone is not enough: a `kill -9`, the 06:00 restart or a sleeping machine leaves the dir behind and blocks that event **forever**, while the channel keeps printing a healthy-looking `Blocked`. A lock older than `LOCK_TTL_MIN` (default 15) is reclaimed.
2. **Job exists** — `openclaw cron get <id>` first. A non-zero exit, an empty answer, or a reply that is not JSON carrying that id is an `Error` line naming the fix. It classifies into exactly `unknown | running | idle`, so a release whose `cron get` exits 0 and prints prose ("job not found") cannot fall through to a run on a bogus id. Verify yours: `openclaw cron get nope; echo $?`.
3. **`runningAtMs` guard** — if the job is mid-run, report `Blocked` and return 0. Never stack turns on a running job.

One event may fan out to several jobs (`source_changed` → reviewer + drift-watch). The shipped mapping's `cr-30-reviewer` and `cr-40-drift-watch` are **illustrative placeholders — this skill defines only `cr-10-worker` and `cr-20`…`cr-23`**; until you point them at jobs you installed, those two events dispatch to nothing but an `Error` line (which is the designed failure, not a silent one). Keep the event vocabulary about **what happened in the world** (`work_ready`, `review_needed`, `source_changed`), never about which job you want to run — that's the mapping's job, and it's the only place that changes when you rename a cron.

## Gotchas

| Symptom | Root cause | Fix |
|---|---|---|
| Event dispatch reports success, job never runs | **`openclaw cron add` accepts no `--id`: the installed job gets an auto-generated UUID**, and its name is prefixed. Your template's tidy `cr-30-reviewer` exists only in your file. The dispatcher's `openclaw cron run cr-30-reviewer` targets a job that was never installed — and it fails in a way that reads like nothing happened. Every job is affected: jobs live in SQLite, and a hand-written `jobs.json` is ignored. | `openclaw cron list`, copy the **real** ids, and point the mapping at those. Re-check after any re-provisioning: new install, new UUIDs. |
| Script dies with no status line, exit 126 | The exec bit did not survive install — ClawHub ships text, not modes | The four `chmod +x` in §Setup. `cron-message.sh` stays 644 |
| Preflight says `reason=config_mode` / `url_not_https` | Config file readable by others, or a plain-http queue URL | `chmod 600` the file; use `https://`. The Bearer is never sent until both hold |
| Feature configured but absent, no error | `plugins` allowlist is exclusive — the entry is missing | Add it to `plugins.entries` and **restart** |
| `Model not allowed` before any answer | Model used but not in `agents.defaults.models` | Add it with its `agentRuntime` |
| Gateway won't boot after an edit | Strict validation rejected an unknown key or a bad enum (`tools.profile: "restricted"` is one) | `openclaw config validate` / `doctor --lint --json`, fix the key by hand. `doctor --fix` only as a human step (§Config) |
| Retired jobs are back after a repair | `doctor --fix` imported a stale legacy `jobs.json` | `openclaw cron disable <id>` / `rm`; delete or archive old `~/.openclaw/cron/` copies before any `--fix` |
| Chat channel received raw input the agent read | `announce` shipped the final text; a prompt was the only guard | §Cron layer: `--no-deliver` + field-allowlisted `command` job |
| Memory guard skips 100 % of runs on macOS | It thresholds on `vm_stat` "free", which sits near zero on a healthy Mac (~160 MB free on 24 GB at pressure 1) | Gate on `sysctl -n kern.memorystatus_vm_pressure_level`: 1 normal, 2 warning, 4 critical. Skip when `> 1` |
| Every wake is slow and expensive | A long reference doc sits in an injected workspace file (`AGENTS.md`, `MEMORY.md`…). Measured: one 17.9k-char API reference = ~5k tokens = 17 % of context, paid every turn | Keep only what the agent acts on in injected files; move script-author references out of the workspace. `/context` shows raw vs injected size |
| Config edited, behaviour unchanged | Last-known-good restored, or `gateway.*`/`plugins.*` needs a restart | `openclaw gateway restart`, then verify live state |
| Persistent "unauthorized" on loopback | A `launchctl setenv` token overrides the config file | Unset it, restart |
| Dispatch always says `Blocked`, no job ever runs | A killed run (restart, sleep, `kill -9`) orphaned its lock dir; the channel looks healthy | Wait: the TTL reclaims it after `LOCK_TTL_MIN` (lower it if your jobs are short). Now: `rmdir` the **exact** path printed in the `Blocked` line's `Next action` — one dir, no glob, no `-r`. `rmdir` refuses anything non-empty; if it refuses, something else wrote there — look before you delete |
| `cr-23` says `ok` while every turn fails | Several profiles in one auth file, and a fresh one masked the dead one — the shipped checker takes the **earliest** expiry precisely for this | Read `field` in the JSON: it names the profile that decided. If you wrote your own checker, take the min — and make "cannot determine" a `warn`, never an `ok` |
| `cr-22` reports `Not an OpenClaw home` | `OPENCLAW_HOME` points somewhere without `openclaw.json` or `agents/` — a typo or a stale env var | Intended: the purge refuses any dir it cannot prove is an agent home rather than deleting on faith. Fix the variable |
| All runs fail overnight, no alert | OAuth expired headless | `cr-23` + human relogin; consider an API key |
| Notification channel unreadable | Jobs invented their own formats | One `cron-message.sh`, no exceptions |

## Ops checklist

| Watch | Cadence | Symptom → cause |
|---|---|---|
| `openclaw gateway status` | daily (`cr-20` restart 06:00) | not up → session logged out / machine slept |
| `openclaw cron list` | daily (`cr-21` watchdog 06:05) | errored/stuck ids reported → a human decides each rerun; missing next-run → scheduler restart |
| `oauth-expiry-check.sh` | daily (`cr-23` 08:00) | `warn`/`missing` → human relogin, today |
| Preflight + `dispatch` status lines | continuous | `reason=no_countable_field` → the endpoint changed shape or the token died (it self-reports; it does not print a green `Nothing to do`); `dispatch - Error` → mapping points at dead ids |
| Heavy-job fallback runs | weekly | fallback firing every time → the preflight is broken, fix the preflight |
| Logs + workspace size | weekly (`cr-22` purge 05:00 Sun) | `mode=dry_run` line → not armed yet: read the list, then arm (§Cron layer); armed → logs past 30d purged; workspace growing → set your own bound |
| `openclaw --version` + Node | on update | after `openclaw update`: `doctor --lint`, `gateway restart`, `health`, `cron list` (same ids, same `enabled`) |
| Host: reboot recovery, auto-login, power | monthly + after any macOS update | gateway down after reboot → see the `mac-mini` skill |

## Scope

This skill ONLY: configures an OpenClaw host you control; polls endpoints **you** own or are authorized to call, over HTTPS; creates cron jobs you review, with per-job tool restrictions; reads auth-profile expiry metadata and alerts a human; deletes only `*.log` files under `$OPENCLAW_HOME/logs` past the stated window, once you arm it; emits normalized status lines.

This skill NEVER: exposes the control plane beyond loopback; bypasses an anti-abuse control, rate limit, or authentication check — when a defence triggers, the run **stops and pings a human** instead of adapting; performs an irreversible action unattended; reruns a job without a human decision; prints a token value; conceals a failure behind an ack; writes secrets into the workspace, the notification channel, or git.

*Alexandre Bloch — Bloch Agents · ClawHub @AlexBloch-IA*
