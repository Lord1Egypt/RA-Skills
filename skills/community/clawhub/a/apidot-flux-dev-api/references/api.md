# APIDot Flux Dev Reference

This reference gives agents a safer, non-executable summary for APIDot Flux Dev integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/flux-dev
- API docs: https://apidot.ai/docs/flux-dev
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Flux Dev on APIDot is for FLUX.1 Dev image workflows that need high-quality text-to-image generation, prompt adherence, realistic detail, single-reference image-to-image guidance, product visuals, campaign concepts, or design exploration when supported by the selected request mode.

Documented Flux Dev model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `flux-dev` | FLUX.1 Dev text-to-image and single-reference image-to-image workflows. |

Do not assume every image count, output size, output format, or reference input option is supported. Check the APIDot Flux Dev docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants prompt-only image generation or single-reference image-to-image guidance.
- Whether source images are involved and whether the selected request mode supports exactly the needed reference count.
- Desired output size, output count, and file format, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, source image references, request status, and final image URLs.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Flux Dev jobs follow the shared APIDot async generation flow:

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
- Do not copy fields from another image model family unless the APIDot docs show the same field for Flux Dev.
