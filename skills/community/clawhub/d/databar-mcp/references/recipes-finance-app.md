# Databar Recipes — Finance, Apps & Web Traffic

Concrete recipes for investor intelligence, app-market analysis, and domain/traffic teardowns. Enrichment IDs and prices were **verified August 2026** — always re-verify with `search_enrichments` before running; the catalog changes and prices shift.

## Recipe F1 — Private company funding intel

Goal: how much a company raised, from whom, and when.

1. `search_enrichments(query="funding raised investors")` → Owler amount-raised + investors per round (#527, 4 cr), Leadmagic funding data (#1265, 4 cr), Crustdata fundraising history (#913, 8 cr), PredictLeads financing events (#679, 7 cr — amounts/dates but no investor names).
2. Combine with news (Recipe M6) — funding events time your outreach and your market map.
3. Investor lists from #527/#1265 double as LP-style research: who invests in this space repeatedly.

## Recipe F2 — Public company teardown

Goal: everything on a listed company, cheaply.

1. Financial Modeling Prep family, all priced like snacks: real-time stock data (#4, **0.05 cr**), earnings call transcripts (#80, 1 cr), income statement (#18, 1 cr), institutional ownership (#1128, 1 cr), press releases (#1126) and stock news (#1119, 1 cr each), all-in-one overview (#1124, 4 cr).
2. Earnings transcripts are the sleeper: management's own words on strategy and pain, per quarter — gold for sales pitches, research, and content.
3. Full quarterly teardown (stock + transcript + income + news) ≈ 3 credits.

## Recipe A1 — App-market intelligence

Goal: size competitors' apps before you build or pitch.

1. Apple App Store: app data by id (#1512, 2 cr — reviews, ratings, owner site), historic **revenue estimates** (#604, 1.5 cr).
2. Google Play: app reviews (#606, 2 cr).
3. Stack: revenue trend + rating trend + review themes = a defensible read on whether a niche is underserved. Combine with Recipe M4 (review mining) for the complaint clusters.

## Recipe W1 — Domain & traffic teardown

Goal: is this site/company real, growing, and how do they get traffic?

1. Free first: Tranco global rank (#139, **0 credits**) — instant size read on any domain.
2. SpyFu visits + SEO statistics (#59, 1 cr — clicks, visits, organic/paid ranks, ad budget), Crustdata historic traffic + growth (#909, 5 cr), Forager traffic + tech stack combined (#1342, 5 cr).
3. Builtwith redirects (#408, 6 cr) for M&A/rebrand archaeology — where a domain has pointed over time.
4. CompanyEnrich firmographics by domain (#1707, 1 cr — industry, size, revenue, tech, funding, socials) is one of the cheapest full-company lookups in the catalog.

## Cross-cutting rules

- Price the full chain before running (see Cost discipline in SKILL.md).
- Bulk results are position-aligned — keep input order.
- Nothing is deleted without explicit instruction; `delete_*` tools are permanent.
- Financial data carries licensing limits — don't redistribute raw provider data; check provider terms.
