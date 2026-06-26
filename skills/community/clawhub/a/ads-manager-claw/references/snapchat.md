# Snapchat Ads API Reference

Base URL: `https://adsapi.snapchat.com/v1/`
Auth: OAuth2 Bearer Token

### Get Access Token (from refresh token)

POST `https://accounts.snapchat.com/login/oauth2/access_token`
```json
{
  "client_id": "CLIENT_ID",
  "client_secret": "CLIENT_SECRET",
  "refresh_token": "REFRESH_TOKEN",
  "grant_type": "refresh_token"
}
```

Use returned `access_token` in header: `Authorization: Bearer {access_token}`

> ⚠️ Snapchat-specific notes:
> - Budgets are in **micro-currency** ($1 = 1,000,000 micros)
> - Snapchat's ad hierarchy: Campaign → Ad Squad → Ad (not "ad set" or "line item")
> - Primary audience is 13–34 year olds — best for young consumer brands
> - As of 2025, use `objective_v2_properties` instead of `objective` for new campaigns
> - MIN_ROAS bid strategy deprecated Feb 2025 — use `AUTO_BID` or `LOWEST_COST_WITH_MAX_BID`

---

## Campaign Objectives (objective_v2_properties)

| User Goal | goal | conversion_location |
|---|---|---|
| Website traffic | `VISITS` | `WEB` |
| Online sales | `PURCHASES` | `WEB` |
| App installs | `APP_INSTALLS` | `APP` |
| Brand awareness | `IMPRESSIONS` | (none) |
| Lead generation | `LEAD_GENERATION` | `WEB` |
| Video views | `VIDEO_VIEWS` | (none) |

---

## Step 1: Create Campaign

POST `adaccounts/{ad_account_id}/campaigns`

```json
{
  "campaigns": [{
    "name": "Summer Sale 2025",
    "ad_account_id": "AD_ACCOUNT_ID",
    "status": "PAUSED",
    "objective_v2_properties": {
      "goal": "PURCHASES",
      "conversion_location": "WEB"
    },
    "daily_budget_micro": 10000000,
    "start_time": "2025-04-01T00:00:00.000Z",
    "end_time": "2025-04-30T23:59:59.000Z"
  }]
}
```

Returns: `{ "campaigns": [{ "campaign": { "id": "CAMPAIGN_ID", ... } }] }`

---

## Step 2: Create Ad Squad (targeting + budget)

POST `campaigns/{campaign_id}/adsquads`

```json
{
  "adsquads": [{
    "name": "Women 18-34 India",
    "campaign_id": "CAMPAIGN_ID",
    "type": "SNAP_ADS",
    "status": "PAUSED",
    "targeting": {
      "regulated_content": false,
      "demographics": [{ "min_age": "18", "max_age": "34", "gender": ["FEMALE"] }],
      "geos": [{ "country_code": "in" }],
      "interests": [{ "category_id": "SNAPCHAT_LIFESTYLE_CATEGORY_ID" }]
    },
    "placement_v2": { "config": "AUTOMATIC" },
    "billing_event": "IMPRESSION",
    "bid_strategy": "AUTO_BID",
    "daily_budget_micro": 10000000,
    "optimization_goal": "PIXEL_PURCHASE",
    "start_time": "2025-04-01T00:00:00.000Z"
  }]
}
```

**Optimization goals:** `PIXEL_PURCHASE`, `SWIPES` (clicks), `IMPRESSIONS`, `VIDEO_VIEWS`, `APP_INSTALL`

---

## Step 3: Create Creative

POST `adaccounts/{ad_account_id}/creatives`

```json
{
  "creatives": [{
    "name": "Summer Sale Creative",
    "ad_account_id": "AD_ACCOUNT_ID",
    "type": "SNAP_AD",
    "top_snap_media_id": "MEDIA_ID",
    "top_snap_crop_position": "MIDDLE",
    "headline": "Summer Sale — Up to 50% Off!",
    "brand_name": "My Brand",
    "call_to_action": "SHOP_NOW",
    "web_view_properties": {
      "url": "https://yoursite.com/sale",
      "allow_snap_javascript_sdk": false,
      "block_preload": false
    },
    "profile_properties": {
      "profile_id": "PUBLIC_PROFILE_ID"
    }
  }]
}
```

**Call-to-action types:** `SHOP_NOW`, `LEARN_MORE`, `SIGN_UP`, `BOOK_NOW`, `INSTALL_NOW`, `WATCH`

Upload media first:
POST `adaccounts/{ad_account_id}/media` (multipart form upload)

---

## Step 4: Create Ad

POST `adsquads/{ad_squad_id}/ads`

```json
{
  "ads": [{
    "name": "Summer Sale Ad",
    "ad_squad_id": "AD_SQUAD_ID",
    "creative_id": "CREATIVE_ID",
    "status": "PAUSED",
    "type": "SNAP_AD"
  }]
}
```

---

## Update Budget

PATCH `campaigns/{campaign_id}`

```json
{
  "campaigns": [{
    "id": "CAMPAIGN_ID",
    "daily_budget_micro": 15000000
  }]
}
```

Or update at Ad Squad level:
PATCH `adsquads/{adsquad_id}`
```json
{
  "adsquads": [{ "id": "ADSQUAD_ID", "daily_budget_micro": 15000000 }]
}
```

---

## Pause / Resume / Delete

PATCH `campaigns/{campaign_id}`
```json
{ "campaigns": [{ "id": "CAMPAIGN_ID", "status": "PAUSED" }] }   // pause
{ "campaigns": [{ "id": "CAMPAIGN_ID", "status": "ACTIVE" }] }   // resume
```

DELETE `campaigns/{campaign_id}` — permanent, confirm first

---

## Performance Report

GET `adaccounts/{ad_account_id}/stats`

```
?fields=impressions,swipes,spend,video_views,conversion_purchases
&start_time=2025-03-14T00:00:00.000-07:00
&end_time=2025-03-21T00:00:00.000-07:00
&granularity=DAY
&breakdown_by=campaign
```

Key metrics:
- `impressions` — times shown
- `swipes` — clicks (Snapchat calls clicks "swipes")
- `swipe_up_percent` — swipe-through rate (like CTR)
- `spend` — amount spent in micros (divide by 1,000,000)
- `video_views` — video views
- `conversion_purchases` — purchases tracked via Snap Pixel

---

## List Campaigns

GET `adaccounts/{ad_account_id}/campaigns`

---

## Audience Targeting Options

- **Demographics:** Age (13+), gender, language
- **Geos:** Country, region, city, postal code, radius
- **Lifestyle categories:** Snapchat's interest segments (Beauty, Fitness, Gaming, etc.)
- **Custom Audiences:** Upload customer email list or phone numbers (hashed)
- **Lookalike Audiences:** Based on your custom audience
- **Device targeting:** iOS/Android, device types, carriers

Get lifestyle category IDs:
GET `targeting_dimensions/interests`

---

## A/B Testing

Create two Ad Squads under the same campaign with equal budgets. Change only one element.
Naming: "Test A — Lifestyle Targeting" vs "Test B — Custom Audience".
Review after 5–7 days and compare `swipe_up_percent` and `cost_per_conversion`.

---

## Common Errors

| Error | Plain English |
|---|---|
| `E3003` | Invalid access token — re-authenticate |
| `E1001` | Field missing or invalid — check required fields |
| `E3006` | Insufficient permissions for this ad account |
| `E5001` | Budget too low — minimum varies by region |
| `CREATIVE_NOT_APPROVED` | Creative rejected by Snap's review team — check their ad policies |
