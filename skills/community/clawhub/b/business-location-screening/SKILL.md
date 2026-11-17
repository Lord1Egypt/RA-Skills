---
name: business-location-screening
description: Compare user-supplied candidate locations for a local business using nearby competitors, public access signals, review samples, and available city-level context. Use for an early screen, not a lease or viability recommendation.
allowed-tools: Bash(scripts/crawlora.sh:*)
---

# Business location screening

## Tool scope and data flow

Use the bundled `scripts/crawlora.sh` helper only for this skill's documented routes in `reference/endpoints.md`; the helper enforces its exact route and method allowlist. It reads `CRAWLORA_API_KEY` from the environment and sends it as an `x-api-key` header over HTTPS to `api.crawlora.net`. It stores the key in a mode-600 curl config under `TMPDIR` and removes it when the command exits. It reads `TMPDIR` only to choose that temporary config location; it does not inspect other environment variables or enumerate files, install software, or run with elevated privileges.

Compare a small set of user-supplied candidate sites or neighborhoods for a
local business. This is an early evidence screen for competition, access, and
public context, not a market-size estimate, commercial rent analysis, or
site-viability recommendation.

## Define the comparison

Before using Google or Apple Maps, explain that candidate locations, exact coordinates, and route anchors are sent through Crawlora to the named mapping provider. Ask for explicit consent before submitting a home address, unpublished business site, or confidential expansion location; use public/general locations or omit that comparison if the user does not approve.

Confirm the business type, candidate addresses or coordinates, target customer,
search radius, travel mode, and the factors the user cares about. Keep the
candidate list fixed across sources. If the user has not provided candidate
locations, ask for a small set or state a narrow search scope; do not invent a
site shortlist from map ranking alone.

## Collect matched location evidence

1. Resolve each candidate location with Google Maps or Apple Maps and record the
   returned coordinates, address, provider ID, and region. Keep IDs from each
   provider separate. A search result is not proof a proposed lease address is
   available.
2. Discover exact Google Maps business-category labels from the dataset facets
   before filtering. Use the same business definition, radius, country, and
   query plan for every candidate. Combine a bounded stored-dataset baseline
   with live Google/Apple/Yelp checks, but keep each source's coverage and
   retrieval time separate.
3. For competitors, count unique businesses within the defined boundary and
   record category, address, status, rating, review count, and source IDs.
   Deduplicate by provider ID first; across providers require a consistent
   address or other identifying evidence. Unknown status and coordinates stay
   unknown rather than being dropped silently.
4. If access matters, use Apple Maps walking/driving directions or ETA between
   each candidate and user-named anchors such as transit stops or destination
   areas. These are route/time snapshots, not footfall, commute, or customer
   traffic measurements. Transit departures are live service data, not a
   long-term frequency guarantee.
5. Read only a small, disclosed sample of nearby competitor reviews when it
   helps characterize service gaps. Keep source, date, sample size, and
   relevant/irrelevant counts; a review sample is not neighborhood demand.
6. Optional Numbeo city indices and Redfin housing-market records provide
   broad household-cost or residential-market context. They are city/metro/ZIP
   housing measures, not commercial lease rates, local incomes for every
   catchment, or site-level affordability.
7. For zoning, licensing, and local tax checks, use user-provided sources or
   find official local-government pages with Bing. Confirm the page applies to
   the candidate's municipality, then scrape that public URL. Preserve the
   municipality, source URL, and date. A page is not confirmation that a
   specific property is permitted for the proposed use.

## Interpret and deliver

Return a candidate-by-candidate evidence matrix with search areas, source,
radius/route settings, retrieved counts, deduplication method, competitor
categories, review sample, access observations, and any city-level context.
State data windows and missing inputs beside each candidate.

Do not rank sites with a single score unless the user supplies the criteria
and weights. Map counts, ratings, nearby anchors, and travel times do not
establish demand, revenue, foot traffic, zoning approval, commercial rent, or
lease availability. Identify the official demographic, traffic, property,
licensing, and cost data that would still be needed before signing a lease.

~~~sh
scripts/crawlora.sh /datasets/google-map-businesses/facets facet=category q=coffee country=us
scripts/crawlora.sh /datasets/google-map-businesses/nearby lat=37.7768 lon=-122.3980 radius_m=1500 page=1 page_size=50
scripts/crawlora.sh -X POST /google/map/search '{"keyword":"coffee shop 700 Folsom St San Francisco","language":"en","country":"us"}'
scripts/crawlora.sh /yelp/search term='coffee shops' location='San Francisco, CA' limit=10
scripts/crawlora.sh /apple-maps/eta origin_latitude=37.7768 origin_longitude=-122.3980 destination_latitude=37.7894 destination_longitude=-122.4010 mode=walking
scripts/crawlora.sh /datasets/housing-markets/search q='San Francisco' region_type=city latest=true
scripts/crawlora.sh /datasets/numbeo-cities/search q='San Francisco' country='United States' page_size=5
scripts/crawlora.sh /bing/search q='San Francisco cafe zoning permit official' count=5 country=us lang=en-us
~~~
