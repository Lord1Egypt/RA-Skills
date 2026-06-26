# Root Failure Taxonomy

Use this file when the host has many symptoms, just updated, or "feels broken" even though one or two checks are green. The point is to classify the root failure before reaching for detailed subsystem commands.

Each class has four parts:

- Root failure: what is usually wrong underneath the symptoms.
- Typical tells: what tends to show up first.
- Fast proof: the smallest evidence that confirms or eliminates the class.
- Mechanic move: the repair style that usually works.

## 1. Access Boundary Failure

Root failure: no OpenClaw command has run in the real target context yet. Transport, SSH auth, target username, shell PATH, or service-user context is blocking diagnosis.

Typical tells:
- SSH timeout, `Permission denied`, or commands missing only in non-interactive shells.
- Local checkout inspection finds nothing useful for a live host problem.
- The CLI runs as one OS user while the gateway runs as another.

Fast proof:
- Prove reachability and effective SSH config.
- Locate the real `openclaw` binary.
- Identify the gateway service user, state dir, and port from the live process or service definition.

Mechanic move: stop treating it as an OpenClaw fault until the real service-user context is available. Resume only after commands run against the live runtime.

## 2. Service Lifecycle Split

Root failure: service-manager state, running process, listener port, and CLI status disagree.

Typical tells:
- Health endpoint is up but the managed service is unloaded.
- Restart/update output reports failure but a detached gateway is still serving.
- Duplicate gateway processes or two listeners compete for the same role.
- A service reinstall changes the managed Node/Bun path and channels or providers fail only through the new runtime.

Fast proof:
- Compare service-manager status, process owner, listener port, `gateway status --deep`, and `/health`.
- Confirm there is one intended managed listener.
- Compare same-runtime network probes from the managed binary with `curl` and interactive-shell probes.

Mechanic move: repair lifecycle ownership first. Restart through the intended manager and remove stale duplicate processes only when they are proven detached from the managed service.

## 3. Version And Plugin Cohort Mismatch

Root failure: OpenClaw core, official plugins, external plugins, install records, and on-disk packages are not on a compatible cohort.

Typical tells:
- `plugins doctor` is mostly clean but runtime commands or providers fail.
- Bundled and globally installed copies shadow each other.
- Install records show bare specs, stale paths, or versions that no longer match disk.

Fast proof:
- Compare `openclaw --version`, `plugins doctor`, `plugins list --json`, `plugins inspect <id>`, install records, and on-disk plugin roots.
- Use plugin update dry-runs before changing state.

Mechanic move: align only the drifting plugin cohort. Keep working external plugins intact unless their API range or package state is the proven fault.

## 4. Migration Or Legacy State Drift

Root failure: old sidecars, task/cron records, plugin indexes, or SQLite migration state partially survived an update.

Typical tells:
- Doctor mentions legacy storage or ignored stale records.
- Task audit shows lost, stale running, blocked restart, or timestamp anomalies.
- Cron views disagree between files, SQLite, CLI, and Gateway state.

Fast proof:
- Run doctor without fixing, `tasks audit`, cron list/status, and targeted cron/run history.
- Inspect legacy sidecars only as evidence, not as the first edit target.

Mechanic move: use supported normalization first. If direct state surgery is unavoidable, back up files and prove the live Gateway sees the repair afterward.

## 5. Config Semantics Drift

Root failure: config still parses but its meaning changed, or an accepted field is no longer accepted by the current version/plugin.

Typical tells:
- Unknown providers, unknown plugins, broken runtime maps, stale web-search provider refs, or model aliases that resolve differently than expected.
- A default route changed, but crons or agent-level maps still use old values.

Fast proof:
- Run config validation, inspect the exact config path used by the service user, and compare with current docs.
- Check effective models and runtime maps through OpenClaw, not only the file.

Mechanic move: patch the smallest semantic mismatch. Preserve provider IDs and aliases that are still working.

## 6. Auth And Secret Precedence Conflict

Root failure: env vars, service-env files, SecretRefs, auth profiles, generated caches, or OAuth state disagree.

Typical tells:
- CLI checks fail but the service works, or the service fails while shell probes work.
- Security tools report unresolved refs, unauthenticated access, or stale generated model catalogs.
- Channel or provider auth errors appear only after restart.

Fast proof:
- Compare service env, SecretRefs, `secrets audit`, auth profiles, and a real authenticated/unauthenticated probe when relevant.
- Treat generated catalogs and per-agent caches as separate surfaces to verify.

Mechanic move: fix the effective secret source, then regenerate or restart only what needs to reload secrets. Do not rotate credentials unless evidence points to credential failure.

## 7. Runtime And Model Route Mismatch

Root failure: model names, aliases, provider IDs, runtime harnesses, fallbacks, and local API endpoints do not all point to the intended route.

Typical tells:
- Agent succeeds through fallback while the primary model fails.
- `curl` works but OpenClaw's Node provider path times out or errors.
- Retrieval models work while chat models fail, or the reverse.
- "Fast/no-thinking" and "thinking" variants are mixed in jobs where cost matters.

Fast proof:
- Run `models status`, provider model lists, direct endpoint checks, and a real OpenClaw smoke.
- Inspect final provider/model, harness, fallback attempts, latency, and prompt size.
- Include a Node/fetch-style probe for self-hosted HTTP APIs.

Mechanic move: keep one gateway and existing provider IDs where possible. Add or repair the missing route variant, then prove `fallbackUsed=false` for the intended path.

## 8. Cron, Session, And Task Lane Drift

Root failure: scheduler payloads persist their own model refs, fallbacks, context mode, and session lane independently of agent defaults.

Typical tells:
- Default model changes do not affect cron cost.
- Isolated jobs still carry channel/direct-session keys.
- Cron timeouts continue after model config looks fixed.
- Task audit is dirty while plugin and gateway checks are green.

Fast proof:
- Count cron payload models/fallbacks by job class.
- Identify deterministic shell/script jobs still stored as isolated agent turns; those are usually command cron candidates rather than approval-policy problems.
- Inspect recent run history for affected jobs, not only job definitions.
- Compare `sessionTarget`, persisted session keys, `lightContext`, task audit, and timeout lines.

Mechanic move: patch the exact job class through supported cron edit or Gateway RPC. Convert deterministic scheduled scripts to command cron jobs, and leave agent-turn crons only where model reasoning is required. Do not flatten intentionally different cron routes into one model.

## 9. Approval Policy Merge Failure

Root failure: effective exec approval behavior is stricter than intended because host policy, agent request, safe bins, trusted dirs, reviewer config, and timeout handling merge together.

Typical tells:
- The agent asks approval for every small command.
- Reviewer requests hang or time out.
- Safe commands are not treated as safe because arguments, paths, or cwd are outside the trust rule.

Fast proof:
- Compare exec policy, gateway approval config, effective `ask`, safe bins, trusted dirs, reviewer model, reviewer timeout, and recent approval logs.
- Check whether recurring approvals are really scheduled agent-turns running shell instructions; if so, fix the cron payload shape before widening exec policy.

Mechanic move: make the effective policy explicit. Use a fast reviewer model for approval review, narrow safe bins carefully, move deterministic scheduled commands to command cron jobs, and prove with one harmless command from the real working directory.

## 10. Channel Transport And Tool Policy Mismatch

Root failure: a channel is connected, but the agent's tool profile, service env, or channel policy does not allow the action path.

Typical tells:
- `channels status` looks connected but replies, message sends, or task delivery fail.
- Shell diagnostics report missing tokens while the service has tokens, or the reverse.

Fast proof:
- Compare live channel status, service env, tool profile, allowed tools, and recent delivery logs.

Mechanic move: repair the layer that owns the failure: transport auth, tool allowlist, or task delivery. Do not assume channel connection equals agent capability.

## 11. Context And Memory Pressure

Root failure: retrieval, embeddings, rerank, context-engine, memory plugin, or bootstrap budget is failing or too expensive independently of the chat model.

Typical tells:
- Huge prompts, slow crons, context-engine fallback, embedding/rerank failures, or memory timeouts.
- Chat endpoints look fine while retrieval is broken, or retrieval works while chat is irrelevant to the issue.

Fast proof:
- Run memory/context status, embedding and rerank probes, vector-dimension checks, relevant plugin logs, and a small representative agent/cron smoke.

Mechanic move: separate retrieval health from chat health. Wire embeddings/rerank first, then reduce context load with light context or route selection where appropriate.

## 12. External Backend Or Network Failure

Root failure: OpenClaw is configured correctly but a model provider, model gateway, self-hosted/local model API, messaging channel provider, GitHub, npm registry, firewall, VPN, or DNS layer is failing.

Typical tells:
- Catalog/model list succeeds but completions return 5xx or timeout.
- A firewall prompt blocks the runtime language path.
- Network probes differ between `curl`, Node, gateway service, and browser.

Fast proof:
- Isolate the upstream with the same runtime path OpenClaw uses.
- Compare host firewall, VPN/tailnet reachability, DNS, and service-user network access.

Mechanic move: keep noncritical broken backends out of active routes until fixed. Do not churn OpenClaw config when the upstream is the proven fault.

## 13. Self-Update And Restart Hazard

Root failure: an agent updated the host or plugins while depending on the gateway it was changing, leaving installed package state and running service state out of sync.

Typical tells:
- Update says done or failed ambiguously, but version, service, and health disagree.
- The agent transcript claims success while outside checks show stale or unloaded service state.

Fast proof:
- From an outside shell, verify installed version, service manager, process, `/health`, channel status, and fresh CLI diagnostics.

Mechanic move: trust the post-update host state, not the transcript. Reconcile package and service lifecycle before changing models or plugins.

## 14. Supply Chain And Install Artifact Uncertainty

Root failure: package churn, stale lock/install metadata, generated files, or advisory timing makes it unclear what was actually installed or loaded.

Typical tells:
- Security scan warnings conflict with on-disk versions.
- Plugin package metadata and install records disagree.
- Generated artifacts persist after package replacement.

Fast proof:
- Compare package metadata, lock/install records, on-disk roots, loaded plugin metadata, and advisory-specific indicators.

Mechanic move: document the evidence and uncertainty. Clean stale artifacts only after proving they are not the active loaded code path.

## Choosing The Next Checklist

- If access, service ownership, or lifecycle is unproven, fix that first.
- If one layer is green but user-visible behavior is bad, test runtime, cron, tasks, channels, and models separately.
- If cost is the symptom, prioritize cron payload models, fallbacks, context load, reviewer model, and retry/timeout loops.
- If the host just updated, prioritize plugin cohort, migration drift, service lifecycle, and self-update hazards before model rewrites.
- If local model APIs are involved, prove the exact OpenClaw runtime path, not only a generic HTTP request.
