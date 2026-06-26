# AgentSentinel For OpenClaw

AgentSentinel `v0.1.2` is packaged for OpenClaw as a local-first safety layer:

- local policy checks by default
- local budget tracking by default
- optional cloud sync when `AGENT_SENTINEL_API_KEY` is present
- self-contained with `python3`

This skill is one part of the broader AgentSentinel product:
- the OpenClaw skill for lightweight local-first control
- the AgentSentinel SDK for Python agent instrumentation
- the AgentSentinel platform for dashboards, approvals, and centralized monitoring

## Why This Release

This release is designed to be more plug and play for OpenClaw and ClawHub:

- no required SDK install for local mode
- no automatic outbound network activity
- no API key persistence to `.env`
- cloud mode uses an explicit direct HTTP call to AgentSentinel only when `sync` is run
- clearer disclosure of optional remote behavior

## Quick Start

Initialize local mode in a workspace:

```bash
python3 sentinel_wrapper.py --bootstrap
```

Check an action before running it:

```bash
python3 sentinel_wrapper.py check --cmd "rm -rf build" --cost 0.05
```

Inspect current local status:

```bash
python3 sentinel_wrapper.py status
```

Reset the local run budget:

```bash
python3 sentinel_wrapper.py reset --scope run
```

Reset all local tracked spend:

```bash
python3 sentinel_wrapper.py reset --scope all
```

Upload local events to the cloud:

```bash
python3 sentinel_wrapper.py sync
```

## Local Mode

Local mode requires only `python3`.

State is stored under:

```text
.agent-sentinel/openclaw_state.json
```

Policy is loaded from:

```text
callguard.yaml
```

If `callguard.yaml` is missing, the wrapper uses built-in defaults.

## Cloud Mode

Cloud mode is optional and opt-in.

To enable it:

1. Set `AGENT_SENTINEL_API_KEY`.
2. Run `python3 sentinel_wrapper.py sync` when you want to upload pending local events.

If the API key is not present, the skill stays local-only.

## SDK And Platform

This package is intentionally lightweight for OpenClaw.

If you want deeper integration, AgentSentinel also ships:
- the AgentSentinel SDK for Python agents, framework instrumentation, and richer telemetry
- the AgentSentinel platform for dashboards, approvals, and multi-agent visibility

The OpenClaw skill should feel safe and low-friction on its own, while still giving users a clean path into the larger AgentSentinel product when they need it.

## Release Checklist

Before publishing `v0.1.2`:

1. Verify the skill folder contains only source files you want published.
2. Run `python3 -m unittest discover -s skills/agent-sentinel -p 'test*.py'`.
3. Re-upload the updated skill bundle to ClawHub from `skills/agent-sentinel/`.
4. Confirm the listing description emphasizes local-first behavior.
