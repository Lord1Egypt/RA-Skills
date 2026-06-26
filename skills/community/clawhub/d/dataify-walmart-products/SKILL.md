---
name: dataify-walmart-products
description: Submit Dataify Walmart Product Information Builder tasks for four Walmart product collection modes. Use when the user wants the Walmart product information collection tool, collect Walmart products, scrape Walmart product information, crawl Walmart product data, collect Walmart products by URL, collect Walmart products by category URL, collect Walmart products by SKU, collect Walmart products by keyword, create Dataify walmart_product_by-url, walmart_product_by-category-url, walmart_product_by-sku, or walmart_product_by-keywords tasks, or asks in Chinese with meanings like "Walmart 产品信息采集", "Walmart 产品信息抓取", "Walmart产品采集", "Walmart产品抓取", "Walmart产品URL采集", "Walmart类别URL采集", "Walmart SKU采集", "Walmart关键词采集", or similar Walmart product noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Walmart Products

Submit Walmart product information collection jobs through Dataify Builder. This skill is a guided wrapper for four collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| Product URL | `walmart_product_by-url` | Collecting one or more Walmart products by product URL. |
| Category URL | `walmart_product_by-category-url` | Collecting Walmart products by category URL. |
| SKU | `walmart_product_by-sku` | Collecting one or more Walmart products by SKU. |
| Keyword | `walmart_product_by-keywords` | Collecting Walmart products by search keyword and domain. |

After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

## API TOKEN Handling

Use `DATAIFY_API_TOKEN` as the long-term saved token name.

- If the user provides a token in the request, use it for this run.
- If no token is provided, first check whether `DATAIFY_API_TOKEN` is already saved locally in the environment.
- If `DATAIFY_API_TOKEN` is saved locally, use it without asking the user to re-enter the token.
- If no token is available locally, tell the user they need to provide a Dataify API TOKEN.
- If the user does not have an API TOKEN, tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one.
- If the user already has an API TOKEN, tell them it is available in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).
- After the user provides an API TOKEN and no local `DATAIFY_API_TOKEN` is saved, ask whether they want to save it locally as `DATAIFY_API_TOKEN` for future use.
- If the user wants to save it, give the appropriate command for their shell and ask them to run it; do not silently persist tokens without confirmation.
- Do not call the Builder endpoint without a token.
- Always call it `API TOKEN` in user-facing instructions. Prefer the environment variable name `DATAIFY_API_TOKEN` for saved local use.

PowerShell examples for saving the token for the current session:

```powershell
$env:DATAIFY_API_TOKEN = "YOUR_DATAIFY_API_TOKEN"
```

For a persistent user-level variable on Windows:

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "YOUR_DATAIFY_API_TOKEN", "User")
```

## Core Workflow

1. First ask the user to choose a collection mode: `url`, `category-url`, `sku`, or `keywords`.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. If the selected mode has dropdown fields, show the dropdown options as Markdown tables with `Label` and `Value` columns.
4. Ask whether the user wants to change any value before running the task.
5. Ask whether the user wants to collect multiple Walmart product groups for the selected mode.
6. Normalize the final values into a list of parameter objects for the selected mode only.
7. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
8. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
9. Validate the selected mode, URLs, domain, SKU, keyword, numeric values, dropdown values, and file name.
10. Submit the Builder request with the selected mode's `spider_id`.
11. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
12. Stop after Builder succeeds.
13. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect Walmart products by product URL | `url` |
| Collect Walmart products by category URL | `category-url` |
| Collect Walmart products by SKU | `sku` |
| Collect Walmart products by keyword | `keywords` |

Ask: "Which collection mode do you want to use: `url`, `category-url`, `sku`, or `keywords`?"

Do not submit a Builder request until the mode is clear.

## Shared Dropdown Options

Dropdown options for `all_variations`:

| Label | Value |
| --- | --- |
| true | `true` |
| false | `false` |

## Product URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true` | `spider_parameters` | Walmart product URL. |
| `all_variations` | No | `false` | `spider_parameters` | Whether to collect all product variations. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Walmart product URL groups? If yes, provide multiple groups with `url` and `all_variations`."

Product URL mode handling:

- `url` is required. If the user does not provide it, use the default only after showing it in the parameter confirmation table.
- `url` must start with `https://www.walmart.com/`.
- `all_variations` must be `true` or `false`.
- Submit `spider_id=walmart_product_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true","all_variations":"true"}]
```

## Category URL Mode Parameters

Use this section only when the user chooses `category-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `category_url` | Yes | `https://www.walmart.com/shop/deals/food/` | `spider_parameters` | Walmart category URL. |
| `all_variations` | Yes | `false` | `spider_parameters` | Whether to collect all product variations. |
| `page_turning` | Yes | `1` | `spider_parameters` | Page limit. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Walmart category URL groups? If yes, provide multiple groups with `category_url`, `all_variations`, and `page_turning`."

Category URL mode handling:

- `category_url` is required. If the user does not provide it, use the default `https://www.walmart.com/shop/deals/food/` only after showing it in the parameter confirmation table.
- `category_url` must start with `https://www.walmart.com/`.
- `all_variations` must be `true` or `false`.
- `page_turning` must be an integer greater than or equal to `0`.
- Submit `spider_id=walmart_product_by-category-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"category_url":"https://www.walmart.com/shop/deals/food/","all_variations":"false","page_turning":"1"}]
```

## SKU Mode Parameters

Use this section only when the user chooses `sku`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `sku` | Yes | `439179861` | `spider_parameters` | Walmart SKU product code. |
| `all_variations` | No | `false` | `spider_parameters` | Whether to collect all product variations. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Walmart SKU groups? If yes, provide multiple groups with `sku` and `all_variations`."

SKU mode handling:

- `sku` is required. If the user does not provide it, use the default `439179861` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `sku`.
- `sku` cannot be empty.
- `all_variations` must be `true` or `false`.
- Submit `spider_id=walmart_product_by-sku`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"sku":"439179861","all_variations":"false"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keywords`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keyword` | Yes | `leggins` | `spider_parameters` | Walmart search keyword. |
| `domain` | Yes | `https://www.walmart.com/` | `spider_parameters` | Walmart main domain. |
| `all_variations` | No | `false` | `spider_parameters` | Whether to collect all product variations. |
| `page_turning` | No | `2` | `spider_parameters` | Page limit. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then show the `all_variations` dropdown table from Shared Dropdown Options.

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Walmart keyword groups? If yes, provide multiple groups with `keyword`, `domain`, `all_variations`, and `page_turning`."

Keyword mode handling:

- `keyword` is required. If the user does not provide it, use the default `leggins` only after showing it in the parameter confirmation table.
- `keyword` cannot be empty.
- `domain` must start with `https://www.walmart.com/`.
- `all_variations` must be `true` or `false`.
- `page_turning` must be an integer greater than or equal to `0`.
- Submit `spider_id=walmart_product_by-keywords`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keyword":"leggins","domain":"https://www.walmart.com/","all_variations":"false","page_turning":"2"}]
```

## Shared File Name Handling

- `file_name` defaults to `{{TasksID}}`.
- If the user changes `file_name`, submit the user-provided value.
- `file_name` cannot be empty.
- Send `file_name` as a Builder form field.

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=walmart.com`
  - `spider_errors=true`
- Mode-specific field:
  - Product URL mode: `spider_id=walmart_product_by-url`
  - Category URL mode: `spider_id=walmart_product_by-category-url`
  - SKU mode: `spider_id=walmart_product_by-sku`
  - Keyword mode: `spider_id=walmart_product_by-keywords`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array.

## Script

For stable execution, prefer `scripts/submit_dataify_walmart_products.py` with Python 3.6 or newer instead of rewriting the Builder flow.

Product URL mode:

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode url --url "https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true" --all-variations "true"
```

Category URL mode:

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode category-url --category-url "https://www.walmart.com/shop/deals/food/" --all-variations "false" --page-turning "1"
```

SKU mode:

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode sku --sku "439179861" --all-variations "false"
```

Keyword mode:

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode keywords --keyword "leggins" --domain "https://www.walmart.com/" --all-variations "false" --page-turning "2"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode sku --sku "439179861" --file-name "{{TasksID}}"
```

To submit multiple product URL groups:

```powershell
python3 ".\scripts\submit_dataify_walmart_products.py" --mode url --params-json '[{"url":"https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true","all_variations":"true"},{"url":"https://www.walmart.com/ip/HI-CHEW-Stand-Up-Pouch-Getaway-Mix-11-65oz/12284762931?athAsset=eyJhdGhjcGlkIjoiMTIyODQ3NjI5MzEiLCJhdGhzdGlkIjoiQ1MwNTV+Q1MwMDR+Q1MwOTgiLCJhdGhlZSI6eyJhIjoyNy44NCwiYiI6Mjk1MS40MSwidyI6MC4wMDk0MjcxMjc3OTA0NzcxMjMsImwiOjAuNX0sImF0aHBvc2IiOiI4IiwiYXRoYW5jaWQiOiIxMDE2NDUwNzU1IiwiYXRocmsiOjAuMH0%3D&athena=true&adsRedirect=true","all_variations":"true"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `url`, `category-url`, `sku`, or `keywords`.

`url must start with https://www.walmart.com/` means the product URL is outside the allowed Walmart domain.

`category_url must start with https://www.walmart.com/` means the category URL is outside the allowed Walmart domain.

`domain must start with https://www.walmart.com/` means the main domain is outside the allowed Walmart domain.

`all_variations must be true or false` means the variation option is invalid.

`page_turning must be an integer greater than or equal to 0` means the page limit is invalid.

`sku cannot be empty` means the SKU is missing.

`keyword cannot be empty` means the keyword is missing.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or the selected mode's object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, selected `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not mix Product URL, Category URL, SKU, and Keyword mode parameters in the same Builder request.
- Do not submit a Builder request until the mode is clear.
- Do not put `file_name` inside `spider_parameters`.
- Do not use a Walmart URL or domain from outside `https://www.walmart.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
