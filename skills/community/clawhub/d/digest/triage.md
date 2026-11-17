# Triage — Filtering, Dedupe, and Ranking

Order of operations is fixed: cluster → filter → rank → budget. Ranking before clustering double-counts popular stories; budgeting before ranking cuts the wrong items.

## Cluster First

- Same-story detection matches on **entities + event**, never on headline text — outlets headline the same event in incompatible ways ("X acquires Y" / "Y sold" / "What the X-Y deal means").
- One cluster = one item. The cluster's source count N is rank input: 3+ independent sources promotes toward Highlights (SKILL.md rule 4). Independence is decided by the test in `verification.md`, not by counting URLs.
- Keep the strongest source as the citation: primary beats reporting beats aggregator (`dimensions.md` → Sources).

## Filter

- Topic match includes; exclusion match drops — binary (SKILL.md rule 3). The only exception: an excluded topic intersecting a confirmed interest ships flagged.
- **Second-order relevance counts as a match**: a supplier, acquirer, regulator, or key partner of a tracked entity is inside scope even if never named as a topic. The why-line must state the connection ("their main chip supplier — supply risk for X").
- Recency windows per content type: canonical values in `dimensions.md` → Sources. An item outside its window is dropped regardless of quality — stale analysis is worse than absent analysis.

## Rank

- Interest match first, freshness second, source weight third (SKILL.md rule 1).
- Tie-break within equal interest match: freshness, then cluster size N.
- Breaking-first ordering only as a learned or stated preference (SKILL.md → Where Experts Disagree).

## Enforce the Budget

- `item_cap` items, ≤3 Highlights (SKILL.md rule 5). Overflow compresses into Worth Noting one-liners or drops entirely — bury, don't delete: a buried item can return tomorrow as a cluster grows.
- A Highlight slot is earned by interest match, not by story size. Zero qualifying items = zero Highlights; the section may be empty, never diluted.

## Slow Day

- Send the short honest version: "quiet day in your topics, 2 items." Padding trains the user to skim, which destroys the Highlights section's authority.
- Do not widen topic scope to fill the budget — that is scope drift the user never asked for. If slow days repeat, propose a scope or cadence change instead (`learning.md`).

## Heavy Day

- A single event flooding coverage (launch day, verdict, outage): cluster the theme into **one block that counts as one item** against `item_cap` — headline for the event, then 2-4 sub-bullets for genuinely distinct developments.
- The rest of the digest still ships. A heavy day in one theme does not cancel the user's other interests.

## Repeats and Updates

- Before shipping, check every item against `~/Clawic/data/digest/sent-log.md` (SKILL.md rule 7).
- Already sent + nothing changed → drop. Already sent + development → ship as "Update:" + the delta only (`writing.md` for phrasing).
- A story that keeps developing daily earns one update line per digest, not a fresh full item each time.
