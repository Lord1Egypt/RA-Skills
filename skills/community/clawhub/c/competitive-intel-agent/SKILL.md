---
name: competitive-intel-agent
version: 1.0.0
description: >
  Competitor monitoring, pricing analysis, market positioning, and SWOT generation.
  Use when you need to track competitor moves, benchmark pricing, analyze market
  positioning, or generate structured competitive intelligence reports.
  NOT for: financial forecasting (use startup-financial-model), legal/IP research
  (use contract-review-agent), or real-time stock/crypto data.
metadata:
  openclaw:
    requires:
      bins: []
    tags:
      - competitive-intelligence
      - market-research
      - strategy
      - business-analysis
      - pricing
---

# Competitive Intel Agent

Competitive intelligence gathering and analysis system. Monitors competitor websites, pricing pages, product launches, job postings, and press coverage — then synthesizes into actionable SWOT reports, positioning maps, and pricing benchmarks.

## When To Use

- Tracking a specific competitor's product updates, pricing changes, or messaging shifts
- Benchmarking your pricing against 3–10 competitors before a repricing decision
- Building a SWOT analysis for a board deck, investor update, or strategic planning session
- Monitoring job postings to infer a competitor's hiring direction (e.g., they're hiring ML engineers → new AI feature coming)
- Summarizing recent press coverage or funding news for a competitor set
- Generating a market map / positioning matrix

## When NOT To Use

- Financial forecasting or runway analysis → use `startup-financial-model`
- Contract or legal clause review → use `contract-review-agent`
- Real-time stock prices, crypto prices, or SEC filings → use a dedicated financial data source
- Deep keyword/SEO research → use `seo-forge` or `seo-health`
- Customer sentiment or NPS analysis (different data source, different workflow)

---

## Capabilities

### 1. Competitor Profile Builder

Scrape and structure a competitor's public-facing profile:

```
Gather a competitor profile for [CompanyName]:
- Website URL: [url]
- Pricing page: [url or "find it"]
- Focus: pricing tiers, key features, target customer, positioning statement
- Output: structured markdown profile
```

**What it extracts:**
- Product/service tiers and price points
- Target customer segment (SMB, enterprise, developer, etc.)
- Core value proposition and messaging angle
- Key integrations and platform plays
- Recent product announcements (blog, changelog, press)

---

### 2. Pricing Benchmark Analysis

Compare your pricing against a competitor set:

```
Benchmark our pricing against competitors:
- Our product: [describe tiers + prices]
- Competitors: [list 3-6 with URLs or names]
- Output: comparison table + positioning recommendation
```

**Output format:**
```
| Competitor | Entry Tier | Mid Tier | Enterprise | Pricing Model | Notes |
|------------|-----------|----------|------------|---------------|-------|
| Us         | $49/mo    | $149/mo  | Custom     | Per seat      |       |
| Comp A     | $39/mo    | $129/mo  | $499/mo    | Per seat      | Cheaper entry |
| Comp B     | Free      | $99/mo   | Custom     | Usage-based   | OSS play |
```

Includes: pricing model analysis (seat vs usage vs flat), value gap identification, where we're over/underpriced.

---

### 3. SWOT Analysis Generator

Generate a structured SWOT for your company vs. a competitor or market segment:

```
Generate a SWOT analysis for [OurCompany] vs [Competitor/Market]:
- Our strengths: [list or "infer from context"]
- Their public positioning: [url or description]
- Market context: [1-2 sentences]
- Output: SWOT matrix + 3 strategic recommendations
```

**Output structure:**
```
## SWOT: [OurCompany] vs [Competitor]

### Strengths
- [S1] Deep accounting integrations (QBO, Xero) — competitors lack this depth
- [S2] ...

### Weaknesses
- [W1] Limited brand recognition vs. incumbent
- [W2] ...

### Opportunities
- [O1] SMB segment underserved by enterprise-priced tools
- [O2] ...

### Threats
- [T1] Competitor just raised $20M Series A — expect aggressive expansion
- [T2] ...

### Strategic Recommendations
1. Double down on [strength] to widen moat in [segment]
2. Address [weakness] before [threat] materializes
3. Move fast on [opportunity] — 6-month window before competition catches up
```

---

### 4. Job Posting Signal Analysis

Read competitor job postings to infer strategic direction:

```
Analyze job postings from [CompanyName] to infer strategic priorities:
- Source: [LinkedIn/Greenhouse URL or "search for them"]
- Time window: last 30-90 days
- Output: signal map of where they're investing
```

**Signal patterns to watch:**
- Heavy ML/AI hiring → new AI feature in 6-12 months
- Sales hiring in [region] → geographic expansion
- "Head of Enterprise" → moving upmarket
- DevRel/Developer Advocate → building a platform/ecosystem play
- CFO/Controller hiring → fundraise or acquisition prep

---

### 5. Press & Funding Monitor

Track competitor news, funding rounds, and announcements:

```
Monitor recent news for [Company1, Company2, Company3]:
- Time window: last [30/60/90] days
- Sources: TechCrunch, Crunchbase, company blog, PR Newswire
- Output: bullet summary + significance rating (High/Medium/Low)
```

**Significance ratings:**
- **High:** New funding, major product launch, acquisition, leadership change
- **Medium:** Partnership, customer win, pricing change, new market entry
- **Low:** Awards, speaking slots, minor feature releases

---

### 6. Positioning Matrix

Map competitors on a 2×2 or 3-axis positioning matrix:

```
Build a positioning matrix for the [market segment] market:
- Axes: [e.g., Price vs. Features] or [e.g., SMB-focus vs. Enterprise-focus, Simple vs. Powerful]
- Competitors to include: [list or "find top players"]
- Output: text-based matrix + narrative positioning analysis
```

**Example output:**
```
                    HIGH PRICE
                        |
          [CompA]       |    [CompB]
  SIMPLE ————————————+————————————— POWERFUL
          [Us]         |    [CompC]
                        |
                    LOW PRICE

Narrative: We occupy the SMB sweet spot — more powerful than CompA but cheaper
than CompC. The open gap is mid-market buyers who need power without enterprise
pricing. CompB owns enterprise; we should own $10K-$50K ACV.
```

---

## Workflow: Full Competitive Teardown

For a complete competitive analysis before a pricing or strategy meeting:

```
Run a full competitive teardown on [CompanyName]:
1. Build their company profile (website, pricing, positioning)
2. Benchmark their pricing against ours
3. Analyze recent job postings for strategic signals
4. Pull 90 days of press/news
5. Generate SWOT: us vs. them
6. Output: executive summary (1 page) + full report appendix
```

---

## Data Sources (Public Only)

All intelligence gathering uses publicly available sources:
- Company websites and pricing pages
- LinkedIn job postings (public)
- Crunchbase / PitchBook public profiles
- G2, Capterra, Trustpilot reviews
- TechCrunch, ProductHunt, HackerNews
- GitHub (for open-source projects)
- Twitter/X, LinkedIn company pages
- SEC EDGAR (for public companies)
- Google News search

**Never:** scrape behind login walls, access private data, or use data obtained unethically.

---

## Output Formats

| Use Case | Format |
|----------|--------|
| Board / investor deck | Executive summary (300-500 words) + SWOT matrix |
| Internal strategy session | Full report with all sections |
| Quick check | Bullet briefing (5-10 bullets) |
| Pricing decision | Comparison table + recommendation memo |
| Regular monitoring | Weekly digest format (What Changed / Why It Matters / Recommended Action) |

---

## Weekly Monitoring Setup

For ongoing competitive monitoring, set up a cron job:

```
Schedule: Every Monday 8 AM
Task: Pull competitive intel digest for [CompanyA, CompanyB, CompanyC]
- New job postings (significant hires only)
- News mentions (High/Medium significance only)
- Pricing or product page changes
- Output: Slack/Discord digest message
```

---

## Examples

### Quick pricing check
```
Benchmark our accounting software pricing ($49/$149/custom) against 
FreshBooks, Wave, and Xero. Focus on SMB tiers. Output a comparison table 
and tell me if we're positioned correctly.
```

### Pre-meeting teardown
```
I have a sales call with a prospect who uses QuickBooks. Give me a competitive 
teardown: where we're stronger, where they're stronger, and the top 3 objections 
I'll face with suggested responses.
```

### Strategic SWOT
```
Generate a SWOT for PrecisionLedger entering the crypto accounting space. 
Competitors: Koinly, CoinTracker, TaxBit. Our advantage: human CPA + AI hybrid. 
Output: board-ready SWOT with 3 strategic recommendations.
```

---

## Integration with Other Skills

- **startup-financial-model**: Use competitive pricing data to validate revenue assumptions
- **kpi-alert-system**: Set alerts when monitored competitor triggers a significant news event
- **cap-table-manager**: Cross-reference competitor funding rounds with dilution modeling
- **solidity-audit-precheck**: For Web3 protocol competitors, analyze on-chain data
- **erc20-tokenomics-builder**: Benchmark token allocation models against comparable projects
