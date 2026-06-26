---
name: dataify-reddit-posts
description: Submit Dataify Reddit Post Information Builder tasks for three Reddit post collection modes. Use when the user wants the Reddit post information collection tool, collect Reddit posts, scrape Reddit posts, crawl Reddit post data, collect Reddit posts by post URL, collect Reddit posts by keyword, collect Reddit posts by subreddit URL, create Dataify reddit_posts_by-url, reddit_posts_by-keywords, or reddit_posts_by-subredditurl tasks, or asks in Chinese with meanings like "Reddit 帖子采集", "Reddit 帖子抓取", "Reddit帖子信息采集", "Reddit帖子信息抓取", "Reddit帖子URL采集", "Reddit关键词采集", "Reddit subreddit url采集", or similar Reddit post noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Reddit Posts

Submit Reddit post information collection jobs through Dataify Builder. This skill is a guided wrapper for three collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| Post URL | `reddit_posts_by-url` | Collecting one or more Reddit posts by post URL. |
| Keyword | `reddit_posts_by-keywords` | Collecting Reddit posts by search keyword. |
| Subreddit URL | `reddit_posts_by-subredditurl` | Collecting Reddit posts from a subreddit URL with sort and time options. |

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

1. First ask the user to choose a collection mode: `url`, `keywords`, or `subredditurl`.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. If the selected mode has dropdown fields, show the dropdown options as Markdown tables with `Label` and `Value` columns.
4. Ask whether the user wants to change any value before running the task.
5. Ask whether the user wants to collect multiple Reddit post groups for the selected mode.
6. Normalize the final values into a list of parameter objects for the selected mode only.
7. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
8. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
9. Validate the selected mode, URLs, numeric values, dropdown values, and file name.
10. Submit the Builder request with the selected mode's `spider_id`.
11. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
12. Stop after Builder succeeds.
13. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect Reddit posts by post URL | `url` |
| Collect Reddit posts by keyword | `keywords` |
| Collect Reddit posts by subreddit URL | `subredditurl` |

Ask: "Which collection mode do you want to use: `url`, `keywords`, or `subredditurl`?"

Do not submit a Builder request until the mode is clear.

## Post URL Mode Parameters

Use this section only when the user chooses `url`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/` | `spider_parameters` | Reddit post URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Reddit post URL groups? If yes, provide multiple `url` values."

Post URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.reddit.com/`.
- Submit `spider_id=reddit_posts_by-url`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"}]
```

## Keyword Mode Parameters

Use this section only when the user chooses `keywords`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `keyword` | Yes | `datascience` | `spider_parameters` | Reddit post search keyword. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of posts to collect. Must be an integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Reddit keyword groups? If yes, provide multiple groups with `keyword` and `num_of_posts`."

Keyword mode handling:

- `keyword` is required. If the user does not provide it, use the default `datascience` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `keyword`.
- `keyword` cannot be empty.
- `num_of_posts` must be an integer greater than or equal to `0`.
- Submit `spider_id=reddit_posts_by-keywords`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"keyword":"datascience","num_of_posts":"10"}]
```

## Subreddit URL Mode Parameters

Use this section only when the user chooses `subredditurl`.

| Field | Required | Default | Location | Notes |
| --- | --- | --- | --- | --- |
| `url` | Yes | `https://www.reddit.com/r/battlefield2042` | `spider_parameters` | Subreddit URL. |
| `sort_by` | No | `Hot` | `spider_parameters` | Post sort option. |
| `num_of_posts` | No | `10` | `spider_parameters` | Maximum number of posts to collect. Must be an integer greater than or equal to `0`. |
| `sort_by_time` | No | `Now` | `spider_parameters` | Time sort option. Time fields do not take effect with `Hot` and `New`. |
| `file_name` | No | `{{TasksID}}` | Builder form field | Use the default when the user does not change it. |

Dropdown options for `sort_by`:

| Label | Value |
| --- | --- |
| Hot | `Hot` |
| Top | `Top` |
| New | `New` |
| Rising | `Rising` |

Dropdown options for `sort_by_time`:

| Label | Value |
| --- | --- |
| Now | `Now` |
| Today | `Today` |
| This Week | `This Week` |
| This Month | `This Month` |
| This Year | `This Year` |
| All Time | `All Time` |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Reddit subreddit URL groups? If yes, provide multiple groups with `url`, `sort_by`, `num_of_posts`, and `sort_by_time`."

Subreddit URL mode handling:

- `url` is required. If the user does not provide it, use the default `https://www.reddit.com/r/battlefield2042` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.reddit.com/`.
- `sort_by` must be one of `Hot`, `Top`, `New`, or `Rising`.
- `sort_by_time` must be one of `Now`, `Today`, `This Week`, `This Month`, `This Year`, or `All Time`.
- `num_of_posts` must be an integer greater than or equal to `0`.
- Time fields do not take effect with `Hot` and `New`; keep the submitted value if the user provides it.
- Submit `spider_id=reddit_posts_by-subredditurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.reddit.com/r/battlefield2042","sort_by":"Rising","num_of_posts":"10","sort_by_time":"Now"}]
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
  - `spider_name=reddit.com`
  - `spider_errors=true`
- Mode-specific field:
  - Post URL mode: `spider_id=reddit_posts_by-url`
  - Keyword mode: `spider_id=reddit_posts_by-keywords`
  - Subreddit URL mode: `spider_id=reddit_posts_by-subredditurl`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array.

## Script

For stable execution, prefer `scripts/submit_dataify_reddit_posts.py` with Python 3.6 or newer instead of rewriting the Builder flow.

Post URL mode:

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode url --url "https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"
```

Keyword mode:

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode keywords --keyword "datascience" --num-of-posts "10"
```

Subreddit URL mode:

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode subredditurl --url "https://www.reddit.com/r/battlefield2042" --sort-by "Rising" --num-of-posts "10" --sort-by-time "Now"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode keywords --keyword "datascience" --file-name "{{TasksID}}"
```

To submit multiple post URL groups:

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode url --params-json '[{"url":"https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"},{"url":"https://www.reddit.com/r/battlefield2042/comments/1cmqs1d/official_update_on_the_next_battlefield_game/"}]'
```

To submit multiple keyword groups:

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode keywords --params-json '[{"keyword":"datascience","num_of_posts":"10"},{"keyword":"machinelearning","num_of_posts":"10"}]'
```

To submit multiple subreddit URL groups:

```powershell
python3 ".\scripts\submit_dataify_reddit_posts.py" --mode subredditurl --params-json '[{"url":"https://www.reddit.com/r/battlefield2042","sort_by":"Rising","num_of_posts":"10","sort_by_time":"Now"},{"url":"https://www.reddit.com/r/battlefield2042","sort_by":"Rising","num_of_posts":"10","sort_by_time":"Now"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `url`, `keywords`, or `subredditurl`.

`url cannot be empty` means the Reddit URL is missing.

`url must start with https://www.reddit.com/` means the URL is outside the allowed Reddit domain.

`keyword cannot be empty` means the Reddit keyword is missing.

`num_of_posts must be an integer greater than or equal to 0` means the post count is invalid.

`sort_by must be one of Hot, Top, New, Rising` means the subreddit sort option is invalid.

`sort_by_time must be one of Now, Today, This Week, This Month, This Year, All Time` means the subreddit time option is invalid.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or the selected mode's object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, selected `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not mix Post URL, Keyword, and Subreddit URL mode parameters in the same Builder request.
- Do not submit a Builder request until the mode is clear.
- Do not put `file_name` inside `spider_parameters`.
- Do not use a Reddit URL from outside `https://www.reddit.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
