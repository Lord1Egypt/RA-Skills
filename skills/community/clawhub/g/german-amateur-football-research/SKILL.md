---
name: german-amateur-football-research
description: Research German amateur-football clubs, teams, competitions, local fixtures, results, tables, and player match records through FUSSBALL.DE. Use for grassroots and regional football, not professional scouting or player outreach.
---

# German amateur-football research

Build a source-attributed brief from FUSSBALL.DE's public amateur-football
records. Its competition tree spans regional associations, seasons, senior,
women's and youth teams, and local leagues. Preserve original German labels
when translating them for the user.

## Discover the competition or local fixture set

- For a competition question, start with /fussballde/filters, then use the
  returned federation and season with /fussballde/competition-options. Use the
  exact returned team type, league, area, and competition identifiers for the
  competition directory and downstream table or match routes; do not guess IDs
  or carry an ID across seasons.
- For local games, resolve the place or postcode with /fussballde/postal-codes
  and use /fussballde/match-calendar. It returns at most ten matches per
  request and has no paging; when truncated is true, narrow the date window or
  filters before presenting the list as complete.
- For a club or team, resolve the club with club search, then read its club
  record to find the team ID. Use the returned team, season, competition, and
  team-type values with match, squad, or standings routes. Keep club IDs
  separate from team IDs.

## Interpret match, table, and player data

- Keep season, federation, league level, team type, matchday, and source time in
  the result. Tables and top-scorer lists are competition-specific; do not rank
  teams or players across different levels without a comparable measure.
- A match-plan response can include both completed and future fixtures. Preserve
  the source status, score, and kickoff time rather than treating every listed
  match as played.
- Player pages may include birth dates and youth-team records. Use only details
  needed for the requested match or competition analysis; do not compile player
  contact lists or infer health, eligibility, or scouting suitability from
  public statistics.
- A blank field is unavailable evidence, not zero. Club and player profiles are
  public source records, not independent verification of a person's identity.

## Deliverable

Return the requested local fixture list, club/team context, competition table,
or player match record with the IDs and season context used. State the
match-calendar truncation and any missing squad or result details.

~~~sh
scripts/crawlora.sh /fussballde/filters
scripts/crawlora.sh /fussballde/postal-codes q="Berlin"
scripts/crawlora.sh /fussballde/match-calendar postal_code=10115
scripts/crawlora.sh /fussballde/club-search text="Berlin"
~~~
