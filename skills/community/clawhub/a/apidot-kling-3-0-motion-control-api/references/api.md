# APIDot Kling 3.0 Motion Control Reference

This reference gives agents a safer, non-executable summary for APIDot Kling 3.0 Motion Control integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/kling-3-0-motion-control
- API docs: https://apidot.ai/docs/kling-3-0-motion-control
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Kling 3.0 Motion Control on APIDot is for motion-transfer video workflows that use a character image and a reference motion video to create controllable animation, dance transfer, action transfer, storyboard previews, or ad creative when supported by the selected request mode.

Documented Kling 3.0 Motion Control model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `kling-3.0-motion-control` | Motion transfer from a reference video onto a character image for controllable animation workflows. |

Do not assume every media input, duration, or resolution option is supported. Check the APIDot Kling 3.0 Motion Control docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants dance transfer, action transfer, character animation, storyboard preview, product motion, or ad creative.
- Which media assets are involved: character image, reference motion video, optional prompt guidance, or other source media supported by current docs.
- Desired resolution, duration, and motion fidelity controls, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, source media references, request status, and final video URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Kling 3.0 Motion Control jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source media URLs before submitting jobs that depend on character images or reference videos.
- Keep request status, selected model, prompt metadata, media references, and final video URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private media URLs, callback URLs, API keys, or generated video URLs.
- Do not copy fields from another Kling or video model family unless the APIDot docs show the same field for Kling 3.0 Motion Control.
