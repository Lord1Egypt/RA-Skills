---
name: dataify-facebook-post-by-url
description: Submit Dataify Facebook Post by Post URL Builder tasks. Use when the user wants the Facebook post collection tool, collect Facebook posts, scrape Facebook posts, crawl Facebook post data, collect Facebook post by URL, create a Dataify facebook_post_by-posts-url task, or asks in Chinese with meanings like "Facebook帖子采集", "Facebook帖子抓取", "Facebook帖子信息采集", "Facebook帖子信息抓取", "帖子URL采集", "帖子采集", "帖子抓取", or similar Facebook post noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Facebook Post By URL

Submit Facebook post collection jobs through Dataify Builder by post URL. After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

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

1. Before submitting, show the user the required values, optional values, and defaults listed in the Parameter Checklist.
2. Ask whether the user wants to change any value before running the task.
3. Ask whether the user wants to collect multiple Facebook posts. If yes, ask for multiple `url` values.
4. Normalize the final values into a list of `spider_parameters` objects.
5. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
6. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
7. Validate the URLs and file name.
8. Submit the Builder request with `spider_id=facebook_post_by-posts-url`.
9. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
10. Stop after Builder succeeds.
11. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Parameter Checklist

When the user invokes this skill, first tell them these values are used. Always display submitted parameters as a Markdown table; do not use a plain sentence or bullet list for the parameter confirmation.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#` | `spider_parameters` | Facebook post URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Facebook posts? If yes, provide multiple `url` values."

If the user has already provided some values, show those values in place of the defaults and only ask whether the remaining/defaulted values should be changed.

## Parameter Handling

- `url` is required. If the user does not provide it, use the default post URL only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.facebook.com/`.
- Multiple collection groups repeat only `url` inside `spider_parameters`.
- `file_name` defaults to `{{TasksID}}`. If the user changes it, submit the user-provided value.
- `file_name` cannot be empty.

Single-group example:

```json
spider_parameters=[{"url":"https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#"}]
```

Multi-group example:

```json
spider_parameters=[{"url":"https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#"},{"url":"https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#"}]
```

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=facebook.com`
  - `spider_id=facebook_post_by-posts-url`
  - `spider_errors=true`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array of URL objects.

## Script

For stable execution, prefer `scripts/submit_dataify_facebook_post_by_url.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_facebook_post_by_url.py" --url "https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_facebook_post_by_url.py" --api-token "YOUR_DATAIFY_API_TOKEN" --url "https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#" --file-name "{{TasksID}}"
```

To submit multiple URLs:

```powershell
python3 ".\scripts\submit_dataify_facebook_post_by_url.py" --params-json '[{"url":"https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#"},{"url":"https://www.facebook.com/permalink.php?story_fbid=pfbid0gNjZBhqCxSqj9xJS5aygNwqFqNEM2fYbTFKKbsvvGdEfTgFyAYWSckvkEHPqAE7gl&id=61574926580533&rdid=86oaujwNGCCdPLfj#"}]'
```

The script prints a JSON summary with `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`url cannot be empty` means the required Facebook post URL is missing.

`url must start with https://www.facebook.com/` means the URL is outside the allowed Facebook domain.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or one `spider_parameters` object is missing `url`.

Missing `task_id` usually means the authorization header, token, `spider_name`, `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not put `file_name` inside `spider_parameters`.
- Do not use a Facebook URL from outside `https://www.facebook.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
