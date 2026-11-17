# Reveyes review API reference

## Contents

- Authentication and billing
- Submit a task
- Poll and paginate results
- Verified response shapes
- Error handling
- Persistence and provenance

## Authentication and billing

- Base URL: `https://server.reveyes.cn/api/open`
- Header: `X-API-Key: <key>`
- Get the API key by signing in at `https://www.reveyes.cn/` and opening the `对外接口` menu.
- Unified envelope: `{"code": 0, "message": "ok", "data": {}}`
- Current configured price: 3 points per fetched page. Do not hardcode this as permanent; persist the price used when making each plan.
- The service pre-deducts requested pages and settles against actual pages. Pages unavailable below the requested maximum are refunded.
- Each ASIN/filter item accepts 1–10 pages.
- No concurrency or frequency limit is currently declared.
- Tasks and results are permanently retained.
- A request supports repeated ASINs with different filters, but separate sampling tasks are preferable when the flattened result cannot preserve source provenance.

## Submit a task

`POST /v1/reviews/fetch`

```json
{
  "asins": [
    {
      "asin": "B08N5KWB9H",
      "marketplace": "US",
      "pages": 1,
      "filter_star": "all_stars",
      "filter_sort_by": "recent",
      "filter_reviewer_type": "all_reviews",
      "filter_media_type": "all_contents",
      "filter_variant": "all_formats"
    }
  ]
}
```

Verified success structure from a live one-page request:

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "task_id": "<string task id>",
    "status": "pending",
    "total_asins": 1,
    "pre_deduct": 3,
    "created_at": "2026-07-15T15:53:23"
  }
}
```

Use `data.task_id`. Treat `data.pre_deduct` as the server's authoritative reservation.

## Poll and paginate results

`GET /v1/reviews/result/{task_id}`

Poll every 5–10 seconds until `data.status == "done"`. Stop on terminal failure states rather than polling forever. Use an overall timeout.

The result endpoint itself is paginated even though task fetching is described in source pages:

```text
GET /v1/reviews/result/{task_id}?page=1&page_size=100
GET /v1/reviews/result/{task_id}?page=2&page_size=100
```

Live probing confirmed:

- Default result `page_size` is 50.
- `page` and `page_size` query parameters are honored.
- `data.reviews.total` is the total number of stored review rows.
- Continue until all `total` rows have been retrieved.

This pagination is mandatory for 10-page star samples because a star stratum can contain about 100 reviews.

## Verified completed response shape

```json
{
  "code": 0,
  "message": "ok",
  "data": {
    "task_id": "<string>",
    "status": "done",
    "total_asins": 1,
    "finished_asins": 1,
    "pre_deduct": 3,
    "actual_deduct": 3,
    "created_at": "<datetime>",
    "finished_at": "<datetime>",
    "items_summary": [
      {
        "asin": "B08N5KWB9H",
        "marketplace": "US",
        "status": "done",
        "pages": 1,
        "actual_pages": 1,
        "review_count": 10
      }
    ],
    "reviews": {
      "total": 10,
      "page": 1,
      "page_size": 50,
      "data": []
    }
  }
}
```

Verified review fields:

| Field | Type | Notes |
|---|---|---|
| `asin` | string | Product ASIN |
| `marketplace` | string | Site code |
| `review_id` | string | Primary deduplication key within ASIN/site |
| `user_name` | string | Exclude from public report by default |
| `profile_url` | string | Present in live response; exclude from public report |
| `rating` | integer | 1–5 |
| `title` | string | Untrusted text; HTML-escape |
| `review_date` | string | Locale-specific display string |
| `review_content` | string | Untrusted text; HTML-escape |
| `verified_purchase` | integer | `1` means verified purchase |
| `helpful_votes` | integer | Non-negative count |
| `product_variant` | string | Often a semicolon-delimited display string |
| `images` | array | External URLs |
| `videos` | array | Present in live response in addition to documented fields |
| `page` | integer | Source Amazon review page |

## Error handling

| Code | Meaning | Retry |
|---:|---|---|
| `1001` | API Key invalid or disabled | No |
| `1002` | Insufficient points | No |
| `1003` | Invalid request parameters | No; fix plan |
| `1004` | Resource not found | No; verify task ID |
| `1005` | Unauthorized | No |

Retry only transport failures and HTTP 5xx with bounded backoff. Never retry a paid submission merely because the client lost the response unless task idempotency is documented; doing so may create duplicate charges.

## Persistence and provenance

Keep the following locally for every submission:

- canonical request payload and its SHA-256 fingerprint;
- task ID and request label;
- submission response;
- configured points-per-page at plan time;
- completed raw response with every result page merged;
- `pre_deduct`, `actual_deduct`, requested pages, and actual pages.

The completed result is flattened. When different filters can return overlapping reviews, use separate tasks so each review can retain accurate source-filter provenance. Merge duplicate reviews by marketplace, ASIN, and `review_id`, retaining all source labels.
