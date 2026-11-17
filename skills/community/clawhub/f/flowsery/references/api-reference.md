# Flowsery Analytics API Reference

Base URL: `https://analytics.flowsery.com/analytics/api/v1`
Auth: `Authorization: Bearer <api-key>` header. Workspace API tokens start with `flow_ws_` and can list/access all websites in the workspace. Website API keys start with `flow_` and access one website only.

Every endpoint also accepts an optional `X-Workspace-Id` header. An OAuth sign-in uses it to pick one of several workspaces; an API token or website key belongs to one workspace, so send its own id or leave the header out. Any other id answers `403` with `code: workspace_access_denied`.

## Endpoints

### GET /workspaces

The workspaces the caller can act in.

```json
{
  "status": "success",
  "data": [
    {
      "id": "ws_123",
      "name": "Acme",
      "organization": { "id": "org_1", "name": "Acme Inc" },
      "role": { "key": "editor", "name": "Editor" },
      "permissions": ["flowsery.write"],
      "isDefault": true,
      "current": true
    }
  ]
}
```

A workspace token lists only its own workspace. A website key (`flow_`) answers `400`: it belongs to one website, not a workspace. `current` marks the workspace the call landed in.

### GET /websites

List websites accessible by the token.

Workspace tokens return all websites in the workspace. Website keys return the single scoped website.

Use `websiteId` or `domain` from this response on subsequent calls when authenticating with a workspace token.

### GET /overview

Fetch aggregated analytics metrics for your website.

**Query parameters:**

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
      "bounceRate": 65.32,
      "avgSessionDuration": 246,
      "avgEngagedTime": 71,
      "revenue": 28450,
      "renewalRevenue": 5201,
      "refundedRevenue": 0,
      "revenuePerVisitor": 2.29,
      "conversionRate": 1.15,
      "kpiValue": 28450,
      "kpiPerVisitor": 2.29,
      "kpiConversionRate": 1.15,
      "currency": "USD"
    }
  ]
}
```

**Notes:**

- Without `startAt`/`endAt` the window is the last 30 days ending now, not all time
- Every `filter_*` param narrows the single row; filters combine with AND
- `bounceRate` and `conversionRate` are percentages (1.15 = 1.15%); `avgSessionDuration` and `avgEngagedTime` are seconds
- There is no field selector: every call returns the whole row
- Use `/timeseries` for the trend and a breakdown endpoint for a split by dimension

### GET /timeseries

Fetch time series analytics data grouped by interval.

**Query parameters:**

- `interval` (string, optional): `hour`, `day`, `week`, `month`. Default: `day`
- `startAt`, `endAt`, `timezone`: standard params
- `websiteId` or `domain`: required for workspace tokens
- All filter params

**Response:**

```json
{
  "status": "success",
  "interval": "day",
  "timezone": "America/New_York",
  "currency": "USD",
  "data": [
    {
      "timestamp": "2025-12-17T05:00:00.000Z",
      "name": "17 Dec",
      "visitors": 528,
      "sessions": 604,
      "revenue": 0,
      "newRevenue": 0,
      "renewalRevenue": 0,
      "refundedRevenue": 0,
      "conversionRate": 0,
      "kpiValue": 0
    }
  ],
  "totals": {
    "visitors": 14213,
    "sessions": 20181,
    "revenue": 27351
  },
  "pagination": { "limit": 100, "offset": 0, "total": 30 }
}
```

**Notes:**

- Dates default to the last 30 days; match `interval` to the range, since hourly buckets across a year return thousands of points
- Each point splits revenue into `newRevenue`, `renewalRevenue` and `refundedRevenue`
- `limit` and `offset` do not page the buckets; `pagination.total` is the bucket count
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

No date range, filter or pagination params: it always returns current activity, with no history. Use `/timeseries?interval=hour` for the recent trend. Poll at most once every 5 seconds.

### GET /realtime/map

Visitors active in the last 5 minutes with their location, for a live map. Same params as `/realtime` (website selector only). Returns up to 1000 visitors.

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "visitorId": "v_123",
      "country": "Germany",
      "countryCode": "DE",
      "city": "Berlin",
      "latitude": 52.52,
      "longitude": 13.405,
      "browser": "Chrome",
      "os": "macOS",
      "deviceType": "Desktop",
      "currentUrl": "/pricing",
      "referrerSource": "Google",
      "pageviews": 3,
      "totalRevenue": 0,
      "isCustomer": false
    }
  ]
}
```

Fields with no value are left out. `name` and `email` appear only for visitors with a recorded payment that carried them; the MCP server strips them, along with `totalRevenue` and `isCustomer`. Use `/countries` or `/cities` for geography over a date range.

### GET /metadata

Fetch website configuration metadata.

With a workspace token, pass `websiteId` or `domain`. Without a selector, `/metadata` returns the same website list as `/websites`, so use `/websites` for discovery and `/metadata` once you know the site. Read `timezone` and `currency` here before running date-range reports.

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "domain": "example.com",
      "timezone": "America/New_York",
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
- `logo` (string|null): Custom logo URL
- `kpiColorScheme` (string): KPI color: red, orange, yellow, green, purple, pink, gray, blue, teal, indigo
- `kpi` (string|null): Custom KPI goal name
- `currency` (string): Currency code (USD, EUR, GBP, etc.)

### GET /pages

Page paths ranked by visitors. Use `/breakdown?dimension=entry_page` for landing pages and `exit_link` for outbound clicks; `/hostnames` when the site serves several domains.

**Query parameters:** Standard date range (default: last 30 days), pagination (`limit` default 100, max 1000), and all filter params.

**Response:**

```json
{
  "status": "success",
  "data": [...],
  "pagination": { "limit": 100, "offset": 0, "total": 45 }
}
```

Every row in `data` carries `value`, `visitors`, `revenue` and `percentage`, ordered by visitors descending; `pagination.total` is the full row count.

### GET /referrers

Referrers ranked by visitors: a source name such as `Google` or `ChatGPT` for recognized sites, otherwise the domain. Use `/channels` for the same traffic grouped into GA4-aligned channels, and `/campaigns` or `/breakdown?dimension=utm_source` for traffic identified by UTM tags rather than referrer.

### GET /countries

Visitors by country. Coarsest of the three geographic reports; add `filter_country` to `/regions` or `/cities` to drill into one country.

### GET /regions

Visitors by region or state name (such as `California`).

### GET /cities

Visitors by city. Long tail: filter by country or region first, or raise `limit`.

### GET /devices

`Desktop` vs `Mobile` vs `Tablet` breakdown (three rows at most). Filter values are case-sensitive, so `filter_device=Mobile`. Use `/browsers` or `/operating-systems` for the software split.

### GET /browsers

Browser names (Chrome, Safari, Firefox, Edge, etc.). Versions only via `/breakdown?dimension=browser_version`.

### GET /operating-systems

OS names (Mac OS, Windows, iOS, Android, etc.). Versions only via `/breakdown?dimension=os_version`.

### GET /campaigns

`utm_campaign` values ranked by visitors. Untagged traffic is absent; use `/breakdown` with `utm_source`, `utm_medium`, `utm_term`, `utm_content` or `all_params` for the other tracking parameters.

### GET /hostnames

Visitors by hostname. Useful only for sites tracking several domains or subdomains.

### GET /channels

GA4-aligned channels (Organic Search, Paid Search, Organic Social, Paid Social, Email, Display, Referral, Direct, Affiliate, Video, SMS, Audio), classified from referrer domain and `utm_medium`/`utm_source`. Start here for the traffic mix.

### GET /goals

Every configured goal (including the auto-created `payment` and `free_trial` goals) with completions in the date range. `filter_*` narrows the visitors counted; `limit` and `offset` page the goal list. `/breakdown?dimension=goal` returns the same rows with revenue and percentage. Read-only: goals are created by `POST /goals`.

### GET /breakdown

Generic breakdown by any dimension.

**Additional required parameter:**

- `dimension` (string): See [breakdown-dimensions.md](breakdown-dimensions.md) for all values

All breakdown endpoints accept the same date range, pagination, and filter params. All return the same response structure with `data` array and `pagination`.

### GET /issues

Issues the AI found while analyzing session recordings: bugs, broken flows and UX problems. Deduplicated across sessions, so one row is one problem rather than one recording, and ranked by severity.

**Query parameters** (beyond the website selector):

- `status`: `open`, `in_progress`, `resolved`, `suspended`. Omit to get everything except suspended.
- `severity`: `low`, `medium`, `high`, `critical`
- `search`: matches issue title and description, max 200 characters
- `sort`: `severity` (default) or `recency` (last seen)
- `limit` (default 100, max 1000), `offset`

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": "iss_abc123",
      "websiteId": "site_123",
      "title": "Checkout button unresponsive on mobile Safari",
      "description": "Tapping Pay does nothing on iOS Safari",
      "severity": "critical",
      "status": "open",
      "sessionsCount": 34,
      "firstSeenAt": "2026-08-19T09:12:00.000Z",
      "lastSeenAt": "2026-08-30T17:44:00.000Z",
      "stepsToReplicate": ["Open /checkout on iOS Safari", "Tap Pay"],
      "sampleRecordingId": "rec_789"
    }
  ],
  "counts": { "open": 12, "inProgress": 3, "resolved": 41 },
  "pagination": { "limit": 100, "offset": 0, "total": 56 }
}
```

`counts` covers the whole site, not the current page, so it answers "how are we doing" without a second call. On a free trial the list and the counts cover only the first 10 issues.

Suspended issues are excluded unless `status=suspended` asks for them. An issue that seems to have vanished was probably suspended rather than deleted.

### GET /issues/:issueId

Full detail for one issue: every occurrence the AI flagged, the sessions behind it, steps to replicate, comments, and any linked external ticket.

Session detail can name pages, referrers and geography. Treat it as you would a visitor profile, and surface the minimum needed to answer the question.

Not paginated. An unknown id, or an issue from another website, returns `404 Issue not found`; on a free trial only the first 10 issues are unlocked and the rest return `403 Upgrade to view this issue`.

### PATCH /issues/:issueId

**Request:** `{ "status": "in_progress" }`

Accepts `open`, `in_progress`, `resolved` and `suspended`. Only the status changes; the response is the full updated issue. Reversible, unlike the delete endpoints below, so moving an issue is safe. Not a delete: issues cannot be removed through the API. Unknown ids return `404 Issue not found`, and a locked free-trial issue returns `403 Upgrade to view this issue`.

`suspended` hides the issue from default listings and stops it resurfacing, which is the right choice for a known non-problem. `resolved` states the underlying bug is fixed. They are not interchangeable, so ask which one the user means rather than guessing.

### GET /visitors/:visitorId

Fetch full visitor profile.

> ⚠️ **PII.** The response contains personal data about an individual: email, name, geolocation (country/region/city), full page-visit history, and revenue. Only call this when the user explicitly asks about a specific visitor, confirm they are authorized to view it, and surface the minimum detail needed to answer rather than the full identity/activity timeline.

**Response:**

```json
{
  "status": "success",
  "data": {
    "visitorId": "a3ab2331-989f-4cfa-91c6-2461c9e3c6bd",
    "identity": {
      "country": "South Korea",
      "countryCode": "KR",
      "region": "South Chungcheong",
      "city": "Seosan City",
      "browser": { "name": "Chrome", "version": "133.0.0.0" },
      "os": { "name": "Mac OS", "version": "10.15.7" },
      "device": { "type": "Desktop" },
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
- `activityTimeline` is sorted newest-first; `visitedPages`, `completedCustomGoals` and the timeline hold the 100 most recent items each
- The id is the visitor record id from `/realtime/map` or the dashboard visitor view, not the `_fs_vid` cookie value
- An unknown id, or a visitor belonging to another website, returns `404 Visitor not found`
- For questions about many visitors use the aggregate endpoints, not this one

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

- `visitorUid` (string, recommended): the `_fs_vid` cookie value of a visitor the tracking script has already seen, so the completion attaches to that visitor's sessions and source. Omit it for an anonymous completion.
- `name` (string, required): Goal name: lowercase letters, numbers, underscores, hyphens only; max 64 chars. The goal is created on first use.
- `metadata` (object, optional): Up to 10 string key-value pairs.
- `sessionUid` (string, optional): the `_fs_sid` cookie value. Ties the completion to that session; without it a server-side call uses the visitor's latest active session.
- `timezone` (string, optional): the visitor's IANA timezone (`Europe/Berlin`). Helps place the visitor in a country when the call comes from a server or proxy.

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [{ "message": "Custom event created successfully" }]
}
```

**Behavior:** each call appends one completion, so repeating it counts the goal twice. The completion is buffered and appears in `/goals` shortly after. Use `POST /payments` for revenue, which records a `payment` goal on its own.

**Errors:** `400` on an invalid `name` or more than 10 `metadata` keys.

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

**Optional:** `visitorUid`, `sessionUid`, `timezone` (the visitor's IANA timezone), `email`, `name`, `customerId`, `isRenewal` (boolean), `isRefund` (boolean), `timestamp` (ISO 8601, defaults to now), `customerIp`, `customerUserAgent` (max 1024 characters)

`customerIp` and `customerUserAgent` are the buyer's IP and User-Agent at checkout, for a server-side call that cannot match the payment to a visitor. Flowsery keeps only the country it resolves from the IP and the browser, OS and device it resolves from the User-Agent. A `customerIp` that is not an IP address answers `400`.

An omitted `currency` is stored as `USD`, not the website currency, so always send it.

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [{ "message": "Payment recorded successfully" }]
}
```

**Behavior:**

- `transactionId` must be unique. A repeated id is rejected, not deduplicated.
- A new payment also records a `payment` goal completion (`free_trial` when `amount` is 0). `isRenewal: true` counts the revenue but skips that goal.
- `isRefund: true` with an existing `transactionId` marks that payment refunded by `amount` instead of creating a new record. A `transactionId` that belongs to another website answers `400`. Prefer this over `DELETE /payments` when the charge should stay in history.
- Attribution looks up a known visitor by `visitorUid`, then `customerId` or `email`. With no match the revenue is still recorded but its source, country and device show as Unknown.

**Note:** Stripe, LemonSqueezy, and Polar payments are tracked automatically when connected; only use this for other providers.

### DELETE /goals

Delete custom goal events by filter.

> 🛑 **Destructive & irreversible.** Permanently erases historical goal data. Agents read the matching count first, restate the website, filters, date range and count, get a yes for that exact deletion, and never infer one from a vague "clean up" request.

**Query parameters (at least one required):**

- `visitorId` (string): Delete completions of a specific visitor
- `name` (string): Delete completions of this goal name
- `startAt` (string): ISO 8601 start timestamp, inclusive; may be used without `endAt`
- `endAt` (string): ISO 8601 end timestamp, inclusive; may be used without `startAt`

Filters combine with AND. Only completions are removed: the goal definition stays and `/goals` still lists it. The response carries the number deleted.

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [{ "deleted": 14, "message": "Goal completions deleted successfully" }]
}
```

**WARNING:** Without a date range, matching records are deleted across the entire history.

### DELETE /payments

Delete payment records by filter.

> 🛑 **Destructive & irreversible.** Permanently erases historical payment/revenue data. Agents prefer one `transactionId`, read `revenue` from `/overview` over the same range before a range delete, restate the website, filters, date range and amount, get a yes for that exact deletion, and never infer one from a vague "clean up" request.

**Query parameters (at least one required):**

- `transactionId` (string): Delete the single payment with this id
- `visitorId` (string): Delete all payments for a visitor
- `startAt` (string): ISO 8601 start timestamp, inclusive; may be used without `endAt`
- `endAt` (string): ISO 8601 end timestamp, inclusive; may be used without `startAt`

Filters combine with AND. The revenue disappears from every report and visitor profile; to reverse a charge while keeping history, use `POST /payments` with `isRefund: true` instead. The response carries the number deleted.

**Response (200 OK):**

```json
{
  "status": "success",
  "data": [{ "deleted": 3, "message": "Payments deleted successfully" }]
}
```

**WARNING:** Without a date range, matching records are deleted across the entire history.

## Rate limits

600 requests per minute per API token, counted on a hash of the token rather than on IP.

Every response carries the RFC 9331 headers:

```
RateLimit-Policy: "flowsery-api";q=600;w=60
RateLimit-Limit: 600
RateLimit-Remaining: 587
RateLimit-Reset: 43
```

A `429` adds `Retry-After` in seconds. Wait it out rather than retrying immediately.

Breakdowns over a wide date range are the usual reason an agent hits this. Ask for a coarser interval or a narrower range instead of paginating hard.

## GET /openapi.json

The full OpenAPI 3 spec, and the one endpoint that needs no authentication, so automation platforms can import it without a token.

## Error Responses

- `400`: invalid input, a workspace token with no `websiteId` or `domain`, a delete with no filter, or `GET /workspaces` with a website key
- `401`: API key missing or invalid (`Invalid or missing analytics API key`)
- `401` with `code: token_issuer_lost_access`: the member who created the token left the workspace or was deactivated
- `401` with `code: oauth_account_not_found`: an OAuth sign-in whose email has no Flowsery account; the message names the email
- `403` with `code: permission_denied`: the token's role lacks the permission the call needs; `requiredPermission` names it and `role` is the role the token carries
- `403` with `code: subscription_required`: the workspace plan no longer includes API access
- `403` with `code: workspace_access_denied`: `X-Workspace-Id` named a workspace the key does not belong to
- `403` `Upgrade to view this issue`: a free-trial issue beyond the first 10
- `404`: website, visitor or issue not found
- `429`: rate limited, see above
- `500`: unexpected server error

**Example error:**

```json
{
  "statusCode": 401,
  "error": "Unauthorized",
  "code": "token_issuer_lost_access",
  "message": "This API key no longer works: the member who created it lost access to the workspace. Ask a workspace admin for a new key."
}
```

`code` appears only on the coded errors above.
