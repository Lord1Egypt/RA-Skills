---
name: dataify-indeed-companies-info
description: Collect Indeed company information through Dataify Scraper API. Use when the user asks to gather, scrape, crawl, fetch, extract, or collect Indeed company/company profile/company information data, including noun-plus-verb requests such as "Indeed company info scrape", "Indeed companies collect", "Indeed 公司信息采集", "Indeed 公司信息抓取", or requests using an Indeed company list URL, company keyword, industry and state/location, or company URL. This skill maps requests to spider IDs indeed_companies-info_by-company-list-url, indeed_companies-info_by-keyword, indeed_companies-info_by-industry-and-state, and indeed_companies-info_by-company-url.
---

# Dataify Indeed Companies Info

Use this skill to create Indeed company information collection tasks through Dataify's builder endpoint.

## Required Workflow

1. Identify the collection mode from the user's request.
   - Use `indeed_companies-info_by-company-list-url` when the user provides or asks to use an Indeed company list URL.
   - Use `indeed_companies-info_by-keyword` when the user provides a company keyword.
   - Use `indeed_companies-info_by-industry-and-state` when the user provides an Indeed industry and optional region/state.
   - Use `indeed_companies-info_by-company-url` when the user provides a specific Indeed company URL.
   - If the mode cannot be inferred, ask which mode to use before showing the parameter table.
2. Check the local Python runtime before calling scripts. Prefer `python`; use `python3` if that is the available Python command. Require Python 3 or newer. Do not use version-specific commands such as `py -3.10`.
3. Ask whether the user wants to collect multiple parameter sets. If yes, collect multiple `spider_parameters` objects for the same spider ID. If the user already supplied multiple values, treat that as a multiple-set request.
4. Before every real API call, show a Markdown confirmation table with the exact parameters that will be submitted. The table must use these columns: `Parameter`, `Current value`, `Default value`, `Required`, `Description`.
5. When the selected mode has dropdown fields, show every available dropdown value in Markdown tables with exactly these columns: `Label`, `Value`. Use `scripts/preview_params.py --dropdown industry` and `scripts/preview_params.py --dropdown state` to generate complete tables.
6. Ask the user whether any value should be changed. Do not call the API until the user explicitly confirms the table.
7. Check for the Dataify API token only after parameter confirmation. Prefer a token explicitly provided by the user, then `DATAIFY_API_TOKEN` from the environment.
8. If no token is available, tell the user: `Missing Dataify API token. Provide a token, or log in/register at` [Dataify](https://dashboard.dataify.com/login?utm_source=skill) `If you already have one, open` [Dataify](https://dashboard.dataify.com?utm_source=skill) `and copy the API TOKEN from the top-right area.`
9. If the user provides a token and `DATAIFY_API_TOKEN` is not already saved locally, ask whether to save it as `DATAIFY_API_TOKEN`. Save it only after explicit consent and never echo the token back.
10. After the API call, report the collection task ID and status. Look for common response fields such as `task_id`, `taskId`, `id`, `status`, `data.task_id`, `data.id`, or `data.status`. Then remind the user to view task details in the official dashboard: [Dataify](https://dashboard.dataify.com?utm_source=skill)

## Parameter Preview

Use the preview helper whenever possible:

```bash
python scripts/preview_params.py --tool keyword --keyword openai
python scripts/preview_params.py --tool company-list-url
python scripts/preview_params.py --tool industry-and-state --industry "Accounting & Tax" --state "Alabama - 60 companies"
python scripts/preview_params.py --tool company-url --company-url "https://www.indeed.com/cmp/Allstate-Insurance"
```

For multiple parameter sets, pass the exact JSON array:

```bash
python scripts/preview_params.py --tool keyword --parameters-json '[{"keyword":"openai"},{"keyword":"anthropic"}]'
```

## API Call

Use the call helper after confirmation and token handling:

```bash
python scripts/indeed_companies_info.py --tool keyword --keyword openai
python scripts/indeed_companies_info.py --tool keyword --parameters-json '[{"keyword":"openai"},{"keyword":"anthropic"}]'
python scripts/indeed_companies_info.py --tool industry-and-state --industry "Accounting & Tax" --state "Alabama - 60 companies"
```

If the token was provided in the conversation instead of the environment, pass it with `--token` and do not expose it in user-facing output:

```bash
python scripts/indeed_companies_info.py --token "USER_TOKEN" --tool company-url --company-url "https://www.indeed.com/cmp/Allstate-Insurance"
```

## Tools

| Mode | Spider ID | Required parameters | Default spider_parameters |
|---|---|---|---|
| `company-list-url` | `indeed_companies-info_by-company-list-url` | `company_list_url` | `[{"company_list_url":"https://www.indeed.com/companies/browse-companies"}]` |
| `keyword` | `indeed_companies-info_by-keyword` | `keyword` | `[{"keyword":"openai"}]` |
| `industry-and-state` | `indeed_companies-info_by-industry-and-state` | `industry` | `[{"industry":"All","state":"United States"}]` |
| `company-url` | `indeed_companies-info_by-company-url` | `company_url` | `[{"company_url":"https://www.indeed.com/cmp/Allstate-Insurance"}]` |

Every tool also accepts `file_name`. If omitted, use `{{TasksID}}`.

## Fixed Request Fields

Always submit to `https://scraperapi.dataify.com/builder?platform=1` with:

| Field | Value |
|---|---|
| `spider_name` | `indeed.com` |
| `spider_id` | One of the four supported Indeed company info spider IDs |
| `spider_parameters` | JSON array of one or more parameter objects |
| `spider_errors` | `true` |
| `file_name` | User value, otherwise `{{TasksID}}` |

Send parameters as form data. Keep `spider_parameters` as a JSON string inside the form body.
