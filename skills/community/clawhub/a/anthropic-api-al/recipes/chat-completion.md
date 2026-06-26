# Recipe — Chat Completion

## Goal

Get a text response from Claude for a prompt or conversation, cheaply and correctly.

## When

Q&A, assistants, summarization, drafting, explanations — any task that returns text.

## Inputs

- `model` — start with `claude-haiku-4-5`.
- `max_tokens` — **required**; smallest value that fits the answer.
- `messages` — full conversation history.
- Optional: `system`, `temperature`.

## Steps

1. Pick the cheapest viable model (default Haiku).
2. Set `max_tokens`.
3. (Optional) Add a `system` prompt for role/constraints.
4. Build `messages` with full history.
5. Call `anthropic_messages`.
6. Read `content[].text`; check `stop_reason`; record `usage`.

## Output

```json
{
  "id": "msg_01...",
  "role": "assistant",
  "model": "claude-haiku-4-5",
  "content": [{ "type": "text", "text": "..." }],
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 24, "output_tokens": 60 }
}
```

## Example

Request:

```json
{
  "model": "claude-haiku-4-5",
  "max_tokens": 200,
  "system": "You are concise.",
  "messages": [{ "role": "user", "content": "What is idempotency in one sentence?" }],
  "temperature": 0.2
}
```

Response:

```json
{
  "content": [{ "type": "text", "text": "Idempotency means repeating an operation yields the same result as doing it once." }],
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 22, "output_tokens": 18 }
}
```

## Edge cases

- `stop_reason: "max_tokens"` → answer truncated; raise the cap deliberately.
- Long history → input cost grows; trim old turns.
- Missing `max_tokens` → `400`. Always include it.

## Production notes (incl. cost)

- **Cost:** input + output tokens are billed. Keep `max_tokens` tight; use Haiku for high volume.
- Cache a large stable `system` prompt with `cache_control` if reused across calls.
- For bulk, non-interactive chats, use Batches (~50% off) via `anthropic_request`.
- Estimate big prompts first with `anthropic_count_tokens`.
