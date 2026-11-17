---
name: "coin-price-median"
description: "AirnodeHub coin price skill for crypto price requests: fetch all available specialist source prices, report each value, median, and deviation from median."
---

# Coin Price Median

## Execute

1. Use this skill when the user asks for a crypto coin/token price, a pair such as `ETH/USD` or `PONS/USD`, or price comparison across sources. Extract the asset, quote currency, chain/venue preference if supplied, and whether the user wants spot price only or richer market context. Ask only when the symbol cannot be mapped safely to an asset. **Done when:** the requested asset and quote currency are clear enough to query.

2. Read `https://airnode-v2-hub.api3.org/llms.txt` or the current AirnodeHub catalogue before querying when it has not been read in this run. Identify every specialist AirnodeHub listing that can directly price the requested crypto asset or pair, such as CoinGecko, TickerLayer, Twelve Data, Nodary, Hyperliquid, dRPC historical/current price operations, or newly listed specialist price sources. Do not use broad web/news/search listings for the median unless no specialist price source exists and the user explicitly permits web search. **Done when:** the candidate specialist sources are listed with the operations likely to return a spot or latest price.

3. For each candidate source, GET the listing documentation before calling it if its schema has not been read in this run. Use only documented operation names, symbol formats, quote currencies, venues, IDs, and required parameters. Prefer exact asset IDs over tickers when a source requires IDs; resolve ambiguous symbols with a documented search/list operation or ask the user. **Done when:** each planned call is schema-valid or excluded with a reason.

4. Before any POST that is paid, metered, credentialed, quota-consuming, or has uncertain cost, state the source, operation, bounded scope, and known or unknown cost, then obtain explicit approval. Free documentation reads do not need approval. Exclude unapproved paid sources from the median and label them as skipped. **Done when:** every source is approved, free, or explicitly skipped.

5. Fetch prices with HTTP POST JSON shaped as `{"operation":"<operation>","parameters":{...}}` to each selected AirnodeHub listing. Use the smallest useful request: one asset, one quote currency, current/spot/latest price, and no broad history unless requested. Retry a source once only for corrected schema or a transient upstream error. **Done when:** all available approved sources have returned an attested price or a concrete blocker.

6. Normalize returned prices to the requested quote currency and a common numeric unit. Exclude stale, missing, zero, nonnumeric, wrong-pair, or clearly venue-specific derivative/index values unless the user requested that venue/type. If multiple values come from the same provider for the same spot concept, keep the most direct/latest one and mention the duplicates were collapsed. **Done when:** the median input set contains comparable spot prices only.

7. Calculate the median of all comparable source prices. For each included source, calculate absolute deviation and percentage deviation from the median as `(source_price - median) / median * 100`. Sort the display by price or by source name when prices are close; show skipped/error sources separately. **Done when:** median and deviations are computed from the final included set.

8. Present a compact table with source, operation or market, price, timestamp if returned, deviation from median, and verification status. Then give the median as the primary value and a one- or two-sentence read on source dispersion. Attribute all values to AirnodeHub providers. Do not give personalized buy/sell advice. **Done when:** the user can see every source value and how the median was derived.

## Verification

Before replying, confirm every included value came from a documented AirnodeHub specialist POST, the asset and quote currency match the request, paid/uncertain calls were approved or skipped, all response envelopes include `airnode`, `requestHash`, `timestamp`, `data`, and `signature`, and the deviation math is correct. Cryptographically verify signatures when tooling is available; otherwise state that the responses were signed/attested but not independently cryptographically verified.
