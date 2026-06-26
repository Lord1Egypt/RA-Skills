---
name: epic-games
description: Fetch current and upcoming free games from Epic Games Store. Use when the user asks about Epic free games, this week's free games, or Epic giveaways.
---

# Epic Free Games

## API

No auth required. GET request:

```
https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale={locale}&country={country}&allowCountries={country}
```

Parameters (match user's language/region, default to `zh-CN` / `US`):
- `locale`: BCP 47 format (e.g. `zh-CN`, `en-US`, `ja-JP`, `ko-KR`)
- `country` / `allowCountries`: ISO 3166-1 alpha-2 (e.g. `US`, `CN`, `JP`, `KR`)

Note: Some regions have restricted catalogs. Use `US` for the most complete game list.

## Steps

1. Fetch the API using `curl` (the response is large, `web_fetch` may truncate it)
2. Parse `data.Catalog.searchStore.elements` from the JSON response
3. Distinguish current vs upcoming by `promotions` field:
   - `promotions.promotionalOffers` has value → **currently free**
   - `promotions.upcomingPromotionalOffers` has value → **upcoming free**
4. Each promotion contains `startDate` and `endDate` (UTC ISO 8601)
5. Ignore entries where `offerType` is not `BASE_GAME` (DLCs, add-ons, etc.)

## Output Format

Group by "currently free" and "upcoming free", show game title, store link, and claim period (converted to local timezone). Date format: match the user's locale.

Store link: `https://store.epicgames.com/{locale}/p/{pageSlug}` where `pageSlug` is from `offerMappings[0].pageSlug`.
