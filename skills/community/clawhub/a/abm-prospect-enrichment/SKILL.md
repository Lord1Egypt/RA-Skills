---
name: prospect-enrichment
description: "Enriches prospect and company profiles by scraping their website and searching for additional context to build comprehensive profiles. Use when the user wants to enrich a prospect, analyze a prospect site, do site enrichment, learn about a company, build a company profile, do prospect research, find out what a company does, or do a company deep dive. Also use when the user mentions 'enrich prospect,' 'company profile,' 'prospect research,' 'company deep dive,' or 'what does this company do.' This skill combines site scraping with web search for comprehensive prospect profiles -- for raw site scraping, see firecrawl-cli; for raw company search, see exa-company-research; for lead list building, see exa-lead-generation. See cold-email for using enriched profiles in outreach, see competitive-intelligence for competitor-focused research."
metadata:
  version: 1.0.0
---

# Prospect Enrichment

You are an expert at building comprehensive prospect profiles. Your goal is to scrape a prospect's website for primary data, then search for supplementary context to create an enriched profile that gives sales and marketing teams everything they need to engage effectively.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand the situation (ask if not provided):

1. **Which company?** -- Company name and website URL
2. **What do you want to learn?** -- Specific areas of interest (tech stack, funding, team, pain points), or use defaults to cover all areas
3. **Why are you researching them?** -- Outreach, partnership, competitive analysis, deal prep
4. **What do you already know?** -- Any existing context about this prospect to avoid redundant research

Work with whatever the user gives you. A company name and URL is enough to start. If they only have a name, search for the URL first.

---

## Workflow

### Step 1: Gather Context

Review product-marketing-context if available. Ask the user for the company name and URL if not provided. Clarify research goals or default to a full enrichment profile.

### Step 2: Scrape Prospect Site with Firecrawl

Start with the prospect's own website. This is your primary data source -- what the company says about itself.

**Scrape the homepage:**

```bash
node tools/clis/firecrawl.js scrape [prospect-url]
```

**Scrape key pages for deeper context:**

```bash
node tools/clis/firecrawl.js scrape [prospect-url]/about
node tools/clis/firecrawl.js scrape [prospect-url]/pricing
node tools/clis/firecrawl.js scrape [prospect-url]/team
```

Try alternate paths if the above return 404:
- `/about-us`, `/about/team`, `/leadership`, `/our-team`
- `/plans`, `/pricing-plans`
- `/careers`, `/jobs` (useful for inferring growth and priorities)
- `/customers`, `/case-studies` (useful for understanding their market)

**Optionally discover page structure:**

```bash
node tools/clis/firecrawl.js map [prospect-url]
```

Use the sitemap to identify pages worth scraping that you might have missed (blog, integrations, docs, changelog).

**What to extract from site scraping:**
- Company description and positioning
- Product/service overview
- Pricing tiers and model
- Team members and leadership
- Customer logos and case studies
- Technology indicators (job postings, integrations page)
- Company size signals (office locations, team page)

### Step 3: Search for Company Context with Exa

After scraping the site, search for external context that the company doesn't publish on their own site.

**Funding and financial context:**

```bash
node tools/clis/exa.js search "[company name] funding" --num-results 5
```

**Recent news and developments:**

```bash
node tools/clis/exa.js search "[company name] news 2025 2026" --num-results 5
```

**Technology stack and infrastructure:**

```bash
node tools/clis/exa.js search "[company name] technology stack" --num-results 5
```

**Reviews and reputation:**

```bash
node tools/clis/exa.js search "[company name] reviews" --num-results 5
```

**Optional targeted searches based on research goals:**

```bash
node tools/clis/exa.js search "[company name] hiring engineering" --num-results 5
node tools/clis/exa.js search "[company name] partnerships integrations" --num-results 5
node tools/clis/exa.js search "[company name] CEO interview" --num-results 5
```

### Step 4: Synthesize Enriched Prospect Profile

Combine data from site scraping (primary) and web search (supplementary) into the output format below. Clearly distinguish between confirmed facts (from the company's own site) and inferred information (from external sources).

---

## Output Format

### Enriched Prospect Profile: [Company Name]

#### Company Overview

| Field | Value |
|-------|-------|
| **Company Name** | [Full legal/brand name] |
| **Website** | [URL] |
| **One-Line Description** | [What they do in one sentence] |
| **Founded** | [Year, if available] |
| **Headquarters** | [City, State/Country] |
| **Employee Count** | [Estimate with source: site, LinkedIn, news] |
| **Industry** | [Primary industry/vertical] |

#### What They Do

2-3 paragraph summary of the company's product/service, target market, and positioning. Based primarily on their own site content.

#### Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | [Inferred from site, job postings, or search] |
| **Backend** | [Inferred from job postings, integrations, or search] |
| **Infrastructure** | [Cloud provider, CDN, etc.] |
| **Key Integrations** | [From integrations page or search] |

Note what is confirmed (from their site/job postings) vs inferred (from external sources).

#### Team

| Person | Role | Notable |
|--------|------|---------|
| [Name] | [Title] | [Background, previous companies, relevant experience] |

Include: CEO/Founder, CTO, VP Sales/Marketing, and other key leadership. Note team size if available.

#### Funding

| Round | Date | Amount | Investors |
|-------|------|--------|-----------|
| [Series X] | [Date] | [Amount] | [Lead investor, others] |

Total raised: [Amount]
Last valuation: [If available, note if confirmed or estimated]

#### Pain Points

Based on the company's positioning, reviews, job postings, and content themes, these are likely pain points:

1. **[Pain Point]** -- [Evidence: where this was inferred from]
2. **[Pain Point]** -- [Evidence]
3. **[Pain Point]** -- [Evidence]

Mark each as **Confirmed** (from reviews, direct statements) or **Inferred** (from positioning, hiring patterns, content themes).

#### Research Confidence

| Section | Confidence | Source |
|---------|-----------|--------|
| Company Overview | High/Medium/Low | [Primary source] |
| Tech Stack | High/Medium/Low | [Primary source] |
| Team | High/Medium/Low | [Primary source] |
| Funding | High/Medium/Low | [Primary source] |
| Pain Points | High/Medium/Low | [Primary source] |

---

## Tips

- **One prospect at a time.** This workflow is designed for deep single-company research. For batch prospecting, see exa-lead-generation.
- **Scrape first, search second.** The company's own site is the most reliable source. Use external search to fill gaps and add context the company doesn't publish.
- **Mark confirmed vs inferred.** Sales teams need to know what's verified and what's a hypothesis. Always note your confidence level.
- **Check the careers page.** Job postings reveal tech stack, growth priorities, team gaps, and organizational challenges better than almost any other source.
- **Look at the pricing page carefully.** Pricing model and tiers reveal target market, average deal size, and competitive positioning.
- **Don't over-scrape.** 4-6 key pages plus targeted Exa searches is usually enough. Diminishing returns set in quickly.

---

## Related Skills

- **cold-email** -- Use enriched profiles to write personalized outreach
- **exa-company-research** -- Raw company search when you don't need full enrichment
- **exa-lead-generation** -- Build lead lists across multiple companies
- **firecrawl-cli** -- Raw site scraping commands and options
- **competitive-intelligence** -- Multi-competitor broad analysis (vs single-prospect deep dive)
