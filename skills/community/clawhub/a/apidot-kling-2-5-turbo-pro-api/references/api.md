# APIDot Kling 2.5 Turbo Pro Reference

This reference gives agents a safer, non-executable summary for APIDot Kling 2.5 Turbo Pro integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/kling-2-5-turbo-pro
- API docs: https://apidot.ai/docs/kling-2-5-turbo-pro
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Kling 2.5 Turbo Pro on APIDot is for prompt-only, start-frame-guided, and start-and-end-frame-guided short video workflows when supported by the selected request mode.

This is a focused Kling 2.5 Turbo Pro skill. Use later Kling-family skills when the user asks for Kling 2.6, Kling O3, Kling 3.0, or motion-control-specific workflows.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants prompt-only text-to-video, start-frame guidance, or start-and-end-frame guidance.
- Whether the workflow depends on one or two source image URLs.
- Desired duration, resolution, aspect ratio, or camera language, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, request status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Kling 2.5 Turbo Pro jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on frame guidance.
- Keep request status, selected model, prompt metadata, media references, and final video URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Kling 2.5 Turbo Pro.
