# Amazon Keyword Match Type Guide

A reference for choosing the right match type at each campaign stage and knowing when to change it.

---

## Match Type Overview

| Match Type | Trigger Behavior | Best For | Typical Bid vs. Exact |
|---|---|---|---|
| Auto | Amazon chooses all queries | Initial discovery, finding unexpected terms | 40-60% of exact |
| Broad | Query contains keyword words in any order | Wide research phase, cheap impressions | 55-70% of exact |
| Phrase | Query contains keyword in order, with words before/after | Moderate control, phrase intent confirmation | 70-85% of exact |
| Exact | Query matches keyword exactly (minor variations allowed) | Proven converters, tight ACoS optimization | 100% (baseline) |

---

## When to Use Each Match Type

### Auto Campaigns — Use when:
- Launching a brand-new ASIN with no search term history
- You want Amazon's algorithm to find unconventional but converting queries
- You need baseline data on how Amazon categorizes your product
- You want to discover ASIN targeting opportunities (auto includes product targeting)

**Caution:** Auto campaigns give Amazon the most control. They almost always require negative keywords within 7 days to prevent waste. Never run auto campaigns without a daily budget cap.

### Broad Match — Use when:
- You have 5-20 seed keywords and want to test variations without paying exact rates
- The product has many synonyms, related phrases, or alternative descriptions
- You want phrase variations like "best [keyword]", "[keyword] for women", "[keyword] under $20"

**Caution:** Broad can generate surprising matches. Keyword "yoga mat" on broad can trigger "door mat" or "yoga mat cleaning spray" — always review search term reports weekly.

### Phrase Match — Use when:
- You've confirmed a search term pattern from auto/broad data
- The keyword has a core phrase that must stay intact (word order matters)
- You want middle-ground control between broad discovery and exact precision

**Example:** Phrase match "silicone spatula" would trigger for:
- "best silicone spatula for eggs" ✓
- "red silicone spatula set" ✓
- "silicone spatula cleaning" ✓
- "spatula silicone" ✗ (order broken)

### Exact Match — Use when:
- A search term has 5+ conversions at or below your target ACoS
- You want maximum bid control over a proven, high-value query
- You're protecting branded terms from ACoS inflation
- You've graduated a term from auto/broad and want to optimize it independently

---

## Match Type Interaction and Cannibalization

Running the same keyword across multiple match types in different campaigns is intentional — but requires negative keywords to prevent overlap.

**Standard isolation setup:**

1. Add the exact-match term as a negative exact in your auto and broad campaigns
2. Add the exact-match term as a negative phrase in your phrase campaign
3. This forces Amazon to serve each match type from its intended campaign

**Why this matters:** Without negatives, Amazon may serve your exact-match ad from the broad campaign at the broad bid — undercutting the exact match bid you worked out from margin math.

---

## Search Term Graduation Workflow

This is the core mechanism that converts research spend into optimized performance spend.

```
Auto Campaign → Search Term Report
    ↓ (5+ conversions at target ACoS)
Create Exact Match Campaign for that term
    ↓
Add term as exact negative in Auto Campaign
    ↓
Monitor exact campaign for 14 days
    ↓ (ACoS stable or improving)
Increase bid 10% and continue
    ↓ (ACoS rising above target)
Decrease bid 15%, monitor 7 more days
```

---

## Negative Keyword Match Types

Negative exact: Blocks only the precise query
Negative phrase: Blocks the phrase and any query containing it

Use negative exact for: specific irrelevant terms you've seen in reports
Use negative phrase for: category-level exclusions ("how to", "diy", "free", "repair", competitor brand names)

**Example:**
- Negative exact "yoga mat blue" → only blocks "yoga mat blue"
- Negative phrase "yoga mat cleaning" → blocks "yoga mat cleaning spray", "best yoga mat cleaning method", etc.

---

## Common Bidding Formulas

```
Max CPC = ASP × Target ACoS × Estimated CVR
Break-even CPC = ASP × Gross Margin % × CVR

Example ($30 product, 40% margin, 10% CVR, 30% target ACoS):
Max CPC = $30 × 0.30 × 0.10 = $0.90
Break-even CPC = $30 × 0.40 × 0.10 = $1.20
Headroom = $1.20 - $0.90 = $0.30 per click for profit contribution
```

If actual CPC ends up above your break-even CPC consistently, the campaign is losing money on a unit economics basis regardless of what the ACoS % shows.
