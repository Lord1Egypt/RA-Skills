# Cache Optimization Patterns

Prompt caching saves cost by reusing previously processed context. Most providers charge ~10% of normal input price for cache reads — up to 90% savings on repeated context.

## What Caches Well

- System prompts (static instructions, personas, rules)
- Large documents loaded repeatedly (codebases, docs, schemas)
- Repeated tool definitions
- Shared base prompts across multiple sub-agents

## What Doesn't Cache

- Dynamic content that changes every request (timestamps, random values)
- Very short prompts (not worth caching)
- One-off requests with unique context

## Key Patterns

### Keep system prompts stable
Put static instructions at the top of your system prompt. They get cached after the first request and reused on every call — avoid injecting dynamic values (timestamps, session IDs) into the system prompt.

```text
[CACHED] System prompt with rules, persona, tools
[NOT CACHED] Current user message
```

### Large document analysis
Load the document once, then ask questions in follow-up turns.

```text
Turn 1: "Here is the codebase: [large content]" → cache miss, full price
Turn 2: "What does the auth module do?"         → cache hit, ~90% cheaper
Turn 3: "Find all API endpoints"                → cache hit, ~90% cheaper
```

### Sub-agent prompts
When spawning many sub-agents with the same base prompt, put shared context first — it gets cached across all of them.

```text
[SHARED — gets cached across all agents]
You are a test fixer. Rules: never comment out tests...

[UNIQUE per agent]
Fix this specific failure: <paste failure>
```

### Order matters
Always put static content before dynamic content. Providers cache from the beginning of the prompt — anything after a dynamic section won't be cached.

## Cache Write vs Read Cost — Break-Even Math

Cache writes cost ~25% **more** than regular input tokens, but cache reads cost 90% **less**. It pays off after just 1–2 reuses.

**Formula:**
```text
break_even_reads = cache_write_cost / (regular_cost - cache_read_cost)
```

**Example — 10k token system prompt on Anthropic Sonnet:**
- Regular cost per read: 10k × $3/M = **$0.030**
- Cache write (one-time): 10k × $3.75/M = **$0.0375**
- Cache read cost: 10k × $0.30/M = **$0.003**
- Break-even: $0.0375 / ($0.030 - $0.003) = **1.4 reads**

→ Cache anything reused 2+ times. For sessions that run long (which they should), almost everything is worth caching.

## Batch API (50% Discount for Non-Urgent Tasks)

Anthropic's Batch API processes requests asynchronously at half price — results returned within 24 hours.

**Best for:**
- Cron/scheduled tasks that don't need immediate responses
- Bulk analysis (e.g. processing many files overnight)
- Background monitoring that can tolerate latency

**Not for:**
- Real-time conversations
- Any task where the user is waiting

```python
# Instead of: real-time API call at full price
response = client.messages.create(model="claude-sonnet-4-6", ...)

# Use: batch API at 50% off for non-urgent work
batch = client.messages.batches.create(requests=[...])
# Poll for results later
```

See Anthropic docs for full Batch API reference.

## Provider Cache Notes

| Provider | Cache Behavior |
|----------|---------------|
| Anthropic | Automatic on repeated prefixes; ~90% discount on cache reads |
| OpenAI | Automatic on prompts >1024 tokens; ~50% discount on cache reads |
| Google | Context caching via API; charged per cache storage + reads |

Check your provider's docs for the exact cache TTL and minimum token threshold.

## Quick Wins

1. **Stable system prompts** — biggest single win
2. **Order: static first, dynamic last**
3. **Batch similar sub-agents** — same base prompt = shared cache
4. **Monitor cache hit rate** — most providers expose this in dashboards or API responses
