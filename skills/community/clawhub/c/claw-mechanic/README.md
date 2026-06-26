# Claw Mechanic

A compact operator skill for diagnosing, auditing, and repairing OpenClaw hosts without guessing at the broken layer.

This skill is designed for both focused triage and full audits. It asks what changed, checks current OpenClaw docs for command-sensitive behavior, inspects the live runtime before making changes, and ends with proof of what improved or a clear escalation path when the root cause is not found.

Install or copy the whole folder so `SKILL.md`, `references/`, and `agents/` stay together.

## What it includes

- `SKILL.md`: the main diagnostic and repair workflow
- `references/root-failure-taxonomy.md`: compressed failure classes from update and repair work
- `references/failure-map.md`: subsystem-specific checks, signatures, and repair guidance
- `references/host-profile-template.md`: non-secret profile template for repeated host work
- `agents/openai.yaml`: lightweight agent metadata for skill catalogs that use it

## What it helps with

- choosing focused versus full OpenClaw audits
- finding gateway, service-manager, config, plugin, cron, task, model, memory, channel, approval, and security failures
- confirming hosted, local, or self-hosted model APIs, including embedding and reranker routes
- reducing expensive cron or agent loops by proving model routes, light context, approval policy, and run history
- repairing only the failing layer, then verifying with live checks
- preserving a redacted handoff bundle when no single root cause is found

## Who this is for

- operators maintaining OpenClaw hosts
- agents tasked with OpenClaw health checks or repair plans
- maintainers who need concise, redacted, evidence-backed debugging notes

## Install

Place the folder where your agent skills live, or install it through a compatible skill manager.

Do not copy only `SKILL.md`. The skill refers to local companion files under `references/` and `agents/`.

The main entry point is:

- `SKILL.md`

## How to use

Invoke the skill when an OpenClaw host is slow, looping, costly, stale, broken after update, or behaving differently across cron, channels, memory, model routes, plugins, or approvals.

Use a focused audit when the user names one failing subsystem. Use a full audit when the symptom spans layers, follows an update, involves unexpected cost, or the first baseline shows cross-layer drift.

## Maintenance model

Keep this skill generic. Add new lessons as root failure classes or subsystem checks, not as private host stories. Do not include hostnames, account names, IP addresses, keys, provider tokens, or raw user content.

Contribution style:

- evidence first
- root cause over incident trivia
- small repairs with verification gates
- redacted handoff notes when escalation is needed

## Suggested catalog description

OpenClaw diagnostic and repair skill for focused triage, full audits, plugin/update checks, cron/model cost control, model API verification, approvals, memory, and clear escalation paths.
