# Angi page shapes and recipes

Every shape below was read off live angi.com bytes (Charlotte, NC / plumbing,
2026-08-10), not inferred from docs. Angi publishes no consumer API — the
search page fires zero XHR, so these pages *are* the API.

Extraction key per page type:

- search / company list → key **`legacyId`** (the provider wrapper)
- pro profile → key **`reviewId`** (the review records)

## 1. Search — pros by trade + city

`GET /companylist/us/<state>/<city>/<trade>.htm[?page=N]`

10 unique pros per page. Each appears **twice** in the payload, so
`--dedupe id` is mandatory.

```sh
fpx get 'https://www.angi.com/companylist/us/nc/charlotte/plumbing.htm' -p angi \
  | node rsc.mjs legacyId --dedupe id > pros.json
jq length pros.json            # 10
```

Provider record (references already resolved by `rsc.mjs`):

```jsonc
{
  "id": "019bea94-1c41-11ee-b010-12f6eb045c11",   // stable uuid — dedupe on this
  "legacyId": "158675609",                        // numeric HomeAdvisor id
  "profileUrl": "/companylist/us/nc/monroe/superior-plumbing-and-drains-reviews-1.htm",
  "logoPhotoUrl": "https://cdn.homeadvisor.com/…",
  "businessType": "LEADS",
  "isSponsored": true,                            // paid placement, not a ranking signal
  "isCorporateAccount": false,
  "recentLeadCount": 2,
  "businessInfo": {
    "businessName": "Superior Plumbing and Drains",
    "businessDescription": "…",
    "yearsInBusiness": 21,
    "serviceArea": "Serving Charlotte, NC and surrounding areas",
    "responseRate": 42,                           // percent
    "responseTime": "1223",                       // string; units undocumented — pass through
    "isAdvertiser": true,
    "amenities": {
      "acceptedPaymentMethods": ["CREDIT_CARD"],
      "emergencyServices": true, "freeEstimates": false, "warrantiesOffered": true,
      "bilingual": false, "veteranOwned": false,
      "smallJobsWelcome": false, "offersCommercialServices": false
    },
    "serviceHours": [...], "presentationCapabilities": {...}
  },
  "contactInfo": { "address": { "street1": "…", "city": "Monroe", "state": "NC", "postalCode": "28110", "country": "US" } },
  "rating": {
    "reviewCount": 34,
    "recommendedRate": 87,                        // percent who'd recommend
    "averageOverallRating": 4.5,                  // rounded, display value
    "averageRatings": {                           // unrounded, per dimension
      "OVERALL": 4.65625, "QUALITY": 4.769, "VALUE": 4.423,
      "PUNCTUALITY": 4.807, "PROFESSIONALISM": 4.769, "RESPONSIVENESS": 4.846
    },
    "bestReview": { "reviewId": "f31be34d-…", "comment": "…", "createdOn": "2020-03-28T23:48:23Z" }
  },
  "tasksOffered": ["Faucets, Fixtures and Pipes - Repair or Replace", …],
  "awards": [...], "proSuppliedPhotos": [...]
}
```

`averageOverallRating` (4.5) and `averageRatings.OVERALL` (4.65625) differ —
the first is the rounded display value. Rank on `averageRatings.OVERALL`.

Recipes:

```sh
# Rank by true overall rating, pros with a meaningful review count
jq -r '[.[] | select(.rating.reviewCount >= 10)]
       | sort_by(-.rating.averageRatings.OVERALL)[]
       | "\(.rating.averageRatings.OVERALL * 100 | round / 100)\t\(.rating.reviewCount) reviews\t\(.businessInfo.businessName)"' pros.json

# Organic only (drop paid placements)
jq '[.[] | select(.isSponsored | not)]' pros.json

# Emergency service + free estimates
jq -r '.[] | select(.businessInfo.amenities.emergencyServices and .businessInfo.amenities.freeEstimates)
       | .businessInfo.businessName' pros.json

# Walk several pages
for p in 1 2 3; do
  fpx get "https://www.angi.com/companylist/us/nc/charlotte/plumbing.htm?page=$p" -p angi \
    | node rsc.mjs legacyId --dedupe id
done | jq -s 'add | unique_by(.id)' > all-pros.json
```

## 2. Pro profile + reviews

`GET <profileUrl>` — the `profileUrl` from a search record, e.g.
`/companylist/us/nc/charlotte/mkb-plumbing-and-septic-llc-reviews-8535260.htm`.
The trailing number is the pro's legacy id.

```sh
fpx get 'https://www.angi.com/companylist/us/nc/charlotte/mkb-plumbing-and-septic-llc-reviews-8535260.htm' -p angi \
  | node rsc.mjs reviewId > reviews.json
jq length reviews.json         # 48
```

Review record:

```jsonc
{
  "reviewId": "…",
  "rating": 5,                       // 1–5
  "starRating": 5,                   // present on some pages
  "text": "…",                       // review body
  "cost": 1500,                      // dollars, or absent
  "reportDate": "2026-04-22T00:35:02.769099",
  "userName": "…",
  "isAnonymous": false,
  "isVerified": true,
  "isGoogleReview": false,
  "source": "…",
  "categories": [ { "haId": 40111, "name": "Septic System Repair", "reviewCount": 1 } ],
  "serviceProviderId": 159707286,
  "serviceProviderUuid": "…",
  "serviceProviderName": "…",
  "leafSlug": "…",
  "spComment": "…",                  // the pro's public response, when present
  "wouldHireAgain": true             // present on some reviews
}
```

`categories` arrives as a `"$b5"` reference that chains (`b5:["$b6"]`);
`rsc.mjs` resolves it. If you see a bare `"$…"` string in output, the row was
missing from the payload — re-fetch rather than trusting it.

Recipes:

```sh
# Rating distribution
jq -r 'group_by(.rating)[] | "\(.[0].rating)★  \(length)"' reviews.json

# Recent negative reviews with the pro's response
jq -r 'sort_by(.reportDate) | reverse
       | .[] | select(.rating <= 3)
       | "\(.reportDate[0:10])  \(.rating)★  \(.text[0:120])\n    pro: \(.spComment // "(no response)")"' reviews.json

# Median job cost where reported
jq '[.[] | .cost | numbers] | sort | .[length/2 | floor]' reviews.json

# What work this pro is actually reviewed for
jq -r '[.[].categories[]?.name] | group_by(.)[] | "\(length)\t\(.[0])"' reviews.json | sort -rn
```

## 3. Taxonomy (plain curl — no bridge)

```sh
# ~312 trade slugs
curl -s https://www.angi.com/sitemap/statecat-sitemap.xml \
  | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' \
  | sed -n 's#.*/companylist/us/[a-z][a-z]/\([^/]*\)\.htm#\1#p' | sort -u

# Index of per-trade geo sitemaps
curl -s https://www.angi.com/sitemap/geo-sitemap-index.xml \
  | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g'

# Cities carrying a given trade — use to validate a city/trade combo before fetching
curl -s https://www.angi.com/sitemap/angi-geocat-plumbing.xml \
  | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' \
  | sed -n 's#.*/companylist/us/\([a-z][a-z]\)/\([^/]*\)/.*#\1/\2#p' | sort -u
```

Other sitemaps in `robots.txt`: `article-sitemap.xml`, `leaf-sitemap-index.xml`,
`nearme-sitemap.xml`, `topic-sitemap.xml`.

## Verified negatives — don't build on these

- **`?zip=` does nothing.** `…/us/nc/charlotte/plumbing.htm?zip=90210` returns
  byte-identical Charlotte pros. Location is path-only.
- **No consumer API.** `api.angi.com` 404s, `developer.angi.com` does not
  resolve, and the search page issues no XHR — everything is SSR.
- **`curl` cannot reach content pages.** 403 Cloudflare on `/`, `/companylist/*`,
  `/nearme/*`. Only `robots.txt`, `/sitemap/*` and `/auth/login` answer.
- **JSON-LD is not enough.** `SearchResultsPage`/`ItemList` carry names,
  addresses, profile URLs and one sample review — no ratings, no review counts,
  no ids.
