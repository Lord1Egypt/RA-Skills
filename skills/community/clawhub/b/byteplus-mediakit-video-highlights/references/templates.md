# Request Templates

These templates are for constructing API payloads or user-facing examples. The script does not inject a default `scoring_prompt` or `analysis_prompt`; use `preset=football` for the normal built-in scene, `scoring_prompt` for custom scoring, and `analysis_prompt` only as an optional analysis enhancement. Only `football` is supported for `preset`, and `story_prompt` / `background_music_urls` are not supported.

`video_urls` and `target_duration` are both arrays, so the CLI flags take JSON arrays that mirror the API fields exactly: `--video-urls '["https://example.com/match.mp4"]'` and `--target-duration '[60]'`. Only HTTP/HTTPS URLs are supported. Scalar fields such as `--preset` take a single value.

## Default Football Submit

Use this shape when the user wants ordinary football highlights and has not provided custom prompt text:

```json
{
  "video_urls": ["https://example.com/match.mp4"],
  "preset": "football",
  "target_duration": [60],
  "callback_args": "football-highlight-demo",
  "client_token": "unique-token"
}
```

The script submits this payload without adding `scoring_prompt` or `analysis_prompt`.

## Multiple Videos and Output Durations

Both `video_urls` and `target_duration` are arrays, so one task can take several input videos and produce several reels. List the videos in order, and up to 5 unique output durations in seconds:

```json
{
  "video_urls": [
    "https://example.com/first.mp4",
    "https://example.com/second.mp4"
  ],
  "preset": "football",
  "target_duration": [60, 90],
  "callback_args": "football-highlight-multi",
  "client_token": "unique-token"
}
```

The response `outputs[]` array is returned in the same order as this `target_duration` array.

Equivalent CLI invocation (the array fields take JSON arrays):

```bash
python3 scripts/video_highlights_llm.py submit \
  --video-urls '["https://example.com/first.mp4", "https://example.com/second.mp4"]' \
  --preset football \
  --target-duration '[60, 90]' \
  --callback-args "football-highlight-multi"
```

## Custom Prompt Override

Use this shape when the user asks to bias the football edit toward specific events or teams. `scoring_prompt` overrides the preset scoring scene; `analysis_prompt` only enhances analysis:

```json
{
  "video_urls": ["https://example.com/match.mp4"],
  "preset": "football",
  "target_duration": [60],
  "scoring_prompt": "Prioritize confirmed goals, key saves, shots off the woodwork, and sustained penalty-box pressure. Raise scores for Team A attacks.",
  "analysis_prompt": "Also record score bug changes, match clock, team names, and visible player numbers.",
  "client_token": "unique-token"
}
```

## Internal Environment Command

The default environment is production. To target an internal environment, set the header values yourself via the dedicated environment variables `BYTEPLUS_MEDIAKIT_USE_PPE` (sets `x-use-ppe`) and `BYTEPLUS_MEDIAKIT_TT_ENV` (sets `x-tt-env`). Use the environment name provided by your environment owner:

```bash
export BYTEPLUS_MEDIAKIT_USE_PPE="1"
export BYTEPLUS_MEDIAKIT_TT_ENV="<environment name>"
python3 scripts/video_highlights_llm.py submit \
  --video-urls '["https://example.com/match.mp4"]' \
  --preset football \
  --target-duration '[60]' \
  --callback-args "football-highlight-eval"
```

`--header` (repeatable) and `BYTEPLUS_MEDIAKIT_HEADERS` (a JSON object) can override any header if you need finer control.

Run preflight first when credentials are uncertain:

```bash
python3 scripts/video_highlights_llm.py doctor
```

## Query

```bash
python3 scripts/video_highlights_llm.py query \
  --task-id "amk-tool-video-highlights-llm-000000000000"
```

## Trigger Examples

Positive examples:

- "Create a one minute football highlight reel from https://example.com/match-001.mp4, prioritizing goals and key saves."
- "Create a 90 second football highlight reel from https://example.com/match-002.mp4, prioritizing goals, saves, and penalty-box pressure."
- "Check whether task amk-tool-video-highlights-llm-000000000000 has completed."

Negative examples:

- "Recognize the video's speech and export an SRT file." This is ASR/subtitle extraction, not highlight editing.
- "Trim the intro and outro, then composite a background image." This is deterministic video editing, not LLM highlight selection.
