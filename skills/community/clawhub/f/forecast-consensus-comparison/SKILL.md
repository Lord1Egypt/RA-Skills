---
name: forecast-consensus-comparison
description: Compare public event forecasts across Crawlora Polymarket, Kalshi, and Metaculus tools. Use for a matched-question consensus brief or dated forecast divergence analysis with resolution rules, outcome labels, scales, timestamps, liquidity, and method differences preserved.
---

# Forecast consensus comparison

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound calls/pages by the requested scope and credit budget. Retain
source IDs, URLs, source dates, and observation/crawl times separately.

Compare source-attributed forecasts for the same precisely defined question.
Establish event, outcome, jurisdiction, time horizon, cutoff, and desired sources.
Keep a match rubric before interpreting a gap between prices or community forecasts.

## Verify the proposition before comparing numbers

- Discover candidates through each source's search/list routes, then fetch event,
  market, or question detail. Compare exact wording, thresholds, geography, time
  zone/deadline, resolution source/rules, settlement status, and conditional scope.
  Similar titles are leads; markets using different conditions remain separate.
- Preserve Polymarket event slugs, market IDs, and outcome token IDs separately.
  Use the token belonging to the matched outcome, not an event/condition ID in a
  token route. Kalshi market tickers differ from event and series tickers; history
  parameters must follow that source's metadata, not a synthesized name.
- For Metaculus inspect question metadata/type, option labels/history, scaling,
  and resolution information when available before interpreting aggregates.
  Multiple-choice option arrays require label/index alignment. Numeric/date
  question centers and the first array component are not automatically a binary
  probability; if a necessary scale is missing, keep that source uncomparable.
- Retain each source's observation time and forecast aggregation method/count.
  `recency_weighted`, `unweighted`, and `single_aggregation` describe different
  summaries. Forecast centers/bounds are not sportsbook prices or universally
  interpretable confidence intervals.

```sh
scripts/crawlora.sh /polymarket/search q="interest rates" status=open limit=5
scripts/crawlora.sh /kalshi/markets status=open limit=5
scripts/crawlora.sh /metaculus/questions limit=5
# Resolve matched market/question IDs and actual outcome labels before detail.
```

## Report comparable snapshots and history

Record whether a market value is last trade, outcome quote, bid, ask, or midpoint,
plus spread/liquidity when provided. Verify price scale from the returned fields;
do not universally divide by 100, treat a stale last trade as an executable price,
or call a market quote a calibrated probability. Normalize only genuinely
matching binary outcomes to a declared common scale.

Show numerical divergence in percentage points only when outcome, scale, timing,
and rules match. Keep uncomparable rows and the failed match condition visible.
Do not average sources into a universal consensus or label a gap an arbitrage
opportunity without accounting for rule, liquidity, fee, and execution differences.
Public forecast questions can have participation/selection bias distinct from markets.

History requests are bounded/capped and use different source timestamps and
sampling intervals. Align actual returned times rather than filling missing data
with zero or claiming a price response proves a news event caused the movement.
Return a proposition-match table, dated source snapshots/history, selected
method/price basis, divergence calculations, and uncertainty. No trading, account,
wallet, order, or automated monitoring actions are part of a comparison request.
