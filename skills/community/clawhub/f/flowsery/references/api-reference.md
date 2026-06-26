# Flowsery Analytics API Reference

Base URL: `https://analytics.flowsery.com/analytics/api/v1`
Auth: `Authorization: Bearer <api-key>` header. Workspace API tokens start with `flow_ws_` and can list/access all websites in the workspace. Website API keys start with `flow_` and access one website only.

## Endpoints

### GET /websites

List websites accessible by the token.

Workspace tokens return all websites in the workspace. Website keys return the single scoped website.

Use `websiteId` or `domain` from this response on subsequent calls when authenticating with a workspace token.

### GET /overview

Fetch aggregated analytics metrics for your website.

**Query parameters:**

- `fields` (string, optional): Comma-separated list of metrics. Accepted: `visitors`, `sessions`, `bounce_rate`, `avg_session_duration`, `currency`, `revenue`, `revenue_per_visitor`, `conversion_rate`. Omit to receive all.
- `startAt` (string, optional): ISO 8601 start date
- `endAt` (string, optional): ISO 8601 end date
- `timezone` (string, optional): IANA timezone. Falls back to site default.
- `websiteId` or `domain` (string, required for workspace tokens): Website selector
- All filter params (see SKILL.md)

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "visitors": 12450,
      "sessions": 16890,
      "bounce_rate": 65.32,
      "avg_session_duration": 245678.45,
      "currency": "$",
      "revenue": 28450,
      "revenue_per_visitor": 2.29,
      "conversion_rate": 1.15
    }
  ]
}
```

**Notes:**

- Returns all-time data when no date range specified
- Conversion rate is a percentage (1.15 = 1.15%)

### GET /timeseries

Fetch time series analytics data grouped by interval.

**Query parameters:**

- `fields` (string): Comma-separated metrics: `visitors`, `sessions`, `revenue`, `conversion_rate`, `name`
- `interval` (string, optional): `hour`, `day`, `week`, `month`. Default: `day`
- `startAt`, `endAt`, `timezone`, `limit`, `offset` — standard params
- `websiteId` or `domain` — required for workspace tokens
- All filter params

**Response:**

```json
{
  "status": "success",
  "fields": ["visitors", "sessions", "revenue"],
  "interval": "day",
  "timezone": "America/New_York",
  "currency": "$",
  "totals": {
    "visitors": 14213,
    "sessions": 20181,
    "revenue": 27351,
    "revenueBreakdown": { "new": 22150.0, "renewal": 5201.0, "refund": 0.0 },
    "conversion_rate": 1.92
  },
  "data": [
    {
      "visitors": 528,
      "name": "17 Dec",
      "sessions": 604,
      "revenue": 0,
      "revenueBreakdown": { "new": 0.0, "renewal": 0.0, "refund": 0.0 },
      "conversion_rate": 0,
      "timestamp": "2025-12-17T00:00:00+05:30"
    }
  ],
  "pagination": { "limit": 100, "offset": 0, "total": 30 }
}
```

**Notes:**

- Same-day queries auto-upgrade to hourly granularity
- Revenue always includes `revenueBreakdown` with new, renewal, refund
- Timestamps follow ISO 8601

### GET /realtime

Fetch current active visitor count (activity within last 5 minutes).

**Response:**

```json
{
  "status": "success",
  "data": [{ "visitors": 42 }]
}
```

No date range params supported — always returns current activity.

### GET /metadata

Fetch website configuration metadata.

With a workspace token, pass `websiteId` or `domain`. Without a selector, `/metadata` returns the same website list as `/websites`.

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "domain": "example.com",
      "timezone": "America/New_York",
      "name": "My Website",
      "logo": "https://cdn.example.com/logo.png",
      "kpiColorScheme": "orange",
      "kpi": "signup",
      "currency": "USD"
    }
  ]
}
```

Fields:

- `domain` (string): Website domain
- `timezone` (string): IANA timezone
- `name` (string): Display name
- `logo` (string|null): Custom logo URL
- `kpiColorScheme` (string): KPI color: red, orange, yellow, green, purple, pink, gray, blue, teal, indigo
- `kpi` (string|null): Custom KPI goal name
- `currency` (string): Currency code (USD, EUR, GBP, etc.)

### GET /pages

Top pages by visitor count.

**Query parameters:** Standard date range, pagination, and all filter params.

**Response:**

```json
{
  "status": "success",
  "data": [...],
  "pagination": { "limit": 100, "offset": 0, "total": 45 }
}
```

### GET /referrers

Traffic sources (referrer domains).

### GET /countries

Visitors by country.

### GET /regions

Visitors by region/state.

### GET /cities

Visitors by city.

### GET /devices

Desktop vs mobile vs tablet breakdown.

### GET /browsers

Browser distribution (Chrome, Safari, Firefox, Edge, etc.).

### GET /operating-systems

OS distribution (Mac OS, Windows, iOS, Android, etc.).

### GET /campaigns

UTM campaign performance.

### GET /hostnames

Traffic by hostname/domain.

### GET /channels

Marketing channel breakdown (Organic Search, Paid Search, Social, Email, Direct, Referral, etc.).

### GET /goals

Goal completion stats within date range.

### GET /breakdown

Generic breakdown by any dimension.

**Additional required parameter:**

- `dimension` (string): See [breakdown-dimensions.md](breakdown-dimensions.md) for all values

All breakdown endpoints accept the same date range, pagination, and filter params. All return the same response structure with `data` array and `pagination`.

### GET /visitors/:visitorId

Fetch full visitor profile.

> ⚠️ **PII.** The response contains personal data about an individual — email, name, geolocation (country/region/city), full page-visit history, and revenue. Only call this when the user explicitly asks about a specific visitor, confirm they are authorized to view it, and surface the minimum detail needed to answer rather than the full identity/activity timeline.

**Response:**

```json
{
  "status": "success",
  "data": {
    "visitorId": "a3ab2331-989f-4cfa-91c6-2461c9e3c6bd",
    "identity": {
      "country": "South Korea",
      "countryCode": "KR",
      "region": "KR-44",
      "city": "Seosan City",
      "browser": { "name": "Chrome", "version": "133.0.0.0" },
      "os": { "name": "Mac OS", "version": "10.15.7" },
      "device": { "type": "desktop" },
      "viewport": { "width": 1728, "height": 998 }
    },
    "source": "youtube.com",
    "sourceIconUrl": "https://icons.duckduckgo.com/ip3/youtube.com.ico",
    "activity": {
      "visitCount": 3,
      "pageViewCount": 8,
      "firstVisitAt": "2025-04-11T03:38:49.154Z",
      "lastVisitAt": "2025-04-11T03:38:49.154Z",
      "currentUrl": "example.com/",
      "visitedPages": [{ "url": "example.com/", "timestamp": "2025-04-11T03:38:49.154Z" }],
      "completedCustomGoals": [{ "name": "newsletter_signup", "timestamp": "2025-04-11T03:38:54.253Z" }]
    },
    "revenue": {
      "totalRevenue": 29.99,
      "isCustomer": true,
      "timeToFirstConversion": 3600
    },
    "profile": {
      "userId": "usr_123",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "activityTimeline": [
      {
        "type": "payment",
        "timestamp": "2025-04-11T04:38:49.154Z",
        "url": null,
        "eventName": null,
        "amount": 29.99
      },
      {
        "type": "goal",
        "timestamp": "2025-04-11T03:38:54.253Z",
        "url": null,
        "eventName": "newsletter_signup",
        "amount": null
      },
      {
        "type": "pageview",
        "timestamp": "2025-04-11T03:38:49.154Z",
        "url": "example.com/",
        "eventName": null,
        "amount": null
      }
    ]
  }
}
```

**Notes:**

- `profile` is null for anonymous visitors (only populated after `identify` call)
- `timeToFirstConversion` is in seconds, or null if no payment recorded
- `activityTimeline` is sorted newest-first

### POST /goals

Track a custom goal event.

**Request:**

```json
{
  "visitorUid": "visitor-uid-from-cookie",
  "name": "newsletter_signup",
  "metadata": {
    "plan": "pro",
    "source": "pricing_page"
  }
}
```

**Fields:**

- `visitorUid` (string, recommended): Visitor ID from `_fs_vid` browser cookie
- `name` (string, required): Goal name — lowercase letters, numbers, underscores, hyphens only; max 64 chars
- `metadata` (object, optional): Up to 10 key-value pairs. Keys: lowercase, max 64 chars. Values: max 255 chars. HTML stripped.

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [{ "message": "Custom event created successfully" }]
}
```

**Errors:** `400` if visitor is a bot. `404` if no pageview exists for the visitor.

### POST /payments

Record a payment for revenue attribution.

> ⚠️ **PII / data minimization.** `email`, `name`, and `customerId` are personal data and are all optional. Send them only when the user explicitly provides them and they are needed for attribution; omit them otherwise. `amount`, `currency`, and `transactionId` alone are sufficient to record a payment.

**Request:**

```json
{
  "amount": 29.99,
  "currency": "USD",
  "transactionId": "payment_456",
  "visitorUid": "visitor-uid-from-cookie",
  "email": "customer@example.com",
  "name": "John Doe",
  "customerId": "cus_123",
  "isRenewal": false,
  "isRefund": false
}
```

**Required:** `amount` (number), `currency` (string), `transactionId` (string)

**Optional:** `visitorUid`, `sessionUid`, `email`, `name`, `customerId`, `isRenewal` (boolean), `isRefund` (boolean)

**Response (200 OK):**

```json
{
  "message": "Payment recorded and attributed successfully",
  "transaction_id": "payment_456"
}
```

**Note:** Stripe, LemonSqueezy, and Polar payments are tracked automatically when connected — only use this for other providers.

### DELETE /goals

Delete custom goal events by filter.

> 🛑 **Destructive & irreversible.** Permanently erases historical goal data. Agents must confirm the website, filters, and date range with the user before calling, and must not infer this from a vague "clean up" request.

**Query parameters (at least one required):**

- `visitorId` (string): Delete goals for a specific visitor
- `name` (string): Delete goals matching event name
- `startAt` (string): ISO 8601 start timestamp
- `endAt` (string): ISO 8601 end timestamp

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [{ "deleted": 14, "message": "Goal events deleted successfully" }]
}
```

**WARNING:** Without a date range, matching records are deleted across the entire history.

### DELETE /payments

Delete payment records by filter.

> 🛑 **Destructive & irreversible.** Permanently erases historical payment/revenue data. Agents must confirm the website, filters, and date range with the user before calling, and must not infer this from a vague "clean up" request.

**Query parameters (at least one required):**

- `transactionId` (string): Delete specific transaction
- `visitorId` (string): Delete all payments for a visitor
- `startAt` (string): ISO 8601 start timestamp
- `endAt` (string): ISO 8601 end timestamp

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [{ "deleted": 3, "message": "Payment records deleted successfully" }]
}
```

**WARNING:** Without a date range, matching records are deleted across the entire history.

## Error Responses

- `400` — Invalid input, missing required parameters, or validation error
- `401` — API key missing or invalid
- `404` — Resource not found (unknown visitor, website not found)
- `500` — Unexpected server error

**Example error:**

```json
{
  "status": "error",
  "error": { "code": 401, "message": "Invalid or missing API key" }
}
```
