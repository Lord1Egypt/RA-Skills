---
name: error-recovery
description: Error Recovery - Strategies for handling failures gracefully
---

# Error Recovery - Handling Failures Gracefully

## OpenClaw Error Types

| Error | Cause | Recovery |
|-------|-------|----------|
| 429 Rate Limit | Too many requests | Wait + retry with backoff |
| 402 Billing | API credits exhausted | Switch model or wait |
| 503 Overloaded | Provider busy | Wait + retry |
| Context Overflow | Context window full | Trigger compaction |
| Role Ordering | Corrupted session | Reset session |
| Transient HTTP | Network issue | Auto-retry (built-in) |

## Error Handling Patterns

### Pattern 1: Retry with Backoff

```javascript
async function retryWithBackoff(fn, maxAttempts = 3) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await fn();
    } catch (err) {
      if (isRetryable(err) && i < maxAttempts - 1) {
        await sleep(1000 * Math.pow(2, i)); // 1s, 2s, 4s
        continue;
      }
      throw err;
    }
  }
}
```

### Pattern 2: Graceful Degradation

```javascript
async function withFallback(primary, fallback) {
  try {
    return await primary();
  } catch (err) {
    console.warn("Primary failed, trying fallback:", err.message);
    return await fallback();
  }
}

// Usage
const result = await withFallback(
  () => callExpensiveModel(msg),
  () => callCheapModel(msg)
);
```

### Pattern 3: Circuit Breaker

```javascript
class CircuitBreaker {
  constructor(fn, threshold = 3) {
    this.fn = fn;
    this.failures = 0;
    this.threshold = threshold;
    this.state = "closed"; // open/closed/half-open
  }

  async execute() {
    if (this.state === "open") {
      throw new Error("Circuit breaker open");
    }
    try {
      const result = await this.fn();
      this.failures = 0;
      this.state = "closed";
      return result;
    } catch (err) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.state = "open";
      }
      throw err;
    }
  }
}
```

## Tool Failure Handling

Tools in OpenClaw are **non-fatal** — if a tool fails, the agent continues:

```javascript
// In agent-runner, tool errors are caught but don't stop execution
.catch((err) => {
  log(`Tool ${toolName} failed: ${err.message}`);
  // Continue execution
});
```

## Session Corruption Recovery

If session becomes corrupted:

1. **Detection**: Role ordering errors, malformed messages
2. **Action**: Session auto-reset by OpenClaw
3. **Recovery**: Fresh session, context preserved via MEMORY.md

## Built-in Recovery Mechanisms

| Mechanism | Trigger | Action |
|----------|---------|--------|
| Auto-retry | 408/429/5xx | Exponential backoff |
| Context overflow | Token limit | Trigger compaction |
| Session corruption | Role error | Reset session |
| Model switch | persistent failure | Fallback model |

## Best Practices

1. **Don't suppress errors silently** — log them
2. **Prefer retries for transient failures** — network/timeout
3. **Reset for corruption** — don't try to fix corrupted state
4. **Use fallback models** — cheap → expensive
5. **Keep MEMORY.md updated** — for recovery after reset
