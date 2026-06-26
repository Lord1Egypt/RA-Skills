---
name: dr-schedule-manager
description: Design and implement reliable scheduled or event-triggered automations for OpenClaw agents so changes to model, prompt, delivery, and policy take effect immediately on the next run. Use when cron jobs, daily briefings, reminders, digests, or background agents keep using stale models, stale prompts, stale session state, or detached execution contexts. Also use when standardizing automation architecture across multiple agents or converting brittle time-triggered workflows into reusable config-driven jobs.
---

# dr-schedule-manager

Build scheduled automations so each run reflects current configuration immediately.

## Core outcome

This skill is a scheduling **architecture and migration playbook**, not a one-command scheduler installer.

After installation or migration, scheduled jobs should:
- pick up current prompt changes on the next run
- pick up current policy changes on the next run
- pick up current delivery changes on the next run
- pick up current default model changes on the next run, unless intentionally pinned
- avoid stale session residue from prior runs

If a design does not guarantee those properties, do not recommend it as the default.

## Current OpenClaw constraint

Treat current OpenClaw cron as **snapshot-based unless proven otherwise**.

In practice, cron jobs may embed:
- prompt text
- model override
- delivery route
- other runtime details

That means editing local files alone may **not** change the behavior of the already-registered job.

Because of this, the preferred practical pattern for current OpenClaw is not "fat job config in cron". It is:
- thin trigger in cron
- local file resolution at runtime
- explicit final delivery through the normal outbound path

## Default architecture

Prefer a **thin-trigger, fresh-run, config-driven job architecture**.

### Rule 1, scheduler is only a trigger carrier

The scheduler should only:
- wake the job
- identify the job slug or manifest
- pass a small stable trigger message

Do not embed business logic, formatting rules, or model decisions in the scheduler unless you intentionally accept snapshot behavior.

### Rule 2, manifest is the operational contract

Each scheduled job should have a manifest file that defines:
- slug
- name
- agent id
- schedule
- runtime mode
- trigger mode
- prompt file path
- policy file paths
- delivery contract
- model policy
- verification rules
- live scheduler id if your local tooling tracks one

### Rule 3, runtime assembly happens at execution time

On every run, load current files before generating output.

Always assemble from:
- current manifest
- current prompt file
- current policy files
- current delivery rules
- current model policy

Do not trust previous session state for these.

### Rule 4, delivery is explicit and provider-aware

Store delivery in a clear adapter contract.

Do not assume session metadata is valid for outbound sends if the provider requires a different target format.

### Rule 5, persistent sessions are not the source of truth

If you keep a persistent automation agent, use it only as a dispatcher or coordinator.

Do not let a persistent scheduled session be the authoritative source for:
- prompt wording
- model selection
- formatting rules
- delivery routing

## Approved patterns

### Pattern A, wake-only trigger into fresh main execution

Use when you want the latest main assistant behavior to apply automatically.

Best for:
- personal briefings
- reminders
- evolving assistant workflows

Strengths:
- changes propagate immediately
- minimal drift risk
- simple to reason about

Weaknesses:
- less isolated
- changes to main behavior affect the job immediately

### Pattern B, thin trigger plus local manifest resolution

Use as the default reusable pattern across agents for current OpenClaw.

Best for:
- reusable automation frameworks
- reports and digests
- jobs that need clean state on every run
- setups where cron otherwise snapshots prompt, model, or delivery

How it works:
- cron stores only a small stable trigger
- the triggered agent reads local job files at runtime
- prompt, policy, model policy, and delivery are resolved from the workspace
- final delivery uses the normal outbound path, not cron announce, when announce is unreliable

Strengths:
- avoids stale embedded prompt drift
- avoids stale model pins in cron payloads
- makes file edits effective on the next run
- easy to migrate across agents

Weaknesses:
- requires the agent to actually honor the trigger by reading the local files
- still depends on reliable final outbound delivery

### Pattern C, persistent dispatcher plus fresh worker run

Use for more advanced orchestration.

Best for:
- retry queues
- fan-out workflows
- multi-step automation pipelines

Strengths:
- scalable
- strong separation between orchestration and generation

Weaknesses:
- more moving parts

## Default recommendation

For most current OpenClaw scheduled jobs, use **Pattern B, thin trigger plus local manifest resolution**.

Reason:
- it works around snapshot-based cron behavior
- it is reusable across many agents
- it avoids stale embedded prompt and model drift
- changes are effective on the next run because runtime inputs are file-based
- it scales better than manual re-registration for every content tweak

## Checkpointed rollout safety

When implementing or changing real scheduled behavior, use `dr-checkpoint-implementation`.

This applies to:
- cron jobs
- reminders
- briefings
- digests
- alerting or monitoring jobs
- delivery flows
- background agents that write, notify, or mutate production state

Work in checkpoints:
1. Discover current scheduler, manifest, prompt, policy, model, session, and delivery state.
2. Design or update the manifest and file-based runtime contract.
3. Dry-run generation from current files without live delivery.
4. Test outbound delivery separately from scheduler announce behavior.
5. Test the scheduler trigger separately from content generation.
6. Calibrate timing, cooldowns, suppression, and failure behavior where alerts or notifications are involved.
7. Enable live cron delivery or production mutations only after user approval.

Self-approve routine checkpoints only when validation passes and no new live side effect is introduced.

Stop for user approval before:
- enabling or changing live cron delivery
- sending notifications, emails, or public posts
- writing or mutating production data
- changing a customer-facing schedule
- changing alert thresholds, cooldowns, or suppression behavior
- accepting weak, missing, or contradictory validation

## Model policy rules

Model behavior must be explicit.

### Preferred

Use inherit-default when upgrades should propagate automatically.

Example:

```json
{
  "modelPolicy": {
    "mode": "inherit-default"
  }
}
```

### Use only when intentionally pinned

```json
{
  "modelPolicy": {
    "mode": "pin",
    "model": "openai-codex/gpt-5.4"
  }
}
```

If pinning is used, document why.

### Shared-policy option

```json
{
  "modelPolicy": {
    "mode": "policy-file",
    "path": "automation/policies/default-runtime.json"
  }
}
```

Use when many jobs should share the same rule.

## Verification rules

Verification should catch broken assembly, not freeze intended upgrades.

Good checks:
- prompt path exists
- policy paths exist
- delivery route matches current job contract
- schedule matches manifest
- pinned model matches manifest, if pinning is intentional

Avoid exact verification for settings that are supposed to inherit current defaults.

If the job should follow current default model changes, do **not** require an exact old model string.

## Anti-patterns

Reject these by default.

### Embedded full-payload cron jobs for dynamic automations

A cron job stores the full prompt, model, and delivery configuration even though the automation is expected to evolve via local files.

### Stale exact model pinning

A manifest or cron payload hardcodes an old model and exact verification preserves it forever.

### Chat-only preference changes

A user requests a format change in chat, but the job still reads an older prompt source.

### Session-derived outbound routing

Outbound delivery copies stale or misleading session metadata rather than a provider-valid target.

### Persistent scheduled generation context

A long-lived automation session accumulates outdated assumptions and keeps using them.

### Assuming scheduler reliability equals delivery reliability

A job can resolve current local files correctly and still fail because the scheduler's announce/delivery adapter is broken.

## Migration workflow

When fixing an existing job:

1. Inspect current manifest and scheduler behavior
2. Identify stale sources
   - model
   - prompt
   - policy
   - delivery
   - session mode
   - embedded cron payloads
3. Move all durable rules into files
4. Replace fat cron payloads with a thin stable trigger
5. Choose model policy
6. Make delivery explicit
7. Reduce over-strict verification that blocks intended inheritance
8. Dry-run generation from current files without live delivery
9. Test final delivery separately
10. Test scheduler trigger behavior separately from delivery
11. Get user approval before enabling live delivery or production mutations
12. Record provider-specific quirks

## Required output when using this skill

Provide:
- recommended runtime pattern
- manifest structure
- model policy recommendation
- delivery contract recommendation
- what must move out of session state
- migration steps
- verification plan
- checkpoint plan and approval gates for rollout
- reliability risks and tradeoffs
- whether additional local execution tooling is still required

## Reliability review checklist

Before declaring the architecture good, confirm:
- a prompt edit affects the next run
- a policy edit affects the next run
- a delivery target edit affects the next run
- a default-model change affects the next run when inherit-default is used
- the scheduler stores only a thin trigger for dynamic jobs, or re-registration is explicitly part of the workflow
- no persistent session is required for content correctness
- provider-specific outbound routing is documented where needed
- final delivery works independently of cron announce delivery
- dry-run or shadow output was reviewed before live delivery
- live delivery, notifications, writes, or production mutations were explicitly approved

## References

Read `references/architecture-patterns.md` when designing the execution model.
Read `references/migration-checklist.md` when converting an existing stale scheduled job.
Read `references/reliability-review.md` before finalizing a job architecture or publishing this pattern for wider reuse.
Read `references/job-manifest-template.json` for the recommended manifest shape.
Read `references/example-migration-daily-briefing.md` for a concrete migration from a stale scheduled digest to a fresh-runtime job.
