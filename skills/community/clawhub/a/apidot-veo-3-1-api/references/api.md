# APIDot Veo 3.1 Reference

This reference gives agents a safer, non-executable summary for APIDot Veo 3.1 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or runnable GitHub examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/veo-3-1
- API docs: https://apidot.ai/docs/veo-3-1
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Runnable examples: https://github.com/APIDotAI/veo-3.1-api
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Veo 3.1 on APIDot is for short video generation workflows that need text prompts, frame guidance, reference images, cinematic camera language, and synchronized audio behavior when supported by the selected model mode.

Documented Veo 3.1 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `veo3.1-lite` | Text-only iteration and lower-friction prompt testing. |
| `veo3.1-fast` | Text, frame-guided, or reference-image video workflows. |
| `veo3.1-quality` | Higher-quality text or frame-guided video workflows. |

Do not assume every request mode is supported by every model entry. Check the APIDot Veo 3.1 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video, image-to-video, frame-guided video, or reference-image video.
- Whether a source image, first frame, last frame, or reference image is involved.
- Desired aspect ratio, duration, and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

For copyable request shapes, open the APIDot docs or the Veo 3.1 GitHub examples instead of recreating examples inside this skill.

## Async Flow

APIDot Veo 3.1 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source media URLs before submitting jobs that depend on images.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Veo 3.1.
