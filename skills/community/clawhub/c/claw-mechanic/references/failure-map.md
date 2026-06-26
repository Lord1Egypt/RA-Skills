# Claw Mechanic Failure Map

Use this reference when the quick workflow points at a specific subsystem. Keep output evidence short and exact.

## Docs To Check

- CLI overview: `https://docs.openclaw.ai/cli`
- Doctor: `https://docs.openclaw.ai/doctor`
- Plugins: `https://docs.openclaw.ai/cli/plugins`
- Cron: `https://docs.openclaw.ai/cli/cron`
- Models: `https://docs.openclaw.ai/cli/models`
- Secrets: `https://docs.openclaw.ai/cli/secrets`
- Exec approvals: `https://docs.openclaw.ai/tools/exec-approvals`
- Gateway APIs/config: `https://docs.openclaw.ai/gateway/configuration`
- Channel behavior: check the relevant OpenClaw channel docs under `https://docs.openclaw.ai/channels/`

Docs source order:
- Record `openclaw --version` first so version drift is visible.
- Prefer installed package docs when exact installed behavior matters; use current `https://docs.openclaw.ai` for live docs and generated/API pages.
- If using a downloaded `llms.txt` docs cache, refresh it outside urgent incidents unless missing docs are blocking the repair.

## Access And Service

Symptoms:
- SSH timeout or `Permission denied (publickey)`.
- `openclaw` not found over SSH.
- Gateway healthy for user A but diagnostics fail for user B.

Look:
- `ssh -G user@host`
- `ps -ef | grep openclaw`
- `launchctl print gui/$(id -u)/ai.openclaw.gateway` on macOS
- native service manager state: launchd, systemd, Docker/Compose, supervisor, tmux/screen, or foreground shell
- `openclaw gateway status --deep`
- `openclaw config file`
- `lsof -nP -iTCP:<port> -sTCP:LISTEN`

Fix pattern:
- Classify transport/auth failures as access blockers before blaming OpenClaw.
- Run diagnostics as the same OS user that owns the gateway and state dir.
- Export a full PATH in non-interactive SSH.
- Kill/restart only the managed gateway when duplicate listeners exist.
- If a remote multi-step update disconnects mid-run, reconnect and snapshot versions/processes/listeners/logs before rerunning anything; do not blindly repeat the whole update script.
- If update output mentions the old CLI after a package swap, verify from a fresh shell plus service command path and live gateway version before rerunning the update.

## Config And Reload Safety

Symptoms:
- Gateway will not start after a config edit.
- A setting looks saved but does not affect the running service.
- Service manager restart loops after invalid config.
- `config reload skipped`, `Invalid config`, or binding validation errors appear in logs.

Look:
- `openclaw config file`
- `openclaw config validate`
- `openclaw doctor --non-interactive --no-workspace-suggestions`
- `openclaw gateway status --deep`
- Gateway config docs for hot-reload versus restart-required keys.
- Service-manager restart counts and recent stdout/stderr logs.

Fix pattern:
- Do not batch-rewrite `openclaw.json`. Use `openclaw config set` for single keys or Gateway `config.patch` with a fresh `baseHash` for structured edits.
- Back up the exact config source file first. If `$include` files are involved, edit the source include file, not a flattened copy.
- JSON5 syntax, env references, and `$include` layout can be valid config features; validate before removing them.
- Most channels, agents, models, cron, tools, bindings, session, messages, and logging changes hot-apply. `gateway.*`, `discovery`, and `plugins` usually need restart or hybrid restart handling; verify against current docs before restarting.
- On systemd or other aggressive supervisors, invalid config can cause crash loops. Stop or rate-limit the service before repair when restart churn is burning API calls or secret-provider quota.
- A single invalid binding can block gateway startup; after agent cleanup, check dangling `bindings` before reinstalling plugins or rotating tokens.
- Immediately after restart, transient Control UI scope/pricing/readiness warnings can coexist with healthy channels and successful smokes; verify final health before classifying them as active failures.
- If `gateway install --force`, package update, service repair, or PATH cleanup changes the managed runtime path, re-prove the exact runtime. Compare `gateway status --deep` ProgramArguments with a same-binary Node/Bun network probe for the affected channel/provider; a different interactive runtime or `curl` can succeed while the managed runtime times out.

## Plugins And Updates

Symptoms:
- `plugins doctor` clean but runtime still broken.
- Plugin listed but command/provider/runtime missing.
- Update changed host version but plugins lag or official plugins are unpinned.

Look:
- `openclaw plugins doctor`
- `openclaw plugins list --json`
- `openclaw plugins inspect <id> --json`
- `openclaw plugins update <id> --dry-run`
- `openclaw plugins registry --refresh` when install records and disk disagree
- `~/.openclaw/plugins/installs.json`
- `~/.openclaw/npm/...`, `~/.openclaw/extensions/...`, global npm root
- `plugins.allow`, `plugins.deny`, `plugins.bundledDiscovery`, `plugins.load.paths`, `plugins.slots.*`, `plugins.entries.<id>`
- gateway logs for plugin load/dependency errors

Fix pattern:
- Distinguish bundled plugins, global npm plugins, and ClawHub/runtime plugins.
- Verify dependency status from `plugins inspect`.
- For non-bundled plugins, verify the requested version exists in the source registry or ClawHub before reinstalling. After install, compare `plugins inspect <id>` loaded source/version, install record, and `plugins doctor`; do not assume a user-mentioned version is published.
- If a duplicate plugin ID warning appears, identify every matching manifest and the loaded source before archiving anything. If the warning points at the same canonical source and no second manifest exists, treat it as a possible diagnostic false positive.
- Use `plugins update <id-or-spec>` for routine upgrades of tracked installs. Use install `--force` only when intentionally replacing the source. Use uninstall only when removing config entries, allowlist rows, and slot assignments is acceptable.
- If `plugins.allow` is restrictive, verify bundled provider IDs and tool-owning plugin IDs are explicitly allowed; `plugins.bundledDiscovery` can change whether bundled providers bypass or obey the allowlist.
- After host updates, a plugin can load at the right version while install records remain floating or stale; pair `plugins inspect` with `security audit --deep` or install-record inspection before declaring official plugin pins clean.
- Pin/update only the plugin that evidence identifies, then rerun inspect and doctor.

## Models, Local APIs, And Secrets

Symptoms:
- Agent succeeds through fallback but intended provider failed.
- `curl /v1/models` works but OpenClaw provider route hangs or fails.
- Cron/model refs point at legacy custom providers.
- `secrets audit` reports plaintext provider keys or unresolved SecretRefs.

Look:
- `openclaw models status --json`
- `openclaw models list --provider <id>`
- `openclaw agent --session-key <fresh> --model <ref> --message "Reply with exactly OK." --json`
- Node `fetch()` probes to `/v1/models` and `/v1/chat/completions`
- `openclaw secrets audit --json`
- generated agent files: `~/.openclaw/agents/*/agent/models.json`

Fix pattern:
- Preserve working provider IDs and aliases. Add missing variants instead of duplicating entire gateways.
- For fast/no-thinking routes, use separate provider IDs or endpoints when the backend exposes them.
- Probe self-hosted providers from the exact Node binary/runtime used by the gateway, not only `curl`. If `curl` works but Node `fetch` fails, separate public egress, private model endpoint, DNS/Tailscale, and service-runtime issues before changing model config. Verify by OpenClaw agent smoke with no fallback.
- If an OpenAI-compatible route fails with a 400 tool-schema error such as an array property missing `items`, treat it as a tool/plugin schema problem that fallback may hide; capture the failing tool owner and sanitized field path.
- If multiple auth profiles exist for a provider, inspect effective profile order and recent auth errors before blaming the model backend. Pin intended profile order when OAuth/API-key rotation would make routing nondeterministic.
- Move provider API keys to SecretRefs where supported.
- Backup and regenerate/archive stale generated model catalogs only after confirming top-level config resolves providers.
- Treat retrieval separately: embedding/rerank may be healthy even when chat routes on the same provider, gateway, or local backend fail.

## Cron And Looping

Symptoms:
- Crons time out, loop, cost too much, or use unexpected expensive models.
- Jobs show `sessionTarget: isolated` but persisted keys target channel lanes.
- `cron edit --model` works but fallback lists still point at old providers.

Look:
- `openclaw cron list --all --json`
- `openclaw cron get <id>`
- `openclaw cron runs --id <id>`
- `openclaw tasks audit`
- gateway logs around scheduler wake and job run IDs

Fix pattern:
- Count enabled and disabled jobs separately.
- Count `payload.model` and `payload.fallbacks` separately; per-job `fallbacks` replaces configured fallbacks.
- Use `openclaw cron edit <id> --model <ref>` for primary model.
- Use `openclaw cron edit <id> --light-context` for cheap isolated jobs that do not need full bootstrap.
- Convert deterministic maintenance/probe jobs to command cron jobs with `openclaw cron edit <id> --command-argv '["/absolute/path/to/wrapper"]'` or `--command ...` when no model reasoning is needed. Command cron jobs run as admin-authored Gateway automation, not as model-visible `tools.exec`, so they avoid reviewer/approval churn while still recording cron history and delivery output.
- If patching payload through `cron.update`, include `payload.kind: "agentTurn"`.
- Avoid direct SQLite edits unless no CLI/RPC path exists; if used, backup first and verify through `cron get/list`.
- For jobs that still need an agent to interpret results, prefer deterministic wrapper scripts over broad interpreter grants. The prompt should run one bounded script, return `NO_REPLY` on clean state, and let runner delivery handle real alerts. Before enabling, allowlist the wrapper path if the agent will call `tools.exec`, run the script directly, then run `openclaw cron run <id> --wait --wait-timeout 10m --poll-interval 2s`; disable or roll back if the gateway restarts or the run errors.
- Do not treat a queued manual run as completed verification. Use `--wait` when supported, then confirm the specific run history/status reached a terminal `ok`.
- Do not treat `NO_REPLY` plus `not-delivered` as failure by itself. Silent tokens intentionally suppress outbound delivery. Verify `status: ok`, `consecutiveErrors: 0`, and summary before fixing delivery.

## Tasks And State Ledger

Symptoms:
- `tasks audit` reports lost sessions, stale running tasks, queued-task drift, or delivery errors.
- Gateway/plugin checks are green but sessions, crons, or restarts still look blocked.

Look:
- `openclaw tasks audit --json`
- `openclaw tasks maintenance --json`
- gateway logs around task restart blockers, delivery failures, and session cleanup

Fix pattern:
- Use `openclaw tasks maintenance --json` as preview before `--apply`.
- If audit shows only lost backing-session warnings and no stale running/queued/delivery errors, report it as historical debt unless it blocks current runs.
- Applying maintenance may prune unrelated history and may not clear lost-session records; get explicit approval before applying on a production host.

## Approvals And Reviewer

Symptoms:
- Agent asks for every command.
- Cron waits for human approval until timeout.
- Reviewer is configured but appears to fall back to humans.

Look:
- `openclaw exec-policy show --json`
- `openclaw approvals get --gateway --json`
- `tools.exec.mode`, `tools.exec.reviewer`, `safeBins`, `safeBinTrustedDirs`, `safeBinProfiles`
- logs for `exec.approval.waitDecision`, reviewer timeouts, or approval fallback

Fix pattern:
- Effective policy is the merge of requested `tools.exec.*` and host approvals.
- `ask: on-miss` is not `ask: always`; frequent prompts often mean commands miss safeBins/allowlist.
- Keep `safeBins` narrow. Interpreter/runtime tools and broad-behavior tools such as `python3`, `bash`, `node`, `jq`, `sed`, and `awk` should usually go through explicit allowlist/reviewer paths unless intentionally profiled.
- When approval volume spikes, inspect actual command forms: chained shell, redirection, command substitution, wrappers, and unallowlisted scripts can all miss allowlist even with `ask: on-miss`. Prefer command cron jobs for deterministic scheduled work, and explicit wrapper/script allowlists for agent turns that still require model reasoning; run `openclaw security audit` after changing exec policy.
- Use a fast no-thinking reviewer model only after proving the model route responds reliably.
- Compare reviewer route latency to `tools.exec.reviewer.timeoutMs`; a route that eventually succeeds after the timeout is still an approval-reviewer failure. Switch to a faster proven route before widening allowlists.

## Memory And Context Engine

Symptoms:
- Memory unavailable, embedding probes fail, context plugin falls back, or prompts are huge.
- Lossless/other context engine loaded but model overrides are denied.
- Context-engine logs show missing transcript/checkpoint/frontier warnings for generated maintenance, recall, dreaming, cron, or subagent sessions.

Look:
- `openclaw memory status --deep --json`
- gateway logs for `context-engine`, `lcm`, `embeddingProbe`, `semanticAvailable`, `vector`, `FTS`
- plugin config under `plugins.entries.<id>`
- plugin-owned state metadata, such as active conversation/session-key counts, without reading raw message bodies or secrets

Fix pattern:
- Verify all agents, not just `main`.
- Confirm provider, model, vector dimensions, semantic availability, and FTS.
- For context-engine plugins, ensure summary/expansion models are allowed by plugin `llm`/`subagent` override policy.
- If generated low-value sessions are noisy, use the plugin's documented ignore/stateless session patterns when supported, and keep productive channel sessions enabled.
- If plugin-owned state is already polluted, back up the plugin database/state first, prefer archiving or retiring generated active rows over deleting raw history, then restart and verify no new warnings.
- `openclaw sessions cleanup` repairs OpenClaw session stores/transcripts; do not assume it cleans plugin-owned context databases.
- If crons are noisy, ignore cron sessions in context-engine config when supported and use cron `lightContext`.

## Channels And Messaging

Symptoms:
- A messaging channel is connected but agents cannot reply or explicit channel actions fail.
- Doctor says channel token missing, but live channel status is connected.
- The channel shows typing/presence/logged model usage but no visible post.
- Direct messages, group/guild/workspace/channel threads, or bot-to-bot messages behave differently than expected.

Look:
- `openclaw channels status --deep --json`
- `tools.profile`, `tools.allow`, `tools.alsoAllow`, `tools.byProvider`
- service-env files when doctor shell lacks channel env vars
- channel config for direct-message policy, group/server/workspace/channel allowlists, mention requirements, delivery mode, bindings, and bot-authored message policy
- for platforms with stable numeric IDs, prefer those IDs in permission probes; display names or slugs can match at runtime while probes cannot fully verify permissions

Fix pattern:
- Trust live channel status over a bare diagnostic shell if the service has env tokens available.
- If channel-routed agents lack the message tool, add a narrow `tools.alsoAllow: ["message"]` instead of replacing `tools.allow`.
- For platform-specific message gating, check direct-message policy, sender allowlists, group/server/workspace/channel allowlists, and mention requirements before treating silence as a model failure.
- If typing/log usage occurs but nothing posts, check ambient room settings and `messages.groupChat.visibleReplies: "message_tool"` before fixing delivery.
- Some adapters ignore bot-authored messages by default; when inter-agent bot traffic is intentional, use explicit bot-allow policy plus loop protection, or separate bot/service accounts.
- In rescue/failover or multi-gateway setups, verify no two live processes are trying to own the same channel token, account, webhook, or bot identity.
- Keep direct/group policies explicit and verify connected accounts after restart.

## Security And Auth

Symptoms:
- Security audit reports no auth, token conflicts, broad safeBins, or multi-user risk.

Look:
- `openclaw security audit --json`
- `openclaw secrets audit --json`
- unauthenticated `POST /tools/invoke` or other gateway HTTP probe
- `~/.openclaw/.env`, service-env files, launchctl env

Fix pattern:
- Remove stale env tokens when config uses a SecretRef token source, but verify CLI/RPC auth still works.
- Confirm "HTTP APIs reachable without auth" with a real unauthenticated request before calling it true.
- If a channel/provider SecretRef resolves in audit but fails at runtime, compare the service runtime's provider access without printing the secret value. With explicit approval, run redacted checks for env quote corruption by printing only variable names and suspicious leading/trailing quote status.
- If Control UI auth fails while Gateway health is good, separate browser/UI token cache mismatch from server-side auth or startup failure.
- Treat multi-user/sandbox warnings as architecture risk unless the user wants a security hardening project.
