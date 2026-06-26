# SKILL.md - Research Assistant

## Description
Your personal research department. Multi-source synthesis that turns scattered information into actionable intelligence â not just summaries, but insights you can act on.

## Price
**Free** â or **$5** to support development.

## Prerequisites
- DuckDuckGo Search (built-in, no key needed)
- YouTube Content tool (built-in, no key needed)  
- arXiv skill (built-in, no key needed)
- Reddit Readonly skill (built-in, no key needed)
- Browser tool (built-in, for paywall bypass)
- Optional: NewsAPI key (free tier: 100 requests/day) â current events
- Optional: OpenWeather API key (free tier: 1,000 calls/day) â location context
- Optional: ExchangeRate-API key (free tier: 1,500 requests/month) â finance data
- Optional: REST Countries API (no key needed) â demographics

## Quick Start
1. **Configure optional APIs:** "Set up my research assistant with NewsAPI"
2. **Research:** "Research [topic]" or "Deep dive into [question]"

## Commands
- "Research [topic]" â Quick synthesis from multiple sources
- "Deep dive into [question]" â Comprehensive analysis
- "Compare [A] vs [B]" â Competitive/feature analysis
- "What's new in [field] this month?" â Temporal research
- "Research for [format]: [topic]" â Brief, thread, blog, or decision matrix
- "Show my research history" â Previous queries and findings

---

## Tool Selection Matrix

| Source Type | Tool to Use | Fallback |
|-------------|-------------|----------|
| Web search | `duckduckgo_search` | None needed |
| YouTube transcripts | `youtube-content` skill | Browser tool |
| Academic papers | `arxiv` skill | `duckduckgo_search` with site:arxiv.org |
| Forums/Reddit | `reddit-readonly` skill | None needed |
| Paywalled articles | `browser_navigate` + archive.org | 12ft.io, textise dot iitty |
| Current events | NewsAPI (if configured) | `duckduckgo_search` news filter |
| Weather data | OpenWeather API | `duckduckgo_search` |
| Financial data | ExchangeRate-API | `duckduckgo_search` |

### Paywall Bypass Strategy
When you hit a paywall:
1. **Try archive.org:** `https://webcache.googleusercontent.com/search?q=URL` or `https://archive.org/web/*/URL`
2. **Try 12ft.io:** `https://12ft.io/URL` (works for Medium, Substack, etc.)
3. **Try textise dot iitty:** `https://r.jina.ai/http://URL` (extracts article text)
4. **Use browser tool:** Navigate and extract text directly
5. **Skip only if all fail** â mark as "paywalled, unverified"

---

## Core Workflows

### 1. Quick Research (2-3 minutes)

**Input:** Any question or topic

**Process:**
1. Parallel search across sources using tool matrix above
2. Fetch top 3-5 results per source
3. Bypass paywalls using strategy above
4. Extract key points from each
5. Synthesize into structured brief
6. Cite all sources with links

**Output:**
```markdown
## Research Brief: [Topic]

### Executive Summary
[3-5 sentences covering the landscape]

### Key Findings
1. **[Finding]** â [Source type: web/video/paper/forum]
2. **[Finding]** â [Source type]
3. **[Finding]** â [Source type]

### Sources
- [Title](URL) â Web article, [Date]
- [Title](URL) â YouTube video, [Channel]
- [Title](URL) â arXiv paper, [Authors]
- [Title](URL) â Reddit discussion, [Subreddit]

### Confidence Score: [High/Medium/Low]
**Why:** [Source quality, recency, consensus level]

### Suggested Next Steps
- [Specific follow-up question]
- [Related topic to explore]
- [Deeper source to check]
```

### 2. Deep Dive Research (5-10 minutes)

**Input:** Complex question requiring comprehensive analysis

**Process:**
1. Multi-query expansion (break topic into sub-questions)
2. 10-15 sources across all channels
3. Apply paywall bypass as needed
4. Temporal analysis (what's new vs. established)
5. Credibility scoring per source
6. Bias detection and flagging
7. Synthesis with uncertainty levels

**Stopping Conditions â When to End:**
- **Saturation:** New sources repeat what you already found
- **Diminishing returns:** 10+ sources but confidence still Low
- **Contradiction ceiling:** >50% of sources disagree
- **Time limit:** 15 minutes max for Deep Dive
- **Confidence achieved:** High confidence with 3+ Tier 1 sources

**Output:**
```markdown
## Deep Dive: [Topic]

### One-Paragraph Summary
[The TL;DR for busy decision-makers]

### Current State (What's Happening Now)
[Recent developments, 0-6 months]

### Established Knowledge (What We Know)
[Consensus views, foundational concepts]

### Points of Contention
- **[Claim A]** â [Evidence for] vs [Evidence against]
- **[Claim B]** â [Evidence for] vs [Evidence against]

### Source Quality Breakdown
| Source | Type | Credibility | Recency | Bias |
|--------|------|-------------|---------|------|
| [Name] | Academic | High | 2024 | Neutral |
| [Name] | News | Medium | 2025 | Center-left |
| [Name] | Forum | Low | 2025 | N/A |

### Confidence Calibration
**Level:** [High/Medium/Low]
**Reasoning:** [Why this level based on criteria below]

### Actionable Insights
1. **[Insight]** â [Specific action to take]
2. **[Insight]** â [Specific action to take]

### Knowledge Gaps
[What we still don't know]

### Recommended Follow-Up
- [Specific research question]
- [Expert to consult]
- [Primary source to find]
```

### 3. Comparative Analysis

**Input:** "Compare X vs Y" or "Feature gap analysis"

**Process:**
1. Research both subjects independently using tool matrix
2. Extract features/capabilities/attributes
3. Build comparison matrix
4. Identify gaps and differentiators
5. Score on key dimensions

**Structured Data Extraction:**
```
Pricing extraction pattern:
- Search: "[Product] pricing cost $"
- Look for: $XXX/month, $XXX/year, free tier limits
- Source: Official pricing page (bypass paywall if needed)

Feature extraction pattern:
- Search: "[Product] features vs [Competitor]"
- Look for: Feature lists, comparison tables
- Use: Browser tool to extract structured data

Sentiment extraction pattern:
- Reddit: Search r/[topic] for "[Product] review"
- Look for: Specific pros/cons with reasoning
- Score: Count positive vs negative mentions
```

**Output:**
```markdown
## Comparison: [A] vs [B]

### At a Glance
| Dimension | [A] | [B] | Winner |
|-----------|-----|-----|--------|
| Price | $X | $Y | [A/B/Tie] |
| Key Feature | [Desc] | [Desc] | [A/B/Tie] |
| User Sentiment | [Score] | [Score] | [A/B/Tie] |

### Detailed Breakdown

**[A] Strengths:**
- [Point with source]
- [Point with source]

**[B] Strengths:**
- [Point with source]
- [Point with source]

**[A] Weaknesses:**
- [Point with source]

**[B] Weaknesses:**
- [Point with source]

### Feature Gap Analysis
- [Feature A]: [A] has it, [B] doesn't
- [Feature B]: Both have it, [A] does it better
- [Feature C]: Neither has it (opportunity)

### Verdict
[Recommendation with reasoning]

### Sources
[All citations]
```

### 4. Temporal Research (What's New)

**Input:** "What's new in [field] this [timeframe]?"

**Process:**
1. Filter sources by date using search filters
2. Compare to baseline (previous period)
3. Identify new developments, trends, shifts
4. Flag emerging vs. fading topics

**Output:**
```markdown
## [Field] Update: [Timeframe]

### New Developments
1. **[Development]** â [Impact level] â [Source]
2. **[Development]** â [Impact level] â [Source]

### Trends to Watch
- [Trend]: [Evidence] â [Trajectory: rising/stable/falling]
- [Trend]: [Evidence] â [Trajectory]

### What's Fading
- [Topic]: [Why it's declining]

### Predictions (Speculative)
- [Prediction] â [Based on]

### Sources from This Period
[All recent citations]
```

### 5. Format-Specific Output

**Brief Mode:** Executive summary only (2-3 paragraphs)

**Thread Mode:** Twitter/X thread format
```
ð§µ [Topic]: [Hook]

1/ [Point]
2/ [Point]
3/ [Point]

[Sources]
```

**Blog Mode:** H2 outline with key points
```
## [Title]

### Introduction
[Hook]

### [Section 1]
[Key points]

### [Section 2]
[Key points]

### Conclusion
[Takeaway]

### Sources
[Citations]
```

**Decision Matrix Mode:** Pros/cons table with scoring
```
| Option | Pros | Cons | Score |
|--------|------|------|-------|
| [A] | [List] | [List] | X/10 |
| [B] | [List] | [List] | X/10 |
```

---

## Confidence Calibration System

Don't guess â use these criteria:

### High Confidence
- **Sources:** 3+ Tier 1 (academic, official, expert) OR 5+ Tier 2
- **Recency:** All sources <6 months old OR established consensus
- **Contradictions:** Zero major contradictions
- **Corroboration:** Findings confirmed by independent sources

### Medium Confidence
- **Sources:** 2+ Tier 2 (industry pubs, established blogs)
- **Recency:** Mix of recent and established
- **Contradictions:** Minor contradictions resolved
- **Gaps:** Some uncertainty acknowledged

### Low Confidence
- **Sources:** Single source OR mostly Tier 4-5
- **Recency:** Old data (>1 year) OR no date
- **Contradictions:** Major contradictions unresolved
- **Gaps:** Significant unknowns

**Flag language:**
- High: "Research shows...", "Evidence confirms..."
- Medium: "Sources suggest...", "It appears that..."
- Low: "One source claims...", "Limited research indicates..."

---

## Source Quality Scoring

### Tier 1: Highest Credibility (Weight: 3x)
- Peer-reviewed journals (Nature, Science, etc.)
- Official documentation (gov, corporate)
- SEC filings, regulatory documents
- Direct primary sources

### Tier 2: High Credibility (Weight: 2x)
- Established news (Reuters, AP, BBC)
- Expert blogs with track record
- Industry analysts (Gartner, McKinsey)
- Technical publications (IEEE, ACM)

### Tier 3: Medium Credibility (Weight: 1x)
- Industry publications
- Established YouTube channels
- Well-moderated forums
- Think tank reports

### Tier 4: Low Credibility (Weight: 0.5x)
- General news coverage
- Encyclopedia entries (Wikipedia â follow citations)
- Content aggregators

### Tier 5: Use Cautiously (Weight: 0.25x)
- Anonymous forums
- Unverified social posts
- Personal blogs without track record

### Auto-Skip
- Known misinformation sources
- Circular references (A cites B cites A)
- Paywalled AND can't bypass

---

## Bias Detection

### Political Spectrum
- Left / Center-left / Center / Center-right / Right
- Flagged when source consistently leans one direction

### Commercial Bias
- **None:** No financial stake in topic
- **Disclosed:** Affiliate links, sponsorships noted
- **Undisclosed:** Potential conflicts not mentioned

### Confirmation Bias Warning
- "This source only presents one side"
- "Contradictory evidence exists"
- "Consensus vs. outlier view"

---

## Domain-Specific Research Patterns

### Product/Competitive Research (ClawMart/Gumroad)
1. Search: "[Product] vs [competitor] review"
2. Check: Pricing pages, feature lists
3. Mine: Reddit for real user experiences
4. Extract: Structured comparison table

### Scientific/Medical Research
1. Start: PubMed, Cochrane Library for clinical
2. Check: arXiv for preprints
3. Verify: Primary sources, not news summaries
4. Flag: Single studies vs. meta-analyses

### Financial Research
1. SEC filings (10-K, 10-Q) for public companies
2. Earnings call transcripts
3. Analyst reports (paid) â use summaries from news
4. ExchangeRate-API for currency data

### Legal Research
1. Court documents via PACER or public dockets
2. Legal databases (Westlaw, Lexis â paywalled)
3. Law reviews and journals
4. Regulatory agency guidance

---

## Configuration

### research-config.json
```json
{
  "apis": {
    "newsapi": {
      "key": "YOUR_NEWSAPI_KEY",
      "tier": "free"
    },
    "openweather": {
      "key": "YOUR_OPENWEATHER_KEY",
      "tier": "free"
    },
    "exchangerate": {
      "key": "YOUR_EXCHANGERATE_KEY",
      "tier": "free"
    }
  },
  "defaults": {
    "max_sources": 10,
    "recency_preference": "balanced",
    "output_format": "brief",
    "confidence_threshold": "medium"
  },
  "quality_thresholds": {
    "min_credibility": "medium",
    "max_age_days": 365,
    "require_diversity": true
  },
  "stopping_conditions": {
    "max_sources": 15,
    "max_time_minutes": 15,
    "saturation_threshold": 3
  }
}
```

---

## Examples

### Example 1: Quick Research
```
User: "Research AI video generation trends"

Agent:
## Research Brief: AI Video Generation Trends

### Executive Summary
AI video generation has exploded in 2024-2025 with Runway, Pika, and Kling leading consumer tools. Quality improved dramatically â 4-second clips now rival professional footage. Open-source alternatives (Stable Video Diffusion) gaining traction. Key limitation: temporal consistency in longer sequences.

### Key Findings
1. **Runway Gen-2** is market leader for quality â $15/mo, 4-second clips
2. **Pika Labs** offers budget alternative at $8/mo with good results
3. **Kling AI** (China-based) emerging as quality competitor
4. **Open source** (Stable Video Diffusion) viable for technical users

### Sources
- [The State of AI Video 2025](URL) â Web, Jan 2025
- [Runway vs Pika: Comparison](URL) â YouTube, TechChannel
- [Stable Video Diffusion Paper](URL) â arXiv, 2024
- [r/MachineLearning discussion](URL) â Reddit, Feb 2025

### Confidence Score: High
Multiple Tier 2+ sources confirm, recent data, established consensus. Zero contradictions.

### Suggested Next Steps
- Deep dive into temporal consistency solutions
- Compare pricing for high-volume production
- Research enterprise alternatives (Sora, etc.)
```

### Example 2: Competitive Analysis with Paywall Bypass
```
User: "Compare ElevenLabs vs Play.ht for voice generation"

Agent:
## Comparison: ElevenLabs vs Play.ht

### At a Glance
| Dimension | ElevenLabs | Play.ht | Winner |
|-----------|------------|---------|--------|
| Price | $5/mo | $30/mo | ElevenLabs |
| Quality | Excellent | Good | ElevenLabs |
| Languages | 29 | 142 | Play.ht |
| API | Yes | Yes | Tie |

### Pricing Research
- ElevenLabs: $5/mo Starter, $22/mo Creator (source: pricing page)
- Play.ht: $30/mo Personal, $99/mo Pro (source: pricing page)

### User Sentiment (Reddit r/elevenlabs, r/speech synthesis)
- ElevenLabs: 85% positive (quality praised, occasional latency issues)
- Play.ht: 70% positive (good languages, expensive for quality)

### Verdict
ElevenLabs for quality/price, Play.ht if you need obscure languages.

[Full breakdown with sources...]
```

---

## Guardrails
- Always cite sources â never present synthesis as original research
- Flag uncertainty with calibrated language ("likely" vs "confirms")
- Bypass paywalls before skipping â don't leave knowledge on the table
- Respect rate limits â cache results, batch when possible
- Verify recency â old data can mislead
- Acknowledge gaps â "limited research exists on..."
- Stop when conditions met â don't over-research

## Troubleshooting

**Error: "No results found"**
- Try broader search terms
- Check tool availability
- Verify internet connection

**Error: "Rate limit exceeded"**
- Wait 60 seconds, retry
- Switch to fallback tools
- Use cached results when available

**Error: "Source quality too low"**
- Broaden search terms
- Remove recency filter
- Try alternative sources from tool matrix
- Accept "Low confidence" finding

**Error: "Paywall blocking access"**
- Try archive.org
- Try 12ft.io
- Try textise dot iitty
- Use browser tool to extract
- Only skip if all methods fail

---

## Version History
- **V1.0:** Multi-source search, synthesis, 4 output formats
- **V1.1:** Bias detection, temporal research, competitive analysis
- **V1.2:** Source quality scoring, citation export, research history
- **V1.3:** Public APIs integration â NewsAPI, OpenWeather, ExchangeRate-API, REST Countries
- **V1.4:** 
  - Added tool selection matrix (platform-agnostic)
  - Added paywall bypass strategy
  - Added confidence calibration system
  - Added stopping conditions
  - Added structured data extraction patterns
  - Added domain-specific research patterns

---

*Turn information into intelligence.*
