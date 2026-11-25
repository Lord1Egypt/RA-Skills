---
name: datapika
description: Fetch live public web data with the Datapika actors on Apify. Use when the user asks for job listings or hiring signals (LinkedIn, Indeed, Glassdoor, ZipRecruiter, company career sites), Reddit posts or comments, TikTok, Douyin, Bilibili, Kuaishou, YouTube, Threads or WeChat content, TikTok Shop products, Trustpilot reviews, Facebook/Instagram or Google ads, Google Maps places, Airbnb listings, hotel prices or Google Flights fares, and wants real rows instead of a guess.
---

# Datapika: live web data for agents

Datapika runs 19 web data actors on Apify. Each one takes a JSON input, collects public data, and returns rows as JSON. Runs bill per result on the user's Apify account. Current prices are on each actor page at https://datapika.com/actors.

## Pick the actor

| The user wants | Actor (`openclawai/<name>`) | Example input |
|---|---|---|
| Jobs from many boards in one search | `job-board-scraper` | `{"searchTerm":"data engineer","location":"Austin, TX","sites":["linkedin","indeed"],"maxResults":20,"hoursOld":72}` |
| LinkedIn jobs only, with descriptions and salary | `linkedin-jobs-scraper` | read the input schema first |
| Indeed / ZipRecruiter jobs and company hiring totals | `indeed-ziprecruiter-scraper` | read the input schema first |
| Every open job at one company (career site or ATS) | `career-site-ats-jobs-scraper` | read the input schema first |
| Reddit posts, comments, subreddits, users | `reddit-scraper` | `{"startUrls":["https://www.reddit.com/r/Python/top/?t=week"],"maxItems":20}` |
| TikTok, Douyin or Bilibili videos, profiles, comments | `tiktok-douyin-bilibili-scraper` | `{"mode":"user_posts","urls":["https://www.tiktok.com/@tiktok"],"maxItems":20}` |
| TikTok Shop products, prices, units sold | `tiktok-shop-scraper` | read the input schema first |
| YouTube videos, Shorts, comments, channels | `youtube-video-scraper` | read the input schema first |
| Threads posts and replies | `threads-scraper` | read the input schema first |
| Bilibili, Kuaishou or WeChat only | `bilibili-scraper`, `kuaishou-scraper`, `wechat-scraper` | read the input schema first |
| Trustpilot reviews and TrustScore | `trustpilot-reviews-scraper` | `{"companies":["www.notion.so"],"maxReviews":50,"languages":["en"]}` |
| Facebook and Instagram ads | `meta-ad-library-scraper` | `{"queries":["https://www.facebook.com/nike"],"country":"US","maxAdsPerQuery":20}` |
| Google ads by brand or domain | `google-ads-transparency-scraper` | `{"queries":["booking.com"],"advertisersPerQuery":1,"maxAdsPerAdvertiser":20,"region":"US"}` |
| Places with phone, website, rating | `google-maps-scraper` | `{"query":"coffee shops in Austin, TX","maxResults":20}` |
| Airbnb listings, prices, calendars | `airbnb-scraper` | `{"mode":"search_by_url","searchUrl":"https://www.airbnb.com/s/Lisbon--Portugal/homes?checkin=YYYY-MM-DD&checkout=YYYY-MM-DD&adults=2","currency":"USD","maxResults":20}` |
| Hotel and rental prices across booking sites | `hotel-rental-scraper` | `{"location":"Lisbon, Portugal","checkIn":"30 days","nights":2,"adults":2,"sites":["booking","airbnb","vrbo"],"maxResultsPerSite":10,"currency":"USD"}` |
| Flight itineraries and fares | `google-flights-scraper` | `{"from_airport":"JFK","to_airport":"LAX","date":"YYYY-MM-DD","trip":"one-way","max_results":20}` |

## Run it

**With the Datapika MCP server** (installed by this plugin, or `claude mcp add --transport http datapika "<url from https://datapika.com/mcp>"`):

1. Call `fetch-actor-details` for the actor to read its input schema and price.
2. Tell the user the actor, the input and the expected cost, and keep the first run small (10–20 results).
3. Call the actor's tool with the input and read the rows back.

**With the REST API** (needs `APIFY_TOKEN` in the environment):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/openclawai~google-maps-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"query":"coffee shops in Austin, TX","maxResults":10}'
```

The synchronous endpoint waits up to 300 seconds. For bigger runs, start the run with `POST /v2/acts/openclawai~<name>/runs`, poll `GET /v2/actor-runs/<runId>`, then read `GET /v2/datasets/<defaultDatasetId>/items`.

To read an input schema without MCP, open `https://apify.com/openclawai/<name>/input-schema`.

## Rules

- Collect public data only. These actors take no login, cookie or password inputs; don't ask the user for any.
- Cap results (`maxResults`, `maxItems` and similar) to what the user needs. Every result is billed.
- Handle personal data (names, profiles, reviews) under GDPR and CCPA, and keep only what the task needs.
- Quote prices from the actor page or `fetch-actor-details`, never from memory.

Examples in Python, Node and curl for each actor: https://github.com/lnvestor/datapika-examples
