# ClawSaver — Integration for OpenClaw Sessions

This document shows how to integrate ClawSaver (session-level message batching) into OpenClaw's session handler.

---

## Architecture

```
OpenClaw Session Handler
    ↓
    └─→ handleUserMessage(sessionKey, message)
           ↓
           └─→ SessionDebouncer.enqueue()
                  ↓
                  └─→ (wait 800ms for more messages)
                      ↓
                      └─→ flushCallback(batchedMessages)
                         ↓
                         └─→ callModel(merged)
                            ↓
                            └─→ sendToSession(response)
```

**Key insight:** ClawSaver sits between message ingestion and model calls, transparently batching without changing any other logic.

---

## Integration Steps

### 1. Import SessionDebouncer

```javascript
import SessionDebouncer from './SessionDebouncer.js';
```

### 2. Create a Map to hold debouncers per session

```javascript
const sessionDebouncers = new Map();

function getOrCreateDebouncer(sessionKey) {
  if (!sessionDebouncers.has(sessionKey)) {
    const debouncer = new SessionDebouncer(
      sessionKey,
      (messages, meta) => processModelCall(sessionKey, messages, meta)
    );
    sessionDebouncers.set(sessionKey, debouncer);
  }
  return sessionDebouncers.get(sessionKey);
}
```

### 3. Update your message handler

**Before:**
```javascript
async function handleUserMessage(sessionKey, message) {
  const result = await model.complete(message.text);
  await sendToSession(sessionKey, result);
}
```

**After:**
```javascript
async function handleUserMessage(sessionKey, message) {
  const debouncer = getOrCreateDebouncer(sessionKey);
  debouncer.enqueue({
    text: message.text,
    id: message.id,  // optional but useful for tracking
  });
}
```

### 4. Implement the model call handler

```javascript
async function processModelCall(sessionKey, messages, meta) {
  const merged = mergeMessages(messages);
  
  // Log for observability
  console.log(
    `[${sessionKey}] Batching: ${meta.batchSize} messages, ` +
    `saving ${meta.savedCalls} model call(s)`
  );
  
  try {
    // Call your model with merged input
    const result = await model.complete(merged);
    
    // Send response back to session
    await sendToSession(sessionKey, result);
  } catch (err) {
    console.error(`[${sessionKey}] Model call failed:`, err);
    // Add retry logic if needed
    throw err;
  }
}

function mergeMessages(messages) {
  return messages
    .map((m, i) => `**Message ${i + 1}:**\n${m.text}`)
    .join('\n\n')
    + '\n\n_Please treat the above as a single combined user input._';
}
```

Done! That's the minimum integration.

---

## Optional: Add Monitoring

```javascript
// Log every Nth batch
let batchCounter = 0;
let savedCallsTotal = 0;

async function processModelCall(sessionKey, messages, meta) {
  batchCounter += 1;
  savedCallsTotal += meta.savedCalls;
  
  if (batchCounter % 10 === 0) {
    console.log(
      `[ClawSaver] ${batchCounter} batches processed, ` +
      `${savedCallsTotal} calls saved (${(savedCallsTotal/batchCounter).toFixed(1)} avg)`
    );
  }
  
  // ... rest of handler
}
```

Or per-session metrics:

```javascript
// Get state from a debouncer
const debouncer = sessionDebouncers.get(sessionKey);
const state = debouncer.getState();

console.log(`[${sessionKey}] Metrics:`, {
  batches: state.metrics.totalBatches,
  messages: state.metrics.totalMessages,
  saved: state.metrics.totalSavedCalls,
  savingsPercent: (state.metrics.totalSavedCalls / state.metrics.totalMessages * 100).toFixed(1),
});
```

---

## Optional: Handle Session Cleanup

```javascript
function removeSession(sessionKey) {
  const debouncer = sessionDebouncers.get(sessionKey);
  if (debouncer) {
    // Flush any pending messages before cleanup
    debouncer.forceFlush('session-cleanup');
    sessionDebouncers.delete(sessionKey);
    console.log(`[${sessionKey}] Cleaned up debouncer`);
  }
}

// Call this when a session ends or is closed
// (hook into your session close handler)
```

---

## Optional: Per-Session Tuning

Different sessions might have different batching needs. You can customize per session:

```javascript
const customConfig = {
  'realtime-session': { debounceMs: 200 },      // Low latency
  'batch-session': { debounceMs: 2000 },        // High cost savings
  'normal-session': { debounceMs: 800 },        // Default
};

function getOrCreateDebouncer(sessionKey) {
  if (!sessionDebouncers.has(sessionKey)) {
    const config = customConfig[sessionKey] || {};
    const debouncer = new SessionDebouncer(
      sessionKey,
      (messages, meta) => processModelCall(sessionKey, messages, meta),
      config
    );
    sessionDebouncers.set(sessionKey, debouncer);
  }
  return sessionDebouncers.get(sessionKey);
}
```

---

## Testing Your Integration

### 1. Unit test (verify debouncer works)

```bash
cd /path/to/clawsaver
npm test
```

Should see 10 passing tests.

### 2. Integration test (send real messages)

```javascript
const session = 'test-session-123';

// Simulate user sending 2 messages quickly
await handleUserMessage(session, { text: 'Hello', id: 'msg1' });
await handleUserMessage(session, { text: 'How are you?', id: 'msg2' });

// Wait for debounce + model call
await new Promise(r => setTimeout(r, 1500));

// Check state
const state = sessionDebouncers.get(session).getState();
console.log(state.metrics);
// Should show: 1 batch, 2 messages, 1 call saved
```

### 3. Manual test (send messages via your UI)

1. Start your session handler
2. Send 2–3 related messages from the same session
3. Watch logs for: `"Batching: N messages, saving M calls"`
4. Verify responses come back normally

---

## Troubleshooting

### "No batching happening"

**Causes:**
- Messages sent > 800ms apart (default debounce)
- `debounceMs` set to 0
- Debouncer not actually enqueuing (check logs)

**Fix:**
```javascript
debouncer.enqueue(message);  // Make sure you're calling this
console.log(debouncer.getStatusString());  // Should show "buffering"
```

### "Batches feel slow to respond"

Increase `debounceMs` to 1500–2000 to capture more messages, OR reduce it to 300–500 to flush faster.

```javascript
new SessionDebouncer(sessionKey, handler, { debounceMs: 300 })
```

### "I want to send immediately (bypass batching)"

Call `forceFlush()`:

```javascript
const debouncer = sessionDebouncers.get(sessionKey);
debouncer.forceFlush('user-clicked-send-now');
```

Or create a separate debouncer with `debounceMs: 0`.

---

## Performance Implications

- **Memory:** ~1-2 KB per active session (negligible)
- **CPU:** <1ms per enqueue, async flush (negligible)
- **Latency:** +800ms average (tunable, acceptable for cost savings)
- **Throughput:** Same (batching doesn't reduce total messages processed, just reduces model calls)

---

## Metrics to Monitor

After integration, track these:

| Metric | How to Calculate | Target |
|--------|-----------------|--------|
| Call reduction | (original calls - batched calls) / original calls | >15% |
| Avg batch size | total messages / total batches | >2 |
| Latency impact | time_with_batching - time_without | <1s |
| User satisfaction | (positive feedback / total feedback) | >95% |

---

## Production Rollout

### Phase 1: Staging (1–2 days)
1. Integrate into staging environment
2. Send realistic message patterns
3. Measure metrics
4. Tune parameters if needed

### Phase 2: Canary (10% of users, 1 day)
1. Enable for 10% of sessions
2. Monitor error rates, latency, cost
3. Confirm no regressions

### Phase 3: Rollout (100%, ongoing)
1. Enable for all sessions
2. Continue monitoring
3. Tune based on real-world usage

### Phase 4: Optimization (optional, 1–2 weeks)
1. Analyze per-user patterns
2. Implement adaptive debounce
3. Add message intent classification

---

## Example: Full Integration

```javascript
import SessionDebouncer from './SessionDebouncer.js';

const sessionDebouncers = new Map();

function getOrCreateDebouncer(sessionKey) {
  if (!sessionDebouncers.has(sessionKey)) {
    sessionDebouncers.set(
      sessionKey,
      new SessionDebouncer(sessionKey, (msgs, meta) => processModelCall(sessionKey, msgs, meta))
    );
  }
  return sessionDebouncers.get(sessionKey);
}

async function handleUserMessage(sessionKey, message) {
  const debouncer = getOrCreateDebouncer(sessionKey);
  debouncer.enqueue({
    text: message.text,
    id: message.id || `${Date.now()}_${Math.random()}`,
  });
}

async function processModelCall(sessionKey, messages, meta) {
  const merged = mergeMessages(messages);
  
  console.log(
    `[${sessionKey}] Processing ${meta.batchSize} msgs (saved ${meta.savedCalls} calls)`
  );

  try {
    const result = await myModel.complete(merged);
    await sendToSession(sessionKey, result);
  } catch (err) {
    console.error(`[${sessionKey}] Error:`, err);
    throw err;
  }
}

function mergeMessages(messages) {
  return messages
    .map((m, i) => `**Message ${i + 1}:**\n${m.text}`)
    .join('\n\n')
    + '\n\n_Please treat the above as a single combined user input._';
}

function removeSession(sessionKey) {
  const debouncer = sessionDebouncers.get(sessionKey);
  if (debouncer) {
    debouncer.forceFlush('cleanup');
    sessionDebouncers.delete(sessionKey);
  }
}

export { handleUserMessage, removeSession, getOrCreateDebouncer };
```

That's it. 🚀

---

## Next Steps

1. Copy `SessionDebouncer.js` into your codebase
2. Follow steps 1–4 above
3. Test with `npm test && npm run demo`
4. Deploy to staging
5. Monitor metrics for 1–2 days
6. Tune if needed
7. Roll out to production

**Questions?** Check `README.md` or run the test suite.
