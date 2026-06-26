# Agent Workflow Failure Taxonomy

Common failure modes, how to diagnose them, and the fix pattern.

## Silent Failures

**Symptoms:** Workflow reports success, nothing was actually done. Logs show "completed" but output is empty or stale.

**Causes:**
- Exception caught but not re-thrown or logged
- API returned 200 with an error payload that wasn't checked
- Async function called without `await`

**Fix:** Log every caught exception. Check API response bodies, not just status codes. Lint for missing `await`.

---

## Phantom Retries

**Symptoms:** Items processed multiple times. Duplicate records, double-sends, duplicate charges.

**Causes:**
- No idempotency key on API calls
- Retry logic re-runs from the beginning instead of from the failed step
- State saved after the step instead of before marking complete

**Fix:** Use deterministic IDs (hash of input) as idempotency keys. Save state *before* marking a step done, not after.

---

## Cascading Timeouts

**Symptoms:** One slow API call causes all downstream steps to hang. Entire workflow stalls.

**Causes:**
- No timeout set on external calls
- No circuit breaker — keeps retrying a down service
- Blocking operations on the main thread

**Fix:** Set explicit timeouts on all fetch/HTTP calls. Circuit breaker with a sensible cooldown. Treat timeout as a failure, not a slow success.

---

## State Drift

**Symptoms:** Workflow thinks step 3 is done but step 2's output was corrupt. Later steps produce garbage.

**Causes:**
- State file written but not validated after write
- Partial writes on crash (file truncated)
- Multiple workflow instances writing the same state file

**Fix:** Validate state after loading (check schema, not just existence). Use atomic writes (write to temp file, rename). Add instance lock file.

---

## Context Window Saturation (LLM-specific)

**Symptoms:** Agent starts dropping earlier context, makes decisions inconsistent with prior steps, "forgets" tool outputs.

**Causes:**
- Accumulating raw API responses in context instead of summaries
- No compaction between workflow phases

**Fix:** Summarize tool outputs immediately after use. Between major phases, compact context. Store raw data in files, keep only references in context.

---

## Tool Call Loops

**Symptoms:** Agent calls the same tool repeatedly with slightly different arguments. Burns tokens, never progresses.

**Causes:**
- No loop guard (no check for "did I already try this?")
- Tool returns ambiguous result, agent re-queries instead of deciding
- Missing stopping condition in the workflow instructions

**Fix:** Track tool calls made in current session. Add explicit stopping conditions: "if you've called X more than 3 times on the same input, stop and report what you have."

---

## Rate Limit Spiral

**Symptoms:** Workflow hits 429, backs off, retries, hits 429 again. Exponential delay keeps growing. Workflow never completes.

**Causes:**
- Parallel requests to rate-limited API
- Retry adds to the queue during a rate limit window
- No maximum delay cap

**Fix:** Serialize requests to rate-limited APIs. Cap backoff at 60–120 seconds. Track 429s separately from other errors — don't count them toward circuit breaker threshold.

---

## Incomplete Cleanup

**Symptoms:** Resources created but not cleaned up on failure: temp files, open connections, created records, started transactions.

**Causes:**
- Cleanup code in `else` branch, not `finally`
- Early returns bypass cleanup

**Fix:** Use try/finally for all resource cleanup. Register cleanup callbacks at resource creation time, not at the end.
