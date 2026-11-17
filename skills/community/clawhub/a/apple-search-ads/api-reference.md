# API Reference — Apple Search Ads

Complete endpoint reference for Campaign Management API v5.

Contents: Authentication · Base URL & Headers · Apps · Campaigns · Ad Groups · Keywords · Creatives & Ads · Reports · Geolocations · Error Handling

## Authentication

### Generate Client Secret (JWT)

```javascript
// Node.js example
const jwt = require('jsonwebtoken');
const fs = require('fs');

function generateClientSecret() {
  const privateKey = fs.readFileSync('AuthKey.p8');
  const now = Math.floor(Date.now() / 1000);
  
  const payload = {
    sub: process.env.ASA_CLIENT_ID,
    aud: 'https://appleid.apple.com',
    iat: now,
    exp: now + (180 * 24 * 60 * 60), // 180 days
    iss: process.env.ASA_TEAM_ID
  };
  
  return jwt.sign(payload, privateKey, {
    algorithm: 'ES256',
    header: {
      alg: 'ES256',
      kid: process.env.ASA_KEY_ID
    }
  });
}
```

### Token Exchange

```bash
curl -X POST "https://appleid.apple.com/auth/oauth2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${ASA_CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  -d "scope=searchadsorg"
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

Access tokens are valid 1 hour — cache and reuse across calls; minting a fresh token per request is the usual cause of auth throttling. The client secret JWT may set `exp` up to 180 days out: generate it once and store it, not per run.

## Base URL & Headers

All endpoints below are relative to the base URL.

```
Base URL: https://api.searchads.apple.com/api/v5
Headers:
  Authorization: Bearer {ACCESS_TOKEN}
  X-AP-Context: orgId={ORG_ID}
  Content-Type: application/json
```

## Apps

### Search Apps

Find apps to promote by name or Adam ID.

```bash
POST /search/apps
```

Request:
```json
{
  "query": "meditation",
  "returnOwnedApps": false,
  "pagination": {
    "offset": 0,
    "limit": 20
  }
}
```

### Get App Eligibility

Check if an app can be promoted.

```bash
GET /apps/{adamId}/eligibilities?countriesOrRegions=US,UK
```

Response:
```json
{
  "data": [
    {
      "countryOrRegion": "US",
      "eligibilityStatus": "ELIGIBLE",
      "supplySource": "APPSTORE_SEARCH_RESULTS"
    }
  ]
}
```

### Get App Details

```bash
GET /apps/{adamId}?include=assets
```

## Campaigns

### List Campaigns

```bash
GET /campaigns?limit=100&offset=0
```

With filters:
```bash
POST /campaigns/find
```

Request:
```json
{
  "conditions": [
    {"field": "status", "operator": "IN", "values": ["ENABLED", "PAUSED"]}
  ],
  "orderBy": [{"field": "name", "sortOrder": "ASCENDING"}],
  "pagination": {"offset": 0, "limit": 100}
}
```

### Create Campaign

```bash
POST /campaigns
```

Request:
```json
{
  "name": "MyApp - US - Brand",
  "adamId": 123456789,
  "countriesOrRegions": ["US"],
  "budgetAmount": {
    "amount": "1000",
    "currency": "USD"
  },
  "dailyBudgetAmount": {
    "amount": "50",
    "currency": "USD"
  },
  "supplySources": ["APPSTORE_SEARCH_RESULTS"],
  "billingEvent": "TAPS",
  "status": "ENABLED",
  "startTime": "2026-01-01T00:00:00.000",
  "endTime": null,
  "locInvoiceDetails": {
    "billingContactEmail": "billing@example.com"
  }
}
```

Notes:
- `supplySources` values: `APPSTORE_SEARCH_RESULTS`, `APPSTORE_SEARCH_TAB`, `APPSTORE_TODAY_TAB`, `APPSTORE_PRODUCT_PAGES`. One per campaign — never blend placements (see `strategy.md`).
- Prefer `dailyBudgetAmount` as the operative lever; lifetime budgets (`budgetAmount`) were phased out for new campaigns (2022). Monthly ceiling ≈ daily budget × 30.4.

### Update Campaign

```bash
PUT /campaigns/{campaignId}
```

Request (partial update):
```json
{
  "dailyBudgetAmount": {
    "amount": "75",
    "currency": "USD"
  },
  "status": "PAUSED"
}
```

### Delete Campaign

```bash
DELETE /campaigns/{campaignId}
```

## Ad Groups

### List Ad Groups

```bash
GET /campaigns/{campaignId}/adgroups
```

### Create Ad Group

```bash
POST /campaigns/{campaignId}/adgroups
```

Request:
```json
{
  "name": "Brand Keywords - Exact",
  "defaultBidAmount": {
    "amount": "2.00",
    "currency": "USD"
  },
  "cpaGoal": {
    "amount": "5.00",
    "currency": "USD"
  },
  "automatedKeywordsOptIn": false,
  "startTime": "2026-01-01T00:00:00.000",
  "targetingDimensions": {
    "age": {
      "included": [{"minAge": 18}]
    },
    "gender": {
      "included": ["M", "F"]
    },
    "deviceClass": {
      "included": ["IPHONE", "IPAD"]
    },
    "appDownloaders": {
      "included": [],
      "excluded": [123456789]
    }
  },
  "status": "ENABLED"
}
```

Notes:
- `cpaGoal` is advisory — it never caps spend (see SKILL.md Traps). Bids and daily budgets are the only hard controls.
- `defaultBidAmount` applies only to keywords without their own bid; a keyword-level `bidAmount` always overrides it.
- Any `age`/`gender`/location refinement restricts delivery to users with Personalized Ads enabled — reach drops silently. `appDownloaders.excluded` is the exception worth using.

### Targeting Dimensions

| Dimension | Values |
|-----------|--------|
| `age` | `minAge`, `maxAge` (18-65+) |
| `gender` | `M`, `F` |
| `deviceClass` | `IPHONE`, `IPAD` |
| `daypart` | Hours 0-23, local time |
| `adminArea` | State/province codes |
| `locality` | City codes |
| `appDownloaders` | Adam IDs to include/exclude |

## Keywords

### Add Keywords (Bulk)

```bash
POST /campaigns/{campaignId}/adgroups/{adGroupId}/targetingkeywords/bulk
```

Request:
```json
[
  {
    "text": "meditation app",
    "matchType": "EXACT",
    "bidAmount": {"amount": "2.50", "currency": "USD"},
    "status": "ACTIVE"
  },
  {
    "text": "mindfulness",
    "matchType": "BROAD",
    "bidAmount": {"amount": "1.00", "currency": "USD"},
    "status": "ACTIVE"
  }
]
```

`matchType: EXACT` also serves plurals and common misspellings (Apple-documented) — verify actual queries via the search term report, not the keyword list.

### Update Keyword

```bash
PUT /campaigns/{campaignId}/adgroups/{adGroupId}/targetingkeywords/{keywordId}
```

### Add Negative Keywords

```bash
POST /campaigns/{campaignId}/adgroups/{adGroupId}/negativekeywords/bulk
```

Request:
```json
[
  {"text": "free meditation", "matchType": "EXACT"},
  {"text": "meditation music", "matchType": "BROAD"}
]
```

### Campaign-Level Negatives

```bash
POST /campaigns/{campaignId}/negativekeywords/bulk
```

## Creatives & Ads

### List Creatives

```bash
GET /creatives?adamId={adamId}
```

### Create Ad

```bash
POST /campaigns/{campaignId}/adgroups/{adGroupId}/ads
```

Request (default creative):
```json
{
  "name": "Default Ad",
  "creativeType": "DEFAULT_PRODUCT_PAGE",
  "status": "ENABLED"
}
```

Request (Custom Product Page):
```json
{
  "name": "Summer Promo Ad",
  "creativeType": "CUSTOM_PRODUCT_PAGE",
  "productPageId": "cpp-uuid-from-app-store-connect",
  "status": "ENABLED"
}
```

### List Custom Product Pages

```bash
GET /apps/{adamId}/customproductpages
```

## Reports

### Campaign Report

```bash
POST /reports/campaigns
```

Request:
```json
{
  "startTime": "2026-01-01",
  "endTime": "2026-01-31",
  "timeZone": "UTC",
  "granularity": "DAILY",
  "selector": {
    "conditions": [
      {"field": "campaignStatus", "operator": "IN", "values": ["ENABLED"]}
    ],
    "orderBy": [{"field": "localSpend", "sortOrder": "DESCENDING"}],
    "pagination": {"offset": 0, "limit": 100}
  },
  "groupBy": ["countryOrRegion"],
  "returnRowTotals": true,
  "returnGrandTotals": true
}
```

`timeZone` accepts `UTC` or `ORTZ` (org time zone) — pick one for ALL reporting and never mix (SKILL.md Traps).

### Available Metrics

| Metric | Description |
|--------|-------------|
| `impressions` | Ad impressions |
| `taps` | Taps on ad |
| `installs` | App installs |
| `newDownloads` | First-time downloads |
| `redownloads` | Re-downloads |
| `latOnInstalls` | LAT-on installs |
| `latOffInstalls` | LAT-off installs |
| `ttr` | Tap-through rate |
| `localSpend` | Spend in local currency |
| `avgCPA` | Average cost per acquisition |
| `avgCPT` | Average cost per tap |
| `conversionRate` | Installs / Taps |

`latOnInstalls`/`latOffInstalls` are legacy — Limit Ad Tracking predates App Tracking Transparency (iOS 14.5); ignore them in new analysis. Watch `redownloads` vs `newDownloads`: a low CPA driven by re-downloads is retention masquerading as acquisition.

### Search Term Report

```bash
POST /reports/campaigns/{campaignId}/searchterms
```

Request:
```json
{
  "startTime": "2026-01-01",
  "endTime": "2026-01-31",
  "selector": {
    "conditions": [
      {"field": "impressions", "operator": "GREATER_THAN", "values": ["10"]}
    ],
    "orderBy": [{"field": "installs", "sortOrder": "DESCENDING"}],
    "pagination": {"offset": 0, "limit": 1000}
  },
  "returnRowTotals": true
}
```

### Impression Share Report

```bash
POST /reports/campaigns/{campaignId}/impressionshare
```

Request:
```json
{
  "startTime": "2026-01-01",
  "endTime": "2026-01-31",
  "granularity": "DAILY",
  "selector": {
    "pagination": {"offset": 0, "limit": 100}
  }
}
```

Impression share comes back as a low/high band (a range, not a point value) — track the band's movement over time; comparing single days is meaningless.

## Geolocations

### Search Geolocations

```bash
GET /search/geo?query=california&countryOrRegion=US&entity=AdminArea
```

Entities: `Country`, `AdminArea` (state), `Locality` (city), `DMA` (metro)

## Error Handling

### Error Response Format

```json
{
  "error": {
    "errors": [
      {
        "messageCode": "INVALID_FIELD",
        "message": "Invalid field: budgetAmount",
        "field": "budgetAmount"
      }
    ]
  }
}
```

### Common Error Codes

| Code | Meaning |
|------|---------|
| `UNAUTHORIZED` | Invalid or expired token |
| `FORBIDDEN` | No access to resource |
| `NOT_FOUND` | Resource doesn't exist |
| `INVALID_FIELD` | Field validation failed |
| `LIMIT_EXCEEDED` | Rate limit hit |

### Rate Limits

Apple throttles per org without publishing exact quotas; `LIMIT_EXCEEDED` / HTTP 429 is the signal.

- On 429: halve request rate, retry with exponential backoff (2s, 4s, 8s...)
- Batch (`/bulk`) endpoints count as one request — always prefer them over per-keyword calls
- Paginate large reads (`limit` ≤ 1000 on reports) instead of one giant request
- Cache the OAuth token for its full hour (→ Authentication); token minting is throttled separately
