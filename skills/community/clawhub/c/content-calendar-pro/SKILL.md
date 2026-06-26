---
name: content-calendar-pro
description: Generate 7-day or 30-day social media content calendars for any niche. Each post is scored for engagement quality (hook strength, specificity, platform fit, CTA clarity) — posts below threshold auto-rewrite. Supports past-performance input to adapt theme weighting toward what worked. Free tier: 7-day calendar. Premium: 30-day, multi-platform, A/B variants, CSV export, engagement tracker.
version: 1.2.0
author: drivenautoplex1
price: 0
tags:
  - content
  - social-media
  - marketing
  - content-calendar
  - scheduling
  - real-estate
  - mortgage
  - crypto
  - saas
  - e-commerce
  - copywriting
  - linkedin
  - twitter
  - instagram
  - facebook
metadata:
  openclaw:
    requires:
      env:
        - ANTHROPIC_API_KEY
      anyBins:
        - python3
    primaryEnv: ANTHROPIC_API_KEY
    emoji: "📅"
    homepage: https://github.com/drivenautoplex1/openclaw-skills
    install:
      - kind: uv
        package: anthropic
        bins: []
---

# Content Calendar Skill

Generate a full month of social content in minutes. Paste in your niche and audience — get back a structured, ready-to-schedule calendar with varied hooks, body copy, CTAs, and hashtags.

## Free vs Premium

**Free tier (no API key needed):**
- `--demo` — generates a complete 7-day real estate sample calendar, zero API calls
- `--version` — print skill version
- `--compliance-only` — check any copy for forbidden words before posting

**Free tier (API key required):**
- 7-day calendar on any platform/niche
- Structured JSON + human-readable output
- Single platform per run

**Premium features (same API key, no upgrade needed):**
- `--days=30` — full 30-day calendars
- `--platforms=all` — LinkedIn + X + Facebook + Instagram in one run
- `--ab-variants` — 2 hook variants per post for A/B testing
- `--csv` — export to CSV for Buffer, Hootsuite, Notion, or any scheduler
- `--theme` — weekly theme override (e.g., "Week 2: objection busting only")
- `--min-score=75` — quality gate: posts scoring below threshold are auto-rewritten (max 2 passes)
- `--past-results=results.json` — feed in engagement data from previous runs; skill adapts theme weights toward what worked
- `--tracker` — output blank engagement tracker template alongside the calendar (paste into Notion/Sheets)

## What this skill does

Generates structured content calendars for any niche with:

- **Variety enforcement** — topics rotate so nothing repeats within 7 days
- **Platform-aware formatting** — character limits, hashtag counts, and tone matched per platform
- **Content mix** — market education, social proof, objection busting, community spotlight, CTAs (5-pillar rotation)
- **Hook-first structure** — every post opens with a pattern interrupt, not a topic statement
- **JSON + human-readable output** — paste JSON into your scheduler; read the human format to review quickly
- **Post-level quality scoring** — every post scored 0–100 across 4 dimensions before output
- **Auto-rewrite loop** — posts below `--min-score` threshold regenerated with fix instructions (max 2 passes)
- **Adaptive theme weighting** — pass in past engagement data and the skill shifts content mix toward what converted

## Supported verticals

| Niche | Example brand voice |
|---|---|
| Real estate | Market urgency, local expertise, lifestyle |
| Mortgage / lending | Education-first, trust-building, compliance-safe |
| Crypto / DeFi | Data-driven, opportunity framing, risk-aware |
| SaaS / tech | Problem-solution, feature → benefit, ROI focus |
| E-commerce | Product-led, social proof heavy, seasonal hooks |
| Coaching / consulting | Authority positioning, transformation stories |
| Healthcare / wellness | Empathy-first, outcome-focused, evidence-backed |
| Any niche | Pass `--niche="your niche"` and `--audience="your audience"` |

## Input contract

```bash
# Minimum — niche and audience
python3 generate_calendar.py --niche="real estate" --audience="first-time buyers"

# Full options
python3 generate_calendar.py \
  --niche="mortgage broker" \
  --audience="move-up buyers" \
  --platform=linkedin \
  --days=30 \
  --tone=educational \
  --ab-variants \
  --csv \
  --output=my_calendar.json
```

**Options:**
| Flag | Default | Description |
|---|---|---|
| `--niche` | required | Your brand/industry (e.g. "real estate agent") |
| `--audience` | "general" | Target reader (e.g. "first-time homebuyers") |
| `--platform` | linkedin | linkedin / x / facebook / instagram / all |
| `--days` | 7 | 7 or 30 |
| `--tone` | conversational | conversational / educational / urgent / luxury / bold |
| `--ab-variants` | off | Generate 2 hook options per post |
| `--csv` | off | Export calendar as CSV |
| `--theme` | auto | Weekly theme override |
| `--min-score` | 70 | Quality gate — posts below this score auto-rewrite (0 to disable) |
| `--past-results` | none | Path to engagement JSON from prior run — adapts content mix |
| `--tracker` | off | Output blank engagement tracker template alongside calendar |
| `--demo` | off | Run on built-in sample, zero API calls |
| `--version` | off | Print version |
| `--format` | human | human / json |

## Output contract

**Human-readable output:**
```
=== 30-Day LinkedIn Calendar: Mortgage Broker → Move-Up Buyers ===

Week 1 Theme: Market Reality

--- Day 1 (Mon) | LinkedIn | Market Education ---
HOOK: Most move-up buyers don't realize they already have the equity to do this.
BODY: If you bought your home 3-5 years ago, you're sitting on an average of $87,000 in
      equity. That's your down payment for the next place — without touching savings.
      The math most people don't run: sell at today's prices, buy at today's prices,
      and the equity gap covers the difference more than you think.
CTA:  Drop your zip code below — I'll run the numbers for your neighborhood.
HASHTAGS: #RealEstate #HomeEquity #MovingUp #Homeownership
CHARS: 487
SCORE: 81/100 | Hook: 26/30 | Platform: 22/25 | Specificity: 20/25 | CTA: 13/20
```

**JSON output (`--format=json`):**
```json
{
  "metadata": {
    "niche": "Mortgage Broker",
    "audience": "Move-up buyers",
    "platform": "linkedin",
    "days": 30,
    "generated_at": "2026-03-27T17:00:00Z"
  },
  "weeks": [
    {
      "week": 1,
      "theme": "Market Reality",
      "posts": [
        {
          "day": 1,
          "weekday": "Mon",
          "platform": "linkedin",
          "content_type": "market_education",
          "hook": "Most move-up buyers don't realize they already have the equity to do this.",
          "body": "...",
          "cta": "Drop your zip code below — I'll run the numbers for your neighborhood.",
          "hashtags": ["#RealEstate", "#HomeEquity", "#MovingUp", "#Homeownership"],
          "char_count": 487,
          "hook_b": null,
          "engagement_score": {
            "total": 81,
            "hook_strength": 26,
            "platform_fit": 22,
            "specificity": 20,
            "cta_clarity": 13,
            "rewrites": 0
          }
        }
      ]
    }
  ]
}
```

**CSV output (`--csv`, compatible with Buffer/Hootsuite/Notion):**
```
day,weekday,platform,hook,body,cta,hashtags,char_count
1,Mon,linkedin,"Most move-up buyers...","If you bought your home...","Drop your zip code...","#RealEstate #HomeEquity",487
```

## Post Quality Scoring

Every generated post is scored across 4 dimensions before output:

| Dimension | Weight | What's measured |
|---|---|---|
| Hook strength | 30 pts | Pattern interrupt quality — does it stop the scroll? Scored on: specificity, unexpected angle, curiosity gap |
| Platform fit | 25 pts | Character count, hashtag count, tone match, reading level for platform |
| Specificity | 25 pts | Concrete numbers, named outcomes, real examples vs. vague generalities |
| CTA clarity | 20 pts | Is the ask clear? Is there exactly one action? Is friction low? |

**Total: 100 points**

Posts scoring below `--min-score` (default: 70) are automatically rewritten with targeted fix instructions (e.g., "hook is vague — add a specific number or outcome"). Max 2 rewrite passes per post.

Each post in the output includes:

```
SCORE: 81/100 | Hook: 26/30 | Platform: 22/25 | Specificity: 20/25 | CTA: 13/20
```

**Why this matters:** A calendar of 30 posts where 8 have weak hooks will underperform a calendar of 30 well-scored posts. The scoring loop catches and fixes low-quality posts before you schedule them.

## Adaptive Theme Weighting

Pass in results from a previous calendar with `--past-results=results.json`. The skill reads which content types drove the most engagement and shifts the next calendar's mix accordingly.

**Tracker format** (also generated with `--tracker`):

```json
{
  "period": "March 2026",
  "platform": "linkedin",
  "posts": [
    {
      "day": 1,
      "content_type": "market_education",
      "impressions": 1240,
      "engagement_rate": 0.048,
      "clicks": 22,
      "score_at_generation": 81
    }
  ]
}
```

**What adapts:**
- Content mix percentages shift toward top-performing `content_type` values (e.g., if social_proof drove 3× the engagement, its share increases from 20% → 30% in the next run)
- Weak themes are reduced proportionally
- Platform formatting rules stay fixed (algorithm constraints don't adapt to your data)

**Example shift:**
```
Past results: social_proof avg engagement 6.2% vs. direct_cta 1.1%
Next run mix: social_proof 30% (+10%), direct_cta 12% (−8%)
```

## Engagement Tracker Template

Run with `--tracker` to get a blank tracker alongside the calendar:

```
content-calendar-pro Engagement Tracker
Generated: [date] | Platform: [platform] | Niche: [niche]

Day | Weekday | Type           | Hook (first 60 chars)     | Score | Impressions | Eng% | Clicks | Notes
----|---------|----------------|---------------------------|-------|-------------|------|--------|-------
1   | Mon     | market_edu     | "Most buyers don't..."    | 81    | ___         | ___  | ___    |
2   | Tue     | social_proof   | "Client bought in..."     | 88    | ___         | ___  | ___    |
...
```

Paste into Notion or Google Sheets. After 30 days, export as JSON and pass to `--past-results` for an optimized next run.

## How the skill works

Uses `generate_calendar.py` in this directory. Local MLX first (free, unlimited), Haiku fallback.

```python
# Base content mix — shifts when --past-results provided
DEFAULT_CONTENT_MIX = {
    "market_education": 0.25,   # Stats, trends, myth-busting
    "social_proof":     0.20,   # Client outcomes, testimonials
    "objection_bust":   0.20,   # Handle common objections
    "community":        0.15,   # Local spotlight, brand building
    "direct_cta":       0.20,   # Urgency-driven asks
}

# Adaptive mix: past_results → recalculate weights toward top performers
def adaptive_content_mix(past_results, base_mix=DEFAULT_CONTENT_MIX):
    if not past_results:
        return base_mix
    # Compute avg engagement rate per content_type from past results
    perf = {}
    for post in past_results["posts"]:
        ct = post["content_type"]
        perf.setdefault(ct, []).append(post.get("engagement_rate", 0))
    avg_perf = {ct: sum(v)/len(v) for ct, v in perf.items()}
    # Blend: 60% performance-weighted, 40% base (prevents over-pivoting)
    total_perf = sum(avg_perf.values()) or 1
    new_mix = {}
    for ct in base_mix:
        perf_weight = avg_perf.get(ct, sum(avg_perf.values()) / len(base_mix)) / total_perf
        new_mix[ct] = 0.6 * perf_weight + 0.4 * base_mix[ct]
    # Normalize to 1.0
    total = sum(new_mix.values())
    return {ct: v / total for ct, v in new_mix.items()}

WEEK_THEMES = [
    "Market Reality",       # Week 1 — establish authority with facts
    "Social Proof",         # Week 2 — build trust with outcomes
    "Education",            # Week 3 — deepen value with expertise
    "Urgency & Action",     # Week 4 — close with timing
]

PLATFORM_LIMITS = {
    "linkedin":  {"chars": 3000, "hashtags": 5,  "tone": "professional", "reading_level": "grade_10"},
    "x":         {"chars": 280,  "hashtags": 2,  "tone": "punchy",        "reading_level": "grade_8"},
    "facebook":  {"chars": 500,  "hashtags": 3,  "tone": "community",     "reading_level": "grade_8"},
    "instagram": {"chars": 300,  "hashtags": 10, "tone": "visual-first",  "reading_level": "grade_7"},
}

# Scoring system — runs on every generated post
POST_SCORE_WEIGHTS = {
    "hook_strength":  30,   # Pattern interrupt quality: specificity, curiosity gap, unexpected angle
    "platform_fit":   25,   # Char count, hashtag count, tone match, reading level
    "specificity":    25,   # Concrete numbers/outcomes vs. vague generalities
    "cta_clarity":    20,   # Clear single ask, low friction
}

# Auto-rewrite: posts below MIN_SCORE get regenerated with targeted fix instructions
MIN_SCORE_DEFAULT = 70
MAX_REWRITE_PASSES = 2
```

**Core generation + scoring prompt:**
```python
CALENDAR_SYSTEM = """You are a social media strategist and direct-response copywriter.
Generate {days} days of {platform} content for: {niche} targeting {audience}.

Rules:
- Hook first: every post opens with a pattern interrupt — a question, stat, or bold claim
- No topic repeats within 7 days
- Match platform tone: {platform_tone}
- Content mix: {content_mix_instructions}
- Week themes: {week_themes}
- Keep under {char_limit} characters per post
- Reading level target: {reading_level}
- {tone_instruction}
- Never use: [forbidden words for niche]

Output ONLY valid JSON matching the schema provided."""

SCORER_SYSTEM = """Score this social media post 0-100 across 4 dimensions.
Return JSON: {{"hook_strength": N, "platform_fit": N, "specificity": N, "cta_clarity": N, "total": N, "fix_notes": "..."}}
Weights: hook_strength/30, platform_fit/25, specificity/25, cta_clarity/20.
fix_notes = specific instructions to fix the lowest-scoring dimension (one sentence, actionable).
Platform: {platform}. Char limit: {char_limit}."""

REWRITER_SYSTEM = """Rewrite this post. The issue is: {fix_notes}. Keep: same topic, same CTA intent, same platform.
Change: fix the specific issue identified. Output only the rewritten post JSON."""
```

## Usage patterns

**Patrick's 2-hour content schedule method:**
```bash
# Step 1: Generate 30-day calendar with quality gate + tracker
python3 generate_calendar.py --niche="mortgage broker" --audience="move-up buyers" \
  --platform=linkedin --days=30 --csv --tracker --output=calendar_march.csv

# Step 2: Review scored posts in CSV — all posts already meet quality bar
# Step 3: Fill in tracker as you post, export results.json after 30 days
# Step 4: Next month — optimized calendar based on what worked
python3 generate_calendar.py --niche="mortgage broker" --audience="move-up buyers" \
  --platform=linkedin --days=30 --past-results=march_results.json --csv
```

**Raise the quality bar:**
```bash
# Default min-score is 70 — set 80 for premium content
python3 generate_calendar.py --niche="SaaS startup" --audience="SMB owners" \
  --days=30 --min-score=80
# Posts below 80 get up to 2 rewrite passes — slower but higher quality
```

**Multi-platform week:**
```bash
# All 4 platforms, 7 days, A/B hooks
python3 generate_calendar.py --niche="real estate" --audience="first-time buyers" \
  --platform=all --days=7 --ab-variants
```

**Crypto trading content:**
```bash
python3 generate_calendar.py --niche="crypto trader + DeFi analyst" \
  --audience="retail investors" --platform=x --days=30 --tone=bold
```

**Pipeline (JSON → scheduler automation):**
```bash
python3 generate_calendar.py --niche="SaaS startup" --audience="SMB owners" \
  --format=json | jq '.weeks[0].posts[] | {day, hook, cta}'
```

## Integration with agent infrastructure

```bash
# Via Telegram
@openclaw content-calendar "30-day LinkedIn calendar for mortgage broker targeting move-up buyers"
@openclaw content-calendar "7-day X calendar, crypto niche, bold tone"

# Via Claude Code
openclaw run content-calendar --niche="real estate" --days=30 --platform=linkedin
```

## Content pillar reference

| Pillar | % of calendar | What it does | Example hook |
|---|---|---|---|
| Market Education | 25% | Build authority with facts | "Most buyers don't know this costs them $340/month" |
| Social Proof | 20% | Build trust with outcomes | "Client bought in [City] with $0 out of pocket. Here's how." |
| Objection Busting | 20% | Remove buying resistance | "Waiting for rates to drop? Here's what that's actually costing you." |
| Community | 15% | Brand affinity, local presence | "Best kept secret neighborhood in [City] right now" |
| Direct CTA | 20% | Drive action | "Drop your zip code — I'll pull what's moving in your area today." |
