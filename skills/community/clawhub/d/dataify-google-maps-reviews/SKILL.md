---
name: dataify-google-maps-reviews
description: Collect Google Maps review/comment information through Dataify Scraper API. Use when the user asks to gather, scrape, crawl, fetch, extract, or collect Google Maps review/comment information from a Google Maps URL, including noun-plus-verb combinations such as Google Maps review information plus collect/scrape/crawl/fetch/extract, Google Maps comments plus collect/scrape/crawl/fetch/extract, Google Maps URL reviews plus collect/scrape/crawl/fetch/extract, "Google Maps review scrape", "Google Maps comments collect", "Google 地图评论信息采集", "Google 地图评论信息抓取", "Google 地图评论信息爬取", "Google 地图评论信息获取", "Google 地图评论URL提取", or requests using spider ID google_comment_by-url.
---

# Dataify Google Maps Reviews

Use this skill to create Google Maps review/comment collection tasks through Dataify's builder endpoint.

## Required Workflow

1. Use the `google_comment_by-url` spider when the user wants to collect Google Maps review information, comment information, or reviews/comments from a Google Maps URL.
2. Check the local Python runtime before calling scripts. Prefer `python`; use `python3` if that is the available Python command. Require Python 3 or newer. Do not use version-specific commands such as `py -3.10`.
3. Tell the user which parameters are required and what the defaults are. Ask whether any values should be changed.
4. Ask whether the user wants to collect multiple parameter sets. If yes, collect multiple `spider_parameters` objects for the same spider ID. If the user already supplied multiple Google Maps URLs or multiple parameter objects, treat that as a multiple-set request.
5. Before every real API call, show a Markdown confirmation table with the exact parameters that will be submitted. The table must use these columns: `Parameter`, `Current value`, `Default value`, `Required`, `Description`.
6. If any dropdown fields are added in the future, show all available dropdown values in Markdown tables with exactly these columns: `Label`, `Value`. This tool currently has no dropdown fields.
7. Ask the user whether any value should be changed. Do not call the API until the user explicitly confirms the table.
8. Check for the Dataify API token only after parameter confirmation. Prefer a token explicitly provided by the user, then `DATAIFY_API_TOKEN` from the environment.
9. If no token is available, tell the user: `Missing Dataify API token. Provide a token, or log in/register at` [Dataify](https://dashboard.dataify.com/login?utm_source=skill) `If you already have one, open` [Dataify](https://dashboard.dataify.com?utm_source=skill) `and copy the API TOKEN from the top-right area.`
10. If the user provides a token and `DATAIFY_API_TOKEN` is not already saved locally, ask whether to save it as `DATAIFY_API_TOKEN`. Save it only after explicit consent and never echo the token back.
11. After the API call, report the collection task ID and status. Look for common response fields such as `task_id`, `taskId`, `taskIdList`, `tasks_id`, `TasksID`, `id`, `status`, `data.task_id`, `data.id`, or `data.status`. Then remind the user to view task details in the official dashboard: [Dataify](https://dashboard.dataify.com?utm_source=skill)

## Parameter Preview

Use the preview helper whenever possible:

```bash
python scripts/preview_params.py --url "https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu" --days-limit 20
```

For multiple parameter sets, pass the exact JSON array:

```bash
python scripts/preview_params.py --parameters-json '[{"url":"https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu","days_limit":"20"},{"url":"https://www.google.com/maps/place/example","days_limit":"30"}]'
```

## API Call

Use the call helper after confirmation and token handling:

```bash
python scripts/google_maps_reviews.py --url "https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu" --days-limit 20
python scripts/google_maps_reviews.py --parameters-json '[{"url":"https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu","days_limit":"20"},{"url":"https://www.google.com/maps/place/example","days_limit":"30"}]'
```

If the token was provided in the conversation instead of the environment, pass it with `--token` and do not expose it in user-facing output:

```bash
python scripts/google_maps_reviews.py --token "USER_TOKEN" --url "https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu" --days-limit 20
```

## Tool

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `url` | `google_comment_by-url` | `url`, `days_limit` | `[{"url":"https://www.google.com/maps/place/Waterfront+Botanical+Gardens/@38.2630366,-85.7288454,15z/data=!4m8!3m7!1s0x8869731e16a7bdbd:0x2f5d238fefed7ca1!8m2!3d38.2632837!4d-85.7239738!9m1!1b1!16s%2Fg%2F11c709xzzx?hl=en&entry=ttu","days_limit":"20"}]` |

Every request also accepts `file_name`. If omitted, use `{{TasksID}}`.

## Fixed Request Fields

Always submit to `https://scraperapi.dataify.com/builder?platform=1` with:

| Field | Value |
|---|---|
| `spider_name` | `google.com` |
| `spider_id` | `google_comment_by-url` |
| `spider_parameters` | JSON array of one or more parameter objects |
| `spider_errors` | `true` |
| `file_name` | User value, otherwise `{{TasksID}}` |

Send parameters as form data. Keep `spider_parameters` as a JSON string inside the form body.
