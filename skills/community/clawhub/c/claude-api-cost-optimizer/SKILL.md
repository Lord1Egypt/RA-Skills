---
name: claude-api-cost-optimizer
description: "Minimize Anthropic Claude API costs through model selection, prompt caching, batching, and cost tracking. ⚠️ Enables local caching and cost logging — review file permissions and exclude secrets. Trigger phrases: reduce API costs, optimize Claude spending, save on API calls, Claude cost optimization, cheaper Claude models."
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":[]},"env":["ANTHROPIC_API_KEY"],"os":["linux","darwin","win32"],"homepage":"https://clawhub.com/djc00p/claude-api-cost-optimizer"}}
---

# Claude API Cost Optimizer

> ⚠️ **Local Data Warning:** This skill creates `~/.claude_cache/`, `costs.log`, and `batch_results.jsonl` which may contain source code, API responses, and prompts. Set `chmod 600` on these files, never cache secrets/PII, and add cache directories to `.gitignore`.

Cut Claude API costs by 70–90% using intelligent model selection, caching, and batching.

## Quick Start

1. **Audit your current API calls** — identify which tasks use Opus or Sonnet that could use Haiku. Model selection alone saves 10–18x on simple tasks. Ensure `ANTHROPIC_API_KEY` is set in your environment (required).
2. Pick the cheapest model tier for each task: Haiku (cheapest) → Sonnet (mid) → Opus (most expensive, use sparingly). See `references/pricing.md` for current rates.
3. Enable prompt caching for repeated context (system prompts, codebases) by adding `"cache_control": {"type": "ephemeral"}` to message blocks
4. Implement cost reporting — track `input_tokens`, `output_tokens`, and cache metrics from API responses

## Key Concepts

- **Model selection** — Haiku for simple tasks (formatting, comments) — cheapest tier. Sonnet for medium (refactoring, debugging) — mid tier. Opus for complex only (architecture, security) — most expensive, use sparingly. See `references/pricing.md` for current rates.
- **Prompt caching** — Cache large static content (system prompts, codebase context). Cache reads cost 90% less; writes pay off after 1–2 reuses.
- **Batching** — Combine multiple requests into one API call to eliminate per-request overhead. 80% fewer calls ≈ 80% lower cost.
- **Local caching** — Cache identical responses locally to skip redundant API calls entirely.
- **Context extraction** — Send only relevant snippets, not whole files. Smaller inputs = lower costs.
- **max_tokens discipline** — Set realistic limits; unused token budget is wasted money.

## Common Usage

> Code examples are in Python but concepts apply to any language or SDK.

**Model selection pattern:**

```python
def select_model(task_type: str) -> str:
    simple_tasks = ["formatting", "comments", "explanation", "rename"]
    complex_tasks = ["architecture", "algorithm", "security_audit"]
    return ("claude-haiku-4-5-20251001" if task_type in simple_tasks else
            "claude-opus-4-6" if task_type in complex_tasks else
            "claude-sonnet-4-6")
```

**Prompt caching:**

```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": system_prompt,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": f"Code:\n{source_code}", 
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": query}
        ]
    }]
)
```

**Cost tracking:**

```python
usage = response.usage
cost = (usage.input_tokens * INPUT_RATE +
        usage.cache_creation_input_tokens * CACHE_WRITE_RATE +
        usage.cache_read_input_tokens * CACHE_READ_RATE +
        usage.output_tokens * OUTPUT_RATE)
```

## Security Checklist

Before using cost tracking and local caching:
- [ ] Set `chmod 600 ~/.claude_cache/` and all log files
- [ ] Never cache content containing secrets, credentials, or PII
- [ ] Set a short TTL (`max_age_hours`) and clear cache regularly
- [ ] Add cache directories to `.gitignore`
- [ ] Use encrypted volumes or ephemeral storage in CI environments
- [ ] Audit cached content periodically for sensitive data leaks

## References

- `references/implementation.md` — Full implementation patterns, model routing, caching setup, batching, retry logic, and anti-patterns
- `references/pricing.md` — Current pricing, cache cost math, savings calculations, and batch API details
