# Meta (Facebook & Instagram) Ads API Reference

Base URL: `https://graph.facebook.com/v21.0/`
Auth: Append `access_token={token}` to all requests (or use Authorization header)
Ad Account format: `act_{account_id}`

> ⚠️ 2025 Note: Meta now uses ODAX (Outcome-Driven Ad Experiences) objectives from v21.0+.
> Use the new objective names listed below. Budgets are in **micros** ($1 = 1,000,000 micros).

---

## Campaign Objectives (ODAX — use these)

| User Goal | API objective value |
|---|---|
| Website traffic | `OUTCOME_TRAFFIC` |
| Sales / conversions | `OUTCOME_SALES` |
| Leads / sign-ups | `OUTCOME_LEADS` |
| Brand awareness | `OUTCOME_AWARENESS` |
| App installs | `OUTCOME_APP_PROMOTION` |
| Engagement | `OUTCOME_ENGAGEMENT` |

---

## Create Campaign

POST `/{ad_account_id}/campaigns`

```json
{
  "name": "Summer Sale 2025",
  "objective": "OUTCOME_TRAFFIC",
  "status": "PAUSED",
  "special_ad_categories": []
}
```

Returns: `{ "id": "CAMPAIGN_ID" }`

---

## Create Ad Set (targeting + budget lives here)

POST `/{ad_account_id}/adsets`

```json
{
  "name": "Women 25-45 Mumbai - Interests",
  "campaign_id": "CAMPAIGN_ID",
  "daily_budget": "2000000",
  "billing_event": "IMPRESSIONS",
  "optimization_goal": "LINK_CLICKS",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "targeting": {
    "geo_locations": {
      "cities": [{ "key": "2295424", "name": "Mumbai" }]
    },
    "age_min": 25,
    "age_max": 45,
    "genders": [2],
    "interests": [
      { "id": "6003107902433", "name": "Fashion" }
    ]
  },
  "start_time": "2025-04-01T00:00:00+0000",
  "status": "PAUSED"
}
```

**Gender values:** `1` = Men, `2` = Women (omit field for all genders)
**Daily budget:** In micros. $10/day = `"10000000"`

---

## Create Ad Creative

POST `/{ad_account_id}/adcreatives`

```json
{
  "name": "Summer Sale Creative",
  "object_story_spec": {
    "page_id": "YOUR_PAGE_ID",
    "link_data": {
      "image_hash": "IMAGE_HASH",
      "link": "https://yoursite.com/sale",
      "message": "Shop our Summer Sale — up to 50% off!",
      "name": "Summer Sale is Here",
      "call_to_action": {
        "type": "SHOP_NOW",
        "value": { "link": "https://yoursite.com/sale" }
      }
    }
  }
}
```

**Call-to-action types:** `SHOP_NOW`, `LEARN_MORE`, `SIGN_UP`, `BOOK_NOW`, `CONTACT_US`, `DOWNLOAD`

---

## Create Ad (links creative to ad set)

POST `/{ad_account_id}/ads`

```json
{
  "name": "Summer Sale Ad",
  "adset_id": "ADSET_ID",
  "creative": { "creative_id": "CREATIVE_ID" },
  "status": "PAUSED"
}
```

---

## Update Budget

POST `/{adset_id}`

```json
{
  "daily_budget": "15000000",
  "access_token": "TOKEN"
}
```

---

## Pause / Resume / Delete

POST `/{campaign_id}` or `/{adset_id}` or `/{ad_id}`
```json
{ "status": "PAUSED" }      // pause
{ "status": "ACTIVE" }      // resume
{ "status": "DELETED" }     // delete (irreversible)
```

---

## Get Performance Report (Insights)

GET `/{ad_account_id}/insights`

```
?fields=campaign_name,impressions,clicks,ctr,spend,cpc,cpm,actions,cost_per_action_type
&date_preset=last_7d
&level=campaign
&access_token=TOKEN
```

**Date presets:** `today`, `yesterday`, `last_7d`, `last_14d`, `last_30d`, `this_month`, `last_month`
**Levels:** `account`, `campaign`, `adset`, `ad`

Key response fields:
- `impressions` — times shown
- `clicks` — link clicks
- `spend` — amount spent (in account currency)
- `ctr` — click-through rate (%)
- `cpc` — cost per click
- `actions` — conversions, purchases, leads (array by action type)

---

## List All Campaigns

GET `/{ad_account_id}/campaigns`
```
?fields=id,name,status,objective,daily_budget,lifetime_budget
&access_token=TOKEN
```

---

## A/B Testing (Split Testing)

Create two Ad Sets under the same campaign with identical settings except one variable.
Name them clearly: "Test A — Blue Image" and "Test B — Red Image".
Set equal budgets. Check back after 5–7 days and compare `cpc` or `cost_per_action`.

---

## Audience — Custom Audiences (from email list)

POST `/{ad_account_id}/customaudiences`
```json
{
  "name": "My Customer List",
  "subtype": "CUSTOM",
  "description": "Existing customers",
  "customer_file_source": "USER_PROVIDED_ONLY"
}
```
Then upload hashed emails via: POST `/{audience_id}/users`

---

## Useful Interest IDs (for targeting)

Use the Search API to find interest IDs:
GET `https://graph.facebook.com/v21.0/search?type=adinterest&q=yoga&access_token=TOKEN`

---

## Common Errors

| Error code | Plain English meaning |
|---|---|
| `100` | Something is missing or wrong in the request — check required fields |
| `200` | Permission error — your access token doesn't have the right permissions |
| `190` | Access token expired — generate a new one |
| `2635` | Daily budget too low — minimum is usually $1/day |
| `1487398` | Special ad category required (housing, credit, employment, politics) |
