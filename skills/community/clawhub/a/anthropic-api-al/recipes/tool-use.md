# Recipe — Tool Use (Function Calling)

## Goal

Let Claude call your functions, then use the results to produce a final answer. Also the recommended path for reliable structured output.

## When

The model needs live data or actions (lookups, calculations, API calls), or you need machine-readable JSON via tool forcing.

## Inputs

- `model` — Sonnet is a good default for agentic tool use; Haiku for simple/high-volume.
- `max_tokens` — **required**.
- `tools` — array of `{ name, description, input_schema }`.
- `tool_choice` — `auto` / `any` / `tool`.
- `messages` — conversation history.

## Steps

1. Define `tools` with strict JSON `input_schema`.
2. Call `anthropic_messages` with `tools` + `tool_choice`.
3. If `stop_reason == "tool_use"`, read each `tool_use` block; **validate `input`**.
4. Execute the tool(s) in your code.
5. Append the assistant `tool_use` turn and a `user` turn with `tool_result` block(s) (matching `tool_use_id`).
6. Call again; repeat until `stop_reason == "end_turn"`.

## Output

Final assistant message with `stop_reason: "end_turn"`, or — for forced tools — a `tool_use.input` you read as structured data.

## Example

Define + first call:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 400,
  "tools": [{
    "name": "lookup_order",
    "description": "Look up an order by ID.",
    "input_schema": {
      "type": "object",
      "properties": { "order_id": { "type": "string" } },
      "required": ["order_id"]
    }
  }],
  "tool_choice": { "type": "auto" },
  "messages": [{ "role": "user", "content": "Where is order A123?" }]
}
```

Model returns:

```json
{ "content": [{ "type": "tool_use", "id": "toolu_01", "name": "lookup_order", "input": { "order_id": "A123" } }],
  "stop_reason": "tool_use" }
```

Return the result:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 400,
  "tools": [ /* same */ ],
  "messages": [
    { "role": "user", "content": "Where is order A123?" },
    { "role": "assistant", "content": [{ "type": "tool_use", "id": "toolu_01", "name": "lookup_order", "input": { "order_id": "A123" } }] },
    { "role": "user", "content": [{ "type": "tool_result", "tool_use_id": "toolu_01", "content": "{\"status\":\"shipped\",\"eta\":\"2026-06-02\"}" }] }
  ]
}
```

Final:

```json
{ "content": [{ "type": "text", "text": "Order A123 has shipped; ETA June 2, 2026." }], "stop_reason": "end_turn" }
```

## Structured output (tool forcing)

Force a tool whose schema is your target object:

```json
{ "tool_choice": { "type": "tool", "name": "extract_invoice" } }
```

Read the result from `tool_use.input`. Lower `temperature` for stability.

## Edge cases

- Multiple `tool_use` blocks → return one `tool_result` per `tool_use_id`.
- Tool failure → `tool_result` with `"is_error": true` so the model recovers.
- Untrusted `input` → validate before executing (prompt-injection risk).

## Production notes (incl. cost)

- **Cost:** each loop turn is a billed call; cap `max_tokens` each turn and minimize loop iterations.
- Cache long tool schemas / system prompts with `cache_control`.
- Prefer Haiku for high-volume, well-scoped tool tasks.
