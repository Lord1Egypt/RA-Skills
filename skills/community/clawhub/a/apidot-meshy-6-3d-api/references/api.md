# APIDot Meshy 6 Reference

This reference gives agents a safer, non-executable summary for APIDot Meshy 6 3D integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no shell commands, no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/meshy-6-3d
- 3D models: https://apidot.ai/models/3d
- API docs: https://apidot.ai/docs/meshy-6-3d
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Meshy 6 on APIDot is for 3D asset generation workflows that need text-to-3D, image-to-3D, multi-image-to-3D, generated asset pipelines, and production async handling when supported by the selected request mode.

Do not assume every 3D request mode is supported by every Meshy 6 model entry. Check the APIDot Meshy 6 docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants text-to-3D, image-to-3D, multi-image-to-3D, or a generated asset pipeline.
- Whether source images or multiple references are involved, and whether the selected Meshy 6 mode supports them.
- Desired output format, quality, or asset handling constraints, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, source media references, request status, and final 3D asset URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Meshy 6 jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible assets.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source image URLs before submitting jobs that depend on references.
- Keep request status, selected model, prompt metadata, media references, and final 3D asset URLs together.
- Retry transient network failures with backoff. Do not retry invalid payloads unchanged.
- Avoid logging private prompts, private source image URLs, callback URLs, API keys, or generated asset URLs.
- Do not copy fields from another 3D model family unless the APIDot docs show the same field for Meshy 6.
