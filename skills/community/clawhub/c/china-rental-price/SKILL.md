---
name: china-rental-price
description: Use when the user needs a China domestic rental-car reference price, especially for same-day or holiday travel where train-station or airport store choice matters and OneHai peak-period minimum-rental rules can be mistaken for zero inventory. This skill uses the user's logged-in Google Chrome session on macOS to query OneHai, return reference prices and booking URLs, and distinguish policy restrictions from true no-car results.
---

# China Rental Price

## Overview

This skill is for China domestic self-drive rental price checks in travel-planning conversations. The currently reliable path is OneHai via the user's logged-in Google Chrome session on macOS.

## When To Use

- The user asks for a China domestic rental-car price, same-day quote, or holiday quote.
- The user wants a station or airport pickup store, not an arbitrary citywide sweep.
- The user shows a "0 cars" page and needs to know whether it is truly sold out or blocked by a peak-period minimum-rental rule.

## Preconditions

- Use absolute dates and times.
- Google Chrome must already be logged into 一嗨租车.
- Chrome must have `查看 > 开发者 > 允许 Apple 事件中的 JavaScript` enabled.
- macOS needs `osascript` and `tesseract`.

## Workflow

1. Prefer scene-based store targeting:
   - High-speed rail or train arrival: `train-station`
   - Flight arrival: `airport`
   - Only use citywide selection when the user did not specify a transit scene.
2. If the user knows the exact store, pass `--pickup-location` and `--dropoff-location`.
3. Run `scripts/query-onehai-live-chrome.mjs`.
4. Interpret the result before answering:
   - `bookingRestriction` means a policy limit such as a holiday minimum-rental rule. Do not describe it as ordinary sellout.
   - `priceMin` and `vehicleSamples` are reference prices captured at query time, not a guaranteed final checkout price.
   - `availableCars = 0` without `bookingRestriction` is the closer match to true no inventory at that store and time.

## Commands

City plus transit scene:

```bash
node /Users/shenmingjie/.codex/skills/china-rental-price/scripts/query-onehai-live-chrome.mjs \
  --pickup-city 宣城 \
  --pickup-scene train-station \
  --pickup-datetime 2026-05-01T15:30 \
  --dropoff-datetime 2026-05-04T10:30
```

Exact store:

```bash
node /Users/shenmingjie/.codex/skills/china-rental-price/scripts/query-onehai-live-chrome.mjs \
  --pickup-city 宣城 \
  --pickup-location "泾县高铁站自助点" \
  --dropoff-city 宣城 \
  --dropoff-location "泾县高铁站自助点" \
  --pickup-datetime 2026-05-01T10:00 \
  --dropoff-datetime 2026-05-04T10:00
```

## Output Shape

The script prints JSON with fields such as:

- `platform`
- `status`
- `capturedAt`
- `bookingUrl`
- `selectedStore`
- `priceMin`
- `priceTotalIfAvailable`
- `availableCars`
- `vehicleSamples`
- `bookingRestriction`
- `warnings`

## Response Guidance

- Report the selected store explicitly so the user knows whether the quote came from a train-station store, airport store, or another branch.
- Keep the wording as `参考实时价`.
- If the query is part of a broader itinerary, combine the rental result with the user's actual arrival mode instead of searching every store in the city.
- Be transparent that the reliable automated path in this skill is currently OneHai.
