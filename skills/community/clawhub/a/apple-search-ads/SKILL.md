---
name: Apple Search Ads
slug: apple-search-ads
version: 1.0.3
description: >-
  Plans, launches, and optimizes Apple Search Ads (Apple Ads, ASA) campaigns for iOS apps: bids,
  keywords, budgets, CPA, attribution. Use for paid iOS user acquisition and App Store ads —
  launching or restructuring campaigns, mining search-term reports, graduating keywords,
  defending brand terms, scaling spend, expanding to new countries, testing Custom Product
  Pages, wiring AdServices or SKAdNetwork attribution, automating reports and changes via the
  Campaign Management API, or diagnosing why CPA spiked, keywords get no impressions, a
  campaign stops spending its budget, ads got rejected, or ASA, SKAN, and MMP install counts
  disagree. Not for App Store listing optimization itself (ASO).
homepage: https://clawic.com/skills/apple-search-ads
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🍎
    configPaths:
    - ~/Clawic/data/apple-search-ads/
    requires:
      bins:
      - curl
      - jq
      env:
      - ASA_CLIENT_ID
      - ASA_TEAM_ID
      - ASA_KEY_ID
      - ASA_ORG_ID
      - ASA_PRIVATE_KEY_FILE
    os:
    - linux
    - darwin
    displayName: Apple Search Ads
---

Toolkit for Apple Search Ads (rebranded "Apple Ads" in 2024; API paths still read `searchads`): Campaign Management API v5, attribution (AdServices + SKAdNetwork), bid math, diagnosis, and scaling strategy. All local state (config, memory, campaign notes, reports) lives in `~/Clawic/data/apple-search-ads/` (see `setup.md` on first use, `memory-template.md` for file formats). If you have data at an old location (`~/apple-search-ads/` or `~/clawic/apple-search-ads/`), move it to `~/Clawic/data/apple-search-ads/`. Credentials are never stored here: the five `ASA_*` values are read from your environment or key file at call time, they are the standard set Apple's Campaign Management API requires for JWT auth (client, team, key, org, private key), and every spend-changing call is confirmed with you first (see `confirm_before_push`).

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/apple-search-ads/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| currency | string (ISO code) | USD | Currency for every bid, budget, and CPA example; passed in all API money objects |
| report_timezone | UTC \| ORTZ | UTC | Passed as `timeZone` in every report request — one value everywhere, never mixed (Traps) |
| ltv_divisor | number (3-5) | 4 | Target CPA = LTV / `ltv_divisor`; 3 = aggressive payback, 5 = conservative (`strategy.md`) |
| mmp | none \| appsflyer \| adjust \| singular \| kochava \| branch | none | With an MMP set, it owns AdServices and SKAN integration and cross-channel truth (`ios-integration.md`, `measurement.md`) |
| confirm_before_push | bool | true | Every API mutation (bids, budgets, status, keywords) is listed and confirmed before pushing; false = push and log without asking. Setting it to false means real ad spend changes without a prompt: only do it for campaigns you own and can afford to have moved unattended; campaign DELETE stays confirmed either way |
| naming_pattern | text | App - Country - Intent | Template for every campaign name in create payloads, scripts, and memory logs; parsing reports assumes this pattern |

Preference areas to record as the user reveals them:

- **tooling** — dashboard vs API/scripts, report automation cadence; decides whether plays are given as UI steps or curl commands
- **conventions** — ad group naming, experiment tagging, negative-list hygiene; shapes create payloads and memory logs
- **markets** — home market, expansion order, localization resources; shapes Multi-Country guidance in `strategy.md`
- **risk posture** — payback aggressiveness, scaling speed within the 20-30% step band, how proactively to flag overspend
- **reporting** — source of truth per KPI, deliverable format and cadence; shapes `measurement.md` reconciliation and report outputs

## When To Use

- Launching or restructuring campaigns for an iOS app
- Optimizing bids, budgets, keywords, or CPA on running campaigns
- Diagnosing problems: no impressions, budget not spending, CPA spikes, rejected ads, API errors, mismatched install counts
- Wiring attribution (AdServices, SKAdNetwork, MMP) into the app and deciding which numbers to trust
- Automating reports and weekly optimization via the API
- Deciding scaling, multi-country expansion, or Custom Product Page tests
- Mode: acts directly via the API when the user grants credentials; otherwise advises on structure and strategy. Not for App Store metadata/screenshot work itself — route to `aso`; this skill only flags when CVR points there.

## Quick Reference

Route by what you need to do. Read one file; each is self-contained.

| Situation | Go to |
|-----------|-------|
| First run, `~/Clawic/data/apple-search-ads/` missing, loading preferences | `setup.md` |
| Saving apps, targets, campaign structure, learnings to memory | `memory-template.md` |
| Authenticating, base URL/headers, endpoints, payloads, campaign/ad group/keyword objects, report requests, metrics, error codes, rate limits | `api-reference.md` |
| No impressions, spend with no installs, budget not spending, CPA suddenly spiked, campaign ON_HOLD or rejected, API 401/403/429 | `troubleshooting.md` |
| Adding attribution in the iOS app (AdServices, SKAdNetwork conversion values, MMP integration, testing) | `ios-integration.md` |
| Choosing a source of truth, reconciling ASA vs SKAN vs MMP counts, estimating LTV, brand-spend incrementality, cohort ROAS | `measurement.md` |
| Planning structure, placements, match types, keyword tiers, bidding, benchmarks, budget allocation, scaling, multi-country, Custom Product Pages | `strategy.md` |
| Running curl/jq automation (get token, daily/search-term/keyword reports, add keywords/negatives, weekly optimization) | `scripts.md` |
| Anything else | Apply Core Rules below, then route to the closest file |

## Core Rules

### 1. Bid Backwards From LTV, Never From Competitors' Bids
Max CPT = target CPA × expected CVR. Target CPA $6 and CVR 50% → max CPT $3.00. A bid above your max CPT needs an explicit reason (brand defense); a bid copied from "what the niche pays" has none. CPA math lives in `strategy.md`; LTV estimation in `measurement.md`.

### 2. Structure Is the Strategy: One Intent Per Campaign
Brand, category, competitor, discovery — separate campaigns. ASA has no portfolio bid strategies or shared budgets; campaign separation is the only budget and reporting control you get, so mixing intents removes your only lever.

### 3. "Exact Match" Is Not Exact
ASA exact match also serves plurals and common misspellings (Apple-documented). Before concluding a keyword works or fails, open the search term report and see which queries actually spent the money.

### 4. Graduate and Negate
Weekly: any search term with ≥2 installs and CPA ≤ target → add as exact match in its intent campaign AND as a negative where it was discovered. Skip the negative and the discovery campaign keeps buying the term, splitting its data forever.

### 5. Defend Your Brand
Competitors WILL bid your name, and your relevance advantage makes brand defense the cheapest CPA in the account. Impression share is reported as a range, not a point; if the high bound on brand terms sits below ~90%, raise brand bids. Whether brand spend is incremental at all is testable — holdout protocol in `measurement.md`.

### 6. One Country Per Campaign
CPT, CVR, and query language differ per market; blended reporting makes every bid decision wrong somewhere. Separate campaigns per country/region.

### 7. Spend Gates Before Scale
Keyword spend ≥ 2× target CPA with 0 installs → cut the bid sharply (30-50%) or pause. Example: target CPA $6 → any keyword that burned $12 with no install acts today, not at month end.

### 8. Bid Your True Max — the Auction Is Second-Price
Apple has described the auction as second-price: you pay just above the next-highest bid. Shading below your max CPT mostly loses auctions; it rarely saves money. Cap risk with the spend gate (Rule 7), not with timid bids.

## Output Gates

Before pushing any change through the API:

- Is the new bid computed from max CPT (Rule 1), not from current bid ± gut feel?
- One variable per keyword/ad group per cycle (bid OR creative OR match type)?
- Is the decision backed by the minimum window in `strategy.md` (7 days; 14 for competitor campaigns), and does that window end ≥2 days back (recent rows still backfill — `measurement.md`)?
- Budget increase within the 20-30% step limit (`strategy.md` → Scaling)?
- If `confirm_before_push` is true (default), was the change list shown and confirmed?
- Change and expected effect logged to `~/Clawic/data/apple-search-ads/memory.md`?

## Architecture

Memory lives in `~/Clawic/data/apple-search-ads/`. See `memory-template.md` for structure.

```
~/Clawic/data/apple-search-ads/
├── config.yaml        # Declared variables (Configuration table above)
├── memory.md          # Active campaigns, preferences, learnings
├── credentials.md     # OAuth config (NEVER commit real secrets)
├── campaigns/         # Campaign-specific notes and performance
│   └── {app-id}/
├── reports/           # Generated reports
└── scripts/           # Custom automation
```

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Treating `cpaGoal` as a spend cap | It is advisory; Apple can spend far past it | Control CPA with bids and the spend gate (Rule 7) |
| Refining age/gender to "focus" targeting | Excludes every user with Personalized Ads off — a large, invisible slice | Stay broad; segment by keyword intent instead |
| Search Match ON in every ad group | Your own ad groups compete for the same queries; data fragments | Search Match only in the discovery campaign |
| Same bid across all keywords | Brand, category, and long-tail have different values | Tier bids off max CPT (`strategy.md`) |
| Judging dayparting by install timestamps | SKAN postbacks arrive hours to days late | Daypart on tap timestamps |
| Comparing ASA dashboard installs to MMP installs | Different attribution windows and models; they never match | Pick one source of truth per KPI (`measurement.md`); record it in memory.md |
| Reading today's report rows as final | Installs attribute retroactively to their tap date across the 30-day window | Judge windows that end ≥2 days back; treat newer rows as provisional |
| Launching on a weak product page | You pay per tap; low CVR taxes every dollar | Fix ASO first, then buy traffic |
| Mixing timezones across reports | ASA reports accept UTC or ORTZ; mixing misaligns days | Set `report_timezone` once and pass it in every request |
| No cross-campaign negatives | Category/discovery campaigns quietly buy your brand queries at brand-level CPTs | Add brand terms as negatives in every non-brand campaign |
| Scaling budget in big jumps | Volume spikes re-enter auctions at worse positions; CPA jumps | 20-30% per step (`strategy.md` → Scaling) |

## Where Experts Disagree

- **Brand bidding incrementality.** One school: most brand taps would have installed organically, so brand spend is a tax. Other: once a competitor bids your name, defense is mandatory. The boundary is empirical: competitor present on your brand terms → defend (Rule 5); nobody bidding them and you rank #1 organically → run the holdout test (`measurement.md`) before committing budget.
- **cpaGoal: set or never set.** Some set it as a pacing signal to Apple; others leave it empty to keep behavior predictable. Either is defensible because it is advisory — the indefensible position is treating it as a cap (Traps).
- **Always-on discovery vs mining sprints.** Always-on ~10% budget suits new apps and new markets where the term pool is unexplored; once weekly search-term reports stop surfacing new graduates, switch to periodic sprints and return the budget to proven campaigns.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://appleid.apple.com/auth/oauth2/token` | Client credentials (JWT) | Get access token |
| `https://api.searchads.apple.com/api/v5/*` | Campaign/keyword data | Campaign management |
| `https://api-adservices.apple.com/api/v1/` | Attribution token | Attribution data |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Campaign configurations sent to Apple Ads API
- Attribution tokens sent to Apple (from iOS app)

**Data that stays local:**
- Credentials in `~/Clawic/data/apple-search-ads/credentials.md`
- Reports and analysis
- Strategy notes

**This skill does NOT:**
- Store API secrets in plain text (use environment variables)
- Access user-level data (attribution is aggregated)
- Make requests to undeclared endpoints

**Guardrails:**
- API mutations are gated by `confirm_before_push` (default true); campaign DELETE is always confirmed regardless of the setting
- Secrets travel only via environment variables named in the frontmatter; never written to config, memory, or reports

## Trust

By using this skill, data is sent to Apple's Search Ads API and AdServices.
Only install if you trust Apple with your advertising data.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/apple-search-ads (install if the user confirms):
- `app-store-connect` — manage apps and releases
- `aso` — App Store Optimization
- `analytics` — track metrics and KPIs
- `ios` — iOS development patterns

## Feedback

- If useful, star it: https://clawic.com/skills/apple-search-ads
- Latest version: https://clawic.com/skills/apple-search-ads

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/apple-search-ads.
