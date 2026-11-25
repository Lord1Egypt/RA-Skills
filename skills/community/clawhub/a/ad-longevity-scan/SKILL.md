---
name: ad-longevity-scan
description: Find which of a brand's Facebook and Instagram ads are working by how long they've been running, what it launched recently, and which messages it keeps testing, from the Meta Ad Library via SocialAPIs. Use when the user asks what ads a competitor runs, which of their ads perform, what offers or hooks they use, or wants ad ideas based on a rival's proven creatives.
---

# Ad longevity scan

Advertisers switch off ads that lose money. An ad that has been live for months is one the brand keeps paying for, which is the best public signal of a winner the Ad Library gives you. This skill ranks a brand's ads by that signal and reads what the long runners have in common.

Needs `SOCIALAPIS_API_KEY`. Auth, parameters and errors are in the `socialapis` skill ([endpoint reference](https://github.com/SocialAPIsHub/skills/blob/main/skills/socialapis/references/endpoints.md)); with the MCP server connected, use `facebook_ads`.

## Ask first (only what's missing)

- The brand (Facebook page URL, or name).
- Country (ISO code, or ALL). Ads differ a lot by country.
- What the user wants from it: ideas for their own ads, a competitor report, or a check on one product line.

## Budget

1 credit per call. Typical: 1 to 2 to find the advertiser + 3 to 6 pages of ads + 3 to 8 archive details for the top ads. About 8 to 15 credits.

## Steps

1. **Find the advertiser's ad page id.**
   - Have the page URL: `/facebook/pages/details?link=…` and read `ad_page_id`.
   - Only a name: `/facebook/ads/keywords?query=<brand>&country=<cc>` and pick the matching page by name and ad count. Confirm with the user if two look alike.
2. Optional: `/facebook/ads/page-details?page_id=<id>` for verification status and total ad count.
3. **Pull active ads.** `/facebook/ads/search?ad_page_id=<id>&country=<cc>&activeStatus=Active&sort_data=recent`, following `end_cursor` to collect up to about 100 ads (stop early if the advertiser has fewer).
4. **Days live** = today minus `start_date` for each active ad. Bucket them:
   - **Proven:** live 60+ days
   - **Promising:** 21 to 59 days
   - **Testing:** under 21 days (new launches)
5. **Group near-duplicates.** Advertisers run the same creative in many variants. Group by the first ~80 characters of `ad_creative_body` plus `cta_type`. A group with many variants that has been live a long time is the strongest signal of all; report group size.
6. **Read the top 3 to 8 proven ads in full** with `/facebook/ads/archive-details?ad_archive_id=…&page_id=<id>&country=<cc>`: full text, CTA, platforms, countries, and spend / impression ranges where Meta publishes them (mostly EU and political ads; usually absent elsewhere, say so).
7. **Extract the pattern** across proven ads: the hook (first line), the offer (discount, free trial, bundle, guarantee), proof (reviews, numbers, press), CTA type, format (from snapshot), and platforms (Facebook, Instagram, Messenger, Audience Network).

## Output

```
## <Brand> ads in <country>, <date>
Active ads: <n> (<g> creative groups). Proven 60d+: <a> · Promising: <b> · Testing: <c>

### Proven winners
| Days live | Variants | Hook (first line) | Offer | CTA | Platforms | Link |

### What the winners share
- Hook pattern: …
- Offer: …
- Proof used: …

### New this month (what they're testing)
| Started | Hook | What's different from the winners |

### Ideas for you
3 to 5 concrete ad angles adapted (not copied) for the user's product, each tied to a winner above.
```

Link every ad with its `snapshot_url` so the user can see the creative.

## Limits

- Longevity is a proxy. Brand-awareness or always-on ads can run long without being great performers; mention it when a brand is very large.
- The Ad Library shows ads, not results: no clicks, conversions or (outside the EU / political ads) spend.
- Don't reproduce ad copy wholesale in the user's own ads; adapt the angle.
