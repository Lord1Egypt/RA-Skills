---
name: ad-market-map
description: Map who advertises on Facebook and Instagram for a keyword or niche in a country - the advertisers, how many ads each runs, who is ramping up, and the offers and angles that dominate the category - from the Meta Ad Library via SocialAPIs. Use when the user is entering a market, sizing competition, looking for competitors they don't know about, or wants to see how a whole category advertises.
---

# Ad market map

One brand's ads tell you about that brand. A keyword's ads tell you about the market: who is spending, how crowded it is, and which promise everyone makes (so you can make a different one).

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `facebook_ads`.

## Ask first (only what's missing)

- 1 to 3 keywords describing the category ("meal prep delivery", "dog insurance"). Suggest close variants if one keyword returns little.
- Country (ISO code). Offer to compare 2 countries.
- Anything to exclude (the user's own brand, marketplaces, news pages).

## Budget

1 credit per call. Per keyword and country: 1 to 2 for advertisers + 3 to 5 pages of ads + up to 5 archive details. About 10 credits; say the total if several keywords or countries.

## Steps

1. **Advertisers.** `/facebook/ads/keywords?query=<kw>&country=<cc>` gives pages with `page_id` and `ad_count`. Keep the top 15 to 20 by ad count.
2. **Ads in the category.** `/facebook/ads/search?query=<kw>&country=<cc>&activeStatus=Active&sort_data=impressions`, 3 to 5 pages via `end_cursor`. Then the same with `sort_data=recent` for 1 to 2 pages to catch newcomers.
3. **Per advertiser** (from the ads collected): active ads seen, oldest `start_date` (how long they've been in the market), ads started in the last 30 days (momentum), platforms.
4. **Classify each advertiser**: direct competitor, adjacent (sells something related), aggregator / marketplace, publisher / affiliate. Use page name and ad text; mark "unsure" instead of guessing.
5. **Category messaging.** Across all ad texts, count recurring themes: price / discount, speed, quality, guarantee, social proof, fear / problem, identity / lifestyle, free trial. Note the most common CTA types.
6. Open 3 to 5 of the highest-impression ads with `/facebook/ads/archive-details` for the full creative and, where published, spend and impression ranges.

## Output

```
## "<keyword>" ads in <country>, <date>

Crowdedness: <n> advertisers with active ads; top 5 run <x>% of the ads seen.

| Advertiser | Type | Active ads | In market since | New in last 30d | Platforms |
|---|---|---|---|---|---|

### Rising (most new ads in 30 days)
<2 to 4 names, one line each>

### What everyone says
| Theme | Share of ads | Example hook |

### White space
2 to 4 angles few or no advertisers use, and why they could work for the user.
```

## Limits

- Keyword search matches ad text, so it misses ads that never use the word, and can include unrelated ads. Mention both.
- Counts are from the ads this run collected, not Meta's full totals (use `/facebook/ads/page-details` for an advertiser's total).
- No performance data; "rising" means "launching ads", not "winning".
