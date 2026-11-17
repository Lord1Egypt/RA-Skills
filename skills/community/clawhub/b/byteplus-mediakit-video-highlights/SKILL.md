---
name: byteplus-mediakit-video-highlights
description: Create and query BytePlus/MediaKit video highlight editing tasks with the video-highlights-llm tool, focused on preset-based football highlight reels. Use when the user asks to generate, submit, or query highlight edits from one or more HTTP/HTTPS video URLs, optionally with preset (football), scoring_prompt, analysis_prompt, callbacks, or one or more target durations.
---

# BytePlus MediaKit Video Highlights

## Overview

Submit BytePlus MediaKit `video-highlights-llm` jobs and query their async results. Default to `preset=football` and `target_duration=[60]` when the user does not provide `preset` or `scoring_prompt`. Respect the API limits: one input video up to 3 hours, all input videos up to 15 hours.

## Workflow

1. Parse the user's request into task inputs:
   - `video_urls`: required; collect at least one HTTP/HTTPS media URL in order. Only HTTP/HTTPS URLs are supported. Supported common formats include mp4, flv, ts, avi, mov, wmv, and mkv.
   - `target_duration`: required array of output durations in seconds. Always an array, even for a single output (for example `[60]`). At most 5 values, each `>= 1`, no duplicates, and each smaller than the combined input duration. The CLI defaults to `[60]` when absent.
   - `preset`: only `football` is supported. Default to `football` when the user provides no `preset` or `scoring_prompt` (other values are rejected).
   - `scoring_prompt`: optional scoring override. If supplied with `preset`, it overrides the preset's scoring scene.
   - `analysis_prompt`: optional analysis enhancement. It does not replace `preset` or `scoring_prompt`.
   - Optional: `callback_url`, `callback_args`, `client_token`.
2. Run `scripts/video_highlights_llm.py doctor` before the first real submit/query in a session, or whenever credentials/environment are uncertain. Do not ask the user to paste an API key into chat.
3. If no usable video material is present, ask the user for real video material before submitting. Accept one or more HTTP/HTTPS video URLs.
4. Submit the task with `scripts/video_highlights_llm.py submit`.
5. Capture the returned `task_id`, usually shaped like `amk-tool-video-highlights-llm-...`.
6. Query the task later with `scripts/video_highlights_llm.py query --task-id <task_id>`.
7. When a task succeeds, report the combined `duration` and each entry in `outputs[]` (`index`, `target_duration`, `duration`, `video_url`).

## Trigger Examples

Use this skill for requests like:

- "Create a 60 second football highlight reel from these two match videos, prioritizing goals and goalkeeper saves: https://..., https://..."
- "Create a 90 second football highlight reel from https://..., prioritizing goals and key saves."
- "Query the result for task amk-tool-video-highlights-llm-000000000000."

Do not use this skill for requests like:

- "Extract subtitles from this video." Use a video OCR or ASR skill instead.
- "Trim this video to the first 10 seconds and add a cover image." Use a video editing skill instead.

## Script

Use the bundled script. The CLI flags mirror the API fields exactly: array fields (`video_urls`, `target_duration`) take a JSON array, and scalar fields take a single value.

```bash
python3 scripts/video_highlights_llm.py submit \
  --video-urls '["https://example.com/match.mp4"]' \
  --preset football \
  --target-duration '[60]' \
  --callback-args "football-highlight-demo"
```

Multiple input videos and multiple output durations in one task are just longer arrays (`target_duration` allows up to 5 unique values):

```bash
python3 scripts/video_highlights_llm.py submit \
  --video-urls '["https://example.com/first.mp4", "https://example.com/second.mp4"]' \
  --preset football \
  --target-duration '[60, 90]'
```

Query:

```bash
python3 scripts/video_highlights_llm.py query \
  --task-id "amk-tool-video-highlights-llm-000000000000"
```

The script reads authentication in this order: `--api-key`, `BYTEPLUS_MEDIAKIT_API_KEY`, legacy `MEDIAKIT_API_KEY`, then `~/.mediakit/config.json`. It accepts `--endpoint` and `--header`.

Prefer `BYTEPLUS_MEDIAKIT_*` environment variables for configuration:

- `BYTEPLUS_MEDIAKIT_API_KEY`
- `BYTEPLUS_MEDIAKIT_ENDPOINT`
- `BYTEPLUS_MEDIAKIT_TT_ENV`
- `BYTEPLUS_MEDIAKIT_USE_PPE`
- `BYTEPLUS_MEDIAKIT_HEADERS`
- `BYTEPLUS_MEDIAKIT_RUNTIME`
- `BYTEPLUS_MEDIAKIT_CONFIG`

Legacy `MEDIAKIT_*` environment variables are accepted only as lower-priority fallbacks.

The default endpoint is the production environment `https://mediakit.ap-southeast-1.bytepluses.com`, and no environment-specific headers are sent by default. There is no built-in PPE profile. To target an internal environment, set the header values yourself with the dedicated environment variables `BYTEPLUS_MEDIAKIT_TT_ENV` (sets `x-tt-env`) and `BYTEPLUS_MEDIAKIT_USE_PPE` (sets `x-use-ppe`). Use the environment name provided by your environment owner. For example:

```bash
export BYTEPLUS_MEDIAKIT_USE_PPE="1"
export BYTEPLUS_MEDIAKIT_TT_ENV="<environment name>"
python3 scripts/video_highlights_llm.py submit --video-urls '["https://example.com/match.mp4"]'
```

`--header` (repeatable) and `BYTEPLUS_MEDIAKIT_HEADERS` (a JSON object) can override any header, including the two above.

Preflight:

```bash
python3 scripts/video_highlights_llm.py doctor
```

If the API key is missing, tell the user to configure it outside the chat:

```bash
export BYTEPLUS_MEDIAKIT_API_KEY="..."
```

or initialize/configure MediaKit so `~/.mediakit/config.json` contains the key. Legacy `MEDIAKIT_API_KEY` works as a fallback, but do not recommend it for new setup. Do not print, log, or ask the user to paste the raw API key into the conversation.

For complex payloads, prefer a JSON file:

```bash
python3 scripts/video_highlights_llm.py submit --request-json request.json
```

## Natural Language Parsing

Map common user wording as follows:

- "make a football highlight", "soccer highlights", "match highlights", "goal highlights" -> `preset=football` unless the user provides a custom `scoring_prompt`.
- "about one minute" -> `target_duration=[60]`.
- "90 seconds" or "one and a half minutes" -> `target_duration=[90]`.
- "give me a 60 and a 90 second cut" or "both a one-minute and 30-second version" -> `target_duration=[60, 90]` / `[60, 30]` (up to 5 unique durations in one task).
- "prefer saves / home team / player number 10" -> custom `scoring_prompt`; keep `preset=football` if the user also specified it.
- "record scoreboard / team names / player numbers" -> custom `analysis_prompt` enhancement.

Only `football` is supported for `preset`. This skill does not support `story_prompt` or `background_music_urls`; if the user asks for a non-football scene (for example basketball or short drama), a story-driven cut, or background music, tell them it is not supported.

If the user supplies only a task ID, skip submission and query that task.

## References

- Read `references/templates.md` when the user asks for JSON payload examples, prompt override templates, or evaluation request templates.
- Read `references/api.md` when changing the script or troubleshooting payload shape, status queries, or returned fields.
