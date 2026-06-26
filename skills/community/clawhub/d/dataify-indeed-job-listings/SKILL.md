---
name: dataify-indeed-job-listings
description: Collect Indeed job listings through Dataify Scraper API. Use when the user asks to gather, scrape, crawl, fetch, extract, or collect Indeed job listing/job posting/job information data from an Indeed job URL, including noun-plus-verb combinations such as Indeed job listing/job posting/job information/job URL plus scrape/collect/crawl/fetch/extract, "Indeed job listing scrape", "Indeed job URL collect", "Indeed job information extract", "Indeed 职位列表采集", "Indeed 职位列表抓取", "Indeed 职位信息爬取", "Indeed 职位信息获取", "Indeed 职位URL提取", or requests using spider ID indeed_job-listings_by-job-url.
---

# Dataify Indeed Job Listings

Use this skill to create Indeed job listing collection tasks through Dataify's builder endpoint.

## Required Workflow

1. Use the `indeed_job-listings_by-job-url` spider when the user wants to collect Indeed job listings, job postings, job information, or data from an Indeed job URL.
2. Check the local Python runtime before calling scripts. Prefer `python`; use `python3` if that is the available Python command. Require Python 3 or newer. Do not use version-specific commands such as `py -3.10`.
3. Tell the user which parameters are required and what the defaults are. Ask whether any values should be changed.
4. Ask whether the user wants to collect multiple parameter sets. If yes, collect multiple `spider_parameters` objects for the same spider ID. If the user already supplied multiple job URLs, treat that as a multiple-set request.
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
python scripts/preview_params.py --job-url "https://fr.indeed.com/viewjob?jk=55b3e5dfa0c2ff66"
```

For multiple parameter sets, pass the exact JSON array:

```bash
python scripts/preview_params.py --parameters-json '[{"job_url":"https://fr.indeed.com/viewjob?jk=55b3e5dfa0c2ff66"},{"job_url":"https://www.indeed.com/viewjob?jk=example"}]'
```

## API Call

Use the call helper after confirmation and token handling:

```bash
python scripts/indeed_job_listings.py --job-url "https://fr.indeed.com/viewjob?jk=55b3e5dfa0c2ff66"
python scripts/indeed_job_listings.py --parameters-json '[{"job_url":"https://fr.indeed.com/viewjob?jk=55b3e5dfa0c2ff66"},{"job_url":"https://www.indeed.com/viewjob?jk=example"}]'
```

If the token was provided in the conversation instead of the environment, pass it with `--token` and do not expose it in user-facing output:

```bash
python scripts/indeed_job_listings.py --token "USER_TOKEN" --job-url "https://fr.indeed.com/viewjob?jk=55b3e5dfa0c2ff66"
```

## Tool

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `job-url` | `indeed_job-listings_by-job-url` | `job_url` | `[{"job_url":"https://fr.indeed.com/viewjob?jk=55b3e5dfa0c2ff66"}]` |

Every request also accepts `file_name`. If omitted, use `{{TasksID}}`.

## Fixed Request Fields

Always submit to `https://scraperapi.dataify.com/builder?platform=1` with:

| Field | Value |
|---|---|
| `spider_name` | `indeed.com` |
| `spider_id` | `indeed_job-listings_by-job-url` |
| `spider_parameters` | JSON array of one or more parameter objects |
| `spider_errors` | `true` |
| `file_name` | User value, otherwise `{{TasksID}}` |

Send parameters as form data. Keep `spider_parameters` as a JSON string inside the form body.
