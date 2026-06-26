# Web Grounding

Read this file when the current unknown is better answered by external evidence than by another graph move.

Search is a peer tool inside the loop, but not the dominant one. Graph structure stays primary. If web evidence suggests a more intuitive narrative than the graph result, do NOT overwrite the graph answer — state the L2 graph finding first, then label the web evidence as explanation, validation, or unresolved tension. Web narratives are L0; graph observations are L2. L2 takes precedence in the verdict.

## Source Hierarchy

Treat search results by trust tier, not by rank order:

- **Tier A: primary / authoritative**
  official docs, official blogs or announcements, foundation or company sites, product docs, GitHub repos or release notes, investor relations, regulator filings, government data, standards bodies, first-party research
- **Tier B: credible secondary**
  established reporting or analysis that cites named sources and can be checked against Tier A material
- **Tier C: low-trust secondary / aggregation**
  AI-written market roundups, finance/news aggregators, exchange blogs, SEO summaries, anonymous reposts, social chatter, affiliate content

Rules:

- Use **Tier A** as the factual anchor whenever the claim is time-sensitive and an original source should exist.
- Use **Tier B** to discover, contextualize, or cross-check. Do not let Tier B alone establish a completed fact when Tier A should be obtainable.
- Use **Tier C** only as a lead generator or user-perspective signal. Never use Tier C alone to support a decision-grade factual claim.

If a claim is about "latest", "recent", "today", "launched", "integrated", "supported", "approved", "partnered", "priced", or "available", and you only found Tier B/C coverage, the answer must explicitly say the claim was **not verified in a primary source**.

## When To Use Web Next

Use web as the next move when:

- the graph already suggests a mechanism, but you need current evidence
- the question is about `latest`, `recently`, or `why now`
- a bridge candidate needs validation
- a company, sector, or asset needs current-state grounding

ClawHub / OpenClaw rule:

- before relying on web grounding, confirm that a web search tool is mounted in the current environment
- if no web search tool is available, tell the user they need to install one before you can do web-grounded validation
- do not pretend that web evidence was checked when the tool is missing

Default bias:

- if you have not yet done at least one or two meaningful graph moves on the active mechanism, go back to graph first
- if you already have a plausible mechanism and the missing piece is dated evidence, use web now

## Unstable Premise Gate

For event-driven opportunity reads, the first unknown may be whether the premise is true at all.

Examples:

- a leak or rumor about a private model
- a product launch claim
- a partnership, shutdown, or acquisition claim
- a corporate reorg presented as breaking news

If the opportunity thesis depends on one of these freshness-sensitive claims, do one minimal premise-verification search before normal graph expansion:

1. Try a Tier A source first when one should exist.
2. If no Tier A source exists yet, look for a clearly sourced Tier B report.
3. If the premise still is not anchored, do not treat it as established fact.
4. Rewrite the task as conditional analysis: `if this premise is true, what opportunity set follows?`
5. Split verifiable subclaims from inferred motive/strategy claims. Keep the latter labeled as inference even when the factual subclaims are anchored.

After that premise check, return to the normal Abel loop.

## Search Order

For unstable factual claims, search in this order:

1. official domain or documentation
2. official repo, release notes, governance repo, or changelog
3. regulator / investor-relations / earnings / standards source
4. credible secondary coverage
5. user-perspective material

Do not stop at step 4 if the claim still needs a step 1-3 confirmation.

## What To Search

Search one grounded subject at a time:

- a key company from `node_description`
- a sector or industry from `node_description`
- a graph-backed mechanism edge
- a repeated bridge candidate that needs validation

## Pre-Search Frame

Before each search, be able to name:

- `edge or mechanism`
- `why it matters`
- `current-state question`

If you cannot name those, return to the graph first.

## Query Shape

Use company names, products, industries, or mechanisms.

Good (financial):

- `Spotify podcast advertising monetization latest`
- `New York Times digital subscription growth latest`
- `startup software funding hiring 2026`
- `Ethereum ETF flows latest`

Good (life decisions):

- `AI designer job market automation risk 2026`
- `MBA salary premium vs opportunity cost latest data`
- `luxury goods pricing cycle EUR CNY exchange rate trend`
- `GPU 5090 vs 9090 XT release date pricing comparison`
- `cooking vs eating out cost health time tradeoff`
- `San Francisco vs Shanghai housing price forecast 2026`

Bad:

- `Spotify stock price`
- `Ethereum price`
- `graph.neighbors news`
- `should I change jobs` (too vague — search the specific mechanism, not the question)

## What To Extract

After each useful result, keep only:

- `graph_fact`
- `searched_mechanism`
- `state_now`
- `counter-evidence`
- `inference`
- `source_tier`
- `verification_status`

## Search Budget (CurioCat-inspired adversarial protocol)

Minimum 4 searches, structured as:
1. **What's happening now** — latest prices, policy changes, dates, events
2. **Supporting evidence** — data that confirms the graph-backed verdict
3. **Contradicting evidence** — actively search for reasons the verdict is WRONG. "Why buying now might be better" if verdict says wait. This is mandatory.
4. **User-perspective data** — what a real buyer/decision-maker would search. Second-hand prices, waitlists, alternative channels, community consensus, real people's experiences.

Up to 6 searches for complex questions. Stop when contradicting search returns nothing new.

For time-sensitive factual claims, at least one of the first three searches should explicitly target a **Tier A** source. If that search fails, say so in the write-up instead of silently filling the gap with lower-tier summaries.

## Stop Rules

- stop when contradicting evidence search returns nothing the verdict hasn't already addressed
- stop when search only repeats generic sector commentary
- stop only after you know whether the claim has or does not have a primary-source anchor

## Return-To-Graph Rules

Go back to the graph when search:

- reveals a new clean node candidate
- reveals a second-order effect worth testing structurally
- contradicts the current causal story

Then return to the orchestration loop and decide the next move explicitly.

## Writing Rules After Search

- Write completed-fact language (`is`, `has`, `supports`, `launched`) only when the evidence anchor is Tier A or a Tier B report that clearly quotes or links the primary source.
- If the best evidence is Tier B only, write `reported`, `according to`, or `appears`.
- If the best evidence is Tier C only, do not present the claim as established. Either verify independently or say the claim remains unconfirmed.
- When sources conflict, name the exact dates and lead with the higher-tier source.
