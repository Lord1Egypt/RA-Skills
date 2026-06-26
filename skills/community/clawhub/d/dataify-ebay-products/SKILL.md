---
name: dataify-ebay-products
description: Submit Dataify eBay Product Information Builder tasks for four eBay product collection modes. Use when the user wants the eBay product information collection tool, collect eBay products, scrape eBay product information, crawl eBay product data, collect eBay products by URL, collect eBay products by category URL, collect eBay products by keyword, collect eBay products by store URL, create Dataify ebay_ebay_by-url, ebay_ebay_by-category-url, ebay_ebay_by-keywords, or ebay_ebay_by-listurl tasks, or asks in Chinese with meanings like "eBay 产品信息采集", "eBay 产品信息抓取", "eBay产品采集", "eBay产品抓取", "eBay产品URL采集", "eBay类别URL采集", "eBay关键词采集", "eBay店铺网址采集", or similar eBay product noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify eBay Products

Submit eBay product information collection jobs through Dataify Builder. This skill is a guided wrapper for four collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| Product URL | `ebay_ebay_by-url` | Collecting one or more eBay products by product URL. |
| Category URL | `ebay_ebay_by-category-url` | Collecting eBay products by category URL. |
| Keyword | `ebay_ebay_by-keywords` | Collecting eBay products by search keyword. |
| Store URL | `ebay_ebay_by-listurl` | Collecting eBay products by store URL. |

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

1. First ask the user to choose a collection mode: `url`, `category-url`, `keywords`, or `listurl`.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple eBay product groups for the selected mode.
5. Normalize the final values into a list of parameter objects for the selected mode only.
6. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
7. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
8. Validate the selected mode, URLs, keyword, numeric values, and file name.
9. Submit the Builder request with the selected mode's `spider_id`.
10. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
11. Stop after Builder succeeds.
12. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect eBay products by product URL | `url` |
| Collect eBay products by category URL | `category-url` |
| Collect eBay products by keyword | `keywords` |
| Collect eBay products by store URL | `listurl` |

Ask: "Which collection mode do you want to use: `url`, `category-url`, `keywords`, or `listurl`?"

Do not submit a Builder request until the mode is clear.

## Product URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm` | `spider_parameters` | eBay product URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple eBay product URL groups? If yes, provide multiple `url` values."

Product URL mode handling:

- `url` is required. If the user does not provide it, use the default only after showing it in the parameter confirmation table.
- `url` must start with `https://www.ebay.com/`.
- Submit `spider_id=ebay_ebay_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"}]
```

## Category URL Mode Parameters

Use this section only when the user chooses `category-url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829` | `spider_parameters` | eBay category URL. |
| `Count` | No | `60` | `spider_parameters` | Count field required by this collector. Must be an integer greater than or equal to `0`. |
| `count` | No | `60` | `spider_parameters` | Quantity field. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple eBay category URL groups? If yes, provide multiple groups with `url`, `Count`, and `count`."

Category URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829` only after showing it in the parameter confirmation table.
- `url` must start with `https://www.ebay.com/`.
- `Count` must be an integer greater than or equal to `0`.
- `count` must be an integer greater than or equal to `0`.
- Submit both `Count` and `count` exactly as separate fields.
- Submit `spider_id=ebay_ebay_by-category-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829","Count":"60","count":"60"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keywords`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keywords` | Yes | `baby toys` | `spider_parameters` | eBay search keyword. |
| `count` | No | `60` | `spider_parameters` | Quantity field. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple eBay keyword groups? If yes, provide multiple groups with `keywords` and `count`."

Keyword mode handling:

- `keywords` is required. If the user does not provide it, use the default `baby toys` only after showing it in the parameter confirmation table.
- `keywords` cannot be empty.
- `count` must be an integer greater than or equal to `0`.
- Submit `spider_id=ebay_ebay_by-keywords`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keywords":"baby toys","count":"60"}]
```

## Store URL Mode Parameters

Use this section only when the user chooses `listurl`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086` | `spider_parameters` | eBay store URL. |
| `count` | No | `60` | `spider_parameters` | Quantity field. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple eBay store URL groups? If yes, provide multiple groups with `url` and `count`."

Store URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086` only after showing it in the parameter confirmation table.
- `url` must start with `https://www.ebay.com/`.
- `count` must be an integer greater than or equal to `0`.
- Submit `spider_id=ebay_ebay_by-listurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086","count":"60"}]
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
  - `spider_name=ebay.com`
  - `spider_errors=true`
- Mode-specific field:
  - Product URL mode: `spider_id=ebay_ebay_by-url`
  - Category URL mode: `spider_id=ebay_ebay_by-category-url`
  - Keyword mode: `spider_id=ebay_ebay_by-keywords`
  - Store URL mode: `spider_id=ebay_ebay_by-listurl`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array.

## Script

For stable execution, prefer `scripts/submit_dataify_ebay_products.py` with Python 3.6 or newer instead of rewriting the Builder flow.

Product URL mode:

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode url --url "https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"
```

Category URL mode:

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode category-url --url "https://www.ebay.com/b/Collectible-Japanese-Bells-1900-Now/165467/bn_3104829" --count "60"
```

Keyword mode:

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode keywords --keywords "baby toys" --count "60"
```

Store URL mode:

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode listurl --url "https://www.ebay.com/str/kptradingdeals?_trksid=p4429486.m145687.l149086" --count "60"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode keywords --keywords "baby toys" --file-name "{{TasksID}}"
```

To submit multiple product URL groups:

```powershell
python3 ".\scripts\submit_dataify_ebay_products.py" --mode url --params-json '[{"url":"https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"},{"url":"https://www.ebay.com/itm/187538926483?_skw=Apple&itmmeta=01K4KYKPQW7M913YDTWF9EJKQ4&hash=item2baa30eb93:g:VbMAAeSwtSRot5L8&itmprp=enc%3AAQAKAAAA4MHg7L1Zz0LA5DYYmRTS30kFPVExlz%2FTbUuctB71Yk%2FfQV0aiX%2BN2ICzGj8BIeYBUa7tIGv3VKEgsvuXC0PvIFFvjxEBfsALP5m0Rkcclb576wHpV5%2FGunXNmnt9grpWOipLuKMA0RDkORHa96xYJy8rg%2BYGIi2l2d0Iw2K%2FcLiqP7TlRBd1LsXAjnXShdLOq%2BFxcbaNCarcoIJ%2Fp5DgBLl5UK3WHBVGnpUQZqOMSz1JX0axUzL%2BxlVrnBGK0wekqYG6ShKyf5iRg5%2BY%2F35FueGxIeViMX5ZU5%2B8nFwIGsMl%7Ctkp%3ABFBMjOzO_qRm"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `url`, `category-url`, `keywords`, or `listurl`.

`url must start with https://www.ebay.com/` means the URL is outside the allowed eBay domain.

`keywords cannot be empty` means the keyword is missing.

`Count must be an integer greater than or equal to 0` means the category Count field is invalid.

`count must be an integer greater than or equal to 0` means the quantity field is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or the selected mode's object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, selected `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not mix Product URL, Category URL, Keyword, and Store URL mode parameters in the same Builder request.
- Do not submit a Builder request until the mode is clear.
- Do not put `file_name` inside `spider_parameters`.
- Do not use an eBay URL from outside `https://www.ebay.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
