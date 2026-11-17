# video-highlights-llm API Notes

## Submit

Endpoint:

```text
POST https://mediakit.ap-southeast-1.bytepluses.com/api/v1/tools/video-highlights-llm
```

Required headers:

```text
Authorization: Bearer <BYTEPLUS_MEDIAKIT_API_KEY>
Content-Type: application/json
```

The default environment is production. No environment-specific headers are added by default.

Environment override (self-configured):

```text
x-use-ppe: <value>
x-tt-env: <environment name>
```

The bundled script targets the production endpoint with no extra headers by default. To target an internal environment, set the header values yourself via dedicated environment variables:

- Default: production endpoint, no `x-use-ppe` / `x-tt-env` headers.
- `BYTEPLUS_MEDIAKIT_TT_ENV` sets the `x-tt-env` header; `BYTEPLUS_MEDIAKIT_USE_PPE` sets the `x-use-ppe` header. Both are unset by default, so nothing is sent unless you configure them. Use the environment name provided by your environment owner.
- Alternatively, pass `--header 'Name: value'` (repeatable) or set `BYTEPLUS_MEDIAKIT_HEADERS` to a JSON object of header name/value pairs.
- `--header` and `BYTEPLUS_MEDIAKIT_HEADERS` values override the dedicated environment variables above.

Authentication fallback is `--api-key`, then `BYTEPLUS_MEDIAKIT_API_KEY`, then legacy `MEDIAKIT_API_KEY`, then `~/.mediakit/config.json`.

Prefer these environment variables for new setup: `BYTEPLUS_MEDIAKIT_API_KEY`, `BYTEPLUS_MEDIAKIT_ENDPOINT`, `BYTEPLUS_MEDIAKIT_TT_ENV`, `BYTEPLUS_MEDIAKIT_USE_PPE`, `BYTEPLUS_MEDIAKIT_HEADERS`, `BYTEPLUS_MEDIAKIT_RUNTIME`, and `BYTEPLUS_MEDIAKIT_CONFIG`. The matching legacy `MEDIAKIT_*` variables remain lower-priority fallbacks.

Run a preflight check before submitting a real task when credentials are uncertain:

```bash
python3 scripts/video_highlights_llm.py doctor
```

If the check reports `api_key.present=false`, ask the user to configure an API key out of band. Prefer environment/config setup over passing `--api-key`, because command histories and logs may retain CLI arguments.

Payload fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `video_urls` | array of string | yes | Ordered list of input video URLs; `minItems` is `1`. Analyzed in list order. Only HTTP/HTTPS URLs are supported. Single video up to 3 hours; all inputs up to 15 hours. |
| `target_duration` | array of number | yes | Target output durations in seconds. Always an array, even for a single output (for example `[60]`). At most 5 items, each `>= 1`, no duplicates, and each must be smaller than the combined input duration. Selection targets each duration within a default tolerance of about 10%. The CLI defaults to `[60]` when the user does not provide a duration; JSON payload callers must send an array explicitly. |
| `preset` | string | recommended | Scene preset. Only `football` is supported; other values are rejected. Use `football` by default when no `preset` or `scoring_prompt` is provided. Explicit `scoring_prompt` / `analysis_prompt` override the preset defaults. |
| `scoring_prompt` | string | optional | Scoring target for the sequential-scoring strategy. With the `football` preset it can be omitted; if supplied, it overrides the preset scoring scene. |
| `analysis_prompt` | string | optional | Extra information-capture requirement for the analysis stage. With a preset it can be omitted; if supplied, it overrides the preset analysis requirement. |
| `callback_url` | string | optional | Callback URL invoked when the task completes. |
| `callback_args` | string | optional | Business value passed through to the callback. |
| `client_token` | string | recommended | Idempotency token, max 64 chars. Use a new token for a forced rerun. |

At least one of `preset` or `scoring_prompt` is required. The script defaults `preset` to `football` only when both are absent. It does not inject a default `scoring_prompt` or `analysis_prompt`. This tool does not support `story_prompt` or `background_music_urls`; the script rejects them.

## Query

Endpoint:

```text
GET https://mediakit.ap-southeast-1.bytepluses.com/api/v1/tasks/<task_id>
```

The submit response returns a task ID shaped like:

```text
amk-tool-video-highlights-llm-000000000000
```

When successful, the final result includes:

| Field | Type | Notes |
| --- | --- | --- |
| `duration` | number | Combined actual duration of all output reels in seconds; this is also the metering/billing basis. |
| `outputs` | array | Per-output results, in the same order as the request `target_duration`. |
| `outputs[].index` | number | Output index, starting at 0, matching the order of the request `target_duration` array. |
| `outputs[].target_duration` | number | Target output duration for this entry, in seconds. |
| `outputs[].duration` | number | Actual output duration for this entry, in seconds. |
| `outputs[].video_url` | string | Signed MP4 download URL for this highlight reel. |

The query behavior mirrors the intent of `mediakit-cli shared query-task --task-id <task_id>` for this tool.
