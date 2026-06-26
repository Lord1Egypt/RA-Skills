# Token Spike Diagnosis & Post-Incident Checklist

## Step-by-Step Diagnosis

### Step 1: Check recent sessions

```
sessions_list (limit: 10, messageLimit: 1)
```

Look for:
- High `estimatedCostUsd` with low output tokens
- `status: "failed"` or `status: "error"`
- Multiple sessions for the same cron job in a short window

### Step 2: Check cron health

```
cron list (includeDisabled: true)
```

Look for:
- `consecutiveErrors > 0`
- `lastError` containing "ModelSwitch", "LiveSession", or "timeout"
- `lastDurationMs` much higher than expected

### Step 3: Check gateway logs

```bash
tail -200 ~/.openclaw/logs/gateway.log | grep -i "model switch\|retry\|error\|LiveSession"
```

Pattern to identify: same session ID with model-switch entries repeating every 25-90 seconds. If this continues for > 5 minutes, it's a runaway retry loop.

### Step 4: Kill the loop

Remove the offending cron job immediately:

```
cron remove (jobId: "<id>")
```

### Step 5: Fix and recreate

1. Recreate WITHOUT `sessionKey` binding
2. Set `sessionTarget: "isolated"`
3. Set explicit `agentId` matching the correct agent
4. Set explicit `model` in payload if available
5. Verify with `cron list` that no stale `sessionKey` was auto-assigned (known gateway bug — it may auto-assign `sessionKey: "agent:main:main"` even for isolated jobs)

## Post-Incident Checklist

- [ ] Offending jobs killed or fixed
- [ ] Root cause documented (which field/config caused the loop)
- [ ] All remaining crons audited for same pattern
- [ ] System prompt size reviewed and trimmed if > 20KB
- [ ] Cost from incident estimated and logged
- [ ] Gateway logs reviewed for any other silent failures
- [ ] Preventive monitoring added (check consecutiveErrors weekly)

## Root Cause Pattern

The most common cause: a cron job with `sessionTarget: "isolated"` but a stale `sessionKey` pointing to the main interactive session. When the main session has been used by multiple models (e.g., Claude + GPT), the gateway's model-resolution logic sees a mismatch and enters a retry loop. Each retry sends the full system prompt to the API with zero useful output.

Compounding factors:
- No circuit breaker on model-switch retries
- No cost anomaly alerting
- Large system prompt (every retry sends the full prompt)
- Silent failure (no notification to the user)
