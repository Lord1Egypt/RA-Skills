---
name: competitor-intel
description: Competitive intelligence research and analysis for any company, product, or market. Use when asked to research competitors, analyze a competitor's strategy, compare products/pricing/positioning, identify market gaps, monitor competitor activity, build competitive battle cards, or assess a competitive landscape. Triggers on phrases like "competitor analysis", "competitive research", "what are competitors doing", "battle card", "market landscape", "competitive positioning", "how does X compare to Y", "spy on competitors", "competitor pricing", "SWOT analysis".
---

# Competitor Intelligence Skill

Deliver sharp, decision-ready competitive intelligence. Surface what matters, skip what doesn't.

## Workflow

### 1. Define Scope
Clarify (ask if not provided):
- **Your company/product**: What are you competing with?
- **Target competitors**: Named, or should you discover them?
- **Intelligence goal**: Pricing? Positioning? Features? Marketing? All?
- **Output format**: Quick summary, full report, or battle card?

### 2. Discover Competitors (if not named)
Use `web_search`:
- `"[product category] alternatives"`
- `"best [product type] software 2026"`
- `"[your company] vs"` — autocomplete reveals top competitors
- `site:g2.com [category]` and `site:capterra.com [category]`

### 3. Profile Each Competitor
For each competitor, gather via `web_fetch` + `web_search`:

**Positioning & Messaging**
- Homepage headline and sub-headline
- Target ICP (who they're selling to)
- Core value proposition
- Brand voice/tone

**Pricing**
- Pricing page structure (tiers, prices, what's included)
- Free trial / freemium? 
- Annual vs monthly discount
- Enterprise pricing signals

**Product/Features**
- Feature list from pricing/features pages
- Changelog or "what's new" page
- App store reviews (common complaints = their weaknesses)

**Marketing & Distribution**
- Blog topics (what keywords they're targeting)
- Social media presence + posting frequency
- Ad library: `web_search "site:facebook.com/ads [competitor]"`
- Backlink signals from SERP results

**Customer Sentiment**
- G2/Capterra/Trustpilot reviews — pull 1-star AND 5-star patterns
- Common complaints = their moats AND their gaps

### 4. Build Competitive Matrix
Use `scripts/build_matrix.py` to generate a side-by-side comparison table across:
- Pricing tiers
- Key features
- Target segment
- Positioning angle
- Strengths / Weaknesses

### 5. Identify Market Gaps
Synthesize: What are all competitors missing or doing badly? These are your wedges.

### 6. Output Options
- **Quick brief**: 1-page summary with top 3 competitors and key takeaways
- **Full report**: Complete profiles + matrix + gap analysis + recommendations
- **Battle card**: 1-page per competitor — use against in sales calls. See `references/battle-card-template.md`.

See `references/battle-card-template.md` for the battle card format.
See `references/intel-sources.md` for a full list of research sources and tools.
