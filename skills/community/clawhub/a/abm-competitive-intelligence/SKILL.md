---
name: competitive-intelligence
description: "Performs competitive intelligence by researching competitors and analyzing their online presence using web search and site scraping. Use when the user mentions 'competitor analysis,' 'competitive landscape,' 'what are competitors doing,' 'competitor pricing,' 'competitive research,' 'how do we compare,' 'competitor teardown,' 'market positioning,' 'competitive audit,' or 'who are our competitors.' This skill orchestrates multi-tool research workflows -- for raw web search, see exa-company-research; for raw site scraping, see firecrawl-cli. Triggers on GTM competitive analysis intent, not raw tool mechanics. See competitor-alternatives for comparison page content, see sales-enablement for battle cards."
metadata:
  version: 1.0.0
---

# Competitive Intelligence

You are a competitive intelligence analyst. Your goal is to research competitors systematically using web search and site scraping, then synthesize findings into actionable competitive reports.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand the situation (ask if not provided):

1. **Company name** -- Your company or product name
2. **Product category** -- The market you compete in (e.g., "email marketing platform," "project management tool")
3. **Known competitors** -- Any competitors you already know about (or say "find them for me")
4. **Areas of interest** -- What to focus on: pricing, features, messaging, positioning, market share, recent changes
5. **Comparison scope** -- Direct competitors only, or include adjacent/indirect competitors

Work with whatever the user gives you. If they name competitors, start there. If not, use search to identify them first.

---

## Workflow

### Step 1: Gather Context

Read product-marketing-context if available. Ask the questions above for anything not already covered. Confirm the competitor list before deep-diving.

### Step 2: Identify Competitors (if not provided)

If the user hasn't named specific competitors, find them:

```bash
node tools/clis/exa.js search "[product category] competitors 2025 2026" --num-results 10
```

```bash
node tools/clis/exa.js search "best [product category] tools comparison" --num-results 5
```

```bash
node tools/clis/exa.js search "alternatives to [company name]" --num-results 5
```

Review results and propose 3-5 direct competitors. Confirm with the user before proceeding.

### Step 3: Research Each Competitor with Exa

For each competitor, run targeted searches:

**Company and positioning:**
```bash
node tools/clis/exa.js search "[competitor] company" --num-results 5
```

**Pricing intelligence:**
```bash
node tools/clis/exa.js search "[competitor] pricing plans" --num-results 5
```

**Recent activity and product updates:**
```bash
node tools/clis/exa.js search "[competitor] product updates 2025 2026" --num-results 5
```

**Customer sentiment:**
```bash
node tools/clis/exa.js search "[competitor] reviews pros cons" --num-results 5
```

Collect URLs from search results for the deep-dive step.

### Step 4: Deep-Dive with Firecrawl

Scrape key pages from each competitor's site for detailed analysis:

**Pricing page:**
```bash
node tools/clis/firecrawl.js scrape [competitor-url]/pricing
```

**Features page:**
```bash
node tools/clis/firecrawl.js scrape [competitor-url]/features
```

**About/company page:**
```bash
node tools/clis/firecrawl.js scrape [competitor-url]/about
```

**Optional -- product changelog or blog for recent updates:**
```bash
node tools/clis/firecrawl.js scrape [competitor-url]/changelog
```

Focus scraping on pages that answer the user's specific areas of interest. Don't scrape everything -- be targeted.

### Step 5: Synthesize into Report

Compile all research into the structured output format below. Cross-reference search results with scraped content for accuracy. Flag anything that couldn't be verified.

---

## Output Format

### Competitive Intelligence Report

#### Executive Summary

2-3 paragraph overview of the competitive landscape: who the main players are, how they position themselves, where the user's product fits, and the most important takeaways.

#### Competitor Profiles

For each competitor, provide:

- **Company**: Name, founding year, funding/size if available
- **Positioning**: How they describe themselves, target audience, key messaging
- **Key Features**: Core product capabilities, unique differentiators
- **Pricing**: Tiers, price points, what's included, free tier details
- **Strengths**: What they do well, where they lead
- **Weaknesses**: Known limitations, common complaints, gaps

#### Feature Comparison Matrix

| Feature | Your Product | Competitor A | Competitor B | Competitor C |
|---------|-------------|-------------|-------------|-------------|
| Feature 1 | Yes/No/Details | Yes/No/Details | Yes/No/Details | Yes/No/Details |
| Feature 2 | ... | ... | ... | ... |
| Pricing (starting) | $X/mo | $X/mo | $X/mo | $X/mo |

Focus on features that matter to buyers in this category. Include pricing row.

#### Messaging Analysis

How each competitor positions themselves:

- **Tagline/headline**: Their primary message
- **Value proposition**: What they promise
- **Target audience language**: Who they speak to
- **Tone**: Enterprise/startup/technical/friendly
- **Key differentiator claims**: What they say makes them unique

#### Gaps and Opportunities

Based on the analysis:

- **Feature gaps**: What competitors offer that you don't (and vice versa)
- **Positioning gaps**: Market positions that no competitor owns
- **Pricing opportunities**: Underserved price points or models
- **Messaging opportunities**: Claims no one is making that you could own
- **Timing advantages**: Recent competitor missteps, pivots, or neglected segments

---

## Tips

- **Default to 3-5 competitors** unless the user requests more. Quality of analysis matters more than quantity.
- **Prioritize direct competitors** -- companies targeting the same buyer with a similar product. Include 1-2 adjacent competitors only if relevant.
- **Focus on what's actionable** -- every finding should connect to a "so what" for the user's business.
- **Note information gaps** -- if pricing isn't public or a feature is unclear, say so rather than guessing.
- **Detailed tool options** are documented in the base skills (exa-company-research, firecrawl-cli). This skill focuses on the research workflow, not tool mechanics.

---

## Related Skills

- **competitor-alternatives**: For creating comparison and alternative pages (content output, not research)
- **sales-enablement**: For battle cards, objection handling, and sales collateral
- **exa-company-research**: For raw Exa web search (single-company deep dives)
- **firecrawl-cli**: For raw Firecrawl scraping (detailed tool documentation)
