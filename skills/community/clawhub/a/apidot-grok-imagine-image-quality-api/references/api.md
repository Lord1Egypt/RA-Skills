# APIDot Grok Imagine Image Quality Reference

This reference gives agents a safer, non-executable summary for APIDot Grok Imagine Image Quality integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/grok-imagine-image-quality
- API docs: https://apidot.ai/docs/grok-imagine-image-quality
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Grok Imagine Image Quality on APIDot is for high-fidelity still image workflows that need stronger detail, readable text, polished lighting, reference-guided editing, product visuals, ad concepts, posters, or UI-style graphics when supported by the selected request mode.

Documented Grok Imagine Image Quality model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `grok-imagine-image-quality` | Quality-focused still image generation and reference-guided image editing. |

Do not assume every image count, aspect ratio, output format, or resolution option is supported. Check the APIDot Grok Imagine Image Quality docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants prompt-only image generation or reference-guided editing.
- Whether the desired result needs 1K lower-cost output or 2K higher-detail output according to the current docs.
- Whether source images are involved and whether the selected request mode supports the number of references.
- Desired aspect ratio, output count, and file format, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, source image references, request status, and final image URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Grok Imagine Image Quality jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Validate all source image URLs before submitting jobs that depend on reference images.
- Keep request status, selected model, prompt metadata, image references, and final image URLs together.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging private prompts, private image URLs, callback URLs, API keys, generated image URLs, or task IDs.
- Do not copy fields from another image model family unless the APIDot docs show the same field for Grok Imagine Image Quality.
