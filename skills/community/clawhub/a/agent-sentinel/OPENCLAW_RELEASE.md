# AgentSentinel `v0.1.2` For OpenClaw

## Recommended Listing Title

AgentSentinel Safety Layer

## Recommended Short Description

Local-first budget and policy guardrails for OpenClaw agents, with optional cloud sync when an API key is provided.

## Recommended Long Description

AgentSentinel is the operational circuit breaker for OpenClaw agents.

This skill is the OpenClaw-facing entry point to the broader AgentSentinel product:
- the OpenClaw skill for local-first guardrails
- the AgentSentinel SDK for Python agent instrumentation
- the AgentSentinel platform for centralized dashboards and approvals

`v0.1.2` is designed to be plug and play:

- local mode works with `python3` only
- no API key is required for local budgets and policy checks
- no secret persistence to `.env`
- optional cloud functionality is unlocked by setting `AGENT_SENTINEL_API_KEY`
- cloud mode uses an explicit `sync` command instead of background upload
- remote behavior is clearly disclosed and never required for local use

Use it to:

- block destructive commands before execution
- cap spend on costly runs
- inspect remaining local budget
- reset local run state between sessions
- connect to the wider AgentSentinel platform when cloud visibility is needed

## 30-Second Quickstart

```bash
python3 sentinel_wrapper.py --bootstrap
python3 sentinel_wrapper.py check --cmd "rm -rf build" --cost 0.05
python3 sentinel_wrapper.py status
python3 sentinel_wrapper.py reset --scope run
```

Optional cloud mode:

```bash
export AGENT_SENTINEL_API_KEY=as_...
python3 sentinel_wrapper.py sync
```

## Security Positioning

Recommended trust-language for ClawHub:

- local-first by default
- cloud is optional
- API keys are not written to disk
- no automatic install step is required
- no remote sync occurs unless the user provides an API key and runs `sync`

## Recommended Tags

- safety
- security
- budget
- compliance
- governance

## Release Notes

- local-only mode now works with `python3` and no SDK install
- API keys are no longer persisted to `.env`
- cloud features are opt-in through `AGENT_SENTINEL_API_KEY` and an explicit `sync` command
- skill metadata and packaging are aligned with OpenClaw conventions
- added `reset` for local run/session control
