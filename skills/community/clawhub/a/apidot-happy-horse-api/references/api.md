# APIDot Happy Horse Reference

This reference gives agents a safer, non-executable summary for APIDot Happy Horse integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or GitHub examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/happy-horse
- API docs: https://apidot.ai/docs/happy-horse
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Model examples: https://github.com/APIDotAI/happy-horse-api
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Happy Horse on APIDot is for Alibaba Happy Horse video generation workflows that need text-to-video, image-to-video, reference-to-video, video editing, source media guidance, and production async handling when supported by the selected request mode.

Happy Horse request modes may include:

| Request Mode | Best Fit |
| --- | --- |
| Text-to-video | Prompt-driven video generation without source media. |
| Image-to-video | Video generation from one or more source images. |
| Reference-to-video | Video generation guided by reference media when the current docs support it. |
| Video editing | Transforming or editing existing video inputs when the current docs support it. |

Do not assume every request mode is supported by every model entry. Check the APIDot Happy Horse docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video, image-to-video, reference-to-video, or video editing.
- Whether source images, reference images, or source video clips are involved.
- Desired aspect ratio, duration, and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, request status, and final video URLs.

For copyable request shapes, open the APIDot docs or the Happy Horse GitHub examples instead of recreating examples inside this skill.

## Async Flow

APIDot Happy Horse jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source media URLs before submitting jobs that depend on images or video inputs.
- Keep request status, selected model, prompt metadata, media references, and final video URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Happy Horse.
