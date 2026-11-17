# AIDSO Human Video Generator Reference

## Endpoints

Use the production endpoints for all account binding and generation operations:

```http
GET https://api.aidso.com/openapi/skills/generate_code
GET https://api.aidso.com/openapi/skills/get_by_code?code=<code>
POST https://api.aidso.com/openapi/skills/submit_text_extract_task
GET  https://api.aidso.com/openapi/skills/get_text_extract_result?taskId=<taskId>
POST https://api.aidso.com/openapi/skills/gen_digital_human_video
GET  https://api.aidso.com/openapi/skills/get_digital_human_video_result?taskId=<taskId>
```

Do not switch business requests to a test, staging, or custom base URL.

## Account Binding

Authorization is runtime-only. Installing this skill must not inspect local binding files; installation summaries should present authorization as a first-use runtime step.

Before generating an authorization link, select and probe a writable local binding path. The default path is `./.aidso/credentials.json` under the current working directory. If that path is not writable, try the installed skill directory, then a temporary runtime path. This prevents a successful authorization from being lost because the save location is blocked by an agent sandbox.

Run authorization in two separate commands:

```bash
python scripts/auth.py --start
# After the user opens the link and approves access:
python scripts/auth.py --complete
```

`--start` calls `generate_code`, stores pending state locally with mode `0600`, prints a fresh `authorization_url`, and exits immediately. Return that exact URL to the user at once. The link expires after about 10 minutes.

`python scripts/auth.py --status` checks local binding state without printing the credential. It reports `bound_locally`, `pending`, `expired`, or `not_bound`; it does not verify whether a stored credential is still valid on the server.

The authorization page is a JavaScript single-page application. Do not fetch, pre-open, inspect, or validate it with a plain HTTP client. An HTTP 200 response only confirms delivery of the application shell. The user must open the URL in a JavaScript-enabled browser.

The page rejects links whose `now` parameter is in the future according to the browser clock or older than 10 minutes. The script refreshes this parameter against local time with a small safety offset before returning the URL. If the page still reports an invalid request, generate a new link with `--start` and send it immediately; do not reuse the old URL.

`generate_code` returns `code: 200` and `data` as a full authorization URL. The script parses the `code` query parameter and never presents the standalone code to the user.

`get_by_code` returns:

```json
{"code":300,"msg":"authorization pending"}
```

while the user has not approved the link. After approval it returns:

```json
{"code":200,"msg":"success","data":"<api_key>"}
```

Call `--complete` only after the user confirms approval. If the response is still pending, keep the same unexpired link and ask the user to finish approval. On success, atomically store the returned authorization credential locally with mode `0600` at the selected writable binding path, unless `AIDSO_CREDENTIALS_FILE` overrides the path. Do not ask the user to paste keys in chat, do not import keys directly, and do not print or summarize keys in install, status, or completion output.

## Credential Resolution

Resolve authorization in this order:

1. Local binding file created by this skill's authorization flow.
2. Interactive authorization-link flow.

The local credentials file format is:

```json
{
  "api_key": "<credential returned by AIDSO after user approval>",
  "created_at": "2026-07-13T00:00:00+00:00"
}
```

## Text Extraction

Submit a benchmark-video text extraction task:

```json
{
  "url": "https://www.douyin.com/jingxuan?modal_id=7654800977366715698"
}
```

Success response:

```json
{
  "code": 200,
  "msg": "success",
  "data": "e5c12851-5aa6-4548-98e8-eab7a4184c62"
}
```

Poll with the returned task id. Use `data.status_message` to judge progress. A successful result includes `data.text` and `data.video_info`.

After extraction succeeds, return `data.text` to the user as the source script and stop. Do not automatically rewrite. Ask the user to choose:

- Use as-is: generate video with the extracted text.
- User edits: wait for the user to provide revised text.
- Rewrite: collect rewrite requirements, then rewrite with the model.

Only continue to video configuration after the user confirms the final script.

## Original Script

For original generation, ask the user directly for the video script and use it as provided. Brand knowledge, product facts, audience, tone, and copywriting requirements are not required inputs. Edit or rewrite the script only when the user asks.

## Video Generation Request

For preview selection, show only `预览`. Do not append a point-consumption note and do not discuss preview point usage in the preview result.

Before full generation, run `scripts/submit_video.py --estimate-only` with the exact final text. Read `required_points`, then tell the user only: `正式生成预计消耗 {required_points} 积分，是否确认提交？`

Do not expose the point formula, source text length, rounding method, arithmetic, or calculation process. `scripts/submit_video.py` requires `--confirm-points <points>` before it creates a full generation task. If confirmation is missing, it returns only the estimated points and exits without submission.

Submit:

```json
{
  "text": "哇哈哈哈 冲姐 我了个DJ 你可知 山有情 曲有义...",
  "desc": "商务男主播，稳重专业",
  "subtitle": "on",
  "aspect_ratio": "Portrait"
}
```

Fields:

- `text`: final script text to generate the digital-human video.
- `desc`: digital-human description, such as character type, age impression, clothing, temperament, or style. Do not require body framing, camera distance, or pose details.
- `subtitle`: `on` or `off`.
- `aspect_ratio`: fixed to `Portrait`; it is not user-configurable.

For preview, send `text` as `测试`. The script supports `--preview` to enforce this.

Success response:

```json
{
  "code": 200,
  "msg": "success",
  "data": "a562665671304e29b1f378b65b5d9cd9"
}
```

Return the `data` value to the user as `taskId`, so they can manually query the result if polling fails.

## Polling Video Result

Query with `taskId`. Success returns:

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "status": "success",
    "msg": "视频生成成功",
    "video_url": "https://...",
    "preview_url": "https://..."
  }
}
```

Use `code` and `msg` to judge request-level success or failure. Use `data.status` and `data.msg` to judge task-level state. Return only `video_url` and `preview_url` when generation succeeds.

## Script Examples

Bind an account:

```bash
python scripts/auth.py --start
python scripts/auth.py --complete
```

Extract benchmark text:

```bash
python scripts/submit_text_extract.py --url "https://www.douyin.com/jingxuan?modal_id=7654800977366715698"
python scripts/poll_text_extract.py --task-id <extract-task-id>
```

Submit a preview video:

```bash
python scripts/submit_video.py \
  --preview \
  --desc "商务男主播，稳重专业" \
  --subtitle on
```

Submit a full video:

```bash
python scripts/submit_video.py \
  --text "final script text" \
  --desc "商务男主播，稳重专业" \
  --subtitle on \
  --confirm-points <confirmed-points>
```

Poll a video task:

```bash
python scripts/poll_video.py --task-id a562665671304e29b1f378b65b5d9cd9
```
