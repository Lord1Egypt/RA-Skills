
# Pricing & Cost Optimization

## Cache Break-Even Analysis

Cache writes cost ~25% MORE than regular input tokens, but cache reads cost 90% LESS. It pays off after just 1–2 reuses.

**Formula:**
```text
break_even_reads = cache_write_cost / (regular_cost - cache_read_cost)
```

**Example — 10k token system prompt on Sonnet:**
- Regular cost per read: 10k × $3/M = **$0.030**
- Cache write cost: 10k × $3.75/M = **$0.0375** (one-time)
- Cache read cost: 10k × $0.30/M = **$0.003**
- Break-even: $0.0375 / ($0.030 - $0.003) = **1.4 reads**

→ If you reuse that context 2+ times, caching wins. Always cache anything used more than once.

---

## Current Pricing (March 2026)

### Input & Output Tokens

| Model | Input | Output | Cache Write | Cache Read |
|-------|-------|--------|-------------|------------|
| Haiku 4.5 | $0.80/M | $4/M | $1/M (1.25×) | $0.08/M (0.1×) |
| Sonnet 4.6 | $3/M | $15/M | $3.75/M (1.25×) | $0.30/M (0.1×) |
| Opus 4.6 | $15/M | $75/M | $18.75/M (1.25×) | $1.50/M (0.1×) |

*All prices in USD per million tokens*

---

## Cache Economics

### Break-Even Analysis

**Question:** When is prompt caching worth it?

**Answer:** After 1–2 cache reads, assuming the cached content is 1KB+.

#### Example: 5,000-token System Prompt with Sonnet

| Operation | Tokens | Rate | Cost |
|-----------|--------|------|------|
| Initial write | 5,000 | $3.75/M | $0.01875 |
| Read 1 | 5,000 | $0.30/M | $0.00150 |
| Read 2 | 5,000 | $0.30/M | $0.00150 |
| Read 3 | 5,000 | $0.30/M | $0.00150 |
| **Total for 3 reads** | — | — | **$0.02325** |

**vs. No Cache (3 reads):**
- 3 × 5,000 tokens = 15,000 tokens at $3/M = $0.045

**Savings: 48%** (after write cost)

### Large Codebase Cache (50,000 tokens)

| Operation | Cost (Sonnet) |
|-----------|-------|
| Write (50K tokens) | $0.1875 |
| Read 1 | $0.0150 |
| Read 2 | $0.0150 |
| Read 10 | $0.0150 |
| **Total 10 reads** | **$0.2475** |

**vs. No Cache:**
- 10 × 50,000 tokens at $3/M = $1.50

**Savings: 83.5%**

---

## Model Selection Savings

### Simple Task: Code Formatting (1K input, 500 output)

| Model | Cost | Overspend |
|-------|------|-----------|
| **Haiku** (optimal) | $0.0044 | — |
| Sonnet | $0.0105 | 2.4× |
| Opus | $0.0225 | 5.1× |

### Medium Task: Refactoring (10K input, 2K output)

| Model | Cost | Overspend |
|-------|------|-----------|
| Haiku | $0.0168 | 1.9× |
| **Sonnet** (optimal) | $0.0345 | — |
| Opus | $0.225 | 6.5× |

### Hard Task: Architecture Review (20K input, 3K output)

| Model | Cost | Underspend |
|-------|------|-----------|
| Haiku | $0.0452 | ⚠️ Too weak |
| Sonnet | $0.0795 | ⚠️ Marginal |
| **Opus** (optimal) | $0.375 | — |

**Key insight:** Using Opus for simple tasks costs **10–18× more**. Always classify first.

---

## Batching Savings

### Scenario: 100 Code Reviews

**Option 1: Synchronous (100 separate calls)**
- 100 × (1K input, 500 output) at Sonnet
- Cost: 100 × $0.00345 = **$0.345**
- Overhead: ~100 HTTP round-trips

**Option 2: One batched call (combine in prompt)**
- 100K input, 50K output at Sonnet
- Cost: **$0.315**
- Savings: 8.7%
- Benefit: 100× fewer API calls

**Option 3: Batch API (async, 50% discount)**
- Same tokens, 50% discount
- Cost: **$0.158**
- Savings: 54.2% vs sync, 68.5% vs separate
- Trade-off: Results in ~1 hour (non-urgent work)

---

## Combined Optimization Scenario

### Project: CI/CD bot reviewing 50 PRs daily

**Base case (unoptimized):**
- Task: Review PR code (5–10K tokens per PR)
- Model: Opus (overspecified)
- No caching, separate API calls
- No batching

```text
50 PRs × 8K input + 2K output per PR
Model: Opus at 50 separate calls
Cost per day: 50 × $0.075 = $3.75
Cost per month: ~$112.50
```

**Optimized approach:**
1. **Model selection** → Use Sonnet (5.0× cheaper than Opus for this task)
2. **Prompt caching** → Cache style guide + review checklist (2K tokens)
3. **Batching** → Group 5 PRs per batch API call
4. **Local caching** → Skip re-reviews of unchanged commits

```text
Breakdown:
- System prompt cache (write once): 2K at $3.75/M = $0.0075
- Per-batch call: 5 PRs × 8K input = 40K tokens
- Batch API (50% discount): (40K × $3 + 10K × $15) / 1M × 0.5 = $0.135/batch
- 10 batches/day: 10 × $0.135 = $1.35/day
- Local cache hits (30% of PRs are re-reviews): saves ~$0.20/day

Cost per day: $1.35
Cost per month: ~$40.50
Savings: 64% reduction
```

---

## Rate Limits & Cost Impact

### Avoiding Rate Limit Cascades

High-frequency requests (>1K calls/min) trigger rate limiting (429 errors).

**Uncached approach:**
- Make 100 calls/minute → Hit rate limit
- Retry with backoff → Waste tokens on failed attempts
- Effective cost: Higher than optimized

**Cached approach:**
- Cache reduces actual API calls by 70–80%
- Fewer calls = Less likely to hit rate limits
- Exponential backoff costs far less

### Example: 1,000 requests/hour

**Without optimization:**
- All 1,000 call API
- ~5–10% hit rate limits and retry
- Wasted tokens on failures: ~50–100 calls
- Extra cost: $0.15–$0.30

**With caching + model selection:**
- 700 requests cached (no API call)
- 300 API calls (200 Haiku, 100 Sonnet)
- No rate limit hits
- Actual cost: $0.12–$0.15 for 1,000 logical requests

---

## Cost Tracking Template

Log all requests to measure savings over time.

```text
timestamp | model | input_tokens | output_tokens | cache_read | cache_write | cost_usd | task_type
2026-03-29 10:00:00 | haiku | 1200 | 500 | 0 | 2500 | 0.0048 | format
2026-03-29 10:01:15 | sonnet | 8000 | 2000 | 5000 | 0 | 0.0243 | refactor
2026-03-29 10:02:30 | opus | 20000 | 3000 | 10000 | 0 | 0.3225 | audit
```

**Monthly analysis:**
- Sum all costs
- Group by model (should be 60%+ Haiku + Sonnet)
- Track cache hit ratio (aim for >50% on repeated work)
- Compare to budget/baseline

---

## Savings Formula

**Expected savings from optimization:**

```text
Savings % = (C_base - C_opt) / C_base × 100

Where:
  C_base = Cost of unoptimized (all Opus, no caching, separate calls)
  C_opt = Cost with model selection + caching + batching
```

**Typical results:**
- **Model selection alone:** 50–70% savings
- **+ Caching:** 70–85% savings
- **+ Batching + Local cache:** 70–90% savings

**Example benchmark:**
- Unoptimized: 1M input + 100K output tokens/month at Opus = $15.75
- Optimized (mixed models + cache): 1M input + 100K output mixed = $3.50–$4.70
- **Savings: 70–77%**
