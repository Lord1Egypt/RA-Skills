---
name: dataify-instagram-profiles
description: Submit Dataify Instagram Profile Builder tasks for two Instagram profile collection modes. Use when the user wants the Instagram personal profile collection tool, collect Instagram profiles, scrape Instagram profiles, crawl Instagram profile data, collect Instagram profiles by username, collect Instagram profiles by profile URL, create Dataify ins_profiles_by-username or ins_profiles_by-profileurl tasks, or asks in Chinese with meanings like "Instagram个人资料采集", "Instagram个人资料抓取", "Instagram个人主页采集", "Instagram个人主页抓取", "Instagram用户资料采集", "Instagram用户名采集", "个人资料URL采集", or similar Instagram profile noun plus collection/scraping action wording. Also use when receiving task_id/status, configuring DATAIFY_API_TOKEN, or troubleshooting this Dataify Builder request.
---

# Dataify Instagram Profiles

Submit Instagram profile collection jobs through Dataify Builder. This skill is a guided wrapper for two collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| Username | `ins_profiles_by-username` | Collecting one or more Instagram profiles by username. |
| Profile URL | `ins_profiles_by-profileurl` | Collecting one or more Instagram profiles by profile URL. |

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

1. First ask the user to choose a collection mode: `username` or `profileurl`. Show the Mode Selection table.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. Ask whether the user wants to change any value before running the task.
4. Ask whether the user wants to collect multiple Instagram profile groups for the selected mode.
5. Normalize the final values into a list of parameter objects for the selected mode only.
6. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
7. If no token is available, ask the user to enter their API TOKEN and ask whether to save it as `DATAIFY_API_TOKEN`.
8. Validate the selected mode, parameters, and file name.
9. Submit the Builder request with the selected mode's `spider_id`.
10. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
11. Stop after Builder succeeds.
12. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect profiles by Instagram username | `username` |
| Collect profiles by profile URL | `profileurl` |

Ask: "Which collection mode do you want to use: `username` or `profileurl`?"

Do not submit a Builder request until the mode is clear.

## Username Mode Parameters

Use this section only when the user chooses `username`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `username` | Yes | `zoobarcelona` | Instagram username. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Instagram profile username groups? If yes, provide multiple `username` values."

Username mode handling:

- `username` is required. If the user does not provide it, use the default `zoobarcelona` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `username`.
- `username` cannot be empty.
- Submit `spider_id=ins_profiles_by-username`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"username":"zoobarcelona"}]
```

## Profile URL Mode Parameters

Use this section only when the user chooses `profileurl`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `profileurl` | Yes | `https://www.instagram.com/cats_of_world_/` | Instagram profile URL. |
| `file_name` | No | `{{TasksID}}` | Builder form field. Use the default when the user does not change it. |

Then ask: "Do you want to change any of these values before I submit the task?"

Also ask: "Do you want to collect multiple Instagram profile URL groups? If yes, provide multiple `profileurl` values."

Profile URL mode handling:

- `profileurl` is required. If the user does not provide it, use the default `https://www.instagram.com/cats_of_world_/` only after showing it in the parameter confirmation table.
- Trim leading and trailing whitespace from `profileurl`.
- `profileurl` cannot be empty.
- `profileurl` must start with `https://www.instagram.com/`.
- Submit `spider_id=ins_profiles_by-profileurl`.
- Submit `spider_parameters` as a JSON string containing one or more objects like:

```json
[{"profileurl":"https://www.instagram.com/cats_of_world_/"}]
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
  - `spider_name=instagram.com`
  - `spider_errors=true`
- Mode-specific field:
  - Username mode: `spider_id=ins_profiles_by-username`
  - Profile URL mode: `spider_id=ins_profiles_by-profileurl`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string array.

## Script

For stable execution, prefer `scripts/submit_dataify_instagram_profiles.py` with Python 3.6 or newer instead of rewriting the Builder flow.

Username mode:

```powershell
python3 ".\scripts\submit_dataify_instagram_profiles.py" --mode username --username "zoobarcelona"
```

Profile URL mode:

```powershell
python3 ".\scripts\submit_dataify_instagram_profiles.py" --mode profileurl --profileurl "https://www.instagram.com/cats_of_world_/"
```

To override the saved environment token or file name:

```powershell
python3 ".\scripts\submit_dataify_instagram_profiles.py" --api-token "YOUR_DATAIFY_API_TOKEN" --mode username --username "zoobarcelona" --file-name "{{TasksID}}"
```

To submit multiple username groups:

```powershell
python3 ".\scripts\submit_dataify_instagram_profiles.py" --mode username --params-json '[{"username":"zoobarcelona"},{"username":"cats_of_world_"}]'
```

To submit multiple profile URL groups:

```powershell
python3 ".\scripts\submit_dataify_instagram_profiles.py" --mode profileurl --params-json '[{"profileurl":"https://www.instagram.com/cats_of_world_/"},{"profileurl":"https://www.instagram.com/zoobarcelona/"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user they need to provide their Dataify API TOKEN, ask whether they want to save it as `DATAIFY_API_TOKEN`, or tell them they can register or log in at [Dataify](https://dashboard.dataify.com/login?utm_source=skill) to get one. If they already have a token, tell them it is in the top-right area of [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `username` or `profileurl`.

`username cannot be empty` means the Instagram username is missing.

`profileurl cannot be empty` means the Instagram profile URL is missing.

`profileurl must start with https://www.instagram.com/` means the URL is outside the allowed Instagram domain.

`File name cannot be empty` means no usable `file_name` was provided.

`Necessary parameters is empty!` usually means the Builder request was not submitted as form fields, `spider_parameters` was not a JSON string array, or the selected mode's object is missing required fields.

Missing `task_id` usually means the authorization header, token, `spider_name`, selected `spider_id`, or `spider_parameters` is wrong.

## Guardrails

- Do not mix username mode and profile URL mode parameters in the same Builder request.
- Do not send `profileurl` in username mode.
- Do not send `username` in profile URL mode.
- Do not submit a Builder request until the mode is clear.
- Use only `API TOKEN` and `DATAIFY_API_TOKEN` when referring to authentication.
- Do not hard-code local Python paths.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
