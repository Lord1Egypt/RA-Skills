---
name: agentfeed-crypto
description: Crypto market data for AI agents (liquidations, funding, open interest, prices), Solana pre-trade checks, OFAC sanctions screening, scholarly papers, utilities and fixed-purpose language tasks (OCR, translate, summarize, extract, classify, prompt-injection check, transcribe). 82 pay-per-call routes at $0.001-$0.10 over x402, paid in USDC on 9 networks in every 402 (Solana, Base, Polygon, Arbitrum, Arc, Algorand, Optimism, Monad, Avalanche) and on 11 more networks on request (not always USDC), MPP on Tempo on every route, and prepaid API keys for bots that cannot pay x402.
version: 1.5.0
homepage: https://x402.ochinimus.app
metadata:
  openclaw:
    emoji: "🌊"
    homepage: https://x402.ochinimus.app
    requires:
      bins:
        - curl
        - base64
    envVars: []
    author: seekdaseek
    links:
      homepage: https://x402.ochinimus.app
      repository: https://github.com/seekdaseek/agentfeed
      documentation: https://x402.ochinimus.app/openapi.json
---

# AgentFeed: crypto market data and fixed-purpose tools for agents

Crypto market data for AI agents (liquidations, funding, open interest, prices), Solana pre-trade checks, OFAC sanctions screening, scholarly papers, utilities and fixed-purpose language tasks (OCR, translate, summarize, extract, classify, prompt-injection check, transcribe). AgentFeed (https://x402.ochinimus.app) sells it per request; this skill covers its 82 paid data routes.

The liquidation tape is recorded by AgentFeed itself from Bybit (the complete, unthrottled
stream), OKX and Binance; exchanges publish no liquidation history, so it cannot be rebuilt
later. No perp, funding or open-interest route reads Bybit, OKX or Binance: those read Hyperliquid.

This skill is instructions for when to call these HTTPS routes and how to pay. It runs no code,
reads no files, needs no account or API key to pay per call, and never places trades or moves
funds beyond the per-call payment (or one prepaid key purchase) the user approved.

## When to use it

- What is being liquidated now on a perp, long vs short totals, where leverage got flushed, or the odds of a liquidation burst in the next 15 minutes.
- Which Hyperliquid perps have unusual funding; the whole perp market in one table for a bot (signal board) or one coin's signal (coin signal).
- One regime read for BTC, ETH, SOL or HYPE; how the biggest Hyperliquid traders are positioned; extreme funding on stock, index, gold or oil perps.
- A Solana token checked before a trade (token check, token flow, holder clusters).
- A wallet screened against OFAC sanctions, an email or domain checked, scholarly papers or a Wikipedia summary.
- SEC filings, insider trades or 8-K events; a web page or PDF as markdown.
- An exact hash, QR code, time-zone conversion or unit conversion.
- A fixed-purpose language task on supplied content: OCR, summary, field extraction, translation, classification, prompt-injection check, transcript.
- A bot that can set an HTTP header but cannot sign an x402 payment: a prepaid API key (section below).

Do not use it for general crypto knowledge, for questions a free source answers
well, or for anything that is not live market state.

## Routes (all GET, JSON)

83 paid data routes, $0.001 to $0.10 per call, at https://x402.ochinimus.app/api/<route>. The tables are
generated from the live `/openapi.json`: check it before relying on a price. `*` marks a required parameter,
path parameters are in braces, ranges and defaults are shown where the spec gives them. Full descriptions and
example responses are in `/openapi.json`. The seven prepaid key routes are not data routes and are not listed.

### Liquidation tape and cascades (12)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `liquidations` | $0.005 | symbol, scope (core/all), limit (1-100, default 25), min_usd | recent liquidation prints across the tape |
| `liquidation-stats` | $0.01 | none | 1h and 24h long/short totals, per exchange |
| `liquidation-leaders` | $0.02 | window_min (5-1440, default 60), limit (1-50, default 10) | top symbols by liquidation USD right now |
| `liq-heatmap` | $0.02 | symbol (default SOLUSDT), hours (1-168, default 24), buckets (5-50, default 20) | USD flushed per price zone, hottest flagged |
| `liq-history` | $0.05 | symbol (default SOLUSDT), scope (symbol/all), hours (1-168, default 24), bucket_min (5-1440, default 60) | time-bucketed liquidation history |
| `cascade` | $0.01 | window (30-300, default 90), min_events (default 4), min_usd (default 50000) | live same-side liquidation clusters on the majors |
| `cascade-scan` | $0.05 | window (30-300, default 90), min_events (default 4), min_usd (default 50000) | the same scan across every recorded perp |
| `cascade-forecast` | $0.02 | symbol (default SOL), symbols | probability of a burst in the next 15 minutes |
| `cascade-history` | $0.03 | symbol (default SOLUSDT), scope (symbol/all), hours (1-72, default 24), min_usd (default 100k), gap_s (default 60) | past flush events, up to 72h back |
| `venue-liq-share` | $0.02 | symbol (default all), hours (1-168, default 24) | liquidation share per exchange |
| `liq-pulse` | $0.005 | none | last-hour total, long/short split, top 5 symbols |
| `liq-feed` | $0.001 | symbols (up to 20, default SOL, BTC, ETH, XRP, DOGE), since (ms, up to 24 h back), next (cursor) | 5-second buckets per symbol of long and short USD liquidated across venues, dominant side and pressure against the symbol's own baseline |

### Funding, open interest, positioning and signals (21)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `signal-board` | $0.01 | n (1-60, default 30), coins | Hyperliquid market in one table, ranked by OI |
| `coin-signal/{coin}` | $0.004 | coin* | one coin: board row, cascade odds, clusters, whales |
| `squeeze-score` | $0.10 | symbol (default SOLUSDT) | 0-100 squeeze and flush scores for a perp |
| `market-state` | $0.02 | symbol | one regime read with flags and their thresholds |
| `funding-rate` | $0.005 | symbol | funding for a Hyperliquid perp, 8h equivalent |
| `funding-radar` | $0.02 | top (1-100, default 20), min_oi_usd (default 10000000) | every Hyperliquid perp with a 30-day funding z-score |
| `funding-extremes` | $0.02 | limit (1-25, default 10), min_turnover_usd (default 1M) | most positive and most negative funding |
| `funding-history` | $0.005 | symbol (default SOLUSDT), limit (1-200, default 30) | hourly funding settlements |
| `funding-pulse` | $0.005 | none | the 5 largest absolute funding rates now |
| `open-interest` | $0.01 | symbol (default SOLUSDT) | OI in USD with 1h and 24h change |
| `oi-spike-scan` | $0.02 | limit (1-25, default 10) | perps whose OI moved abnormally in the last hour |
| `positioning` | $0.005 | none | SOL and BTC OI and top-250 net-long share |
| `hl-whales` | $0.02 | coin, top (1-50, default 20) | largest Hyperliquid accounts' positions per coin |
| `trade-context` | $0.01 | none | prices, funding, positioning, liquidations in one call |
| `basis` | $0.01 | symbol (default SOLUSDT) | perp mark against the Hyperliquid oracle |
| `volatility` | $0.01 | symbol (default SOLUSDT) | 7d and 30d realized volatility |
| `top-movers` | $0.01 | limit (1-25, default 10), min_turnover_usd (default 1M) | 24h gainers and losers with funding |
| `orderbook-imbalance` | $0.01 | symbol (default SOLUSDT), bps (5-500, default 50) | bid and ask liquidity within N bps of mid |
| `orderbook-walls` | $0.01 | symbol (default SOLUSDT), top (1-15, default 5) | largest resting orders per side |
| `perp` | $0.005 | symbol (default SOLUSDT) | one perp: funding, OI, 24h liquidations |
| `market-snapshot` | $0.005 | none | SOL and BTC spot, funding, OI, Fear and Greed |

### Spot prices (4)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `price` | $0.001 | symbol (default SOL) | on-chain DEX price for SOL, BTC or ETH |
| `sol-price` | $0.001 | none | SOL price, median of the two deepest pools |
| `btc-price` | $0.001 | none | BTC price, median of three Uniswap V3 reads |
| `eth-price` | $0.001 | none | ETH price from two Uniswap V3 pools |

### Solana pre-trade checks and wallet data (11)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `sol-token-check/{mint}` | $0.025 | mint* | pre-trade check: authorities, holders, depth, verdict |
| `sol-token-flow/{mint}` | $0.008 | mint*, swaps (20-100, default 50) | who trades it: unique traders, bundles |
| `sol-holder-clusters/{mint}` | $0.008 | mint* | top-20 holders grouped by first funder |
| `token-risk/{mint}` | $0.01 | mint* | authorities, holder concentration, risk flags |
| `token-holders/{mint}` | $0.02 | mint* | top holders and concentration |
| `token-metadata/{mint}` | $0.005 | mint* | name, supply, authorities, mutability |
| `wallet-holdings/{wallet}` | $0.008 | wallet* | SOL, SPL tokens and NFT count |
| `wallet-activity/{wallet}` | $0.02 | wallet*, limit (1-25, default 10) | recent transactions with balance changes |
| `priority-fees` | $0.005 | none | fee percentiles and a recommended level |
| `jito-tips` | $0.005 | none | tip percentiles with a landing recommendation |
| `sol-network` | $0.005 | none | TPS, slot and epoch progress |

### Base chain and honeypot checks (4)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `base-gas` | $0.005 | none | gas price in gwei and wei |
| `base-balance` | $0.005 | address*, token, chain | ERC20 or native balance on Base or Ethereum |
| `base-launches` | $0.02 | min_liq_usd (default 1000), limit (1-100, default 20) | new pools on Base in the last 24h |
| `honeypot-check` | $0.01 | token*, chain | buy-then-sell simulation on Base, BNB Chain, Ethereum |

### Tokenized stocks, tradfi perps, macro and FX (9)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `peg-deviation` | $0.02 | symbol*, hours (1-168, default 24) | tokenized stock against its underlying, in bps |
| `peg-sessions` | $0.03 | symbol*, days (1-30, default 7) | peg deviation by trading session |
| `peg-universe` | $0.05 | days (1-30, default 7), min_liquidity_usd | tokenized stocks ranked by off-hours peg risk |
| `exit-quote` | $0.02 | symbol*, size_usd | what a liquidator realises selling a Kamino reserve |
| `equity-24h` | $0.01 | symbol* | indicative weekend price of a US stock or index |
| `tradfi-radar` | $0.02 | class (default all), top (1-200, default 25), min_oi_usd (default 0) | stock, index, commodity, FX perps ranked by funding |
| `tradfi-perps` | $0.005 | symbol | 24/7 HIP-3 perp prices for stocks, gold, FX |
| `macro-calendar` | $0.005 | type (default all), days (1-400, default 90) | FOMC, CPI, NFP, PCE dates in UTC |
| `fx-rates` | $0.002 | base (default EUR) | ECB reference rates, about 30 currencies |

### Filings and documents (5)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `sec-filings` | $0.005 | ticker*, form, limit (1-50, default 10) | latest EDGAR filings for a ticker |
| `insider-trades` | $0.01 | ticker*, days (1-180, default 30) | Form 4 insider transactions |
| `sec-8k` | $0.01 | hours (1-72, default 24) | 8-K filings across the market |
| `web-markdown` | $0.005 | url* | a web page as markdown |
| `pdf-markdown` | $0.01 | url* | a PDF as markdown |

### Research and compliance (6)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `sanctions-check/{address}` | $0.008 | address* | exact OFAC SDN match; no match is not a clearance |
| `papers` | $0.015 | q*, year_from, limit (1-25, default 10) | OpenAlex scholarly search |
| `paper/{doi}` | $0.005 | doi* | one paper by DOI, with abstract |
| `wiki` | $0.005 | title*, lang (default en) | Wikipedia summary and lead section |
| `email-verify` | $0.005 | email* | syntax, MX, disposable and role checks, no SMTP |
| `domain/{domain}` | $0.005 | domain* | DNS records and TLS certificate facts |

### Utilities (4)

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `hash` | $0.005 | alg* (sha256/keccak256/blake2b), data*, as (utf8/hex) | SHA-256, Keccak-256 or BLAKE2b-512 |
| `qr` | $0.005 | data*, format (svg/png) | QR code as SVG or PNG |
| `time` | $0.005 | tz (default UTC), at (default now) | time in any IANA zone, DST-aware |
| `convert` | $0.005 | value*, from*, to* | exact unit conversion |

### Fixed-purpose language tasks (7)

Content in, never a prompt or model. Answers 451 before any payment where the model API behind them is not offered.

| Route | Price | Parameters | Returns |
|---|---|---|---|
| `ocr` | $0.04 | url* | text in an image |
| `summarize` | $0.02 | url*, length (short/medium) | summary of a page or PDF |
| `extract` | $0.025 | url*, schema* | named fields from a page or PDF, null if absent |
| `translate` | $0.04 | to*, text* | translation of up to 4,000 characters |
| `classify` | $0.005 | text*, labels* | a score per label you supply |
| `injection-check` | $0.004 | text* | no_injection_found, suspicious or malicious |
| `transcribe` | $0.02 | url* | audio to text with timed segments |

Examples:

```
https://x402.ochinimus.app/api/liquidations?symbol=SOLUSDT&limit=25
https://x402.ochinimus.app/api/cascade-forecast?symbols=SOL,BTC,ETH
https://x402.ochinimus.app/api/signal-board?n=10
https://x402.ochinimus.app/api/coin-signal/SOL
```

Every paid 200 is `{ "tool": "<name>", "data": { ... }, "paid": true }`. A malformed parameter, or a
symbol the route does not serve, returns 400 and is not charged (an unsupported symbol also carries
`"supported"`). A source that failed, is stale or has no history yet returns 503 with `Retry-After` and
is not charged. Only where the decline is the product (squeeze-score on a coin whose inputs do not
resolve) does a supported symbol return 200 with a `decline` field. The seven language routes (ocr,
summarize, extract, translate, classify, injection-check, transcribe) answer 451 before any payment where
the model API behind them is not offered: do not promise them for every location. A withdrawn route
answers 410 with the closest live routes.

## Free routes: try these first

- `GET /api/sample/<route>`: a real captured response, price and input schema for a paid route (for example `/api/sample/liq-heatmap`); `GET /api/sample` lists them. Show the user what they would get before paying.
- `GET /api/last-liquidation`: the last liquidation on each major, delayed 15 minutes.
- `GET /api/forecast-record`: the settled track record of the cascade forecast. Pass a full perp symbol such as `symbol=SOLUSDT`; the alias `SOL` returns an empty summary.
- `GET /api/fear-greed` and `GET /api/exit-method` are free too, and so is `GET /api/keys/balance` (with a prepaid key). `GET /openapi.json` lists the 83 paid data routes, 7 free routes and 7 prepaid key routes.

## How to pay (x402 v2)

1. Send the GET with no payment. The route answers **HTTP 402**. The payment
   challenge is base64 JSON in the **`PAYMENT-REQUIRED` response header**, not in
   the body. A HEAD request returns the same header with no body:

   ```bash
   curl -sI 'https://x402.ochinimus.app/api/funding-radar?top=10' \
     | grep -i '^payment-required:' | cut -d' ' -f2 | tr -d '\r' | base64 -d
   ```

2. The decoded challenge has an `accepts` array, one entry per payment option, each
   with `scheme`, `network`, `amount` (atomic units of the token, 6 decimals, so
   `20000` = $0.02), `asset` (the token) and `payTo`. The per-call options use
   `scheme` `exact`, in USDC, on 9 networks that are in every 402:
   - Solana mainnet `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`
   - Base `eip155:8453`
   - Polygon `eip155:137`
   - Arbitrum `eip155:42161`
   - Arc `eip155:5042`
   - Algorand mainnet `algorand:wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=`
   - Optimism `eip155:10`
   - Monad `eip155:143`
   - Avalanche `eip155:43114`

   11 more networks are on request. Ask with `GET /api/<route>|<network>` (`<network>` is
   the CAIP-2 id; the `|` may be sent as `%7C`, for example `/api/sol-price|eip155:42220`)
   and the 402 carries that network too; a payment on any of them is accepted on the plain
   URL as well. They are Celo `eip155:42220`, HyperEVM `eip155:999`, Unichain `eip155:130`,
   Scroll `eip155:534352`, SKALE Base `eip155:1187947933` (USDC.e), BNB Chain `eip155:56`
   (AUSD), Ethereum `eip155:1`, Robinhood Chain `eip155:4663` (USDG), World Chain
   `eip155:480`, and on routes priced $0.005 or more also Sei `eip155:1329` and X Layer
   `eip155:196`. The token is USDC unless named: read `asset` in the option before signing.
   That is 20 x402 networks, 21 chains with MPP on Tempo.

   Our proof payments settled on Optimism https://optimism.blockscout.com/tx/0xdc642dc7c4c3e96fa59e0704737adce62693e69cd534961676e43501ff55d4c5, Monad https://monadscan.com/tx/0xdf06372e33166459c41944703f536b4e551c136e483d0366664f38a9f004da2d and Avalanche https://snowscan.xyz/tx/0x5c3ee5c2d858732abca327500e761e0977807a53a4de0f44d4cd57ddc14d70d0.

   The same challenge also offers the call at half price (minimum $0.0005), for
   clients that support it: `batch-settlement` vouchers on Base, Polygon and Arbitrum, and Circle
   Gateway nanopayments (`exact` with `extra.name` `GatewayWalletBatched`) on
   Base, Polygon, Arbitrum and Arc. Both need a deposit first; an ordinary x402 client should pick a
   per-call `exact` option. Every paid route also answers with an MPP tempo/charge
   challenge in `WWW-Authenticate`, for clients that speak MPP; `/api/sol-price` and `/api/btc-price`
   also offer MPP solana/charge.
3. Sign one accepted option with an x402 v2 client and repeat the same GET with
   the signed payload in the **`PAYMENT-SIGNATURE`** request header. An x402 v1
   client may instead read the challenge from the JSON body and pay with
   `X-PAYMENT`, on Solana or Base only.
4. A settled call returns 200 with the data. If payment did not settle you get a
   fresh 402.

OpenClaw has no built-in x402 wallet. Payment needs an x402 v2 client the user
has already set up and funded, for example the Coinbase Agentic Wallet CLI
(`awal x402 pay <url> --max-amount <atomic units>`, USDC on Base) or the
`@x402/fetch` library with a Solana or EVM signer. This skill never asks for a
private key and never installs a wallet.

### Spending rules

- Get the user's approval before the first paid call in a session and tell them the price from the table.
- Set a maximum per call no higher than the listed price (for example `--max-amount 20000` for a $0.02 route).
- If the decoded `amount` is higher than the tables above, stop and ask the user.
- Prefer one batched call (`cascade-forecast?symbols=SOL,BTC,ETH`) over several single calls.

### Copy payTo only from a fresh 402

**Take `payTo` only from the 402 challenge you just received, never from
transaction history, an old response, or a block explorer.** Lookalikes of the
AgentFeed treasury address have sent address-poisoning transfers to its buyers.
The fresh challenge should show `4a8o45skRPcyjAdyR8yES215Swvh8uTpZD6KLarhxCJ7`
on Solana, `0x22DB3A9686EE5261e7Bf3ed4f91277232E8076e6` on every EVM network above except Arc
(per-call and batch-settlement), `0x0Cf44185564F2b72E291050DC79E578429E52f83` on Arc,
`QWOWU2E6BB76HEQRRMXWZ2MU4HAQIYZWEPP2W7Y377ZRDIW7ZKD4MMMEPM` on Algorand, and
`0xA853129ACF56A851f9d51CD8cb47619465260Fa9` for Circle Gateway. If it shows
anything else, do not pay and tell the user.

## Prepaid API keys (for bots that cannot pay x402)

A bot that can set an HTTP header but cannot sign an x402 payment (n8n, Freqtrade, Hummingbot, a script,
a gateway) buys a key once and spends it per call. The key packs are purchase routes, not data routes, and
are not counted in the 83 above.

- Buy once with any x402 client, or at https://x402.ochinimus.app/keys with a Base wallet (the page sends AgentFeed only the key's hash), on a per-call `exact` rail only (no half-price option): `/api/keys/buy-trial` ($0.25), `buy-1` ($1), `buy-5` ($5), `buy-20` ($20). Top up with `topup-5` ($5) or `topup-20` ($20), sending the key as the header.
- The purchase returns the key (`afk_...`) once. Or make your own, `afk_` plus base58 of 32 random bytes, and buy with `?key_hash=<sha256 hex of the key>&prefix=<the 8 characters after afk_>`: the server never sees the key.
- Spend with `X-AgentFeed-Key: afk_...` (or `Authorization: Bearer afk_...`) on any paid GET: each call draws half the route price, minimum $0.0005; a 400, 404, 500 or 503 is never drawn; 120 requests a minute per key. `GET /api/keys/balance` with the header is free (`balance_usd`, `calls`, `spent_usd`, `status`).
- The bot pass: `/api/keys/buy-pass` ($25, per-call `exact` only) returns a key that works for 30 days from the moment the payment settles, and only on `liq-feed` and the MCP tool `get_liq_feed`. Nothing is drawn per call. The 10 second limit and 120 requests a minute still apply, every other route answers 403, and a pass cannot be topped up.
- The balance is usage credit, non-refundable, no expiry. The key is a bearer secret: keep it out of chats and logs; abuse means revocation. Buying a key is a payment: tell the user the pack price and get their approval first.

```bash
curl -s 'https://x402.ochinimus.app/api/signal-board?n=10' -H 'X-AgentFeed-Key: afk_...'
```

## Reading the answers

- `liquidations`: `event` is `long_liquidated` (forced sell) or `short_liquidated` (forced buy).
- `liq-feed`: each row is a 5-second bucket for one symbol with `longs` and `shorts` (USD, quantity and vwap, rounded), the `dominant` side and `pressure` against that symbol's own baseline. Pass `next` from the last answer to continue without gaps. A bucket is served once it is 10 seconds old, and the limit is one call per 10 seconds (a 429 carries Retry-After).
- `liq-heatmap`: `hottest_zone` marks historical flush zones, not estimated liquidation levels of open positions.
- `cascade-forecast`: `p` is a probability against the symbol's own 90th-percentile window, not a price call. Report `support`, and say so when `evidence` is weak or the answer declines.
- `market-state`, `signal-board`, `coin-signal`: report `flags` with their rules; a flag is a threshold crossing, not a prediction. Every source carries its `as_of`.
- `funding-radar`: a high positive `z_30d` means longs pay unusually much against that perp's own month; a new perp has no z-score yet (see `z_note`); rates are shown at their 8h equivalent.
- `sanctions-check`: an exact OFAC SDN match only; no match is not a clearance. `sol-token-check`: report the verdict with its rules. `extract`: null means not stated, never fill it in.

None of this is trading advice. Present the data and its limits; leave the
decision to the user.

## More

- Route list: https://x402.ochinimus.app/openapi.json (83 paid data routes, 7 free); agent guide: https://x402.ochinimus.app/SKILL.md and /llms.txt
- MCP server with the same data tools: `POST https://x402.ochinimus.app/mcp` (streamable HTTP); the prepaid key routes are HTTP only
- Source and issues: https://github.com/seekdaseek/agentfeed
