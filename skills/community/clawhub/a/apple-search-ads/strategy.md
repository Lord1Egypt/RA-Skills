# Strategy Playbook — Apple Search Ads

Planning, launching, and scaling ASA campaigns. Bid math and campaign math live here; SKILL.md Core Rules reference this file. Everything assumes the standard cost-per-tap product — Apple retired the Basic (cost-per-install) tier around the Apple Ads rebrand.

Contents: Campaign Planning · Campaign Architecture · Keyword Strategy · Bidding · Scaling · Multi-Country Expansion · Custom Product Pages · Advanced Tactics · Reporting & Analysis

## Campaign Planning

### Prerequisites

- [ ] Product page conversion-ready (screenshots, first description lines) — you pay per tap, so page CVR multiplies every dollar spent
- [ ] Attribution implemented (AdServices or MMP) — without it, every optimization is a guess
- [ ] LTV estimated, even roughly — it anchors all bid math below
- [ ] Competitor research done (who ranks and bids on your terms)
- [ ] Budget floor: ~$500/month buys signal slowly; below that, expect weeks per decision

### Know Your Numbers

| Metric | Formula | Use |
|--------|---------|-----|
| Target CPA | LTV / 3 (aggressive) to LTV / 5 (conservative payback) | pick by cash runway |
| **Max CPT** | **target CPA × expected CVR** | the only bid ceiling that matters |
| Breakeven CPA | LTV − delivery/margin costs | absolute stop line |
| TTR | taps / impressions | keyword + creative relevance |
| CVR | installs / taps | product page quality |

Worked example (canonical — SKILL.md Rule 1 uses the same numbers): LTV $24, divide by 4 → target CPA $6. Expected CVR 50% → max CPT = 6 × 0.50 = $3.00. Every bid in the account derives from this ceiling.

Sanity ranges, not targets (vary widely by category and market): TTR for relevant keywords commonly 5-10%; search-results CVR is high relative to other channels (search intent) — 30-60% typical, brand terms above that; CPT roughly $0.50-3.00 in Tier-1 English markets, brand cheapest. Impression share is a trend metric reported as a range, never a point value.

## Campaign Architecture

### Hierarchy

```
Organization (orgId)
└── Campaign (one placement, one country, one intent)
    ├── Daily budget & schedule
    └── Ad Groups
        ├── Keywords (targeting + negative)
        ├── Audience (avoid refinements — see SKILL.md Traps)
        ├── Creatives (default page or Custom Product Page)
        └── Bid settings (default bid, cpaGoal)
```

### Placements (Supply Sources)

| Supply source | Placement | Best for |
|---------------|-----------|----------|
| `APPSTORE_SEARCH_RESULTS` | Top of search results | High intent; where all CPA math above applies |
| `APPSTORE_SEARCH_TAB` | Suggested apps before typing | Cheap reach, lower intent, lower CVR |
| `APPSTORE_TODAY_TAB` | App Store front page | Launches and brand moments; requires creative review |
| `APPSTORE_PRODUCT_PAGES` | "You Might Also Like" on other apps' pages | Conquesting users browsing adjacent apps |

Default: start with Search Results only; add other placements as separate campaigns once Search Results hits target CPA — never blend placements in one campaign.

### The 4-Campaign Structure

```
1. BRAND (defend)      — your app name and brand terms; goal: max impression share
2. CATEGORY (capture)  — generic intent terms; goal: volume at target CPA
3. COMPETITOR (steal)  — competitor names; goal: profitable poaching, judged slowly
4. DISCOVERY (learn)   — Search Match + broad; goal: feed terms to campaigns 1-3
```

Cross-negation wiring (do this at creation, not later): brand terms as negatives in category/discovery/competitor; every graduated term as a negative in discovery (SKILL.md Rule 4). Without it, campaigns silently buy each other's queries and every report lies.

Budget split by stage is the canonical table under Scaling below — the structure itself carries no fixed percentages.

### Ad Group Structure

Default: split ad groups **by match type** (exact / broad / discovery) — cleanest bid control and search-term reading. Switch to **theme-based** ad groups (meditation / sleep / stress) when you use Custom Product Pages: creatives attach at ad-group level, so themes are what let each keyword cluster get its matching page.

## Keyword Strategy

### Match Types

| Type | Behavior | Use case |
|------|----------|----------|
| **Exact** | Query = keyword **plus plurals and common misspellings** | Brand terms, proven converters |
| **Broad** | Synonyms, related terms, partial matches | Expansion in discovery |
| **Search Match** | Auto-matched from your app's metadata | New apps, query mining |

Search Match is seeded by your App Store metadata — improving ASO keywords literally changes what Search Match buys. Weak metadata → garbage Search Match traffic; fix order matters.

### Keyword Research Process

1. Organic search terms from App Store Connect — proven intent, seed the exact ad groups
2. Competitor keyword coverage (Sensor Tower, AppTweak, Mobile Action)
3. ASA dashboard suggestions — enter via broad at discovery bids, never straight to exact
4. Search term mining weekly — the graduate-and-negate loop (SKILL.md Rule 4) is the engine; steps 1-3 only prime it

### Keyword Tiers (bids anchored to max CPT)

| Tier | Keywords | Bid vs max CPT |
|------|----------|----------------|
| 1 | Brand terms | At or above — defense justifies it; the second-price auction (SKILL.md Rule 8) limits what you actually pay |
| 2 | Proven converters (graduated from search terms) | At max CPT |
| 3 | Category heads | Just below; raise only with CPA proof |
| 4 | Long-tail specific | Well below; cheap tests |
| 5 | Competitor names | Start low, judge on the 14-day window; usually the first tier to cut |
| 6 | Broad / Search Match | Lowest in account; their job is data, not installs |

### Negative Keywords

Immediately at launch: "free" (if paid app), competitor names (in brand campaign), unrelated categories. Campaign-level negatives = terms you never want anywhere; ad-group-level = terms that belong to a sibling ad group.

## Bidding

### Starting Bids (no-data defaults, Tier-1 English markets)

| Campaign | Starting bid | First judgment after |
|----------|--------------|----------------------|
| Brand | $2-3 | 7 days |
| Category | $1-2 | 7 days |
| Competitor | $0.50-1 | 14 days (low volume → slow signal) |
| Discovery | $0.30-0.50 | 7 days |

These are seeds, not strategy: after the first window, every bid derives from max CPT and the rules below.

### Optimization Cadence

- **Daily (5 min):** spend vs budget; apply the spend gate (SKILL.md Rule 7) to anything at ≥2× target CPA with 0 installs
- **Weekly (30 min):** search terms → graduate and negate; bid adjustments per rules below
- **Monthly (2 h):** budget reallocation across campaigns; new keyword batch; competitor drift

### Bid Adjustment Rules

```
Volume gate first: below ~50 lifetime taps on a keyword (rule of thumb),
  judge ONLY by the spend gate — CVR on a handful of taps is noise.

CPA ≤ 0.8× target AND impression share range not in the top band → bid +20%
CPA ≥ 1.2× target → bid −20%; still over after 2 more weeks → pause
Impressions ≈ 0 but keyword relevant → raise bid stepwise until impressions appear;
  if TTR <3% once they do, it is a relevance problem — no bid fixes it
```

±20% steps, one move per keyword per week: ASA has no learning-phase reset, but smaller oscillations make cause and effect readable in your own log.

## Scaling

### Budget Allocation by Stage (canonical split)

| Stage | Brand | Category | Competitor | Discovery |
|-------|-------|----------|------------|-----------|
| Launch | 40% | 40% | 10% | 10% |
| Growth | 20% | 50% | 20% | 10% |
| Scale | 10% | 60% | 25% | 5% |

### Phases

- **Validation ($500-2K/mo):** Brand + Category only, 20-50 keywords, US only. Goal: attribution verified end-to-end, first real CPA benchmark. Nothing else matters yet.
- **Optimization ($2K-10K/mo):** full 4-campaign structure, 100-200 keywords, add UK/CA/AU. Goal: hold target CPA while volume grows.
- **Scale ($10K+/mo):** campaigns per country, Custom Product Pages per theme, automation for reports and gates. Goal: max volume at CPA, not min CPA.

### Budget Scaling Rule (canonical)

Increase budgets **20-30% per step**; hold until CPA re-stabilizes at target before the next step. CPA spikes after an increase → revert to the last stable budget the same day.

```
Week 1: $50/day → Week 2: $65 → Week 3: $85 → Week 4: $110   (≈ +30% steps, each gated on CPA)
```

## Multi-Country Expansion

Order: US → UK/CA/AU (same language, cheaper testing) → DE/FR (high value, localization required) → JP/KR (high LTV, unique query culture) → BR/MX/IN (volume play, low CPT).

Per new country: translated listing, localized screenshots, **keywords researched natively — never translated**: Japanese and Korean queries are not translations of English ones, and translated keyword lists are the top cause of dead international campaigns. Separate campaign, local-currency budget.

| Country | Notes |
|---------|-------|
| US | Highest competition and CPT, most volume — benchmark market |
| UK | US-like, smaller; good second test |
| DE | High LTV, privacy-conscious, localization mandatory |
| JP | Very high LTV for games; keyword culture unlike English |
| BR | High volume, low CPT, Portuguese required |

## Custom Product Pages

App Store Connect allows up to 35 CPPs per app; ads attach them at ad-group level. Build CPPs per keyword theme (sleep-keyword ad group → sleep-focused page), per intent (problem vs aspiration), and seasonally.

A/B pattern: two ad groups, identical keywords and bids, default page vs CPP, 2 weeks minimum, decide on CVR. At low tap counts small CVR gaps are noise — extend the test rather than crown a winner.

## Advanced Tactics

- **Dayparting:** run all hours 2 weeks, analyze **by tap timestamps** (install-based hourly analysis is corrupted by SKAN delays — SKILL.md Traps), cut worst hours via the `daypart` targeting dimension.
- **Exclude existing users:** `targetingDimensions.appDownloaders.excluded: [YOUR_ADAM_ID]` — the one audience refinement that is nearly always right; the rest shrink reach (SKILL.md Traps).
- **Cross-promote a portfolio:** `appDownloaders.included: [YOUR_OTHER_APP_ADAM_ID]` in a dedicated campaign — the warmest audience ASA can address. Like every audience refinement it only reaches users with Personalized Ads on (SKILL.md Traps); here the trade is deliberate: small reach, highest intent, so run it as its own campaign with its own budget, never as a refinement on a core campaign.
- **Seasonal pushes:** raise brand bids and budgets ahead of your category's peak (fitness in January, shopping in Q4) — auctions get more expensive exactly when CVR also rises; judge the season on cohort ROAS (`measurement.md`), not on in-season CPA alone.

## Reporting & Analysis

| Report | Frequency | Purpose |
|--------|-----------|---------|
| Campaign performance | Daily | Spend/CPA monitoring, spend gate |
| Search terms | Weekly | Graduate and negate |
| Ad group / keyword | Weekly | Bid adjustments |
| Impression share | Monthly | Competitive pressure (read as ranges) |
| Geo performance | Monthly | Country decisions |

Attribution: ASA counts a 30-day tap-through window by default; re-downloads are reported separately (`redownloads`) — a "cheap CPA" built on re-downloads of an existing user base is not acquisition. Search term reports withhold low-volume terms for privacy: a slice of spend will never map to a visible term; treat it as the cost of discovery, not a bug.
