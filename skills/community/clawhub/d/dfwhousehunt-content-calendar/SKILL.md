---
name: dfw-content-calendar
description: Generate 7-day or 30-day social media content calendars for any niche. Outputs structured JSON + human-readable schedule with hooks, body copy, CTAs, and hashtags per post. Free tier: 7-day calendar. Premium: 30-day, multi-platform, A/B variants, CSV export.
version: 1.0.0
author: dfw-area-house-hunt
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
    homepage: https://github.com/dfw-area-house-hunt/openclaw-skills
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

## What this skill does

Generates structured content calendars for any niche with:

- **Variety enforcement** — topics rotate so nothing repeats within 7 days
- **Platform-aware formatting** — character limits, hashtag counts, and tone matched per platform
- **Content mix** — market education, social proof, objection busting, community spotlight, CTAs (5-pillar rotation)
- **Hook-first structure** — every post opens with a pattern interrupt, not a topic statement
- **JSON + human-readable output** — paste JSON into your scheduler; read the human format to review quickly

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
python3 generate_calendar.py --niche="DFW real estate" --audience="first-time buyers"

# Full options
python3 generate_calendar.py \
  --niche="DFW mortgage broker" \
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
| `--niche` | required | Your brand/industry (e.g. "DFW real estate agent") |
| `--audience` | "general" | Target reader (e.g. "first-time homebuyers") |
| `--platform` | linkedin | linkedin / x / facebook / instagram / all |
| `--days` | 7 | 7 or 30 |
| `--tone` | conversational | conversational / educational / urgent / luxury / bold |
| `--ab-variants` | off | Generate 2 hook options per post |
| `--csv` | off | Export calendar as CSV |
| `--theme` | auto | Weekly theme override |
| `--demo` | off | Run on built-in sample, zero API calls |
| `--version` | off | Print version |
| `--format` | human | human / json |

## Output contract

**Human-readable output:**
```
=== 30-Day LinkedIn Calendar: DFW Mortgage Broker → Move-Up Buyers ===

Week 1 Theme: Market Reality

--- Day 1 (Mon) | LinkedIn | Market Education ---
HOOK: Most DFW move-up buyers don't realize they already have the equity to do this.
BODY: If you bought your home 3-5 years ago, you're sitting on an average of $87,000 in
      equity. That's your down payment for the next place — without touching savings.
      The math most people don't run: sell at today's prices, buy at today's prices,
      and the equity gap covers the difference more than you think.
CTA:  Drop your zip code below — I'll run the numbers for your neighborhood.
HASHTAGS: #DFWRealEstate #HomeEquity #MovingUp #DFWHomes
CHARS: 487
```

**JSON output (`--format=json`):**
```json
{
  "metadata": {
    "niche": "DFW Mortgage Broker",
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
          "hook": "Most DFW move-up buyers don't realize they already have the equity to do this.",
          "body": "...",
          "cta": "Drop your zip code below — I'll run the numbers for your neighborhood.",
          "hashtags": ["#DFWRealEstate", "#HomeEquity", "#MovingUp", "#DFWHomes"],
          "char_count": 487,
          "hook_b": null
        }
      ]
    }
  ]
}
```

**CSV output (`--csv`, compatible with Buffer/Hootsuite/Notion):**
```
day,weekday,platform,hook,body,cta,hashtags,char_count
1,Mon,linkedin,"Most DFW move-up buyers...","If you bought your home...","Drop your zip code...","#DFWRealEstate #HomeEquity",487
```

## How the skill works

Uses `generate_calendar.py` in this directory. Local MLX first (free, unlimited), Haiku fallback.

```python
CONTENT_MIX = {
    "market_education": 0.25,   # Stats, trends, myth-busting
    "social_proof":     0.20,   # Client outcomes, testimonials
    "objection_bust":   0.20,   # Handle common objections
    "community":        0.15,   # Local spotlight, brand building
    "direct_cta":       0.20,   # Urgency-driven asks
}

WEEK_THEMES = [
    "Market Reality",       # Week 1 — establish authority with facts
    "Social Proof",         # Week 2 — build trust with outcomes
    "Education",            # Week 3 — deepen value with expertise
    "Urgency & Action",     # Week 4 — close with timing
]

PLATFORM_LIMITS = {
    "linkedin":  {"chars": 3000, "hashtags": 5,  "tone": "professional"},
    "x":         {"chars": 280,  "hashtags": 2,  "tone": "punchy"},
    "facebook":  {"chars": 500,  "hashtags": 3,  "tone": "community"},
    "instagram": {"chars": 300,  "hashtags": 10, "tone": "visual-first"},
}
```

**Core generation prompt:**
```python
CALENDAR_SYSTEM = """You are a social media strategist and direct-response copywriter.
Generate {days} days of {platform} content for: {niche} targeting {audience}.

Rules:
- Hook first: every post opens with a pattern interrupt — a question, stat, or bold claim
- No topic repeats within 7 days
- Match platform tone: {platform_tone}
- Content mix: 25% education, 20% social proof, 20% objection handling, 15% community, 20% CTA
- Week themes: {week_themes}
- Keep under {char_limit} characters per post
- {tone_instruction}
- Never use: [forbidden words for niche]

Output ONLY valid JSON matching the schema provided."""
```

## Usage patterns

**Patrick's 2-hour content schedule method:**
```bash
# Step 1: Generate 30-day calendar
python3 generate_calendar.py --niche="DFW mortgage broker" --audience="move-up buyers" \
  --platform=linkedin --days=30 --csv --output=calendar_march.csv

# Step 2: Review and approve in CSV (Buffer, Hootsuite, Notion)
# Step 3: Schedule — done in 10 minutes
```

**Multi-platform week:**
```bash
# All 4 platforms, 7 days, A/B hooks
python3 generate_calendar.py --niche="DFW real estate" --audience="first-time buyers" \
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
@openclaw content-calendar "30-day LinkedIn calendar for DFW mortgage broker targeting move-up buyers"
@openclaw content-calendar "7-day X calendar, crypto niche, bold tone"

# Via Claude Code
openclaw run content-calendar --niche="real estate" --days=30 --platform=linkedin
```

## Content pillar reference

| Pillar | % of calendar | What it does | Example hook |
|---|---|---|---|
| Market Education | 25% | Build authority with facts | "Most DFW buyers don't know this costs them $340/month" |
| Social Proof | 20% | Build trust with outcomes | "Client bought in Frisco with $0 out of pocket. Here's how." |
| Objection Busting | 20% | Remove buying resistance | "Waiting for rates to drop? Here's what that's actually costing you." |
| Community | 15% | Brand affinity, local presence | "Best kept secret neighborhood in McKinney right now" |
| Direct CTA | 20% | Drive action | "Drop your zip code — I'll pull what's moving in your area today." |
