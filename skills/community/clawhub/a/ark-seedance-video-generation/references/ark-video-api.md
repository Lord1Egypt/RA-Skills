# Ark Video API Notes

Use this file for exact field behavior, endpoint references, and advanced request construction while continuing to execute only through `scripts/seedance-video.js`. The guidance here is intentionally agent-agnostic so it can be followed by Codex, Claude Code, Cursor, OpenClaw, or similar agents.

## Official Endpoints

- Create task: `POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`
- Get task: `GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}`
- List tasks: `GET https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks?page_num={page_num}&page_size={page_size}&filter.status={filter.status}&filter.task_ids={filter.task_ids}&filter.model={filter.model}`
- Delete task: `DELETE https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{id}`

Authentication is `Authorization: Bearer $ARK_API_KEY`.

Base URL and API key guidance come from the official Ark auth documentation. Use `ARK_API_KEY`, not AK/SK.

## Official Model Example

The current Seedance 2.0 API reference page includes a sample request that uses:

- `model: "doubao-seedance-2-0-260128"`

Treat this as a representative current Seedance 2.0 model ID.

For this skill package, do not expose the full upstream model surface by default. Restrict operational choices to the approved pair in `references/video-models.json`. The SOP default is `doubao-seedance-1-0-pro-250528`, but the script itself should still require an explicit `model` value.

## Execution Policy

- Use the bundled script for all live execution.
- Do not build a second implementation in Python, Bash, or another Node.js wrapper.
- When advanced fields are needed, put them into a JSON payload file and pass that file to the bundled script.
- For concrete payload examples, also read `references/payload-patterns.md`.

## Common Input Fields

These are explicitly visible in the official API reference or sample payloads:

- `model`
- `content`
- `resolution`
- `ratio`
- `duration`
- `frames`
- `seed`
- `camera_fixed`
- `watermark`
- `callback_url`
- `return_last_frame`

The official page notes that `resolution`, `ratio`, `duration`, `frames`, `seed`, `camera_fixed`, and `watermark` use the upgraded parameter style, while still remaining backward compatible with older request forms.

The sample payload also shows that either `duration` or `frames` can be used.

## Supported Content Types

The official docs expose these `content[].type` variants:

- `text`
- `image_url`
- `video_url`
- `audio_url`
- `draft_task`

For `image_url` and `audio_url`, the docs explicitly allow:

- Public URL
- Base64 data URL
- Asset ID such as `asset://<ASSET_ID>`

The docs also mention `draft_task.id` for reusing an existing draft task.

## Output Fields

The task query API documents:

- `status`
- `content.video_url`
- `content.last_frame_url` when the create request used `return_last_frame: true`

The official text says generated video URLs and tail-frame URLs are retained for 24 hours, so download immediately.

## Status Handling

Treat these as terminal:

- `succeeded`
- `failed`
- `expired`

Polling logic should stop on any terminal state.

## Practical Guidance

- Prefer `run` in the bundled script so the video and last frame get downloaded before the 24-hour window expires.
- Use `--payload-file` whenever Seedance 2.0 introduces new fields faster than the CLI wrapper is updated.
- Keep `request.json` and `task.json` beside downloaded assets so runs are reproducible.

## Script Surface Summary

The bundled script already supports these operational surfaces:

- Default `run` flow for create + poll + download
- `create`
- `get`
- `list`
- `delete`
- `download`

The bundled script already accepts these common generation inputs:

- `--prompt`
- `--model`
- `--image-url`
- `--image-file`
- `--video-url`
- `--video-file`
- `--audio-url`
- `--audio-file`
- `--draft-task-id`
- `--resolution`
- `--ratio`
- `--duration`
- `--frames`
- `--seed`
- `--camera-fixed`
- `--watermark`
- `--return-last-frame`
- `--callback-url`
- `--payload-file`
- `--download-dir`

Use this existing surface area. Do not add or substitute another runtime path during normal skill execution.

## Official Sources

- Ark auth and base URL: https://www.volcengine.com/docs/82379/1399008
- Create video task: https://www.volcengine.com/docs/82379/1520757
- Get video task: https://www.volcengine.com/docs/82379/1521309
- List video tasks: https://www.volcengine.com/docs/82379/1521675
- Delete video task: https://www.volcengine.com/docs/82379/1521720
