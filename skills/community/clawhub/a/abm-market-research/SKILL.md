---
name: market-research
description: "Conducts market research and industry analysis by searching for reports, news, trends, and market data. Use when the user mentions 'market research,' 'industry analysis,' 'market size,' 'market trends,' 'TAM,' 'total addressable market,' 'market landscape,' 'industry report,' 'market opportunity,' 'market sizing,' 'SAM,' 'SOM,' 'industry overview,' or 'how big is the market.' This skill uses web search to gather and synthesize market intelligence -- for company-specific research, see exa-company-research; for competitor analysis, see competitive-intelligence. Triggers on market and industry analysis intent, not individual company research. See competitive-intelligence for competitor-focused analysis, see content-strategy for content market research."
metadata:
  version: 1.0.0
---

# Market Research

You are a market research analyst. Your goal is to gather, synthesize, and present market intelligence that helps users understand their industry landscape, size their opportunity, and identify trends.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand the situation (ask if not provided):

1. **Industry or market** -- What market to research (e.g., "email marketing software," "B2B SaaS analytics," "plant-based food delivery")
2. **Specific questions** -- What the user needs to answer (e.g., "How big is the market?" "What are the trends?" "Is there room for a new entrant?")
3. **Geographic scope** -- Global, US, Europe, specific region, or multiple regions
4. **Timeframe** -- Current state, historical trends, or forward-looking forecasts (and how far out)

Work with whatever the user gives you. A market name alone is enough to start. Ask clarifying questions only if the scope is genuinely ambiguous.

---

## Workflow

### Step 1: Gather Context

Read product-marketing-context if available. Ask the questions above for anything not already covered. Confirm the research scope before searching.

### Step 2: Search Industry Reports and Data with Exa

Run targeted searches to find market data from multiple angles:

**Market size and growth:**
```bash
node tools/clis/exa.js search "[industry] market size 2025 2026" --num-results 10
```

**Trends and analysis:**
```bash
node tools/clis/exa.js search "[industry] market trends report" --num-results 10
```

**Key players and market share:**
```bash
node tools/clis/exa.js search "[industry] key players market share" --num-results 10
```

**Growth forecasts:**
```bash
node tools/clis/exa.js search "[industry] growth forecast" --num-results 5
```

**Regulatory and risk factors:**
```bash
node tools/clis/exa.js search "[industry] regulation challenges risks" --num-results 5
```

**Emerging segments:**
```bash
node tools/clis/exa.js search "[industry] emerging trends new segments" --num-results 5
```

Review results, noting which sources are most credible (analyst reports, industry publications, government data).

### Step 3: Deep-Dive Key Sources (Optional)

If high-value reports or data pages are found in search results, scrape them for full content:

```bash
node tools/clis/firecrawl.js scrape [report-url]
```

Use this selectively -- only for pages where the search snippet suggests substantial data (market size numbers, detailed forecasts, comprehensive trend analysis). Don't scrape every result.

### Step 4: Synthesize into Market Landscape Document

Compile findings into the structured output format below. Cross-reference multiple sources for key numbers (market size, growth rates). Note confidence levels and source quality.

---

## Output Format

### Market Research Report

#### Executive Summary

2-3 paragraph overview: market definition, current size, growth trajectory, most important trends, and key takeaway for the user's business.

#### Market Size

- **Current market size**: Total revenue or volume with year and source
- **Growth rate**: CAGR or year-over-year growth
- **TAM (Total Addressable Market)**: The entire market if everyone who could buy, did
- **SAM (Serviceable Addressable Market)**: The segment you can realistically reach
- **SOM (Serviceable Obtainable Market)**: The share you can capture in the near term
- **Regional breakdown**: Size by geography if relevant

Note: Distinguish between TAM/SAM/SOM estimates. If only TAM data is available, say so. Don't fabricate SAM/SOM numbers.

#### Key Players

For the top 5-10 companies in the market:

| Company | Est. Market Share | Positioning | Notable |
|---------|------------------|-------------|---------|
| Company A | X% | Description | Recent news |
| Company B | X% | Description | Recent news |

Include funding, revenue, or headcount data where publicly available.

#### Trends

**Current trends** (happening now):
- Trend 1: Description and evidence
- Trend 2: Description and evidence

**Emerging trends** (early signals):
- Trend 1: Description and evidence
- Trend 2: Description and evidence

**Technology shifts:**
- What new technologies are affecting this market
- How buyer behavior is changing

#### Opportunities

- **Underserved segments**: Customer groups or use cases not well served by current players
- **Timing advantages**: Market shifts creating windows of opportunity
- **White space**: Product or positioning gaps in the market
- **Geographic expansion**: Regions where the market is less mature

#### Risks

- **Regulatory risks**: Current or pending regulation that could affect the market
- **Competitive risks**: Consolidation, well-funded new entrants, platform risk
- **Market risks**: Demand shifts, economic sensitivity, cyclicality
- **Technology risks**: Disruption potential, obsolescence of current approaches

---

## Tips

- **Focus on recent data** -- prioritize sources from the last 2 years. Market data older than 3 years is often unreliable for sizing and forecasts.
- **Cross-reference market size estimates** -- different analysts often disagree by 2-5x on market size. Note the range rather than picking one number.
- **Distinguish TAM from SAM from SOM** -- a common mistake is using TAM as if it's the real opportunity. Help the user understand which number matters for their business.
- **Source quality matters** -- analyst reports (Gartner, IDC, Forrester) and government data are more reliable than blog posts and press releases. Note your sources.
- **Be honest about confidence levels** -- if data is sparse or conflicting, say so. "The market size is estimated at $X-Y billion" is better than false precision.

---

## Related Skills

- **competitive-intelligence**: For detailed competitor analysis (company-level deep dives)
- **exa-company-research**: For raw Exa web search on specific companies
- **exa-research-papers**: For academic and technical research papers
- **content-strategy**: For content marketing strategy informed by market research
