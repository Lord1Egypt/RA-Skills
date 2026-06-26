---
name: fast-response-optimizer
description: Response speed optimizer - implements reply-first-then-process, parallel tool calls, and memory file caching
version: 1.0.0
author: opendolph
source: https://github.com/opendolph/skills/tree/main/fast-response-optimizer
---

# Fast Response Optimizer ⚡

> Reduce response time from 5-20 seconds to under 1 second

---

## Core Optimization Strategies

### 1. Reply First, Process Later

**Rule:**
- Receive request → Immediately reply "Received/Processing" → Execute in background → Push result when done

**Implementation:**
```javascript
// Quick reply
await message.send("Received, processing...");

// Background execution
const result = await processInBackground(task);

// Push result
await message.send(result);
```

### 2. Parallel Tool Execution

**Rule:**
- Execute independent tool calls in parallel instead of waiting sequentially

**Implementation:**
```javascript
// Before (sequential)
const result1 = await toolA();
const result2 = await toolB();
const result3 = await toolC();

// After (parallel)
const [result1, result2, result3] = await Promise.all([
  toolA(),
  toolB(),
  toolC()
]);
```

### 3. Memory File Caching

**Rule:**
- Load cache every 1 minute via scheduled task
- Reload cache if more than 1 minute since last message
- Cache stored in SESSION-STATE.md

**Implementation:**
```javascript
// Cache structure
const cache = {
  lastUpdate: timestamp,
  userProfile: {...},
  memorySummary: {...},
  skills: [...]
};

// Check if refresh needed
if (now - lastMessage > 60000 || now - cache.lastUpdate > 60000) {
  await refreshCache();
}
```

---

## Trigger Conditions

| Scenario | Trigger Method |
|----------|----------------|
| Auto-trigger | Execute on every message processing |
| Scheduled refresh | Cron job every 1 minute |
| Manual trigger | User inputs "refresh cache" |

---

## Cache Files

```
SESSION-STATE.md          # Active state + cache
├── cache/               # Cache directory
│   ├── user_profile.json    # User profile cache
│   ├── memory_summary.json  # Memory summary cache
│   └── skills_list.json     # Skills list cache
└── last_refresh.txt     # Last refresh timestamp
```

---

## Performance Goals

| Metric | Before | After |
|--------|--------|-------|
| First Response | 5-20s | <1s |
| Tool Calls | Sequential accumulation | Parallel execution |
| File Reading | Read every time | Cache hit |
| Cache Refresh | None | Every 1 min / >1 min |

---

## Usage

```bash
# Initialize optimizer
node skills/fast-response-optimizer/bootstrap.js

# Manual cache refresh
node skills/fast-response-optimizer/scripts/cache-manager.js refresh

# Check cache status
node skills/fast-response-optimizer/scripts/cache-manager.js status

# Update message timestamp
node skills/fast-response-optimizer/scripts/cache-manager.js message
```

---

*Make every response lightning fast ⚡*
