# casino-game-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Only the endpoints used by this workflow. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**8 endpoints across 2 platform group(s).**

## DraftKings Casino (5)

### `draftkings_casino_cleopatra_guide`

- **HTTP:** `GET /draftkings/casino/slots/cleopatra-guide`
- **What:** DraftKings Cleopatra slot guide. Returns written gameplay sections from DraftKings Casino's public Cleopatra tutorial. The image-only payout table and promotional recommendation/CTA sections are omitted. This is informational page content, not wagering advice.
- **Params:** _none_

### `draftkings_casino_directory`

- **HTTP:** `GET /draftkings/casino/directory`
- **What:** DraftKings Casino slots directory. Returns the public Online Slots and How to Play Slots links from the DraftKings Casino homepage. Fetch the guide sections with draftkings_casino_slots_guide. It does not fetch game catalogs, promotions, winners, jackpots, or account data.
- **Params:** _none_

### `draftkings_casino_slots_categories`

- **HTTP:** `GET /draftkings/casino/slots/categories`
- **What:** DraftKings Casino slot categories. Lists public slot-category sections from the logged-out Casino configuration. It returns category labels and upstream IDs only; it does not return game listings, winners, jackpots, promotions, personal data, or jurisdiction eligibility.
- **Params:** _none_

### `draftkings_casino_slots_guide`

- **HTTP:** `GET /draftkings/casino/slots-guide`
- **What:** DraftKings Casino slots guide. Returns the public slots guide's basic rules and responsible-play sections. Account setup, payments, promotions, and strategy sections are omitted. This is informational page content, not gambling advice.
- **Params:** _none_

### `draftkings_casino_wheel_of_fortune_guide`

- **HTTP:** `GET /draftkings/casino/slots/wheel-of-fortune-guide`
- **What:** DraftKings Wheel of Fortune slot guide. Returns written gameplay instructions from DraftKings Casino's public Wheel of Fortune: Triple Extreme Spin tutorial. The video embed, demo-mode call to action, and jurisdiction-specific footer are omitted. This is informational content, not wagering advice.
- **Params:** _none_

## FanDuel (3)

### `fanduel_casino_categories`

- **HTTP:** `GET /fanduel/casino/categories`
- **What:** FanDuel Casino categories. Lists the FanDuel Casino lobby's public categories (slots, jackpots, blackjack, roulette, live dealer, exclusives and more) with the slug the `category` route takes. `region` picks the lobby: `mi` (default) is the Michigan lobby at casino.fanduel.com, which includes the Michigan-only MotorCity Favorites collection, and `on` is the Ontario lobby at casino.fanduel.ca, which has three Ontario-only collections and lacks Hot Slots, Classic Reels and Bonus Buy. The casino site serves one state's lobby to every address tried, so no other state is offered. The signed-in player's own favorites list is not a public category and is not included.
- **Params:** `region` (string, optional) — Lobby: `mi` Michigan (default) or `on` Ontario

### `fanduel_casino_category`

- **HTTP:** `GET /fanduel/casino/category`
- **What:** FanDuel Casino category games. Returns a page of a casino category's games in the lobby's own order, with each game's slug, name, studio, badge (`Exclusive`, `Jackpot`), whether it is flagged as a site-wide jackpot game, and a link to its page. `providers` and `badges` count the whole category so the values the `provider` and `badge` filters accept are always visible; `q` matches every word against the game name. `all-games`, `slots` and `double-your-bet-category` hold the whole catalog (about 3,800 games) in one 30MB page, so their first call is slow and the parsed list is then cached for 15 minutes.
- **Params:** `badge` (string, optional) — Keep only games with this badge, exactly as listed in the response `badges` (for example `Exclusive`, `Jackpot`); `category` (string, **required**) — Category slug from the `categories` route for the same `region`. Michigan has `all-games`, `new`, `slots`, `double-your-bet-category`, `jackpots`, `daily-jackpots`, `hot-slots`, `classic-reels-category`, `bonus-buy-category`, `high-limit-category`, `spooky-slots-category`, `exclusives`, `pick-play`, `arcade`, `blackjack`, `baccarat`, `roulette`, `table`, `livecasino`, `online-casino-favorites`, `explore-videos`, `motorcity-favorites`; Ontario has the same list without `hot-slots`, `classic-reels-category`, `bonus-buy-category`, `online-casino-favorites` and `motorcity-favorites`, and adds `fallsview-favourites-category`, `the-wolf-den-category`, `sports-central`. A slug the lobby lacks returns `400`; `limit` (integer, optional) — Games per page, 1 to 200; default 50; `offset` (integer, optional) — Games to skip; default 0; `provider` (string, optional) — Keep only games from this studio, exactly as listed in the response `providers` (for example `NYX`, `Evolution`, `IGT`); a value the category does not have returns `400`; `q` (string, optional) — Words to find in the game name, such as `huff puff`; every word must match; `region` (string, optional) — Lobby: `mi` Michigan (default) or `on` Ontario

### `fanduel_casino_game`

- **HTTP:** `GET /fanduel/casino/game`
- **What:** FanDuel Casino game detail. Returns a casino game's detail page: category, minimum and maximum bet, studio, volatility, themes, features, how many players are in it right now, its badge and description, and the identifiers its play link carries (provider, provider reference, game id and the lobby region). Slugs come from the `category` route; an unknown game returns 404.
- **Params:** `game` (string, **required**) — Game slug from the `category` route (`games[].slug`), lower-case, such as `huff-n-even-more-puff-hard-hat-edition`; `region` (string, optional) — Lobby of the game: `mi` Michigan (default) or `on` Ontario
