# Execution Strategies

Each step has an `execution_strategy` that controls error recovery. Default is `fail`.

## fail (default)

Stops the workflow immediately and raises `ExecutionError` (`BEDDEL-EXEC-002`).

```yaml
execution_strategy:
  type: fail
```

**When to use:** Critical steps where failure should halt the entire workflow.

## skip

Logs the error, sets the step result to `None`, and continues to the next step.

```yaml
execution_strategy:
  type: skip
```

**When to use:** Optional/non-critical steps. Downstream steps should check for `None`:

```yaml
if: "$stepResult.optional_step"
```

Note: This is different from the `SKIPPED` sentinel (used when a step's `if` condition is falsy). The skip *execution strategy* stores `None` on error; the `SKIPPED` sentinel is stored when a step is conditionally skipped.

## retry

Re-executes the step with exponential backoff. Raises `ExecutionError` (`BEDDEL-EXEC-003`) when all attempts are exhausted.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `max_attempts` | int | `3` | Number of retry attempts (after initial failure) |
| `backoff_base` | float | `2.0` | Base for exponential backoff (seconds) |
| `backoff_max` | float | `60.0` | Upper bound for delay |
| `jitter` | bool | `true` | Add random jitter (0.5x–1.5x multiplier) |

Delay formula: `min(backoff_base ^ attempt, backoff_max) * random(0.5, 1.5)`

```yaml
execution_strategy:
  type: retry
  retry:
    max_attempts: 5
    backoff_base: 2.0
    jitter: true
```

**When to use:** Transient failures — API rate limits, network timeouts, flaky services.

## fallback

Executes an alternative inline step when the primary step fails. Raises `ExecutionError` (`BEDDEL-EXEC-004`) if no fallback step is defined.

```yaml
execution_strategy:
  type: fallback
  fallback_step:
    id: fallback-summarize
    primitive: llm
    config:
      model: gpt-4o-mini
      prompt: "Simple summary of: $input.text"
```

The `fallback_step` is a full inline step definition (same schema as a regular step).

**When to use:** When a cheaper/simpler alternative exists — e.g., fall back to a smaller model, a cached response, or a static default.

## delegate

Delegates error recovery to an LLM that chooses between `retry`, `skip`, or `fallback` (if a `fallback_step` is defined). Raises `ExecutionError` if the LLM provider is missing (`BEDDEL-EXEC-010`) or returns an invalid action (`BEDDEL-EXEC-011`).

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `max_attempts` | int | — | Not directly configurable; delegate uses `RetryConfig(max_attempts=2)` when it chooses retry |
| `model` | str | `gpt-4o-mini` | Model for the delegate LLM call (from `context.deps.delegate_model`) |

```yaml
execution_strategy:
  type: delegate
  fallback_step:
    id: safe-default
    primitive: output-generator
    config:
      template: "Service unavailable"
      format: text
```

The LLM receives the step id, primitive name, error details, and available actions, then responds with exactly one word. If it chooses `retry`, the step is retried with `max_attempts=2`.

**When to use:** Complex failure scenarios where the right recovery depends on the error type — e.g., retry on rate limits but skip on invalid input.

## Summary Table

| Strategy | Stops Workflow? | Requires LLM? | Config Object |
|----------|----------------|----------------|---------------|
| `fail` | Yes | No | — |
| `skip` | No | No | — |
| `retry` | On exhaustion | No | `retry: {max_attempts, backoff_base, backoff_max, jitter}` |
| `fallback` | On fallback failure | No | `fallback_step: <Step>` |
| `delegate` | On invalid action | Yes | Optional `fallback_step` |
