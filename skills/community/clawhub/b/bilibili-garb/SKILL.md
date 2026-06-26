---
name: bilibili-garb
description: Bilibili garb (个性装扮) data collection and management. Search garb items, query suit/collection details, scan benefit data for owned items (including discontinued), and determine scarcity tiers. Use when working with Bilibili's personalization system (装扮), digital card collections (收藏集), suit items (套装子项), or any task involving bilibili.com/garb or bilibili.com/h5/mall/digital-card endpoints. Triggers on "bilibili garb", "B站装扮", "装扮搜索", "套装查询", "收藏集", "benefit扫描", "品级判别".
---

# Bilibili Garb (B站个性装扮)

Collect and manage Bilibili personalization items: garb suits, digital card collections, and benefit sub-items.

## Setup

All authentication credentials are read from environment variables or a config file. Create `configs/bili-api-creds.json` in your workspace:

```json
{
  "appkey": "27eb53fc9058f8c3",
  "appsecret": "<obtain from Bilibili mobile client>",
  "access_key": "<your access_key>",
  "csrf": "<your bili_jct>",
  "DedeUserID": "<your uid>",
  "SESSDATA": "<your SESSDATA>"
}
```

Or export environment variables:

```bash
export BILI_SESSDATA="<your SESSDATA>"
export BILI_ACCESS_KEY="<your access_key>"
export BILI_CSRF="<your bili_jct>"
export BILI_UID="<your uid>"
```

> **How to obtain credentials**: Capture from Bilibili mobile app HTTP traffic (e.g., mitmproxy, Charles). The `access_key` expires periodically and must be refreshed.

## Commands

### Search Garb Items

```bash
bash scripts/bilibili-garb-search.sh "关键词"
```

Searches both the official API and a local gallery database. Outputs Markdown with:
- Collection items (收藏集) with `biz_id`
- Suit items (套装) with `item_id`
- Discontinued items from local gallery marked `[藏馆-绝版]`

### Query Collection/Suit Details

```bash
bash scripts/bilibili-garb-collection.sh -i <ID>
```

- ID ≤ 6 digits → collection (收藏集) mode
- ID > 6 digits → suit (套装) mode
- Falls back to local gallery database for discontinued items

### Scan Benefit Data

```bash
python3 scripts/garb-benefit-scan.py [options]
```

Scans owned garb items from `data/decorations-database.json`, calls benefit API for each, and appends results to `data/garb-benefit-results.ndjson`.

Options:
- `--limit N` — process only N items
- `--dry-run` — show what would be scanned without making API calls
- `--force` — rescan items that already have benefit data
- `--debug` — output full API responses

Supports resume (Ctrl+C safe) and deduplication.

## Key API Knowledge

See [references/bilibili-garb-api-reference.md](references/bilibili-garb-api-reference.md) for full API documentation.

Critical points:
1. **Benefit API** (`/x/garb/v2/user/suit/benefit`) is the only way to get data for discontinued items. Requires sign authentication.
2. **DIY suits**: When `item_id` contains a hyphen (e.g., `1775103232001-0`), pass `biz_id` as the `item_id` parameter instead — the original `item_id` returns `-400`.
3. **`part` parameter**: Only one call with `part=space_bg` returns all 9 sub-item types. No need to iterate.
4. **Scarcity tiers**: Use `item_list` API's `scarcity` field as the primary source. When `scarcity_rate=2` and `rate2_count==1`, default to small-hidden (30), do not auto-upgrade to large-hidden.
5. **DLC avatar frames**: Must come from `lottery_home_detail`, never from collection's own `frame`/`frame_image`.

## Standard Operating Procedure

See [references/bilibili-garb-sop.md](references/bilibili-garb-sop.md) for step-by-step workflows.
