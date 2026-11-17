---
name: "digital-employee-onboarding"
description: "Onboard a new digital employee with a repeatable four-phase machine, Discord, skill, and responsibility setup."
---

# Digital Employee Onboarding

Use when Daniel asks to set up, migrate, rebuild, or standardise a Daniel-owned digital employee. Follow the four phases in order. Do not skip ahead because a later step looks convenient.

## Operating rules

- One digital employee owns one machine, its credentials, runtime configuration, and outbound identity.
- Use the current ClawHub registry-visible release for every shared fleet skill. Do not substitute a workspace, Workshop, or host-specific fork.
- Keep host-specific paths, identities, remotes, credentials, and delivery targets in local configuration or manifests, never shared skill logic.
- Give Daniel one bounded host action at a time and validate it before the next action. Use a source-controlled installer or small chunks for generated scripts; do not require an oversized terminal paste.
- Keep Azure/source agents online as rollback until Daniel approves cutover. Never enable two agents on the same Discord identity or production schedule.

## Phase 1 — Install all tools

1. Capture a read-only host baseline: OS, CPU/RAM/disk, required binaries, OpenClaw state, user services, and Git state. Completion: the baseline identifies every missing prerequisite.
2. Install the required baseline applications from `AGENT_BASELINE_APPLICATIONS.md`, including Node 24, Bubblewrap, Git, ripgrep, curl, jq, Python, Azure CLI, and required Python helpers. Completion: every required binary passes its listed verification command.
3. Configure the agent user’s npm prefix and persistent workspace environment. Make PATH configuration idempotent, then prove it in a fresh interactive login shell. Completion: user-level tools resolve once through PATH after a fresh login.
4. Install ClawHub and OpenClaw through their official installers with onboarding skipped. Completion: the CLI versions are reported and no Gateway or channel is active before Phase 2.

## Phase 2 — Set up Discord communications

1. Create or select a dedicated Discord bot identity for this employee. Do not reuse another employee’s bot identity.
2. Configure Discord through `openclaw channels add discord` or `openclaw configure`; enter tokens only in the local masked prompt. Prefer SecretRefs when supported.
3. Configure the employee’s approved Discord scope, DM/channel policy, and requester attribution rules. Do not copy another employee’s roster, token, or delivery target.
4. Prove a private isolated message path with the new bot. Keep production schedules and automated delivery disabled. Completion: the dedicated identity can receive and send only through its approved test scope.

## Phase 3 — Install and configure skills one by one

1. Create the workspace, then discover and verify each needed shared skill through `openclaw skills`. Record the exact registry-visible version before installing.
2. Install one skill at a time, verify it, and apply its procedure before installing the next skill. Run `openclaw skills check` after each logical batch.
3. Install and apply the fleet foundation in this order: baseline operating standard, memory foundation, context pipeline, checkpointed implementation, secrets, runtime contract, backup, and schedule management. Install additional skills only when the employee’s approved role needs them.
4. Configure protected environment or SecretRef settings only after `dr-agent-secrets` is installed. Use `dr-runtime-contract` for persistent runtime changes and verify every enabled execution path before declaring them complete.
5. Prove semantic memory with a live search. If an offline deep-index check is blocked by a running Gateway state owner, record that limitation separately; do not mistake it for a failed semantic search.
6. Do not install a shared skill when its required exact release is not registry-visible or its verification fails. Record the blocker and stop that skill’s rollout. Completion: all installed skills are registry-verified, checked, and configured using one canonical implementation.

## Phase 4 — Onboard the digital employee

1. Restore existing state only through a staged, allowlisted review. Include durable workspace policy, curated memory, intentional skills, and active automation source. Exclude env files, credentials, raw transcripts, caches, runtime logs, databases, media, generated output, and stale material.
2. Set identity, role, responsibilities, and the authorised engineer roster in the employee’s workspace/configuration. Keep the employee’s sender identity separate from the requesting engineer’s attribution.
3. Configure the approved model, local embeddings, memory indexing, and role-specific tools. Prove memory search and model capability before enabling work.
4. Replace any temporary Gateway proof process with a managed systemd user service before activation. Prove service status, loopback binding, and the approved channel connection.
5. Before any backup setup, require a dedicated Microsoft Entra service principal for the employee and grant it least-privilege access to the approved Azure DevOps repository. Use the service principal to obtain short-lived tokens for the deterministic backup runner; use a PAT only as Daniel's explicit recorded exception. Keep tenant and application identifiers in the host manifest and client credentials in protected local secret storage.
6. Create a separate backup contract with an allowlisted, source-controlled runner; a local ledger; workspace-backed systemd units; and a failure-only notification contract. Prove service-principal login with `--allow-no-subscriptions`, read access to the approved remote, a dry-run, one real commit/push, notification dry-run, unit validation, service execution, and an enabled six-hour timer. Never inherit another employee’s backup credentials, service names, or failure target.
7. Inventory all source automations before cutover. Migrate one job at a time using its file-backed manifest and fresh runtime; prove new delivery before disabling the old job. Keep schedules and automated delivery active on only one agent at a time.
8. Assign the employee’s initial tasks and responsibilities in durable workspace state. Complete a private end-to-end validation with the dedicated Discord identity.
9. Ask Daniel for approval before enabling live schedules, production delivery, a live Gateway, customer-facing integrations, or cutover from a source agent. Completion: the employee has a defined identity, tested capability, durable responsibilities, and an approved activation state.

## Completion receipt

Report the completed phase, versions and checks, installed skill versions, identity and delivery scope without secrets, active/inactive Gateway and scheduler state, backup status, and the exact next approval gate. Do not report secret values, tokens, private keys, or credential-bearing URLs.
