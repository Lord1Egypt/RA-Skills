---
name: ecommerce-competitor-price-monitor
description: Analyze competitor ecommerce price history through Glasser. Match exact Amazon product variants, detect abnormal price increases and decreases, measure their dates and observed duration, explain the surrounding pattern, and optionally compare current merchant offers or propose monitoring thresholds. Use for historical pricing, promotions, repricing signals, and competitor price monitoring.
metadata:
  version: "0.1.0"
  category: research
---

# Ecommerce competitor price monitor

This skill requires Glasser — one Key across many paid data providers. Install it first: https://glasser.ai/SKILL.md?utm_source=clawhub covers installation and use.

Use Glasser for all data acquisition here. Reach for another tool only when the Glasser catalog has no endpoint for what is needed.

## Purpose

Start with **historical pricing** when the user asks when a competitor raised or cut prices, how long a change lasted, or whether it was unusual. Use the Glasser skill for fresh catalog search, endpoint inspection, pricing, spending controls, runs, and charge reporting. Current shopping snapshots and alerts are secondary paths.

## Define one comparable product

Get the market, exact product or ASIN, variant attributes (size, color, pack count, condition), requested lookback period, and the price basis of interest. Default to one market, one verified product variant, a 180-day history, and Amazon's retail price if available. A competing model or color is a **separate series**. If the user supplies only a product name or URL, resolve the ASIN with a small Amazon product search, then check the history response's ASIN, title, brand, size, and color before analysis. Stop or label uncertainty when identity is ambiguous. Do not attach a near-match ASIN's history to the user's item.

## Process: get the history

1. Search Glasser's current catalog for a product history endpoint, inspect its input schema, price, charge exceptions, and run mode, then state the expected cost and number of calls before paid collection. Use the user's existing authorization or budget cap; do not repeat an approval already granted. Start with one ASIN and do not perform bulk or speculative calls.
2. For Keepa `/product`, request history for the verified ASIN and marketplace. Keep the raw Run JSON and a source link. Confirm the returned product again. Prefer `csv[0]` (`AMAZON`) for Amazon's retail price; if unavailable and relevant, analyze `csv[1]` (`NEW`) as marketplace lowest new offer, labeled separately. Never mix `AMAZON`, `NEW`, `LISTPRICE`, and Buy Box. `NEW` changed from lowest listing price to lowest landed price on 2026-02-23; do not calculate one continuous baseline across that date. Buy Box/shipping history can require a different endpoint or extra input and cost; inspect before requesting it.
3. Decode the selected Keepa series according to [Keepa's product history specification](https://keepa.com/api-docs/product-object.html): alternating Keepa-time minutes and price in the marketplace's smallest currency unit. Convert timestamps to UTC; `-1` is unavailable, not a price. Keepa appends history points when the value changes. Verify that the requested history and observation date cover the claimed period. Do not assume coupons, tax, final checkout price, seller intent, or stock details from a price series alone.

## Detect and interpret changes

Build time intervals between consecutive price events, and explicitly exclude unavailable intervals. For an initial screen, compare each price run against the **time-weighted median of available prices in the preceding 30 calendar days**. Flag a candidate only when its change is at least 15% **and** at least $3 (or a suitable local-currency threshold), with at least 24 cumulative hours at the new available price. Group tiny price differences (up to $0.05 for USD) into one run; a gap of more than 48 hours of unavailable prices breaks the run. State thresholds in the report and adapt them when the product category or user request calls for it. This screen is a heuristic, not proof of a promotion or an error.

For each candidate report:

- First observation at the new price; next different observed price or retrieval time; calendar span and cumulative hours with an available offer. If the episode is still open at retrieval, say so. Never call a low-price episode continuous when unavailable gaps occur.
- Before/after price, amount and percentage versus both the prior 30-day median **and** the immediately preceding available price when they differ; whether and when the price reverted. Use decimal arithmetic and one fixed price type.
- Context: earlier baseline, subsequent recovery or new level, repeat events, unavailable periods, sparse or stale history, and plausible explanations as hypotheses only. Distinguish a short spike, sustained reset, and possible discount. Avoid attributing a change to a sale, algorithm, or competitor reaction without corroboration.

Compute candidate episodes with deterministic arithmetic and review them against the raw timeline before reporting. Do not join `NEW` windows across the 2026-02-23 definition change. If the selected series is sparse or unavailable, report that limit rather than manufacture a trend.

## Optional current snapshot and monitoring

When the user also wants today's merchant comparison, search and inspect a current shopping endpoint. Match exact variants and conditions; save retrieval time, seller, listing URL, currency, displayed price, shipping/tax/coupon/stock fields, and link type. Classify results as verified exact, provisional, or excluded. Google Shopping result links are search listings, not verified merchant checkout pages. Exclude accessories, multipacks, suspicious placeholders, and mismatched sizes. Do not trigger a price alert from a provisional match.

For repeated checks, compare the same ASIN or exact merchant SKU, market, currency, and price basis with a saved baseline. A missing offer or different seller is not a price cut. Report a suggested cadence, threshold, and expected per-run spend when the user asks for monitoring; this research skill does not create automations or change store prices.

## Deliverable

Lead with a dated price-history table: event, price, benchmark, start/end, calendar span, available-price duration, and caveats. Follow with a short approximate interpretation and a price timeline or saved machine-readable analysis when useful. Include the exact product identity, marketplace, series type, thresholds, missing periods, and latest observed price. Label any present-tense price from a separate shopping source rather than treating Keepa history as a checked checkout quote.

Report every Glasser Run's actual charge, status, provider response, and Run URL. If a paid Run yielded no usable history, include that outcome and its charge. Do not claim historical prices for other merchants from one Amazon ASIN's series.
