---
name: openclaw-update-runbook
description: Use when updating OpenClaw or debugging an OpenClaw instance after an update. This skill acts as a structured update runbook with emphasis on gateway startup, service-manager state, plugin registry and install drift, bundled-vs-npm/clawhub plugin confusion, stale config carried across upgrades, channel health, task ledger corruption, and logs that explain why the updated system is slow, disconnected, or half-broken.
version: 1.0.6
metadata:
  openclaw:
    emoji: "🦞"
---

# OpenClaw Update Runbook

Use this skill when an OpenClaw host was just updated, is about to be updated, or is behaving strangely after an update. It is a generic operator runbook, not a release-specific checklist.

This skill is meant to be installed as a folder, not copied as a single file. It expects `references/failure-patterns.md` to exist locally beside `SKILL.md` inside the same skill bundle.

The goal is not only to get it running, but to prove which layer is broken:

- service lifecycle and service-manager state
- host package version
- plugin/package compatibility
- config drift
- model/provider runtime routing
- channel health
- task ledger health
- cron/session isolation and channel-lane ownership
- runtime performance
- command-path and update-channel assumptions
- self-update hazards when an agent updates the gateway that is running it
- supply-chain and package-integrity spot checks after plugin/npm churn

## Quick workflow

1. Establish the real starting state.
   For remote multi-host updates, first prove SSH reachability to each host
   with a short timeout. If a host cannot be reached directly or through an
   available jump host, record it as a transport/access blocker instead of an
   OpenClaw update failure, because no OpenClaw command has executed on that
   host yet.

   If you are connected over non-interactive SSH, do not assume the
   login-shell `PATH` is available. First locate the binary with common install
   paths such as a package-manager prefix and `~/.local/bin/openclaw`, then
   export the correct `PATH` for the audit session.

   If the gateway process is owned by a different OS user than the SSH login
   user, run OpenClaw diagnostics as the gateway service user. The SSH user can
   have no `openclaw` on PATH, or a private package-manager shim can be
   unreadable, while the LaunchAgent/systemd service is healthy under another
   home directory. Derive the service user, state dir, CLI path, and port from
   the live process/service definition before running `doctor` or editing
   config.

   Check:
   - `openclaw --version`
   - `openclaw update status`
   - `openclaw status --deep`
   - `openclaw doctor --non-interactive --no-workspace-suggestions`
   - `openclaw channels status --deep`
   - `openclaw tasks audit`
   - current model routing: agent defaults, agent-level model maps, fallback chains, and cron payload models
   - recent successful sessions for the primary model and runtime, not just the display model name

2. Verify the gateway is actually managed correctly.
   Look at service-manager state, running PID, and `/health`.
   Derive the service label/name and gateway port from `openclaw status --deep`
   and/or the service definition instead of guessing them.
   Do not trust only one of:
   - the host's service manager
   - process list
   - health endpoint

   It is common to have:
   - a service definition present but not loaded
   - a detached gateway process still serving traffic
   - the service manager and the live process disagreeing

3. Separate bundled plugins from globally installed plugins.
   First inspect plugin health:
   - `openclaw plugins doctor`
   - `openclaw plugins list --json`
   - `openclaw plugins inspect <id>`

   Important rule:
   - If a capability is supposed to be bundled, verify whether a stale global npm install is shadowing it.
   - If a capability is not bundled, check npm and ClawHub before assuming config is wrong.
   - For special runtime plugins such as `codex`, compare `plugins inspect <id>`
     with `plugins list --json`; inspect can report a runtime as loaded while
     raw plugin metadata still says disabled.
   - For ClawHub/runtime plugins such as `codex`, compare the plugin version
     against the host version even when `plugins doctor` is clean. Use
     `openclaw plugins update <id> --dry-run` to see whether an official
     matching package exists before changing broader model config.

4. Check for config carried across the upgrade that no longer validates.
   Pay attention to:
   - `tools.web.search.provider`
   - `plugins.allow`
   - `plugins.entries.*`
   - model aliases and fallback chains
   - runtime mappings for `openai/*`, `openai-codex/*`, `codex`, and `pi`
   - cron job payload model refs, which can be normalized separately from agent defaults
   - update channel metadata

   If doctor says a provider or plugin is unknown, inspect the actual config file and do not assume `doctor --fix` fully cleaned it.

5. Compare plugin install records to what exists on disk.
   Inspect:
   - `~/.openclaw/plugins/installs.json`
   - `~/.openclaw/npm/node_modules/@openclaw/...`
   - `~/.openclaw/extensions/...`

   Look for:
   - recorded install paths that do not exist
   - recorded versions drifting from installed versions
   - ClawHub-installed runtime plugins under `~/.openclaw/extensions/<id>` that
     load successfully but lag the host cohort
   - npm install records where `resolvedSpec`, integrity, and installed version
     are exact, but the stored `spec` is still a bare package name such as
     `@openclaw/discord`
   - package specs rewritten or preserved during `openclaw update --channel ...`
   - external plugins that lack a release for the selected channel and were
     installed from a fallback tag such as `@latest`
   - source-only TypeScript plugin packages with no compiled `dist/`
   - plugin runtime deps removed from third-party plugin directories

6. Inspect recent gateway logs before changing too much.
   Read:
   - `~/.openclaw/logs/gateway.log`
   - `~/.openclaw/logs/gateway.err.log`
   - `/tmp/openclaw/openclaw-YYYY-MM-DD.log`

   Prioritize recent startup lines and warnings involving:
   - plugin load failures
   - config validation
   - provider fallback attempts and primary-route auth or module failures
   - update lifecycle messages such as service stop fallbacks,
     config overwrites/backups, and service reload timing
   - channel auth (if a channel returns 401/auth-failure post-update, inspect `~/.openclaw/service-env/*.env` for token-line quote corruption — see Pattern #23 — before assuming the upstream credential was rotated)
   - context-engine fallback
   - active-memory timeouts
   - event loop degradation
   - task restart blocking
   - transient post-restart UI/websocket scope errors that clear after the
     gateway is ready

7. Audit runtime/task health after the upgrade.
   Check for:
   - stale running tasks
   - lost tasks
   - delivery failures
   - timestamp inconsistencies
   - cron jobs whose persisted `sessionKey` points at a live channel lane
     such as `agent:<agent>:discord:direct:*` despite `sessionTarget: isolated`

   A successful package update can still leave the system unhealthy if stale tasks block restarts or keep the audit red.

8. Prove the primary model route, not just overall agent success.
   Run a narrow direct agent smoke test with a fresh session id and inspect the returned metadata:
   - final provider and model
   - runtime or harness id
   - `fallbackAttempts`
   - provider auth errors
   - module load errors
   - schema validation errors

   Treat `status: ok` as insufficient if the primary model failed and a fallback provider completed the run.
   Treat a clean `plugins doctor` as insufficient for runtime plugins until a
   fresh direct agent run proves that the intended harness can load and execute.

9. If the update was initiated from inside OpenClaw, audit it as a special risk.
   An OpenClaw agent can sometimes update the package it is running under, but
   that path has repeatedly left hosts with the package changed and the managed
   service unloaded or not restarted. From an outside SSH shell, verify:
   - whether the requested version actually installed
   - whether the managed service is loaded/running after the update
   - whether the gateway `/health` endpoint and channels recovered
   - whether a fresh `openclaw gateway restart` repairs an installed-but-unloaded
     service without any further package changes

   Do not treat the agent conversation's final message as authoritative. Trust
   the post-update host state.

10. Test at least one representative cron path.
   Check:
   - cron payload model counts
   - model counts by `agentId` so temporary provider workarounds can be
     rolled back without flattening full-size and mini cron routes together
   - persisted `sessionKey` values, especially channel/direct-message keys on
     isolated cron jobs
   - named or high-value cron job status
   - manual `cron run` behavior
   - whether `--expect-final` actually waits for final completion on the current build
   - recent run history for the specific job id, not only current job state,
     so stale last-run errors are separated from active regressions

   If cron verification only proves enqueue, state that clearly in the handoff notes.

11. Run a targeted npm/plugin supply-chain spot check when plugin installs changed.
   This is especially important after a failed plugin install, external plugin
   fallback, or public npm compromise advisory. Check:
   - whether `openclaw security audit --deep` flags unpinned npm plugin specs
     after plugin update churn
   - exact installed package versions against the advisory list
   - plugin install roots such as `~/.openclaw/npm/node_modules`
   - global OpenClaw/npm roots such as `/opt/homebrew/lib/node_modules`
   - obvious malicious lifecycle hooks in `package.json`
   - persistence artifacts named by the advisory
   - lockfiles and config files for strong IoCs

   State the limits of the check: a live-system scan cannot prove a package was
   never installed and removed earlier.

12. Re-run the narrowest fix, then verify again.
   Common fix sequence:
   - stop gateway cleanly
   - update host package
   - refresh plugin registry if needed
   - repair or update broken plugin installs
   - restart gateway
   - re-run `doctor`, `plugins doctor`, `status --deep`, `channels status --deep`, and `tasks audit`

## Where to look first

Use this order when diagnosing post-update failures:

- Service state: service manager, PID, `/health`
- Host version: `openclaw --version`
- Plugin mismatch: `openclaw plugins doctor`
- Config drift: `openclaw doctor`
- Channel reality: `openclaw channels status --deep`
- Task ledger: `openclaw tasks audit`
- Model/runtime route reality: direct smoke metadata and fallback attempts
- Runtime symptoms: gateway logs

## When to open references

Start with this file first.

Open [references/failure-patterns.md](references/failure-patterns.md) when:

- `doctor` or `plugins doctor` points to a known-looking regression
- `channels status` or logs disagree with the apparent service health
- plugin installs, install records, or config state do not match what is on disk
- the update completed, but the host is still slow, disconnected, noisy, or half-broken

Use the reference file for symptom matching and concrete examples after the main workflow has narrowed the likely failure area.

## Bundled vs external plugin rule

Do not assume a broken plugin means "plugin missing."

There are three common cases:

- Bundled plugin exists in the host package, but stale config still points at an old provider/plugin id.
- Bundled plugin exists, but a globally installed npm plugin shadows it and is on the wrong version.
- Plugin is not bundled, so the fix is to inspect npm or ClawHub and reconcile install records.

A channel plugin is a good example of the second case: a host can upgrade correctly while still loading an older globally installed plugin package.

If the feature is not bundled, check npm and ClawHub before rewriting config.

## Fixing mindset

Prefer the smallest fix that makes state consistent again:

- refresh registry before reinstalling everything
- update one stale plugin before removing all plugins
- inspect the actual config file when helper commands appear to succeed but warnings remain
- verify whether a third-party plugin needs local runtime deps before deleting plugin-side `node_modules`

Do not stop at "service is up." A good finish means:

- the right version is installed
- the gateway is managed correctly
- channels are connected
- the intended primary model route succeeds without an unexpected fallback
- cron payload models and representative cron jobs are healthy
- plugin doctor is clean or explained
- task audit is not carrying a fresh blocking error

## Handoff notes

If the upgrade exposed an OpenClaw bug rather than local drift, collect enough information for the next operator or project/support contact. Do not assume the user has any particular external account or wants a public report created.

- exact version before and after
- relevant config keys
- primary model route before and after, including runtime id
- direct smoke result metadata, especially `fallbackAttempts`
- cron model map before and after any temporary workaround, including mini
  routes and inherited/default model cases
- exact first bad cron run timestamps from `openclaw cron runs --id <id>`,
  not just the time the operator noticed the issue
- any cron `sessionKey` values that crossed channel/session boundaries, after
  replacing channel ids and account ids with placeholders
- plugin source path actually loaded
- installed package version and file layout for any failing npm plugin
- whether the plugin was bundled or globally installed
- gateway OS service user and command path when they differ from the SSH user
- exact update command and selected channel
- whether external plugins used channel-specific versions or fallbacks
- service stop/restart messages, especially if the service manager needed a fallback stop/unload path
- `doctor`/`plugins doctor` warning text
- the specific log lines around startup failure or restart

Sanitize handoff notes before sharing externally:
- remove hostnames, usernames, IPs, machine names, tokens, account ids, channel ids, and personal job names
- replace local paths with placeholders such as `<state>`, `<global-openclaw>`, and `~/.openclaw`
- summarize private prompt/session contents instead of quoting them
- keep exact version numbers, package names, model ids, runtime ids, and error classes when they are needed to reproduce the bug

For concrete regression patterns and example symptoms, read [references/failure-patterns.md](references/failure-patterns.md).

## Updating this skill

When another operator or agent learns something new from a different OpenClaw host:

- do not delete existing workflow steps unless they are clearly wrong
- do not replace an existing failure pattern with a narrower one
- prefer additive updates over rewrites
- add new regression patterns to `references/failure-patterns.md`
- only tighten the main workflow in this file if the new lesson changes the recommended audit order for most hosts

If a new finding is host-specific or uncertain, add it as a new failure pattern with:

- symptom
- what to inspect
- why it matters

Do not silently erase older patterns just because the current host did not hit them.
