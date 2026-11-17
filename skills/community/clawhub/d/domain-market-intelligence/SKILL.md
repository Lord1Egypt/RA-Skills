---
name: domain-market-beat
description: Produce a time-bounded domain-market news briefing with source tiers, event types, and explicit inference limits, covering notable sales, registration trends, and recent domain movements. Use when a user wants to know what is happening in the domain market now. This is a briefing, not investment advice.
---

# Domain Market Briefing

**What this does:** produces a domain-market news briefing anchored to an explicit time window, with sourced headlines, a sales table that distinguishes sale types, registration-trend figures, recent domain movements, and a clear split between confirmed causes, plausible context, and unknowns.

**Data interfaces it needs.** DomainKits MCP supplies part of the structured evidence through the tools below; host-provided web search and WebFetch supply current news, original announcements, and sale verification. Equivalent providers are acceptable. Never assume a field is present when the actual payload omits it; mark it `Not Provided` or the capability `Unavailable` and continue. Query sources fresh on every run; do not rely on model memory for current events.

- Keyword registration trends (hot and emerging), DomainKits: `keywords_trends`
- Recent premium-domain changes, DomainKits: `domain_changes`
- Registration status and WHOIS, for validating movements, DomainKits: `whois`
- DNS resolution / nameserver validation, DomainKits: `dns`
- Web access for sales, news, and market events

Optional follow-up capabilities (used only when the user chooses to go deeper, not required for the briefing): `nrds`, `aged`, `deleted`, `expired`.

## Time scope

- Follow the user's requested window when given.
- Otherwise default to the last 7 days, with recent movements broken out separately. Default recent movements to the last 24 hours when the tool supports that window; otherwise state the exact coverage the tool returns and do not imply it covers the full briefing window.
- Build all search queries from the actual current date and the requested window. Never hard-code a calendar year.
- Header every briefing with the cutoff time, the timezone, and the time the queries were run.
- Distinguish the event date (when the sale, transfer, or change happened) from the article publication date. Do not present an old sale re-published this week as a new sale.

## Evidence discipline

- **Source tier and verification status are two separate fields.** Source tier measures how authoritative the source is; verification status measures the state of the event (completed / reported / pending / unverified). A high-tier source does not by itself make a sale a verified completed sale, an official marketplace announcement may still describe a pending or reported transaction, not a finalized, paid-and-transferred one. Record both fields independently.
- **Classify every sale by type.** Distinguish verified completed sale, publicly reported sale, auction result, current bid, asking / listing price, and unverified claim. Never report a listing price or a current auction bid as a completed sale.
- **Independent sources only.** The same story republished across several sites is one source, not several. Count independent reporting, not copies.
- **Source tiers** (lead conclusions with higher tiers):
  1. Official announcements from a registry, ICANN, a company, or a marketplace, including a company's or marketplace's verified official social account.
  2. Verifiable sales databases and reliable industry press.
  3. Other news reporting.
  4. Anonymous, unofficial, or otherwise unverifiable sources (including unverified social posts and forum tips) go in a separate Unverified section and do not feed the main conclusions by default. An official verified account is Tier 1, not Tier 4, even though it posts on social media.
- **Disclosure bias.** Public sales data is heavily disclosure-biased: undisclosed sales are not in the sample, so a public leaderboard does not represent the whole market. State this.
- **Cause discipline.** For any spike, separate Confirmed cause (an official source explicitly links it), Plausible context (correlated in time but causation unproven), and Unknown (no reliable explanation). Do not read related news as the cause by default.
- **Low-base caution.** A move from 2 to 10 is +400% but may not be a meaningful trend. Always show absolute numbers alongside percentages.
- **Registration signals are not end-user demand.** Trend counts and cross-TLD registration breadth can reflect speculation, promotions, bulk registration, or defensive registration; do not equate them with end-user demand.

## Movement discipline

Registration and DNS changes are weaker evidence than they look. Do not over-infer:

- A registrar transfer is not a sale or a change of ownership.
- A nameserver change is not a site launch or a sale.
- A passed expiry date is not imminent deletion.
- Redemption, auction, and pending-delete are distinct stages; name the stage.

Validate by the right source: registrar, expiry, and lifecycle status with `whois`; nameserver and DNS state with `dns`. Ownership change usually cannot be confirmed from either one alone. If the validating capability is unavailable, report only the observed technical change, not an inferred transaction or deletion.

## Workflow

1. **Set scope.** Establish the window (default last 7 days) and stamp the cutoff time, timezone, and run time. Build queries from the current date.

2. **Gather, fresh, from multiple sources.**
   - Web search for notable sales, industry news, and market events within the window.
   - `keywords_trends` (hot) for high-volume keywords and weekly movement.
   - `keywords_trends` (emerging) for recent spikes.
   - `domain_changes` for recent premium-domain transfers, expirations, and nameserver changes.

3. **Analyze with figures, not adjectives.**
   - For trend keywords, report current value, prior value, absolute change, percentage change, the baseline window, the sample size, and any rating the tool provides. Report each field only when the source provides it; otherwise mark it Not Provided, and never estimate or reconstruct a missing sample size or rating. When the current or prior value is zero, write the percentage change as Not Meaningful rather than an infinite or undefined percentage. If the tool gives no significance measure, do not call a move "significant"; call it the "largest observed change".
   - For each spike, assign Confirmed cause / Plausible context / Unknown, and watch for low-base effects.
   - For sales, classify each by sale type, and record source tier and verification status as two separate fields plus event and publication dates. Keep current bids and listing prices out of the sales set; route them to the active market offers table.
   - For movements, name the lifecycle stage and validate by the right source: registrar, expiry, and lifecycle status with `whois`; nameserver and DNS state with `dns`. When a movement from `domain_changes` is a nameserver change, confirm the current NS / DNS state with `dns` rather than inferring a launch or sale. If the validating source is unavailable, report only the observed change.

4. **Present** using the output structure below, leading with facts and higher-tier sources.

## Output structure

1. **Scope, cutoff time and timezone**: the window, the cutoff, the timezone, and when queries ran.
2. **Top headlines by source tier**: highest-tier, in-window items, each labeled with its verification status; a high source tier does not by itself mean the event is a verified completed one.
3. **Notable sales table**: completed and reported sale events only; see columns below.
4. **Active market offers table**: current bids, asking / listing prices, and open auctions; see columns below. These are offers, not sales, and never appear in the sales table.
5. **Registration trend table**: current, prior, absolute change, percentage change, baseline window, sample size, tool rating.
6. **Recent domain movements**: transfers, expirations, nameserver changes, each with its lifecycle stage and validation.
7. **Confirmed causes / plausible context / unknowns**: the split for each notable trend or spike.
8. **Data gaps and coverage limitations**: Unavailable sources, disclosure bias, unverified items held aside.
9. **Sources with event and publication dates**: per item, with source tier.
10. **Market-intelligence disclaimer**: "This is a market-intelligence briefing for reference only, not investment advice. Public sales data is disclosure-biased and does not represent the whole market; figures reflect only what was verifiable at the cutoff time."

Notable sales table columns (completed and reported sale events only): Domain, Sale type (verified completed sale / publicly reported sale / finalized auction result), Price and currency, Venue, Event date, Publication date, Source, Source tier (1-4), Verification status (completed / reported / pending). Source tier and verification status are two separate columns: tier measures how authoritative the source is, verification status measures the state of the event; a Tier 1 source can still carry a reported or pending event. Current bids and listing prices do not belong in this table.

Active market offers table columns: Domain, Offer type (current auction bid / asking or listing price / minimum offer / lease-to-own), Price and currency, Venue, Observation date, Source, Source tier (1-4). An offer is not a transaction; never promote a row here into the sales table without completed-sale evidence.

## Next steps

Let the user choose whether to go deeper. Optional follow-ups: for an emerging keyword, use `nrds` to inspect aggregate registration patterns, `deleted` for dropped candidates that still require availability verification, and `expired` for expiring / backorder inventory. After a notable sale, use `nrds` to look for a registration wave, and `aged` only to inspect related for-sale inventory (a rise in for-sale listings is not proof a sale triggered a registration wave). For a notable expiration, track its status with the monitoring tool. Do not attempt to bypass WHOIS privacy or identify private registrants.

## Key principles

- Anchor every briefing to an explicit window with cutoff time and timezone; build queries from the current date and query fresh, never from memory.
- Classify every sale by type; never report a listing or current bid as a completed sale. Current bids and listing prices go in the separate active market offers table, not the sales table. Republished copies are one source.
- Source tier and verification status are two separate fields, and headlines are ranked by tier, not marked "verified": a Tier 1 source can still carry a reported or pending event.
- Lead with higher-tier sources; forums and social media stay in a separate Unverified section.
- Report trend changes as figures (absolute and percentage, with baseline and sample size); avoid "significant" unless the tool measures it.
- Separate Confirmed cause, Plausible context, and Unknown; watch low-base effects; registration signals are not end-user demand.
- Do not over-infer movements: a transfer, a nameserver change, or a passed expiry is not a sale or a deletion. Validate registration status with `whois` and DNS state with `dns`, or report only the observed change.
- Define why a domain is notable (short, common word, public sale history, known attention, clear status change); do not call it high-value without valuation evidence.
