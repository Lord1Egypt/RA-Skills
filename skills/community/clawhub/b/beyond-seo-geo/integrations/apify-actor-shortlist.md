# Apify Actor Shortlist

Generated from Apify Store checks on 2026-05-26. Actor availability, quality, and pricing can change, so re-check before large runs.

Do not store API tokens in this file.

## Recommended Starting Actors

| Workflow | Preferred Actor | Actor ID | Maintainer | Confidence | Notes |
|---|---|---|---|---|---|
| Website/content crawl | `apify/website-content-crawler` | `aYG0l9s7dbB7j3gbS` | Apify | High | Best first choice for page inventory and content extraction. |
| Custom crawl/scrape | `apify/web-scraper` | `moJRLRc85AitArpNN` | Apify | High | Use when custom extraction or JS rendering is needed. |
| Google SERP sample | `apify/google-search-scraper` | `nFJndFXA5zjCTuudP` | Apify | High | Use for keyword SERP snapshots, competitor discovery, PAA/related result checks where available. |
| Google Trends | `apify/google-trends-scraper` | `DyNQEYDj9awfGQf9A` | Apify | Medium | Useful for directional demand and seasonality; validate important decisions with other data. |
| Google Maps/local | `compass/crawler-google-places` | `nwua9Gu5YrADL7ZDj` | Compass | High | Strong local SEO starting point for map pack and local competitor discovery. |
| Google reviews | `compass/Google-Maps-Reviews-Scraper` | `Xb8osYTtOjlsgI6k9` | Compass | High | Use for review pattern analysis when local SEO requires it. |
| PageSpeed/Core Web Vitals via Apify | `alizarin_refrigerator-owner/pagespeed-insights` | `wEonoqiLlBBugf5Xk` | Community | Medium | Use through Apify first. Treat as confirmed when raw URL/device/timestamp metrics are returned; otherwise directional. |
| GSC via Apify | Search Apify Store per project | varies | varies | Medium-High | Prefer authenticated GSC connector/export actors when available. Confirm query/page/click/impression data only when actor uses owned-account auth or uploaded export. |
| GA4 via Apify | Search Apify Store per project | varies | varies | Medium-High | Prefer authenticated GA4 connector/export actors when available. Confirm traffic/conversion data only when actor uses owned-account auth or uploaded export. |
| Ahrefs/Semrush/Moz via Apify | Search Apify Store per project | varies | varies | Medium | Use Apify actors where available. Treat as confirmed only if the actor connects to an owned paid account/export; public/free-tool scrapes stay directional. |
| Backlink/authority style checks | Community SEO/backlink actors | varies | Community | Low-Medium | Use through Apify when no export/account actor exists, but label authority/backlink metrics as directional. |

## Credit-Safe Default Sequence

1. Crawl homepage and sitemap first.
2. Limit first crawl to 50 pages.
3. Run only 5-10 SERP queries for the initial keyword sample.
4. Crawl 3-5 competitors after SERP discovery.
5. Use GSC/GA4 actors or Apify-hosted exports when first-party performance data is needed.
6. Use Maps/reviews only for local SEO projects.
7. Use authority/backlink actors after checking whether Apify has authenticated Ahrefs/Semrush/Moz workflows for the project.
