---
name: ad-library-research
description: Research any brand's live ads for free with the public ad libraries (Meta, Google, TikTok, LinkedIn, Snap) and turn what you find into hooks and angles.
license: MIT
---

# Ad-library research (no account needed)

Every major platform publishes the ads running on it as an official transparency tool, for exactly this kind of research. This skill is the map: where each library is, what it can
filter, what it hides, and how to turn a pile of ads into something a marketer can use.

## Where to look
| Library | URL pattern | What it shows | Limits |
|---|---|---|---|
| Meta Ad Library (Facebook, Instagram, Messenger, Threads) | `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=<brand or keyword>&search_type=keyword_unordered` | creative, copy, start date, platforms; EU results add reach and targeting | no spend for non-political ads; "active" vs "all" matters, because the longest-running ads are the proven winners |
| Google Ads Transparency Center | `https://adstransparency.google.com/?region=US&domain=<brand.com>` | Search, Display, YouTube creatives by advertiser or domain, with first/last-shown dates | no copy for many Search ads unless you open each; filter by format |
| TikTok Creative Center (Top Ads) | `https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en` | top-performing TikTok ads by region, industry, objective, with likes and CTR proxies | curated sample, not the whole library |
| TikTok Ad Library (EU transparency) | `https://library.tiktok.com/ads?region=all` | every ad shown in the EU, searchable by the advertiser's LEGAL entity name | search is exact on the registered entity ("Duolingo, Inc."), EU only |
| LinkedIn Ad Library | `https://www.linkedin.com/ad-library/search?companyName=<Company>` | B2B ads by company or keyword, with impressions by country | needs a signed-in LinkedIn session in the browser |
| Snap political/issue ads | `https://www.snap.com/en-US/political-ads` | political and issue ads with spend | political only |

## Use these the way a person does
Open the pages in a normal browser session, one query at a time, and read what they show. These are transparency tools the
platforms publish for the public; their terms prohibit scripted bulk collection, scraping, or working around rate limits, so
do not automate requests against them from the agent. For automated, licensed research use a tool built for it.

## Procedure
1. **Start with the brand's own ads**, then 3 to 5 direct competitors, then 2 brands outside the category that are famous
   for great creative (that is where the copyable ideas usually are).
2. **Sort by longevity, not recency.** An ad still running after 60+ days is paying for itself. In Meta's library use
   "active" first, then "all" to see what they retired.
3. **Log each ad in one line**: brand · format (image/video/carousel) · hook mechanic · angle · offer · run length.
4. **Cluster the angles.** Five ads about "no more back pain" and one about "fits under a suit" tell you which angle
   the market has already validated and which is under-served.
5. **Write the brief from the clusters**: the top 3 angles, the hook mechanic each uses, and one specific thing to
   do differently. Quote the actual headlines; paraphrase loses the mechanic.

## Reading a creative fast
- First 2 seconds: what stops the thumb (see the `ad-hooks` skill for the mechanics by name).
- Is the product on screen inside 3 seconds? Long-running DTC video almost always says yes.
- Who is talking: brand voice, creator, or nobody (product-only). Note the ratio across the winners.
- Ending: offer + CTA, or a soft "learn more"? Match the strongest cluster.

## Next
Tear the strongest brand down properly with the `ad-teardown` skill, and write your own versions with `ad-hooks`
and `ugc-ad-scripts`.
