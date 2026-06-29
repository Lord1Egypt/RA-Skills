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
- use an execution substrate appropriate to the job, instead of defaulting every scheduled reference into an LLM-backed agent run

If a design does not guarantee those properties, do not recommend it as the default.

## Current OpenClaw constraint

Treat current OpenClaw cron as **snapshot-based unless proven otherwise**.

In practice, cron jobs may embed:
- prompt text
- model override
- delivery route
- other runtime details

That means editing local files alone may **not** change the behavior of the already-registered job.

Because of this, the preferred practical pattern is not "fat job config in cron". It is:
- thin scheduler reference
- local file resolution at runtime
- explicit final delivery through the correct outbound path when delivery is needed

The scheduler reference may point to an agent runner or a non-agent runner. Choose that substrate deliberately.

## Default architecture

Prefer a **thin-reference, fresh-run, config-driven job architecture**.

### Rule 1, scheduler is only a trigger/reference carrier

The scheduler should only:
- wake the job
- identify the job slug or manifest
- pass a small stable trigger message or command reference

Do not embed business logic, formatting rules, prompt text, delivery rules, or model decisions in the scheduler unless you intentionally accept snapshot behavior.

### Rule 2, manifest is the operational contract

Each scheduled job should have a manifest file that defines:
- slug
- name
- agent id when an agent runner is required
- execution substrate
- schedule
- runtime mode
- trigger mode
- prompt file path when generation/reasoning is required
- policy file paths
- delivery contract
- model policy when an LLM is used
- verification rules
- live scheduler id if your local tooling tracks one

### Rule 3, runtime assembly happens at execution time

On every run, load current files before generating output or executing deterministic work.

Always assemble from:
- current manifest
- current prompt file when applicable
- current policy files
- current delivery rules
- current model policy when applicable
- current deterministic script/CLI configuration when applicable

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
- deterministic script configuration

## Execution substrate gate

Before choosing an approved pattern, decide whether the scheduled task needs an agent/LLM at run time.

Thin trigger means **thin stable reference**, not automatically **OpenClaw agentTurn**.

### Deterministic non-LLM jobs

If the scheduled task is a deterministic script, CLI, ETL, monitor, report generator, reconciliation job, artifact builder, or health check that does not need natural-language reasoning at run time, default to a non-agent runner.

Appropriate non-agent substrates include:
- systemd timer
- OS cron
- platform scheduler
- queue worker
- direct command runner available in the environment
- another deterministic execution substrate already approved for that host

Rules:
- The scheduler entry should point to a stable runner, wrapper, or manifest path.
- The scheduler entry must not embed the job definition.
- OpenClaw, Codex, or another LLM must not be in the hot path for high-frequency deterministic jobs.
- The deterministic runner should still load current manifest/config files at run time.

### Agent/LLM jobs

Use OpenClaw `agentTurn` or another LLM-backed agent path only when the scheduled run genuinely needs one or more of:
- agent reasoning
- natural-language generation
- tool orchestration with judgment
- conversational context
- adaptive summarization or decision-making

Even then, the payload must stay thin:
- pass only a job slug, manifest path, and small trigger message
- make the agent load current manifest, prompt, policy, delivery, and model files at runtime
- avoid embedding the full prompt, model, policy, or delivery details into the scheduler payload

### High-frequency guardrail

For frequent jobs, especially every 5-15 minutes or less, require an explicit written justification before using an LLM-backed scheduler path.

The justification should explain why deterministic execution is insufficient.

If no justification exists, choose a non-agent execution substrate.

### Substrate decision checklist

Ask:
- Does the job require natural-language generation or reasoning on every run?
- Does it require tool orchestration where judgment changes run-to-run?
- Is the output deterministic from API/file inputs?
- Is the frequency high enough that token cost or model latency matters?
- Can a script/CLI produce the artifact and only alert on exceptions?
- Does delivery require an agent, or can delivery be handled by a provider adapter or direct command?

Default answer:
- deterministic job -> Pattern B1
- agent/LLM job -> Pattern B2
- mixed job -> deterministic runner first; call an agent only for the genuinely reasoning-dependent step

## Approved patterns

### Pattern A, wake-only trigger into fresh main execution

Use when you want the latest main assistant behavior to apply automatically and the job genuinely needs an agent/LLM.

Best for:
- personal briefings
- reminders with natural-language rendering
- evolving assistant workflows

Strengths:
- changes propagate immediately
- minimal drift risk
- simple to reason about

Weaknesses:
- less isolated
- changes to main behavior affect the job immediately
- inappropriate for deterministic high-frequency jobs

### Pattern B1, thin trigger to non-agent runner plus local manifest resolution

Use as the default for deterministic scheduled jobs.

Best for:
- health checks
- ETL/sync jobs
- deterministic report generation
- monitors that poll APIs or local state
- high-frequency jobs
- jobs where the output is produced by a script or CLI without natural-language reasoning

How it works:
- scheduler stores only a small stable reference to a runner, wrapper, command, or manifest
- the non-agent runner reads local job files at runtime
- script/config/policy/delivery are resolved from the workspace or approved config path
- output artifacts, ledgers, and exit status are written for validation
- final delivery uses a deterministic delivery adapter when needed

Strengths:
- avoids LLM token spend for deterministic work
- avoids model latency and model availability risk
- avoids stale embedded prompt/model drift
- changes are effective on the next run because runtime inputs are file-based
- easy to validate with unit/integration checks and scheduler logs

Weaknesses:
- cannot perform open-ended reasoning or natural-language synthesis unless another step is added
- requires local execution tooling, scripts, and observability

### Pattern B2, thin trigger to agent runner plus local manifest resolution

Use as the default only for jobs that actually need an agent/LLM.

Best for:
- natural-language briefings and digests
- judgment-heavy summaries
- workflows that need adaptive tool orchestration
- jobs that rely on conversational context

How it works:
- scheduler stores only a small stable trigger
- the triggered agent reads local job files at runtime
- prompt, policy, model policy, and delivery are resolved from the workspace
- final delivery uses the normal outbound path, not cron announce, when announce is unreliable

Strengths:
- avoids stale embedded prompt and model drift
- avoids stale model pins in cron payloads
- makes file edits effective on the next run
- appropriate when the actual task needs an agent

Weaknesses:
- consumes LLM tokens
- introduces model latency and model availability risk
- requires stronger justification for high-frequency jobs
- still depends on reliable final outbound delivery

### Pattern C, persistent dispatcher plus fresh worker run

Use for more advanced orchestration.

Best for:
- retry queues
- fan-out workflows
- multi-step automation pipelines
- mixed deterministic and agent work

Strengths:
- scalable
- strong separation between orchestration and generation
- can route deterministic work to non-agent runners and reasoning work to agents

Weaknesses:
- more moving parts
- requires careful observability and ownership boundaries

## Default recommendation

For most current scheduled jobs, use **Pattern B1** when the job is deterministic and **Pattern B2** only when the job genuinely needs an agent/LLM.

Reason:
- both preserve the thin-reference, file-based scheduling contract
- B1 prevents high-frequency deterministic jobs from accidentally consuming LLM tokens
- B2 keeps agent-backed jobs fresh without embedding stale prompt/model/delivery payloads
- both avoid stale embedded scheduler payload drift when implemented correctly

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
1. Discover current scheduler, manifest, prompt, policy, model, session, substrate, delivery state, and registered scheduler payload.
2. Decide the execution substrate using the substrate gate.
3. Design or update the manifest and file-based runtime contract.
4. Dry-run deterministic execution or generation from current files without live delivery.
5. Test outbound delivery separately from scheduler announce behavior.
6. Test the scheduler trigger separately from content generation or deterministic work.
7. Validate the actual registered scheduler payload/substrate.
8. Calibrate timing, cooldowns, suppression, and failure behavior where alerts or notifications are involved.
9. Enable live cron delivery or production mutations only after user approval.

Self-approve routine checkpoints only when validation passes and no new live side effect is introduced.

Stop for user approval before:
- enabling or changing live cron delivery
- sending notifications, emails, or public posts
- writing or mutating production data
- changing a customer-facing schedule
- changing alert thresholds, cooldowns, or suppression behavior
- accepting weak, missing, or contradictory validation
- using an LLM-backed path for a high-frequency deterministic job without explicit justification

## Model policy rules

Model behavior must be explicit when an LLM-backed path is used.

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
    "model": "replace-with-intentional-model"
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

For deterministic non-LLM jobs, model policy should be absent or explicitly marked not applicable.

## Verification rules

Verification should catch broken assembly and wrong execution substrates, not freeze intended upgrades.

Good checks:
- prompt path exists when prompt is required
- policy paths exist
- delivery route matches current job contract
- schedule matches manifest
- pinned model matches manifest, if pinning is intentional
- registered scheduler payload is a thin reference, not an embedded full job definition
- registered scheduler payload points to the intended substrate
- deterministic jobs do not start `agentTurn` or another agent/LLM session unless explicitly justified
- LLM-backed jobs pass only slug/manifest path and a small trigger message
- artifacts, ledgers, or logs prove the selected runner loaded current files

For systemd timers, verify:
- unit file exists and points to the intended wrapper/runner
- timer file exists
- timer is active/enabled when live operation is approved
- next run is visible
- last run exit status is available
- logs or ledger/artifact output prove what ran

Keep separate validation for:
- delivery
- schedule
- manifest loading
- actual registered scheduler payload/substrate
- live side effects

Avoid exact verification for settings that are supposed to inherit current defaults.

If the job should follow current default model changes, do **not** require an exact old model string.

Do not claim OpenClaw cron can directly execute shell commands unless the runtime actually supports that. If shell execution is required, choose an OS/platform scheduler or another direct command runner.

## Anti-patterns

Reject these by default.

### Embedded full-payload cron jobs for dynamic automations

A cron job stores the full prompt, model, and delivery configuration even though the automation is expected to evolve via local files.

### Treating thin trigger as automatically agent-backed

A design says "thin trigger" but always starts OpenClaw `agentTurn`, even when the job is deterministic and could run as a script or CLI.

### High-frequency deterministic LLM polling

A deterministic monitor, health check, ETL, or report generator runs through Codex/OpenClaw every few minutes even though no run-time reasoning is needed.

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

## Anti-regression example

### Integration Platform Health Monitor, every 5 minutes

A health monitor runs every 5 minutes and executes a Python CLI that checks deterministic API and platform status.

Correct design:
- Pattern B1
- systemd timer, OS cron, platform scheduler, or approved direct command runner
- scheduler points to a wrapper or manifest-backed CLI command
- CLI loads current manifest/config files at runtime
- CLI writes a ledger/artifact with checked targets, timestamp, result, and exit status
- delivery is deterministic and separate from scheduler behavior

Incorrect design:
- OpenClaw `agentTurn` every 5 minutes
- agent starts even when the Python CLI itself contains all deterministic logic
- Codex tokens are consumed on every poll without a reasoning requirement

Escalation design:
- deterministic CLI runs every 5 minutes
- agent/LLM is invoked only for exception analysis, incident summary generation, or operator-facing natural-language report when needed

## Migration workflow

When fixing an existing job:

1. Inspect current manifest and scheduler behavior.
2. Inspect the registered scheduler payload, not just local files.
3. Identify stale sources:
   - model
   - prompt
   - policy
   - delivery
   - session mode
   - substrate
   - embedded cron payloads
4. Decide whether the job is deterministic, agent/LLM-backed, or mixed.
5. Move all durable rules into files.
6. Replace fat cron payloads with thin references.
7. Choose execution substrate:
   - B1 for deterministic jobs
   - B2 for agent/LLM jobs
   - C for mixed orchestration
8. Choose model policy only when an LLM is used.
9. Make delivery explicit.
10. Reduce over-strict verification that blocks intended inheritance.
11. Dry-run deterministic execution or generation from current files without live delivery.
12. Test final delivery separately.
13. Test scheduler trigger behavior separately from delivery.
14. Get user approval before enabling live delivery or production mutations.
15. Record provider-specific quirks and substrate validation details.

## Required output when using this skill

Provide:
- recommended runtime pattern
- execution substrate recommendation and justification
- manifest structure
- model policy recommendation, or why model policy is not applicable
- delivery contract recommendation
- what must move out of session state or scheduler payload
- migration steps
- verification plan, including registered scheduler payload/substrate checks
- checkpoint plan and approval gates for rollout
- reliability risks and tradeoffs
- whether additional local execution tooling is still required

## Reliability review checklist

Before declaring the architecture good, confirm:
- the execution substrate matches the job need
- deterministic jobs use non-agent runners unless explicitly justified
- high-frequency deterministic jobs do not consume LLM tokens in the hot path
- the registered scheduler payload is inspected and matches the intended substrate
- a prompt edit affects the next run when prompts are part of the job
- a policy edit affects the next run
- a delivery target edit affects the next run
- a default-model change affects the next run when inherit-default is used
- the scheduler stores only a thin trigger/reference for dynamic jobs, or re-registration is explicitly part of the workflow
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
