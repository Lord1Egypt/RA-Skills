---
name: durable-workflow
description: |
  Patterns and procedures for building AI agent workflows that survive real-world failures. Use when asked to build a multi-step automation, pipeline, or agent workflow — especially when it involves external APIs, file operations, long-running tasks, or anything that must not lose state. Triggers on: "automate", "pipeline", "workflow", "agent loop", "multi-step", "background task", "retry", "error handling", "won't lose progress", "keeps failing", "handle errors", "resilient", or any request to build an automation that must stay running.
---

# Durable Workflow Patterns

Build automations that survive API failures, timeouts, and unexpected state — without rebuilding from scratch every time something breaks.

## Core Principle

Every step in a multi-step workflow must answer three questions:
1. **What did I finish?** (checkpoint)
2. **What do I do if this step fails?** (recovery)
3. **Who finds out if something goes wrong?** (alerting)

Skip any of these and the workflow will eventually fail silently.

## Scripts

Ready-to-use implementations in `scripts/`:

| Script | Purpose |
|--------|---------|
| `workflow-template.js` | Complete workflow skeleton with checkpoints, retry, DLQ, exit handler |
| `lock.js` | File-based process lock — prevents concurrent runs |

### workflow-template.js

Copy and fill in the step TODOs:

```bash
cp scripts/workflow-template.js my-workflow.js
node my-workflow.js           # Run (or re-run — resumes from last checkpoint)
WORKFLOW_STATE_PATH=/tmp/state.json node my-workflow.js   # Custom state path
```

Features: atomic state saves, exponential backoff, timeout wrapper, DLQ, abnormal-exit logging.

### lock.js

Prevent two instances of the same workflow from running at once:

```javascript
const { withLock, LockError } = require('./lock');

withLock('/tmp/my-workflow.lock', async () => {
  // Only one process runs this block at a time
  await runWorkflow();
}).catch(e => {
  if (e.name === 'LockError') {
    console.error('Already running:', e.message);
  } else {
    throw e;
  }
});
```

## Pattern 1: Checkpoint State

Save progress after every meaningful step. Never trust in-memory state across network calls.

```javascript
// checkpoint.js pattern
const state = loadState('workflow-id') || { step: 0, results: [] };

if (state.step < 1) {
  state.results.push(await fetchData());
  state.step = 1;
  saveState('workflow-id', state);
}
if (state.step < 2) {
  state.results.push(await processData(state.results[0]));
  state.step = 2;
  saveState('workflow-id', state);
}
// Restart from any step — already-done steps are skipped
```

## Pattern 2: Circuit Breaker

Stop hammering a failing service. Open the circuit after N failures, half-open after a cooldown.

```javascript
class CircuitBreaker {
  constructor(threshold = 3, cooldownMs = 30000) {
    this.failures = 0; this.threshold = threshold;
    this.state = 'closed'; this.nextRetry = 0;
  }
  async call(fn) {
    if (this.state === 'open') {
      if (Date.now() < this.nextRetry) throw new Error('Circuit open');
      this.state = 'half-open';
    }
    try {
      const result = await fn();
      this.failures = 0; this.state = 'closed';
      return result;
    } catch (e) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.state = 'open';
        this.nextRetry = Date.now() + this.cooldownMs;
      }
      throw e;
    }
  }
}
```

## Pattern 3: Exponential Backoff with Jitter

```javascript
async function withRetry(fn, maxAttempts = 4, baseDelayMs = 1000) {
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try { return await fn(); }
    catch (e) {
      if (attempt === maxAttempts - 1) throw e;
      const delay = baseDelayMs * Math.pow(2, attempt) + Math.random() * 500;
      await new Promise(r => setTimeout(r, delay));
    }
  }
}
```

## Pattern 4: Dead Letter Queue

When a step fails after all retries, don't silently drop it. Route it somewhere reviewable.

```javascript
async function processWithDLQ(items, processFn, dlqPath) {
  const failed = [];
  for (const item of items) {
    try { await withRetry(() => processFn(item)); }
    catch (e) { failed.push({ item, error: e.message, failedAt: new Date() }); }
  }
  if (failed.length) {
    const existing = fs.existsSync(dlqPath) ? JSON.parse(fs.readFileSync(dlqPath)) : [];
    fs.writeFileSync(dlqPath, JSON.stringify([...existing, ...failed], null, 2));
  }
}
```

## Pattern 5: Idempotent Operations

Design every step so running it twice produces the same result as running it once.

```javascript
// BAD: running twice creates two records
await db.insert({ id: uuid(), data });

// GOOD: upsert on natural key
await db.upsert({ id: deterministicId(data), data }, { onConflict: 'update' });
```

## Pattern 6: Instance Lock

Prevent duplicate runs (e.g. cron overlap, manual re-trigger while running).

```javascript
const { withLock, LockError } = require('./scripts/lock');

const LOCK_PATH = '/tmp/my-workflow.lock';

async function main() {
  await withLock(LOCK_PATH, async () => {
    // Safe: only one instance reaches here at a time
    await runWorkflow();
  });
}

main().catch(e => {
  if (e.name === 'LockError') {
    // Not an error — just another instance running
    console.log(`Skipping: ${e.message}`);
    process.exit(0);
  }
  console.error('Fatal:', e.message);
  process.exit(1);
});
```

The lock uses PID detection — stale locks from crashed processes are automatically reclaimed.

## Workflow Design Checklist

Before shipping any multi-step automation:
- [ ] Each step saves state before moving to the next
- [ ] External API calls wrapped in retry + backoff
- [ ] Circuit breaker on services called more than once per run
- [ ] Failed items go to a dead letter file/queue, not `/dev/null`
- [ ] The workflow can restart from any step without duplicating completed work
- [ ] Alerting fires when the workflow exits abnormally (not just on exception)
- [ ] Timeouts set on all external calls (never `await fetch()` without a deadline)
- [ ] Instance lock in place if triggered by cron or multiple callers

## Alerting

Send a Telegram message on workflow failure so you know before you look. Uses only the `https` built-in.

Set env vars: `ALERT_TELEGRAM_TOKEN` and `ALERT_CHAT_ID`.

```javascript
const https = require('https');

function sendTelegramAlert(message) {
  const token  = process.env.ALERT_TELEGRAM_TOKEN;
  const chatId = process.env.ALERT_CHAT_ID;
  if (!token || !chatId) return Promise.resolve(); // alerting not configured, skip silently

  const body = JSON.stringify({ chat_id: chatId, text: message, parse_mode: 'Markdown' });
  return new Promise((resolve) => {
    const req = https.request(
      {
        hostname: 'api.telegram.org',
        path: `/bot${token}/sendMessage`,
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
      },
      res => { res.resume(); res.on('end', resolve); }
    );
    req.on('error', () => resolve()); // don't let alert failure crash the workflow
    req.setTimeout(5000, () => { req.destroy(); resolve(); });
    req.write(body);
    req.end();
  });
}

// Usage — in your main() catch block:
main().catch(async e => {
  console.error('Fatal:', e.message);
  await sendTelegramAlert(`❌ *Workflow failed*\n\`${e.message}\``);
  process.exit(1);
});
```

## Common Failure Modes

See `references/failure-taxonomy.md` for a full catalog of agent workflow failures with diagnosis and fix patterns.
