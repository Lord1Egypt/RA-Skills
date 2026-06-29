# APIDot Sora 2 Official Reference

This reference gives agents a safer, non-executable summary for APIDot Sora 2 Official integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or GitHub examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/sora-2-official
- API docs: https://apidot.ai/docs/sora-2-official
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Model examples: https://github.com/APIDotAI/sora-2-official-api
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Sora 2 Official on APIDot is for OpenAI Sora video generation workflows that need prompt-to-video, image-guided video, cinematic scene direction, and Standard or Pro routing when supported by the selected model mode.

Documented Sora 2 Official model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `sora-2-official` | Standard Sora 2 Official video generation workflows. |
| `sora-2-pro-official` | Pro Sora 2 Official workflows when the current docs expose that model entry. |

Do not assume every request mode is supported by every model entry. Check the APIDot Sora 2 Official docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants prompt-to-video, image-guided video, Standard, or Pro.
- Whether a source image is involved and whether the selected model entry supports image guidance.
- Desired aspect ratio, duration, and resolution, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, request status, and final video URLs.

For copyable request shapes, open the APIDot docs or the Sora 2 Official GitHub examples instead of recreating examples inside this skill.

## Async Flow

APIDot Sora 2 Official jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source image URLs before submitting jobs that depend on image guidance.
- Keep request status, selected model, prompt metadata, media references, and final video URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Sora 2 Official.
