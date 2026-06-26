# API Discovery Procedure

## Overview

Most modern websites fetch data from APIs. Finding and calling these APIs directly is faster, more reliable, and less token-intensive than automating the UI. This is the single most valuable browser technique.

## Step 1: Open the Page

```
browser open url="https://example.com/data-page"
```

Wait for load. Take a snapshot to confirm the page rendered.

## Step 2: Check the Console for Network Activity

```
browser console
```

Look for fetch/XHR requests in the output. The data you want is usually loaded via:
- `/api/...` endpoints
- `/graphql` endpoints
- JSON responses containing the data visible on the page

## Step 3: Identify the Data Endpoint

Common patterns:
- `GET /api/v1/items?page=1&limit=20` — REST pagination
- `POST /graphql` with a query body — GraphQL
- `GET /api/search?q=keyword` — search endpoints
- Internal fetch to same domain: `/api/internal/...`

Look for:
- URLs containing `/api/`, `/v1/`, `/v2/`, `/graphql`
- Responses with JSON content type
- Requests that fire when you scroll or click "load more"

## Step 4: Replicate the Request

Once you find the endpoint, call it directly:

```bash
# REST example
curl -s "https://example.com/api/v1/items?page=1&limit=100" \
  -H "Cookie: session=..." | python3 -m json.tool

# Or use web_fetch
web_fetch url="https://example.com/api/v1/items?page=1&limit=100"
```

For authenticated endpoints, you may need cookies from the browser session. Check if the API works without auth first (many do for read-only data).

## Step 5: Paginate or Batch

Most APIs support pagination:
- `?page=1&limit=100` — offset pagination
- `?cursor=abc123` — cursor pagination
- `?offset=0&count=50` — offset/count

Loop through pages until you get all the data. This is typically 100x faster than scrolling through a UI.

## Real Example: Carpark Data

**Task:** Get parking rates for 1,000 Singapore carparks from sgcarmart.com

**UI approach (failed):** Playwright script clicking through pages. 8 hours, 0 usable results. Site had bot detection, dynamic URLs, redirects.

**API discovery approach (worked):**
1. Opened one carpark page in browser
2. Noticed the page made a fetch to `/api/carpark/fetch-carpark-detail-data?id=123`
3. Called that endpoint directly for IDs 1-1143 with 10 concurrent requests
4. 1,000 results in 2 minutes. All structured JSON.

## When API Discovery Fails

- **Static HTML sites** — no API, data is in the HTML. Use `web_fetch` with markdown extraction.
- **Heavy anti-bot** — APIs require tokens that rotate per session. Fall back to browser snapshot + act.
- **WebSocket data** — real-time data via WS connections. Browser is the only option.
- **Captcha-gated APIs** — require human verification. Don't automate these.
