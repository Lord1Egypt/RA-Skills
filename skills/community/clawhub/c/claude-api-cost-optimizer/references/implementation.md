
# Implementation Patterns

> **Security note — local caching:** Patterns in this file cache API responses and codebases to local files (e.g. `~/.claude_cache/`, `costs.log`, `batch_results.jsonl`). These files may contain source code, API responses, or other sensitive data.
> - Set file permissions: `chmod 600 ~/.claude_cache/` and any log files
> - Never cache content containing secrets, credentials, or PII
> - Set a short `max_age_hours` TTL and clear cache regularly
> - Add cache directories to `.gitignore`

## Model Selection Strategy

Pick the cheapest model that solves the problem. Overspending on Opus for simple tasks can cost **10–18x more** than using Haiku.

### Task Classification

**Haiku ($0.80/M input)** — Use for:
- Code formatting, linting fixes
- Comment generation, documentation
- Simple renames, variable extraction
- Explanation of existing code
- Boilerplate generation
- Token counting

**Sonnet ($3/M input)** — Use for:
- Refactoring and optimization
- Bug debugging with context
- Code review and critique
- Test writing
- Minor architecture changes
- Error triage with logs

**Opus ($15/M input)** — Use only for:
- Complex architecture decisions
- Algorithm design
- Security audits
- Multi-file refactoring
- Novel problem solving
- Performance optimization with constraints

### Routing Function

```python
import anthropic

def select_model(task_type: str, complexity_signal: float = 0.5) -> str:
    """
    task_type: "format", "refactor", "debug", "architecture", etc.
    complexity_signal: 0.0–1.0 (context size, branching logic, ambiguity)
    """
    simple = {
        "format", "lint", "comment", "doc", "explain", 
        "rename", "boilerplate", "tokens"
    }
    complex = {
        "architecture", "algorithm", "audit", "perf",
        "multi_file_refactor"
    }
    
    if task_type in simple:
        return "claude-haiku-4-5-20251001"
    elif task_type in complex or complexity_signal > 0.8:
        return "claude-opus-4-6"
    else:
        return "claude-sonnet-4-6"

def call_api(task_type: str, prompt: str, context: str = "") -> dict:
    client = anthropic.Anthropic()
    model = select_model(task_type, len(context) / 10000)
    
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[
            {"role": "user", "content": f"{context}\n\n{prompt}"}
        ]
    )
    return {"text": response.content[0].text, "cost": _calc_cost(response.usage)}
```

---

## Prompt Caching

Cache **large, repeated static content** (system prompts, codebase context). Cache **reads cost 90% less** than normal input tokens.

**When to cache:**
- System prompt + instructions (reused across multiple requests)
- Large codebase context (entire module, library reference)
- Known context blocks (documentation, style guide)
- Anything >1KB used 2+ times in a session

**When NOT to cache:**
- User queries (unique per request)
- Data that changes frequently
- Small snippets (<200 tokens)

### Setup Example

```python
import anthropic

def create_cached_request(
    system_prompt: str,
    codebase_context: str,
    user_query: str,
    model: str = "claude-sonnet-4-6"
) -> dict:
    """Create a request with cached system prompt and codebase."""
    client = anthropic.Anthropic()
    
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Codebase:\n{codebase_context}",
                        "cache_control": {"type": "ephemeral"}
                    },
                    {
                        "type": "text",
                        "text": user_query
                    }
                ]
            }
        ]
    )
    
    usage = response.usage
    cache_savings = (usage.cache_read_input_tokens * 0.9 * 
                     INPUT_RATE_PER_MODEL[model])
    
    return {
        "response": response.content[0].text,
        "cache_read": usage.cache_read_input_tokens,
        "cache_created": usage.cache_creation_input_tokens,
        "savings_usd": cache_savings
    }
```

### Cache Payoff Math

- **Cache write cost:** ~25% more than normal input (one-time)
- **Cache read cost:** 10% of normal input (recurring)
- **Breakeven:** After 2–3 reads, the savings exceed the write cost

Example: Caching a 5,000-token system prompt with Sonnet:
- Write cost: 5,000 × $3 × 1.25 / 1M = $0.01875
- Per read: 5,000 × $3 × 0.1 / 1M = $0.0015
- Breakeven: ~13 reads

---

## Batching

Combine multiple independent requests into one API call to eliminate per-request overhead.

### Batch API (Async, 50% Discount)

```python
import anthropic
import time

def batch_requests(tasks: list[dict], output_file: str = "batch_results.jsonl"):
    """
    tasks: [{"type": "refactor", "code": "...", "prompt": "..."}, ...]
    Submits batch to Anthropic, returns job_id.
    Poll with get_batch_results(job_id).
    """
    client = anthropic.Anthropic()
    
    # Format requests for batch API
    requests = []
    for i, task in enumerate(tasks):
        requests.append({
            "custom_id": f"task-{i}",
            "params": {
                "model": select_model(task["type"]),
                "max_tokens": 2048,
                "messages": [{"role": "user", "content": task["prompt"]}]
            }
        })
    
    # Submit batch
    batch = client.beta.messages.batches.create(requests=requests)
    print(f"Batch {batch.id} submitted. Check back in ~1 hour.")
    return batch.id

def get_batch_results(batch_id: str) -> list[dict]:
    """Poll and retrieve batch results."""
    client = anthropic.Anthropic()
    batch = client.beta.messages.batches.retrieve(batch_id)
    
    if batch.processing_status == "succeeded":
        results = []
        for result in client.beta.messages.batches.results(batch_id):
            results.append({
                "id": result.custom_id,
                "text": result.result.message.content[0].text,
                "usage": result.result.message.usage
            })
        return results
    elif batch.processing_status == "processing":
        return {"status": "processing", "id": batch_id}
    else:
        return {"status": batch.processing_status, "errors": batch.errors}
```

**Cost savings:** 50% off all token costs. Trade-off: results available within ~24 hours (non-urgent tasks only).

### Synchronous Batching (Multiple Requests in One Call)

```python
def batch_code_reviews(code_samples: list[str]) -> list[str]:
    """Review multiple code snippets in one request."""
    client = anthropic.Anthropic()
    
    combined_prompt = "\n---\n".join([
        f"Review snippet {i+1}:\n{code}"
        for i, code in enumerate(code_samples)
    ])
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,  # Larger buffer for multiple reviews
        messages=[
            {"role": "user", "content": combined_prompt}
        ]
    )
    
    # Parse response into individual reviews
    reviews = response.content[0].text.split("---")
    return [r.strip() for r in reviews]
```

---

## Local Caching

For identical requests, cache responses locally to skip API calls entirely.

```python
import hashlib
import json
import os
from pathlib import Path

CACHE_DIR = Path.home() / ".claude_cache"
CACHE_DIR.mkdir(exist_ok=True)

def cache_key(model: str, system: str, messages: str) -> str:
    """Generate deterministic cache key."""
    content = f"{model}:{system}:{messages}"
    return hashlib.sha256(content.encode()).hexdigest()

def get_or_call(
    model: str, 
    system: str, 
    messages: list[dict],
    max_age_hours: int = 24
) -> tuple[str, bool]:
    """Return (response_text, from_cache)."""
    
    msg_str = json.dumps(messages, sort_keys=True)
    key = cache_key(model, system, msg_str)
    cache_file = CACHE_DIR / f"{key}.json"
    
    # Check cache
    if cache_file.exists():
        age = (Path(cache_file).stat().st_mtime)
        if time.time() - age < max_age_hours * 3600:
            with open(cache_file) as f:
                data = json.load(f)
                return data["text"], True
    
    # Call API
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=system,
        messages=messages
    )
    
    # Cache result
    result = {
        "text": response.content[0].text,
        "timestamp": time.time(),
        "model": model
    }
    with open(cache_file, "w") as f:
        json.dump(result, f)
    
    return result["text"], False
```

---

## Cost Tracking

Always track actual costs from API responses.

```python
import anthropic

PRICING = {
    "claude-haiku-4-5-20251001": {
        "input": 0.80 / 1e6,
        "output": 4.0 / 1e6,
        "cache_write": 1.0 / 1e6,
        "cache_read": 0.08 / 1e6
    },
    "claude-sonnet-4-6": {
        "input": 3.0 / 1e6,
        "output": 15.0 / 1e6,
        "cache_write": 3.75 / 1e6,
        "cache_read": 0.30 / 1e6
    },
    "claude-opus-4-6": {
        "input": 15.0 / 1e6,
        "output": 75.0 / 1e6,
        "cache_write": 18.75 / 1e6,
        "cache_read": 1.50 / 1e6
    }
}

def calculate_cost(model: str, usage) -> float:
    """Return cost in USD for this request."""
    rates = PRICING[model]
    return (
        usage.input_tokens * rates["input"] +
        usage.cache_creation_input_tokens * rates["cache_write"] +
        usage.cache_read_input_tokens * rates["cache_read"] +
        usage.output_tokens * rates["output"]
    )

def call_and_track(model: str, prompt: str, log_file: str = "costs.log"):
    """Call API and log cost."""
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )
    
    cost = calculate_cost(model, response.usage)
    
    with open(log_file, "a") as f:
        f.write(f"{model}\t{cost:.6f}\t{response.usage.input_tokens}\t"
                f"{response.usage.output_tokens}\t"
                f"{response.usage.cache_read_input_tokens}\n")
    
    return response, cost

# Example usage
response, cost = call_and_track("claude-haiku-4-5-20251001", "What is 2+2?")
print(f"Cost: ${cost:.4f}")
```

---

## Retry with Exponential Backoff

Handle rate limits (429) gracefully.

```python
import anthropic
import time
from anthropic import RateLimitError

def call_with_backoff(
    model: str,
    messages: list[dict],
    max_retries: int = 5,
    base_wait: float = 1.0
) -> str:
    """Call API with exponential backoff on rate limit."""
    
    client = anthropic.Anthropic()
    
    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                messages=messages
            )
            return response.content[0].text
        
        except RateLimitError:
            wait_time = base_wait * (2 ** attempt)
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
    
    raise Exception(f"Failed after {max_retries} retries")
```

---

## Anti-Patterns to Avoid

1. **Using Opus for simple tasks** → Costs 10–18x more than Haiku. Always classify first.
2. **Not caching system prompts** → If you use the same instructions 10 times, you're overpaying 9x.
3. **Sending entire files** → Extract only the relevant function/class. A 10KB file might need only 200 tokens.
4. **max_tokens set too high** → If you're generating a 100-token response, don't request 4,096 tokens.
5. **Separate API calls for batch work** → Combine independent requests into one call.
6. **No cost tracking** → You can't optimize what you don't measure.
7. **Ignoring cache payoff** → Don't cache single-use content; cache reused static context.
