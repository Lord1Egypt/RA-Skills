---
name: fantasy-sports-research
description: Compare public daily-fantasy contest formats, rules, slates, and source-published player projections from DraftKings and FanDuel. Use for fantasy-sports research, not lineup or wager recommendations.
---

# Fantasy sports research

Produce a source-attributed overview of contest formats or projection inputs
from DraftKings DFS/Pick6 and FanDuel Research. Use scripts/crawlora.sh or the
named Crawlora tools; read the generated endpoint reference for exact fields.

## Discover the relevant product and slate

- Start with DraftKings sport, rules, or Pick6 directories for product and
  format questions. The featured NFL Best Ball endpoint returns the cards on
  that landing page, not the complete contest lobby or a guarantee that an
  entry is currently available.
- For FanDuel projections, read the projection tables first to discover valid
  type, position, and scope values. For DAILY projections, retrieve the
  matching sport/date slate and pass its exact slate_id to the projections
  request. IDs and format codes are source-specific.
- Preserve sport, slate/date/week, projection type, position, scope, and
  retrieval time. Do not compare projections from different slates or scoring
  systems as if they were the same measurement.

## Interpret contest and projection evidence

- Label projections as provider estimates, not actual results, guarantees, or
  independent forecasts. Keep salary, projected points, and value fields in
  their source units; do not turn them into an expected return or winning
  probability.
- DraftKings public guides, rules, and scoring pages describe product formats.
  They do not establish a user's location eligibility, contest access, or
  account status. The Pick6 sports directory is a dated help-center snapshot;
  keep its restriction note attached to that source.
- Use displayed fees, prizes, and entry limits only when the selected public
  contest card supplies them. Do not infer the full lobby or contest capacity
  from a featured list.
- Do not produce lineups, tell a user which player to select, or recommend an
  entry fee. Explain the source's contest rules and projection fields instead.

## Deliverable

Return a concise format matrix or slate table with source date, sport, contest
type, selection scope, and important unavailable fields. Separate official
rules from provider projections and label estimates plainly.

~~~sh
scripts/crawlora.sh /draftkings/dfs/sports
scripts/crawlora.sh /draftkings/dfs/rules-and-scoring
scripts/crawlora.sh /draftkings/pick6/rules
scripts/crawlora.sh /fanduel/research/projection-tables sport=nfl
scripts/crawlora.sh /fanduel/research/projection-slates sport=nfl
# Use a slate_id returned by projection-slates:
# scripts/crawlora.sh /fanduel/research/projections sport=nfl type=DAILY slate_id=SLATE_ID_FROM_RESPONSE
~~~
