---
name: clawmem
description: Lightweight memory management system for OpenClaw with 3-tier retrieval (L0/L1/L2), automatic lifecycle monitoring, and advanced search. Saves 60-80% on token costs while providing efficient memory storage and retrieval.
---

# ClawMem Skill - OpenClaw Memory Management

## Overview

ClawMem is a lightweight memory management system designed for OpenClaw agents. It provides efficient memory storage and retrieval with significant token cost optimization.

## Features

- 🎯 **3-Tier Retrieval** - L0 Index → L1 Timeline → L2 Details
- 👁️ **Automatic Lifecycle Monitoring** - Intercepts 5 key OpenClaw events
- 💰 **Token Optimization** - Save 60-80% on token costs
- 🔍 **Advanced Search** - Keyword/Time/Tag/Session search
- 🗄️ **SQLite Storage** - High performance, easy deployment

## Quick Start

### 1. Install Dependencies

```bash
cd /root/.openclaw/workspace/projects/clawmem
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Initialize Database

```bash
npm run db:init
```

### 4. Use in OpenClaw

```javascript
import clawMem from './projects/clawmem/src/index.js';

// Store memory
const recordId = clawMem.storeL0({
  category: 'session',
  summary: 'User queried TSLA stock',
  timestamp: Math.floor(Date.now() / 1000)
});

// Retrieve memory
const result = await clawMem.retrieve({
  category: 'session',
  includeTimeline: true,
  limit: 10
});
```

## Usage Examples

### Store Memory

```javascript
// L0 Index (minimal)
clawMem.storeL0({
  category: 'session',
  summary: 'Short summary (< 100 chars)',
  timestamp: Date.now()
});

// L1 Timeline (semantic)
clawMem.storeL1({
  record_id: recordId,
  session_id: 'session_001',
  event_type: 'query',
  semantic_summary: 'Detailed summary (< 500 chars)',
  tags: ['tag1', 'tag2']
});

// L2 Details (full content, on-demand)
clawMem.storeL2({
  record_id: recordId,
  full_content: 'Full content',
  metadata: { key: 'value' }
});
```

### Search Memory

```javascript
import { memorySearch } from './projects/clawmem/src/index.js';

// Keyword search
const results = memorySearch.searchByKeyword('keyword', {
  category: 'session',
  limit: 10
});

// Time range search
const results = memorySearch.searchByTimeRange({
  start: oneHourAgo,
  end: Date.now() / 1000
});

// Session search
const session = memorySearch.searchBySession('session_001', {
  includeDetails: true
});

// Advanced search
const result = await memorySearch.advancedSearch({
  keyword: 'stock',
  timeRange: { start, end },
  includeDetails: true,
  limit: 10
});
```

### Lifecycle Monitoring

```javascript
import { lifecycleMonitor } from './projects/clawmem/src/index.js';

// Start monitoring
lifecycleMonitor.start();

// Intercept events
lifecycleMonitor.intercept('tool.call', {
  tool_name: 'yahoo_finance',
  args: { symbol: 'AAPL' }
});
```

## Configuration

Edit `.env` file:

```bash
# Database
DATABASE_PATH=./clawmem.db
DATABASE_WAL_MODE=true

# L0/L1/L2 Limits
L0_MAX_SUMMARY_LENGTH=100
L1_MAX_SUMMARY_LENGTH=500

# Worker Interval
WORKER_INTERVAL_MS=1000

# LLM Configuration
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
```

## API Reference

### ClawMemCore

- `storeL0(record)` - Store minimal index
- `storeL1(record)` - Store timeline index
- `storeL2(record)` - Store full details
- `retrieve(query)` - 3-tier retrieval workflow

### MemorySearch

- `searchByKeyword(keyword, options)` - Keyword search
- `searchByTimeRange(timeRange, options)` - Time-based search
- `searchByTags(tags, options)` - Tag-based search
- `searchBySession(sessionId, options)` - Session search
- `advancedSearch(query)` - Combined search
- `getStats()` - Get statistics

### LifecycleMonitor

- `start()` - Start monitoring
- `intercept(eventName, payload)` - Intercept event

## Performance

| Metric | Value |
|--------|-------|
| L0 Search | < 10ms |
| L1 Search | < 50ms |
| L2 Search | < 100ms |
| Token Savings | 60-80% |

## Token Optimization

**Traditional:** 100 records × 500 tokens = 50,000 tokens

**ClawMem:**
- L0: 100 × 25 = 2,500 tokens
- L1: 50 × 125 = 6,250 tokens
- L2: 10 × 500 = 5,000 tokens
- **Total:** 13,750 tokens (72.5% savings!)

## Project Structure

```
clawmem/
├── src/
│   ├── core/
│   │   ├── retrieval.js
│   │   ├── lifecycle-monitor.js
│   │   └── search.js
│   └── index.js
├── database/
│   └── init.js
├── config/
│   └── loader.js
├── docs/
├── .env.example
├── package.json
└── README.md
```

## License

MIT License

## Author

PocketAI for Leo - OpenClaw Community

## Repository

https://github.com/leohuang8688/clawmem
