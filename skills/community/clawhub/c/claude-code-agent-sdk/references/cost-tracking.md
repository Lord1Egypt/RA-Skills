# Tracking Costs and Usage

> Track token usage, estimate costs, and configure prompt caching.

## Key Concepts

- **`query()` call**: One invocation of the `query()` function, may involve multiple steps, yields one [`result`] message at the end
- **Step**: A single request/response cycle, each step yields an assistant message with token usage
- **Session**: A series of `query()` calls linked by a session ID (using `resume` option), each call reports its own costs independently

⚠️ `total_cost_usd` / `costUSD` is a **client-side estimate**, not authoritative billing data. The SDK calculates locally from a price table bundled at build time. Use for development insights and rough budgeting, not for billing end users.

## Getting Total Query Cost

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({ prompt: "Summarize this project" })) {
  if (message.type === "result") {
    console.log(`Total cost: $${message.total_cost_usd}`);
  }
}
```

```python
from claude_agent_sdk import query, ResultMessage

async def main():
    async for message in query(prompt="Summarize this project"):
        if isinstance(message, ResultMessage):
            print(f"Total cost: ${message.total_cost_usd or 0}")
```

## Tracking Per-Step Usage

Each assistant message contains a nested `BetaMessage` (TypeScript: `message.message`) with an `id` and `usage` object.

⚠️ Parallel tool calls produce multiple assistant messages sharing the same `id` and `usage`. **Always deduplicate by ID**.

```typescript
const seenIds = new Set<string>();
let totalInput = 0, totalOutput = 0;

for await (const message of query({ prompt: "..." })) {
  if (message.type === "assistant") {
    if (!seenIds.has(message.message.id)) {
      seenIds.add(message.message.id);
      totalInput += message.message.usage.input_tokens;
      totalOutput += message.message.usage.output_tokens;
    }
  }
}
```

## Breakdown by Model

Result messages include `modelUsage` (TypeScript) / `model_usage` (Python), mapping model names to token counts and costs per model.

```typescript
for await (const message of query({ prompt: "..." })) {
  if (message.type !== "result") continue;
  for (const [modelName, usage] of Object.entries(message.modelUsage)) {
    console.log(`${modelName}: $${usage.costUSD.toFixed(4)}`);
    console.log(`  Input: ${usage.inputTokens}, Output: ${usage.outputTokens}`);
    console.log(`  Cache read: ${usage.cacheReadInputTokens}`);
    console.log(`  Cache creation: ${usage.cacheCreationInputTokens}`);
  }
}
```

## Aggregating Costs Across Multiple Calls

Each `query()` call returns its own `total_cost_usd`, aggregate them yourself:

```typescript
let totalSpend = 0;
for (const prompt of prompts) {
  for await (const message of query({ prompt })) {
    if (message.type === "result") totalSpend += message.total_cost_usd;
  }
}
console.log(`Total spend: $${totalSpend.toFixed(4)}`);
```

## Cache Tokens

The SDK automatically uses prompt caching. The usage object contains two cache fields:
- `cache_creation_input_tokens`: Creating a new cache entry (billed at a higher rate)
- `cache_read_input_tokens`: Reading from an existing cache (billed at a reduced rate)

### Extending to 1 Hour TTL

Set the environment variable `ENABLE_PROMPT_CACHING_1H=1`. The 1-hour TTL has a higher write rate but greater read savings. Claude subscribers automatically get 1-hour TTL.

## Notes

- Both success and error result messages contain `usage` and `total_cost_usd`
- Messages with the same ID may occasionally have different `output_tokens` — use the highest value
- The `total_cost_usd` in result messages is more reliable than summing yourself