# APIDot Kling Avatar 2.0 Reference

Use this non-executable reference to choose the current APIDot documentation path and plan Kling Avatar 2.0 inputs before implementation.

It contains no shell commands, runnable request examples, bundled clients, or stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/kling-avatar-2-0
- API docs: https://apidot.ai/docs/kling-avatar-2-0
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- General examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model IDs, media limits, request fields, availability, and commercial terms.

## Model Family

Kling Avatar 2.0 on APIDot creates a talking-avatar video from one reference image and one speech audio track. The current APIDot surface provides Standard and Pro variants and may accept optional performance direction.

Use separate workflows for speech synthesis, multiple characters, multiple audio tracks, or unrelated video-generation tasks.

## Request Planning

Before planning a request, identify:

- Whether Standard or Pro is appropriate for the current goal.
- The single reference image that defines the avatar.
- The speech audio source that drives timing and delivery.
- Optional direction for emotion, gesture, camera feel, or speaking style.
- Whether polling is sufficient for testing or webhook delivery is needed for production.
- Where the backend will persist `task_id`, selected model, media references, status, and final video URL.

Open the live APIDot docs for exact media validation rules and copyable request shapes.

## Async Flow

1. Select the current Kling Avatar 2.0 model variant in the live docs.
2. Validate the reference image and speech audio sources.
3. Submit through the documented APIDot generation flow.
4. Store `data.task_id` before retries, page transitions, or status checks.
5. Poll status for local tests and use `callback_url` for production jobs.
6. Treat webhook delivery as idempotent.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate both media URLs before submission.
- Keep request status, model variant, media references, direction metadata, and final URL together.
- Retry transient failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private media URLs, prompts, callback URLs, API keys, or generated video URLs.
