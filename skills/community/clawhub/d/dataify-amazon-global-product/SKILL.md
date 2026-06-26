---
name: dataify-amazon-global-product
description: Use for Dataify Amazon global product collection Builder tasks. Trigger when the user says or asks for Amazon 全球产品详情采集工具, Amazon global product collection tool, Amazon global product details collection tool, Amazon global product collection, Amazon global product scraping, Amazon global product harvesting, or Amazon global product crawling, especially with product URL, category URL, keyword, keyword brand, brand, or similar Amazon global product task keywords. Supports creating Amazon global product tasks by product URL, category URL, keyword, or keyword and brand; returning the task_id; configuring or reusing the DATAIFY_API_TOKEN environment variable; and troubleshooting Dataify Builder request failures.
---

# Dataify Amazon Global Product

Submit Amazon global product collection jobs through Dataify Builder, then stop. After a successful submission, give the user the `task_id` and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

This skill covers four Amazon global product collection modes:

| Mode | Use for | Builder `spider_id` |
| --- | --- | --- |
| `product-url` | Collect global Amazon product details by product URL. | `amazon_global-product_by-url` |
| `category-url` | Collect global Amazon product details from a category URL. | `amazon_global-product_by-category-url` |
| `keyword` | Collect global Amazon product details from a keyword search. | `amazon_global-product_by-keywords` |
| `keyword-brand` | Collect global Amazon product details from a keyword and brand filter. | `amazon_global-product_by-keywords-brand` |

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

1. Identify the collection mode from the user's request: `product-url`, `category-url`, `keyword`, or `keyword-brand`.
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

### Product URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.amazon.com/dp/B0CHHSFMRL/` | Amazon product URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Submit `spider_parameters` as an array with one object, for example `[{"url":"https://www.amazon.com/dp/B0CHHSFMRL/"}]`.

### Category URL

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.amazon.com/s?i=luggage-intl-ship` | Amazon category URL. |
| `maximum` | Yes | `5` | Integer greater than or equal to `0`. |
| `sort_by` | No | `Best Sellers` | Dropdown-style option. |
| `get_sponsored` | No | `true` | Dropdown-style option: `true` or `false`. |
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

Show all `get_sponsored` options as a Markdown table with both `Label` and `Value` columns before asking the user to choose.

| Label | Value |
| --- | --- |
| `Include Sponsored Products` | `true` |
| `Exclude Sponsored Products` | `false` |

Accepted `sort_by` display values and submitted values:

- best sellers or `Best Sellers` -> `Best Sellers`
- newest arrivals or `Newest Arrivals` -> `Newest Arrivals`
- average customer review or `Avg. Customer Review` -> `Avg. Customer Review`
- price high to low or `Price: High to Low` -> `Price: High to Low`
- price low to high or `Price: Low to High` -> `Price: Low to High`
- featured recommendations or `Featured` -> `Featured`

### Keyword

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `coffee` | Amazon search keyword. |
| `domain` | Yes | `https://www.amazon.com` | Amazon domain. |
| `lowest_price` | No | `20` | Integer greater than or equal to `0`. |
| `highest_price` | No | `50` | Integer greater than or equal to `0`, and must not be less than `lowest_price`. |
| `page_turning` | No | `2` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

Require `highest_price >= lowest_price`.

### Keyword Brand

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `shirts` | Amazon search keyword. |
| `brands` | Yes | `Adidas` | Brand filter. |
| `page_turning` | Yes | `2` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=amazon.com`
  - `spider_errors=true`
- Dynamic fields:
  - The Builder URL depends on the chosen mode.
  - `spider_id` must match the chosen mode.
  - `spider_parameters` must be a JSON string, not a raw object.
  - `file_name` defaults to `{{TasksID}}` and can be changed by the user.
- Send `file_name` as the Builder form field, not as a downloaded output name.

Builder URL by mode:

| Mode | URL |
| --- | --- |
| `product-url` | `https://scraperapi.dataify.com/builder` |
| `category-url` | `https://scraperapi.dataify.com/builder?platform=1` |
| `keyword` | `https://scraperapi.dataify.com/builder?platform=1` |
| `keyword-brand` | `https://scraperapi.dataify.com/builder?platform=1` |

## Script

For stable execution, prefer `scripts/submit_amazon_global_product.py` with Python 3.6 or newer instead of rewriting the Builder flow. The script writes and reads UTF-8 text.

```powershell
python3 ".\scripts\submit_amazon_global_product.py" product-url
python3 ".\scripts\submit_amazon_global_product.py" category-url --url "https://www.amazon.com/s?i=luggage-intl-ship" --maximum 5 --sort-by "Best Sellers" --get-sponsored true
python3 ".\scripts\submit_amazon_global_product.py" keyword --keyword "coffee" --domain "https://www.amazon.com"
python3 ".\scripts\submit_amazon_global_product.py" keyword-brand --keyword "shirts" --brands "Adidas" --page-turning 2
```

If `python3` is not available, use the local Python 3 command for that machine, such as `python`. The script checks the runtime version and tells the user to use Python 3.6 or newer if the active interpreter is too old.

To override the saved environment token or default file name for one run:

```powershell
python3 ".\scripts\submit_amazon_global_product.py" keyword --api-token "YOUR_DATAIFY_API_TOKEN" --keyword "coffee" --file-name "amazon-global-coffee"
```

The script prints a JSON summary with `task_id`, submitted parameters, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).

`URL cannot be empty` means no usable URL was provided.

`Keyword cannot be empty` means no usable keyword was provided.

`Brands cannot be empty` means no usable brand value was provided.

`Domain cannot be empty` means no usable domain was provided.

`Maximum must be greater than or equal to 0` means the requested maximum count is invalid.

`Page turning must be greater than or equal to 0` means the requested page count is invalid.

`Lowest price must be greater than or equal to 0` means the requested lowest price is invalid.

`Highest price must be greater than or equal to 0` means the requested highest price is invalid.

`Highest price cannot be less than lowest price` means the price range must be corrected before submission.

`Unsupported sort_by` means the category sort option must be one of the accepted display values or submitted values.

`get_sponsored must be true or false` means the sponsored option must be corrected before submission.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string, or the object is missing required mode parameters.

Missing `task_id` usually means the authorization header, token, `spider_name`, or `spider_id` is wrong.

## Guardrails

- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
