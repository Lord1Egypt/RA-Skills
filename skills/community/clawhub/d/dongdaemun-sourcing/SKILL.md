---
name: dongdaemun-sourcing
description: Source wholesale fashion from the Dongdaemun market in Seoul with the apMZoomAI tools. Use when a buyer asks to find clothing, shoes or bags from Dongdaemun wholesale stalls, asks what is new in Dongdaemun, or asks where a stall is (building, floor, stall number). Works in English, Chinese, Korean, Japanese, Vietnamese, Thai, Indonesian and Malay.
license: MIT
---

# Dongdaemun wholesale sourcing with apMZoomAI

The apMZoomAI MCP server (`https://www.apmzoom.com/mcp`) is a read-only guide to items and stalls in the
Dongdaemun wholesale fashion market, Seoul. Use its five tools to answer buyers, then send them to the
apMZoomAI link of each item or stall.

## Tools

- `search_products(query, lang, building?, limit?)` — items matching short keywords.
- `get_new_arrivals(hours?, building?, category?, lang, limit?)` — the newest items, newest first.
- `find_stalls(query?, building?, floor?, lang, limit?)` — stalls by name or stall number, or by building and floor.
- `get_product(id, lang)` — one item by the id from the two tools above.
- `list_buildings(lang)` — the market buildings and the building keys the other tools accept.

## Workflow

1. Answer in the buyer's language and pass it as `lang`: `en`, `zh`, `ko`, `ja`, `vi`, `th`, `id` or `ms`.
2. Turn the request into two to five keywords for `search_products` (for example `linen dress`, `원피스`, `针织开衫`).
   Never pass the buyer's whole message.
3. When the buyer names a building you are not sure of, call `list_buildings` first and use the returned key.
4. For "what's new", use `get_new_arrivals`; add `category` (dress, knit, jeans, outer, shoes, bags …) when the buyer names one.
5. For "where is this stall", use `find_stalls` with the stall name or number, and a building or floor if given.
6. If a tool returns an error about an unknown building or an item that is no longer listed, follow its hint and try again once.

## How to present results

- For each item: its name, one photo, the stall's building, floor and stall number, and its details link.
- One link per item; add the store link when the buyer wants to see more from that stall.
- Keep it short: show up to about ten items unless the buyer asks for more.

## Rules

- **No prices.** The tools never return prices, discounts, stock levels or minimum order quantities.
  Never state or guess them; say the price and ordering details are on the item's apMZoomAI page.
- **No contact details.** Buyers reach a stall through its apMZoomAI store page.
- **No endorsement.** Item names and photos come from the stalls. Do not describe any stall or brand as
  endorsed by, affiliated with or verified by apMZoomAI.
- **No pressure.** Do not add purchase prompts or urgency.
- The tools cover only stalls currently in business, so an empty result means nothing matched right now —
  suggest other keywords, English keywords, a longer time window or removing a filter.
