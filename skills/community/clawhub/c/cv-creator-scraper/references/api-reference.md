# API Reference

## Protocol

| Item | Description |
|------|-------------|
| Base URL | `https://{host}/openapi/v1/` |
| Protocol | HTTPS |
| Method | All endpoints use **POST** |
| Format | JSON (`Content-Type: application/json`) |
| Auth | `X-API-Key` + `X-User-Identity` headers |
| Encoding | UTF-8 |
| Timestamps | ISO 8601 (e.g., `2026-03-15T10:30:00Z`) |
| Pagination | `page` (starts at 1), `size` (default 50) |

## Response Structure

```json
{
  "success": true,
  "data": { ... },
  "error": null,
  "meta": {
    "request_id": "req_abc123",
    "page": 1,
    "size": 50,
    "total": 1200,
    "quota_remaining": -1,
    "credits_consumed": 150,
    "credits_remaining": 131500
  }
}
```

`meta.quota_remaining`: remaining daily API request quota. It is **not** a credits balance. `-1` means unlimited.
`meta.service_level`: service level used for this search request (`S1`/`S2`/`S3`). Only present in search responses. Default is `S2`.
`meta.credits_consumed`: credits deducted for this request. `0` means no charge.
`meta.credits_remaining`: actual OpenAPI credits balance. `-1` means unlimited. This field may be absent from non-billed endpoints.
`meta.total`: total matching records. For search endpoints, only returned when filter conditions > 2 (excluding `page`, `size`, `sort_field`, `sort_order`, `service_level`). Returns `null` when ≤ 2 filters.
`meta.lang`: response translation language (`cn`/`en`). `null` when `lang` param not provided.

Never report insufficient credits from `quota_remaining`. Only error code `40201` confirms insufficient credits.

## Endpoints

| Endpoint | Path | Description |
|----------|------|-------------|
| Search TikTok creators | `/openapi/v1/creators/tiktok/search` | Multi-dimensional filtering, supports `service_level` (S1/S2/S3) |
| Search YouTube creators | `/openapi/v1/creators/youtube/search` | Multi-dimensional filtering, supports `service_level` (S1/S2/S3) |
| Search Instagram creators | `/openapi/v1/creators/instagram/search` | Multi-dimensional filtering, supports `service_level` (S1/S2/S3) |
| Submit collection task | `/openapi/v1/collection/tasks/submit` | Batch collect by links/usernames |
| Submit keyword collection | `/openapi/v1/collection/tasks/keyword-submit` | Collect by keywords |
| Query task status | `/openapi/v1/collection/tasks/status` | Check collection progress |
| Get task data | `/openapi/v1/collection/tasks/data` | Paginated results |
| Export task data | `/openapi/v1/collection/tasks/export` | Export to xlsx/csv/html file |
| Get file download URL | `/openapi/v1/files/download-url` | Get temporary download URL |
| Find similar creators | `/openapi/v1/creators/lookalike` | Lookalike search by username/URL, auto-resolves platform ID |

## Task Types

| task_type | Description | values content | Max items |
|-----------|-------------|---------------|-----------|
| `LINK_BATCH` | Link collection | Creator profile URLs | 500 |
| `FILE_UPLOAD` | Username collection | Creator usernames | 500 |

## Task Status

| status | Description |
|--------|-------------|
| `processing` | In progress (collecting or importing data) |
| `completed` | Completed |
| `failed` | Failed |
| `timeout` | Timed out |

## Supported Platforms

| Platform | ID | Search | Link Collection | Username Collection | Keyword Collection |
|----------|----|--------|----------------|--------------------|--------------------|
| TikTok | `tiktok` | ✅ | ✅ | ✅ | ✅ |
| YouTube | `youtube` | ✅ | ✅ | ✅ | ✅ |
| Instagram | `instagram` | ✅ | ✅ | ✅ | ✅ |

## Search Response Fields by Service Level

### TikTok

| Field | Type | Level | Description |
|-------|------|-------|-------------|
| `uid` | string | S1 | Creator unique ID |
| `username` | string | S1 | Username |
| `nickname` | string | S1 | Nickname |
| `avatar_url` | string | S1 | Avatar URL |
| `profile_url` | string | S1 | Profile URL |
| `followers_count` | integer | S1 | Followers count |
| `likes_count` | integer | S1 | Likes count |
| `video_count` | integer | S1 | Total videos |
| `has_showcase` | boolean | S1 | Has showcase/store |
| `has_email` | boolean | S1 | Has email |
| `has_mcn` | boolean | S1 | Has MCN |
| `has_line` | boolean | S1 | Has Line |
| `has_zalo` | boolean | S1 | Has Zalo |
| `last_video_publish_date` | string | S1 | Last video publish date (YYYY-MM-DD) |
| `country_code` | string | S2 | Country/region code |
| `gender` | string | S2 | Gender (translated when `lang` is set) |
| `avg_views` | integer | S2 | Avg views of last 10 videos |
| `engagement_rate` | number | S2 | Avg interaction rate of last 10 videos |
| `views_per_follower` | number | S2 | Views per follower ratio |
| `is_verified` | boolean | S2 | Whether verified |
| `last10_video_views_per_sub` | number | S2 | Last 10 video views per subscriber |
| `last10_med_video_views_cnt` | integer | S2 | Last 10 video views median |
| `last10_med_video_views_per_sub` | number | S2 | Last 10 video views median per subscriber |
| `product_categories` | string[] | S2 | Product categories |
| `industry_categories` | array | S2 | Industry categories (primary/secondary/tertiary) |
| `bio` | string | S2 | Bio / profile description |
| `hashtags` | string[] | S2 | Hashtag list |
| `language` | string | S2 | Language |
| `email` | string | S2 | Email address |
| `link_whatsapp` | string | S2 | WhatsApp link |
| `link_line` | string | S2 | Line link |
| `link_zalo` | string | S2 | Zalo link |
| `mcn` | string | S2 | MCN agency |
| `audience_female_rate` | number | S3 | Female audience ratio (percentage, e.g. 78.65 = 78.65%) |
| `audience_country_code_list` | string[] | S3 | Audience country distribution |
| `audience_language_code_list` | string[] | S3 | Audience language distribution |
| `audience_age_id_list` | string[] | S3 | Audience age distribution (translated when `lang` is set) |

### YouTube

| Field | Type | Level | Description |
|-------|------|-------|-------------|
| `uid` | string | S1 | Creator unique ID |
| `username` | string | S1 | Username |
| `nickname` | string | S1 | Channel name |
| `avatar_url` | string | S1 | Avatar URL |
| `channel_url` | string | S1 | Channel URL |
| `has_email` | boolean | S1 | Has email |
| `has_whatsapp` | boolean | S1 | Has WhatsApp |
| `last_video_publish_time` | string | S1 | Last video publish time (ISO 8601) |
| `country_code` | string | S2 | Country/region code |
| `language` | string | S2 | Language |
| `gender` | string | S2 | Gender |
| `bio` | string | S2 | Channel bio / description |
| `followers_count` | integer | S2 | Subscribers count |
| `video_count` | integer | S2 | Video count |
| `view_count` | integer | S2 | Total views |
| `avg_views` | integer | S2 | Avg views of last 10 videos (all) |
| `avg_views_short` | integer | S2 | Avg views of last 10 short videos |
| `avg_views_long` | integer | S2 | Avg views of last 10 long videos |
| `engagement_rate` | number | S2 | Interaction rate of last 10 videos (all) |
| `engagement_rate_short` | number | S2 | Interaction rate of last 10 short videos |
| `engagement_rate_long` | number | S2 | Interaction rate of last 10 long videos |
| `is_verified` | boolean | S2 | Whether verified |
| `last10_video_views_per_sub` | number | S2 | Last 10 video views per subscriber (all) |
| `last10_video_views_per_sub_short` | number | S2 | Last 10 short video views per subscriber |
| `last10_video_views_per_sub_long` | number | S2 | Last 10 long video views per subscriber |
| `last10_med_video_views_cnt` | integer | S2 | Last 10 video views median (all) |
| `last10_med_video_views_cnt_short` | integer | S2 | Last 10 short video views median |
| `last10_med_video_views_cnt_long` | integer | S2 | Last 10 long video views median |
| `last10_med_video_views_per_sub` | number | S2 | Last 10 video views median per subscriber (all) |
| `last10_med_video_views_per_sub_short` | number | S2 | Last 10 short video views median per subscriber |
| `last10_med_video_views_per_sub_long` | number | S2 | Last 10 long video views median per subscriber |
| `industry_categories` | array | S2 | Industry categories (primary/secondary/tertiary) |
| `hashtags` | string[] | S2 | Hashtag list |
| `email` | string | S2 | Email address |
| `whatsapp` | string | S2 | WhatsApp |
| `audience_female_rate` | number | S3 | Female audience ratio (percentage) |
| `audience_country_code_list` | string[] | S3 | Audience country distribution |
| `audience_language_list` | string[] | S3 | Audience language distribution |
| `audience_age_list` | string[] | S3 | Audience age distribution (translated when `lang` is set) |

### Instagram

| Field | Type | Level | Description |
|-------|------|-------|-------------|
| `uid` | string | S1 | Creator unique ID |
| `username` | string | S1 | Username |
| `nickname` | string | S1 | Nickname |
| `avatar_url` | string | S1 | Avatar URL |
| `profile_url` | string | S1 | Profile URL |
| `has_email` | boolean | S1 | Has email |
| `has_whatsapp` | boolean | S1 | Has WhatsApp |
| `last_video_publish_time` | string | S1 | Last post/video publish time |
| `country_code` | string | S2 | Country/region code |
| `language` | string | S2 | Language |
| `gender` | string | S2 | Gender (translated when `lang` is set) |
| `bio` | string | S2 | Bio / profile description |
| `followers_count` | integer | S2 | Followers count |
| `video_count` | integer | S2 | Posts/videos count |
| `avg_views` | integer | S2 | Avg views of last 10 videos |
| `engagement_rate` | number | S2 | Avg interaction rate of last 10 videos |
| `is_verified` | boolean | S2 | Whether verified |
| `last10_video_views_per_sub` | number | S2 | Last 10 video views per subscriber |
| `last10_med_video_views_cnt` | integer | S2 | Last 10 video views median |
| `last10_med_video_views_per_sub` | number | S2 | Last 10 video views median per subscriber |
| `industry_categories` | array | S2 | Industry categories (primary/secondary/tertiary) |
| `hashtags` | string[] | S2 | Hashtag list |
| `email` | string | S2 | Email address |
| `link_whatsapp` | string | S2 | WhatsApp |
| `audience_female_rate` | number | S3 | Female audience ratio (percentage) |
| `audience_country_code_list` | string[] | S3 | Audience country distribution |
| `audience_language_code_list` | string[] | S3 | Audience language distribution |
| `audience_age_id_list` | string[] | S3 | Audience age distribution (translated when `lang` is set) |

### Lookalike

| Field | Type | Description |
|-------|------|-------------|
| `uid` | string | Creator unique ID |
| `username` | string / null | Username |
| `nickname` | string / null | Nickname |
| `avatar_url` | string / null | Avatar URL |
| `profile_url` | string / null | Profile URL |
| `country_code` | string / null | Country/region code |
| `followers_count` | integer / null | Followers count |
| `avg_views` | integer / null | Avg views of last 10 videos |
| `engagement_rate` | number / null | Avg interaction rate of last 10 videos |
| `match_score` | number / null | Similarity match score |

## Export Formats

| format | Description |
|--------|-------------|
| `xlsx` | Excel file with bold headers, background colors, auto column width |
| `csv` | CSV file, UTF-8 BOM encoding (Excel compatible) |
| `html` | HTML table page, viewable in browser |
| `feishu_doc` | Feishu document (not yet available, returns 400) |

## Export Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `file_id` | string | Unique file identifier (reusable via get_download_url) |
| `file_name` | string | File name |
| `file_url` | string | Authenticated temporary download URL |
| `file_expire_at` | string | URL expiration time (ISO 8601 UTC) |
| `format` | string | Export format |
| `row_count` | integer | Number of data rows |

## Webhook

Pass `webhook_url` when submitting collection tasks for completion notification.

Callback payload:

```json
{
  "event": "collection.completed",
  "task_id": "task_xxx",
  "task_type": "LINK_BATCH",
  "status": "completed",
  "total": 2,
  "completed": 2,
  "failed": 0,
  "timestamp": "2026-03-15T10:45:00Z"
}
```

Signature: `X-Webhook-Signature` header, HMAC-SHA256.
Retry policy: max 3 attempts (10s → 30s → 90s).
