# Prompt — Cost Control

## Purpose

A reusable prompt to enforce **cost discipline** on every Claude call: tight `max_tokens`, cheapest viable model, caching, batching, and token estimation. Claude calls are billed per token — this prompt prevents runaway spend.

## Reusable template

```
Before issuing this Claude request, enforce cost control:

Task: {{task_description}}
Expected output size: {{expected_output}}     # e.g. "a single JSON object, ~50 tokens"
Reuse of context: {{context_reuse}}           # none | repeated_large_prefix
Interactivity: {{interactivity}}              # interactive | bulk_offline

Apply these rules and report the final request plan:
1. Choose the cheapest model that meets quality (default claude-haiku-4-5).
2. Set max_tokens = smallest value that fits {{expected_output}}.
3. If {{context_reuse}} == repeated_large_prefix, add cache_control:{type:ephemeral}
   on the stable system/context blocks.
4. If {{interactivity}} == bulk_offline, route through Batches
   (anthropic_request -> POST /messages/batches) for ~50% savings.
5. For large prompts, run anthropic_count_tokens first to estimate input cost.
6. Do not enable extended thinking unless the task genuinely needs it.

Output: model, max_tokens, caching plan, batch decision, and estimated tokens.
```

## Variables

| Variable | Meaning |
|----------|---------|
| `{{task_description}}` | What the request does. |
| `{{expected_output}}` | Size/shape of the answer (sets `max_tokens`). |
| `{{context_reuse}}` | Whether a large prefix repeats (caching). |
| `{{interactivity}}` | Interactive vs. bulk offline (batching). |

## Example (filled)

```
Task: Extract invoice total and date from each of 10,000 documents.
Expected output: one small JSON object (~40 tokens)
Reuse of context: repeated_large_prefix   (same extraction instructions)
Interactivity: bulk_offline
```

Plan: **claude-haiku-4-5**, `max_tokens: 64`, cache the instruction prefix with `cache_control`, route via **Batches** (~50% off), estimate with `anthropic_count_tokens` on a sample.

## Bad

> Request: `{ "model": "claude-opus-4-8", "messages": [...] }` (no `max_tokens`), sent one at a time, with the full instructions repeated uncached.

Missing `max_tokens` → 400; Opus on a simple extraction → expensive; no caching, no batching → maximal cost.

## Good

> Request: `{ "model": "claude-haiku-4-5", "max_tokens": 64, "system": [{ "type": "text", "text": "<instructions>", "cache_control": { "type": "ephemeral" } }], "messages": [...] }`, submitted via `/messages/batches`.

Cheapest model, tight cap, cached prefix, batched for 50% savings.
