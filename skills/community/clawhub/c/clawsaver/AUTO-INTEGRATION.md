# ClawSaver Auto-Integration Guide

Getting started with ClawSaver takes 10 minutes. Here's how to wire it in with minimal friction.

## Approach 1: Drop-in Wrapper (Recommended)

Use the OpenClaw middleware pattern. ClawSaver sits between your message handler and your model, completely transparent.

### Step 1: Copy the wrapper

```javascript
// In your skills/my-skill/src/clawsaver-middleware.js
import SessionDebouncer from 'clawsaver';

const debouncers = new Map();

export function clawsaverMiddleware(sessionKey, options = {}) {
  if (!debouncers.has(sessionKey)) {
    debouncers.set(sessionKey, new SessionDebouncer(sessionKey, null, {
      debounceMs: options.debounceMs ?? 800,
      maxWaitMs: options.maxWaitMs ?? 3000,
      maxMessages: options.maxMessages ?? 5,
    }));
  }
  return debouncers.get(sessionKey);
}

export async function processWithBatching(sessionKey, message, modelHandler, options = {}) {
  const debouncer = clawsaverMiddleware(sessionKey, options);
  
  // Set handler if not already set (only once per debouncer)
  if (!debouncer.handler) {
    debouncer.handler = async (messages, meta) => {
      const merged = messages
        .map((m, i) => `**Message ${i + 1}:**\n${m.text}`)
        .join('\n\n') + '\n\n_Combined user input._';
      
      return modelHandler(merged, { batchSize: meta.batchSize, saved: meta.savedCalls });
    };
  }
  
  // Enqueue and let it batch automatically
  debouncer.enqueue({ text: message });
}
```

### Step 2: Use it in your handler

```javascript
// In your skill's message handler
import { processWithBatching } from './src/clawsaver-middleware.js';

async function handleMessage(sessionKey, userMessage, modelFn) {
  // Instead of calling model immediately:
  // const response = await modelFn(userMessage);
  
  // Wrap it with batching:
  return processWithBatching(sessionKey, userMessage, modelFn, {
    debounceMs: 800,      // Tune if needed
  });
}
```

**Result:** Every message is now batched. No other changes needed.

---

## Approach 2: Manual Batch Control

For workflows where you want explicit batch points:

```javascript
import { getOrCreateDebouncer } from 'clawsaver/example-integration.js';

// Collect messages
const debouncer = getOrCreateDebouncer(sessionKey);
debouncer.enqueue({ text: userMessage1 });
debouncer.enqueue({ text: userMessage2 });

// When you're ready to process:
debouncer.forceFlush('user-explicit');
```

---

## Approach 3: Profile-Based (Production)

Choose a profile based on your traffic pattern:

```javascript
const profiles = {
  chat: { debounceMs: 800, maxWaitMs: 3000, maxMessages: 5 },
  batch: { debounceMs: 1500, maxWaitMs: 4000, maxMessages: 10 },
  realtime: { debounceMs: 200, maxWaitMs: 1000, maxMessages: 2 },
};

const debouncer = new SessionDebouncer(
  sessionKey,
  handler,
  profiles[process.env.CLAWSAVER_PROFILE || 'chat']
);
```

Set `CLAWSAVER_PROFILE=batch` in production to tune for your use case.

---

## Monitoring the Savings

Enable metrics logging to see actual cost reduction:

```javascript
import { startMetricsReporter } from 'clawsaver/example-integration.js';

// Log metrics every 60 seconds
startMetricsReporter(60000);
```

Output:
```
--- ClawSaver Metrics ---
session-123: 45 batches, 127 calls saved, avg batch 3.2
session-456: 32 batches, 89 calls saved, avg batch 3.1

Total: 77 batches, 216 calls saved (73.7% reduction)
```

---

## Zero-Config Option: Just Install

If you're using an OpenClaw agent that supports skill middleware auto-loading:

```bash
clawhub install clawsaver
```

That's it. The agent automatically:
1. Detects the skill
2. Wraps message handlers with batching
3. Logs metrics to your session

**No code changes needed.**

---

## Cleanup & Graceful Shutdown

Before shutdown, flush pending messages:

```javascript
import { flushAllSessions } from 'clawsaver/example-integration.js';

process.on('SIGTERM', () => {
  flushAllSessions('shutdown');
  process.exit(0);
});
```

---

## Typical Savings Timeline

**Day 1:** Basic buffering enabled → 20–25% reduction  
**Week 1:** Tuned to message patterns → 28–35% reduction  
**Month 1:** Optimized profile + routing → 35–40% reduction  

Savings compound as you understand your traffic better.

---

## Troubleshooting

**Q: Messages feel slow**  
A: Lower `debounceMs` (200-400ms instead of 800ms). Trade: fewer savings (5-15% instead of 20-40%).

**Q: Not seeing savings**  
A: Check if messages are actually being sent. Run metrics reporter. Ensure handler is being called.

**Q: Need immediate flush (e.g., timeout)**  
A: `debouncer.forceFlush('timeout')` sends pending batch now.

---

## Next Steps

- **Production setup:** Use profile-based config above
- **Fine-tuning:** Enable metrics, adjust `debounceMs` based on your patterns
- **Integration:** See `example-integration.js` for full code
- **Monitoring:** Log `debouncer.getState()` to your observability platform
