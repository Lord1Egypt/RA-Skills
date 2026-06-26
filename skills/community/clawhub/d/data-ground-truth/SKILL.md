---
name: data-ground-truth
description: Before presenting numbers in reports or recommendations, verify facts and check values against industry baselines.
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://agentutil.net
    always: false
---

# data-ground-truth

When presenting numbers, metrics, or statistics in reports, recommendations, or analysis — verify the facts and contextualize the figures against industry baselines. Combines verify (live fact-checking) with norm (statistical benchmarking).

## When to Activate

Use this skill when:

- Writing a report that cites specific metrics (revenue, churn, conversion rates)
- A user shares their business numbers and asks "is this good?"
- Comparing a metric to industry standards ("how does our 5% churn compare?")
- Building a recommendation that depends on current market data
- Presenting financial figures that may have changed since training
- Analyzing a dataset and wanting to flag outliers against known baselines

**Do NOT use for:** opinions, qualitative assessments, or metrics with no established baseline.

## Workflow

### Step 1: Classify the data point

Determine whether each number is:
- **A factual claim** (exchange rate, stock price, population) → route to **verify**
- **A business/performance metric** (churn rate, NPS, response time) → route to **norm**
- **Both** (e.g., "our conversion rate of 3.2% is above average") → check both

### Step 2: Verify factual claims

For current facts (prices, rates, dates), use verify-claim.

**MCP (preferred):** `verify_claim({ claim: "The USD to EUR exchange rate is 0.92" })`

**HTTP:**
```bash
curl -X POST https://verify.agentutil.net/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "The USD to EUR exchange rate is 0.92"}'
```

Handle verdicts per the verify-claim decision tree (confirmed → use, stale → update, disputed → present both sides, false → correct).

### Step 3: Benchmark metrics against baselines

For business metrics, check where the value falls on the distribution.

**MCP (preferred):** `norm_check({ category: "saas:churn_rate_monthly", value: 5.2, unit: "%" })`

**HTTP:**
```bash
curl -X POST https://norm.agentutil.net/v1/check \
  -H "Content-Type: application/json" \
  -d '{"category": "saas:churn_rate_monthly", "value": 5.2, "unit": "%"}'
```

For multiple metrics at once:
```bash
curl -X POST https://norm.agentutil.net/v1/batch \
  -H "Content-Type: application/json" \
  -d '{"items": [{"category": "saas:churn_rate_monthly", "value": 5.2}, {"category": "saas:nps_score", "value": 45}]}'
```

Optional: add `company_size` (startup/smb/mid_market/enterprise) and `region` for more specific baselines.

### Step 4: Present with context

When reporting findings, combine verification and benchmarking:

| Data type | How to present |
|-----------|---------------|
| Verified fact | "The current [metric] is [current_truth] (verified live, [freshness])." |
| Benchmarked metric | "[Value] is at the [percentile]th percentile — [assessment] for [category]." |
| Both | "At [current_truth] (verified), this is [percentile]th percentile vs. industry ([baseline source])." |
| Anomalous metric | Flag clearly: "[Value] is [assessment] — [percentile]th percentile. The typical range is [p25]-[p75]." |

Assessment values from norm: `very_low`, `low`, `normal`, `high`, `very_high`, `anomalous`.

### Available baseline categories

121 baselines across 14 domains. Browse with:
```bash
curl https://norm.agentutil.net/v1/categories
```

Common categories: `saas:churn_rate_monthly`, `saas:nps_score`, `saas:ltv_cac_ratio`, `ecommerce:cart_abandonment_rate`, `infrastructure:api_latency_p99`, `infrastructure:uptime_percentage`.

## Data Handling

This skill sends claims (natural language text) and metric values (category identifiers + numbers) to two external APIs. No documents, user data, or file contents are transmitted.

## Pricing

- Verify: 25 free/day, then $0.004/query
- Norm: free category listing, $0.002/check or $0.001/batch item
- Full ground-truth check (verify + norm): ~$0.006 per data point

All via x402 protocol (USDC on Base). No authentication required for free tiers.

## Privacy

No personal data collected. Claims cached up to 1 hour (verify), metric checks are stateless (norm). Rate limiting uses IP hashing only.
