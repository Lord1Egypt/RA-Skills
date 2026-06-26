---
name: dataify-booking-hotellist
description: Collect Booking hotel information through Dataify Scraper API. Use when the user asks to gather, scrape, crawl, fetch, extract, or collect Booking hotel information, Booking hotel details, Booking hotel listings, Booking hotel URLs, or data from a Booking URL, including noun-plus-verb combinations such as Booking hotel information plus collect/scrape/crawl/fetch/extract, "Booking hotel info scrape", "Booking hotel URL collect", "Booking hotel information extract", "Booking 酒店信息采集", "Booking 酒店信息抓取", "Booking 酒店信息爬取", "Booking 酒店信息获取", "Booking URL 提取", or requests using spider ID booking_hotellist_by-url.
---

# Dataify Booking Hotel Info

Use this skill to create Booking hotel information collection tasks through Dataify's builder endpoint.

## Required Workflow

1. Use the `booking_hotellist_by-url` spider when the user wants to collect Booking hotel information from one or more Booking URLs.
2. Check the local Python runtime before calling scripts. Prefer `python`; use `python3` if that is the available Python command. Require Python 3 or newer. Do not use version-specific commands such as `py -3.10`.
3. Tell the user which parameters are required and what the defaults are. Ask whether any values should be changed.
4. Ask whether the user wants to collect multiple parameter sets. If yes, collect multiple `spider_parameters` objects for the same spider ID. If the user already supplied multiple Booking URLs, treat that as a multiple-set request.
5. Before every real API call, show a Markdown confirmation table with the exact parameters that will be submitted. The table must use these columns: `Parameter`, `Current value`, `Default value`, `Required`, `Description`.
6. If any dropdown fields are added in the future, show all available dropdown values in Markdown tables with exactly these columns: `Label`, `Value`. This tool currently has no dropdown fields.
7. Ask the user whether any value should be changed. Do not call the API until the user explicitly confirms the table.
8. Check for the Dataify API token only after parameter confirmation. Prefer a token explicitly provided by the user, then `DATAIFY_API_TOKEN` from the environment.
9. If no token is available, tell the user: `Missing Dataify API token. Provide a token, or log in/register at` [Dataify](https://dashboard.dataify.com/login?utm_source=skill) `If you already have one, open` [Dataify](https://dashboard.dataify.com?utm_source=skill) `and copy the API TOKEN from the top-right area.`
10. If the user provides a token and `DATAIFY_API_TOKEN` is not already saved locally, ask whether to save it as `DATAIFY_API_TOKEN`. Save it only after explicit consent and never echo the token back.
11. After the API call, report the collection task ID and status. Look for common response fields such as `task_id`, `taskId`, `id`, `status`, `data.task_id`, `data.id`, or `data.status`. Then remind the user to view task details in the official dashboard: [Dataify](https://dashboard.dataify.com?utm_source=skill)

## Parameter Preview

Use the preview helper whenever possible:

```bash
python scripts/preview_params.py --url "https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"
```

For multiple parameter sets, pass the exact JSON array:

```bash
python scripts/preview_params.py --parameters-json '[{"url":"https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"},{"url":"https://www.booking.com/hotel/us/example.en-gb.html"}]'
```

## API Call

Use the call helper after confirmation and token handling:

```bash
python scripts/booking_hotellist.py --url "https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"
python scripts/booking_hotellist.py --parameters-json '[{"url":"https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"},{"url":"https://www.booking.com/hotel/us/example.en-gb.html"}]'
```

If the token was provided in the conversation instead of the environment, pass it with `--token` and do not expose it in user-facing output:

```bash
python scripts/booking_hotellist.py --token "USER_TOKEN" --url "https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"
```

## Tool

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `by-url` | `booking_hotellist_by-url` | `url` | `[{"url":"https://www.booking.com/hotel/gb/westlands-of-pitlochry.en-gb.html#tab-main"}]` |

Every request also accepts `file_name`. If omitted, use `{{TasksID}}`.

## Fixed Request Fields

Always submit to `https://scraperapi.dataify.com/builder?platform=1` with:

| Field | Value |
|---|---|
| `spider_name` | `booking.com` |
| `spider_id` | `booking_hotellist_by-url` |
| `spider_parameters` | JSON array of one or more parameter objects |
| `spider_errors` | `true` |
| `file_name` | User value, otherwise `{{TasksID}}` |

Send parameters as form data. Keep `spider_parameters` as a JSON string inside the form body.
