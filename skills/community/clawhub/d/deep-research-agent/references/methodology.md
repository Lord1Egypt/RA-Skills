# Research Agent — Methodology Reference

## Source Hierarchy

Rank sources by reliability:

| Level | Source Type | Confidence | Example |
|-------|------------|------------|---------|
| 1 | Official docs / primary source | High | Project README, official API docs |
| 2 | Code / data | High | GitHub repo, benchmarks, usage stats |
| 3 | Expert analysis | Medium-High | Technical blog posts, conference talks |
| 4 | Community discussion | Medium | Reddit, HN, Discord, Stack Overflow |
| 5 | News / press | Medium-Low | TechCrunch, press releases |
| 6 | Opinion / speculation | Low | Personal blogs, social media hot takes |

**Rule:** Always cite the highest-level source available. If you only have Level 4-6 sources, flag the finding as "unverified."

## Research Report Template

```markdown
# Research: [Topic]

**Date:** YYYY-MM-DD
**Question:** [Original research question]
**Confidence:** High / Medium / Low

## Executive Summary

[3-5 sentences. What did we find? What's the bottom line?]

## Key Findings

1. **[Finding]** — [1 sentence explanation] (Source: [URL])
2. **[Finding]** — [1 sentence explanation] (Source: [URL])
3. **[Finding]** — [1 sentence explanation] (Source: [URL])

## Detailed Analysis

### [Theme 1]
[Analysis with supporting evidence]

### [Theme 2]
[Analysis with supporting evidence]

## Gaps & Caveats

- [What we couldn't verify]
- [What might have changed since source was published]
- [Author biases in our sources]

## Recommendation

[If applicable. Clear, actionable, with reasoning.]

## Sources

1. [Title](URL) — [credibility level, date]
2. [Title](URL) — [credibility level, date]
```

## Comparison Matrix Template

```markdown
| Dimension | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| [Feature] | 30%    | ⭐⭐⭐⭐   | ⭐⭐⭐     | ⭐⭐⭐⭐⭐  |
| [Cost]    | 20%    | ⭐⭐       | ⭐⭐⭐⭐   | ⭐⭐⭐     |
| [Ease]    | 25%    | ⭐⭐⭐⭐⭐  | ⭐⭐⭐     | ⭐⭐       |
| [Ecosystem]| 25%   | ⭐⭐⭐     | ⭐⭐⭐⭐⭐  | ⭐⭐⭐⭐   |
| **Total** | 100%   | **3.4**  | **3.7**  | **3.5**  |

**Recommendation:**
- Choose A if [condition]
- Choose B if [condition]
- Choose C if [condition]
```

## Web Search Strategy

When researching a topic, run these searches in order:

1. **Official:** `"[topic]" site:github.com` or `"[topic]" official docs`
2. **Community:** `"[topic]" site:reddit.com` or `"[topic]" site:news.ycombinator.com`
3. **Comparison:** `"[topic]" vs alternatives comparison 2026`
4. **Critical:** `"[topic]" problems limitations issues`
5. **Stats:** `"[topic]" stars users adoption metrics`

This gives you: official story → real user opinions → competitive context → honest downsides → market validation.

## Bias Detection

Watch for these biases in sources:

| Bias | Signal | Counter |
|------|--------|---------|
| **Sponsor bias** | "In partnership with..." | Find independent reviews |
| **Recency bias** | "Latest and greatest" | Check if older solutions still work |
| **Popularity bias** | "Most popular = best" | Best for whom? For what? |
| **Confirmation bias** | Only positive mentions | Actively search for criticism |
| **Author bias** | Author works for the company | Weight community sources higher |

## When to Stop Researching

- **Quick mode:** 1-2 sources. Done in 30 seconds.
- **Deep Dive mode:** 5-10 sources. Stop when themes repeat.
- **Compare mode:** 1 source per option + 1 independent comparison. Done.
- **Landscape mode:** Enough to categorize all major players. Usually 10-20 sources.
- **Evaluate mode:** Enough to score each dimension with confidence. Usually 5-8 sources.

**Diminishing returns rule:** If your last 3 sources didn't change your conclusion, stop.
