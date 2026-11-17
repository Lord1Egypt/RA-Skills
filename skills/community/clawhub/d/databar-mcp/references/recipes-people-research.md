# Databar Recipes — Job Search, Recruiting & Research

Concrete recipes for people-finding and research workflows. Enrichment IDs and prices were **verified August 2026** — always re-verify with `search_enrichments` before running; the catalog changes and prices shift. Waterfall identifiers (`email_getter`, etc.) are stable.

## Recipe P1 — Find the decision-maker at a target company

Goal: names, titles, LinkedIn URLs for the person who can say yes.

1. `search_enrichments(query="search people")` → price tiers run wide: Crustdata title+company search (#718, **0.4 cr**), Icypeas filtered people search (#1448, 1 cr), Pubrio (#1616, 2 cr), Explee by domain+title (#1721, 2 cr), Findymail (#668, 3.5 cr), Leadmagic (#887, 6 cr), Databar Labs (#1613, 10 cr), Sales Navigator URL export (#1662, 100 cr).
2. Default to the cheap tier first (Crustdata at 0.4 cr), verify hit quality on a small batch, and only escalate if hit rate disappoints. A 25× price gap for the same nominal capability is the norm in this catalog, not the exception.
3. Feed results into the email waterfall (`recipes.md` Recipe 1) for verified contacts.
4. Recruiting flip side: same tools find candidates by title; combine with job-postings search to find companies hiring (budget confirmed) vs. cold.

## Recipe P2 — Warm-intro path (who do I know there?)

Goal: turn a target company into a warm-intro map.

1. `search_enrichments(query="search people at company")` → run the cheap-tier search for a range of plausible titles at the target company.
2. Cross-reference the returned LinkedIn URLs against your own network's profiles.
3. `get a person's LinkedIn posts` (#1927, 2 cr) on shortlisted contacts — their recent posts are your conversation opener, and post activity signals whether they're approachable via content engagement.

## Recipe P3 — Job-search intelligence (the flip side of hiring signals)

Goal: as a job seeker or researcher, know which companies are actually growing.

1. Job postings search (`recipes.md` Recipe 3): companies posting for your role, filtered by tech in the description (TheirStack #676) or with filters (Pubrio #1615).
2. `search_enrichments(query="company profile")` → Pubrio company lookup (#1608, 4 cr): firmographics + news + job postings + web signals in one call.
3. Stack the signals: a company hiring 3+ relevant roles, with fresh funding news (Recipe M6), that runs tools you know (tech stack, `recipes.md` Recipe 4) is a high-probability target. Their job post language also names the exact pain you can speak to in an interview or pitch.
4. For direct outreach to hiring managers: Recipe P1 + email waterfall, title = the manager of the posted role.

## Recipe P4 — Deep company dossier

Goal: everything on one company before a meeting, pitch, or interview.

1. `search_enrichments(query="company data by domain")` → pick firmographics provider (Pubrio #1608, TheirStack #677, others).
2. Add tech stack (`recipes.md` Recipe 4), news (Recipe M6), LinkedIn company posts (#1928, 2 cr), brand social stats (#716, 2.5 cr).
3. Total dossier cost: roughly 10–20 credits depending on provider choices — cheap for a meeting that matters.

## Recipe P5 — Research & content sourcing

Goal: ground research or content in real data instead of vibes.

1. `search_enrichments` by topic — HN (#15, free), Reddit search (#1273, 3 cr), LinkedIn posts (#1929), X tweets (#1294) are the raw feeds.
2. Pull complaints/praise from review platforms (Recipe M4 in `recipes-marketing-social.md`).
3. Pattern-match across platforms: the same complaint on Reddit + Capterra + HN is a validated pain, not an anecdote. The same question repeated in LinkedIn comments is a content topic with proven demand.
4. Structured output: land results in a table with columns per platform, then cluster themes with your own analysis pass.

## Cross-cutting rules

- Price the full chain before running (see Cost discipline in SKILL.md).
- Bulk results are position-aligned — keep input order.
- Nothing is deleted without explicit instruction; `delete_*` tools are permanent.
- Employment data and outreach are regulated differently by jurisdiction (GDPR, state privacy laws) — verify your use is lawful for the region.
