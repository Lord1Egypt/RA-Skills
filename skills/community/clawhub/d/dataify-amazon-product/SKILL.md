---
name: dataify-amazon-product
description: Use for Dataify Amazon product collection Builder tasks. Trigger when the user asks for Amazon product collection, Amazon product scraping, Amazon product harvesting, or Amazon product crawling, especially with ASIN, URL, keyword, category URL, Best Sellers URL, or similar Amazon product task keywords. Supports creating Amazon product tasks by ASIN, product URL and zip code, keyword, category URL, or Best Sellers URL; returning the task_id; configuring or reusing the DATAIFY_API_TOKEN environment variable; and troubleshooting Dataify Builder request failures.
---

# Dataify Amazon Product

Submit Amazon product collection jobs through Dataify Builder, then stop. Do not download result files. After a successful submission, give the user the `task_id` and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

This skill covers five Amazon product collection modes:

| Mode | Use for | Builder `spider_id` |
| --- | --- | --- |
| `asin` | Collect product details by ASIN. Amazon product URLs can be accepted and converted to ASINs. | `amazon_product_by-asin` |
| `url` | Collect product details by one or more Amazon product URLs and a zip code. | `amazon_product_by-url` |
| `keyword` | Collect Amazon keyword search results. | `amazon_product_by-keywords` |
| `category-url` | Collect Amazon category listing results from a category URL. | `amazon_product_by-category-url` |
| `best-sellers-url` | Collect Amazon Best Sellers listing results from a Best Sellers URL. | `amazon_product_by-best-sellers` |

## API TOKEN Handling

Use `DATAIFY_API_TOKEN` as the long-term saved token name.

- If the user provides a token in the request, use it for this run.
- If no token is provided, first check whether `DATAIFY_API_TOKEN` is already saved locally in the environment.
- If `DATAIFY_API_TOKEN` is saved locally, use it.
- If no token is available locally, tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).
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

1. Identify the collection mode from the user's request: `asin`, `url`, `keyword`, `category-url`, or `best-sellers-url`.
2. Before submitting, show the user the required values, optional values, and defaults for that mode.
3. Always display submitted parameters as a Markdown table; do not use a plain sentence or bullet list for parameter confirmation.
4. Ask: "Do you want to change any of these values before I submit the task?"
5. Normalize and validate the final values for the chosen mode.
6. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
7. If no token is available, tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).
8. Submit a Builder request to create the task.
9. Read `data.task_id` from the Builder response.
10. Stop after Builder succeeds.
11. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Parameter Checklists

### ASIN

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `asin` | Yes | No default | One or more ASINs. Amazon product URLs can be accepted and converted to ASINs. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Submit multiple ASINs as an array of objects, for example `[{"asin":"B0BZYCJK89"}]`.

### Product URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | No default | One or more complete Amazon product URLs. |
| `zip_code` | Yes | No default | Zip code used for each Amazon URL, for example `94107`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Submit multiple URLs as an array of objects, for example `[{"url":"https://www.amazon.com/.../dp/B0BRXPR726","zip_code":"94107"}]`.

### Keyword

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | No default | Amazon search keyword. |
| `page_turning` | No | `2` | Integer greater than or equal to `1`. |
| `lowest_price` | No | `10` | Lowest price filter. |
| `highest_price` | No | `50` | Highest price filter. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Require `lowest_price <= highest_price`.

### Category URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | No default | Amazon category URL. |
| `page_turning` | Yes | No default | Integer greater than or equal to `1`. |
| `sort_by` | No | `Best Sellers` | Dropdown-style option. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Show all `sort_by` options as a Markdown table with both `Label` and `Value` columns before asking the user to choose.

| Label | Value |
| --- | --- |
| `Best Sellers` | `Best Sellers` |
| `Newest Arrivals` | `Newest Arrivals` |
| `Avg. Customer Review` | `Avg. Customer Review` |
| `Price: High to Low` | `Price: High to Low` |
| `Price: Low to High` | `Price: Low to High` |
| `Featured` | `Featured` |

Accepted `sort_by` display values and submitted values:

- best sellers or `Best Sellers` -> `Best Sellers`
- newest arrivals or `Newest Arrivals` -> `Newest Arrivals`
- average customer review or `Avg. Customer Review` -> `Avg. Customer Review`
- price high to low or `Price: High to Low` -> `Price: High to Low`
- price low to high or `Price: Low to High` -> `Price: Low to High`
- featured recommendations or `Featured` -> `Featured`

### Best Sellers URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | No default | Amazon Best Sellers category URL. |
| `page_turning` | Yes | No default | Integer greater than or equal to `1`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=amazon.com`
  - `spider_errors=true`
- Dynamic fields:
  - `spider_id` must match the chosen mode.
  - `spider_parameters` must be a JSON string, not a raw object.
  - `file_name` defaults to `{{TasksID}}` and can be changed by the user.
- Send `file_name` as the Builder form field, not as a downloaded output name.

## Script

For stable execution, prefer `scripts/submit_amazon_product.py` with Python 3.6 or newer instead of rewriting the Builder flow. The script writes and reads UTF-8 text.

```powershell
python3 ".\scripts\submit_amazon_product.py" asin B0BZYCJK89
python3 ".\scripts\submit_amazon_product.py" url --zip-code "94107" "https://www.amazon.com/HISDERN-Checkered-Handkerchief-Classic-Necktie/dp/B0BRXPR726"
python3 ".\scripts\submit_amazon_product.py" keyword --keyword "coffee"
python3 ".\scripts\submit_amazon_product.py" category-url --url "https://www.amazon.com/s?i=fashion" --page-turning 2 --sort-by "Best Sellers"
python3 ".\scripts\submit_amazon_product.py" best-sellers-url --url "https://www.amazon.com/Best-Sellers-Tools-Home-Improvement-Kitchen-Bath-Fixtures/zgbs/hi/3754161/ref=zg_bs_unv_hi_2_680350011_1" --page-turning 1
```

If `python3` is not available, use the local Python 3 command for that machine, such as `python`. The script checks the runtime version and tells the user to use Python 3.6 or newer if the active interpreter is too old.

To override the saved environment token or default file name for one run:

```powershell
python3 ".\scripts\submit_amazon_product.py" keyword --api-token "YOUR_DATAIFY_API_TOKEN" --keyword "coffee" --file-name "amazon-coffee"
```

The script prints a JSON summary with `task_id`, submitted parameters, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).

`No valid ASINs were provided` means the required `asin` value is missing or could not be extracted from the provided input.

`No valid URLs were provided` or `URL cannot be empty` means the required URL value is missing.

`Zip code cannot be empty` means no usable `zip_code` was provided.

`Keyword cannot be empty` means the required `keyword` value is missing.

`Page turning must be greater than or equal to 1` means the requested page count is invalid.

`Lowest price cannot be greater than highest price` means the price range must be corrected before submission.

`Unsupported sort_by` means the category sort option must be one of the accepted display values or submitted values.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string, or the object is missing required mode parameters.

Missing `task_id` usually means the authorization header, token, `spider_name`, or `spider_id` is wrong.

## Guardrails

- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
