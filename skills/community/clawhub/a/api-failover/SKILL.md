---
name: api-failover
description: Detect AI API/provider/model failures and route requests to healthy fallback providers or downgraded models. Use when creating or maintaining automatic failover, downgrade routing, provider health checks, circuit breakers, retry policy, model fallback chains, graceful degradation for LLM/API calls, or semi-automatic failover proxy deployment.
---

# API Failover

Create or improve a lightweight failover layer for AI APIs.

## Goals

Build systems that:
- detect unavailable or degraded providers/models
- classify failures before retrying blindly
- switch to a safe fallback chain
- avoid hammering broken endpoints
- recover back to preferred providers after cooldown

## Workflow

1. Identify the call path.
2. Classify failure modes.
3. Define a fallback policy.
4. Add health memory.
5. Implement guarded retries.
6. Emit observable logs.
7. Validate with forced-failure tests.

Use the detailed rules below and the bundled scripts instead of re-inventing routing logic each time.

## Practical defaults

### Error classes

Use these normalized categories:
- `AUTH_ERROR`
- `BAD_REQUEST`
- `RATE_LIMIT`
- `TIMEOUT`
- `SERVER_ERROR`
- `NETWORK_ERROR`
- `MODEL_UNAVAILABLE`
- `QUOTA_EXCEEDED`
- `UNKNOWN_TRANSIENT`

### Suggested routing behavior

- `AUTH_ERROR`, `BAD_REQUEST`: fail fast; do not retry other providers unless config explicitly maps to another credential set.
- `RATE_LIMIT`: short backoff, then fallback.
- `TIMEOUT`, `SERVER_ERROR`, `NETWORK_ERROR`, `MODEL_UNAVAILABLE`, `UNKNOWN_TRANSIENT`: retry briefly, then fallback.
- `QUOTA_EXCEEDED`: mark provider unavailable for a longer cooldown and fallback immediately.

### Circuit breaker defaults

Start with:
- open after `3` consecutive transient failures
- cooldown `60-180s`
- half-open with `1` probe
- close after `1-2` successful probes

## Configuration pattern

Keep policy in config, not hard-coded logic.

Recommended shape:
- provider registry
- task profiles with ordered fallback chains
- retry policy
- circuit-breaker policy
- per-provider overrides

## Design guidance

- Prefer fewer, well-understood providers over large fallback chains.
- Keep the fallback chain semantically compatible when possible.
- Separate "best quality" from "must return something" behavior.
- Keep downgrade rules explicit; avoid silent huge capability drops for critical tasks.
- For tool-using agents, treat provider switching as a reliability event and report it when user-visible quality may change.

## Semi-automatic deployment model

Use this skill to discover the environment, generate a production-ish config, run a local HTTP failover proxy, and verify health.

Do not claim full autonomous takeover unless the environment-specific integration is actually completed.

## References

Read these only when needed:
- `references/config-example.yaml` for a compact policy example
- `references/config-realworld-example.yaml` for a more practical multi-provider template
- `references/config-production.yaml` for a ready-to-edit production template
- `references/test-scenarios.md` for failure-injection and validation cases
- `references/realworld-notes.md` for local proxy deployment and environment-variable setup
- `references/api-failover.service` for a user-systemd service example

## Bundled scripts

### `scripts/discover_env.py`
Inspect the current environment.

### `scripts/generate_config.py`
Generate a production-ish YAML config from simple defaults.

### `scripts/failover_proxy.py`
Run a minimal CLI failover call path.

### `scripts/http_proxy.py`
Expose a single local OpenAI-compatible entrypoint.

Endpoints:
- `POST /v1/chat/completions`
- `GET /health`

Optional request header:
- `X-Failover-Profile: cheap|default|critical|local-first`

### `scripts/selfcheck.py`
Validate that the local proxy is reachable and can process a minimal chat request.

### `scripts/bootstrap_failover.py`
Run the semi-automatic bootstrap flow:
- discover environment
- generate config
- optionally start the proxy
- run self-check
- print next actions

Example:

```bash
python3 scripts/bootstrap_failover.py \
  --default-model custom-ai-td-ee/gpt-5.4 \
  --start-proxy
```

Keep these scripts small and inspectable. Extend them instead of turning SKILL.md into code-heavy instructions.
