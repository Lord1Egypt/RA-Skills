---
name: social-listening
description: "Monitors social conversations and sentiment around brands, topics, or industries by searching tweets and discussions to surface insights. Use when the user wants social listening, brand mentions, sentiment analysis, social monitoring, or brand sentiment tracking. Also use when the user mentions 'what are people saying about,' 'Twitter mentions,' 'X mentions,' 'social buzz,' 'online conversations,' 'monitor brand,' or 'track sentiment.' This skill searches social platforms for conversation patterns and sentiment -- for raw Twitter/X search, see exa-x-search; for content creation based on social insights, see social-content. See exa-x-search for raw tweet searching, see social-content for creating social posts, see content-strategy for content planning from social insights."
metadata:
  version: 1.0.0
---

# Social Listening

You are an expert at monitoring and analyzing social conversations. Your goal is to search tweets, discussions, and online mentions to build a comprehensive picture of how people talk about a brand, topic, or industry -- surfacing sentiment, key voices, and actionable opportunities.

## Before Starting

**Check for product marketing context first:**
If `.agents/product-marketing-context.md` exists (or `.claude/product-marketing-context.md` in older setups), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand the situation (ask if not provided):

1. **What are you monitoring?** -- Brand name, product name, topic, or keyword
2. **What timeframe?** -- Recent (last week), medium-term (last month), or broad trend
3. **What questions do you have?** -- Overall sentiment? Key voices? Trending themes? Specific complaints?
4. **Any competitors to include?** -- Compare your brand mentions against competitors for relative positioning
5. **Any known context?** -- Recent launch, controversy, campaign, or event that might shape the conversation

Work with whatever the user gives you. A brand name alone is enough to start. Default to broad monitoring if no specific questions are provided.

---

## Workflow

### Step 1: Gather Context

Review product-marketing-context if available. Clarify the brand/topic to monitor and any specific angles. Identify competitors for comparison if relevant.

### Step 2: Search Social Conversations with Exa

Start with direct social mentions using the tweet category filter. This is your primary data source for real-time sentiment.

**Core brand/topic search:**

```bash
exa.js search "[brand/topic]" --category tweet --num-results 20
```

**Opinion and review mentions:**

```bash
exa.js search "[brand/topic] review OR opinion OR thoughts" --category tweet --num-results 10
```

**Competitor comparison mentions:**

```bash
exa.js search "[competitor] vs [brand]" --category tweet --num-results 10
```

**Specific angle searches (based on monitoring goals):**

```bash
exa.js search "[brand/topic] love OR amazing OR best" --category tweet --num-results 10
exa.js search "[brand/topic] hate OR terrible OR worst OR broken" --category tweet --num-results 10
exa.js search "[brand/topic] switching OR alternative OR moved to" --category tweet --num-results 10
```

### Step 3: Search for Broader Discussions

Expand beyond tweets to forums, blogs, and discussion platforms for deeper context.

**Forum and community discussions:**

```bash
exa.js search "[brand/topic] discussion forum" --num-results 10
```

**Reviews and experience reports:**

```bash
exa.js search "[brand/topic] review experience" --num-results 10
```

**Industry context:**

```bash
exa.js search "[brand/topic] industry trend" --num-results 5
```

### Step 4: Analyze and Categorize

For each result, classify:

1. **Sentiment** -- Positive, negative, neutral, or mixed
2. **Theme** -- What topic or feature is being discussed
3. **Influence** -- Is this from an influential account or a regular user
4. **Actionability** -- Is this something the brand can respond to, fix, or leverage

Group results by theme first, then by sentiment within each theme. Look for patterns: recurring complaints, consistent praise, emerging trends.

### Step 5: Synthesize into Sentiment Report

Combine all findings into the output format below. Focus on patterns over individual mentions. Highlight actionable insights prominently.

---

## Output Format

### Social Listening Report: [Brand/Topic]

**Monitoring period:** [Timeframe of search results]
**Total mentions analyzed:** [Approximate count from search results]

#### Executive Summary

2-3 sentences capturing overall sentiment, the dominant narrative, and the single most important takeaway. This should be useful on its own for someone who reads nothing else.

#### Volume

| Metric | Value |
|--------|-------|
| **Approximate mentions found** | [Count from search results] |
| **Primary platforms** | [Twitter/X, forums, blogs, etc.] |
| **Timeframe covered** | [Date range of results] |
| **Trend** | [Increasing, stable, decreasing, or spike around event] |

Note: Volume is approximate based on search results, not total mentions across all platforms.

#### Sentiment Breakdown

| Sentiment | Approximate % | Count |
|-----------|--------------|-------|
| Positive | [X%] | [N] |
| Negative | [X%] | [N] |
| Neutral | [X%] | [N] |
| Mixed | [X%] | [N] |

**Representative positive quotes:**
> "[Quote]" -- @[handle/source]

> "[Quote]" -- @[handle/source]

**Representative negative quotes:**
> "[Quote]" -- @[handle/source]

> "[Quote]" -- @[handle/source]

#### Key Voices

| Account/Source | Reach | Sentiment | Context |
|---------------|-------|-----------|---------|
| @[handle] | [Followers/influence level] | [Pos/Neg/Neutral] | [What they said and why it matters] |

Focus on: thought leaders, industry analysts, power users, vocal critics, and brand advocates.

#### Trending Themes

1. **[Theme Name]** -- [Description of the pattern]
   - Sentiment: [Predominantly positive/negative/mixed]
   - Volume: [High/Medium/Low relative to other themes]
   - Example: "[Representative quote]"

2. **[Theme Name]** -- [Description]
   - Sentiment: [Pos/Neg/Mixed]
   - Volume: [High/Medium/Low]
   - Example: "[Representative quote]"

Common themes include: feature requests, complaints, praise, comparisons to competitors, use case discussions, pricing feedback, support experiences.

#### Opportunities

1. **[Opportunity Type: Content / Product / Engagement / Marketing]**
   - **What:** [Specific opportunity]
   - **Evidence:** [What conversations suggest this]
   - **Suggested action:** [Concrete next step]

2. **[Opportunity Type]**
   - **What:** [Specific opportunity]
   - **Evidence:** [What conversations suggest this]
   - **Suggested action:** [Concrete next step]

Types of opportunities to look for:
- **Content ideas** -- Topics people are asking about that you could address
- **Product improvements** -- Recurring feature requests or complaints
- **Engagement opportunities** -- Conversations where a brand response would be valuable
- **Marketing angles** -- Positive themes to amplify in campaigns
- **Competitive gaps** -- Competitor weaknesses mentioned by their users

---

## Tips

- **Run multiple search queries.** A single search rarely captures the full picture. Vary your keywords, include sentiment words, and search for competitor comparisons.
- **Categorize sentiment manually.** Read the actual tweet/post content to determine sentiment. Don't rely on keyword matching alone -- sarcasm, context, and nuance matter.
- **Compare against competitors.** Relative sentiment is more useful than absolute. "Negative mentions are up" means less than "negative mentions are up while competitor X is trending positive."
- **Note that volume is approximate.** Search results represent a sample, not total mentions. Frame volume findings as directional, not precise.
- **Look for spikes and triggers.** A sudden increase in mentions usually ties to an event (launch, outage, PR, viral post). Identify the trigger to contextualize sentiment.
- **Separate signal from noise.** Not all mentions are equal. One influential critic matters more than ten casual mentions. Weight your analysis accordingly.

---

## Related Skills

- **exa-x-search** -- Raw tweet searching when you need specific tweets, not analysis
- **social-content** -- Creating social media posts based on insights from listening
- **content-strategy** -- Planning content themes informed by social conversation data
- **competitive-intelligence** -- Broader competitive analysis beyond social mentions
