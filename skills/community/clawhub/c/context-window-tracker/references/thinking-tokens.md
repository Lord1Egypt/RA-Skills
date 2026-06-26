# Thinking / Reasoning Tokens

How each provider handles extended thinking and how it affects token counts.

Thinking tokens always cost money and always count against the context window. But providers report them differently:

```
Anthropic   → Bundled into input_tokens (same billing rate)
OpenAI      → Separate field: completion_tokens_details.reasoning_tokens
z.ai        → Varies by model, may bundle into input or output
```

OpenClaw's `totalTokens` always includes thinking tokens — it's the authoritative count for "how full is my window."

## Detection

The script can't detect thinking tokens from usage fields alone (they're bundled for most providers). It notes the provider's behavior in the report output:

```
Thinking: bundled into input (Anthropic)
Thinking: separate reasoning_tokens field (OpenAI)
Thinking: varies by model (z.ai)
```

For definitive detection, scan the transcript JSONL for content blocks with `"type": "thinking"`.
