# flashscore-match-analysis — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**13 endpoints across 1 platform group(s).**

## Flashscore (13)

### `flashscore_match_box_score`

- **HTTP:** `GET /flashscore/match-box-score`
- **What:** Flashscore basketball, hockey and baseball box score. Returns the per-player box score of a basketball, hockey or baseball match: one table per team (hockey adds a goalkeeper table and baseball a pitcher table) with the statistic columns the provider defines for that sport, and each player's value per column, or null where Flashscore shows a dash. Other sports and matches without box-score coverage return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_darts`

- **HTTP:** `GET /flashscore/match-darts`
- **What:** Flashscore darts throw-by-throw and statistics. Returns a darts match leg by leg: who started and won each leg, the leg score, every visit with the points scored, the score remaining and 180 or 140-plus highlights, and the score the winner finished from, plus the statistics comparison (three-dart average, 180s, 140+ and 100+ visits, checkout percentage, highest checkout). Set-play matches add the set of each leg, the leg score within the set and the statistics of every set; a live match includes the leg being played. Streamed events whose scoring is not tracked and non-darts matches return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_missing_players`

- **HTTP:** `GET /flashscore/match-missing-players`
- **What:** Flashscore missing and doubtful players. Returns the players listed as missing and as doubtful for each side of a match, with the stated reason. Empty lists are a valid answer: nobody is reported missing, or the match has no coverage. Expected return dates are not provided by the source.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_momentum`

- **HTTP:** `GET /flashscore/match-momentum`
- **What:** Flashscore football match momentum. Returns the per-minute momentum series of a football match (values from -1 to 1, positive favouring the home side) with the half and stoppage-time marker of each minute, and the key events plotted on it (goals, own goals, penalties, red cards) with their team and player. Matches without momentum coverage and non-football matches return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore football match id

### `flashscore_match_player_stats`

- **HTTP:** `GET /flashscore/match-player-stats`
- **What:** Flashscore football player match statistics and ratings. Returns per-player statistics for a football match with player-statistics coverage: the Flashscore rating, highlight badges and every statistic of the player-statistics tabs (shots, expected goals, passes, duels, goalkeeping and more) with display text, unrounded value and rank, plus the statistic and group definitions. The full response is large; narrow it with group, or with player_id for a single player. Other sports and matches without coverage return not found.
- **Params:** `group` (string, optional) — Optional statistic group; `id` (string, **required**) — Eight-character Flashscore football match id; `player_id` (string, optional) — Eight-character Flashscore player id from this match; returns only that player

### `flashscore_match_point_by_point`

- **HTTP:** `GET /flashscore/match-point-by-point`
- **What:** Flashscore point-by-point scoring history. Returns the scoring history of a tennis, volleyball, badminton, handball or basketball match, grouped by set, quarter or half. Tennis lists each game with its server, winner, the running score inside the game and break, set and match point flags, plus tiebreak points; the other sports list every rally or basket with the leading side's margin. When a tennis match is live, current_game holds the game or tiebreak in progress. Other sports and matches without coverage return not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_predicted_lineups`

- **HTTP:** `GET /flashscore/match-predicted-lineups`
- **What:** Flashscore predicted lineups. Returns each side's predicted formation, predicted starters with position tags and player details, lineup groups, and coaches. Predictions usually appear shortly before kickoff for covered matches; a match with no predicted players on either side returns not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_report`

- **HTTP:** `GET /flashscore/match-report`
- **What:** Flashscore editorial match report. Returns Flashscore's written match report: title, author, publication time, the full text as ordered paragraphs and inline images (with links to teams, players and competitions kept as structured data), and the credited photos. Only matches with editorial coverage have a report; every other match returns not found.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_match_stats`

- **HTTP:** `GET /flashscore/match-stats`
- **What:** Flashscore match statistics. Returns Flashscore's public delimited statistics feed for a match id copied from a Flashscore match URL. The raw upstream feed is preserved as text because its format is not JSON.
- **Params:** `id` (string, **required**) — Eight-character Flashscore match id

### `flashscore_news_article_body`

- **HTTP:** `GET /flashscore/news-article-body`
- **What:** Flashscore news article with full text. Returns a Flashscore article with its headline, standfirst, author, source credit, tags, publication and edit times, cover image and the full body converted to plain-text paragraphs and headings with structured links to players, teams, matches and other articles. Embedded posts, images and info boxes are kept as placeholder blocks, not in the text. Live blogs work too. An unknown article id returns not found. For metadata and image variants only, use flashscore-news-article.
- **Params:** `id` (string, **required**) — Eight-character Flashscore news article id from a news listing, flashscore-entity-news or flashscore-news-most-read

### `flashscore_news_most_read`

- **HTTP:** `GET /flashscore/news-most-read`
- **What:** Flashscore most-read news. Returns Flashscore's site-wide list of the most-read news articles right now (about 20) in the provider's order, with title, slug, path, publication time and cover image. Use flashscore-news-article-body for an article's full text.
- **Params:** _none_

### `flashscore_search`

- **HTTP:** `GET /flashscore/search`
- **What:** Flashscore search. Searches the same public entity index used by Flashscore's search box. Results can include teams, players, and tournament templates across supported sports.
- **Params:** `q` (string, **required**) — Search phrase (2 to 80 characters)

### `flashscore_tournament_archive_seasons`

- **HTTP:** `GET /flashscore/tournament-archive-seasons`
- **What:** Flashscore competition seasons by stage id. Returns every season of the competition that owns a tournament stage: season label, season tournament id, whether it is current, the winning participants and the stage ids of each season, plus the requested stage's names and page tabs (summary, odds, standings, results, fixtures, draw, news). Get a stage id from tournament_stage_id in the competition block of team, player and match event lists, then reuse the stage ids returned here for older seasons. Pass a stage id, not a season tournament id or a competition id: other ids can return an unrelated competition, so check the returned tournament name. An unknown stage id returns not found.
- **Params:** `stage_id` (string, **required**) — Eight-character tournament stage id (tournament_stage_id of an event competition block)
