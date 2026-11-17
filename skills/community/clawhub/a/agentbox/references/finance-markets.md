# Finance and markets: quote, market

Use this for stock, index, FX and crypto prices, and for Polymarket prediction markets. No API key needed.

## Quotes

```bash
agentbox quote get NVDA
agentbox quote get NVDA 2330.TW ^TWII USDTWD=X BTC-USD
agentbox quote history 2330.TW --range 6mo
agentbox quote history NVDA --range 1y --interval 1wk --save
agentbox quote search "Taiwan Semiconductor"
agentbox quote search 台積電
```

Symbols use Yahoo format:

| Market | Examples |
|---|---|
| US stocks | `NVDA`, `AAPL`, `BRK-B` |
| Taiwan listed / OTC | `2330.TW` (TWSE), `6488.TWO` (TPEx) |
| Hong Kong | `0700.HK` |
| Indices | `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^DJI`, `^TWII` (Taiwan), `^HSI`, `^N225` |
| FX | `USDTWD=X`, `EURUSD=X`, `JPYTWD=X` |
| Crypto | `BTC-USD`, `ETH-USD` |
| Commodities | `GC=F` (gold), `CL=F` (crude oil) |

- Do not know the symbol? Run `quote search` with the company name, then use the `symbol` from `data.results[]`.
- A bare number like `2330` fails with `ambiguous_symbol`. Add `.TW` (listed) or `.TWO` (OTC).
- `quote get` takes up to 10 symbols. Failed ones go to `data.errors[]`; the rest still return.

`quote get` fields in `data.quotes[]`: `symbol`, `name`, `price`, `currency`, `change`, `change_pct`, `previous_close`, `day_high`, `day_low`, `volume`, `week52_high`, `week52_low`, `exchange`, `market_state` (pre, regular, post, closed), `time` (ISO with exchange offset), `backend`.

`quote history` returns `data.summary` (`start_date`, `start_close`, `end_date`, `end_close`, `change`, `change_pct`, `high`, `high_date`, `low`, `low_date`, `points`) and the last 30 `rows`. `--save` stores all rows as `tbl:N` for `table query`.
Ranges: `5d`, `1mo`, `3mo`, `6mo`, `ytd`, `1y`, `5y`, `max`. Intervals: `1d`, `1wk`, `1mo`.

Errors:

- `symbol_not_found`: run `quote search` with the name.
- `rate_limited` or `network_error`: retry once with `--backend stooq` (latest price only; no Taiwan stocks; `change` is null).
- `stooq_needs_key`: Stooq history needs a key. Use the default backend.

Always say the quote time from `time` and that quotes may be delayed about 15 minutes. Compute extra numbers (returns, differences) with `agentbox calc`.

## Polymarket

```bash
agentbox market trending --limit 10
agentbox market trending --tag politics --limit 10
agentbox market search election --limit 10
agentbox market search "fed rate" --limit 15 --sort volume
agentbox market search bitcoin --closed --limit 10
agentbox market get balance-of-power-2026-midterms
agentbox market get https://polymarket.com/event/presidential-election-winner-2028
agentbox market history 2026-balance-of-power-d-senate-d-house-949 --interval 1w
agentbox market trending --limit 20 --save-table
```

- `trending` = most 24h volume right now. Good for "top markets" or "what is hot".
- `search` matches every word in titles, questions, descriptions and tags. Use 1-3 keywords. Use `--limit 10` or more; small limits miss markets.
- Default is active markets. `--closed` = resolved only; both flags = all.
- `--sort volume` (default), `liquidity`, `end` (ending soonest), `newest`. `--tag` filters by tag slug: `politics`, `elections`, `crypto`, `sports`, `economy`, `tech`, `geopolitics`.
- If `data.match` is `fuzzy`, no event had all your words. Check relevance or change keywords.

Event fields in `data.events[]`: `title`, `slug`, `url`, `end_date`, `volume`, `volume_24h`, `liquidity`, `tags`, `markets[]`.
Market fields: `question`, `odds` (e.g. `Yes 63.5% · No 36.5%`), `yes_pct` for yes/no markets, or `leader` and `leader_pct` for multi-outcome markets, `change_1d_pts`, `volume_24h`, `slug`, `market_id`.

- `market get SLUG` takes an event or market slug, a numeric id, or a polymarket.com URL. It lists all markets with `outcomes[]`, `change_1w_pts`, `description` (resolution rules) and each market `url`.
- `market history` needs ONE market. For an event with many markets you get `ambiguous_market`; the hint lists market slugs. Pick one and rerun.
- History returns `data.summary` (`start_pct`, `end_pct`, `change_pts`, `high_pct`, `low_pct`, times in UTC) and `rows`.
- `dns_error` or `network_error`: a DNS filter may block polymarket.com. Report it; do not invent odds.

Writing about markets: give the percentage, the move in points, the 24h volume, the end date and the event `url`. Say that percentages are market prices, not forecasts.
