# Architecture patterns for reliable scheduled jobs

## Design goal

A scheduled job should reflect current configuration on the very next run.

That means changes to:
- prompt
- policy
- delivery route
- default model

must be loaded at execution time, not remembered from stale session state.

## Recommended default

Use a thin-trigger, file-resolved execution path.

The scheduler should carry only a small stable trigger. The runtime then assembles the job from local files.

## Current OpenClaw reality

Current OpenClaw cron jobs may embed prompt text, model choice, and delivery details directly in the registered job.

That means cron can behave as a snapshot system unless you deliberately design around it.

For dynamic automations, do not treat the cron registration as the canonical source of truth.
Treat it as a trigger carrier.

## Pattern A, wake-only trigger into fresh main execution

Use when:
- you want the latest main assistant behavior automatically
- isolation is less important than immediate propagation

Pros:
- very low drift
- changes apply immediately

Cons:
- less isolated
- changes in main behavior can affect the job unexpectedly

## Pattern B, fresh isolated run from manifest

Use when:
- you want reusable architecture across many agents
- each run should start clean
- immediate application of file changes matters

Pros:
- predictable
- portable
- avoids stale session memory

Cons:
- requires disciplined manifests and policy files

## Pattern C, dispatcher plus fresh worker

Use when:
- orchestration complexity exists
- retries or queues matter
- multi-step automations are needed

Pros:
- scalable
- separates orchestration from generation

Cons:
- more moving parts

## Manifest recommendations

A manifest should explicitly define:
- slug
- name
- agentId
- schedule
- runtimeMode
- triggerMode
- promptFile
- policyFiles
- delivery
- modelPolicy
- verify
- live scheduler id when your local tooling keeps one

## Model policy recommendations

### Best default

```json
{
  "modelPolicy": {
    "mode": "inherit-default"
  }
}
```

Use when the job should follow system model upgrades.

### Intentional pinning

```json
{
  "modelPolicy": {
    "mode": "pin",
    "model": "replace-with-intentional-model"
  }
}
```

Only use if output stability outweighs automatic upgrades.

### Shared policy file

```json
{
  "modelPolicy": {
    "mode": "policy-file",
    "path": "automation/policies/default-runtime.json"
  }
}
```

Use when many jobs should share the same resolution behavior.

## Verification recommendations

Verification should ensure assembly correctness.

Good checks:
- manifest exists
- prompt file exists
- policy files exist
- delivery target matches policy
- schedule matches manifest
- pinned model matches manifest if pinning is intentional

Bad checks:
- exact model verification when model inheritance is intended
- exact prompt text verification when prompt changes should be allowed through file edits

## Delivery recommendations

Delivery must be explicit and provider-aware.

Example:

```json
{
  "delivery": {
    "channel": "discord",
    "target": "user:270548320366100480",
    "accountId": "default"
  }
}
```

Do not trust session metadata blindly for outbound sends.
