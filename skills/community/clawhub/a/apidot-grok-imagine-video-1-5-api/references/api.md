# APIDot Grok Imagine Video 1.5 Reference

This reference gives agents a safer, non-executable summary for APIDot Grok Imagine Video 1.5 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/grok-imagine-video-1-5
- API docs: https://apidot.ai/docs/grok-imagine-video-1-5
- Broader Grok Imagine model page: https://apidot.ai/models/grok-imagine
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Grok Imagine Video 1.5 on APIDot is for xAI image-to-video workflows that animate a reference image into a short prompt-guided video when supported by the current APIDot request surface.

Use the broader `apidot-grok-imagine-api` skill when the user needs Grok Imagine image generation, image editing, or a mixed family overview. Use this skill when the request is specifically about Grok Imagine Video 1.5 or its image-to-video flow.

## Request Planning

Before choosing a request shape, identify:

- Whether the user has one suitable reference image URL.
- What motion, subject behavior, or camera language the prompt should guide.
- Desired duration and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source image references, request status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Grok Imagine Video 1.5 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on reference images.
- Keep request status, selected model, prompt metadata, source media references, and final video URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Grok Imagine Video 1.5.
