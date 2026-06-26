---
name: flowsery
description: Query web analytics data from Flowsery Analytics — a privacy-first web analytics platform. Retrieve real-time visitors, time series, breakdowns (device, page, country, referrer, campaign, channel, exit link, and 24 dimensions total), and visitor profiles with activity timelines. Also supports a small set of write operations that require explicit user confirmation: creating custom goal/payment records, and permanently (irreversibly) deleting goal events and payment records. Visitor profiles and payments include personal data (email, name, location, revenue) — handle as PII. Use when the user wants to check their website traffic, analyze visitor behavior, view revenue data, track conversions, or manage goal/payment records on their Flowsery-tracked sites.
homepage: https://flowsery.com
metadata: { 'openclaw': { 'emoji': '📊', 'primaryEnv': 'FLOWSERY_API_KEY', 'requires': { 'env': ['FLOWSERY_API_KEY'] } } }
---

# Flowsery Analytics

Privacy-first web analytics. Query real-time visitors, breakdowns, time series, revenue, goals, and visitor profiles — all via one API.

## Safety & Privacy (read first)

This skill is read-only by default, but the API also exposes **write** and **irreversible delete** operations and returns **personal data**. Before acting, observe these rules:

- **Destructive operations require confirmation.** `DELETE /goals` and `DELETE /payments` permanently erase historical business data and cannot be undone. Never run them as a side effect of an analytics request. Always restate exactly what will be deleted (website, filters, date range, and how many records if known) and get explicit user confirmation first. Never run a DELETE without a date range or other narrowing filter unless the user has explicitly confirmed a full-history wipe.
- **Treat a request to "clean up", "fix", or "remove" data as deletion, not querying** — confirm intent before translating it into a DELETE call.
- **Visitor profiles and payments are PII.** Profiles can contain email, name, geolocation, full page history, and revenue. Only retrieve an individual visitor profile when the user explicitly asks about a specific person/visitor, and confirm they are authorized to view it. Present the minimum detail needed to answer — do not dump full identity, contact, and activity timelines unless asked.
- **Minimize personal data on writes.** When recording payments/goals, send only the fields required for the task. Do not add `email`, `name`, or `customerId` unless the user explicitly provides them and they are needed for attribution.
- **Never expose API keys** in output, logs, or client-side code.

## Setup

1. Sign up at https://flowsery.com/signup
2. Add your website and install the tracking snippet
3. Go to the workspace-level API Tokens page and create a workspace API token
4. Set the environment variable:
   ```bash
   export FLOWSERY_API_KEY="flow_ws_your-token-here"
   ```

Base URL: `https://analytics.flowsery.com/analytics/api/v1`
Auth header: `Authorization: Bearer $FLOWSERY_API_KEY`

Workspace API tokens use the `flow_ws_` prefix. Use these for API, MCP, OpenClaw, and multi-website access. Website API keys use the `flow_` prefix and are scoped to a single website, mainly for server-side custom goal and payment ingestion. Treat both like passwords — never expose them in client-side code.

## Core Workflow

### 1. List accessible websites

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  https://analytics.flowsery.com/analytics/api/v1/websites
```

With a workspace token, choose the website and pass `websiteId=<id>` or `domain=<domain>` on subsequent API calls. With a website key, this returns only the scoped website.

### 2. Check website metadata

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/metadata?websiteId=WEBSITE_ID"
```

Returns `{ "status": "success", "data": [{ "domain", "timezone", "name", "logo", "kpiColorScheme", "kpi", "currency" }] }`. Use the `timezone` and `currency` values for subsequent queries.

### 3. Get site overview (aggregated metrics)

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/overview?websiteId=WEBSITE_ID&startAt=2026-01-01&endAt=2026-01-31&timezone=America/New_York"
```

Returns: `visitors`, `sessions`, `bounce_rate`, `avg_session_duration`, `revenue`, `revenue_per_visitor`, `conversion_rate`.

Omit date params for all-time data. Use `fields` param to select specific metrics: `?fields=visitors,revenue`.

### 4. Get time series data

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/timeseries?websiteId=WEBSITE_ID&interval=day&fields=visitors,sessions,revenue&startAt=2026-03-01&endAt=2026-03-31"
```

Intervals: `hour`, `day`, `week`, `month`. Returns timestamped data buckets with totals.

Response includes `data` array, `totals` object (with `visitors`, `sessions`, `revenue`, `revenueBreakdown`), and `pagination`.

### 5. Check real-time visitors

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/realtime?websiteId=WEBSITE_ID"
```

Returns `{ "data": [{ "visitors": 42 }] }` — active visitors in the last 5 minutes.

### 6. Get breakdown reports

Each returns top items for a dimension with visitor/session counts. All accept date range, pagination, and filter params.

```bash
# Top pages
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/pages?websiteId=WEBSITE_ID&startAt=2026-03-01&endAt=2026-03-31&limit=20"

# Top referrers
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/referrers?websiteId=WEBSITE_ID&startAt=2026-03-01&endAt=2026-03-31"

# Countries
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/countries?websiteId=WEBSITE_ID&startAt=2026-03-01&endAt=2026-03-31"

# Devices (desktop/mobile/tablet)
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/devices?websiteId=WEBSITE_ID&startAt=2026-03-01&endAt=2026-03-31"

# Marketing channels
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/channels?websiteId=WEBSITE_ID&startAt=2026-03-01&endAt=2026-03-31"
```

Available breakdown endpoints: `pages`, `referrers`, `countries`, `regions`, `cities`, `devices`, `browsers`, `operating-systems`, `campaigns`, `hostnames`, `channels`, `goals`.

For any dimension, use the generic breakdown:

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/breakdown?websiteId=WEBSITE_ID&dimension=utm_source&startAt=2026-03-01&endAt=2026-03-31"
```

See [references/breakdown-dimensions.md](references/breakdown-dimensions.md) for all 24 dimensions.

### 7. Get a visitor profile

> ⚠️ **PII.** This endpoint returns personal data about an individual (email, name, city/region, full page history, revenue). Only call it when the user explicitly asks about a specific visitor, confirm they are authorized to view that person's data, and present the minimum detail that answers the question — don't dump the full identity and activity timeline unless asked.

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/visitors/VISITOR_ID_HERE?websiteId=WEBSITE_ID"
```

Returns comprehensive visitor data:

- **identity**: country, region, city, browser, OS, device type, viewport
- **source**: original traffic source with favicon URL
- **activity**: visit count, page views, first/last visit, visited pages, completed goals
- **revenue**: total revenue, customer flag, time to first conversion (seconds)
- **profile**: identified user data (userId, name, email) or null for anonymous visitors
- **activityTimeline**: merged chronological list of all pageviews, goals, and payments

The visitor ID comes from the `_fs_vid` browser cookie set by the Flowsery tracking script.

### 8. Track a custom goal

```bash
curl -X POST https://analytics.flowsery.com/analytics/api/v1/goals \
  -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "websiteId": "WEBSITE_ID",
    "visitorUid": "VISITOR_UID_FROM_COOKIE",
    "name": "newsletter_signup",
    "metadata": { "plan": "pro", "source": "pricing_page" }
  }'
```

- `name` (required): lowercase letters, numbers, underscores, hyphens; max 64 chars
- `visitorUid` (recommended): from the `_fs_vid` browser cookie
- `metadata` (optional): up to 10 key-value pairs (keys: lowercase, max 64 chars; values: max 255 chars)

The visitor must have at least one recorded pageview before a goal can be created.

### 9. Record a payment

> If you use Stripe, LemonSqueezy, or Polar, payments are tracked automatically when connected. Use this endpoint only for other providers.

> ⚠️ **PII / data minimization.** `email`, `name`, and `customerId` are personal data and are all optional. Send them only when the user explicitly provides them and they are needed for revenue attribution. Omit them otherwise — `amount`, `currency`, and `transactionId` are enough to record a payment.

```bash
curl -X POST https://analytics.flowsery.com/analytics/api/v1/payments \
  -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "websiteId": "WEBSITE_ID",
    "amount": 29.99,
    "currency": "USD",
    "transactionId": "payment_456",
    "visitorUid": "VISITOR_UID_FROM_COOKIE",
    "email": "customer@example.com"
  }'
```

Required: `amount`, `currency`, `transactionId`. Optional: `visitorUid`, `sessionUid`, `email`, `name`, `customerId`, `isRenewal` (boolean), `isRefund` (boolean).

### 10. Delete goal events (irreversible — confirm first)

> 🛑 **Destructive.** This permanently erases historical goal data and cannot be undone. Before running it, restate the website, filters, and date range to the user and get explicit confirmation. Do not infer a DELETE from a vague "clean up"/"fix" request.

```bash
curl -X DELETE "https://analytics.flowsery.com/analytics/api/v1/goals?websiteId=WEBSITE_ID&name=signup&startAt=2026-01-01T00:00:00Z&endAt=2026-01-31T23:59:59Z" \
  -H "Authorization: Bearer $FLOWSERY_API_KEY"
```

At least one filter required: `visitorId`, `name`, `startAt`, `endAt`.

**WARNING**: Without a date range, matching records are deleted across the entire history. Never omit the date range unless the user has explicitly confirmed a full-history wipe.

### 11. Delete payment records (irreversible — confirm first)

> 🛑 **Destructive.** This permanently erases historical payment/revenue data and cannot be undone. Before running it, restate the website, filters, and date range to the user and get explicit confirmation. Do not infer a DELETE from a vague "clean up"/"fix" request.

```bash
curl -X DELETE "https://analytics.flowsery.com/analytics/api/v1/payments?websiteId=WEBSITE_ID&transactionId=payment_456" \
  -H "Authorization: Bearer $FLOWSERY_API_KEY"
```

At least one filter required: `transactionId`, `visitorId`, `startAt`, `endAt`.

**WARNING**: Without a date range, matching records are deleted across the entire history. Never omit the date range unless the user has explicitly confirmed a full-history wipe.

## Query Parameters

### Date range & pagination (all GET endpoints)

| Param       | Type    | Description                                                          |
| ----------- | ------- | -------------------------------------------------------------------- |
| `startAt`   | string  | ISO 8601 start date (e.g. `2026-01-01`)                              |
| `endAt`     | string  | ISO 8601 end date (e.g. `2026-01-31`)                                |
| `timezone`  | string  | IANA timezone (e.g. `America/New_York`). Falls back to site default. |
| `limit`     | integer | Max results, 1-1000 (default: 100)                                   |
| `offset`    | integer | Pagination offset (default: 0)                                       |
| `websiteId` | string  | Website to query when using a workspace token                        |
| `domain`    | string  | Website domain to query when using a workspace token                 |

### Filters (all GET endpoints)

All filters use the `filter_` prefix.

| Filter                | Description                                    |
| --------------------- | ---------------------------------------------- |
| `filter_country`      | Country name or code                           |
| `filter_region`       | Region or state                                |
| `filter_city`         | City name                                      |
| `filter_device`       | Device type: `desktop`, `mobile`, `tablet`     |
| `filter_browser`      | Browser: `Chrome`, `Safari`, `Firefox`, `Edge` |
| `filter_os`           | OS: `Mac OS`, `Windows`, `iOS`, `Android`      |
| `filter_referrer`     | Referrer domain                                |
| `filter_ref`          | `ref` URL parameter value                      |
| `filter_source`       | `source` URL parameter value                   |
| `filter_via`          | `via` URL parameter value                      |
| `filter_utm_source`   | UTM source                                     |
| `filter_utm_medium`   | UTM medium                                     |
| `filter_utm_campaign` | UTM campaign                                   |
| `filter_utm_term`     | UTM term                                       |
| `filter_utm_content`  | UTM content                                    |
| `filter_page`         | Page path                                      |
| `filter_hostname`     | Hostname/domain                                |
| `filter_entry_page`   | Landing page                                   |
| `filter_channel`      | Marketing channel                              |
| `filter_goal`         | Goal name                                      |

Combine multiple filters to drill down:

```bash
curl -s -H "Authorization: Bearer $FLOWSERY_API_KEY" \
  "https://analytics.flowsery.com/analytics/api/v1/pages?websiteId=WEBSITE_ID&filter_country=United%20States&filter_device=mobile&startAt=2026-03-01&endAt=2026-03-31"
```

## Response Format

**Success (200 OK):**

```json
{
  "status": "success",
  "data": { ... }
}
```

**Error:**

```json
{
  "status": "error",
  "error": { "code": 401, "message": "A descriptive error message" }
}
```

Error codes: `400` (invalid input), `401` (bad API key), `404` (not found), `500` (server error).

## Marketing Channels

Flowsery auto-classifies traffic into GA4-aligned channels:

| Channel        | How it's classified                                                 |
| -------------- | ------------------------------------------------------------------- |
| Organic Search | Google, Bing, DuckDuckGo, etc.                                      |
| Paid Search    | utm_medium: cpc, ppc, paid_search                                   |
| Organic Social | Facebook, Twitter, LinkedIn, Reddit, etc.                           |
| Paid Social    | utm_medium: paid_social, social_cpc                                 |
| Email          | utm_medium: email, newsletter; or source: mailchimp, sendgrid, etc. |
| Display        | utm_medium: display, banner, cpm                                    |
| Referral       | Other websites                                                      |
| Direct         | No referrer                                                         |
| Affiliate      | utm_medium: affiliate, partner                                      |
| Video          | utm_medium: video, paid_video                                       |
| SMS            | utm_medium: sms                                                     |
| Audio          | utm_medium: audio, podcast                                          |

## Tips for the Agent

### Read-only by default

Most commands are safe GET queries. The only write operations are:

- `POST /goals` — track a goal event
- `POST /payments` — record a payment
- `DELETE /goals` — delete goal events (irreversible)
- `DELETE /payments` — delete payment records (irreversible)

**Always confirm with the user before running DELETE operations.**

### Date handling

- When the user says "this month", "last week", "yesterday" — calculate the actual ISO dates
- Default to the last 30 days when no date range is specified
- With a workspace token, call `/websites` first and choose a `websiteId` or `domain`
- Always use UTC or the site's timezone (from the metadata endpoint)

### Revenue data is sensitive

When displaying payment or revenue data, ask the user about the appropriate level of detail before dumping raw numbers.

### Polling

Do not poll the `realtime` endpoint more than once per 5 seconds.

### Common agent tasks

| User says                          | What to do                                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| "How's my traffic?"                | Call `overview` with last 30 days                                                           |
| "What are my top pages?"           | Call `pages` with date range                                                                |
| "Where is my traffic coming from?" | Call `referrers` or `channels`                                                              |
| "How many visitors right now?"     | Call `realtime`                                                                             |
| "Show me traffic trends"           | Call `timeseries` with `interval=day`                                                       |
| "Who is this visitor?"             | Call `visitors/{id}`                                                                        |
| "Track a signup"                   | Call `POST /goals` with name and visitor UID                                                |
| "How's my revenue?"                | Call `overview` with `fields=revenue,conversion_rate` or `timeseries` with `fields=revenue` |
| "Break down traffic by country"    | Call `countries`                                                                            |
| "Show me mobile vs desktop"        | Call `devices`                                                                              |
| "What campaigns are working?"      | Call `campaigns` or `breakdown?dimension=utm_source`                                        |
