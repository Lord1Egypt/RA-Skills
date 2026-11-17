---
name: casino-game-research
description: Research public casino game catalogs and source-published game descriptions from FanDuel and DraftKings. Use for game-category or feature lookups, not wagering strategy or recommendations.
---

# Casino game research

Answer informational questions about publicly listed games, categories, and
published game attributes using the FanDuel and DraftKings catalog surfaces.
Use scripts/crawlora.sh or the named Crawlora tools and the generated endpoint
reference for exact methods and parameters.

## Find games and read their attributes

- Start with FanDuel's category directory and select a supported lobby region
  (mi or on) when the user has a market in mind. Region selects which public
  catalog is read; it does not establish that a person is eligible to play.
- Use a returned category slug to list games, then a returned game slug for
  detail. Keep provider name, region, studio, category, badge, and observation
  time attached to each record.
- FanDuel's detail page may report minimum/maximum bet, volatility, themes,
  features, or concurrent players. Treat these as source-reported attributes;
  volatility is not a probability or a forecast of a result.
- DraftKings' public endpoints expose slot categories and selected written
  guides. They do not provide a complete game catalog, image-only payout tables,
  promotions, jackpots, or account-specific access. Report those limits instead
  of filling gaps from another source.

Do not recommend a game, betting amount, strategy, or expected return. Keep the
answer to source-listed categories and descriptive attributes.

~~~sh
scripts/crawlora.sh /draftkings/casino/slots/categories
scripts/crawlora.sh /draftkings/casino/slots-guide
scripts/crawlora.sh /fanduel/casino/categories region=mi
scripts/crawlora.sh /fanduel/casino/category category=slots region=mi
# Use a returned game slug for the detail page:
# scripts/crawlora.sh /fanduel/casino/game game=GAME_SLUG_FROM_CATEGORY region=mi
~~~
