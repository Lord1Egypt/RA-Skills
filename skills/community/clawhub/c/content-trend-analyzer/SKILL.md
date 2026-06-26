---
name: content-trend-analyzer
description: Cross-platform content trend analysis and outline generation tool. Platforms covered include but are not limited to: Google Trends, Reddit, YouTube, Medium, Substack, Twitter/X, Zhihu, Weibo, Douyin, Bilibili, Baidu Index, WeChat Official Accounts, GitHub Trending, Product Hunt.
---

# Content Trend Analyzer

Multi-platform content trend aggregation and analysis, producing data-driven article outlines and content strategies. Triggers when users need: content trend analysis, topic heat tracking, trending topic discovery, user intent analysis, content gap mining, competitive content research, SEO keyword trends, data-driven article outline generation, content strategy formulation.

## Trigger Keywords

Trend analysis, content trends, trending topics, trend analysis, content gap, topic analysis, topic selection, content strategy, outline generation, content outline.

## Workflow

1. **Requirement Understanding** → Determine the analysis domain, target platforms, and time range
2. **Data Collection** → Perform layered search by platform, aggregate trend signals
3. **Intent Analysis** → Identify user pain points, interest shifts, and information gaps
4. **Gap Mining** → Compare existing content coverage to discover untapped opportunities
5. **Outline Generation** → Output structured article outlines + topic scores

## Step 1: Requirement Understanding

Confirm with the user (if not explicitly provided):

- **Domain/Industry**: Technology, Finance, Health, Education, etc.
- **Target Audience**: B2B/B2C, technical level, region
- **Target Platforms**: Platforms where content will be published (affects style and depth)
- **Time Range**: Real-time trending / Last 7 days / Last 30 days / Quarterly
- **Analysis Depth**: Quick scan / Standard report / Competitive benchmarking

## Step 2: Data Collection

Collect data in layers by priority, using the corresponding tool for each layer:

### Layer 1: Trend Baseline (Mandatory)

| Platform | Tool | Content Collected |
|----------|------|-------------------|
| Google Trends | `web_fetch` trends.google.com | Search heat trends, related queries, geographic distribution |
| Reddit | `web_search` site:reddit.com | Popular discussions, highly upvoted answers, community pain points |
| YouTube | `web_search` site:youtube.com | Video popularity, comment sentiment, title keywords |

### Layer 2: In-Depth Content (On Demand)

| Platform | Tool | Content Collected |
|----------|------|-------------------|
| Medium/Substack | `web_search` site:medium.com OR site:substack.com | Long-form topic selection, subscriber interaction, writing styles |
| Twitter/X | `web_search` site:x.com | Real-time discussions, hashtags, KOL perspectives |
| Zhihu/Weibo | `web_search` site:zhihu.com OR site:weibo.com | Chinese community Q&A, trending topics |
| Baidu Index | `web_fetch` index.baidu.com | Chinese search trends, audience profiles |
| Product Hunt | `web_search` site:producthunt.com | New product trends, technology directions |

### Layer 3: Competitive Benchmarking (For In-Depth Reports)

| Platform | Tool | Content Collected |
|----------|------|-------------------|
| Competitor Blogs/Official Accounts | `web_fetch` + `web_search` | Existing content coverage, publishing frequency, engagement data |
| GitHub Trending | `web_search` site:github.com/trending | Developer technology trends |

**Collection Strategy:**
- Execute 2-3 targeted searches per platform (from different angles)
- Search query combinations: `"{domain} + {time-related term}"`, `"{domain} + pain point term"`, `"{domain} + how/why/what"`
- Record for each finding: source, popularity metric, core topic, user sentiment

## Step 3: Intent Analysis

Perform the following analysis on the collected data:

1. **Topic Clustering**: Group similar topics; identify 3-5 core themes
2. **Intent Classification**:
   - 🎯 Learning (how-to, tutorials, guides)
   - 🤔 Exploratory (comparisons, reviews, analysis)
   - 😤 Pain Points (errors, problems, complaints)
   - 🚀 Forward-Looking (trend forecasts, new tools, best practices)
3. **Sentiment Tendency**: Positive/Negative/Neutral; identify controversial topics
4. **User Personas**: Infer technical level and role identity from discussion language

## Step 4: Gap Mining

Compare existing content with user needs:

```
Existing Content Coverage Matrix:
  Topic A: ████░░░░ 50% (Lacks advanced content)
  Topic B: ██░░░░░░ 25% (Significant gaps)
  Topic C: ████████ 90% (Saturated; difficult to differentiate)
  Topic D: ░░░░░░░░  0% (Blue ocean opportunity)
```

Scoring Dimensions:
- **Demand Intensity** (search volume + discussion heat) → Scale of 1-5
- **Content Gap** (insufficient existing coverage) → Scale of 1-5
- **Differentiation Potential** (likelihood of a unique angle) → Scale of 1-5
- **Timeliness** (current heat window) → Scale of 1-5
- **Composite Recommendation Score** = Weighted average

## Step 5: Outline Generation

See [references/outline-templates.md](references/outline-templates.md) for output format.

Generate for each high-scoring topic:

### Article Outline Structure

```
## [Topic Title]
- Recommendation Score: X.X/5.0
- Target Platform: [Platform]
- Estimated Word Count: [Word Count]
- Difficulty: [Beginner/Intermediate/Expert]

### Core Value Proposition
[One sentence explaining what the reader will gain]

### Outline
1. [Introduction hook - based on real user pain points]
   - Data Support: [Cite trend data]
2. [Core Argument 1]
   - Sub-points + Examples/Data
3. [Core Argument 2]
   - Sub-points + Examples/Data
4. [Core Argument 3]
   - Sub-points + Examples/Data
5. [Conclusion + Call to Action]

### SEO Recommendations
- Primary Keyword: [Keyword]
- Long-Tail Keywords: [KW1], [KW2], [KW3]
- Title Alternatives: [Alt Title 1], [Alt Title 2]
```

### Topic Ranking Report

Generate a comparison table of all candidate topics:

```
| Rank | Topic | Rec. Score | Demand Intensity | Content Gap | Differentiation | Timeliness |
|------|-------|-----------|-----------------|-------------|----------------|------------|
| 1    | ...   | 4.5       | 5               | 4           | 4              | 5          |
```

## Output Format Selection

- **Quick Scan**: Concise table + Top 3 outlines
- **Standard Report**: Full analysis + Top 5 outlines + Gap matrix
- **In-Depth Report**: Full dataset + Competitive benchmarking + Top 10 outlines + Monthly recommendations

## Notes

- Annotate all data points with source URLs to ensure traceability
- Distinguish between "noise topics" (short-term hype) and "trend topics" (sustained growth)
- For Chinese content, prioritize data from Zhihu, Weibo, and Baidu Index
- For English content, prioritize Google Trends, Reddit, and Hacker News
- For tech topics, additionally check GitHub Trending and Stack Overflow