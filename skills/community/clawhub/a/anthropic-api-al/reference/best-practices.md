# Reference — Best Practices

Distilled rules for using Claude well. Cost discipline is the throughline.

---

## Model choice

- **Default to `claude-haiku-4-5`.** Escalate to Sonnet, then Opus, only when a representative sample shows quality is insufficient.
- Don't use Opus for trivial tasks — it's the most expensive tier.
- Validate model IDs with `anthropic_models`.

## `max_tokens`

- **Always set it** (required) and keep it **as small as the answer needs**. It's your primary output cost cap.
- If you see `stop_reason: "max_tokens"`, the answer was truncated — raise the cap deliberately, not reflexively.

## Prompt caching

- Mark large, **stable** context (system prompt, long docs, tool schemas) with `cache_control: { "type": "ephemeral" }`.
- Keep the cached prefix byte-identical across calls; any change invalidates it.
- Verify savings via `usage.cache_read_input_tokens > 0`.
- Biggest wins: many calls sharing the same long preamble.

## Batches (~50% off)

- For bulk, non-interactive jobs (summarization, classification, evals), use `anthropic_request` → `POST /messages/batches`.
- Submit with `custom_id`s, poll, then fetch results.
- Use when latency doesn't matter and volume is high.

## Tool use

- Give each tool a clear `description` and a strict `input_schema`.
- **Validate `tool_use.input`** before executing — treat it as untrusted.
- Return one `tool_result` per `tool_use_id`; set `is_error: true` on failures so the model can recover.
- Force a tool (`tool_choice: { type: "tool", name }`) for reliable structured output.

## Token estimation

- Run `anthropic_count_tokens` before large/expensive prompts to budget cost and confirm context fit.

## Determinism / structured output

- Lower `temperature` for extraction and structured tasks.
- Prefer tool forcing over free-text JSON for machine-readable output.

## Conversation state

- The API is **stateless** — send the full `messages` history each call. Trim old turns to control input cost when history grows.

## Extended thinking

- Enable only for genuinely hard reasoning. It adds tokens; skip it for simple tasks.

## Security

- Never expose/hardcode `ANTHROPIC_API_KEY`; never echo `x-api-key`.
- Treat model output and tool arguments as untrusted; guard against prompt injection from documents and tool results.

## Reliability

- Retry only 429/5xx/529 with backoff; never retry 401/400 unchanged.
- Tune `ANTHROPIC_TIMEOUT_MS` up for long thinking calls.

## Monitoring

- Aggregate `usage` (input/output/cache tokens) to track spend.
- Alert on token spikes and on 429/529 rates.

> Verification needed: confirm pricing, caching TTL, and batch discount at https://docs.anthropic.com/en/api
