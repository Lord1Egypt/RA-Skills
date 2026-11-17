---
name: flashscore-match-analysis
description: Build a sourced Flashscore match report from covered team and player statistics, lineups, absences, momentum, box scores, point-by-point or darts feeds, and editorial coverage. Use for detailed event analysis; use multi-sport-match-research for basic fixture and score checks.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Flashscore match analysis

Produce a bounded, source-grounded account of one Flashscore event. Resolve the
exact match before loading detail, then choose only the statistics or editorial
surface that answers the user's question. Coverage varies by sport, league, and
event; a missing surface does not mean the event or statistic was absent.

## Resolve and scope the event

1. Use `/flashscore/search` to find candidate teams, competitions, or matches.
   Confirm both participants, sport, competition, date, and status. Preserve the
   eight-character match ID from the returned match URL; do not transfer IDs
   from LiveScore, SofaScore, or FotMob.
2. For a simple score or schedule check, route to
   `multi-sport-match-research`. Use this skill for detailed event data that
   needs the Flashscore-specific response and coverage rules below.
3. Preserve the requested period, whether the event is live or complete, and
   the collection time. Keep regulation, extra time, aggregate ties, and
   shootouts separate.

## Choose a covered detail surface

- **Football team statistics:** `/flashscore/match-stats` returns the provider's
  delimited team-stat feed, which may include expected goals, possession, shots,
  chances, corners, and passes. Read the returned labels and values as supplied;
  keep home/away, units, groups, and any period markers attached. The available
  fields vary by event. Empty or not-found coverage is unknown, not zero. Use this
  when the user asks for team totals or when those totals add useful context to a
  detailed report; it is separate from the per-player feed below.
- **Football player statistics:** `/flashscore/match-player-stats` is football
  only and exists only for matches with individual-stat coverage. Narrow large
  responses with `group` or `player_id`. Keep source labels, raw values,
  rankings, and provider ratings together; they are not a universal scouting
  grade.
- **Predictions and absences:** `/flashscore/match-predicted-lineups` contains
  predictions, not confirmed starters. `/flashscore/match-missing-players`
  records the names and reasons Flashscore lists, but provides no expected
  return date. An empty list can mean no reports or no match coverage; it does
  not certify that all players are healthy or available.
- **Momentum:** `/flashscore/match-momentum` returns a per-minute source series
  for covered football events. Its positive/negative direction is observed to
  favor home/away but is not a causal explanation. Empty momentum is a coverage
  gap, not evidence that the match had no swings.
- **Other sports:** `/flashscore/match-box-score` is for covered basketball,
  hockey, and baseball matches; `/flashscore/match-darts` for supported darts
  feeds; `/flashscore/match-point-by-point` for its documented sports. Keep
  sport-specific units and scoring periods intact. Not-found or empty responses
  are not zero-stat records.
- **Editorial content:** `/flashscore/match-report` returns reports only for
  editorially covered matches. `/flashscore/news-article-body` fetches a
  referenced article, and `/flashscore/news-most-read` returns provider order
  rather than measured readership. Preserve author, publisher credit, and
  publication time; label editorial statements separately from match data.
- **Competition history:** use `/flashscore/tournament-archive-seasons` only
  with a returned stage ID. Keep the season tournament ID and tournament stage
  ID distinct; similarly named or colliding IDs can point at a different
  competition.

Broadcast listings and odds use viewer-market rules. Use
`football-viewing-guide` for football TV listings and `sports-betting-research`
for bookmaker markets; do not treat either as an access guarantee or prediction.

```sh
scripts/crawlora.sh /flashscore/search q="Arsenal Manchester City"
# Use a verified match ID from the exact returned event.
scripts/crawlora.sh /flashscore/match-stats id=example-match-id
scripts/crawlora.sh /flashscore/match-player-stats id=example-match-id group=shots
scripts/crawlora.sh /flashscore/match-predicted-lineups id=example-match-id
scripts/crawlora.sh /flashscore/match-report id=example-match-id
```

Return event identity, status/time, selected observations, source URLs and
timestamps, coverage or unavailable fields, and the limits of the sample.
Describe numerical differences before interpretation. Do not claim a statistic
caused the result, a player is medically cleared, or a brief predicts future
performance.
