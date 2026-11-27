---
name: "digital-employee-onboarding"
description: "Onboard a new digital employee with a repeatable four-phase machine, Discord, skill, and responsibility setup."
---

# Digital Employee Onboarding

Use when Daniel asks to set up, migrate, rebuild, or standardise a Daniel-owned digital employee. Own the work through completion: track each phase and the remaining checks, recover from fixable failures, and continue without waiting for Daniel to direct each step. Follow the phase dependencies, but prepare model authentication early enough to make the Discord end-to-end test meaningful.

## Operating rules

- One digital employee owns one machine, its credentials, runtime configuration, and outbound identity.
- Use the current ClawHub registry-visible release for every shared fleet skill. Do not substitute a workspace, Workshop, or host-specific fork.
- Keep host-specific paths, identities, remotes, credentials, and delivery targets in local configuration or manifests, never shared skill logic.
- Perform host actions yourself over authorised SSH. If sudo needs a password, use `dr-agent-secrets` and the available `remote-sudo-secret` procedure: have Daniel enter it once through a masked prompt into a separate protected per-host file, verify permissions and sudo, and run the authorised commands yourself. Never request passwords or tokens in chat or arguments.
- Ask Daniel for a host action only if an access, masked secret entry, MFA, or other genuinely human-only step requires it; provide one bounded action and validate it. Do not request repeat approval for already-authorised routine setup or minor reversible troubleshooting.
- Maintain a compact non-secret onboarding checklist with completed, in-progress, blocked and remaining work, verification evidence, and any genuine approval gates. Give concise progress and proactively state what remains; do not make Daniel ask for the next step.
- If a test or watchdog reports a gap, treat it as a failed checkpoint, not an instruction to abandon the onboarding: investigate and correct in-scope causes, then rerun the relevant check. Preserve the failure evidence and never claim a pass without proof. Ask only when blocked by missing human input, an explicit separate rollout gate, or unavailable authority.
- Use a source-controlled installer or small chunks for generated scripts; do not require an oversized terminal paste.
- Keep Azure/source agents online as rollback until Daniel approves cutover. Never enable two agents on the same Discord identity or production schedule.

## Phase 1 — Install all tools

1. Capture a read-only host baseline: OS, CPU/RAM/disk, required binaries, OpenClaw state, user services, and Git state. Completion: the baseline identifies every missing prerequisite.
2. Locate the current `AGENT_BASELINE_APPLICATIONS.md` checklist; if the referenced file is missing, use the available verified fleet baseline and report the missing reference instead of silently assuming completeness. Install Node 24, Bubblewrap, Git, ripgrep, curl, jq, Python, Azure CLI, and required Python helpers. Completion: every required binary passes its listed verification command.
3. Configure the agent user’s npm prefix and persistent workspace environment. Make PATH configuration idempotent, then prove it in a fresh interactive login shell. Completion: user-level tools resolve once through PATH after a fresh login.
4. Install ClawHub and OpenClaw through their official installers with onboarding skipped. Completion: the CLI versions are reported and no Gateway or channel is active before Phase 2.

## Phase 2 — Set up Discord communications

1. Create or select a dedicated Discord bot identity for this employee. Do not reuse another employee’s bot identity.
2. Apply `dr-agent-secrets` from the outset, including during initial bootstrap; never wait until Phase 3 to protect credentials. Enter the dedicated Discord token through a masked prompt on the employee host and configure it as a SecretRef through supported OpenClaw commands. Preserve existing access settings and keep the bot disabled until its approved test scope is ready.
3. Configure the employee’s approved Discord scope, DM/channel policy, and requester attribution rules. Do not copy another employee’s roster, token, or delivery target.
4. Prepare model authentication as described below before asking Daniel to converse with the bot. Prove an isolated private send and receive; then prove an actual model-generated response. Keep production schedules and automated delivery disabled, explicitly disable automatic heartbeat/cron execution before the first Gateway start, and verify no unsolicited jobs ran. Completion: the dedicated identity sends and receives in its approved test scope and its configured model produces a response.

### Model credential and runtime preflight

- Ask once for the employee's own approved model credential or login method if unavailable; do not reuse another employee's credential. Distinguish an API key from a subscription/OAuth token before configuring either. Store it on the employee's host via masked entry and `dr-agent-secrets`; keep values out of chat, argv, logs, workspace, and receipts.
- Inspect the fleet's intended model and the new host's provider configuration. Install/enable the provider and required execution harness (for OpenAI Codex routes, the official matching-version `@openclaw/codex` plugin) before testing.
- For a supported API-key provider, create a file/env SecretRef with the supported configuration commands. If the Codex runtime needs an explicit auth profile, create a reference-only profile with `openclaw secrets apply` and the same SecretRef; never copy the key into a plaintext profile. For OAuth/subscription authentication, use the supported login flow instead of treating the token as an API key.
- Test the intended fleet model with a real isolated agent turn, set the intended default through a supported model-management flow, and verify a fresh session and the actual Discord path. Track incomplete execution paths in `dr-runtime-contract`; a valid key or a model catalog entry alone is not proof.

## Phase 3 — Install and configure skills one by one

1. Create the workspace, then discover and verify each needed shared skill through `openclaw skills`. Record the exact registry-visible version before installing.
2. Install one skill at a time, verify it, and apply its procedure before installing the next skill. Run `openclaw skills check` after each logical batch.
3. Install and apply the fleet foundation in this order: baseline operating standard, memory foundation, context pipeline, document intake, checkpointed implementation, secrets, runtime contract and schedule management. Respect documented employee-specific exceptions; install and apply backup only where it is approved and not retired. Install additional skills only when the employee’s approved role needs them.
   - Record Daniel's standing communication directives in the employee's `USER.md`, including a concise footer with the exact active model, files read and files updated. If runtime metadata is not already available, instruct the employee to check the current session-status tool; use `unknown` only when that check cannot verify the model and `none` where appropriate. Never substitute a configured default for the active session model. Do not rely only on a skill reference. Verify a fresh, ordinary reply without prompting specifically for the footer, compare its model with runtime metadata, and note whether existing conversation sessions have been verified separately.
   - The memory-foundation installer creates templates, not a finished startup index. Inspect the employee's existing memory and `USER.md`, then replace empty placeholder headings in `memory/always_on.md` with concise, factual standing guidance and an index of the actual memory files. Preserve existing notes, link to authoritative role and approval rules rather than inventing them, and verify that referenced files exist. Do not mark memory foundation applied just because template files were created.
4. Use `dr-agent-secrets` throughout bootstrap as well as after its installation on the employee. Use `dr-runtime-contract` for persistent runtime changes and verify every enabled execution path before declaring them complete.
5. Prove semantic memory with a live search. If an offline deep-index check is blocked by a running Gateway state owner, record that limitation separately; do not mistake it for a failed semantic search.
6. Do not install a shared skill when its required exact release is not registry-visible or its verification fails, unless Daniel explicitly authorizes a specific exception. Record the blocker or exception and verify the installed artifact against the release. Completion: installed skills are checked and use one canonical implementation, with any authorized exceptions reported.

## Phase 4 — Onboard the digital employee

1. Restore existing state only through a staged, allowlisted review. Include durable workspace policy, curated memory, intentional skills, and active automation source. Exclude env files, credentials, raw transcripts, caches, runtime logs, databases, media, generated output, and stale material.
2. Set identity, role, responsibilities, and the authorised engineer roster in the employee’s workspace/configuration. Keep the employee’s sender identity separate from the requesting engineer’s attribution.
3. Configure the approved model, local embeddings, memory indexing, and role-specific tools. Prove memory search and model capability before enabling work.
4. Replace any temporary Gateway proof process with a managed systemd user service before activation. Prove service status, loopback binding, and the approved channel connection.
5. Only when a separate backup rollout is approved and no employee-specific exception prohibits it, require a dedicated Microsoft Entra service principal for the employee and grant it least-privilege access to the approved Azure DevOps repository. Use the service principal to obtain short-lived tokens for the deterministic backup runner; use a PAT only as Daniel's explicit recorded exception. Keep tenant and application identifiers in the host manifest and client credentials in protected local secret storage.
6. Only for an approved backup rollout, create a separate backup contract with an allowlisted, source-controlled runner; a local ledger; workspace-backed systemd units; and a failure-only notification contract. Prove service-principal login with `--allow-no-subscriptions`, read access to the approved remote, a dry-run, one real commit/push, notification dry-run, unit validation, service execution, and an enabled six-hour timer. Never inherit another employee’s backup credentials, service names, or failure target.
7. Inventory all source automations before cutover. Migrate one job at a time using its file-backed manifest and fresh runtime; prove new delivery before disabling the old job. Keep schedules and automated delivery active on only one agent at a time.
8. Assign the employee’s initial tasks and responsibilities in durable workspace state. Complete a private end-to-end validation with the dedicated Discord identity.
   - Build a role-specific readiness matrix: authorised people and channels; required accounts and integrations; actual read/write permissions; expected workflows; failure handling; and escalation owner. Treat a loaded plugin or installed skill as inventory, not proof of account connectivity or working behaviour.
   - For each required workflow, run a safe, representative end-to-end test in an isolated session or approved test scope. Test at least an ordinary non-technical request, unavailable-service handling, an unauthorised disclosure or identity claim, an unapproved technical change, and scheduled-delivery limitations. Do not contact real third parties, create live schedules, send misleading messages or alter access just for a test.
   - Ensure the employee explains limitations plainly and never claims an email, event, reminder, or other action succeeded without a successful relevant tool result. Report pass, fail, blocked and untested separately, including the specific user/integration and execution path. Never call an employee fully ready for a role while its essential users, integrations, or workflows remain unverified.
9. Treat Daniel's request to onboard as authorisation for routine, bounded setup and diagnosis within the stated scope; do not ask again at every checkpoint. Obtain any required separate approval for live schedules, backup rollout, production delivery, a live Gateway not already approved, customer-facing integrations, or cutover. Reuse an existing explicit approval for the same scope. Completion: the employee has a defined identity, tested capability, durable responsibilities, and an approved activation state.

## Completion receipt

Report completed work and what remains in plain language, versions and checks where useful, identity and delivery scope without secrets, Gateway and scheduler state, backup status, and only the actual outstanding approval gates. Keep updating the checklist through completion; do not imply work continues after a final reply. Do not report secret values, tokens, private keys, or credential-bearing URLs.
