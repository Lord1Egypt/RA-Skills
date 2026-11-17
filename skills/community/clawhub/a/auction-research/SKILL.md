---
name: auction-research
description: Researches Bonhams auctions and lots via the Crawlora API — upcoming and past sales, lot search, estimates, realized prices, departments, and auction detail — returning clean JSON. Use when the user wants auction-house research, comparable lots, sale calendars, or public estimate/realized-price data.
---

# Auction research

Search Bonhams' public auction and lot catalog as normalized JSON for sale
calendar research, lot comparisons, estimates, and realized prices.

## When to use this skill

- Find upcoming or past Bonhams auctions.
- Search lots across auctions by object, artist, or category.
- Inspect one auction's metadata and lot list.
- Pull one lot's estimate, realized price, department, and sale facts.

## Setup

- Get a Crawlora API key at [crawlora.net](https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills).
- Set `CRAWLORA_API_KEY` in the environment before running the helper.
- The helper reads `CRAWLORA_API_KEY` from the environment and sends requests to `https://api.crawlora.net/api/v1`.

## How it works

Use `/bonhams/auctions/search` for sale discovery and
`/bonhams/lots/search` for cross-sale lot research. Follow an auction id into
`/bonhams/auctions/{id}` and `/bonhams/auctions/{id}/lots`; use
`/bonhams/lots/{auctionId}/{lotNumber}` for full lot detail.

Full endpoint list: [`reference/endpoints.md`](reference/endpoints.md).
