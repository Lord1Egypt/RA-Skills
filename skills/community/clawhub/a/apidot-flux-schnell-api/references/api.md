# APIDot Flux Schnell Reference

This reference gives agents a safer, non-executable summary for APIDot Flux Schnell integration work. Use it to choose the right documentation path and request mode before opening the live APIDot docs or general examples.

It contains no runnable request examples, no bundled clients, and no stored credentials.

## Source Of Truth

- Model page: https://apidot.ai/models/flux-schnell
- API docs: https://apidot.ai/docs/flux-schnell
- Quickstart: https://apidot.ai/docs/quickstart
- Webhooks: https://apidot.ai/docs/webhooks
- Main examples: https://github.com/APIDotAI/apidot-examples

Use the live APIDot docs for current model availability, supported fields, limits, and commercial terms.

## Model Family

Flux Schnell on APIDot is for FLUX.1 Schnell image workflows that need fast, low-cost text-to-image drafts, prompt exploration, batch creative iteration, or early concept generation before moving to a heavier image model.

Documented Flux Schnell model entries include:

| Model Entry | Best Fit |
| --- | --- |
| `flux-schnell` | Fast FLUX.1 Schnell text-to-image drafts and prompt exploration. |

Do not assume every image count, output size, output format, or reference input option is supported. Check the APIDot Flux Schnell docs before preparing a payload.

## Request Planning

Before choosing a request shape, identify:

- Whether the user wants fast prompt-only image drafts or a higher-fidelity model instead.
- Desired output size, file format, and iteration volume, if the current APIDot docs expose those controls.
- Whether the workflow should use polling for local testing or webhook delivery for production.
- Where the backend will persist `task_id`, selected model, user ID, prompt metadata, request status, and final image URLs.
- Whether generated URLs, prompts, or callback URLs contain private customer or campaign data.

For copyable request shapes, open the APIDot docs or general APIDot examples instead of recreating examples inside this skill.

## Async Flow

APIDot Flux Schnell jobs follow the shared APIDot async generation flow:

1. Choose the model entry and request mode from the live APIDot docs.
2. Submit the job through the documented APIDot generation submit flow.
3. Store `data.task_id` before any retry, page transition, or status check.
4. Use task status polling for local tests and debugging.
5. Use `callback_url` webhook delivery for production jobs that may outlive the current browser session.
6. Treat webhook handlers as idempotent because duplicate delivery should not create duplicate visible results.

## Implementation Notes

- Keep `APIDOT_API_KEY` server-side only.
- Keep request status, selected model, prompt metadata, and final image URLs together.
- Retry transient network failures with backoff. Do not retry invalid requests unchanged.
- Avoid logging private prompts, callback URLs, API keys, generated image URLs, or task IDs.
- Do not copy fields from another image model family unless the APIDot docs show the same field for Flux Schnell.
