---
name: dataify-youtube-video-post
description: Use for Dataify YouTube video post collection Builder tasks. Trigger when the user asks for the YouTube video post collection tool, YouTube video collection, YouTube video scraping, YouTube video post scraping, YouTube videos by URL, search filters, hashtag, podcast URL, keyword, or Explore URL, or asks with Chinese wording such as YouTube视频抓取, YouTube视频采集, YouTube视频帖子采集, 通过关键词抓取YouTube视频, 通过URL抓取YouTube视频, 通过标签抓取YouTube视频, or 通过探索抓取YouTube视频. Supports choosing between youtube_video-post_by-url, youtube_video-post_by-search-filters, youtube_video-post_by-hashtag, youtube_video-post_by-podcast-url, youtube_video-post_by-keyword, and youtube_video-post_by-explore; receiving task_id/status; and troubleshooting Dataify Builder requests.
---

# Dataify YouTube Video Post

Submit YouTube video post collection jobs through Dataify Builder, then stop. This skill is a guided wrapper for six collection modes:

| Mode | Collector ID | Use For |
| --- | --- | --- |
| URL | `youtube_video-post_by-url` | Collecting video posts from a YouTube channel Videos URL. |
| Search Filters | `youtube_video-post_by-search-filters` | Searching video posts by keyword plus filters. |
| Hashtag | `youtube_video-post_by-hashtag` | Collecting video posts by hashtag. |
| Podcast URL | `youtube_video-post_by-podcast-url` | Collecting video posts from a YouTube podcast or playlist URL. |
| Keyword | `youtube_video-post_by-keyword` | Collecting video posts by keyword. |
| Explore | `youtube_video-post_by-explore` | Collecting video posts from a YouTube Explore URL. |

After a successful submission, give the user the `task_id`, the returned or inferred status, and tell them to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view results.

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

1. First ask the user to choose a collection mode. Show the Mode Selection table.
2. After the user chooses a mode, show only that mode's parameter table and defaults.
3. For any dropdown-style field in the selected mode, show all allowed options as a Markdown table with `Label` and `Value` columns.
4. Ask whether the user wants to change any value before running the task.
5. Ask whether the user wants to collect multiple YouTube video post groups for the selected mode.
6. Normalize the final values into a list of parameter objects for the selected mode only.
7. Resolve the Dataify token from explicit input or saved `DATAIFY_API_TOKEN`.
8. If no token is available, tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).
9. Validate the selected mode, parameters, and file name.
10. Submit the Builder request with the selected mode's `spider_id`.
11. Read `data.task_id` from the Builder response and read `data.status` or `status` when present.
12. Stop after Builder succeeds.
13. Tell the user to visit [Dataify](https://dashboard.dataify.com?utm_source=skill) to view or manage results.

## Mode Selection

When the user invokes this skill, first show this Markdown table and ask them to choose one mode:

| Label | Value |
| --- | --- |
| Collect video posts by channel Videos URL | `url` |
| Collect video posts by search filters | `search_filters` |
| Collect video posts by hashtag | `hashtag` |
| Collect video posts by podcast URL | `podcast_url` |
| Collect video posts by keyword | `keyword` |
| Collect video posts by Explore URL | `explore` |

Ask: "Which collection mode do you want to use?"

Do not submit a Builder request until the mode is clear.

## URL Mode

Use this section only when the user chooses `url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/@stephcurry/videos` | YouTube channel Videos URL. Must use `https://www.youtube.com`. |
| `order_by` | No | `最新` | Dropdown-style option. |
| `start_index` | No | `1` | Integer greater than or equal to `0`. |
| `num_of_posts` | No | `5` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

`order_by` options:

| Label | Value |
| --- | --- |
| Latest | `最新` |
| Popular | `热门` |
| Oldest | `最早` |

Submit `spider_id=youtube_video-post_by-url` with objects like:

```json
[{"url":"https://www.youtube.com/@stephcurry/videos","order_by":"最新","start_index":"1","num_of_posts":"5"}]
```

For multiple URL groups, provide multiple `url`, `order_by`, `start_index`, and `num_of_posts` objects.

## Search Filters Mode

Use this section only when the user chooses `search_filters`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword_search` | Yes | `popular music` | Keyword used to search YouTube videos. |
| `features` | No | `All` | Dropdown-style option. |
| `type` | No | `Videos` | Dropdown-style option. |
| `duration` | No | `Under 3 minutes` | Dropdown-style option. |
| `upload_date` | No | `Last hour` | Dropdown-style option. |
| `num_of_posts` | No | `200` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

`features` options:

| Label | Value |
| --- | --- |
| All | `All` |
| Live | `Live` |
| 4K | `4K` |
| HD | `HD` |
| Subtitles/CC | `Subtitles/CC` |
| Creative Commons | `Creative Commons` |
| 360° | `360°` |
| VR180 | `VR180` |
| 3D | `3D` |
| HDR | `HDR` |

`type` options:

| Label | Value |
| --- | --- |
| Video | `Videos` |
| Movie | `Movies` |

`duration` options:

| Label | Value |
| --- | --- |
| 4 分钟以内 | `4 分钟以内` |
| 4-20 分钟 | `4-20 分钟` |
| 20 分钟以上 | `20 分钟以上` |
| 全部 | `None` |

`upload_date` options:

| Label | Value |
| --- | --- |
| 上一小时 | `Last hour` |
| 今天 | `Today` |
| 本周 | `This week` |
| 本月 | `This month` |
| 今年 | `This year` |
| 全部 | `All` |

Submit `spider_id=youtube_video-post_by-search-filters` with objects like:

```json
[{"keyword_search":"popular music","features":"Subtitles/CC","type":"Videos","duration":"None","upload_date":"Last hour","num_of_posts":"200"}]
```

For multiple search-filter groups, provide multiple `keyword_search`, `features`, `type`, `duration`, `upload_date`, and `num_of_posts` objects.

## Hashtag Mode

Use this section only when the user chooses `hashtag`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `hashtag` | Yes | `shopping` | Topic hashtag used to filter YouTube videos. |
| `num_of_posts` | No | `10` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

Submit `spider_id=youtube_video-post_by-hashtag` with objects like:

```json
[{"hashtag":"shopping","num_of_posts":"10"}]
```

For multiple hashtag groups, provide multiple `hashtag` and `num_of_posts` objects.

## Podcast URL Mode

Use this section only when the user chooses `podcast_url`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/playlist?list=RDCLAK5uy_lS3E3PgpboCkZ_PfLPCkLLNPI1uH6kfc0` | YouTube podcast or playlist URL. Must use `https://www.youtube.com`. |
| `num_of_posts` | No | `10` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

Submit `spider_id=youtube_video-post_by-podcast-url` with objects like:

```json
[{"url":"https://www.youtube.com/playlist?list=RDCLAK5uy_lS3E3PgpboCkZ_PfLPCkLLNPI1uH6kfc0","num_of_posts":"10"}]
```

For multiple podcast URL groups, provide multiple `url` and `num_of_posts` objects.

## Keyword Mode

Use this section only when the user chooses `keyword`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `keyword` | Yes | `top videos` | Keyword used to search YouTube videos. |
| `num_of_posts` | No | `10` | Integer greater than or equal to `0`. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

Submit `spider_id=youtube_video-post_by-keyword` with objects like:

```json
[{"keyword":"top videos","num_of_posts":"10"}]
```

For multiple keyword groups, provide multiple `keyword` and `num_of_posts` objects.

## Explore Mode

Use this section only when the user chooses `explore`.

| Field | Required | Default | Notes |
| --- | --- | --- | --- |
| `url` | Yes | `https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D` | YouTube Explore URL. Must use `https://www.youtube.com`. |
| `all_tabs` | No | `true` | Dropdown-style option. Specifies whether to collect all tabs. |
| `file_name` | No | `{{TasksID}}` | Builder form field. |

`all_tabs` options:

| Label | Value |
| --- | --- |
| Collect all tabs | `true` |
| Do not collect all tabs | `false` |

Submit `spider_id=youtube_video-post_by-explore` with objects like:

```json
[{"url":"https://www.youtube.com/feed/storefront?bp=ogUCKAU%3D","all_tabs":"true"}]
```

For multiple Explore groups, provide multiple `url` and `all_tabs` objects.

## Shared Parameter Handling

- `file_name` defaults to `{{TasksID}}`.
- If the user changes `file_name`, submit the user-provided value.
- `file_name` cannot be empty.
- URL-based modes must accept only URLs whose scheme and host are exactly `https://www.youtube.com`.
- Integer fields must be greater than or equal to `0`.
- Submit numeric and boolean-like values as strings, matching the Builder examples.
- Submit `spider_parameters` as a JSON string containing an array of one or more objects.

## Dataify Builder Request

Use form fields rather than hand-built URL-encoded strings.

- URL: `https://scraperapi.dataify.com/builder?platform=1`
- Method: `POST`
- Authorization header: `Bearer DATAIFY_API_TOKEN`
- Content type: `application/x-www-form-urlencoded`
- Fixed fields:
  - `spider_name=youtube.com`
  - `spider_errors=true`
- Mode-specific `spider_id`:
  - URL mode: `youtube_video-post_by-url`
  - Search Filters mode: `youtube_video-post_by-search-filters`
  - Hashtag mode: `youtube_video-post_by-hashtag`
  - Podcast URL mode: `youtube_video-post_by-podcast-url`
  - Keyword mode: `youtube_video-post_by-keyword`
  - Explore mode: `youtube_video-post_by-explore`
- Default field:
  - `file_name={{TasksID}}`
- Dynamic field:
  - `spider_parameters` must be a JSON string, not a raw object.

## Script

For stable execution, prefer `scripts/submit_dataify_youtube_video_post.py` with Python 3.6 or newer instead of rewriting the Builder flow.

```powershell
python3 ".\scripts\submit_dataify_youtube_video_post.py" --mode keyword --keyword "top videos"
```

If `python3` is not available, use the local Python 3 command for that machine, such as `python`. The script checks the runtime version and tells the user to use Python 3.6 or newer if the active interpreter is too old.

To submit multiple groups, pass a JSON array for the selected mode:

```powershell
python3 ".\scripts\submit_dataify_youtube_video_post.py" --mode hashtag --params-json '[{"hashtag":"shopping","num_of_posts":"10"},{"hashtag":"music","num_of_posts":"25"}]'
```

The script prints a JSON summary with `mode`, `spider_id`, `task_id`, `status`, `parameters`, `file_name`, `dashboard_url`, and `message`.

## Troubleshooting

`Missing Dataify API TOKEN` means no explicit token was passed and `DATAIFY_API_TOKEN` is not saved locally. Tell the user to get an API TOKEN from [Dataify](https://dashboard.dataify.com?utm_source=skill).

`Unsupported mode` means the mode must be `url`, `search_filters`, `hashtag`, `podcast_url`, `keyword`, or `explore`.

`URL must use https://www.youtube.com` means the URL is non-compliant.

`Unsupported order_by`, `Unsupported all_tabs`, or other unsupported dropdown messages mean the value must be one of that field's allowed values.

`File name cannot be empty` means no usable `file_name` was provided.

Missing `task_id` usually means the authorization header, token, `spider_name`, or selected `spider_id` is wrong.

## Guardrails

- Do not mix parameters from different modes in the same Builder request.
- Do not invent result fields.
- Always direct the user to [Dataify](https://dashboard.dataify.com?utm_source=skill) after successful task creation.
