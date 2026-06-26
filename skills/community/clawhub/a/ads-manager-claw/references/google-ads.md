# Google Ads API Reference

Base URL: `https://googleads.googleapis.com/v19/`
Auth headers:
- `Authorization: Bearer {oauth2_access_token}`
- `developer-token: {developer_token}`
- `login-customer-id: {manager_account_id}` (if using a manager account)

Customer ID format: `customers/{customer_id}` (no dashes, e.g. `customers/1234567890`)

> ⚠️ Google Ads API uses **micros** for money. $1 = 1,000,000 micros.
> The API is primarily gRPC-based but also supports REST. Use REST for simplicity.
> Always create campaigns in PAUSED status — activate after review.

---

## Campaign Types (AdvertisingChannelType)

| User Goal | channelType | Subtype |
|---|---|---|
| Search ads (text ads on Google) | `SEARCH` | — |
| Display ads (banner images) | `DISPLAY` | — |
| YouTube video ads | `VIDEO` (read-only via API — use DEMAND_GEN instead) | — |
| All-in-one smart campaigns | `PERFORMANCE_MAX` | — |
| Discovery / social-style | `DEMAND_GEN` | — |
| Shopping ads | `SHOPPING` | — |

---

## Step 1: Create Campaign Budget

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/campaignBudgets:mutate`

```json
{
  "operations": [{
    "create": {
      "name": "Summer Sale Budget",
      "amountMicros": "10000000",
      "deliveryMethod": "STANDARD"
    }
  }]
}
```

Returns resource name like: `customers/123/campaignBudgets/456`

---

## Step 2: Create Campaign

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/campaigns:mutate`

```json
{
  "operations": [{
    "create": {
      "name": "Summer Sale - Search",
      "advertisingChannelType": "SEARCH",
      "status": "PAUSED",
      "campaignBudget": "customers/123/campaignBudgets/456",
      "biddingStrategyType": "MAXIMIZE_CLICKS",
      "networkSettings": {
        "targetGoogleSearch": true,
        "targetSearchNetwork": true,
        "targetContentNetwork": false
      },
      "startDate": "20250401",
      "endDate": "20250430"
    }
  }]
}
```

**Bidding strategies:** `MAXIMIZE_CLICKS` (traffic), `MAXIMIZE_CONVERSIONS` (leads/sales), `TARGET_CPA` (cost per lead), `TARGET_ROAS` (return on ad spend), `TARGET_IMPRESSION_SHARE` (awareness)

---

## Step 3: Create Ad Group

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/adGroups:mutate`

```json
{
  "operations": [{
    "create": {
      "name": "Summer Sale - Shoes",
      "campaign": "customers/123/campaigns/789",
      "status": "PAUSED",
      "type": "SEARCH_STANDARD",
      "cpcBidMicros": "1000000"
    }
  }]
}
```

---

## Step 4: Add Keywords

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/adGroupCriteria:mutate`

```json
{
  "operations": [{
    "create": {
      "adGroup": "customers/123/adGroups/456",
      "status": "ENABLED",
      "keyword": {
        "text": "summer shoes sale",
        "matchType": "PHRASE"
      }
    }
  }]
}
```

**Match types:** `EXACT` (exact phrase only), `PHRASE` (phrase + close variants), `BROAD` (wide reach)

---

## Step 5: Create Responsive Search Ad

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/ads:mutate`

```json
{
  "operations": [{
    "create": {
      "adGroupAd": {
        "adGroup": "customers/123/adGroups/456",
        "status": "PAUSED",
        "ad": {
          "responsiveSearchAd": {
            "headlines": [
              { "text": "Summer Sale — Up to 50% Off" },
              { "text": "Shop Now & Save Big" },
              { "text": "Free Shipping on All Orders" }
            ],
            "descriptions": [
              { "text": "Browse our huge summer collection. Limited time offer!" },
              { "text": "Top brands, unbeatable prices. Shop today." }
            ],
            "path1": "summer",
            "path2": "sale"
          },
          "finalUrls": ["https://yoursite.com/summer-sale"]
        }
      }
    }
  }]
}
```

Min: 3 headlines, 2 descriptions. Max: 15 headlines, 4 descriptions.

---

## Update Budget

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/campaignBudgets:mutate`

```json
{
  "operations": [{
    "update": {
      "resourceName": "customers/123/campaignBudgets/456",
      "amountMicros": "15000000"
    },
    "updateMask": "amountMicros"
  }]
}
```

---

## Pause / Enable / Remove Campaign

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/campaigns:mutate`

```json
{
  "operations": [{
    "update": {
      "resourceName": "customers/123/campaigns/789",
      "status": "PAUSED"
    },
    "updateMask": "status"
  }]
}
```

Status values: `ENABLED`, `PAUSED`, `REMOVED` (permanent delete)

---

## Performance Report (Google Ads Query Language — GAQL)

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/googleAds:search`

```json
{
  "query": "SELECT campaign.name, campaign.status, metrics.impressions, metrics.clicks, metrics.ctr, metrics.average_cpc, metrics.cost_micros, metrics.conversions, metrics.cost_per_conversion FROM campaign WHERE segments.date DURING LAST_7_DAYS ORDER BY metrics.cost_micros DESC"
}
```

**Date ranges:** `TODAY`, `YESTERDAY`, `LAST_7_DAYS`, `LAST_14_DAYS`, `LAST_30_DAYS`, `THIS_MONTH`, `LAST_MONTH`

Key metrics: `metrics.impressions`, `metrics.clicks`, `metrics.ctr`, `metrics.average_cpc`, `metrics.cost_micros`, `metrics.conversions`, `metrics.cost_per_conversion`

Convert cost from micros: divide by 1,000,000.

---

## Geo Targeting

Add location targeting via campaign criteria:

POST `https://googleads.googleapis.com/v19/customers/{customer_id}/campaignCriteria:mutate`

```json
{
  "operations": [{
    "create": {
      "campaign": "customers/123/campaigns/789",
      "location": {
        "geoTargetConstant": "geoTargetConstants/1023191"
      }
    }
  }]
}
```

Common geo target constants: US=`2840`, UK=`2826`, India=`2356`, Mumbai=`1007786`
Search for location IDs via: GET `https://googleads.googleapis.com/v19/geoTargetConstants:suggest?locale=en&countryCode=IN&query=Mumbai`

---

## A/B Testing — Draft & Experiments

For proper A/B testing, use Google's Campaign Experiments (ExperimentService).
For simple testing, just create two ad groups with identical settings except one variable and compare performance after 7+ days.

---

## Common Errors

| Error | Plain English |
|---|---|
| `AUTHORIZATION_ERROR` | Your developer token or OAuth token is invalid |
| `CUSTOMER_NOT_FOUND` | Wrong Customer ID |
| `BUDGET_ERROR: BUDGET_AMOUNT_TOO_LOW` | Budget below minimum ($1/day) |
| `POLICY_ERROR` | Ad copy violates Google's ad policies |
| `KEYWORD_MATCH_TYPE_NOT_ALLOWED` | Check keyword format |
