# APIDot Kling 2.1 Reference

This reference gives agents a safer, non-executable summary for APIDot Kling 2.1 integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general APIDot examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/kling-2-1
- API docs: https://apidot.ai/docs/kling-2-1
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Kling 2.1 on APIDot is for image-to-video workflows that need source-image guidance, controlled motion, optional end-frame planning, and short-form video output when supported by the selected model mode.

Documented Kling 2.1 model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `kling-2.1/standard` | General image-to-video generation and lower-complexity clip iteration. |
| `kling-2.1/pro` | Higher-control image-to-video jobs when the user needs stronger motion or final-frame planning. |

Do not assume every request mode is supported by every model entry. Check the APIDot Kling 2.1 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user has one start image or also needs end-frame guidance.
- Whether the clip needs simple motion, character movement, camera movement, or a transition between frames.
- Desired duration, output mode, and model variant, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, source media references, status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Kling 2.1 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate source image URLs before submitting jobs that depend on image guidance.
- Keep request status, selected model, prompt metadata, media references, and final result URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another video model family unless the APIDot docs show the same field for Kling 2.1.
