---
name: freebeat-mcp-workflows
description: Generate AI music videos from any MCP client. Turn text prompts into cinematic music videos with multiple styles and modes. Existing features include character consistency, lip-sync, one-click generation, and special effects. Run Freebeat MCP creative workflows for effect and music video generation, including upload, parameter validation, async task polling, and result retrieval. Use when the user mentions Freebeat MCP, generate_effect, generate_music_video, list_effects, upload_audio, upload_image, get_task_status, or get_task_result.
---

# Freebeat MCP Workflows

Use this skill for reliable Freebeat MCP task execution with correct tool order and async handling.

## Quick Start

1. Confirm the user goal:
   - `generate_effect` (template-based effect generation)
   - `generate_music_video` (MV generation from uploaded audio)
2. Gather required inputs.
3. Execute the correct workflow.
4. Poll task status until terminal state.
5. Fetch result only after completion.

## Tool Map

- `upload_audio`: Upload local audio or import from URL. Returns `music_id`.
- `upload_image`: Upload one or two images. Returns `image_urls`.
- `list_effects`: Discover templates and defaults for effect generation.
- `generate_effect`: Start async effect generation task.
- `generate_music_video`: Start async MV generation task.
- `get_task_status`: Poll async task state.
- `get_task_result`: Fetch output only when status is `completed`.

## Workflow A: Generate Effect

Preferred order:

1. Call `list_effects`.
2. Select `effect_id` and collect defaults:
   - `default_music_id`
   - `image_url` (default image)
3. Optional overrides:
   - If user provides custom music, call `upload_audio` and use returned `music_id`.
   - If user provides custom image, call `upload_image` with one image and use `image_urls[0]`.
4. Call `generate_effect` with:
   - `effect_id` (required)
   - `music_id` (required)
   - `prompt` (required, trimmed length 1..2000)
   - `reference_image_urls` (required, exactly one URL)
   - `watermark` (optional, default `false`)
5. Poll with `get_task_status` until `completed` or `failed`.
6. On `completed`, call `get_task_result` and return `video_url` and `cover_url`.

## Workflow B: Generate Music Video

Preferred order:

1. Call `upload_audio` first and capture `music_id`.
2. Optional image references:
   - Call `upload_image` and pass returned `image_urls` to `generate_music_video.reference_image_urls`.
3. Call `generate_music_video` with:
   - `music_id` (required)
   - `prompt` (required, trimmed length 1..2000)
   - Optional: `mv_type`, `style`, `aspect_ratio`, `resolution`, `watermark`, `start_ms`, `end_ms`, `reference_image_urls`
4. Poll with `get_task_status` until terminal state.
5. On `completed`, call `get_task_result` and return `video_url` and `cover_url`.

## Async Handling Rules

- Treat task submission as asynchronous.
- Continue polling while status indicates in-progress work (for example `pending`).
- Status values may be lowercase (`pending`, `completed`, `failed`) and some older systems may use uppercase variants.
- Do not call `get_task_result` before status is `completed`.
- If `get_task_result` returns `TASK_NOT_COMPLETED`, continue polling.
- On `failed`, report `error_message`, `error_code`, and any backend message from status response.

## Input Validation Checklist

Before generation calls, verify:

- Prompt is present and trimmed length is within `1..2000`.
- For `generate_effect`, `reference_image_urls` contains exactly one image URL.
- For `generate_effect`, `music_id` is either `default_music_id` from `list_effects` or from `upload_audio`.
- For `generate_music_video`, `music_id` comes from `upload_audio`.
- For `upload_audio`, provide exactly one of `file_path` or `url`.

## Response Format Guidelines

When reporting progress or final outputs, include:

- Task type (`effect_generation` or `music_video_generation`)
- `task_id`
- Current status
- On completion: `video_url` and `cover_url`
- On failure: failure code/message and next fix step

## Defaults and Practical Guidance

- Use `list_effects` defaults unless the user explicitly asks to override.
- For effect generation, default image is `list_effects.image_url`.
- For MV generation, default values are acceptable unless user specifies otherwise.
- Keep polling cadence steady and avoid tight loops.

## Example Decision Logic

If user asks "make an effect from template":
- Use Workflow A.

If user asks "make a music video from this song":
- Use Workflow B.

If user provides only a prompt without media:
- For effect: use `list_effects` defaults.
- For MV: request audio input (or URL) and run `upload_audio` first.

