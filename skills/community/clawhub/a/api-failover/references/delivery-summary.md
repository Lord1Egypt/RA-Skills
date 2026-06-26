# API Failover delivery summary

This file describes the delivered state of the `api-failover` skill in this workspace.

## Delivered outcome

This skill is now delivered as an intelligent routing and downgrade layer for the providers the user has actually configured.

In the current workspace, that means:
- one active provider is present: `custom-ai-td-ee`
- the system can automatically route across multiple task profiles
- the system can automatically downgrade across multiple models inside the active provider
- the system is ready to extend to real multi-provider failover if the user later adds more providers

## What is working now

### Active runtime
- local endpoint: `http://127.0.0.1:4010/v1`
- service: `api-failover.service`
- health endpoint: `http://127.0.0.1:4010/health`

### Routing behavior
- profile-aware routing: `default`, `cheap`, `critical`, `code`
- automatic profile inference from request content
- header-based routing control
- body-based routing control
- explicit override support

### Downgrade behavior
- same-provider model downgrade is working
- code-specialized route selection is working
- failure metadata is returned in `_failover`

### Failure UX
- all-routes-failed now returns a readable `user_message`
- summary data is included instead of only raw low-level error blobs

## Current boundary

This delivery does **not** invent new providers.
It manages whatever providers the user has actually configured.

So in the current environment:
- single-provider intelligent routing is active
- real multi-provider failover is framework-ready but not activated because no second provider credentials are present

## Secondary activation readiness

The delivery includes:
- `references/api-failover.service`
- `scripts/activate_secondary.py`
- `references/activation-checklist.md`
- forced-failover drill configs

If the user later adds:
- `OPENROUTER_API_KEY`
- `ANTHROPIC_API_KEY`
- or a local backend on `127.0.0.1:11434`

then the same delivery can activate secondary routing without redesign.

## Packaged artifact

After packaging, the distributable artifact is expected at workspace root as:
- `api-failover.skill`

## Recommended final description

`api-failover` is now a delivered intelligent AI routing layer that:
- manages the user’s currently configured providers
- automatically selects task-appropriate routes
- downgrades to available models when stronger routes fail
- returns cleaner degraded failure messages when no routes are available
