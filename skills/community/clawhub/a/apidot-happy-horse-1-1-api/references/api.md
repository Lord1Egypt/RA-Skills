# APIDot Happy Horse 1.1 Reference

Use this non-executable reference to choose the right APIDot documentation path and Happy Horse 1.1 request mode before implementation.

It contains no shell commands, runnable request examples, bundled clients, or stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/happy-horse-1-1
- API docs: https://apidot.ai/docs/happy-horse-1-1
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- General examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, request fields, limits, and commercial terms.

## Model Family

Happy Horse 1.1 on APIDot supports short video generation from a prompt, one source image, or reference images. Use the current docs to choose among text-to-video, image-to-video, and reference-to-video.

Do not assume fields from the earlier Happy Horse entry or another video model are valid for Happy Horse 1.1.

## Request Planning

Before planning a request, identify:

- Whether the user needs text-to-video, image-to-video, or reference-to-video.
- Whether source images or multiple reference images are involved.
- Desired resolution and duration when the current docs expose those controls.
- Whether polling is sufficient for testing or webhook delivery is needed for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

Open the live APIDot docs for copyable request shapes instead of recreating them inside this skill.

## Async Flow

1. Choose the Happy Horse 1.1 request mode in the live docs.
2. Submit through the documented APIDot generation flow.
3. Store `data.task_id` before retries, page transitions, or status checks.
4. Poll status for local tests and debugging.
5. Use `callback_url` for production jobs that may outlive the current browser session.
6. Treat webhook delivery as idempotent.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submission.
- Keep request status, selected model, prompt metadata, media references, and final URLs together.
- Retry transient failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, media URLs, callback URLs, API keys, or generated video URLs.
