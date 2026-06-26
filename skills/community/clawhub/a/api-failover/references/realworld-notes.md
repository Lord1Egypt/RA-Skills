# Real-world setup notes

Use `config-realworld-example.yaml` as the starting point when wiring this skill into an actual environment.

## Current validated setup in this workspace

This workspace now has a working local failover endpoint backed by the current OpenClaw model provider config.

### Local endpoint

- Base URL: `http://127.0.0.1:4010/v1`
- Chat endpoint: `POST /chat/completions`
- Health endpoint: `GET http://127.0.0.1:4010/health`
- Service name: `api-failover.service`

### Current primary route

- Provider: `custom-ai-td-ee`
- Base URL: `https://ai.td.ee/v1`
- Default model: `gpt-5.4`
- Credential source: inherited from `/root/.openclaw/openclaw.json`

### Current fallback routes

- `anthropic` — configured, but not usable until `ANTHROPIC_API_KEY` is provided
- `openrouter` — configured, but not usable until `OPENROUTER_API_KEY` is provided
- `local` — configured, but not usable until a local OpenAI-compatible backend is actually listening (currently expected Ollama on `127.0.0.1:11434`)

## Current scope and boundary

This layer manages whatever providers the user has actually configured.

That means:
- if the user currently has one provider, the system mainly behaves as single-provider intelligent routing plus model downgrade
- if the user later adds more providers, the same layer naturally extends to real multi-provider failover
- the system does not invent providers or credentials that do not exist

In the current workspace, the user effectively has one active provider:
- `custom-ai-td-ee`

So the currently validated behavior is:
- automatic task/profile routing
- model-aware downgrade within the active provider
- provider failover framework ready for future providers

## Current profile semantics in this workspace

These profiles now mean something concrete.

### `default`
Use the strongest normal route first, then degrade within the same provider before crossing providers.

Current order:
1. `custom-ai-td-ee / gpt-5.4`
2. `custom-ai-td-ee / gpt-5.4-mini`
3. `custom-ai-td-ee / gpt-5.4-nano`
4. `anthropic / claude-opus-4-6`
5. `openrouter / anthropic/claude-sonnet-4`
6. `local / qwen2.5:latest`

### `cheap`
Prefer cheaper routes up front.

Current order:
1. `custom-ai-td-ee / gpt-5.4-mini`
2. `custom-ai-td-ee / gpt-5.4-nano`
3. `openrouter / openai/gpt-4o-mini`
4. `local / qwen2.5:latest`

### `critical`
Prefer highest-quality cross-provider route first, but still degrade safely.

Current order:
1. `anthropic / claude-opus-4-6`
2. `custom-ai-td-ee / gpt-5.4`
3. `custom-ai-td-ee / gpt-5.4-mini`
4. `openrouter / anthropic/claude-sonnet-4`
5. `local / qwen2.5:latest`

### `code`
Prefer code-specialized models first.

Current order:
1. `custom-ai-td-ee / gpt-5-codex`
2. `custom-ai-td-ee / gpt-5.3-codex`
3. `custom-ai-td-ee / gpt-5.4-mini`
4. `local / qwen2.5:latest`

## Automatic and hinted profile selection

Profile selection now follows this priority:

1. `X-Failover-Profile`
2. request body control fields
3. `X-Task-Type` and `X-Quality`
4. automatic content-based inference
5. default fallback profile

### Supported explicit routing headers

#### `X-Failover-Profile`
Hard override.

Examples:
- `cheap`
- `default`
- `critical`
- `code`

#### `X-Task-Type`
Intent hint.

Supported values:
- `code`
- `coding`
- `programming`
- `chat`
- `general`
- `analysis`
- `critical`
- `security`

#### `X-Quality`
Quality/cost hint.

Supported values:
- `cheap`
- `fast`
- `balanced`
- `default`
- `best`
- `high`

### Supported request body control fields

The proxy now also accepts routing hints inside the JSON body.

Supported shapes:

```json
{
  "failover": {
    "profile": "code",
    "task_type": "analysis",
    "quality": "best"
  }
}
```

```json
{
  "meta": {
    "task_type": "chat",
    "quality": "cheap"
  }
}
```

```json
{
  "metadata": {
    "taskType": "analysis",
    "quality": "best"
  }
}
```

Current behavior:
- `failover.profile` can directly force a profile from the body
- `task_type` / `taskType` + `quality` can act as body-level hints
- headers still override body hints
- internal control fields are stripped before upstream forwarding

### Current hint combination behavior

- `X-Task-Type: code` + `X-Quality: best` → `code`
- `X-Task-Type: code` + `X-Quality: cheap` → `cheap`
- `X-Task-Type: analysis` + `X-Quality: best` → `critical`
- `X-Task-Type: chat` + `X-Quality: cheap` → `cheap`
- quality-only hints map directly if no task-type is present

If you do not send any of those headers or body fields, the HTTP proxy does a lightweight auto-classification.

Current rules:
- obvious code / stack traces / code keywords / fenced blocks → `code`
- obviously important / security / legal / production / incident-like wording → `critical`
- very short or obviously low-cost tasks like quick summary/rewrite/translate → `cheap`
- everything else → `default`

The response `_failover` metadata now includes:
- `profile`
- `profile_source` (`explicit`, `body-hint`, `hint`, or `auto`)
- `profile_reason`

## Failure behavior

When every route fails, the proxy now returns a cleaner service-style failure payload instead of only raw low-level errors.

Current failure body includes:
- `error`
- `user_message`
- `summary`
- `_failover.attempts`

Typical `summary` fields:
- `providers_tried`
- `error_counts`
- `last_errors_by_provider`

Example user-facing message:
- `当前已配置的模型路由暂时都不可用，请稍后再试或检查 provider 配置。`

This means OpenClaw or any client above the proxy sees a readable degraded failure instead of a wall of internal trace-like detail.

## Suggested provider order

For a typical OpenClaw-style setup:
1. primary OpenAI-compatible endpoint
2. Anthropic backup for high-value tasks
3. OpenRouter backup for ecosystem breadth
4. local Ollama for emergency or cost-control fallback

## Environment variables

Set provider credentials with environment variables instead of hard-coding them in config files.

Example:

```bash
export PRIMARY_API_KEY=...
export ANTHROPIC_API_KEY=...
export OPENROUTER_API_KEY=...
export OLLAMA_DUMMY_KEY=dummy
```

In this workspace, the primary route is intentionally different:
- primary API key is currently inherited from OpenClaw config
- only secondary providers still depend on environment variables

## HTTP proxy mode

Use `scripts/http_proxy.py` to expose a single local endpoint.

Example:

```bash
python3 scripts/http_proxy.py \
  --config references/config-realworld-example.yaml \
  --host 127.0.0.1 \
  --port 4010
```

Then send OpenAI-compatible chat requests to:
- `POST /v1/chat/completions`

Optional per-request profile override:
- header: `X-Failover-Profile: cheap`
- header: `X-Failover-Profile: critical`
- header: `X-Failover-Profile: code`

Optional intent/quality hints:
- header: `X-Task-Type: code|chat|analysis|critical|security`
- header: `X-Quality: cheap|balanced|best`

Or put them in the body under:
- `failover`
- `meta`
- `metadata`

Health/state endpoint:
- `GET /health`

## Service operations

Check service status:

```bash
systemctl --user status api-failover.service
```

Restart service:

```bash
systemctl --user restart api-failover.service
```

Stop service:

```bash
systemctl --user stop api-failover.service
```

## Quick validation commands

### Health check

```bash
curl -s http://127.0.0.1:4010/health | jq
```

### Minimal chat check

```bash
curl -s http://127.0.0.1:4010/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Reply with exactly: ok"}],
    "max_tokens": 16,
    "temperature": 0
  }' | jq
```

### Body-controlled code route

```bash
curl -s http://127.0.0.1:4010/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "Reply with exactly: ok"}],
    "failover": {"profile": "code"},
    "max_tokens": 32,
    "temperature": 0
  }' | jq
```

### Body-controlled cheap route

```bash
curl -s http://127.0.0.1:4010/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role": "user", "content": "普通聊天内容"}],
    "meta": {"task_type": "chat", "quality": "cheap"},
    "max_tokens": 32,
    "temperature": 0
  }' | jq
```

## Integration pattern

Point tools that expect an OpenAI-compatible base URL at the local proxy, and let the proxy decide which real backend to call.

For clients that require an API key field even for local endpoints, use any placeholder unless the client enforces upstream auth itself.

## Current limitations

- Minimal schema translation only
- No streaming support yet
- No provider-specific advanced parameters passthrough guarantees
- State is stored in a local JSON file, not Redis/DB
- Secondary fallback providers are configured but not yet fully activated in this workspace
- Automatic profile selection is heuristic, not a learned classifier
