# APIDot Wan 2.6 Reference

This reference gives agents a safer, non-executable summary for APIDot Wan 2.6 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/wan-2-6
- API docs: https://apidot.ai/docs/wan-2-6
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Wan 2.6 on APIDot is for short-form video generation workflows that need prompt-driven clips, single-image animation, source-video-guided generation, multi-shot structure, and selectable output planning when supported by the selected model mode.

Documented Wan 2.6 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `wan2.6-text-to-video` | Prompt-led multi-shot short clips through APIDot. |
| `wan2.6-image-to-video` | Animate a single source image with prompt guidance through APIDot. |
| `wan2.6-video-to-video` | Source-video-guided generation or restyling through APIDot. |

Do not assume every request mode is supported by every model entry. Check the APIDot Wan 2.6 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video, image-to-video, or video-to-video.
- Whether the workflow depends on one source image or source video references.
- Whether the clip needs multi-shot structure, a specific scene plan, or source-video guidance.
- Desired resolution and duration, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Wan 2.6 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image and video URLs before submitting jobs that depend on media guidance.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Wan 2.6.
