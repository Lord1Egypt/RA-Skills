# Baton resilience policy

## Retry ladder

Maximum three attempts per subtask unless the user authorises more.

1. Same model/agent with precise correction prompt.
2. Stronger tier or specialist agent; include validator findings.
3. Strongest appropriate selected model; reduce scope and request minimal verifiable output.

## Failure classes

- `schema_error`: malformed or missing output fields.
- `tool_unavailable`: required tool absent.
- `rate_limited`: provider/model load or 429.
- `timeout`: child exceeded expected runtime.
- `safety_block`: dangerous or disallowed action.
- `evidence_conflict`: sources or children disagree.
- `capability_mismatch`: selected model lacks context/tool/vision/reasoning ability.

## Stop conditions

Stop and report partial progress when tools/config are unavailable, repeated validation fails, rate limits prevent safe fan-out, child outputs conflict without resolution, or the remaining action requires explicit user confirmation.
