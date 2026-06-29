# APIDot Wan 2.5 Reference

This reference gives agents a safer, non-executable summary for APIDot Wan 2.5 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/wan-2-5
- API docs: https://apidot.ai/docs/wan-2-5
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Wan 2.5 on APIDot is for higher-quality short video workflows that need text-to-video, single-image image-to-video, optional audio text planning, controlled duration, resolution planning, product teasers, storyboard clips, or social ad drafts when supported by the selected request mode.

Documented Wan 2.5 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `wan2.5-text-to-video` | Prompt-only Wan 2.5 video generation through APIDot. |
| `wan2.5-image-to-video` | Single-image-guided Wan 2.5 video generation through APIDot. |

Do not assume every request mode is supported by every model entry. Check the APIDot Wan 2.5 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video or image-to-video.
- Whether source images or optional audio text are involved.
- Desired duration and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, source media references, request status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Wan 2.5 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on image guidance.
- Keep request status, selected model, prompt metadata, media references, and final video URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Wan 2.5.
