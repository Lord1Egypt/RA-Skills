---
name: dataify-facebook-events
description: Submit Dataify Facebook Event Builder tasks for three Facebook event collection modes. Use when the user wants the Facebook event collection tool, collect Facebook events, scrape Facebook events, crawl Facebook event data, collect Facebook events by event list URL, collect Facebook events by event search URL, collect Facebook events by event URL, create Dataify facebook_event_by-eventlist-url, facebook_event_by-search-url, or facebook_event_by-events-url tasks, or asks in Chinese with meanings like "Facebook活动采集", "Facebook活动抓取", "Facebook活动信息采集", "Facebook活动信息抓取", "活动列表URL采集", "活动搜索URL采集", "活动URL采集", or similar Facebook event noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Facebook Events

Submit Facebook event collection jobs through Dataify Builder. This skill is a guided wrapper for three collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| Event List URL | `facebook_event_by-eventlist-url` | Collecting events from a Facebook event list URL. |
| Event Search URL | `facebook_event_by-search-url` | Collecting events from a Facebook event search URL. |
| Event URL | `facebook_event_by-events-url` | Collecting one or more specific Facebook event URLs. |

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

1. First ask the user to choose a collection mode: `eventlist-url`, `search-url`, or `events-url`. Show the Mode Selection table.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple Facebook event groups for the selected mode. If yes, ask for multiple `url` values.
5. Normalize the final values into a list of parameter objects for the selected mode only.
6. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
7. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
8. Validate the selected mode, URLs, and file name.
9. Submit the Builder request with the selected mode's `spider_id`.
10. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
11. Stop after Builder succeeds.
12. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect by event list URL | `eventlist-url` |
| Collect by event search URL | `search-url` |
| Collect by event URL | `events-url` |

Ask: "Which collection mode do you want to use: `eventlist-url`, `search-url`, or `events-url`?"

Do not submit a Builder request until the mode is clear.

## Event List URL Mode Parameters

Use this section only when the user chooses `eventlist-url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/nohoclub/events` | Facebook event list URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Facebook event list URL groups? If yes, provide multiple `url` values."

Submit `spider_id=facebook_event_by-eventlist-url`.

## Event Search URL Mode Parameters

Use this section only when the user chooses `search-url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/events/explore/us-atlanta/107991659233606` | Facebook event search URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Facebook event search URL groups? If yes, provide multiple `url` values."

Submit `spider_id=facebook_event_by-search-url`.

## Event URL Mode Parameters

Use this section only when the user chooses `events-url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.facebook.com/events/1546764716269782` | Facebook event URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Facebook event URL groups? If yes, provide multiple `url` values."

Submit `spider_id=facebook_event_by-events-url`.

## Parameter Handling

- `url` is required. If the user does not provide it, use the selected mode's default only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `url`.
- `url` cannot be empty.
- `url` must start with `https://www.facebook.com/`.
- Multiple collection groups repeat only `url` inside `spider_parameters`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"url":"https://www.facebook.com/events/1546764716269782"},{"url":"https://www.facebook.com/events/1546764716269782"}]
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
  - `spider_name=facebook.com`
  - `spider_errors=true`
- Mode-specific field:
  - Event list URL mode: `spider_id=facebook_event_by-eventlist-url`
  - Event search URL mode: `spider_id=facebook_event_by-search-url`
  - Event URL mode: `spider_id=facebook_event_by-events-url`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array of URL objects.

## Script

For stable execution, prefer `scripts/submit_dataify_facebook_events.py` with Python 3.6 or newer instead of rewriting the Builder flow.

Event list URL mode:

```powershell
python3 ".\scripts\submit_dataify_facebook_events.py" --mode eventlist-url --url "https://www.facebook.com/nohoclub/events"
```

Event search URL mode:

```powershell
python3 ".\scripts\submit_dataify_facebook_events.py" --mode search-url --url "https://www.facebook.com/events/explore/us-atlanta/107991659233606"
```

Event URL mode:

```powershell
python3 ".\scripts\submit_dataify_facebook_events.py" --mode events-url --url "https://www.facebook.com/events/1546764716269782"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_facebook_events.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode events-url --url "https://www.facebook.com/events/1546764716269782" --file-name "{{TasksID}}"
```

To submit multiple URL groups:

```powershell
python3 ".\scripts\submit_dataify_facebook_events.py" --mode events-url --params-json '[{"url":"https://www.facebook.com/events/1546764716269782"},{"url":"https://www.facebook.com/events/1546764716269782"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `eventlist-url`, `search-url`, or `events-url`.

`url cannot be empty` means the required Facebook URL is missing.

`url must start with https://www.facebook.com/` means the URL is outside the allowed Facebook domain.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or one `spider_parameters` object is missing `url`.

Missing `task_id` usually means the authorization header, token, `spider_name`, selected `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not mix mode-specific meanings in one Builder request.
- Do not submit a Builder request until the mode is clear.
- Do not use a Facebook URL from outside `https://www.facebook.com/`.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
