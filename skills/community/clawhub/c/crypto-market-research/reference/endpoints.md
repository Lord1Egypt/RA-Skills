# crypto-market-research — endpoint reference

> Generated from `scripts/tools.json` by `scripts/generate.mjs` — do not edit by hand.

Endpoints this skill uses, grouped by platform. Call them via `scripts/crawlora.sh` (see SKILL.md).

All paths are relative to the API base `https://api.crawlora.net/api/v1` and require the header `x-api-key: $CRAWLORA_API_KEY`. Path params like `{id}` are substituted into the URL; `GET` params go in the query string; `POST` params go in a JSON body.

**21 endpoints across 1 platform group(s).**

## CoinGecko (21)

### `coingecko_categories`

- **HTTP:** `GET /coingecko/categories`
- **What:** CoinGecko categories. Lists CoinGecko coin categories, up to `limit` rows (default and max 100), priced in the `vs_currency` you choose. Each row has its rank, id, slug, name, URL, 1h, 24h and 7d percentage changes, market cap, 24h volume and coin count, where CoinGecko shows them.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_category_coins`

- **HTTP:** `GET /coingecko/category/{slug}/coins`
- **What:** CoinGecko category coins. Lists the coins in one CoinGecko category, identified by the required `slug` such as `stablecoins`. Paged with `page` (default 1) and `limit` (default and max 100), priced in `vs_currency`. Each coin has rank, symbol, price, 1h to 30d changes, 24h volume, market cap and fully diluted valuation.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `slug` (string, **required**) — CoinGecko category slug such as stablecoins; `vs_currency` (string, optional) — Quote currency

### `coingecko_chain`

- **HTTP:** `GET /coingecko/chains/{id}`
- **What:** CoinGecko chain detail. Returns sections from a CoinGecko chain detail page. Sections are omitted when not present. This endpoint supports the documented `vs_currency` enum.
- **Params:** `id` (string, **required**) — CoinGecko chain id such as ethereum; `limit` (integer, optional) — Rows per section to return, default 20, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_chains`

- **HTTP:** `GET /coingecko/chains`
- **What:** CoinGecko chains. Lists blockchains from CoinGecko's chains table, up to `limit` rows (default and max 100), in the `vs_currency` you pick. Each chain has its rank, id, name, URL, logo, top gainers, 24h, 7d and 30d changes, 24h volume, TVL, dominance percent and coin count, where shown.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_coin`

- **HTTP:** `GET /coingecko/coin/{id}`
- **What:** CoinGecko coin profile. Returns CoinGecko profile, market stats, links, and categories for one coin id. This endpoint supports the documented `vs_currency` enum and is not intended for real-time trading.
- **Params:** `id` (string, **required**) — CoinGecko coin id such as bitcoin; `vs_currency` (string, optional) — Quote currency

### `coingecko_coin_analysis`

- **HTTP:** `GET /coingecko/coin/{id}/analysis`
- **What:** CoinGecko coin chart analysis. Returns derived price-chart metrics from CoinGecko public chart JSON. This endpoint supports the documented `vs_currency` enum and is not investment advice or real-time trading data.
- **Params:** `id` (string, **required**) — CoinGecko coin id such as bitcoin; `include_annotations` (boolean, optional) — Fetch optional CoinGecko chart annotations; `range` (string, optional) — Chart range; `vs_currency` (string, optional) — Quote currency

### `coingecko_exchange`

- **HTTP:** `GET /coingecko/exchange/{id}`
- **What:** CoinGecko exchange detail. Returns profile stats and market rows from a CoinGecko exchange page. This endpoint supports the documented `vs_currency` enum.
- **Params:** `id` (string, **required**) — CoinGecko exchange id such as binance; `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_exchanges`

- **HTTP:** `GET /coingecko/exchanges`
- **What:** CoinGecko exchanges. Lists CoinGecko exchanges from one table chosen by `kind`: `spot` (default), `dex`, `derivatives` or `perp_dex`. Paged with `page` and `limit` (default and max 100). Each exchange has rank, id, name, URL, logo, and, where shown, a trust score and 24h volume in `vs_currency`.
- **Params:** `kind` (string, optional) — Exchange table kind, default spot; `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_gainers_losers`

- **HTTP:** `GET /coingecko/gainers-losers`
- **What:** CoinGecko crypto gainers and losers. Returns CoinGecko's top crypto gainers and top losers as two separate arrays, `gainers` and `losers`, each up to `limit` rows (default 20, max 100). Each coin has its rank, symbol, name, price in `vs_currency`, 24h percentage change and 24h volume.
- **Params:** `limit` (integer, optional) — Rows per section to return, default 20, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_global`

- **HTTP:** `GET /coingecko/global`
- **What:** CoinGecko global market snapshot. Returns CoinGecko's global crypto market snapshot: total market cap in USD with its 24-hour and 1-year change, Bitcoin market cap, Bitcoin and Ethereum dominance, stablecoin market cap and share, and the number of coins, exchanges and categories tracked. Takes no parameters.
- **Params:** _none_

### `coingecko_global_charts`

- **HTTP:** `GET /coingecko/global/charts`
- **What:** CoinGecko global chart series. Returns a time series for one global crypto metric from CoinGecko: total market cap (default), Bitcoin dominance, altcoin market cap or DeFi market cap. Choose a `range` from `24h` to `max` (default `90d`) and cap points per series with `limit` (default 120, max 500). Each point has a timestamp, datetime and value.
- **Params:** `kind` (string, optional) — Chart kind, default total_market_cap; `limit` (integer, optional) — Rows per series to return, default 120, max 500; `range` (string, optional) — Chart range, default 90d

### `coingecko_learn_articles`

- **HTTP:** `GET /coingecko/learn/articles`
- **What:** CoinGecko Learn articles. Lists article cards from CoinGecko Learn, optionally narrowed by `category` (`all` by default, `latest`, `guides`, `reviews`, `api` and others), up to `limit` (default 20, max 50). Each card has title, URL, image, category, excerpt, author, published date and, where present, rating score, text and votes.
- **Params:** `category` (string, optional) — Learn category, default all; `limit` (integer, optional) — Rows to return, default 20, max 50

### `coingecko_markets`

- **HTTP:** `GET /coingecko/markets`
- **What:** CoinGecko markets. Returns cryptocurrency market rows from CoinGecko. This endpoint supports the documented `vs_currency` enum and is not intended for real-time trading.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_new_coins`

- **HTTP:** `GET /coingecko/new-coins`
- **What:** CoinGecko new cryptocurrencies. Lists newly listed cryptocurrencies from CoinGecko, paged with `page` (default 1) and `limit` (default and max 100), priced in `vs_currency`. Each coin has its rank, symbol, name, chain, price, 1h and 24h changes, 24h volume, fully diluted valuation and when it was last added.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_news`

- **HTTP:** `GET /coingecko/news`
- **What:** CoinGecko news cards. Returns recent crypto news cards from CoinGecko, up to `limit` articles (default 20, max 50). Each article has its title, URL, image URL, summary, publisher and `published_text`, plus the coins it mentions with their id, name, symbol, URL and `change_percent` when present.
- **Params:** `limit` (integer, optional) — Rows to return, default 20, max 50

### `coingecko_nft_category`

- **HTTP:** `GET /coingecko/nft/category/{slug}`
- **What:** CoinGecko NFT category. Lists NFT collections in one CoinGecko NFT category, identified by the required `slug` such as `metaverse`. Paged with `page` and `limit` (default and max 100). Each collection has chain, floor price and market cap in native and USD terms, 24h volume, 24h sales, and 24h, 7d and 30d changes.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `slug` (string, **required**) — CoinGecko NFT category slug such as metaverse; `vs_currency` (string, optional) — Quote currency

### `coingecko_nfts`

- **HTTP:** `GET /coingecko/nfts`
- **What:** CoinGecko NFT collections. Lists NFT collections from CoinGecko's main NFT table, paged with `page` (default 1) and `limit` (default and max 100). Each collection has rank, name, chain, floor price, market cap and 24h volume in native and USD terms, 24h sales, and 24h, 7d and 30d percentage changes.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100; `page` (integer, optional) — Page number, default 1; `vs_currency` (string, optional) — Quote currency

### `coingecko_search`

- **HTTP:** `GET /coingecko/search`
- **What:** CoinGecko discovery search. Searches CoinGecko for the required query `q` and returns matches in separate sections: `coins`, `categories`, `markets`, `nft_contracts`, `asset_platforms` and `posts`, each up to `limit` rows (default 10, max 50). Every section is always an array, and a search with no matches returns empty arrays.
- **Params:** `limit` (integer, optional) — Rows per section to return, default 10, max 50; `q` (string, **required**) — Search query

### `coingecko_token_unlocks`

- **HTTP:** `GET /coingecko/token-unlocks`
- **What:** CoinGecko incoming token unlocks. Returns CoinGecko's list of upcoming token unlocks, up to 100 rows. Each row has the coin's name, symbol, rank, price, 1-hour, 24-hour and 7-day change and market cap, the share of supply already released, and the next unlock's amount, percentage, USD value and time remaining.
- **Params:** `limit` (integer, optional) — Rows to return, default 100, max 100

### `coingecko_treasuries`

- **HTTP:** `GET /coingecko/treasuries`
- **What:** CoinGecko crypto treasuries. Lists entities that hold crypto treasuries, filtered by `asset` (`all`, `bitcoin`, `ethereum`, `solana`, `bnb`, `xrp`, `tron`) and `holder_type` (`all`, `companies`, `governments`), up to `limit` (default and max 100). Setting both filters to non-`all` values is rejected. Rows show holdings, cost, current value, mNAV and 30-day activity.
- **Params:** `asset` (string, optional) — Treasury asset filter, default all; `holder_type` (string, optional) — Treasury holder type filter, default all; `limit` (integer, optional) — Rows to return, default 100, max 100; `vs_currency` (string, optional) — Quote currency

### `coingecko_trending`

- **HTTP:** `GET /coingecko/trending`
- **What:** CoinGecko trending highlights. Returns trending coins and trending categories from CoinGecko's highlights, deduplicated by slug, each section up to `limit` rows (default 20, max 50). Items carry name, URL and, where CoinGecko shows them, price in `vs_currency` and 1h, 24h and 7d percentage changes.
- **Params:** `limit` (integer, optional) — Rows per section to return, default 20, max 50; `vs_currency` (string, optional) — Quote currency
