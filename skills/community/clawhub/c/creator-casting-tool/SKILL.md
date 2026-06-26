---
name: creator-casting-tool
description: "Find the right creators for any brand campaign, activation, or ambassador program. Takes a campaign brief (brand, vibe, category, budget, audience), searches Instagram, TikTok, YouTube, and Substack, and returns a castable shortlist with stats, content examples, rate estimates, and brand conflict checks. Use when casting creators for campaigns, sourcing influencers for a brand, building ambassador shortlists, finding creators for events/activations, or matching talent to a brief. Triggers on: 'find creators for,' 'cast for this campaign,' 'who should we use for,' 'source influencers,' 'creator shortlist,' 'casting list,' 'find talent for [brand],' 'ambassador search,' or any request to match creators to a brand or campaign brief."
---

# Creator Casting Tool

Find and shortlist the right creators for any brand campaign, activation, event, or ambassador program.

## Who This Is For

- Brand marketing teams casting influencer campaigns
- PR and comms agencies sourcing talent for clients
- Casting directors for events, activations, content shoots
- DTC brands building ambassador or affiliate programs
- Creative agencies staffing content productions

## Prerequisites

- **web_search** tool (required) — for cross-platform discovery, rate research, conflict checks
- **web_fetch** tool (required) — for reading profiles, articles, and content
- **gram CLI** (optional but recommended) — for Instagram discovery, engagement data, and content analysis. If unavailable, web search is used as fallback.

Check gram:
```bash
which gram
```

## Workflow

### 1. Collect Campaign Brief

Ask the user for (or detect from context):

| Parameter | Required | Description |
|-----------|----------|-------------|
| `brand` | yes | Brand name and brief description |
| `campaign_type` | yes | Content, event, activation, ambassador, gifting, UGC |
| `category` | yes | Fashion, beauty, food, fitness, lifestyle, art, tech, travel, wellness, home, luxury, music, gaming, comedy, parenting, finance |
| `vibe` | yes | Aesthetic/tonal direction (e.g., "minimalist, editorial, elevated" or "playful, bold, Gen-Z") |
| `audience_demo` | recommended | Target audience age, gender, location |
| `budget_range` | recommended | Per-creator budget (e.g., "$1K-5K" or "$10K+") |
| `num_creators` | 10 | How many to return |
| `platforms` | all | Which platforms matter: instagram, tiktok, youtube, substack |
| `follower_range` | 10K-500K | Min and max followers |
| `geo_focus` | US | Geographic focus for creators |
| `exclusions` | none | Competitor brands, creators to avoid, agencies to skip |
| `deliverables` | optional | What the creators would produce (e.g., "1 IG Reel + 3 Stories") |

### 2. Discover Creators

Search across platforms for creators matching the brief. Cast a wide net (40-60 candidates) to filter down.

**Instagram (via gram CLI if available):**
```bash
gram search "[category] [vibe keyword]" --limit 20
gram explore "[category]" --limit 20
gram hashtag "[relevant hashtag]" --limit 20
```

If gram unavailable, use web search:
```
"[category] [vibe] instagram creator" [geo]
"[category] influencer" aesthetic [vibe keywords] 2026
site:instagram.com "[category]" "[vibe keyword]"
```

**TikTok:**
```
"[category] tiktok creator" [vibe] [geo] 2026
"[category] tiktoker" [audience_demo keywords]
"best [category] tiktok" [vibe] creators
```

**YouTube:**
```
"[category] youtube creator" [vibe] [geo]
"[category] youtuber" [audience_demo] subscribers
```

**Substack:**
```
"[category] substack" [vibe] newsletter writer
site:substack.com "[category]" "[vibe keyword]"
```

**Also search for:**
```
"[brand name] type creator" OR "[competitor brand] influencer"
"[vibe] creators to watch 2026"
"[category] creators for brand campaigns"
best "[category] [vibe]" influencer lists 2026
```

**Listicles and round-ups** (great for discovery):
```
"[category] influencers to watch 2026"
"[vibe] creators" brand campaign
"best [category] content creators" [geo]
```

### 3. Gather Creator Profiles

For each candidate, collect:

**From gram (if available):**
```bash
gram user info [handle]
gram user posts [handle] --limit 12
```

**From web search / web_fetch:**
```
"[creator name]" [platform] followers engagement
"[creator handle]" brand partnership OR sponsored
"[creator name]" rate OR pricing (for rate estimates)
```

Build a profile for each:
- Name / handles per platform
- Follower counts per platform
- Engagement quality (like-to-follower ratio, comment quality, saves if visible)
- Content style and aesthetic
- Audience demo indicators (comments, content topics, stated location)
- Recent brand partnerships (last 6 months)
- Content quality notes (production value, editing, originality)

### 4. Check Brand Conflicts

This is critical. For each candidate, check if they're currently working with or recently posted for a competitor.

```
"[creator name]" "[competitor brand 1]" OR "[competitor brand 2]"
"[creator handle]" sponsored "[competitor category]"
```

**From gram (if available):**
```bash
gram user posts [handle] --limit 30
```
Scan recent posts for competitor brand tags, #ad/#sponsored with competitors, or gifted product from competing brands.

Classify as:
- **Clear** — No competitor conflicts found
- **Potential conflict** — Posted competitor product but unclear if paid
- **Active conflict** — Currently in a paid campaign with a competitor → FLAG prominently

Also check for:
- Controversial content or past brand safety issues
- Alignment between creator's personal brand and the campaign brand

### 5. Estimate Rates

Based on follower count, engagement, platform, and niche, estimate per-creator rates:

| Follower Range | IG Post | IG Reel | IG Story Set | TikTok | YouTube |
|----------------|---------|---------|--------------|--------|---------|
| 10K-50K | $250-1K | $500-2K | $150-500 | $300-1.5K | $500-2K |
| 50K-100K | $1K-3K | $2K-5K | $500-1.5K | $1.5K-4K | $2K-5K |
| 100K-250K | $3K-7K | $5K-10K | $1.5K-3K | $4K-8K | $5K-10K |
| 250K-500K | $7K-15K | $10K-20K | $3K-5K | $8K-15K | $10K-25K |
| 500K+ | $15K+ | $20K+ | $5K+ | $15K+ | $25K+ |

Adjust estimates based on:
- **Niche premium:** Luxury, finance, tech command higher rates
- **Engagement quality:** High engagement = higher rates justified
- **Content production value:** High-quality production = premium
- **Exclusivity:** If campaign requires exclusivity, add 30-50%

Cross-reference with web search:
```
"[creator name]" rate card OR pricing
influencer rate calculator [follower count] [platform]
```

Note: These are ESTIMATES. Always flag them as approximate.

### 6. Score & Rank (1-100 Campaign Fit Score)

| Signal | Points |
|--------|--------|
| Aesthetic/vibe alignment with brief | +25 |
| Audience demo match | +20 |
| Engagement quality (not just rate — comment quality, saves, shares) | +15 |
| Brand safety — clean history, no conflicts | +15 |
| Within budget range | +10 |
| Multi-platform presence (amplification potential) | +10 |
| Past brand campaign experience (knows how to deliver) | +5 |

Deductions:
- Active competitor conflict: -30
- Potential competitor conflict: -10
- Low engagement relative to following: -15
- Inconsistent posting: -10
- Content quality below brief standard: -20

### 7. Output Format

```markdown
# Creator Casting Report

**Brand:** [brand name]
**Campaign:** [campaign type and description]
**Category:** [category]
**Vibe:** [vibe description]
**Budget:** [per-creator range]
**Platforms:** [target platforms]
**Geo:** [geographic focus]
**Candidates Screened:** [total reviewed]
**Shortlist:** [number returned]

---

## Shortlist

### 1. [Creator Name] — Fit Score: [X]/100
**Handles:** IG @[handle] ([X]K) · TikTok @[handle] ([X]K) · YT [channel] ([X]K)
**Engagement:** [avg likes/comments per post, engagement rate if available]
**Content Style:** [2-3 sentence description of their aesthetic and content approach]
**Why They Fit:** [Specific reasons this creator matches the brief — reference vibe, audience, content style]
**Recent Brand Work:** [List 2-3 recent partnerships if any, or "No recent sponsored content visible"]
**Conflict Check:** 🟢 Clear / 🟡 Potential conflict with [brand] / 🔴 Active conflict with [brand]
**Est. Rate:** $[X]-[Y] for [deliverable type]
**Content Examples:** [Link or describe 2-3 posts that demonstrate campaign-relevant content]
**Notes:** [Anything else relevant — representation status, availability signals, negotiation notes]

---

### 2. [Creator Name] — Fit Score: [X]/100
...

---

## Budget Summary

| Creator | Est. Rate | Fit Score | Conflict |
|---------|-----------|-----------|----------|
| [Name] | $[X]-[Y] | [score] | 🟢/🟡/🔴 |
| ... | ... | ... | ... |
| **Total Est. Range** | **$[min]-[max]** | | |

## Casting Notes
- **Best value picks:** [creators with high fit score relative to rate]
- **Premium picks:** [highest fit score, may be above budget]
- **Safe bets:** [proven brand campaign performers with clean histories]
- **Rising stars:** [smaller but high-momentum, great for long-term ambassador programs]

## Methodology
- Platforms searched: [list]
- Search queries run: [count]
- Candidates screened: [count]
- Excluded (conflicts): [count]
- Excluded (poor fit): [count]
- Instagram data source: [gram CLI / web search]
- Rate estimates are approximate and based on publicly available data + industry benchmarks
```

## Error Handling

| Issue | Action |
|-------|--------|
| gram not installed | Use web search for all Instagram data; note reduced accuracy in engagement metrics |
| Vague brief | Ask clarifying questions before searching. Minimum: brand, category, vibe |
| No budget given | Return creators across ranges, flag estimated rates, let user filter |
| Very niche category | Broaden to adjacent categories, note limited pool |
| Can't find enough creators | Lower follower minimum, expand geo, broaden vibe interpretation. Report what you found. |
| Rate data unavailable | Use benchmark table, flag as "estimated based on industry averages" |
| Competitor list unclear | Ask user to confirm top 3-5 competitors to check against |
| Creator has no recent posts | Flag as "potentially inactive" with last post date |

## Tips for Best Results

- Be specific with the vibe. "Elevated minimalist with warm tones" yields better results than "fashion"
- Include competitor brands in exclusions — this prevents embarrassing casting overlaps
- For ambassador programs, prioritize creators with owned audience (newsletter, podcast, Substack) over pure social
- Smaller creators (10K-50K) often deliver better engagement rates and are more responsive to briefs
- Always verify shortlist manually before presenting to a client — this tool finds candidates, humans close deals
- Run quarterly for ongoing programs to catch rising creators before they price up
- For events/activations, factor in location — a creator's city matters for in-person work
