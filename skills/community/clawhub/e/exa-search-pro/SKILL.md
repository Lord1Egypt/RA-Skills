---
name: Exa Search
description: >
  Advanced web search with precise date filtering and content type selection. Use when
  you need academic papers, GitHub repositories, research content, or specific date ranges.
  Handles neural search (semantic understanding), keyword search, and content type filtering
  (research papers, GitHub, news, PDFs). Perfect for research, competitive analysis, and
  content discovery.
metadata:
  requires:
    env:
      - CLAW0X_API_KEY
---

# Exa Search

**Cloud skill by [Claw0x](https://claw0x.com)** — powered by Claw0x Gateway API.

Advanced web search with precise date filtering, content type selection, and neural search. Perfect for research, competitive analysis, and specialized content discovery.

> **Requires Claw0x API key.** Sign up at [claw0x.com](https://claw0x.com) to get your key.

## Prerequisites

1. **Sign up at [claw0x.com](https://claw0x.com)**
2. **Create API key** in Dashboard
3. **Set environment variable**:
   ```bash
   # Add to ~/.openclaw/.env
   CLAW0X_API_KEY=ck_live_...
   ```

## Pricing

**$0.005 per successful call.** Failed calls are free.

- Pay only for successful responses (2xx status)
- No monthly fees, no subscriptions
- Get started with $5 free credit

## Quick Reference

| When This Happens | Do This | What You Get |
|-------------------|---------|--------------|
| Need academic papers from specific dates | Use `category: "research paper"` + date range | Filtered research results |
| Find GitHub projects from 2024 | Use `category: "github"` + `start_published_date: "2024-01-01"` | Recent open-source projects |
| Semantic search for concepts | Use `search_type: "neural"` | Intent-based results |
| Exact keyword matching | Use `search_type: "keyword"` | Traditional search results |

## 5-Minute Quickstart

### Step 1: Get API Key (30 seconds)
Sign up at [claw0x.com](https://claw0x.com) → Dashboard → Create API Key

### Step 2: Set Environment Variable (30 seconds)
```bash
export CLAW0X_API_KEY="ck_live_..."
```

### Step 3: Install Skill (30 seconds)
```bash
openclaw skills install exa-search
```

### Step 4: Use Skill (1 minute)
```typescript
const result = await agent.run('exa-search', {
  query: 'transformer architecture improvements',
  category: 'research paper',
  start_published_date: '2024-01-01',
  end_published_date: '2024-03-31',
  search_type: 'neural',
  num_results: 5
});

console.log(`Found ${result.result_count} papers`);
result.results.forEach(paper => {
  console.log(`${paper.title} (${paper.published_date})`);
});
```

## Real-World Use Cases

### Scenario 1: Academic Research
**Problem**: Find transformer papers from Q1 2024
**Solution**: Use precise date filtering + research paper category
**Example**:
```typescript
{
  query: "transformer architecture improvements",
  category: "research paper",
  start_published_date: "2024-01-01",
  end_published_date: "2024-03-31"
}
```

### Scenario 2: GitHub Discovery
**Problem**: Find Rust web frameworks created in 2024
**Solution**: Use GitHub category + date filtering
**Example**:
```typescript
{
  query: "rust web framework",
  category: "github",
  start_published_date: "2024-01-01"
}
```

### Scenario 3: Competitive Analysis
**Problem**: Find similar companies in AI agent space
**Solution**: Use company category + domain exclusion
**Example**:
```typescript
{
  query: "AI agent platforms",
  category: "company",
  exclude_domains: ["competitor.com"]
}
```

## Integration Recipes

### OpenClaw Agent
```typescript
import { Claw0xClient } from '@claw0x/sdk';

const claw0x = new Claw0xClient(process.env.CLAW0X_API_KEY);

const papers = await claw0x.call('exa-search', {
  query: 'large language model reasoning',
  category: 'research paper',
  start_published_date: '2024-01-01',
  search_type: 'neural'
});
```

### LangChain Agent
```python
from claw0x import Claw0xClient

client = Claw0xClient(api_key=os.environ['CLAW0X_API_KEY'])

repos = client.call('exa-search', {
    'query': 'rust web framework',
    'category': 'github',
    'start_published_date': '2024-01-01'
})
```

### Custom Agent
```javascript
const response = await fetch('https://api.claw0x.com/v1/call', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.CLAW0X_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    skill: 'exa-search',
    input: {
      query: 'AI regulation news',
      category: 'news',
      start_published_date: '2024-03-15',
      end_published_date: '2024-03-22'
    }
  })
});
```

## Exa vs Tavily Comparison

| Feature | Tavily | Exa |
|---------|--------|-----|
| Date filtering | time_range (coarse) | start/end date (precise) |
| Search mode | basic/advanced (depth) | neural/keyword (algorithm) |
| Content types | general/news | 7+ types (papers, GitHub, PDF) |
| AI answer | ✅ Built-in | ❌ Not available |
| Best for | Quick lookups, general info | Research, specialized content |

**Use Tavily when**: You need a quick answer or general web search.

**Use Exa when**: You need precise dates, specific content types, or semantic search.

## Why Use Via Claw0x?

- **Unified billing**: One API key for all skills
- **Atomic pricing**: Pay per call, not per month
- **Zero cost on failure**: Failed calls don't charge
- **Production-ready**: 99.9% uptime, <100ms latency
- **Security scanned**: OSV.dev integration
- **No Exa API key needed**: Claw0x handles upstream authentication

## About Claw0x

[Claw0x](https://claw0x.com) is the native skills layer for AI agents — providing unified API access, atomic billing, and quality control.

**Explore more skills**: [claw0x.com/skills](https://claw0x.com/skills)

**GitHub**: [github.com/kennyzir/exa-search](https://github.com/kennyzir/exa-search)
