---
name: dataify-amazon-seller
description: Use for Dataify Amazon seller information collection Builder tasks. Trigger when the user says or asks for Amazon 卖家信息采集工具, Amazon seller information collection tool, Amazon seller collection tool, Amazon seller information collection, Amazon seller scraping, or Amazon seller URL collection by URL. Supports creating an amazon_seller_by-url task; returning the task_id; configuring or reusing the DATAIFY_API_TOKEN environment variable; and troubleshooting Dataify Builder request failures.
---

# Dataify Amazon Seller

Submit Amazon seller information collection jobs by URL through Dataify Builder, then stop. After a successful submission, give the user the `task_id` and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

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

1. Before submitting, show the user the required values, optional values, and defaults listed in the Parameter Checklist.
2. Always display submitted parameters as a Markdown table; do not use a plain sentence or bullet list for parameter confirmation.
3. Ask: "Do you want to change any of these values before I submit the task?"
4. Normalize the final values into `url` and `file_name`.
5. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
6. If no token is available, tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).
7. Validate the URL and file name.
8. Submit a Builder request to create the task.
9. Read `data.task_id` from the Builder response.
10. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Parameter Checklist

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.amazon.com/sp?ie=UTF8&seller=ADZ7LD48GVFQJ&asin=B07H56J7K1&ref_=dp_merchant_link&isAmazonFulfilled=1` | Amazon seller URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Can be changed by the user. |

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=amazon.com`
  - `spider_id=amazon_seller_by-url`
  - `spider_errors=true`
- Dynamic fields:
  - `spider_parameters` must be a JSON string, not a raw object.
  - `file_name` defaults to `{{TasksID}}` and can be changed by the user.

## Script

For stable execution, prefer `scripts/submit_amazon_seller.py` with Python 3.6 or newer instead of rewriting the Builder flow. The script writes and reads UTF-8 text.

```powershell
python3 ".\scripts\submit_amazon_seller.py"
python3 ".\scripts\submit_amazon_seller.py" --url "https://www.amazon.com/sp?ie=UTF8&seller=ADZ7LD48GVFQJ&asin=B07H56J7K1&ref_=dp_merchant_link&isAmazonFulfilled=1" --file-name "amazon-seller"
```

The script prints a JSON summary with `task_id`, `url`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).

`URL cannot be empty` means no usable seller URL was provided.

`File name cannot be empty` means no usable `file_name` was provided.

Missing `task_id` usually means the authorization header, token, `spider_name`, or `spider_id` is wrong.

## Guardrails

- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
