# X (Twitter) Ads API Reference

Base URL: `https://ads-api.x.com/12/`
Auth: OAuth 1.0a (use all 4 credentials: API Key, API Secret, Access Token, Access Token Secret)

> ⚠️ Important limitations:
> - Funding instruments (credit cards) CANNOT be created via API — must be set up at ads.twitter.com first
> - Max 200 active campaigns per account
> - Budgets are in the account's currency (NOT micros like Meta/Snapchat)
> - A paused campaign still counts toward the 200-campaign limit

---

## Campaign Objectives

| User Goal | API objective |
|---|---|
| Website traffic | `WEBSITE_CLICKS` |
| Brand awareness | `AWARENESS` |
| Video views | `VIDEO_VIEWS` |
| App installs | `APP_INSTALLS` |
| Engagement | `TWEET_ENGAGEMENTS` |
| Reach | `REACH` |
| Followers | `FOLLOWERS` |

---

## Step 1: Get Funding Instrument ID (must exist already)

GET `accounts/{account_id}/funding_instruments`

```
Authorization: OAuth oauth_consumer_key="...", oauth_token="...", ...
```

Note the `id` of an active funding instrument — you'll need it for campaign creation.

---

## Step 2: Create Campaign

POST `accounts/{account_id}/campaigns`

```
name=Summer+Sale+Campaign
&funding_instrument_id=FUNDING_ID
&objective=WEBSITE_CLICKS
&daily_budget_amount_local_micro=10000000
&status=PAUSED
&start_time=2025-04-01T00:00:00Z
&end_time=2025-04-30T23:59:59Z
```

Note: X Ads API uses form-encoded POST bodies, not JSON.

`daily_budget_amount_local_micro`: $10/day = `10000000` (yes, micros here too)

---

## Step 3: Create Line Item (equivalent to Ad Set)

POST `accounts/{account_id}/line_items`

```
campaign_id=CAMPAIGN_ID
&name=Mumbai+Women+25-44
&product_type=PROMOTED_TWEETS
&placements=ALL_ON_TWITTER
&objective=WEBSITE_CLICKS
&bid_type=AUTO
&status=PAUSED
&start_time=2025-04-01T00:00:00Z
```

---

## Step 4: Set Targeting on Line Item

POST `accounts/{account_id}/targeting_criteria`

```
line_item_id=LINE_ITEM_ID
&targeting_type=LOCATION
&targeting_value=LOCATION_ID
```

Multiple calls needed for different targeting types:

| targeting_type | targeting_value example |
|---|---|
| `LOCATION` | `b6b8d75a320f81d9` (use Search API to find IDs) |
| `AGE` | `AGE_25_TO_34` |
| `GENDER` | `female` |
| `INTEREST` | interest category ID |
| `FOLLOWER_LOOK_ALIKE` | `@competitorhandle` |
| `KEYWORD` | `summer fashion sale` |
| `DEVICE` | `smartphone` |

Search for location IDs:
GET `targeting_criteria/locations?q=Mumbai&location_type=CITY`

---

## Step 5: Create Promoted Tweet

First, post a regular tweet (or use an existing tweet ID), then promote it:

POST `accounts/{account_id}/line_items/{line_item_id}/promoted_tweets`

```
tweet_ids=TWEET_ID_HERE
```

To create a new tweet with a card (image + link):
POST `https://api.x.com/2/tweets`
```json
{
  "text": "Shop our Summer Sale — up to 50% off! 🛍️",
  "card_uri": "card://CARD_ID"
}
```

---

## Update Budget

POST `accounts/{account_id}/campaigns/{campaign_id}`

```
daily_budget_amount_local_micro=15000000
```

---

## Pause / Resume / Delete

POST `accounts/{account_id}/campaigns/{campaign_id}`

```
status=PAUSED        // pause
status=ACTIVE        // resume
status=DELETED       // delete (irreversible)
```

Same pattern works for line items and promoted tweets.

---

## Performance Reports (Analytics)

GET `stats/accounts/{account_id}`

```
?entity=CAMPAIGN
&entity_ids=CAMPAIGN_ID
&metric_groups=ENGAGEMENT,BILLING,VIDEO
&placement=ALL_ON_TWITTER
&start_time=2025-03-01T00:00:00Z
&end_time=2025-03-21T00:00:00Z
&granularity=DAY
```

Key metrics returned:
- `billed_engagements` — paid interactions
- `impressions` — times shown
- `clicks` — link clicks  
- `spend` — total spend in local currency (in micros — divide by 1,000,000)
- `video_views` — video completions
- `app_clicks` — app install clicks

---

## List Campaigns

GET `accounts/{account_id}/campaigns`
```
?with_deleted=false&count=100
```

---

## A/B Testing

Create two line items under the same campaign with identical settings except the test variable.
Give them clear names ("Test A — Image Ad" vs "Test B — Video Ad").
Use equal budgets. Review after 7+ days.

---

## Common Errors

| Error | Meaning |
|---|---|
| `INVALID_PARAMETER` | Check your form field names and values |
| `NO_ACTIVE_FUNDING_INSTRUMENTS` | No payment method set up — go to ads.twitter.com |
| `OVER_CAPACITY` | Too many active campaigns (200 limit) — pause or delete some |
| `UNAUTHORIZED` | OAuth credentials are wrong or expired |
| `CAMPAIGN_NOT_FOUND` | Wrong campaign ID or it was deleted |
