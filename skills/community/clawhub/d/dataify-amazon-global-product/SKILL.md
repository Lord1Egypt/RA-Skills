---
name: dataify-amazon-global-product
description: "Collect Amazon global-marketplace products by product URL, category URL, keyword, or keyword plus brand. Use when the request explicitly concerns global or multi-market Amazon product data. Do not use for ordinary single-product ASIN details or keyword-and-domain product lists."
---

# Dataify Amazon Global Product

Submit Amazon global product collection jobs through Dataify Builder and continue through final-result retrieval. After submission, continue monitoring the returned `task_id` and return the final result by default.

This skill covers four Amazon global product collection modes:

| Mode | Use for | Builder `spider_id` |
| --- | --- | --- |
| `product-url` | Collect global Amazon product details by product URL. | `amazon_global-product_by-url` |
| `category-url` | Collect global Amazon product details from a category URL. | `amazon_global-product_by-category-url` |
| `keyword` | Collect global Amazon product details from a keyword search. | `amazon_global-product_by-keywords` |
| `keyword-brand` | Collect global Amazon product details from a keyword and brand filter. | `amazon_global-product_by-keywords-brand` |

## Quick Start

**Input:** a product keyword and Amazon domain.

```bash
python3 scripts/submit_amazon_global_product.py keyword --keyword "coffee" --domain "https://www.amazon.com"
```

The command waits up to 10 minutes and prints the final JSON result. Add `--no-wait` only for submission-only behavior.

If `DATAIFY_API_TOKEN` is missing, log in or register at https://dashboard.dataify.com/login?utm_source=skill. New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed.

## API TOKEN Handling

Use `DATAIFY_API_TOKEN` as the long-term saved token name.

- If `DATAIFY_API_TOKEN` is saved locally, use it.
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
4. Ask: "Do you want to change any of these values before I submit the task?"
5. Normalize and validate the final values for the chosen mode.
8. Submit a Builder request to create the task.
9. Read `data.task_id` from the Builder response.
If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

For detailed mode schemas and advanced fields, read [references/modes-and-parameters.md](references/modes-and-parameters.md) only when needed.

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
python3 ".\scripts\submit_amazon_global_product.py" keyword --keyword "coffee" --file-name "amazon-global-coffee"
```

The script prints a JSON summary with `task_id`, submitted parameters and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means `DATAIFY_API_TOKEN` is not set in the environment. Tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).

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

## Default completion behavior

The default deliverable is the collected result, not only a `task_id`.

1. Submit the Builder task once and capture its `task_id`.
2. Immediately continue with `$dataify-task-operations` and monitor the same task ID.
   - Use the default 600-second wait for ordinary collections.
   - Use `--timeout 1800` for media downloads or clearly high-volume, multi-page, or multi-input collections.
3. When the task succeeds, download and return the final JSON result. Summarize large payloads while preserving access to the raw result.
4. If monitoring times out or is interrupted, return the task ID and a resume command. Do not resubmit the paid task.
5. Stop after submission only when the user explicitly asks for submission only, a task ID, or `--no-wait` behavior.

## Parameter interaction policy

- For a clear, low-risk, read-only, and low-cost request, apply safe defaults and execute immediately. A short execution summary is optional; do not pause for confirmation.
- Ask only for a missing required input, a material ambiguity, a high-volume or multi-page scope, a media download, a choice that materially changes credit usage, an irreversible action, or an explicit user request to review parameters.
- When confirmation is required, show only user-facing values that affect the target, scope, output, or cost. Prefer one concise sentence; use a compact table only when three or more consequential values are easier to compare.
- Never show fixed fields, empty optional fields, unchanged defaults, credentials, or internal implementation parameters such as engine selectors, response-format flags, offsets, spider IDs, and file-name templates.
- Keep advanced filters hidden unless the user asks for them or they are needed to resolve ambiguity. Never substitute documentation example values for missing required user input.
- After returning results, offer relevant refinements instead of forcing all optional decisions before the first result.

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
