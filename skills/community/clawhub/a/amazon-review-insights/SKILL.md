---
name: amazon-review-insights
description: Amazon product review intelligence analysis tool for global e-commerce sellers. Core capabilities:fetch Amazon reviews, AI-powered negative review analysis, quantify high-frequency issues, discover hidden negative feedback in 5-star reviews, generate improvement suggestions, track review trends, incremental updates.
slug: amazon-review-insights
displayName: amazon-review-insights
version: 1.2.6
summary: Amazon product review intelligence analysis tool for global e-commerce sellers. Fetch Amazon reviews, run AI-powered negative review analysis, quantify high-frequency issues, discover hidden negative feedback in 5-star reviews, generate improvement suggestions, track review trends, and support incremental updates.
license: MIT-0
metadata:
  openclaw:
    requires:
      env:
        - CUSTOMER_INSIGHTS_API_KEY
    dependencies:
      python:
        - requests>=2.28.0
---

# AstrMap Review Insights Skill

## Language

- Reply in **English** if user input is in English or non-Chinese (as this is the unified language)
- Reply in **中文** if user input is in Chinese

## Configuration

### API Key

All API calls require an API Key for authentication.

**Note**: The API endpoint is fixed at `https://api.astrmap.com` and is not configurable.

**Recommended**: Set the environment variable in `~/.zshrc` or `~/.bashrc`:

```bash
export CUSTOMER_INSIGHTS_API_KEY="your-api-key-here"
```

> To obtain an API Key: Open https://app.astrmap.com/ and sign in (register first if needed), then click **User Menu (bottom-left)** → **API Keys**, create and copy your API Key.

**Important**: If `CUSTOMER_INSIGHTS_API_KEY` is not set or no API Key is provided, **ask the user first**:
> "Please provide your AstrMap API Key (open https://app.astrmap.com/, sign in, then go to User Menu → API Keys to create one)"
>
> Then pass it via `--api-key` parameter for all subsequent commands.

**Security Notice**: This Skill sends the API Key to AstrMap servers (api.astrmap.com) for authentication. The API Key will not be used to access other services.

### Feature Tiers

| Feature | Requires Collection Channel (Chrome browser extension) | Requires API Key |
|---------|------------------------|-----------------|
| Query completed analysis results | No | Yes |
| Create collection-only task | Yes (online) | Yes |
| Create auto-analysis task | Yes (online) | Yes |
| Incremental fetch | Yes (online) | Yes |
| Manual trigger analysis | No | Yes |

> Tip: If you only need to query completed analysis results, you can use the API Key directly without installing any collection component.

### Collection Channel: Chrome Browser Extension

Creating tasks requires a collection channel running online. AstrMap's collection channel is the **Chrome browser extension** (the website no longer offers the desktop client for download).

> The online endpoint returned by `check_device` carries an `endpoint_type` field: `extension` for the browser extension,
> `desktop` for legacy desktop client installs (historical builds, no longer distributed).
> Either way, as long as `is_alive=true` you can create tasks.

**When the collection channel is offline** (`check_device` returns `is_alive=false` with `endpoint_id`/`endpoint_type` `null` — a normal response, not an error code):

1. **Tell the user**: "No collection channel is online. You need to install and sign in to the AstrMap browser extension first."
2. **Guide installation**: Point the user to https://www.astrmap.com/en/#download and follow the steps on that page
3. **Guide login**: After installing, sign in to an Amazon buyer account in Chrome (do not use your seller account) and make sure Amazon is reachable
4. **Re-check**: Run `check_device` again; confirm `is_alive=true` before creating the task

### Extension Installation Guide

#### 1. Get Download Links

```bash
python scripts/api_client.py --action get_download_links
```

#### 2. Installation Steps

1. Download and extract the extension package
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" in the top-right corner
4. Click "Load unpacked"
5. Select the extracted extension folder to complete installation

#### 3. Setup After Installation

After installing the extension:
1. Open the Web app at https://app.astrmap.com/ and sign in to your AstrMap account
2. Sign in to your Amazon buyer account in Chrome (do not use your seller account)
3. Make sure Amazon is reachable
3. Ensure Amazon access is working

### Security & Verification

For detailed security verification, privacy risk statement, Amazon account security, and API Key safety guidelines, **read** `{baseDir}/references/security.md`.

### Dependency Installation

```bash
pip install -r requirements.txt
```

## Important Notes

### Points System
- **Create task (auto mode)**: Free review collection, AI analysis deducts points
- **Create task (collection-only mode)**: Free review collection, no point deduction
- **Incremental fetch**: Fetch latest reviews and re-analyze, deducts points
- **Query results**: View completed results, no point deduction

### Prerequisites (only for creating tasks)

1. Collection channel online (Chrome extension installed and connected; `check_device` returns `is_alive=true`)
2. Signed in to an Amazon buyer account in the browser (do not use your seller account)
3. Amazon access is working

> Querying completed task results has no restrictions and can be called directly.

## Workflow

### Invocation

```bash
python scripts/api_client.py --action <action> [--params...]
```

### 1. Check Device Online

```bash
python scripts/api_client.py --action check_device --api-key "your-key"
```

Response: `{is_alive: true, endpoint_id: "xxx", endpoint_type: "desktop", status: "idle"}`

> v2.2 field rename: `online → is_alive`, `device_id → endpoint_id`, plus new `endpoint_type`. When offline, `is_alive` is `false` and `endpoint_id / endpoint_type` are `null`.

### 2. Create Task

> Note: Creating a task deducts points. Before executing, inform the user and wait for confirmation:
> "About to create task. Current points: {points}. This will deduct points. Continue?"

**Create Task Flow**:
1. `--action check_device` → Check device online status
2. `--action get_points` → Check account points
3. **Inform user of point consumption, wait for confirmation**
4. Confirm prerequisites, then `--action create_task --asin <ASIN> --site <site> [--is-auto false]`

**Run Mode**:
| Parameter | Description |
|-----------|-------------|
| `--is-auto true` (default) | Auto mode: automatically trigger AI analysis after collection |
| `--is-auto false` | Collection-only mode: stops at "pending analysis" status |

**Site Mapping**: US/CA/UK(English), DE(German), FR(French), IT(Italian), ES(Spanish), JP(Japanese)

**Command Examples**:
```bash
python scripts/api_client.py --action create_task --api-key "your-key" --asin "B09V3KXJPB" --site US
```

### 3. Poll Task Status

After submission, poll every **6 minutes**:

```bash
python scripts/api_client.py --action get_task_detail --api-key "your-key" --task-id "TSK_xxx"
```

**Status Flow**:

**Auto Mode** (`is_auto=true`): `PENDING` → `DISPATCHING` → `COLLECTING` → `PROCESSING` → `ANALYZING` → `SUCCESS/FAILED/CANCELLED`

**Collection-only Mode** (`is_auto=false`): `PENDING` → `DISPATCHING` → `COLLECTING` → `COLLECTED`

**Status Prompts**:

| Status | User Message |
|--------|-------------|
| PENDING | "Task submitted, waiting for scheduling..." |
| DISPATCHING | "Allocating device..." |
| COLLECTING | "Fetching Amazon review data, please wait (usually 20~120 seconds)" |
| PROCESSING | "Review data fetched, processing..." |
| ANALYZING | "Data processing complete, AI analyzing..." |
| SUCCESS | "Analysis complete! Fetching results..." |
| FAILED | "Task failed. Please check device status and network connection." |
| CANCELLED | "Task cancelled" |
| COLLECTED | "Collection complete! In pending analysis state." |

> If task does not complete after a long time (over 18 minutes), prompt user to check if the collection channel (browser extension) is online.

### 4. Get Analysis Results

```bash
# AI Insights Summary
python scripts/api_client.py --action get_ai_insights --api-key "your-key" --task-id "TSK_xxx"
# Category-Tag Distribution
python scripts/api_client.py --action get_category_tag_distribution --api-key "your-key" --task-id "TSK_xxx"
# Basic Statistics
python scripts/api_client.py --action get_basic_statistics --api-key "your-key" --task-id "TSK_xxx"
# Negative Reviews List
python scripts/api_client.py --action get_negative_reviews --api-key "your-key" --task-id "TSK_xxx" --page 1 --page-size 20
```

> Note: Querying completed task results does not deduct points and has no prerequisites.

### 5. Get Product Info

Product info is the **contextual foundation** of negative review analysis, especially for "negative review vs. selling points" semantic alignment.

```bash
# Mode 1: by task (returns all products under that task)
python scripts/api_client.py --action get_product_detail --api-key "your-key" --task-id "TSK_xxx"

# Mode 2: by ASIN directly (no task needed)
python scripts/api_client.py --action get_product_detail --api-key "your-key" --asin "B0XXXXXXXX" --site US
```

**Returned fields** (full, for secondary analysis):

| Category | Fields |
|------|------|
| Identity | `asin` / `site` / `product_title` / `brand` / `image_main` |
| Rating | `rating_average` / `rating_count` / `rating_distribution` (5→1 star %) / `rating_health` |
| Category | `category_path` / `category_levels` / `category_node_ids` (consistent across languages) / `category_leaf_id` |
| Price | `price_current` / `price_original` / `price_discount` / `price_off_amount` / `currency` |
| **Content** | `bullets` (five bullet points) / `product_description` / `has_aplus_content` / `aplus_image_urls` |
| Status | `availability` / `date_first_available` / `featured_badge` / `is_active` |

**`rating_health` values**: `healthy` (5-star ≥80%) / `polarized` (5-star ≥40% and 1-star ≥10%, average score masks polarization) / `poor` (5-star <40%) / `moderate`.

> ⚠️ **Ownership check**: in ASIN mode, the ASIN must appear in **one of your tasks**, otherwise the server returns
> `无权访问该商品信息（该 ASIN 不在您的任何任务中）`.
> Reason: product data is stored globally per `(platform, site, asin)`; without the check, cross-account data leaks would occur.
>
> Note: `product_description` may be `null` — this does **not** mean collection failed. Brand-registry sellers
> often publish image-only descriptions (A+ content); in that case `has_aplus_content=true` and you can present `aplus_image_urls`.

### 6. Incremental Fetch

> Note: Incremental fetch deducts points. Before executing, inform user and wait for confirmation.

**Incremental Fetch Flow**:
1. Check device and points
2. Inform user of point consumption, wait for confirmation
3. `--action create_incremental --task-id <task_id>`
4. Poll status (same as create task)

### 7. Manual Trigger Analysis (Collection-only Mode)

Tasks in collection-only mode (`is_auto=false`) stop at COLLECTED status, requiring manual AI analysis trigger:

```bash
python scripts/api_client.py --action trigger_analysis --api-key "your-key" --task-id "TSK_xxx"
```

Status flow: `COLLECTED` → `PROCESSING` → `ANALYZING` → `SUCCESS`

### 8. Positive Review Analysis (`polarity="positive"`)

> Workflow 1-6 above focuses on the negative-review side / AI insights. `scripts/api_client.py` also supports `polarity="positive"` to fetch positive review quotes, representative positive reviews, and positive tag distribution — for listing copy extraction, marketing material libraries, and comparison tables against the negative side.

**Three methods, quick calls**:

```python
from api_client import CustomerInsightsClient

client = CustomerInsightsClient(api_key="sk_live_...")

# 1. Full positive review quotes (same fields as get_negative_reviews, supports paging)
pos = client.get_sentiment_reviews(tid, polarity="positive", page=1, page_size=50)
# Response: {items: [...], total: N, page_max: M, page: 1, page_size: 50}

# 2. Representative positive reviews (ranked by dimension, limit tested ≤ 5)
rep_pos = client.get_representative_reviews(tid, polarity="positive", limit=5)
# Response fields: content / title / star / dimension / dimension_name / rank_in_dimension / url

# 3. Positive tag frequency (three-level nesting: dimension → category → tag)
dist_pos = client.get_category_tag_distribution(tid, polarity="positive")
# Response: category_tag_distribution.dimensions.{experience|product|service}.categories.{...}.tags
```

**Equivalence (important)**: `get_negative_reviews` is an alias of `get_sentiment_reviews(polarity="negative")` (see `scripts/api_client.py` source comments). **Do not write two sets** — switch with polarity.

**Typical usage**:
- **Listing copy**: take quotes from `get_representative_reviews(polarity="positive")` as bullet points, top-5 frequency list as main selling points
- **Marketing material library**: classify positive quotes into "feature description / emotional resonance / scenario immersion / problem solving"
- **Negative vs. positive comparison table**: same-dimension polarization detection (e.g., "easy to operate 97 vs. complicated to operate 126" — the app flow is friendly to some users but deters others)

> **⚠️ Must pass the V1 self-check**: ① `polarity="positive"` items may contain 1★/2★ (pitfall #28 — filter by `review_star >= 4` first); ② representative 4★ content may contain hidden negative feedback (pitfall #29); ③ if the negative side missed a P0, scan the positive side again to confirm (subscription / consumables / privacy).

## All Available Actions

| action | Description | Required Parameters |
|--------|-------------|-------------------|
| get_download_links | Get browser extension download links | - |
| check_device | Check if device is online | - |
| create_task | Create task | --asin, --site |
| create_incremental | Incremental fetch | --task-id |
| rename_task | Rename a task | --task-id, --name |
| trigger_analysis | Manual trigger analysis | --task-id |
| get_task_detail | Query task details | --task-id |
| get_task_list | Get task list | - |
| get_ai_insights | Get AI insights | --task-id |
| get_basic_statistics | Get basic statistics | --task-id |
| get_representative_reviews | Get representative reviews | --task-id |
| get_category_tag_distribution | Get category-tag distribution | --task-id |
| get_negative_reviews | Get negative reviews list | --task-id |
| get_trend | Get review trends | --task-id |
| get_related_comments | Get comments associated with tag/category | --task-id, --association-type |
| get_comments | Get raw comments | --task-id |
| get_comments_overview | Get comments overview | --task-id |
| get_product_detail | Get product info (full fields: title/brand/rating/star distribution/category tree/price/bullets/description/A+ images) | --task-id or --asin(+--site) |
| get_points | Query points balance | - |

## Error Handling

> Note: `api_client` throws `API Error: {msg}` for any non-zero `code` — rely on the returned **msg** for diagnosis;
> an offline collection channel is **not** an error code, but `check_device`'s normal `is_alive=false` response.

| Error Code | Description | Handling |
|-----------|-------------|----------|
| Device offline | `check_device` returns `is_alive=false` (normal response, not an error code) | No collection channel online; guide the user to install/sign in to the browser extension |
| Insufficient points | msg contains "积分余额不足" (formerly 1002) | Prompt user to recharge points |
| Invalid API Key | auth failure msg (formerly 2001) | Check if API Key is correct |
| API Key disabled | auth failure msg (formerly 2002) | Prompt user to create new API Key |
| API Key expired | auth failure msg (formerly 2003) | Prompt user to create new API Key |
| Insufficient permissions | permission msg (formerly 2004) | Check API Key permission configuration |
| Rate limit exceeded | rate-limit msg (formerly 2005) | Prompt user to retry later |
| PRODUCT_NOT_ACCESSIBLE | "无权访问该商品信息（该 ASIN 不在您的任何任务中）" | ASIN direct product query requires the ASIN to appear in one of your tasks |
| InvalidTaskStatus | Task status is not COLLECTED | Only collection-only tasks with COLLECTED status can trigger analysis |

## Detailed API Documentation

For detailed API endpoint documentation, request parameters, and response formats, see [API Reference](references/api_reference.md).

## Usage Examples

### Scenario 1: Create New Task

```
User: Help me get and analyze reviews for B09V3KXJPB
AI Agent:
1. Check API Key → if not configured, ask user to provide
2. Check device and points
3. Inform point consumption, wait for confirmation
4. Create task
5. Poll status every 6 minutes, provide real-time progress
6. After analysis complete, get results
```

### Scenario 2: Collection-only Mode + Manual Trigger Analysis

```
User: Help me collect reviews only, don't analyze for now
AI Agent:
1. Check API Key and device
2. Create task with --is-auto false
3. Poll status until COLLECTED
4. After user confirms analysis, run trigger_analysis (API Key only, no collection channel required)
```

### Scenario 3: Query Completed Task

```
User: View analysis results for TSK_xxx
AI Agent:
1. Check API Key
2. Get analysis results directly (no device or prerequisites required)
```
