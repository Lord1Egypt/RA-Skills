# APIDot Seedance 1.5 Pro Reference

This reference gives agents a safer, non-executable summary for APIDot Seedance 1.5 Pro integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/seedance-1-5-pro
- API docs: https://apidot.ai/docs/seedance-1-5-pro
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Seedance 1.5 Pro on APIDot is for cinematic short-form video workflows that need prompt-driven clips, image guidance, synchronized audio planning, first/last-frame control, fixed-camera behavior, and compact campaign or storyboard output.

The documented APIDot model entry is:

| Model Entry | Best Fit |
| --- | --- |
| `seedance-1.5-pro` | Seedance 1.5 Pro text-to-video and image-to-video jobs through APIDot. |

Do not assume Seedance 2 fields apply to Seedance 1.5 Pro. Check the APIDot Seedance 1.5 Pro docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-video, image-to-video, or first/last-frame control.
- Whether synchronized audio or fixed-camera behavior is part of the desired output.
- Whether the workflow depends on one or more source image URLs.
- Desired duration and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Seedance 1.5 Pro jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on frame guidance.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Seedance 1.5 Pro.
