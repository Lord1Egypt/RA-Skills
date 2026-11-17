# Sources — Building and Vetting the List

The digest is only as good as its inputs. Sourcing failures are silent: a dead feed or a lazy source list narrows coverage without ever throwing an error.

## Cold-Start Seeding (new topic or entity)

Seed every new topic with a deliberate layer mix, not whatever search returns first:

| Layer | What it is | Seed count |
|---|---|---|
| Primary | Company blogs, changelogs, filings, regulators, standards bodies, papers | 2-3 |
| Reporting | Beat journalists and trade press that break or verify, not rewrite | 2-3 |
| Discovery | Aggregators, link communities, social | 1-2 |

Discovery finds stories; primary and reporting confirm and cite them. A list that is all discovery produces a digest of other people's front pages.

## Per-Entity Source Kits

- **Company**: their blog + changelog + status page + careers page + filings (if public) + the beat reporter who covers them. The careers page often signals strategy before the blog does (`competitors.md`).
- **Person**: their own feed/blog/talks — track statements and moves by them, not coverage about them (`dimensions.md` → Content).
- **Topic/industry**: 1-2 trade publications + the relevant regulator or standards body + one research firehose (preprints, court dockets, tender boards — whichever the domain has).

## Vetting a Candidate Source

Run these checks before a source earns a slot; any two failures = discovery-only, never citation:

- **Original-information test**: does it break, verify, or add analysis — or only rewrite? Compare its version of one story against the outlet it links; identical structure and quotes = same press release, zero independent value.
- **Author and dateline**: named author, real publication date, corrections policy. Their absence is the leading signal of scraped or generated content, along with mirror-domain names and stock imagery around thin text.
- **Track record on their beat**: one retracted or silently-edited story you catch outranks any masthead prestige.

## Source Rot

- A feed silent beyond its normal cadence: check whether it moved (redesigns break feed URLs) before dropping it. A silently dead trusted source is the most common cause of "you keep missing X" complaints.
- Review the list when coverage complaints arrive, not on a timer — the complaint names the hole.

## Diversity Check

If more than about a third of a week's shipped items trace to one outlet, the digest has become that outlet's editorial line. Either diversify the layer that outlet dominates or tell the user explicitly ("most of this week's coverage came via X").

## Aggregators

- Aggregator timestamps are ingestion times, not publication times. Always carry the original dateline; an old story resurfacing on an aggregator is not news (SKILL.md Traps).
- Follow the aggregator's link to the origin and cite the origin. The aggregator never appears as the source line.

## Paywalls and Partial Access

- Never reproduce paywalled full text. If only headline and standfirst are accessible, the item ships marked thin: "(headline only — paywalled)".
- A paywalled scoop corroborated nowhere else is still a single source: `single_source_policy` applies.

## User-Declared Sources

- **Trusted** sources (declared, in `preferences.md`): their items skip the corroboration hold — the user has delegated that judgment.
- **Blocked** sources: never cited AND never counted as corroboration. Blocked means the user distrusts their facts, not just their prose.
- If the user reads a major outlet daily, its front page is `saturated`: skip what they will have seen; ship second-order analysis of it instead (`dimensions.md` → Content).
