---
name: claw-mechanic
description: Diagnose, audit, and repair OpenClaw hosts when an agent, gateway, plugin, cron, model route, memory engine, channel, approval policy, or update looks broken, expensive, slow, looping, stale, or misconfigured. Use for focused OpenClaw health checks, post-update triage, plugin update verification, model provider/API wiring audits, cron timeout/root-cause work, exec approval/reviewer problems, and rectification plans that need live proof against openclaw.ai docs instead of guesses.
---

# Claw Mechanic

Use this skill like a practical shop manual: find the failing layer, make the smallest safe repair, and prove the host is healthier after the work. Prefer targeted diagnosis over a giant everything-scan unless the user explicitly asks for a full audit or the symptom spans multiple layers.

For broad, mixed, or post-update symptoms, skim [references/root-failure-taxonomy.md](references/root-failure-taxonomy.md) first. It compresses the update runbook into root failure classes so you can choose the right proof path without loading incident-specific detail. For subsystem-specific signatures and command details, read [references/failure-map.md](references/failure-map.md) only when the symptom touches that area or the baseline points there. For repeated work on one host, use [references/host-profile-template.md](references/host-profile-template.md) to keep non-secret install facts out of the generic skill.

## Execution Context

- First classify whether you are an external operator agent or an OpenClaw-hosted agent dispatched through ACP, a channel, or cron. External agents can survive gateway restarts; OpenClaw-hosted agents may lose their own runtime when they restart or reinstall the gateway.
- When running inside OpenClaw, prefer native Gateway tools such as config, cron, and message RPCs when available, because they expose less secret material than shell commands.
- Before an in-gateway agent triggers `gateway restart`, `gateway stop`, update, or service reinstall, arrange a continuation or wake-up path for post-restart verification.

## Operating Rules

- Work on the live OpenClaw runtime, not a nearby checkout, unless the user explicitly asks for repo-only analysis.
- At intake, ask whether the user has a specific failing symptom, recent change, affected agent/channel/cron/model, or artifact/log they want prioritized. If the target or allowed change scope is unclear, ask one or two concrete questions before changing things.
- Before docs-sensitive config changes, record `openclaw --version`; prefer installed package docs when you need exact-version behavior, then current official docs at `https://docs.openclaw.ai`. Use docs for command semantics, plugin behavior, cron model/fallback behavior, approvals, secrets, and gateway APIs.
- Do not trust one green command. Pair static checks with live proof: gateway health, plugin doctor, task/cron state, model smoke, channel status, or direct endpoint probes as appropriate.
- Back up config/state before edits. Prefer `openclaw config set`, Gateway `config.patch`, or other supported CLI/Gateway RPC paths over direct file/database edits. Use direct DB/file edits only when the live API has no path, and verify by re-reading through OpenClaw afterward.
- Keep repairs small. Do not update OpenClaw, reinstall plugins, restart gateways, or rewrite model routes unless the evidence points there or the user approved that class of change.
- Separate confirmed findings from stale/historical warnings and from audit-tool false positives.
- Do not read raw secrets, env files, session bodies, or agent workspace contents unless the user approves that exact inspection. Prefer audits, redacted probes, metadata, and config paths over secret values.

## Audit Depth

- Focused audit: use when the user names one subsystem or symptom. Run the baseline plus only the relevant subsystem checks, then repair and verify that layer.
- Full audit: use when the user asks for a full/thorough audit, when recent updates changed multiple layers, when costs are unexpectedly high, when security/auth is involved, or when the first baseline shows cross-layer drift. Cover gateway, service manager, config, plugins, tasks, cron, models, memory/context, channels, approvals, secrets/security, logs, and a representative smoke test.
- When a full audit is warranted, still start with the user's symptom and recent-change answer so the audit has a priority path instead of becoming an unfocused checklist.

## Quick Workflow

1. Establish the real target.
   - Confirm SSH/reachability if remote.
   - Locate the real `openclaw` binary and state dir from the live service user.
   - Export a reliable PATH for non-interactive SSH before running diagnostics.
   - Record host, user, OpenClaw version, config file, state dir, gateway port, profile, and service manager status.

2. Capture a small baseline.
   - `openclaw --version`
   - `openclaw config file`
   - `openclaw gateway status --deep`
   - `curl -fsS http://127.0.0.1:<port>/health`
   - `openclaw config validate`
   - `openclaw plugins doctor`
   - `openclaw status --json` or `openclaw status --deep`
   - `openclaw channels status --deep`
   - `openclaw tasks audit`
   - `openclaw cron list --all --json` when cron/cost/looping is relevant
   - `openclaw models status --json` and `openclaw models list --provider <id>` when model routing is relevant
   - `openclaw secrets audit --json` when SecretRefs, generated model catalogs, or auth drift are relevant

3. Inspect the logs before guessing.
   - Read recent startup and failure lines from `~/.openclaw/logs/gateway.log`, `~/.openclaw/logs/gateway.err.log`, and `/tmp/openclaw/openclaw-YYYY-MM-DD.log`.
   - Search for the symptom words plus `plugin`, `provider`, `fallback`, `approval`, `cron`, `timeout`, `context-engine`, `memory`, `secret`, `auth`, `stalled`, and `event loop`.

4. Branch to the likely subsystem.
   - If symptoms are noisy, expensive, or post-update, classify them with the root-failure taxonomy before choosing a subsystem checklist.
   - Plugins/update: prove installed versions, install roots, dependency status, and whether bundled/global/ClawHub copies are shadowing each other.
   - Gateway/service/config: prove one managed listener, correct service user, config path, runtime binary, reload mode, health, and channel connection state after restarts.
   - Models: verify provider IDs, allowlist aliases, exact model names, SecretRefs, direct endpoint reachability, and an OpenClaw agent smoke with `fallbackUsed=false`.
   - Memory/context: run `openclaw memory status --deep`; verify embeddings, vector dims, FTS, context-engine plugin load, and model override permissions.
   - Cron: count payload models/fallbacks, identify disabled vs enabled jobs, inspect recent run history, check `lightContext`, identify deterministic agent-turn jobs that should be command cron jobs, and avoid flattening intentionally different job classes.
   - Approvals: run `openclaw exec-policy show --json` and `openclaw approvals get --gateway --json`; verify effective `ask`, `security`, reviewer model, route latency versus timeout, allowlist entries, safeBins, and reviewer timeouts.
   - Channels: use live `channels status --deep`; distinguish diagnostic-shell missing env vars from service-env tokens that are actually available.
   - Secrets/security: use `secrets audit`, `security audit`, and live HTTP auth probes. Treat "HTTP APIs reachable without auth" as unconfirmed until an unauthenticated call actually succeeds.

5. Repair only the failing layer.
   - Use `openclaw doctor --fix --non-interactive --no-workspace-suggestions` only when doctor reports safe migrations/normalizations and the user has approved repair.
   - Use `openclaw plugins update <id> --dry-run` before plugin updates; inspect plugin status again after updating.
   - Never batch-rewrite the whole `openclaw.json` unless replacement is explicitly intended. Use key-level config edits or Gateway `config.patch` with validation, and restart only when the touched keys require it.
   - Use `openclaw cron edit` for supported cron fields. For deterministic scripts or probes, prefer `cron edit <id> --command-argv ...` or `--command ...` so the Gateway scheduler runs bounded admin-authored automation without starting an isolated agent/model turn. When using Gateway RPC for payload fields not exposed by CLI, confirm method shape against current docs or `gateway call` help, back up cron state, include the intended `payload.kind`, and verify with `cron show/list`.
   - For model providers or custom routes, preserve existing provider IDs and aliases. Add missing no-thinking/fast variants without duplicating gateways or replacing working endpoints.
   - For expensive crons, prefer fast/no-thinking local routes and `--light-context` when the job does not need full workspace bootstrap.

6. Verify and report.
   - Re-run only the checks touched by the repair plus gateway health.
   - For model or harness changes, run a fresh agent smoke and inspect final provider/model, fallback attempts, runtime/harness, latency, and prompt/context size.
   - For cron changes, re-read `cron list --all`, verify enabled counts, fallback refs, `lightContext`, and recent run status; manually run only a representative safe job unless the user approves a real production run.
   - End with: changed, proof, still dirty, and next recommended action.

## Rectification Plan Template

Use this shape when the user asks for a plan rather than immediate repair:

1. Safety and access: target, service user, backup location, no-destructive boundary.
2. Baseline proof: gateway, version, plugins, tasks, channels, cron, models, secrets/security.
3. Targeted fixes: one subsection per failing layer, each with commands and rollback.
4. Verification gates: exact checks that must pass before moving to the next layer.
5. Residual risks: external backends, intentionally expensive models, stale audit warnings, manual auth/OAuth steps.

## If No Root Cause Is Found

1. State what was proven healthy and what remains unproven; do not round up uncertainty to "all clear."
2. Separate likely external dependencies from OpenClaw-controlled layers, and give the smallest safe containment option, such as disabling one cron, pinning a known-good model route, removing a broken backend from active fallbacks, or postponing a plugin update.
3. Preserve a redacted handoff bundle: version, install type, service manager, loaded plugin source/version, exact failing command or smoke test, fallback metadata, recent redacted log lines, non-secret config keys, and docs pages checked.
4. Recommend the next escalation path: current docs check, upstream issue/support report, plugin maintainer report, provider/network escalation, or a deeper read-only state audit.
5. Ask the user whether to continue deeper, apply containment, or stop with the current evidence.

## Good Defaults From Prior Incidents

- A clean `plugins doctor` is necessary but not sufficient; still check tasks, cron, model smokes, and logs.
- Remote macOS SSH often has a tiny PATH. Locate `/opt/homebrew/bin/openclaw`, `/opt/homebrew/opt/node/bin`, or `~/.local/bin/openclaw` and prepend them explicitly.
- One gateway means one managed listener on the configured port. Do not leave detached duplicate gateway processes behind.
- Service reinstalls can change the runtime binary even when the version stays healthy. Re-prove channel/provider network reachability through the exact managed Node/Bun path, not only `curl` or the interactive shell.
- Cron cost problems often come from both model routing and bootstrap context. Fix model refs and check `lightContext`.
- Recurring command friction should usually be solved at the cron payload boundary: deterministic checks become command cron jobs; agent-turn crons keep only the tools and wrapper-path allowlists they actually need.
- Model API proof should include Node/undici-style probes, not only `curl`, when OpenClaw reaches the route through Node.
- Embedding/rerank health can be independent from chat health on the same provider, local backend, or OpenAI-compatible gateway; do not mark retrieval broken just because chat routes fail.
- SecretRef cleanup is not complete until generated per-agent model catalogs and unresolved refs are clean.
- Agent workspaces are default working directories, not sandboxes; verify sandbox mode before trusting filesystem isolation.
- Silent channel failures often come from access policy, mention gating, delivery mode, or tool allowlists rather than model failure.
