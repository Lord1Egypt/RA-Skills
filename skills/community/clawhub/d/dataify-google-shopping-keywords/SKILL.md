---
name: dataify-google-shopping-keywords
description: Collect Google Shopping product information through Dataify Scraper API by keyword. Use when the user asks to gather, scrape, crawl, fetch, extract, or collect Google Shopping product data, product information, product listings, or product keyword data, including noun-plus-verb combinations such as Google Shopping product information plus collect/scrape/crawl/fetch/extract, product keyword information plus collect/scrape/crawl/fetch/extract, Instagram Reel information plus collect/scrape/crawl/fetch/extract, "Instagram Reel info scrape", "Instagram Reel information collect", "Instagram Reel 信息采集", "Instagram Reel 信息抓取", "Instagram Reel 信息爬取", "Instagram Reel 信息获取", or requests using spider ID google_shopping_by-keywords.
---

# Dataify Google Shopping Keywords

Use this skill to create Google Shopping keyword collection tasks through Dataify's builder endpoint.

## Required Workflow

1. Use the `google_shopping_by-keywords` spider when the user wants to collect product information by keyword.
2. Check the local Python runtime before calling scripts. Prefer `python`; use `python3` if that is the available Python command. Require Python 3 or newer. Do not use version-specific Python launcher commands.
3. Tell the user which parameters are required and what the defaults are. Ask whether any values should be changed.
4. Ask whether the user wants to collect multiple parameter sets. If yes, collect multiple `spider_parameters` objects for the same spider ID. If the user already supplied multiple keywords or multiple parameter objects, treat that as a multiple-set request.
5. Before every real API call, show a Markdown confirmation table with the exact parameters that will be submitted. The table must use these columns: `Parameter`, `Current value`, `Default value`, `Required`, `Description`.
6. If any dropdown fields are added in the future, show all available dropdown values in Markdown tables with exactly these columns: `Label`, `Value`. This tool currently has no confirmed dropdown fields.
7. Ask the user whether any value should be changed. Do not call the API until the user explicitly confirms the table.
8. Check for the Dataify API token only after parameter confirmation. Prefer a token explicitly provided by the user, then `DATAIFY_API_TOKEN` from the environment.
9. If no token is available, tell the user: `Missing Dataify API token. Provide a token, or log in/register at` [Dataify](https://dashboard.dataify.com/login?utm_source=skill) `If you already have one, open` [Dataify](https://dashboard.dataify.com?utm_source=skill) `and copy the API TOKEN from the top-right area.`
10. If the user provides a token and `DATAIFY_API_TOKEN` is not already saved locally, ask whether to save it as `DATAIFY_API_TOKEN`. Save it only after explicit consent and never echo the token back.
11. After the API call, report the collection task ID and status. Look for common response fields such as `task_id`, `taskId`, `taskIdList`, `tasks_id`, `TasksID`, `id`, `status`, `data.task_id`, `data.id`, or `data.status`. Then remind the user to view task details in the official dashboard: [Dataify](https://dashboard.dataify.com?utm_source=skill)

## Parameter Preview

Use the preview helper whenever possible:

```bash
python scripts/preview_params.py --keyword iphone
```

For multiple parameter sets, pass the exact JSON array:

```bash
python scripts/preview_params.py --parameters-json '[{"keyword":"iphone"},{"keyword":"ipad"}]'
```

## API Call

Use the call helper after confirmation and token handling:

```bash
python scripts/google_shopping_keywords.py --keyword iphone
python scripts/google_shopping_keywords.py --parameters-json '[{"keyword":"iphone"},{"keyword":"ipad"}]'
```

If the token was provided in the conversation instead of the environment, pass it with `--token` and do not expose it in user-facing output:

```bash
python scripts/google_shopping_keywords.py --token "USER_TOKEN" --keyword iphone
```

## Tool

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `keyword` | `google_shopping_by-keywords` | `keyword` | `[{"keyword":"iphone"}]` |

Every request also accepts `file_name`. If omitted, use `{{TasksID}}`.

The user mentioned a `Google country` parameter, but the provided API mapping does not include a confirmed request field or default value for it. Do not include a country field in `spider_parameters` unless the user provides the exact API field name supported by Dataify for this spider.

## Fixed Request Fields

Always submit to `https://scraperapi.dataify.com/builder?platform=1` with:

| Field | Value |
|---|---|
| `spider_name` | `google.com` |
| `spider_id` | `google_shopping_by-keywords` |
| `spider_parameters` | JSON array of one or more parameter objects |
| `spider_errors` | `true` |
| `file_name` | User value, otherwise `{{TasksID}}` |

Send parameters as form data. Keep `spider_parameters` as a JSON string inside the form body.
