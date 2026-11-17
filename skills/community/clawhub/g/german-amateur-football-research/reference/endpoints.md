# german-amateur-football-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**27 endpoints across 1 platform group(s).**

## FUSSBALL.DE (27)

### `fussballde_amateur_stats`

- **HTTP:** `GET /fussballde/amateur-stats`
- **What:** Get FUSSBALL.DE amateur top statistics. Returns a page of one of the ten Top-Amateurstatistiken rankings (Kreisklasse to Regionalliga, championship matches): top teams by goals, goal ratio, goals against and points average, highest-scoring matches, biggest draws, and top scorers by goals, ratio and goals in one match per week or season. Filter by season, team type and federation and page with `limit` and `offset`. A ranking is bounded to roughly its top 200 entries; `final` marks the last page.
- **Params:** `federation_id` (string, optional) — Federation id; omit for all federations; `limit` (integer, optional) — Rows per call, 1 to 100, default 30; `offset` (integer, optional) — Number of rows to skip, 0 to 1000, default 0; `season` (string, optional) — Four-digit season code, 2627 for 2026/27; the site offers the current and previous season; `stat` (string, **required**) — Ranking id; `team_type` (string, optional) — Team type id; omit for all

### `fussballde_club`

- **HTTP:** `GET /fussballde/club`
- **What:** Get a FUSSBALL.DE club. Returns one club: name, federation, team counts, profile facts (founding year, address, website) and the club's teams with their competitions and team type. Teams are those of the current season; set `season` for an earlier one and `competition_kind` to keep only teams in championships, cups, friendlies and so on. Club ids appear as `club_id` on teams and matches.
- **Params:** `club_id` (string, **required**) — Club id from a team or match, e.g. 00ES8GN8N400008VVV0AG08LVUPGND5I; `competition_kind` (string, optional) — Competition kind id; omit for all kinds; `season` (string, optional) — Four-digit season code such as 2526; default current season

### `fussballde_club_matches`

- **HTTP:** `GET /fussballde/club-matches`
- **What:** Get FUSSBALL.DE fixtures and results of a club. Returns the fixtures and results across all of a club's teams (senior and youth). `all` (default) is the club match plan for a date window (default the current season) optionally for one competition kind and paged with `limit` and `offset`; `next` is the next fixtures and `previous` the latest results. Each match names its competition and team type.
- **Params:** `club_id` (string, **required**) — Club id from fussballde-club or fussballde-club-search; `competition_kind` (string, optional) — kind all only: competition kind id; omit for all kinds; `date_from` (string, optional) — kind all only: first day as YYYY-MM-DD, default 1 July of the current season; `date_to` (string, optional) — kind all only: last day as YYYY-MM-DD, default 30 June of the season; `kind` (string, optional) — Match list kind, default all; `limit` (integer, optional) — Matches (kind all only) per call, 1 to 50, default 10; `offset` (integer, optional) — Number of matches to skip, 0 to 1000, default 0

### `fussballde_club_search`

- **HTTP:** `GET /fussballde/club-search`
- **What:** Search FUSSBALL.DE clubs by name or place. Searches FUSSBALL.DE clubs by club name, postcode or place, or both (both must match), and returns each club's id, name, postal code, city and logo. The first page reports the `total` hit count; page with `limit` (1 to 100, default 20) and `offset`, and `final` marks the last page. Zero results is a valid response. The site's search is not fuzzy and matches a club's official name (for example `RasenBallsport Leipzig`, `SC Freiburg`), so a looser display name such as `RB Leipzig` can return nothing: search by place or one distinctive word, or use the `club_id` that every team, table and match row already carries.
- **Params:** `limit` (integer, optional) — Clubs per call, 1 to 100, default 20; `offset` (integer, optional) — Number of clubs to skip, 0 to 2000, default 0; `place` (string, optional) — Postcode or place name; text or place is required; `text` (string, optional) — Club name or part of it; text or place is required

### `fussballde_competition_options`

- **HTTP:** `GET /fussballde/competition-options`
- **What:** List FUSSBALL.DE team types, leagues and areas. Returns the team types (Herren, Frauen, A-Junioren, ...), the leagues (Spielklassen) of each team type and the areas (Gebiete) of each league for one federation, season and competition type. Team type, league and area ids are federation-specific, so take them from this response and pass them to `fussballde-competitions`.
- **Params:** `competition_type` (string, optional) — Competition type id, default 1; `federation_id` (string, **required**) — Federation id; `season` (string, **required**) — Four-digit season code, 2627 for 2026/27

### `fussballde_competitions`

- **HTTP:** `GET /fussballde/competitions`
- **What:** List FUSSBALL.DE competitions for a league and area. Returns the competitions (Staffeln) at one selector path: a federation, season, competition type, team type, league and area. Each competition `id` (for example `031BFREJC800001BVS5489BUVUR5FS5A-G` for the 2026/27 Bundesliga) is the key used by the matchday, match plan, table and top-scorer endpoints. An empty list is a valid result for a path with no competitions.
- **Params:** `area` (string, **required**) — Area id from fussballde-competition-options; `competition_type` (string, optional) — Competition type id, default 1; `federation_id` (string, **required**) — Federation id; `league` (string, **required**) — League id from fussballde-competition-options; `season` (string, **required**) — Four-digit season code; `team_type` (string, **required**) — Team type id from fussballde-competition-options

### `fussballde_federation`

- **HTTP:** `GET /fussballde/federation`
- **What:** Get a FUSSBALL.DE federation or regional association. Returns the profile of one of the 22 federations (the DFB and the regional and state associations) or of one of the five regional associations (Norddeutscher, Nordostdeutscher, Süddeutscher, Südwest and Westdeutscher): name, address, website, president, club, member and team counts, and the latest news items. Provide exactly one of `federation_id` and `regional_association`.
- **Params:** `federation_id` (string, optional) — Federation id; provide exactly one of federation_id and regional_association; `regional_association` (string, optional) — Regional association; provide exactly one of federation_id and regional_association

### `fussballde_filters`

- **HTTP:** `GET /fussballde/filters`
- **What:** List FUSSBALL.DE federations, seasons and competition types. Returns the competition selector base data of FUSSBALL.DE, the German amateur-football portal: the 22 federations (DFB plus regional associations), the available seasons per federation, and the competition types per federation and season. Use it first to get valid `federation_id`, `season` and `competition_type` values for the competition discovery endpoints.
- **Params:** `federation_id` (string, optional) — Optional federation id that narrows seasons and competition types to one federation

### `fussballde_match`

- **HTTP:** `GET /fussballde/match`
- **What:** Get a FUSSBALL.DE match. Returns one match: teams, competition, date, kick-off time, venue, score and half-time score, match number and matchday, officials, goals with minutes and timeline events such as substitutions. Fields the match has not published (for example a future match's score) are omitted.
- **Params:** `match_id` (string, **required**) — Match id from fussballde-matchday or fussballde-match-plan

### `fussballde_match_calendar`

- **HTTP:** `GET /fussballde/match-calendar`
- **What:** Get FUSSBALL.DE matches near a postcode. Returns the matches FUSSBALL.DE's Matchkalender lists around a five-digit postcode within a date range (default today plus six days, at most 92 days), optionally filtered by team types and competition kind. Each match includes its team type (for example D-Junioren) and league. The upstream returns at most 10 matches per request and has no paging: `truncated` is true when the page is full, so narrow the dates or filters to see the rest. Zero matches is a valid response.
- **Params:** `competition_kind` (string, optional) — Competition kind id; omit for all kinds; `date_from` (string, optional) — First day as YYYY-MM-DD, default today (Europe/Berlin); `date_to` (string, optional) — Last day as YYYY-MM-DD, at most 92 days after date_from, default six days after date_from; `postal_code` (string, **required**) — Five-digit German postcode; look one up with fussballde-postal-codes; `team_types` (string, optional) — Comma-separated team type ids such as 1,3; omit for all team types

### `fussballde_match_comparison`

- **HTTP:** `GET /fussballde/match-comparison`
- **What:** Compare the two teams of a FUSSBALL.DE match. Returns a pre-match comparison for one match: `history` is the all-time head-to-head record (duels, wins, draws, defeats, goals), `meetings` lists the other fixtures and results between the two teams, and `season` compares both teams' current standing, points, goals, form, top scorer and cards.
- **Params:** `match_id` (string, **required**) — Match id from fussballde-matchday or fussballde-match-plan; `view` (string, optional) — Comparison view, default history

### `fussballde_match_plan`

- **HTTP:** `GET /fussballde/match-plan`
- **What:** Get the full FUSSBALL.DE match plan of a competition. Returns every match of a competition's season (fixtures and results), including the earliest matchdays, optionally filtered to one team and a date window; the date window is applied by the site, so a narrow window is cheaper than filtering a full season. Cups and tournaments are assembled round by round: every match carries its `round` and the response lists the `rounds` with their ids. Use it for a complete schedule; use `fussballde-matchday` for one matchday.
- **Params:** `competition_id` (string, **required**) — Competition id from fussballde-competitions; `date_from` (string, optional) — Earliest match date as YYYY-MM-DD; default is the whole season; `date_to` (string, optional) — Latest match date as YYYY-MM-DD; default is the whole season; `team_id` (string, optional) — Team id to keep only that team's matches

### `fussballde_matchday`

- **HTTP:** `GET /fussballde/matchday`
- **What:** Get FUSSBALL.DE matches of a competition matchday. Returns the matches of a competition's current matchday, of a numbered matchday (`matchday`, 1 to the competition's matchday count, reported as `matchday_count`) or of the matchday around a date. Each match has teams, date, kick-off time, score and status (`finished`, `scheduled`, `cancelled` and the other values listed below). Cups and tournaments have no numbered matchdays; for them the response lists the competition's `rounds` (each round id works as `competition_id` to read that round) and labels every match with its `round`. Dates, times and scores are decoded from the site's obfuscated glyph fonts.
- **Params:** `competition_id` (string, **required**) — Competition id from fussballde-competitions; `date` (string, optional) — Matchday date as YYYY-MM-DD; omit for the current matchday; cannot be combined with matchday; `matchday` (integer, optional) — Matchday number, 1 to the competition's matchday count (34 for the Bundesliga); cannot be combined with date

### `fussballde_national_top_scorers`

- **HTTP:** `GET /fussballde/national-top-scorers`
- **What:** Get the nationwide FUSSBALL.DE top scorers by league level. Returns the top 10 scorers of every league level across Germany for men or women (the site's Torjägerkanone), with goals, matches played and club. Only championship matches count and the upstream refreshes the ranking once a day; the response `note` carries its last-update time. Adult teams only.
- **Params:** `team_type` (string, optional) — Ranking to return, default men

### `fussballde_news`

- **HTTP:** `GET /fussballde/news`
- **What:** List FUSSBALL.DE news. Returns news teasers of one FUSSBALL.DE stream (all news, magazine, Regionalliga, federations, service, campaigns or help center) with title, category, publication date and time, and excerpt, paged with `limit` (1 to 50, default 10) and `offset`; `final` is true on the last page. Use `regional_league` or `help_category` to narrow the Regionalliga and help-center streams to one league or category. Use the article id with `fussballde-news-article` for the full text.
- **Params:** `help_category` (string, optional) — Only help-center articles of one category (implies stream helpcenter); `limit` (integer, optional) — Articles per call, 1 to 50, default 10; `offset` (integer, optional) — Number of articles to skip, 0 to 5000, default 0; `regional_league` (string, optional) — Only Regionalliga news of one league (implies stream regionalliga); `stream` (string, optional) — News stream, default all_news

### `fussballde_news_article`

- **HTTP:** `GET /fussballde/news-article`
- **What:** Get a FUSSBALL.DE news article. Returns one FUSSBALL.DE news article: title, category, publication date and time, lead image and caption, and the body paragraphs as plain text.
- **Params:** `article_id` (string, **required**) — Numeric article id from fussballde-news

### `fussballde_news_search`

- **HTTP:** `GET /fussballde/news-search`
- **What:** Search FUSSBALL.DE news. Searches FUSSBALL.DE editorial news (`news`) or the Profi-Newsflash (`pro_news`) by keyword and returns teasers with title, category, date and excerpt. The first page (offset 0) also reports the total hit count; page with `limit` (1 to 50) and `offset`. No hits is a valid empty result.
- **Params:** `channel` (string, optional) — News channel, default news; `limit` (integer, optional) — Articles per call, 1 to 50, default 10; `offset` (integer, optional) — Number of hits to skip, 0 to 10000, default 0; `q` (string, **required**) — Search text, 2 to 80 characters

### `fussballde_player`

- **HTTP:** `GET /fussballde/player`
- **What:** Get a FUSSBALL.DE player profile. Returns a player's public profile: name, team, team type, birth date and, for registered players (`profile_type` full), the current-season statistics such as appearances, minutes played, goals, goals against and cards. Players without a registered profile (`profile_type` basic) only have name, team and team type. Player ids come from `fussballde-player-search`, scorer lists, squads and amateur statistics.
- **Params:** `player_id` (string, **required**) — Player id from fussballde-player-search, fussballde-top-scorers, fussballde-team-squad or fussballde-amateur-stats

### `fussballde_player_matches`

- **HTTP:** `GET /fussballde/player-matches`
- **What:** Get a FUSSBALL.DE player's match-by-match record. Returns a registered player's matches for one season and team: date, teams, result and per match the goals, the minute they were substituted in or out, and minutes played. Also lists the player's teams and competitions for the season so another team can be selected with `team_id`. Basic profiles without registration have no match data.
- **Params:** `player_id` (string, **required**) — Player id of a full profile, see fussballde-player; `season` (string, optional) — Four-digit season code, default current season; `team_id` (string, optional) — Team id from the teams list of a previous response; default the player's main team

### `fussballde_player_search`

- **HTTP:** `GET /fussballde/player-search`
- **What:** Search FUSSBALL.DE players by name. Searches players registered on FUSSBALL.DE by first and/or last name, optionally narrowed by postcode or place, and returns each player's id, name, birth date, team and team type. The first page reports the `total` hit count; page with `limit` (1 to 100, default 20) and `offset`, and `final` marks the last page. At least one of `first_name` and `last_name` is required. No match is a valid empty result.
- **Params:** `first_name` (string, optional) — First name; first_name or last_name is required; `last_name` (string, optional) — Last name; first_name or last_name is required; `limit` (integer, optional) — Players per call, 1 to 100, default 20; `offset` (integer, optional) — Number of players to skip, 0 to 2000, default 0; `place` (string, optional) — Postcode or place name to narrow the result; cannot be used alone

### `fussballde_position_history`

- **HTTP:** `GET /fussballde/position-history`
- **What:** Get the FUSSBALL.DE fever curve of a competition. Returns every team's table position after each played matchday of a competition (the site's Fieberkurve), as one ordered list of positions per team. Position 1 is the leader; the list index is the matchday.
- **Params:** `competition_id` (string, **required**) — Competition id from fussballde-competitions

### `fussballde_postal_codes`

- **HTTP:** `GET /fussballde/postal-codes`
- **What:** Look up German postcodes by place name. Returns the German postcodes (with city and district) that FUSSBALL.DE's own location search suggests for a place name or postcode prefix. Use it to turn a place such as Dortmund into the five-digit `postal_code` that `fussballde-match-calendar` requires. No match is a valid empty list.
- **Params:** `q` (string, **required**) — Place name or postcode prefix, 2 to 40 characters

### `fussballde_table`

- **HTTP:** `GET /fussballde/table`
- **What:** Get a FUSSBALL.DE competition standings table. Returns a competition's standings in one view: `overall`, `home_away` (home and away tables), `rounds` (first and second half-season tables), `fairness` (fair-play table) or `cross` (cross table of results between every pair of teams). Set `matchday` to get the standings as they were after that matchday (not available for `fairness`). Rows carry position, team, played, won, drawn, lost, goals and points where the view has them, plus the raw cells.
- **Params:** `competition_id` (string, **required**) — Competition id from fussballde-competitions; `matchday` (integer, optional) — Return the standings after this matchday, 1 to the competition's matchday count; not available for the fairness view; `view` (string, optional) — Standings view, default overall

### `fussballde_team`

- **HTTP:** `GET /fussballde/team`
- **What:** Get a FUSSBALL.DE team. Returns one team page: name, team type, federation, standing summary (competition, table position, points, goal ratio), current competitions, home venues, the club profile (founding year, address, contact) and the team's season-by-season history with final placings and the highest league reached. Use `fussballde-team-matches` and `fussballde-team-squad` for fixtures and players.
- **Params:** `team_id` (string, **required**) — Team id from fussballde-matchday, fussballde-table or fussballde-club

### `fussballde_team_matches`

- **HTTP:** `GET /fussballde/team-matches`
- **What:** Get FUSSBALL.DE fixtures and results of a team. Returns a team's matches across its competitions. `all` (default) is the match plan for a date window (default the current season, 1 July to 30 June), optionally for one competition kind and paged with `limit` and `offset`; `next` is the next 10 fixtures, `previous` the latest 10 results, and `wins`, `draws` and `losses` the latest 10 finished matches with that outcome.
- **Params:** `competition_kind` (string, optional) — kind all only: competition kind id; omit for all kinds; `date_from` (string, optional) — kind all only: first day as YYYY-MM-DD, default 1 July of the current season; `date_to` (string, optional) — kind all only: last day as YYYY-MM-DD, default 30 June of the season; `kind` (string, optional) — Match list kind, default all; `limit` (integer, optional) — Matches (kind all only) per call, 1 to 50, default 10; `offset` (integer, optional) — Number of matches to skip, 0 to 1000, default 0; `team_id` (string, **required**) — Team id, see fussballde-team

### `fussballde_team_squad`

- **HTTP:** `GET /fussballde/team-squad`
- **What:** Get a FUSSBALL.DE team squad. Returns a team's players for a season: the `squad` (appearances, minutes, goals), `arrivals` or `departures` with the columns the site publishes for each. Player names come in the site's `Surname, Forename` order.
- **Params:** `kind` (string, optional) — Player list kind, default squad; `season` (string, optional) — Four-digit season code, default current season; `team_id` (string, **required**) — Team id, see fussballde-team

### `fussballde_top_scorers`

- **HTTP:** `GET /fussballde/top-scorers`
- **What:** Get the FUSSBALL.DE top scorers of a competition. Returns a page of a competition's top-scorer list with position, player, team and goals; page through it with `limit` (1 to 100, default 30) and `offset`. Tied scorers share a position. A competition without recorded scorers returns an empty list; cups and tournaments have no scorer list at all and return 404.
- **Params:** `competition_id` (string, **required**) — Competition id from fussballde-competitions; `limit` (integer, optional) — Scorers per call, 1 to 100, default 30; `offset` (integer, optional) — Number of scorers to skip, 0 to 1000, default 0
