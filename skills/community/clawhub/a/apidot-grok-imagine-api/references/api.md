# APIDot Grok Imagine Reference

This reference gives agents a safer, non-executable summary for APIDot Grok Imagine integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/grok-imagine
- Grok Imagine docs: https://apidot.ai/docs/grok-imagine
- Grok Imagine Video 1.5 docs: https://apidot.ai/docs/grok-imagine-video-1-5
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Grok Imagine on APIDot covers image generation, image editing, text-to-video, and image-to-video workflows when supported by the selected model entry and request mode.

Do not assume every image or video request mode is supported by every Grok Imagine model entry. Check the APIDot Grok Imagine docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants image generation, image editing, text-to-video, image-to-video, or a mixed media workflow.
- Whether source images or reference media are involved, and whether the selected Grok Imagine mode supports them.
- Desired aspect ratio, duration, quality, or resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, source media references, request status, and final result URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Grok Imagine jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source media URLs before submitting jobs that depend on image or video references.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated result URLs.
- Do not copy fields from another media model family unless the APIDot docs show the same field for Grok Imagine.
