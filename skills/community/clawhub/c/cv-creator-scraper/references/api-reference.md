# API Reference

## Protocol

| Item | Description |
|------|-------------|
| Base URL | `https://{host}/openapi/v1/` |
| Protocol | HTTPS |
| Method | All endpoints use **POST** |
| Format | JSON (`Content-Type: application/json`), or multipart for video upload |
| Auth | `X-API-Key` + `X-User-Identity` headers |
| Encoding | UTF-8 |
| Timestamps | ISO 8601 (e.g., `2026-03-15T10:30:00Z`) |
| Pagination | `page` starts at 1. Each endpoint defines its own page size. |

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
`meta.service_level`: service level used for this search request (`S1`/`S2`/`S3`). Only present in search responses. Default is `S2`. Note: Navos users automatically default to `S3` (handled by `_api_client.mjs`).
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
| Natural-language creator search | `/openapi/v1/creators/nl-search` | Single-platform search from one natural-language query |
| Find similar creators | `/openapi/v1/creators/lookalike` | Lookalike search by username/URL, auto-resolves platform ID |
| Audit creator fake-follower risk | `/openapi/v1/fake-follower-audit/run` | Synchronous creator-level authenticity and engagement-quality audit |
| Search videos | `/openapi/v1/videos/search` | Search one platform by hashtag or creator identity |
| Find brand collaboration creators | `/openapi/v1/brand-discovery/collaboration-creators` | Look up indexed TikTok and Instagram collaborations |
| Search brand video insights | `/openapi/v1/brand-discovery/video-insights/search` | Expand a brand into up to 5 hashtags, search existing videos, and summarize brand content signals |
| Upload video for audit | `/openapi/v1/media/upload` | Upload a local video and return its material URL |
| Submit video script audit | `/openapi/v1/video-script-audit/tasks/submit` | Start one asynchronous video audit |
| Query audit task status | `/openapi/v1/video-script-audit/tasks/status` | Poll audit task (recommended interval: 10s) |
| Get audit task result | `/openapi/v1/video-script-audit/tasks/result` | Fetch the structured audit result when status is completed |

## Structured Creator Search

Search one of TikTok, Instagram or YouTube through its platform endpoint. See [Platform Parameters](platform-params.md) for supported filters and field names.

- `union_user_ids` and `profile_urls` are optional exact-match lists, each with up to 200 entries. Matches from the two lists are combined and can be filtered further. The query searches indexed creators.
- The backend accepts `size` up to 100. The Skill requests 20 on the first page when the user does not provide a quantity.
- S1 provides core account details and contact-availability flags, S2 adds performance data and available contact details, and S3 adds audience distributions. Platform data and field configuration determine which fields have values.
- TikTok supports filtering by recent commerce metrics. S2 and S3 can also return 30-day GMV, GPM, order value, commission and product sales display fields when available.

Structured search returns a `data` array. Use `scripts/export_to_csv.mjs` to write the current structured or natural-language search results to a local CSV.

## Natural-Language Creator Search

Use `POST /openapi/v1/creators/nl-search` for content direction, creator profile, style, scenario, and product-fit descriptions that are difficult to express as exact structured fields.

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | Yes | Natural-language requirement, 1-1000 characters |
| `platform` | string | No | `instagram` (default), `tiktok`, or `youtube`; common aliases are accepted |
| `limit` | integer | No | Result limit, default 20, range 1-100; channel limits still apply |

Do not send `lang`, `service_level`, `debug`, route tuning, pagination, or structured filters. Search one platform per request.

The API Key must have `creator:nl_search` or `creator:*` scope.

Instagram `scalar_fallback` runs within the same request. Searching multiple platforms requires separate requests. Use the billing response or applicable product pricing for credit amounts.

Recall behavior:

- Instagram uses vector recall when the query contains content topic, style, or commercial semantics.
- Instagram automatically uses `scalar_fallback` when there is not enough semantic content.
- TikTok and YouTube currently use scalar recall.
- Instagram vector recall does not execute email-availability or update-time constraints. Use structured search when either is mandatory.

Response items contain only `uid`, `username`, `nickname`, `avatar_url`, `profile_url`, `country_code`, `followers_count`, `avg_views`, `engagement_rate`, and `match_score`. `engagement_rate` is a decimal ratio, so `0.0432` means `4.32%`. `match_score` is meaningful only within the same request.

Inspect `meta.recall_type` for `vector`, `scalar`, or `scalar_fallback`. This endpoint has a fixed compact response and does not expose S1/S2/S3 selection or S3 audience fields.

## Fake Follower Audit

Use `POST /openapi/v1/fake-follower-audit/run` to inspect one TikTok, Instagram, or YouTube creator for fake-follower and suspicious-engagement risk.

Provide exactly one target form:

```json
{"profile_url":"https://www.tiktok.com/@creator","lang":"cn"}
```

```json
{"platform":"instagram","platform_user_id":"creator","lang":"en"}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `profile_url` | string | Conditional | Creator profile URL |
| `platform` | string | Conditional | `tiktok` / `instagram` / `youtube` |
| `platform_user_id` | string | Conditional | username / union_user_id / sec_user_id |
| `service_level` | string | No | Defaults to `S1` |
| `lang` | string | No | `cn` / `en`; controls `conclusion`, default `en` |

Response fields include:

- `quality_score`: 0-100, higher means healthier engagement.
- `fake_follower_rate`: decimal estimate; `0.12` means 12%.
- `risk_level`: `low` / `medium` / `high` / `critical`.
- `conclusion`, `abnormal_types`, and `signals`.
- `creator_profile`: nickname, avatar, followers, following, and available audience distributions.
- `partial_result` and `warnings`: degradation caused by insufficient content, comments, or profile data.

The fake-follower rate is an estimate, not a platform-provided follower-by-follower audit. When `partial_result=true`, present the response as partial data and include relevant warnings. Billing is determined by the active backend rule for this endpoint; do not hard-code a credit amount.

## Video Search

Use `POST /openapi/v1/videos/search` with one `platform` (`tiktok`, `instagram` or `youtube`). Provide at least one `hashtag` or one creator identifier in `union_user_ids`. When both filter types are present, results must satisfy both.

| Field | Contract |
|-------|----------|
| `hashtag` | Up to 5 exact tags |
| `union_user_ids` | Up to 100 creator identifiers on the requested platform |
| `query_type` | `union_user_id` (default), `kol_page_url` or `user_name` for the entire list |
| `video_title` | Optional title keyword |
| `video_views_cnt_gte` / `video_views_cnt_lte` | Optional play-count range |
| `video_interaction_rate_gte` / `video_interaction_rate_lte` | Optional interaction-rate range, with `3` meaning 3% |
| `video_publish_date_gte` / `video_publish_date_lte` | Optional `YYYY-MM-DD` boundaries. Omit both to search without a date filter. |
| `page` / `size` | Each accepts 1–10 |

Results include video identifiers, titles and links, publish dates, duration, hashtags, play and interaction metrics, and creator identifiers, usernames or nicknames when available.

## Brand Video Insight Search

Use `POST /openapi/v1/brand-discovery/video-insights/search` when the user wants brand/competitor video insight, such as "find Fenty Beauty related videos", "brand hashtag performance", or "竞品品牌视频洞察".

This endpoint expands the brand name into hashtags or uses the given hashtags to search videos CreatiVault has already indexed.

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `brand_name` | string | Yes | Brand or competitor name |
| `platforms` | string[] | No | `tiktok`, `youtube`, `instagram`; defaults to `["tiktok"]` |
| `hashtags` | string[] | No | Manual hashtags, max 5. If provided, auto expansion is skipped |
| `expand_count` | integer | No | Auto-expanded hashtag count, default 5, range 1-5 |
| `limit` | integer | No | Max returned videos, default 20, range 1-50 |
| `per_hashtag_size` | integer | No | Candidate videos per platform and hashtag, default 10, range 1-10 |
| `video_views_cnt_gte` / `video_views_cnt_lte` | integer | No | View-count filters |
| `video_interaction_rate_gte` / `video_interaction_rate_lte` | number | No | Percentage filters, so `3` means 3% |
| `video_publish_date_gte` / `video_publish_date_lte` | string | No | `YYYY-MM-DD` filters |

Example:

```json
{
  "brand_name": "Fenty Beauty",
  "platforms": ["tiktok"],
  "expand_count": 5,
  "video_interaction_rate_gte": 3,
  "limit": 20
}
```

Response `data` includes:

- `keyword_expansion.used_hashtags`: the actual search hashtags.
- `items`: matched videos, each with `matched_hashtag`.
- `summary`: count, platform distribution, top hashtags and top creators in the returned sample.

## Search Response Fields by Service Level

The structured search tables describe field meanings. The endpoint serializes populated scalar values as strings, including values within nested arrays and objects. Field availability depends on the active service level and data.

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
| `last30day_gmv_dollar_show` | string | S2 | 30-day GMV display value (USD) |
| `last30day_gpm_dollar_show` | string | S2 | 30-day GPM display value (USD) |
| `last30day_gmv_per_buyer_dollar_show` | string | S2 | 30-day order value display value (USD) |
| `last30day_commission_rate_show` | string | S2 | 30-day commission rate display value |
| `last30day_prod_sales_show` | string | S2 | 30-day product sales display value |
| `recent_videos` | array | S2 | Recent videos (up to 3; each item has `cover_url` / `video_url` / `video_title` / `video_type`) |
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
| `followers_count` | integer | S1 | Subscribers count |
| `video_count` | integer | S1 | Video count |
| `view_count` | integer | S1 | Total views |
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
| `recent_videos` | array | S2 | Recent videos (up to 3; each item has `cover_url` / `video_url` / `video_title` / `video_type`) |
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
| `followers_count` | integer | S1 | Followers count |
| `video_count` | integer | S1 | Posts/videos count |
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
| `recent_videos` | array | S2 | Recent videos (up to 3; each item has `cover_url` / `video_url` / `video_title` / `video_type`) |
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

## Video Script Audit

Async single-video audit pipeline with **two ingestion paths**:

| Path | Input | Use case | Creator data dimensions |
|------|-------|----------|------------------------|
| **Path 1 (Social URL)** | `video_url` | Published video analysis | Creator and video metrics when available |
| **Path 2 (Upload)** | `oss_url` (via `/media/upload`) | Pre-publish self-audit | `creator_metadata.status=not_applicable` |

Submit one video per task and keep the returned UUID `task_id` for status and result requests.

### Endpoints

| Endpoint | Path | Body | Notes |
|----------|------|------|-------|
| Upload media | `/openapi/v1/media/upload` | `multipart/form-data: file` | Returns a publicly accessible `oss_url` for path 2 |
| Submit | `/openapi/v1/video-script-audit/tasks/submit` | `{video_url?, oss_url?, brief?, ...}` | Send exactly one input URL |
| Status | `/openapi/v1/video-script-audit/tasks/status` | `{task_id}` | Query task status and progress |
| Result | `/openapi/v1/video-script-audit/tasks/result` | `{task_id}` | Fetch results when status is `completed` |

### Upload Media Request (Path 2 Step 1)

```http
POST /openapi/v1/media/upload
Content-Type: multipart/form-data
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | ✓ | Video file (mp4/mov/avi/mkv/webm, ≤ 500MB) |

**Response**: `{oss_key, oss_url, filename, size_bytes}`. Pass **`oss_url`** (not `oss_key`) as the submit `oss_url`.
`oss_key` is for upload tracking only — submit rejects it.

### Submit Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `video_url` | string | △ | Path 1: Video URL (TikTok video / Instagram Reels / YouTube Shorts only) |
| `oss_url` | string | △ | Path 2: full `oss_url` from `/media/upload`; must be HTTPS under `*.creativault.tech` |
| `brief` | string | × | Customer brief, enables `brief_compliance` audit |
| `campaign_id` | string | × | Campaign id for archival |
| `audit_mode` | string | × | `high` (default) / `low` |
| `enable_benchmark` | boolean | × | Compare against existing benchmark cases |

**Deprecated aliases** (auto-mapped by `video_audit_submit.mjs`, avoid in new code):
`url` → `video_url`, `oss_url_override` → `oss_url`.
`uploaded_oss_key` is **rejected** — it is an OSS key, not a URL; pass `oss_url` instead.

> △ `video_url` and `oss_url`: provide exactly one, not both, not neither.

### Audit Task Status

| status | Description | progress |
|--------|-------------|----------|
| `pending` / `queued` | Queued | 0 |
| `processing` | Downloading / analyzing / persisting | 50 |
| `completed` | Result available | 100 |
| `failed` | See `error_message` | 0 |

### Result Payload Fields

| Field | Type | Description |
|-------|------|-------------|
| `task_id` | string | Audit task UUID |
| `audit_result.storyboard` | object | Shot list, script structure, content theme, cinematography stats |
| `audit_result.viral_factors` | object | Hook / rhythm / selling-point integration / pain point / conversion / emotional value |
| `audit_result.content_audit` | object | Brief compliance, content standard, common pitfalls, risks, QA baseline |
| `audit_result.benchmark_comparison` | object \| null | Comparison when enabled and a suitable case is available |
| `audit_result.suggestions` | array | Prioritized improvement actions (`P0`/`P1`/`P2`) |
| `audit_result.scores` | object | Overall score and up to five sub-scores (0–10) for hook, rhythm, selling points, creativity and production |
| `audit_result.diagnosis_level` | string \| null | Diagnostic rating |
| `audit_result.confidence` | object | Overall + per-dimension confidence; `requires_human_review` flag |
| `audit_result.creator_metadata` | object | Account background (followers, last10 avg views/interaction) |
| `audit_result.video_metrics` | object | Video metrics (views, likes, interaction rate, viral level) |
| `hashtags` / `content_type_label` / `structured_analysis` | varies | Content labels and additional structured results when present |
| `html_report_url` | string \| null | Public HTML report URL when generated |

### Audit-Specific Errors

| code | HTTP | Description |
|------|------|-------------|
| 40004 | 400 | Social video URL does not match a supported link format |
| 40001 | 200 | Task not found (invalid task_id) |
| 40002 | 200 | Task not completed (status ≠ completed); keep polling |
| 40003 | 200 | A completed task has no stored audit result |

